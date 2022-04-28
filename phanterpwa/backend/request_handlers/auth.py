import os
import base64
import json
import re
from urllib.request import urlopen
from passlib.hash import pbkdf2_sha512
from phanterpwa.backend.decorators import (
    check_client_token,
    check_url_token,
    check_public_csrf_token,
    check_private_csrf_token,
    check_user_token,
    requires_no_authentication
)
from phanterpwa.mail import MailSender
from phanterpwa.samples import (
    email_activation_code,
    email_password,
    email_two_factor_code,
    sms_password,
    sms_two_factor_code,
    sms_activation_code
)
from phanterpwa.backend.dataforms import FieldsDALValidateDictArgs
from phanterpwa.tools import (
    humanize_seconds,
    temporary_password,
    interpolate,
    generate_activation_code,
    check_activation_code,
    user_agent_parse,
    checkbox_bool
)
from phanterpwa.backend.pydal.extra_validations import (
    PASSWORD_MATCH_WITH_HASH,
    VALID_PASSWORD
)
from phanterpwa.i18n import browser_language
from phanterpwa.third_parties.xss import xssescape as E
from phanterpwa.gallery.cutter import PhanterpwaGalleryCutter
from phanterpwa.gallery.integrationDAL import PhanterpwaGalleryUserImage
from tornado import (
    web
)
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serialize,
    BadSignature,
    SignatureExpired,
    URLSafeSerializer
)
from pydal import Field
from pydal.validators import (
    IS_EQUAL_TO,
    IS_EMAIL
)
from datetime import (
    datetime,
    timedelta
)


compiled_mobilemail = re.compile(r"^[0-9]+\.mobile@phanterpwa\.com$")


def arbritary_login(app_name, projectConfig, db, email, user_agent, remote_ip, client_token):
    _client_token = client_token
    q_user = db(db.auth_user.email == email).select().first()
    if q_user:
        timeout_token_user = projectConfig['BACKEND'][app_name]['default_time_user_token_expire_remember_me']
        t_user = Serialize(
            projectConfig['BACKEND'][app_name]['secret_key'],
            timeout_token_user
        )
        content = {
            'id': str(q_user.id),
            'email': email
        }
        token_user = t_user.dumps(content)
        token_user = token_user.decode('utf-8')
        q_role = db(
            (db.auth_membership.auth_user == q_user.id) &
            (db.auth_group.id == db.auth_membership.auth_group)
        ).select(db.auth_group.id, db.auth_group.role, orderby=db.auth_group.grade)
        roles = [x.role for x in q_role]
        dict_roles = {x.id: x.role for x in q_role}
        roles_id = [x.id for x in q_role]
        role = None
        if roles:
            role = roles[-1]
        q_user.update_record(login_attempts=0)
        t_client = Serialize(
            projectConfig['BACKEND'][app_name]['secret_key'],
            projectConfig['BACKEND'][app_name]['default_time_client_token_expire']
        )
        t_url = URLSafeSerializer(
            projectConfig['BACKEND'][app_name]["secret_key"],
            salt="url_secret_key"
        )
        r_client = db(db.client.token == _client_token).select().first()
        if r_client:
            r_client.delete_record()
        id_client = db.client.insert(auth_user=q_user.id, date_created=datetime.now())
        q_client = db(db.client.id == id_client).select().first()
        content = {
            'id_user': str(q_user.id),
            'id_client': str(id_client),
            'user_agent': user_agent,
            'remote_addr': remote_ip
        }
        token_url = t_url.dumps(content)
        token_client = t_client.dumps(content)
        token_client = token_client.decode('utf-8')
        q_client.update_record(
            token=token_client,
            date_created=datetime.now(),
            remember_me=True,
            locked=False,
        )

        if not q_user.permit_mult_login:
            r_client = db(
                (db.client.auth_user == q_user.id) &
                (db.client.token != token_client)
            ).select()
            if r_client:
                r_client = db(
                    (db.client.auth_user == q_user.id) &
                    (db.client.token != token_client)
                ).delete()
        db.commit()
        user_image = PhanterpwaGalleryUserImage(q_user.id, db, projectConfig)
        return {
            'authorization': token_user,
            'client_token': token_client,
            'url_token': token_url,
            'auth_user': {
                'id': str(q_user.id),
                'first_name': E(q_user.first_name),
                'last_name': E(q_user.last_name),
                'email': email,
                'fone_number': q_user.fone_number,
                'remember_me': q_client.remember_me,
                'roles': roles,
                'role': role,
                'dict_roles': dict_roles,
                'roles_id': roles_id,
                'activated': q_user.activated,
                'image': user_image.id_image,
                'two_factor': q_user.two_factor_login,
                'multiple_login': q_user.permit_mult_login,
                'locale': q_user.locale,
                'social_login': None
            }
        }
    else:
        return None


def arbritary_new_user(app_name, projectConfig, db, email, first_name, last_name, user_agent, remote_ip, client_token):
    _client_token = client_token 
    new_password = os.urandom(3).hex()
    password_hash = pbkdf2_sha512.hash("password{0}{1}".format(
        new_password, projectConfig['BACKEND'][app_name]['secret_key']))
    table = db.auth_user
    social_image = googleapi_user.get("picture", None)
    first_name = googleapi_user.get("given_name", "")
    last_name = googleapi_user.get("family_name", "")
    dict_arguments = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password_hash": password_hash,
        "activated": True
    }
    result = FieldsDALValidateDictArgs(
        dict_arguments,
        *[table[x] for x in table.fields if x in [
            "first_name", "last_name", "email", "password_hash"]]
    )
    r = result.validate_and_insert(db.auth_user)
    if r and r.id:
        q_user = db(db.auth_user.id == r.id).select().first()
        id_user = r.id
        if r.id == 1:
            role = "root"
            id_role = db(db.auth_group.role == 'root').select().first()
            if id_role:
                db.auth_membership.insert(auth_user=1,
                auth_group=id_role.id)
        else:
            role = "user"
            db.auth_membership.insert(auth_user=r.id, auth_group=3)
        t_user = Serialize(
            projectConfig['BACKEND'][app_name]['secret_key'],
            projectConfig['BACKEND'][app_name]['default_time_user_token_expire']
        )
        content_user = {
            'id': str(r.id),
            'email': dict_arguments['email']
        }
        token_user = t_user.dumps(content_user)
        token_user = token_user.decode('utf-8')
        token_client = _client_token
        id_client = db.client.update_or_insert(auth_user=r.id)
        t_client = Serialize(
            projectConfig['BACKEND'][app_name]['secret_key'],
            projectConfig['BACKEND'][app_name]['default_time_client_token_expire']
        )
        t_url = URLSafeSerializer(
            projectConfig['BACKEND'][app_name]["secret_key"],
            salt="url_secret_key"
        )
        content_client = {
            'id_user': str(r.id),
            'id_client': str(id_client),
            'user_agent': user_agent,
            'remote_addr': remote_ip
        }
        token_url = t_url.dumps(content_client)
        token_client = t_client.dumps(content_client)
        token_client = token_client.decode('utf-8')
        q_client = db(db.client.id == id_client).select().first()
        q_client.update_record(
            token=token_client,
            date_created=datetime.now()
        )
        r_client = db(db.client.token == _client_token).select().first()
        if r_client:
            r_client.delete_record()
        if not q_user.permit_mult_login:
            r_client = db(
                (db.client.auth_user == id_user)
                & (db.client.token != _client_token)
            ).select()
            if r_client:
                r_client = db(
                    (db.client.auth_user == id_user)
                    & (db.client.token != _client_token)
                ).remove()
        db.commit()
        q_role = db(
            (db.auth_membership.auth_user == q_user.id)
            & (db.auth_group.id == db.auth_membership.auth_group)
        ).select(
            db.auth_group.id, db.auth_group.role, orderby=db.auth_group.grade
        )
        roles = [x.role for x in q_role]
        dict_roles = {x.id: x.role for x in q_role}
        roles_id = [x.id for x in q_role]
        user_image = PhanterpwaGalleryUserImage(r.id, db, projectConfig)
        return {
            'authorization': token_user,
            'client_token': token_client,
            'url_token': token_url,
            'auth_user': {
                'id': str(q_user.id),
                'first_name': E(q_user.first_name),
                'last_name': E(q_user.last_name),
                'email': email,
                'fone_number': q_user.fone_number,
                'remember_me': q_client.remember_me,
                'roles': roles,
                'role': role,
                'dict_roles': dict_roles,
                'roles_id': roles_id,
                'activated': q_user.activated,
                'image': user_image.id_image,
                'two_factor': q_user.two_factor_login,
                'multiple_login': q_user.permit_mult_login,
                'locale': q_user.locale,
                'social_login': None
            }
        }


class Auth(web.RequestHandler):
    """
        url: '/api/auth/'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, Translator_email, SMSSender=None, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.Translator_email = Translator_email
        self.i18nTranslator = i18nTranslator
        self.SMSSender = SMSSender
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-authorization,"
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, DELETE')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip
        self.phanterpwa_form_identify = None

    def check_origin(self, origin):
        return True

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})

    @check_client_token()
    @check_user_token()
    def get(self, *args):
        t_client = Serialize(
            self.projectConfig['BACKEND'][self.app_name]['secret_key'],
            self.projectConfig['BACKEND'][self.app_name]['default_time_client_token_expire']
        )
        if self.phanterpwa_client_token:
            db = self.DALDatabase
            # self.phanterpwa_current_client.as_dict(datetime_to_str=True)
            q = db(db.client.token == self.phanterpwa_client_token).select().first()
            if q:
                token_content_client = None
                try:
                    token_content_client = t_client.loads(self.phanterpwa_client_token)
                except BadSignature:
                    msg = 'The client have a invalid client-token, a new one has been generated.'
                    self.logger_api.warning("{0} - {1}".format(self.phanterpwa_current_user.email, msg))
                    token_content_client = None
                except SignatureExpired:
                    msg = 'The client have a expired client-token, a new one has been generated.'
                    self.logger_api.warning("{0} - {1}".format(self.phanterpwa_current_user.email, msg))
                    token_content_client = None
                if token_content_client:
                    sessions = []
                    q_sessions = db(db.client.auth_user == self.phanterpwa_current_user.id).select(orderby=db.client.date_created)
                    for x in q_sessions:
                        this_session = False
                        if x.token == self.phanterpwa_client_token:
                            this_session = True
                        tc = None
                        try:
                            tc = t_client.loads(x.token)
                        except Exception:
                            tc = None
                        user_agent = None
                        remote_addr = None
                        date_created = x.date_created
                        if tc:
                            remote_addr = tc['remote_addr']
                            user_agent = tc['user_agent']
                        sessions.append(
                            dict(
                                user_agent=user_agent,
                                agent=user_agent_parse(user_agent),
                                remote_addr=remote_addr,
                                date_created=str(date_created),
                                this_session=this_session,
                                identify=x.id
                            )
                        )
                    q_role = db(
                        (db.auth_membership.auth_user == self.phanterpwa_current_user.id) &
                        (db.auth_group.id == db.auth_membership.auth_group)
                    ).select(
                        db.auth_group.id, db.auth_group.role, orderby=db.auth_group.grade
                    )
                    roles = [x.role for x in q_role]
                    dict_roles = {x.id: x.role for x in q_role}
                    roles_id = [x.id for x in q_role]
                    role = None

                    if roles:
                        role = roles[-1]

                    t_url = URLSafeSerializer(
                        self.projectConfig['BACKEND'][self.app_name]["secret_key"],
                        salt="url_secret_key"
                    )
                    id_client = q.id
                    content = {
                        'id_user': str(self.phanterpwa_current_user.id),
                        'id_client': str(id_client),
                        'user_agent': self.phanterpwa_user_agent,
                        'remote_addr': self.phanterpwa_remote_ip
                    }
                    token_url = t_url.dumps(content)
                    user_image = PhanterpwaGalleryUserImage(self.phanterpwa_current_user.id, db, self.projectConfig)
                    self.set_status(200)
                    self.write({
                        'status': 'OK',
                        'code': 200,
                        'message': 'Session list and user',
                        'sessions': sessions,
                        'authorization': self.phanterpwa_authorization,
                        'client_token': self.phanterpwa_client_token,
                        'url_token': token_url,
                        'auth_user': {
                            'id': str(self.phanterpwa_current_user.id),
                            'first_name': E(self.phanterpwa_current_user.first_name),
                            'last_name': E(self.phanterpwa_current_user.last_name),
                            'email': self.phanterpwa_current_user.email,
                            'email': self.phanterpwa_current_user.email,
                            'fone_number': self.phanterpwa_current_user.fone_number,
                            'remember_me': q.remember_me,
                            'roles': roles,
                            'role': role,
                            'dict_roles': dict_roles,
                            'roles_id': roles_id,
                            'activated': self.phanterpwa_current_user.activated,
                            'image': user_image.id_image,
                            'two_factor': self.phanterpwa_current_user.two_factor_login,
                            'multiple_login': self.phanterpwa_current_user.permit_mult_login,
                            'locale': self.phanterpwa_current_user.locale,
                            'social_login': None
                        },
                        'i18n': {
                            'message': self.T('Lista de sessões e usuário'),
                            'auth_user': {'role': self.T(role)}
                        }
                    })

    @check_public_csrf_token(form_identify=[
        "phanterpwa-form-login", "user_locked", "phanterpwa-form-request_password"])
    def post(self, *args):
        self.phanterpwa_authorization = self.request.headers.get('phanterpwa-authorization')
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}

        login_by_phone = False
        if dict_arguments.get("mobile", False):
            login_by_phone = True

        if self.phanterpwa_authorization:
            t = Serialize(
                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire']
            )
            token_content = None
            try:
                token_content = t.loads(self.phanterpwa_authorization)
            except BadSignature:
                token_content = None
            except SignatureExpired:
                token_content = None
            if token_content and 'id' in token_content:
                id_user = token_content['id']
                q_user = self.DALDatabase(self.DALDatabase.auth_user.id == id_user).select().first()
                q_client = self.DALDatabase(
                    (self.DALDatabase.client.auth_user == id_user) &
                    (self.DALDatabase.client.token == self.phanterpwa_client_token)
                ).select().first()
                if q_user and q_client and not q_client.locked:
                    q_role = self.DALDatabase(
                        (self.DALDatabase.auth_membership.auth_user == q_user.id) &
                        (self.DALDatabase.auth_group.id == self.DALDatabase.auth_membership.auth_group)
                    ).select(
                        self.DALDatabase.auth_group.id, self.DALDatabase.auth_group.role, orderby=self.DALDatabase.auth_group.grade
                    )
                    roles = [x.role for x in q_role]
                    dict_roles = {x.id: x.role for x in q_role}
                    roles_id = [x.id for x in q_role]
                    role = None

                    t_url = URLSafeSerializer(
                        self.projectConfig['BACKEND'][self.app_name]["secret_key"],
                        salt="url_secret_key"
                    )
                    id_client = q_client.id
                    content = {
                        'id_user': str(q_user.id),
                        'id_client': str(q_client.id),
                        'user_agent': self.phanterpwa_user_agent,
                        'remote_addr': self.phanterpwa_remote_ip
                    }
                    token_url = t_url.dumps(content)

                    if roles:
                        role = roles[-1]
                    user_image = PhanterpwaGalleryUserImage(q_user.id, self.DALDatabase, self.projectConfig)
                    self.DALDatabase.commit()
                    self.set_status(202)
                    return self.write({
                        'status': 'Accepted',
                        'code': 202,
                        'message': 'The user already login',
                        'authorization': self.phanterpwa_authorization,
                        'client_token': self.phanterpwa_client_token,
                        'url_token': token_url,
                        'used_temporary': None,
                        'auth_user': {
                            'id': str(q_user.id),
                            'first_name': E(q_user.first_name),
                            'last_name': E(q_user.last_name),
                            'email': q_user.email,
                            'fone_number': q_user.fone_number,
                            'remember_me': q_client.remember_me,
                            'roles': roles,
                            'role': role,
                            'dict_roles': dict_roles,
                            'roles_id': roles_id,
                            'activated': q_user.activated,
                            'image': user_image.id_image,
                            'two_factor': q_user.two_factor_login,
                            'multiple_login': q_user.permit_mult_login,
                            'locale': q_user.locale,
                            'social_login': None
                        },
                        'i18n': {
                            'message': self.T('The user already login'),
                            'auth_user': {'role': self.T(role)}
                        }
                    })

        google_captcha = dict_arguments.get("google_captcha_token", None)
        two_factor = False
        if google_captcha:
            url_google_captcha = "https://www.google.com/recaptcha/api/siteverify?secret={0}&response={1}&remoteip={2}"
            url_google_captcha.format(
                self.projectConfig['RECAPTCHA_GOOGLE']['client_secret'],
                google_captcha,
                self.phanterpwa_remote_ip
            )
            googlecaptcha_response = {}
            try:
                with urlopen(url_google_captcha) as req:
                    googlecaptcha_response = req.read()
                    googlecaptcha_response = json.loads(googlecaptcha_response)
            except Exception as e:
                self.logger_api.warning(e)
                message = "There was a problem trying to load google captcha."
                self.set_status(400)
                return self.write({
                    'status': 'Bad Request',
                    'code': 400,
                    'message': message,
                    'i18n': {
                        'message': self.T(message)
                    }
                })
            score = float(googlecaptcha_response.get("score", 0.0))
            two_factor = True
            if googlecaptcha_response.success and score >= 5.0:
                two_factor = False

        # if not login
        if dict_arguments.get('edata'):
            used_temporary = None
            edata = dict_arguments['edata']
            if login_by_phone:
                fone_number, password = edata.split(":")
                if fone_number:
                    fone_number = base64.b64decode(fone_number).decode('utf-8')
                    fone_number = fone_number.strip().lower()
                password = base64.b64decode(password).decode('utf-8')

                numbers = [str(x) for x in range(10)]
                new_mobile = ""
                for n in fone_number:
                    if n in numbers:
                        new_mobile += n
                fone_number = new_mobile
                if len(fone_number) < 4 or len(fone_number) > 15:
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': 'Invalid mobile number',
                        'i18n': {
                            'message': self.T('Invalid mobile number')
                        }
                    })
                q_user = self.DALDatabase(self.DALDatabase.auth_user.fone_number == fone_number).select().first()
            else:
                email, password = edata.split(":")
                if email:
                    email = base64.b64decode(email).decode('utf-8')
                    email = email.strip().lower()
                password = base64.b64decode(password).decode('utf-8')
                q_user = self.DALDatabase(self.DALDatabase.auth_user.email == email).select().first()
            if q_user:
                if login_by_phone:
                    email = q_user.email
                if not q_user.login_attempts:
                    q_user.update_record(login_attempts=1)
                else:
                    q_user.update_record(login_attempts=q_user.login_attempts + 1)
                result = None
                try:
                    result = pbkdf2_sha512.verify(
                        "password{0}{1}".format(
                            password, self.projectConfig['BACKEND'][self.app_name]['secret_key']),
                        q_user.password_hash
                    )
                except Exception:
                    self.logger_api.error("Problem on check password", exc_info=True)
                finally:
                    if not result and\
                        q_user.temporary_password_expire and\
                        (datetime.now() < q_user.temporary_password_expire) and q_user.temporary_password_hash:
                        result = pbkdf2_sha512.verify(
                            "password{0}{1}".format(
                                password, self.projectConfig['BACKEND'][self.app_name]['secret_key']),
                            q_user.temporary_password_hash
                        )
                        if result:
                            used_temporary = password
                            q_user.update_record(login_attempts=0)
                if q_user.login_attempts > self.projectConfig['BACKEND'][self.app_name]['max_login_attempts']:
                    if q_user.datetime_next_attempt_to_login and\
                            (datetime.now() <= q_user.datetime_next_attempt_to_login):
                        t_delta = q_user.datetime_next_attempt_to_login - datetime.now()
                        msg = "Please, wait approximately {time_next_attempt} to try again."
                        tna = int(t_delta.total_seconds())
                        message = msg.format(time_next_attempt=humanize_seconds(tna))
                        message_i18n = self.T(msg).format(time_next_attempt=humanize_seconds(tna, self.i18nTranslator))
                        self.DALDatabase.commit()
                        if login_by_phone:
                            self.logger_api.warning("{0}:{1} - {2}".format(fone_number, password, message))
                        else:
                            self.logger_api.warning("{0}:{1} - {2}".format(email, password, message))
                        self.set_status(400)
                        return self.write({
                            'status': 'Bad Request',
                            'code': 400,
                            'message': message,
                            'login_attempts': q_user.login_attempts,
                            'i18n': {
                                'message': message_i18n,
                            }
                        })
                    else:
                        q_user.update_record(login_attempts=1)
                if result:
                    remember_me = False
                    timeout_token_user = self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire']
                    rem_me = checkbox_bool(dict_arguments['remember_me'])
                    if rem_me:
                        remember_me = True
                        timeout_token_user = self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire_remember_me']
                    t_user = Serialize(
                        self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                        timeout_token_user
                    )
                    if login_by_phone:
                        content = {
                            'id': str(q_user.id),
                            'email': email,
                            'fone_number': str(fone_number)
                        }
                    else:
                        content = {
                            'id': str(q_user.id),
                            'email': email
                        }

                    token_user = t_user.dumps(content)
                    token_user = token_user.decode('utf-8')
                    q_role = self.DALDatabase(
                        (self.DALDatabase.auth_membership.auth_user == q_user.id) &
                        (self.DALDatabase.auth_group.id == self.DALDatabase.auth_membership.auth_group)
                    ).select(
                        self.DALDatabase.auth_group.id, self.DALDatabase.auth_group.role, orderby=self.DALDatabase.auth_group.grade
                    )
                    roles = [x.role for x in q_role]
                    dict_roles = {x.id: x.role for x in q_role}
                    roles_id = [x.id for x in q_role]
                    role = None
                    if roles:
                        role = roles[-1]
                    q_user.update_record(login_attempts=0)
                    t_client = Serialize(
                        self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                        self.projectConfig['BACKEND'][self.app_name]['default_time_client_token_expire']
                    )
                    t_url = URLSafeSerializer(
                        self.projectConfig['BACKEND'][self.app_name]["secret_key"],
                        salt="url_secret_key"
                    )
                    r_client = self.DALDatabase(
                        self.DALDatabase.client.token == self.phanterpwa_client_token).select().first()
                    if r_client:
                        r_client.delete_record()
                    id_client = self.DALDatabase.client.insert(auth_user=q_user.id, date_created=datetime.now())
                    q_client = self.DALDatabase(self.DALDatabase.client.id == id_client).select().first()
                    content = {
                        'id_user': str(q_user.id),
                        'id_client': str(id_client),
                        'user_agent': self.phanterpwa_user_agent,
                        'remote_addr': self.phanterpwa_remote_ip
                    }

                    token_url = t_url.dumps(content)
                    token_client = t_client.dumps(content)
                    token_client = token_client.decode('utf-8')
                    q_client.update_record(
                        token=token_client,
                        date_created=datetime.now(),
                        remember_me=remember_me,
                        locked=False,
                    )

                    if not q_user.permit_mult_login:
                        r_client = self.DALDatabase(
                            (self.DALDatabase.client.auth_user == q_user.id) &
                            (self.DALDatabase.client.token != token_client)
                        ).select()
                        if r_client:
                            r_client = self.DALDatabase(
                                (self.DALDatabase.client.auth_user == q_user.id) &
                                (self.DALDatabase.client.token != token_client)
                            ).delete()
                    self.DALDatabase.commit()
                    user_image = PhanterpwaGalleryUserImage(q_user.id, self.DALDatabase, self.projectConfig)

                    if (q_user.two_factor_login or two_factor) and not used_temporary and not self.phanterpwa_form_identify == "user_locked":
                        two_factor_serialize = URLSafeSerializer(
                            self.projectConfig['BACKEND'][self.app_name]["secret_key"],
                            salt="two_factor_url"
                        )
                        content = {
                            'id_user': str(q_user.id),
                            'id_client': str(id_client),
                            'user_agent': self.phanterpwa_user_agent,
                            'remote_addr': self.phanterpwa_remote_ip
                        }
                        two_factor_url = two_factor_serialize.dumps(content)
                        two_factor_code = generate_activation_code()
                        self.Translator_email.direct_translation = self.phanterpwa_language

                        if login_by_phone:
                            keys_formatter = dict(
                                app_name=self.projectConfig['PROJECT']['name'],
                                code=two_factor_code,
                            )
                            text_sms = sms_two_factor_code.text.html(
                                minify=True,
                                translate=True,
                                formatter=keys_formatter,
                                i18nInstance=self.Translator_sms,
                                dictionary=self.phanterpwa_language,
                                do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                                escape_string=False
                            )
                            if self.SMSSender:
                                e_sms = self.SMSSender(
                                    q_user.fone_number,
                                    identify="two-factor-authentication-code",
                                    text_message=text_sms,
                                    app_name=self.app_name,
                                    projectConfig=self.projectConfig
                                )
                            else:
                                raise SyntaxError("The SMSSender is indefined")
                            result = ""
                            try:
                                if self.projectConfig["PROJECT"]["debug"]:
                                    self.logger_api.warning("TWO FACTOR CODE: {0}".format(two_factor_code))
                                else:
                                    self.logger_api.warning("SMS to '{0}' -> Two Factor Code: {1}".format(
                                        q_user.fone_number,
                                        two_factor_code
                                    ))
                                    e_sms.send()
                            except Exception as e:
                                result = "SMS to '{0}' don't send! -> Error: {1} -> Two Factor Code: {2}".format(
                                    fone_number,
                                    e,
                                    two_factor_code
                                )
                                self.logger_api.error(result, exc_info=True)
                                message = "There was an error trying to send the sms."
                                message_i18n = self.T("There was an error trying to send the sms.")
                                self.DALDatabase.rollback()
                                self.set_status(400)
                                return self.write({
                                    'status': 'Bad Request',
                                    'code': 400,
                                    'message': message,
                                    'i18n': {'message': message_i18n}
                                })
                            else:
                                self.DALDatabase.two_factor_login.insert(
                                    auth_user=q_user.id,
                                    two_factor_url=two_factor_url,
                                    two_factor_code=two_factor_code
                                )
                                message = 'A code has been sent to your sms.'
                                message_i18n = self.T('A code has been sent to your sms.')
                                self.DALDatabase.commit()
                                self.set_status(206)
                                return self.write({
                                    'status': 'OK',
                                    'message': message,
                                    'client_token': token_client,
                                    'as': self.phanterpwa_form_identify,
                                    'auth_user': {
                                        'remember_me': q_client.remember_me
                                    },
                                    'i18n': {
                                        'message': message_i18n
                                    },
                                    'authorization_url': two_factor_url
                                })
                        else:
                            keys_formatter = dict(
                                app_name=self.projectConfig['PROJECT']['name'],
                                user_name="{0} {1}".format(
                                    q_user.first_name,
                                    q_user.last_name
                                ),
                                code=two_factor_code,
                                time_expires=humanize_seconds(
                                    self.projectConfig['BACKEND'][self.app_name]['default_time_two_factor_code_expire'],
                                    self.Translator_email
                                ),
                                user_agent=self.phanterpwa_user_agent,
                                user_ip=self.phanterpwa_remote_ip,
                                copyright=interpolate(
                                    self.projectConfig['CONTENT_EMAILS']['copyright'], {'now': datetime.now().year}),
                                link_to_your_page=self.projectConfig['CONTENT_EMAILS']['link_to_your_site']
                            )
                            text_email = email_two_factor_code.text.html(
                                minify=True,
                                translate=True,
                                formatter=keys_formatter,
                                i18nInstance=self.Translator_email,
                                dictionary=self.phanterpwa_language,
                                do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                                escape_string=False
                            )
                            html_email = email_two_factor_code.html.html(
                                minify=True,
                                translate=True,
                                formatter=keys_formatter,
                                i18nInstance=self.Translator_email,
                                dictionary=self.phanterpwa_language,
                                do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                                escape_string=False
                            )
                            e_mail = MailSender(
                                self.projectConfig['EMAIL']['default_sender'],
                                self.projectConfig['EMAIL']['password'],
                                q_user.email,
                                subject="Two factor authentication code",
                                text_message=text_email,
                                html_message=html_email,
                                server=self.projectConfig['EMAIL']['server'],
                                port=self.projectConfig['EMAIL']['port'],
                                use_tls=self.projectConfig['EMAIL']['use_tls'],
                                use_ssl=self.projectConfig['EMAIL']['use_ssl']
                            )
                            result = ""
                            try:
                                if self.projectConfig["PROJECT"]["debug"]:
                                    self.logger_api.warning("TWO FACTOR CODE: {0}".format(two_factor_code))
                                else:
                                    self.logger_api.warning("Email from '{0}' to '{1}' -> Two Factor Code: {2}".format(
                                        self.projectConfig['EMAIL']['default_sender'],
                                        q_user.email,
                                        two_factor_code
                                    ))
                                    e_mail.send()
                            except Exception as e:
                                result = "Email from '{0}' to '{1}' don't send! -> Error: {2} -> Two Factor Code: {3}".format(
                                    self.projectConfig['EMAIL']['default_sender'],
                                    dict_arguments['email'],
                                    e,
                                    two_factor_code
                                )
                                self.logger_api.error(result, exc_info=True)
                                message = "There was an error trying to send the email."
                                message_i18n = self.T("There was an error trying to send the email.")
                                self.DALDatabase.rollback()
                                self.set_status(400)
                                return self.write({
                                    'status': 'Bad Request',
                                    'code': 400,
                                    'message': message,
                                    'i18n': {'message': message_i18n}
                                })
                            else:

                                self.DALDatabase.two_factor_login.insert(
                                    auth_user=q_user.id,
                                    two_factor_url=two_factor_url,
                                    two_factor_code=two_factor_code
                                )
                                message = 'A code has been sent to your email.'
                                message_i18n = self.T('A code has been sent to your email.')
                                self.DALDatabase.commit()
                                self.set_status(206)
                                return self.write({
                                    'status': 'OK',
                                    'message': message,
                                    'client_token': token_client,
                                    'as': self.phanterpwa_form_identify,
                                    'auth_user': {
                                        'remember_me': q_client.remember_me
                                    },
                                    'i18n': {
                                        'message': message_i18n
                                    },
                                    'authorization_url': two_factor_url
                                })

                    else:
                        if role != "root":
                            self.DALDatabase.auth_activity.insert(
                                auth_user=q_user.id,
                                request="login",
                                activity="Logged!",
                                date_activity=datetime.now()
                            )
                            self.DALDatabase.commit()

                        self.set_status(200)
                        return self.write({
                            'status': 'OK',
                            'code': 200,
                            'message': 'The user is logged',
                            'authorization': token_user,
                            'client_token': token_client,
                            'url_token': token_url,
                            'used_temporary': used_temporary,
                            'auth_user': {
                                'id': str(q_user.id),
                                'first_name': E(q_user.first_name),
                                'last_name': E(q_user.last_name),
                                'email': email,
                                'fone_number': q_user.fone_number,
                                'remember_me': q_client.remember_me,
                                'roles': roles,
                                'role': role,
                                'dict_roles': dict_roles,
                                'roles_id': roles_id,
                                'activated': q_user.activated,
                                'image': user_image.id_image,
                                'two_factor': q_user.two_factor_login,
                                'multiple_login': q_user.permit_mult_login,
                                'locale': q_user.locale,
                                'social_login': None
                            },
                            'i18n': {
                                'message': self.T('The user is logged'),
                                'auth_user': {'role': self.T(role)}
                            }
                        })
                else:
                    default_time_temporary_password_expire = self.projectConfig[
                        'BACKEND'][self.app_name]['default_time_temporary_password_expire']
                    timeout_to_next_login_attempt = self.projectConfig[
                        'BACKEND'][self.app_name]['timeout_to_next_login_attempt']
                    q_user.update_record(
                        temporary_password_expire=datetime.now() + timedelta(seconds=default_time_temporary_password_expire),
                        datetime_next_attempt_to_login=datetime.now() + timedelta(seconds=timeout_to_next_login_attempt)
                    )
                    msg = 'Wrong password! Attempt {attempt_number} from {max_attempts}'
                    message = msg.format(
                        attempt_number=q_user.login_attempts,
                        max_attempts=self.projectConfig['BACKEND'][self.app_name]['max_login_attempts']
                    )
                    message_i18n = self.T(msg).format(
                        attempt_number=q_user.login_attempts,
                        max_attempts=self.projectConfig['BACKEND'][self.app_name]['max_login_attempts']
                    )
                    self.DALDatabase.commit()
                    self.logger_api.warning("{0}:{1} - {2}".format(email, password, message))
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': message,
                        'login_attempts': q_user.login_attempts,
                        'i18n': {
                            'message': message_i18n
                        }
                    })
            else:
                if login_by_phone:
                    self.logger_api.warning("{0} - {1}".format(
                        fone_number, "Added mobile number does not exist!"))
                    self.set_status(401)
                    return self.write({
                        'status': 'Unauthorized',
                        'code': 401,
                        'reasons': "Mobile number does not exist",
                        'fone_number': fone_number,
                        'password': password,
                        'message': 'Mobile number does not exist!',
                        'i18n': {
                            'message': self.T('Mobile number does not exist!')
                        }
                    })
                else:
                    self.logger_api.warning("{0} - {1}".format(
                        email, "Added email does not exist!"))
                    self.set_status(401)
                    return self.write({
                        'status': 'Unauthorized',
                        'code': 401,
                        'reasons': "Email does not exist",
                        'email': email,
                        'password': password,
                        'message': 'Email does not exist!',
                        'i18n': {
                            'message': self.T('Email does not exist!')
                        }
                    })
        self.set_status(400)
        return self.write({
            'status': 'Bad Request',
            'code': 400,
            'message': 'Invalid password or email',
            'as': dict_arguments.get('edata'),
            'i18n': {
                'message': self.T('Invalid password or email')
            }
        })

    @check_client_token()
    @check_user_token()
    def delete(self, *args):
        id_session = args[0]
        t_client = Serialize(
            self.projectConfig['BACKEND'][self.app_name]['secret_key'],
            self.projectConfig['BACKEND'][self.app_name]['default_time_client_token_expire']
        )
        if self.phanterpwa_client_token:
            db = self.DALDatabase
            # self.phanterpwa_current_client.as_dict(datetime_to_str=True)
            q = db(db.client.token == self.phanterpwa_client_token).select().first()
            if q:
                token_content_client = None
                try:
                    token_content_client = t_client.loads(self.phanterpwa_client_token)
                except BadSignature:
                    token_content_client = None
                except SignatureExpired:
                    token_content_client = None
                if token_content_client:
                    sessions = []
                    q_sessions = db(db.client.auth_user == self.phanterpwa_current_user.id).select(orderby=db.client.date_created)
                    for x in q_sessions:
                        this_session = False
                        if x.token == self.phanterpwa_client_token:
                            this_session = True
                        if (str(x.id) == id_session) and not this_session:
                            x.delete_record()
                        else:
                            tc = None
                            try:
                                tc = t_client.loads(x.token)
                            except Exception:
                                tc = None
                            user_agent = None
                            remote_addr = None
                            date_created = x.date_created
                            if tc:
                                remote_addr = tc['remote_addr']
                                user_agent = tc['user_agent']
                            sessions.append(
                                dict(
                                    user_agent=user_agent,
                                    agent=user_agent_parse(user_agent),
                                    remote_addr=remote_addr,
                                    date_created=str(date_created),
                                    this_session=this_session,
                                    identify=x.id
                                )
                            )

                    self.set_status(200)
                    self.write({
                        'status': 'OK',
                        'code': 200,
                        'message': 'Deleted Session',
                        'i18n': {
                            'message': self.T('Deleted Session')
                        },
                        'sessions': sessions
                    })


class Activity(web.RequestHandler):
    """
        url: 'api/auth/activity/'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.i18nTranslator = i18nTranslator
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "phanterpwa-authorization,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip

    def check_origin(self, origin):
        return True

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})

    @check_client_token()
    @check_user_token()
    def get(self, *args):
        id_user = self.phanterpwa_current_user.id
        db = self.DALDatabase
        r_activity = db(db.auth_activity.auth_user == id_user).select(orderby=~db.auth_activity.id, limitby=(0, 100))
        self.set_status(200)
        self.write({
            'status': 'OK',
            'code': 200,
            'message': 'Activity list',
            'data': json.loads(r_activity.as_json()),
            'i18n': {
                'message': self.T('Activity list')
            }
        })


class TwoFactor(web.RequestHandler):
    """
        url: '/api/auth/two-factor/<authorization_url>'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, Translator_email, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.Translator_email = Translator_email
        self.i18nTranslator = i18nTranslator
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, PUT')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip

    def check_origin(self, origin):
        return True

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})

    @check_client_token()
    def put(self, *args):
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        two_factor_code = dict_arguments.get("code", None)
        checked_code = None
        try:
            checked_code = check_activation_code(
                two_factor_code
            )
        except Exception:
            self.logger_api.error("Problem on check activation code", exc_info=True)
        if not checked_code:
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': 'Invalid two factor code',
                'i18n': {
                    'message': self.T('Invalid two factor code')
                }
            })

        authorization_url = args[0]
        if authorization_url and checked_code:
            db = self.DALDatabase
            token_content = None
            two_factor_serialize = URLSafeSerializer(
                self.projectConfig['BACKEND'][self.app_name]["secret_key"],
                salt="two_factor_url"
            )
            try:
                token_content = two_factor_serialize.loads(authorization_url)
            except BadSignature:
                token_content = None
            except SignatureExpired:
                token_content = None
            if token_content and 'id_user' in token_content:
                id_user = token_content['id_user']
                q_user = db(db.auth_user.id == id_user).select().first()
                q_client = db(
                    (db.client.auth_user == id_user) &
                    (db.client.token == self.phanterpwa_client_token)
                ).select().first()
                if q_user and q_client and not q_client.locked:
                    r_twofactor_code = db(
                        (db.two_factor_login.auth_user == q_user.id)
                        & (db.two_factor_login.two_factor_code == checked_code)
                        & (db.two_factor_login.two_factor_url == authorization_url)
                    ).select().first()
                    if not r_twofactor_code:
                        self.set_status(400)
                        return self.write({
                            'status': 'Bad Request',
                            'code': 400,
                            'message': 'Invalid two factor code',
                            'i18n': {
                                'message': self.T('Invalid two factor code')
                            }
                        })
                    else:
                        db(db.two_factor_login.auth_user == q_user.id).delete()
                        db.commit()

                    remember_me = q_client.remember_me
                    timeout_token_user = self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire']
                    if remember_me:
                        timeout_token_user = self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire_remember_me']
                    t_user = Serialize(
                        self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                        timeout_token_user
                    )
                    content = {
                        'id': str(q_user.id),
                        'email': str(q_user.email)
                    }
                    token_user = t_user.dumps(content)
                    token_user = token_user.decode('utf-8')
                    q_role = db(
                        (db.auth_membership.auth_user == q_user.id) &
                        (db.auth_group.id == db.auth_membership.auth_group)
                    ).select(
                        db.auth_group.id, db.auth_group.role, orderby=db.auth_group.grade
                    )
                    roles = [x.role for x in q_role]
                    dict_roles = {x.id: x.role for x in q_role}
                    roles_id = [x.id for x in q_role]
                    role = None
                    if roles:
                        role = roles[-1]
                    q_user.update_record(login_attempts=0)
                    t_client = Serialize(
                        self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                        self.projectConfig['BACKEND'][self.app_name]['default_time_client_token_expire']
                    )
                    t_url = URLSafeSerializer(
                        self.projectConfig['BACKEND'][self.app_name]["secret_key"],
                        salt="url_secret_key"
                    )
                    q_client.delete_record()
                    id_client = db.client.insert(auth_user=q_user.id, date_created=datetime.now())
                    q_client = db(db.client.id == id_client).select().first()
                    content = {
                        'id_user': str(q_user.id),
                        'id_client': str(id_client),
                        'user_agent': self.phanterpwa_user_agent,
                        'remote_addr': self.phanterpwa_remote_ip
                    }

                    token_url = t_url.dumps(content)
                    token_client = t_client.dumps(content)
                    token_client = token_client.decode('utf-8')
                    q_client.update_record(
                        token=token_client,
                        date_created=datetime.now(),
                        remember_me=remember_me,
                        locked=False,
                    )

                    if not q_user.permit_mult_login:
                        r_client = db(
                            (db.client.auth_user == q_user.id) &
                            (db.client.token != token_client)
                        ).select()
                        if r_client:
                            r_client = db(
                                (db.client.auth_user == q_user.id) &
                                (db.client.token != token_client)
                            ).delete()
                    db.commit()
                    user_image = PhanterpwaGalleryUserImage(q_user.id, db, self.projectConfig)
                    if role != "root":
                        db.auth_activity.insert(
                            auth_user=q_user.id,
                            request="two-factor",
                            activity="Logged!",
                            date_activity=datetime.now()
                        )
                        db.commit()
                    self.set_status(200)
                    return self.write({
                        'status': 'OK',
                        'code': 200,
                        'message': 'The user is logged',
                        'authorization': token_user,
                        'client_token': token_client,
                        'url_token': token_url,
                        'used_temporary': None,
                        'auth_user': {
                            'id': str(q_user.id),
                            'first_name': E(q_user.first_name),
                            'last_name': E(q_user.last_name),
                            'email': q_user.email,
                            'fone_number': q_user.fone_number,
                            'remember_me': q_client.remember_me,
                            'roles': roles,
                            'role': role,
                            'dict_roles': dict_roles,
                            'roles_id': roles_id,
                            'activated': q_user.activated,
                            'image': user_image.id_image,
                            'two_factor': q_user.two_factor_login,
                            'multiple_login': q_user.permit_mult_login,
                            'locale': q_user.locale,
                            'social_login': None
                        },
                        'i18n': {
                            'message': self.T('The user is logged'),
                            'auth_user': {'role': self.T(role)}
                        }
                    })

        else:
            self.set_status(401)
            return self.write({
                'status': 'Unauthorized',
                'code': 401,
                'message': 'Invalid activation code',
                'i18n': {
                    'message': self.T('Invalid activation code')
                }
            })


class LockUser(web.RequestHandler):
    """
        url: '/api/auth/lock/'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.i18nTranslator = i18nTranslator
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "phanterpwa-authorization,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip

    def check_origin(self, origin):
        return True

    @check_client_token()
    @check_user_token()
    def get(self):
        self.phanterpwa_current_client.update_record(
            locked=True
        )
        self.DALDatabase.commit()
        self.set_status(200)
        return self.write({
            'status': 'OK',
            'code': 200,
            'message': 'The session has been locked',
            'i18n': {
                'message': self.T('The session has been locked')
            }
        })

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})


class ImageUser(web.RequestHandler):
    """
        url: '/backend/<app_name>/auth/image/<id_image>'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.i18nTranslator = i18nTranslator
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language

    def check_origin(self, origin):
        return True

    @check_url_token(ignore_user_agent=True)
    def get(self, *args, **kargs):
        """
        Receive request to create and response with a token csrf or captcha
        """
        image_id = args[0]
        buf_size = 4096
        self.set_header('Content-Type', 'application/octet-stream')
        q_image = self.DALDatabase(
            (self.DALDatabase.auth_user_phanterpwagallery.id == image_id)
            & (self.DALDatabase.auth_user_phanterpwagallery.subfolder == 'profile')
        ).select(
            self.DALDatabase.auth_user_phanterpwagallery.phanterpwagallery
        ).last()
        if q_image:
            file = os.path.join(
                self.projectConfig['PROJECT']['path'],
                "backapps",
                self.app_name,
                'uploads',
                q_image.phanterpwagallery.folder,
                q_image.phanterpwagallery.alias_name
            )
            self.set_header(
                'Content-Disposition', 'attachment; filename="{0}"'.format(
                    q_image.phanterpwagallery.filename)
            )
            if os.path.isfile(os.path.normpath(file)):
                self.set_status(200)
                with open(file, 'rb') as f:
                    while True:
                        data = f.read(buf_size)
                        if not data:
                            break
                        self.write(data)
                self.finish()
                return
        self.set_status(202)
        file = os.path.join(
            self.projectConfig['PROJECT']['path'],
            "backapps",
            self.app_name,
            'static',
            'images',
            'user.png'
        )
        with open(file, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        self.finish()

    def options(self, *args):
        self.set_status(200)
        return self.write({"status": "OK"})


class ChangeAccount(web.RequestHandler):
    """
        url: 'api/auth/change/'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, Translator_email, SMSSender=None, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.SMSSender = SMSSender
        self.i18nTranslator = i18nTranslator
        self.Translator_email = Translator_email
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "phanterpwa-authorization,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'OPTIONS, PUT')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip

    def check_origin(self, origin):
        return True

    @check_private_csrf_token(form_identify=["phanterpwa-form-profile", "phanterpwa-form-change_account"])
    def put(self, *args, **kargs):

        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        first_name = dict_arguments['first_name']
        last_name = dict_arguments['last_name']
        email_now = self.phanterpwa_current_user.email
        fone_number_now = self.phanterpwa_current_user.fone_number
        new_email = dict_arguments['email'].strip().lower()
        new_fone_number = dict_arguments.get('fone_number', None)
        two_factor = checkbox_bool(dict_arguments.get('two_factor', False))
        multiple_login = checkbox_bool(dict_arguments.get('multiple_login', False))

        table = self.DALDatabase.auth_user
        result = FieldsDALValidateDictArgs(
            dict_arguments,
            *[table[x] for x in table.fields if x in ["first_name", "last_name"]],
            table["email"] if new_email != email_now else None
        )
        r = result.validate()
        if r:
            message = 'The form has errors'
            i18n_errors = {}
            for x in result.errors:
                tran = self.T(result.errors[x])
                i18n_errors[x] = tran
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': message,
                'errors': result.errors,
                'i18n': {
                    'message': self.T(message),
                    'errors': i18n_errors
                }
            })
        else:
            email_change = False
            first_name_change = False
            last_name_change = False
            image_change = False
            two_factor_change = False
            multiple_login_change = False
            fone_number_change = False

            if(first_name != self.phanterpwa_current_user.first_name):
                self.phanterpwa_current_user.update_record(first_name=first_name)
                first_name_change = True

            if(last_name != self.phanterpwa_current_user.last_name):
                self.phanterpwa_current_user.update_record(last_name=last_name)
                last_name_change = True

            if(two_factor != self.phanterpwa_current_user.two_factor_login):
                self.phanterpwa_current_user.update_record(two_factor_login=two_factor)
                two_factor_change = True

            if(multiple_login != self.phanterpwa_current_user.permit_mult_login):
                self.phanterpwa_current_user.update_record(permit_mult_login=multiple_login)
                multiple_login_change = True

            if self.request.files and\
                "phanterpwa-gallery-file-input" in self.request.files:
                imageBytes = self.request.files["phanterpwa-gallery-file-input"][0]['body']
                filename = self.request.files["phanterpwa-gallery-file-input"][0]['filename']
                cutterSizeX = dict_arguments['phanterpwa-gallery-input-cutterSizeX']
                cutterSizeY = dict_arguments['phanterpwa-gallery-input-cutterSizeY']
                cut_file = PhanterpwaGalleryCutter(
                    imageName=filename,
                    imageBytes=imageBytes,
                    cutterSizeX=cutterSizeX,
                    cutterSizeY=cutterSizeY
                )
                if 'phanterpwa-gallery-input-autoCut' in dict_arguments and\
                    dict_arguments['phanterpwa-gallery-input-autoCut']:
                    cutedImage = cut_file.auto_cut()
                else:
                    positionX = dict_arguments['phanterpwa-gallery-input-positionX']
                    positionY = dict_arguments['phanterpwa-gallery-input-positionY']
                    newSizeX = dict_arguments['phanterpwa-gallery-input-newSizeX']
                    newSizeY = dict_arguments['phanterpwa-gallery-input-newSizeY']
                    cutedImage = cut_file.specific_cut(
                        newSizeX=newSizeX,
                        newSizeY=newSizeY,
                        positionX=positionX,
                        positionY=positionY
                    )
                upload_image = PhanterpwaGalleryUserImage(
                    self.phanterpwa_current_user.id,
                    self.DALDatabase,
                    self.projectConfig
                )
                image_change = upload_image.set_image(
                    *cutedImage
                )
            activate = self.phanterpwa_current_user.activated
            if new_email != email_now:
                activation_code = generate_activation_code()
                self.Translator_email.direct_translation = self.phanterpwa_language
                keys_formatter = dict(
                    app_name=self.projectConfig['PROJECT']['name'],
                    user_name="{0} {1}".format(
                        first_name,
                        last_name
                    ),
                    code=activation_code,
                    time_expires=humanize_seconds(
                        self.projectConfig['BACKEND'][self.app_name]['default_time_activation_code_expire'],
                        self.Translator_email
                    ),
                    copyright=interpolate(self.projectConfig['CONTENT_EMAILS']['copyright'], {'now': datetime.now().year}),
                    link_to_your_page=self.projectConfig['CONTENT_EMAILS']['link_to_your_site']
                )
                email_password.text.formatter(keys_formatter)
                text_email = email_activation_code.text.html(
                    minify=True,
                    translate=True,
                    formatter=keys_formatter,
                    i18nInstance=self.Translator_email,
                    dictionary=self.phanterpwa_language,
                    do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                    escape_string=False
                )
                html_email = email_activation_code.html.html(
                    minify=True,
                    translate=True,
                    formatter=keys_formatter,
                    i18nInstance=self.Translator_email,
                    dictionary=self.phanterpwa_language,
                    do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                    escape_string=False
                )

                e_mail = MailSender(
                    self.projectConfig['EMAIL']['default_sender'],
                    self.projectConfig['EMAIL']['password'],
                    new_email,
                    subject="Activation code",
                    text_message=text_email,
                    html_message=html_email,
                    server=self.projectConfig['EMAIL']['server'],
                    port=self.projectConfig['EMAIL']['port'],
                    use_tls=self.projectConfig['EMAIL']['use_tls'],
                    use_ssl=self.projectConfig['EMAIL']['use_ssl']
                )
                result = ""
                try:
                    if self.projectConfig["PROJECT"]["debug"]:
                        self.logger_api.warning("ACTIVATION CODE: {0}".format(activation_code))
                    else:
                        self.logger_api.warning("Email from '{0}' to '{1}' -> Activation Code: {2}".format(
                            self.projectConfig['EMAIL']['default_sender'],
                            new_email,
                            activation_code
                        ))
                        e_mail.send()
                except Exception as e:
                    result = "Email from '{0}' to '{1}' don't send! -> Error: {2} -> Activation Code: {3}".format(
                        self.projectConfig['EMAIL']['default_sender'], dict_arguments['email'], e, activation_code)
                    self.logger_api.error(result, exc_info=True)
                    message = "There was an error trying to send the email."
                    message_i18n = self.T("There was an error trying to send the email.")
                    self.DALDatabase.rollback()
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': message,
                        'i18n': {'message': message_i18n}
                    })
                else:
                    self.phanterpwa_current_user.update_record(
                        activation_code=activation_code.split("-")[0],
                        timeout_to_resend_activation_email=datetime.now() +
                            timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['default_time_activation_code_expire'])
                    )
                    activate = False
                    self.phanterpwa_current_user.update_record(email=new_email, activated=activate)
                    q_list = self.DALDatabase(
                        (self.DALDatabase.email_user_list.auth_user == self.phanterpwa_current_user.id) &
                        (self.DALDatabase.email_user_list.email == email_now)
                    ).select().first()
                    if q_list:
                        q_list.update_record(
                            datetime_changed=datetime.now()
                        )
                    else:
                        self.DALDatabase.email_user_list.insert(
                            auth_user=self.phanterpwa_current_user.id,
                            email=email_now
                        )
                    email_change = True

            if new_fone_number != fone_number_now:
                activation_code = generate_activation_code()
                self.Translator_email.direct_translation = self.phanterpwa_language
                keys_formatter = dict(
                    app_name=self.projectConfig['PROJECT']['name'],
                    code=activation_code,
                )
                text_sms = sms_activation_code.text.html(
                    minify=True,
                    translate=True,
                    formatter=keys_formatter,
                    i18nInstance=self.Translator_email,
                    dictionary=self.phanterpwa_language,
                    do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                    escape_string=False
                )
                sms_token_serialize = URLSafeSerializer(
                    self.projectConfig['BACKEND'][self.app_name]["secret_key"],
                    salt="sms_token"
                )
                content = {
                    'id_user': str(self.phanterpwa_current_user.id),
                    'user_agent': self.phanterpwa_user_agent,
                }
                if self.SMSSender:
                    e_sms = self.SMSSender(
                        new_fone_number,
                        identify="two-factor-authentication-code",
                        text_message=text_sms,
                        app_name=self.app_name,
                        projectConfig=self.projectConfig
                    )
                else:
                    raise SyntaxError("The SMSSender is indefined")

                result = ""
                try:
                    if self.projectConfig["PROJECT"]["debug"]:
                        self.logger_api.warning("TWO FACTOR CODE: {0}".format(activation_code))
                    else:
                        self.logger_api.warning("SMS to '{0}' -> Two Factor Code: {1}".format(
                            new_fone_number,
                            activation_code
                        ))
                        e_sms.send()
                except Exception as e:
                    result = "SMS to '{0}' don't send! -> Error: {1} -> Two Factor Code: {2}".format(
                        new_fone_number,
                        e,
                        activation_code
                    )
                    self.logger_api.error(result, exc_info=True)
                    message = "There was an error trying to send the sms."
                    message_i18n = self.T("There was an error trying to send the sms.")
                    self.DALDatabase.rollback()
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': message,
                        'i18n': {'message': message_i18n}
                    })
                else:
                    self.phanterpwa_current_user.update_record(
                        activation_code=activation_code.split("-")[0],
                        timeout_to_resend_activation_email=datetime.now() +
                            timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['default_time_activation_code_expire'])
                    )
                    activate = False
                    self.phanterpwa_current_user.update_record(
                        email=new_email, activated=activate
                    )
                    q_list = self.DALDatabase(
                        (self.DALDatabase.email_user_list.auth_user == self.phanterpwa_current_user.id) &
                        (self.DALDatabase.email_user_list.email == email_now)
                    ).select().first()
                    if q_list:
                        q_list.update_record(
                            datetime_changed=datetime.now()
                        )
                    else:
                        self.DALDatabase.email_user_list.insert(
                            auth_user=self.phanterpwa_current_user.id,
                            email=email_now
                        )
                    fone_number_change = True

            if any([email_change,
                    fone_number_change,
                    first_name_change,
                    last_name_change,
                    image_change,
                    two_factor_change,
                    multiple_login_change]):
                q_role = self.DALDatabase(
                    (self.DALDatabase.auth_membership.auth_user == self.phanterpwa_current_user.id) &
                    (self.DALDatabase.auth_group.id == self.DALDatabase.auth_membership.auth_group)
                ).select(
                    self.DALDatabase.auth_group.id, self.DALDatabase.auth_group.role, orderby=self.DALDatabase.auth_group.grade
                )
                roles = [x.role for x in q_role]
                dict_roles = {x.id: x.role for x in q_role}
                roles_id = [x.id for x in q_role]
                role = None
                if roles:
                    role = roles[-1]
                q_client = self.DALDatabase(
                    (self.DALDatabase.client.auth_user == self.phanterpwa_current_user.id) &
                    (self.DALDatabase.client.token == self.phanterpwa_client_token)
                ).select().first()
                self.DALDatabase.commit()
                user_image = PhanterpwaGalleryUserImage(self.phanterpwa_current_user.id, self.DALDatabase, self.projectConfig)
                self.set_status(200)
                return self.write({
                    'status': 'OK',
                    'code': 200,
                    'message': 'Account was successfully changed',
                    'auth_user': {
                        'id': str(self.phanterpwa_current_user.id),
                        'first_name': E(first_name),
                        'last_name': E(last_name),
                        'email': new_email,
                        'fone_number': new_fone_number,
                        'remember_me': q_client.remember_me,
                        'roles': roles,
                        'role': role,
                        'dict_roles': dict_roles,
                        'roles_id': roles_id,
                        'activated': activate,
                        'image': user_image.id_image,
                        'two_factor': self.phanterpwa_current_user.two_factor_login,
                        'multiple_login': self.phanterpwa_current_user.permit_mult_login,
                        'locale': self.phanterpwa_current_user.locale,
                        'social_login': None
                    },
                    'i18n': {
                        'message': self.T('Account was successfully changed'),
                        'auth_user': {'role': self.T(role)}
                    }
                })
            else:
                message = "Nothing has changed!"
                self.DALDatabase.commit()
                self.set_status(202)
                return self.write({
                    'status': 'Accepted',
                    'code': 202,
                    'message': message,
                    'i18n': {
                        'message': self.T(message)
                    }
                })

    def options(self, *args):
        self.set_status(200)
        self.write({
            "status": "OK",
        })


class CreateAccount(web.RequestHandler):
    """
        url: 'api/auth/create/'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.i18nTranslator = i18nTranslator
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip

    def check_origin(self, origin):
        return True

    @requires_no_authentication()
    @check_public_csrf_token(form_identify="phanterpwa-form-register")
    def post(self):
        self.phanterpwa_client_token = self.request.headers.get('phanterpwa-client-token')
        table = self.DALDatabase.auth_user
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        password, password_repeat = dict_arguments["edata"].split(":")
        try:
            dict_arguments['password'] = base64.b64decode(password).decode('utf-8')
            dict_arguments['password_repeat'] = base64.b64decode(password_repeat).decode('utf-8')
        except UnicodeDecodeError:
            self.logger_api.warning(
                "UnicodeError (CreateAccount)\nArguments: {0}".format(str(dict_arguments))
            )
            message = self.T('The form has errors')
            i18n = {
                'message': self.T(message),
                'errors': {
                    'password': self.T('Password contains invalid characters.'),
                    'password_repeat': self.T('Password contains invalid characters.')
                }
            }
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': message,
                'errors': {
                    'password': 'Password contains invalid characters.',
                    'password_repeat': 'Password contains invalid characters.'
                },
                'i18n': i18n,
            })
        pass_hash = pbkdf2_sha512.hash("password{0}{1}".format(
            dict_arguments['password'], self.projectConfig['BACKEND'][self.app_name]['secret_key']
        ))
        dict_arguments['password_hash'] = pass_hash
        login_by_phone = False
        if dict_arguments.get("mobile", False):
            login_by_phone = True
            fone_number = dict_arguments.get("mobile")
            numbers = [str(x) for x in range(10)]
            new_mobile = ""
            for n in fone_number:
                if n in numbers:
                    new_mobile += n
            email = "{0}.mobile@phanterpwa.com".format(new_mobile)
            dict_arguments['email'] = email
            dict_arguments['fone_number'] = new_mobile
            if len(new_mobile) < 4 or len(new_mobile) > 15:
                self.set_status(400)
                return self.write({
                    'status': 'Bad Request',
                    'code': 400,
                    'message': 'Invalid mobile number',
                    'i18n': {
                        'message': self.T('Invalid mobile number')
                    }
                })
        else:
            email = dict_arguments['email'].strip().lower()
            dict_arguments['email'] = email
        result = FieldsDALValidateDictArgs(
            dict_arguments,
            *[table[x] for x in table.fields if x in ["first_name", "last_name", "email", "fone_number", "password_hash"]] + [
                Field(
                    'password',
                    'string',
                    requires=IS_EQUAL_TO(
                        dict_arguments['password_repeat'], error_message=self.T("The passwords isn't equals"))),
                Field(
                    'password_repeat',
                    'string',
                    requires=IS_EQUAL_TO(
                        dict_arguments['password'], error_message=self.T("The passwords isn't equals"))),
            ]
        )
        r = result.validate_and_insert(self.DALDatabase.auth_user)
        if r and r.id:
            id_user = r.id
            q_user = self.DALDatabase(self.DALDatabase.auth_user.id == id_user).select().first()
            if id_user == 1:
                role = "root"
                id_role = self.DALDatabase(self.DALDatabase.auth_group.role == 'root').select().first()
                if id_role:
                    self.DALDatabase.auth_membership.insert(
                        auth_user=1,
                        auth_group=id_role.id
                    )
            else:
                role = "user"
                self.DALDatabase.auth_membership.insert(auth_user=id_user, auth_group=3)
            t_user = Serialize(
                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire']
            )
            content_user = {
                'id': str(id_user),
                'email': dict_arguments['email']
            }
            token_user = t_user.dumps(content_user)
            token_user = token_user.decode('utf-8')
            token_client = self.phanterpwa_client_token
            id_client = self.DALDatabase.client.update_or_insert(auth_user=id_user)
            t_client = Serialize(
                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                self.projectConfig['BACKEND'][self.app_name]['default_time_client_token_expire']
            )
            t_url = URLSafeSerializer(
                self.projectConfig['BACKEND'][self.app_name]["secret_key"],
                salt="url_secret_key"
            )
            content_client = {
                'id_user': str(id_user),
                'id_client': str(id_client),
                'user_agent': self.phanterpwa_user_agent,
                'remote_addr': self.phanterpwa_remote_ip
            }
            token_url = t_url.dumps(content_client)
            token_client = t_client.dumps(content_client)
            token_client = token_client.decode('utf-8')
            q_client = self.DALDatabase(self.DALDatabase.client.id == id_client).select().first()
            q_client.update_record(
                token=token_client,
                date_created=datetime.now()
            )
            r_client = self.DALDatabase(self.DALDatabase.client.token == self.phanterpwa_client_token).select().first()
            if r_client:
                r_client.delete_record()
            if not q_user.permit_mult_login:
                r_client = self.DALDatabase(
                    (self.DALDatabase.client.auth_user == id_user)
                    & (self.DALDatabase.client.token != self.phanterpwa_client_token)
                ).select()
                if r_client:
                    r_client = self.DALDatabase(
                        (self.DALDatabase.client.auth_user == id_user)
                        & (self.DALDatabase.client.token != self.phanterpwa_client_token)
                    ).remove()
            self.DALDatabase.commit()
            user_image = PhanterpwaGalleryUserImage(id_user, self.DALDatabase, self.projectConfig)
            self.set_status(201)
            roles = ["user"]
            role = "user"
            q_role = self.DALDatabase(
                (self.DALDatabase.auth_membership.auth_user == id_user)
                & (self.DALDatabase.auth_group.id == self.DALDatabase.auth_membership.auth_group)
            ).select(
                self.DALDatabase.auth_group.id, self.DALDatabase.auth_group.role, orderby=self.DALDatabase.auth_group.grade
            )
            dict_roles = {x.id: x.role for x in q_role}
            roles_id = [x.id for x in q_role]
            return self.write({
                'status': 'Created',
                'code': 201,
                'message': 'The user has been added',
                'authorization': token_user,
                'client_token': token_client,
                'url_token': token_url,
                'auth_user': {
                    'id': id_user,
                    'first_name': E(dict_arguments['first_name']),
                    'last_name': E(dict_arguments['last_name']),
                    'email': dict_arguments['email'],
                    'remember_me': q_client.remember_me,
                    'fone_number': q_user.fone_number,
                    'roles': roles,
                    'role': role,
                    'dict_roles': dict_roles,
                    'roles_id': roles_id,
                    'activated': q_user.activated,
                    'image': user_image.id_image,
                    'two_factor': q_user.two_factor_login,
                    'multiple_login': q_user.permit_mult_login,
                    'locale': q_user.locale,
                    'social_login': None
                },
                'i18n': {
                    'message': self.T('The user has been added'),
                    'auth_user': {
                        'role': self.T(role)
                    }
                }
            })
        else:
            message = self.T('The form has errors')

            i18n_errors = {}
            for x in result.errors:
                tran = self.T(result.errors[x])
                i18n_errors[x] = tran
            i18n = {
                'message': self.T(message),
                'errors': i18n_errors
            }
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': message,
                'errors': result.errors,
                'i18n': i18n,
            })

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})


class RequestAccount(web.RequestHandler):
    """
        url: '/api/auth/request-password/'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, Translator_email, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.i18nTranslator = i18nTranslator
        self.Translator_email = Translator_email
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip

    def check_origin(self, origin):
        return True

    @requires_no_authentication()
    @check_public_csrf_token(form_identify="phanterpwa-form-request_password")
    def post(self, *args, **kargs):
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        request_by_phone = False
        if dict_arguments.get("mobile", False):
            request_by_phone = True
            fone_number = dict_arguments.get("mobile")
            numbers = [str(x) for x in range(10)]
            new_mobile = ""
            for n in fone_number:
                if n in numbers:
                    new_mobile += n
            email = "{0}.mobile@phanterpwa.com".format(new_mobile)
            dict_arguments['email'] = email
            dict_arguments['fone_number'] = new_mobile
            if len(new_mobile) < 4 or len(new_mobile) > 15:
                self.set_status(400)
                return self.write({
                    'status': 'Bad Request',
                    'code': 400,
                    'message': 'Invalid mobile number',
                    'i18n': {
                        'message': self.T('Invalid mobile number')
                    }
                })
            else:
                q_user = self.DALDatabase(self.DALDatabase.auth_user.fone_number == fone_number).select().first()
                now = datetime.now()
                t_expires = self.projectConfig['BACKEND'][self.app_name]['default_time_temporary_password_expire']
                t_wait = self.projectConfig['BACKEND'][self.app_name]['timeout_to_resend_temporary_password_mail']
                delta_time_wait = timedelta(seconds=t_expires)
                if t_expires > t_wait:
                    delta_time_wait = timedelta(seconds=t_expires - t_wait)
                if not q_user:
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': 'The user was not found',
                        'i18n': {'message': self.T('The user was not found')}
                    })
                elif q_user.timeout_to_resend_temporary_password_mail and\
                    now < (q_user.timeout_to_resend_temporary_password_mail - delta_time_wait):
                    t_delta = (q_user.timeout_to_resend_temporary_password_mail - delta_time_wait) - now
                    msg = "Please, wait approximately {time_next_attempt} to try again."
                    tna = int(t_delta.total_seconds())
                    message = msg.format(time_next_attempt=humanize_seconds(tna))
                    message_i18n = self.T(msg).format(time_next_attempt=humanize_seconds(tna, self.i18nTranslator))
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': message,
                        'i18n': {'message': message_i18n}
                    })
                else:
                    new_password = temporary_password()
                    self.Translator_sms.direct_translation = self.phanterpwa_language
                    keys_formatter = dict(
                        app_name=self.projectConfig['PROJECT']['name'],
                        user_name="{0} {1}".format(q_user.first_name, q_user.last_name),
                        password=new_password,
                        time_expires=humanize_seconds(
                            self.projectConfig['BACKEND'][self.app_name]['default_time_temporary_password_expire'],
                            self.Translator_sms
                        ),
                        copyright=interpolate(self.projectConfig['CONTENT_EMAILS']['copyright'], {'now': datetime.now().year}),
                        link_to_your_page=self.projectConfig['CONTENT_EMAILS']['link_to_your_site']
                    )
                    sms_password.text.formatter(keys_formatter)
                    text_sms = sms_password.text.html(
                        minify=True,
                        translate=True,
                        formatter=keys_formatter,
                        i18nInstance=self.Translator_sms,
                        dictionary=self.phanterpwa_language,
                        do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                        escape_string=False
                    )
                    if self.SMSSender:
                        e_sms = self.SMSSender(
                            q_user.fone_number,
                            identify="request-password",
                            text_message=text_sms,
                            app_name=self.app_name,
                            projectConfig=self.projectConfig
                        )
                    else:
                        raise SyntaxError("The SMSSender is indefined")
                    result = ""
                    try:
                        if self.projectConfig["PROJECT"]["debug"]:
                            self.logger_api.warning("TEMPORARY PASSWORD: {0}".format(new_password))
                        else:
                            self.logger_api.warning("SMS to '{0}' -> Temporary Password Recovery: {2}".format(
                                q_user.fone_number,
                                new_password
                            ))
                            e_sms.send()
                    except Exception as e:
                        result = "SMS to '{0}' don't send! -> Error: {1} -> Temporary Password: {2}".format(
                            fone_number,
                            e,
                            new_password
                        )
                        self.logger_api.error(result, exc_info=True)
                        message = "There was an error trying to send the sms."
                        message_i18n = self.T("There was an error trying to send the sms.")
                        self.DALDatabase.rollback()
                        self.set_status(400)
                        return self.write({
                            'status': 'Bad Request',
                            'code': 400,
                            'message': message,
                            'i18n': {'message': message_i18n}
                        })
                    else:
                        pass_hash = pbkdf2_sha512.hash("password{0}{1}".format(
                            new_password, self.projectConfig['BACKEND'][self.app_name]['secret_key']))
                        q_user.update_record(
                            temporary_password_hash=pass_hash,
                            temporary_password_expire=datetime.now() +
                                timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['default_time_temporary_password_expire']),
                            timeout_to_resend_temporary_password_mail=datetime.now() +
                                timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['timeout_to_resend_temporary_password_mail'])
                        )
                        self.DALDatabase.commit()
                        message = 'An email was sent instructing you how to proceed to recover your account.'
                        self.set_status(200)
                        return self.write({
                            'status': 'OK',
                            'code': 200,
                            'message': message,
                            'i18n': {
                                'message': self.T(message)
                            }
                        })


        else:
            result = FieldsDALValidateDictArgs(
                dict_arguments,
                Field(
                    'email',
                    'string',
                    requires=IS_EMAIL(
                        dict_arguments.get('email', None), error_message="The email isn't valid.")),
            )
            r = result.validate()
            if r:
                message = 'The form has errors'

                i18n_errors = {}
                for x in result.errors:
                    tran = self.T(result.errors[x])
                    i18n_errors[x] = tran
                self.set_status(400)
                return self.write({
                    'status': 'Bad Request',
                    'code': 400,
                    'message': message,
                    'errors': result.errors,
                    'i18n': {
                        'message': self.T(message),
                        'errors': i18n_errors
                    }
                })
            else:
                q_user = self.DALDatabase(self.DALDatabase.auth_user.email == dict_arguments['email']).select().first()
                now = datetime.now()
                t_expires = self.projectConfig['BACKEND'][self.app_name]['default_time_temporary_password_expire']
                t_wait = self.projectConfig['BACKEND'][self.app_name]['timeout_to_resend_temporary_password_mail']
                delta_time_wait = timedelta(seconds=t_expires)
                if t_expires > t_wait:
                    delta_time_wait = timedelta(seconds=t_expires - t_wait)
                if not q_user:
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': 'The user was not found',
                        'i18n': {'message': self.T('The user was not found')}
                    })
                elif q_user.timeout_to_resend_temporary_password_mail and\
                    now < (q_user.timeout_to_resend_temporary_password_mail - delta_time_wait):
                    t_delta = (q_user.timeout_to_resend_temporary_password_mail - delta_time_wait) - now
                    msg = "Please, wait approximately {time_next_attempt} to try again."
                    tna = int(t_delta.total_seconds())
                    message = msg.format(time_next_attempt=humanize_seconds(tna))
                    message_i18n = self.T(msg).format(time_next_attempt=humanize_seconds(tna, self.i18nTranslator))
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': message,
                        'i18n': {'message': message_i18n}
                    })
                else:
                    new_password = temporary_password()
                    self.Translator_email.direct_translation = self.phanterpwa_language
                    keys_formatter = dict(
                        app_name=self.projectConfig['PROJECT']['name'],
                        user_name="{0} {1}".format(q_user.first_name, q_user.last_name),
                        password=new_password,
                        time_expires=humanize_seconds(
                            self.projectConfig['BACKEND'][self.app_name]['default_time_temporary_password_expire'],
                            self.Translator_email
                        ),
                        copyright=interpolate(self.projectConfig['CONTENT_EMAILS']['copyright'], {'now': datetime.now().year}),
                        link_to_your_page=self.projectConfig['CONTENT_EMAILS']['link_to_your_site']
                    )
                    email_password.text.formatter(keys_formatter)
                    text_email = email_password.text.html(
                        minify=True,
                        translate=True,
                        formatter=keys_formatter,
                        i18nInstance=self.Translator_email,
                        dictionary=self.phanterpwa_language,
                        do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                        escape_string=False
                    )

                    html_email = email_password.html.html(
                        minify=True,
                        translate=True,
                        formatter=keys_formatter,
                        i18nInstance=self.Translator_email,
                        dictionary=self.phanterpwa_language,
                        do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                        escape_string=False
                    )

                    e_mail = MailSender(
                        self.projectConfig['EMAIL']['default_sender'],
                        self.projectConfig['EMAIL']['password'],
                        dict_arguments['email'],
                        subject="Temporary Password Recovery",
                        text_message=text_email,
                        html_message=html_email,
                        server=self.projectConfig['EMAIL']['server'],
                        port=self.projectConfig['EMAIL']['port'],
                        use_tls=self.projectConfig['EMAIL']['use_tls'],
                        use_ssl=self.projectConfig['EMAIL']['use_ssl']
                    )
                    result = ""
                    try:
                        if self.projectConfig["PROJECT"]["debug"]:
                            self.logger_api.warning("TEMPORARY PASSWORD: {0}".format(new_password))
                        else:
                            self.logger_api.warning("Email from '{0}' to '{1}' -> Temporary Password Recovery: {2}".format(
                                self.projectConfig['EMAIL']['default_sender'],
                                dict_arguments['email'],
                                new_password
                            ))
                            e_mail.send()
                    except Exception as e:
                        result = "Email from '{0}' to '{1}' don't send! -> Error: {2} -> Temporary Password: {3}".format(
                            self.projectConfig['EMAIL']['default_sender'], dict_arguments['email'], e, new_password)
                        self.logger_api.error(result, exc_info=True)
                        message = "There was an error trying to send the email."
                        message_i18n = self.T("There was an error trying to send the email.")
                        self.set_status(400)
                        return self.write({
                            'status': 'Bad Request',
                            'code': 400,
                            'message': message,
                            'i18n': {'message': message_i18n}
                        })
                    else:
                        pass_hash = pbkdf2_sha512.hash("password{0}{1}".format(
                            new_password, self.projectConfig['BACKEND'][self.app_name]['secret_key']))
                        q_user.update_record(
                            temporary_password_hash=pass_hash,
                            temporary_password_expire=datetime.now() +
                                timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['default_time_temporary_password_expire']),
                            timeout_to_resend_temporary_password_mail=datetime.now() +
                                timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['timeout_to_resend_temporary_password_mail'])
                        )
                        self.DALDatabase.commit()
                        message = 'An email was sent instructing you how to proceed to recover your account.'
                        self.set_status(200)
                        return self.write({
                            'status': 'OK',
                            'code': 200,
                            'message': message,
                            'i18n': {
                                'message': self.T(message)
                            }
                        })

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})


class ActiveAccount(web.RequestHandler):
    """
        url: '/api/auth/active-account/'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, Translator_email, SMSSender=None, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.SMSSender = SMSSender
        self.DALDatabase = DALDatabase
        self.i18nTranslator = i18nTranslator
        self.Translator_email = Translator_email
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "phanterpwa-authorization,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip

    def check_origin(self, origin):
        return True

    @check_user_token(ignore_activation=True)
    def get(self, *args, **kargs):
        now = datetime.now()
        t_expires = self.projectConfig['BACKEND'][self.app_name]['default_time_activation_code_expire']
        t_wait = self.projectConfig['BACKEND'][self.app_name]['timeout_to_resend_activation_email']
        delta_time_wait = timedelta(seconds=t_expires)
        if t_expires > t_wait:
            delta_time_wait = timedelta(seconds=t_expires - t_wait)

        if not self.phanterpwa_current_user:
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': 'The user was not found',
                'i18n': {'message': self.T('The user was not found')}
            })
        elif self.phanterpwa_current_user.activated:
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': 'Account is activated',
                'i18n': {'message': self.T('Account is activated')}
            })            
        elif self.phanterpwa_current_user.timeout_to_resend_activation_email and\
            now < (self.phanterpwa_current_user.timeout_to_resend_activation_email - delta_time_wait):
            t_delta = (self.phanterpwa_current_user.timeout_to_resend_activation_email - delta_time_wait) - now
            msg = "Please, wait approximately {time_next_attempt} to try again."
            tna = int(t_delta.total_seconds())
            message = msg.format(time_next_attempt=humanize_seconds(tna))
            message_i18n = self.T(msg).format(time_next_attempt=humanize_seconds(tna, self.i18nTranslator))
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': message,
                'i18n': {'message': message_i18n}
            })
        else:
            if compiled_mobilemail.match(self.phanterpwa_current_user.email):
                activation_code = generate_activation_code()
                self.Translator_email.direct_translation = self.phanterpwa_language
                keys_formatter = dict(
                    app_name=self.projectConfig['PROJECT']['name'],
                    code=activation_code,
                )
                text_sms = sms_activation_code.text.html(
                    minify=True,
                    translate=True,
                    formatter=keys_formatter,
                    i18nInstance=self.Translator_email,
                    dictionary=self.phanterpwa_language,
                    do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                    escape_string=False
                )
                if self.SMSSender:
                    e_sms = self.SMSSender(
                        self.phanterpwa_current_user.fone_number,
                        identify="two-factor-authentication-code",
                        text_message=text_sms,
                        app_name=self.app_name,
                        projectConfig=self.projectConfig
                    )
                else:
                    raise SyntaxError("The SMSSender is indefined")
                result = ""
                try:
                    if self.projectConfig["PROJECT"]["debug"]:
                        self.logger_api.warning("ACTIVATION CODE: {0}".format(activation_code))
                        e_sms.send()
                    else:
                        self.logger_api.warning("SMS to '{0}' -> Activation Code: {1}".format(
                            self.phanterpwa_current_user.fone_number,
                            activation_code
                        ))
                        e_sms.send()
                except Exception as e:
                    result = "SMS to '{0}' don't send! -> Error: {1} -> Activation Code: {2}".format(
                        self.phanterpwa_current_user.fone_number,
                        e,
                        activation_code
                    )
                    self.logger_api.error(result, exc_info=True)
                    message = "There was an error trying to send the sms."
                    message_i18n = self.T("There was an error trying to send the sms.")
                    self.DALDatabase.rollback()
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': message,
                        'i18n': {'message': message_i18n}
                    })
                else:
                    self.phanterpwa_current_user.update_record(
                        activation_code_by_mobile=activation_code.split("-")[0],
                        timeout_to_resend_activation_email=datetime.now() +
                            timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['default_time_activation_code_expire'])
                    )
                    self.DALDatabase.commit()
                    message = 'An sms was sent instructing you how to proceed to activate your account.'
                    self.set_status(200)
                    return self.write({
                        'status': 'OK',
                        'code': 200,
                        'message': message,
                        'email': self.phanterpwa_current_user.email,
                        'i18n': {
                            'message': self.T(message)
                        }
                    })

            else:
                activation_code = generate_activation_code()
                self.Translator_email.direct_translation = self.phanterpwa_language
                keys_formatter = dict(
                    app_name=self.projectConfig['PROJECT']['name'],
                    user_name="{0} {1}".format(
                        self.phanterpwa_current_user.first_name,
                        self.phanterpwa_current_user.last_name
                    ),
                    code=activation_code,
                    time_expires=humanize_seconds(
                        self.projectConfig['BACKEND'][self.app_name]['default_time_activation_code_expire'],
                        self.Translator_email
                    ),
                    copyright=interpolate(self.projectConfig['CONTENT_EMAILS']['copyright'], {'now': datetime.now().year}),
                    link_to_your_page=self.projectConfig['CONTENT_EMAILS']['link_to_your_site']
                )
                email_password.text.formatter(keys_formatter)
                text_email = email_activation_code.text.html(
                    minify=True,
                    translate=True,
                    formatter=keys_formatter,
                    i18nInstance=self.Translator_email,
                    dictionary=self.phanterpwa_language,
                    do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                    escape_string=False
                )
                html_email = email_activation_code.html.html(
                    minify=True,
                    translate=True,
                    formatter=keys_formatter,
                    i18nInstance=self.Translator_email,
                    dictionary=self.phanterpwa_language,
                    do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                    escape_string=False
                )

                e_mail = MailSender(
                    self.projectConfig['EMAIL']['default_sender'],
                    self.projectConfig['EMAIL']['password'],
                    self.phanterpwa_current_user.email,
                    subject="Activation code",
                    text_message=text_email,
                    html_message=html_email,
                    server=self.projectConfig['EMAIL']['server'],
                    port=self.projectConfig['EMAIL']['port'],
                    use_tls=self.projectConfig['EMAIL']['use_tls'],
                    use_ssl=self.projectConfig['EMAIL']['use_ssl']
                )
                result = ""
                try:
                    if self.projectConfig["PROJECT"]["debug"]:
                        self.logger_api.warning("ACTIVATION CODE: {0}".format(activation_code))
                    else:
                        self.logger_api.warning("Email from '{0}' to '{1}' -> Activation Code: {2}".format(
                            self.projectConfig['EMAIL']['default_sender'],
                            self.phanterpwa_current_user.email,
                            activation_code
                        ))
                        e_mail.send()
                except Exception as e:
                    result = "Email from '%s' to '%s' don't send! -> Error: %s -> Activation Code: %s" %\
                        (self.projectConfig['EMAIL']['default_sender'], self.phanterpwa_current_user.email, e, activation_code)
                    self.logger_api.error(result, exc_info=True)
                    message = "There was an error trying to send the email."
                    message_i18n = self.T("There was an error trying to send the email.")
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': message,
                        'i18n': {'message': message_i18n}
                    })
                else:
                    self.phanterpwa_current_user.update_record(
                        activation_code=activation_code.split("-")[0],
                        timeout_to_resend_activation_email=datetime.now() +
                            timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['default_time_activation_code_expire'])
                    )
                    self.DALDatabase.commit()
                    message = 'An email was sent instructing you how to proceed to activate your account.'
                    self.set_status(200)
                    return self.write({
                        'status': 'OK',
                        'code': 200,
                        'message': message,
                        'email': self.phanterpwa_current_user.email,
                        'i18n': {
                            'message': self.T(message)
                        }
                    })

    @check_private_csrf_token(form_identify="phanterpwa-form-activation", ignore_activation=True)
    def post(self, *args, **kargs):
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        activation_code = dict_arguments.get("activation_code", None)
        active_by_mobile = False
        if activation_code and self.phanterpwa_current_user:
            q_user = self.phanterpwa_current_user
            if q_user.activated:
                q_role = self.DALDatabase(
                    (self.DALDatabase.auth_membership.auth_user == q_user.id) &
                    (self.DALDatabase.auth_group.id == self.DALDatabase.auth_membership.auth_group)
                ).select(
                    self.DALDatabase.auth_group.id, self.DALDatabase.auth_group.role, orderby=self.DALDatabase.auth_group.grade
                )
                roles = [x.role for x in q_role]
                dict_roles = {x.id: x.role for x in q_role}
                roles_id = [x.id for x in q_role]
                role = None
                if roles:
                    role = roles[-1]
                q_client = self.DALDatabase(
                    (self.DALDatabase.client.auth_user == q_user.id) &
                    (self.DALDatabase.client.token == self.phanterpwa_client_token)
                ).select().first()
                user_image = PhanterpwaGalleryUserImage(q_user.id, self.DALDatabase, self.projectConfig)
                self.set_status(200)
                return self.write({
                    'status': 'OK',
                    'code': 200,
                    'auth_user': {
                        'id': q_user.id,
                        'first_name': E(q_user.first_name),
                        'last_name': E(q_user.last_name),
                        'email': q_user.email,
                        'remember_me': q_client.remember_me,
                        'fone_number': q_user.fone_number,
                        'roles': roles,
                        'role': role,
                        'dict_roles': dict_roles,
                        'roles_id': roles_id,
                        'activated': q_user.activated,
                        'image': user_image.id_image,
                        'two_factor': q_user.two_factor_login,
                        'multiple_login': q_user.permit_mult_login,
                        'locale': q_user.locale,
                        'social_login': None
                    },
                    'message': 'Account is activated',
                    'i18n': {
                        'message': self.T('Account is activated'),
                        'auth_user': {'role': self.T(role)}
                    }
                })
            else:
                if not q_user.activation_attempts:
                    q_user.update_record(activation_attempts=1)
                else:
                    q_user.update_record(activation_attempts=q_user.activation_attempts + 1)
                result = None
                checked_code = None
                try:
                    checked_code = check_activation_code(
                        activation_code
                    )
                except Exception:
                    self.logger_api.error("Problem on check activation code", exc_info=True)
                code = None
                if checked_code:
                    code = checked_code.split("-")[0]
                if code and q_user.activation_code == code:
                    result = True
                    active_by_mobile = False
                elif code and q_user.activation_code_by_mobile == code:
                    result = True
                    active_by_mobile = True
                if q_user.activation_attempts > self.projectConfig['BACKEND'][self.app_name]['max_activation_attempts']:
                    if q_user.datetime_next_attempt_to_activate and\
                            datetime.now() <= q_user.datetime_next_attempt_to_activate:
                        t_delta = q_user.datetime_next_attempt_to_activate - datetime.now()
                        msg = "Please, wait approximately {time_next_attempt} to try again."
                        tna = int(t_delta.total_seconds())
                        message = msg.format(time_next_attempt=humanize_seconds(tna))
                        message_i18n = self.T(msg).format(time_next_attempt=humanize_seconds(tna, self.i18nTranslator))
                        self.DALDatabase.commit()
                        self.set_status(400)
                        return self.write({
                            'status': 'Bad Request',
                            'code': 400,
                            'message': message,
                            'activation_attempts': q_user.activation_attempts,
                            'i18n': {
                                'message': message_i18n,
                            }
                        })
                    else:
                        q_user.update_record(activation_attempts=1)
                if result:
                    if compiled_mobilemail.match(q_user.email) or active_by_mobile:
                        q_user.update_record(
                            activation_attempts=0,
                            activated=True,
                            fone_number_activated=True,
                            activation_code=None,
                            activation_code_by_mobile=None,
                            timeout_to_resend_activation_email=None
                        )
                    else:
                        q_user.update_record(
                            email_activated=True,
                            activation_attempts=0,
                            activated=True,
                            activation_code=None,
                            timeout_to_resend_activation_email=None
                        )

                    q_role = self.DALDatabase(
                        (self.DALDatabase.auth_membership.auth_user == q_user.id) &
                        (self.DALDatabase.auth_group.id == self.DALDatabase.auth_membership.auth_group)
                    ).select(
                        self.DALDatabase.auth_group.id, self.DALDatabase.auth_group.role, orderby=self.DALDatabase.auth_group.grade
                    )
                    roles = [x.role for x in q_role]
                    dict_roles = {x.id: x.role for x in q_role}
                    roles_id = [x.id for x in q_role]
                    role = None
                    if roles:
                        role = roles[-1]
                    q_client = self.DALDatabase(
                        (self.DALDatabase.client.auth_user == q_user.id) &
                        (self.DALDatabase.client.token == self.phanterpwa_client_token)
                    ).select().first()
                    self.DALDatabase.commit()
                    user_image = PhanterpwaGalleryUserImage(q_user.id, self.DALDatabase, self.projectConfig)
                    self.set_status(200)
                    return self.write({
                        'status': 'OK',
                        'code': 200,
                        'auth_user': {
                            'id': q_user.id,
                            'first_name': E(q_user.first_name),
                            'last_name': E(q_user.last_name),
                            'email': q_user.email,
                            'remember_me': q_client.remember_me,
                            'fone_number': q_user.fone_number,
                            'roles': roles,
                            'role': role,
                            'dict_roles': dict_roles,
                            'roles_id': roles_id,
                            'activated': q_user.activated,
                            'image': user_image.id_image,
                            'two_factor': q_user.two_factor_login,
                            'multiple_login': q_user.permit_mult_login,
                            'locale': q_user.locale,
                            'social_login': None
                        },
                        'message': 'The Account has been activated',
                        'i18n': {
                            'message': self.T('The Account has been activated'),
                            'auth_user': {'role': self.T(role)}
                        }
                    })
                else:
                    q_user.update_record(
                        datetime_next_attempt_to_activate=datetime.now() +
                            timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['wait_time_to_try_activate_again'])
                    )
                    msg = 'Wrong activation code! Attempt {attempt_number} from {max_attempts}'
                    message = msg.format(
                        attempt_number=q_user.activation_attempts,
                        max_attempts=self.projectConfig['BACKEND'][self.app_name]['max_activation_attempts']
                    )
                    message_i18n = self.T(msg).format(
                        attempt_number=q_user.activation_attempts,
                        max_attempts=self.projectConfig['BACKEND'][self.app_name]['max_activation_attempts']
                    )
                    self.DALDatabase.commit()
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': message,
                        'activation_attempts': q_user.activation_attempts,
                        'i18n': {'message': message_i18n}
                    })
        else:
            self.set_status(401)
            return self.write({
                'status': 'Unauthorized',
                'code': 401,
                'message': 'Invalid activation code',
                'i18n': {
                    'message': self.T('Invalid activation code')
                }
            })

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})


class ChangePassword(web.RequestHandler):
    """
        url: '/api/auth/change-password'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.i18nTranslator = i18nTranslator
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "phanterpwa-authorization,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip

    def check_origin(self, origin):
        return True

    @check_private_csrf_token(form_identify="phanterpwa-form-change_password")
    def post(self):
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        password, new_password, new_password_repeat = dict_arguments['edata'].split(":")
        password = base64.b64decode(password).decode('utf-8')
        new_password = base64.b64decode(new_password).decode('utf-8')
        new_password_repeat = base64.b64decode(new_password_repeat).decode('utf-8')
        pass_hash = pbkdf2_sha512.hash("password{0}{1}".format(
            new_password, self.projectConfig['BACKEND'][self.app_name]['secret_key']))
        dict_arguments['password'] = "password{0}{1}".format(
            password, self.projectConfig['BACKEND'][self.app_name]['secret_key'])

        if self.phanterpwa_current_user.login_attempts >= self.projectConfig['BACKEND'][self.app_name]['max_login_attempts']:
            if self.phanterpwa_current_user.datetime_next_attempt_to_login and\
                    (datetime.now() <= self.phanterpwa_current_user.datetime_next_attempt_to_login):
                t_delta = self.phanterpwa_current_user.datetime_next_attempt_to_login - datetime.now()
                msg = "Please, wait approximately {time_next_attempt} to try again."
                tna = int(t_delta.total_seconds())
                message = msg.format(time_next_attempt=humanize_seconds(tna))
                message_i18n = self.T(msg).format(time_next_attempt=humanize_seconds(tna, self.i18nTranslator))
                self.DALDatabase.commit()
                self.set_status(400)
                self.logger_api.warning("{0}:{1} - {2}".format(self.phanterpwa_current_user.email, password, message))
                return self.write({
                    'status': 'Bad Request',
                    'code': 400,
                    'message': message,
                    'login_attempts': self.phanterpwa_current_user.login_attempts,
                    'i18n': {
                        'message': message_i18n,
                    }
                })
            else:
                self.phanterpwa_current_user.update_record(login_attempts=0)

        check_passwords = FieldsDALValidateDictArgs(
            dict_arguments,
            Field('password',
                'string',
                requires=VALID_PASSWORD(
                    self.phanterpwa_current_user, error_message=self.T('The password is not valid!')
                )
            ),
            Field(
                'new_password',
                'string',
                requires=IS_EQUAL_TO(
                    new_password_repeat, error_message=self.T("The new passwords isn't equals"))),
            Field(
                'new_password_repeat',
                'string',
                requires=IS_EQUAL_TO(
                    new_password, error_message=self.T("The new passwords isn't equals"))),

        )
        r = check_passwords.validate()
        password_fail = True
        if r:
            if not self.phanterpwa_current_user.login_attempts:
                self.phanterpwa_current_user.update_record(login_attempts=1)
            else:
                self.phanterpwa_current_user.update_record(
                    login_attempts=self.phanterpwa_current_user.login_attempts + 1)
            self.phanterpwa_current_user.update_record(
                datetime_next_attempt_to_login=datetime.now() +
                    timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['timeout_to_next_login_attempt'])
            )
            self.phanterpwa_current_user.login_attempts
            self.projectConfig['BACKEND'][self.app_name]['max_login_attempts']
            message = 'The form has errors. Attempt {0} to {1}'
            msg_i18n = self.T(message).format(
                self.phanterpwa_current_user.login_attempts, self.projectConfig['BACKEND'][self.app_name]['max_login_attempts'])
            msg = message.format(
                self.phanterpwa_current_user.login_attempts, self.projectConfig['BACKEND'][self.app_name]['max_login_attempts'])
            i18n_errors = {}
            for x in check_passwords.errors:
                tran = self.T(check_passwords.errors[x])
                i18n_errors[x] = tran
            self.DALDatabase.commit()
            self.set_status(400)
            return self.write({
                'status': 'Bad Requests',
                'code': 400,
                'message': msg,
                'i18n': {
                    'message': msg_i18n
                }
            })
        else:

            self.phanterpwa_current_user.update_record(
                login_attempts=0,
                password_hash=pass_hash
            )
            self.DALDatabase.commit()
            self.set_status(200)
            return self.write({
                'status': 'OK',
                'code': 200,
                'message': 'Password changed!',
                'i18n': {
                    'message': self.T('Password changed!'),
                }
            })

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})


class SMSGateway(web.RequestHandler):
    """
        url: '/api/auth/sms-gateway'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, Translator_email, SMSSender=None, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.Translator_email = Translator_email
        self.i18nTranslator = i18nTranslator
        self.SMSSender = SMSSender
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-sms-token,",
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip
        self.phanterpwa_form_identify = None

    def check_origin(self, origin):
        return True

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})

    def get(self, *args, **kargs):
        if args[0] == "config":
            sms_config = {
                'prefix': 55,
                'prefix_list': [55],
                'mask': "(##) # ####-####"
            }

            self.set_status(200)
            return self.write({
                "status": "OK",
                "config": sms_config
            })

    def post(self, *args, **kargs):
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        authorization_token = self.request.headers.get('phanterpwa-sms-token')
        args0 = args[0]
        if authorization_token:
            token_content = None
            sms_sender_serialize = Serialize(
                self.projectConfig['BACKEND'][self.app_name]["secret_key"],
                salt="sms_token"
            )
            try:
                token_content = sms_sender_serialize.loads(authorization_token)
            except BadSignature:
                token_content = None
            except SignatureExpired:
                token_content = None
            if token_content and 'id_user' in token_content:
                id_user = token_content['id_user']
                q_user = self.DALDatabase(self.DALDatabase.auth_user.id == id_user).select().first()
                if q_user:
                    """
                        put your sms gateway here and send the message 
                    """
                    mobile = dict_arguments.get("mobile", None)
                    text = dict_arguments.get("text", None)
                    self.logger_api.warning("{0} - {1}\n{2}\n{3}\n\n{4}".format(
                        mobile,
                        "Sending sms message not implemented yet!",
                        args0,
                        str(mobile),
                        str(text)
                    ))
                    self.set_status(200)
                    return self.write({
                        'status': 'OK',
                        'code': 200,
                        'message': 'Message sent',
                        'i18n': {
                            'message': self.T('Message sent')
                        }
                    })
        self.set_status(400)
        return self.write({
            'status': 'Bad Request',
            'code': 400,
            'message': 'Invalid SMS authorization',
            'i18n': {
                'message': self.T('Invalid SMS authorization')
            }
        })
