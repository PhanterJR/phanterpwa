import os
import urllib.request
import base64
import json
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
    email_two_factor_code
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
from phanterpwa.backend.security import (
    Serialize,
    SignatureExpired,
    BadSignature,
    URLSafeSerializer,
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


class CAS(web.RequestHandler):
    """
        url: '/api/cas/'
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
                "phanterpwa-cas-authorization,"
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT, DELETE')
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

    def _request_summary(self) -> str:
        client_ip = self.request.headers.get('X-Real-IP') or\
            self.request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or\
            self.request.remote_ip
        summary = "{0} {1} ({2})".format(
            self.request.method,
            self.request.uri,
            client_ip,
        )
        if hasattr(self, "phanterpwa_current_user") and self.phanterpwa_current_user is not None:
            summary = "{0} {1} ({2} - {3})".format(
                self.request.method,
                self.request.uri,
                client_ip,
                self.phanterpwa_current_user.email
            )
        return summary

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})

    @check_cas_token()
    def get(self):
        self.write({
            "status": "OK",
            "message": "Hello World!",
            "project": self.projectConfig["PROJECT"]
        })


    @check_public_csrf_token(form_identify=[
        "phanterpwa-form-login", "user_locked", "phanterpwa-form-request_password"])
    def post(self, *args):
        self.phanterpwa_authorization = self.request.headers.get('phanterpwa-authorization')
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}

        if dict_arguments.get('edata'):
            used_temporary = None
            edata = dict_arguments['edata']
            email, password = edata.split(":")
            email = base64.b64decode(email).decode('utf-8').strip().lower()
            password = base64.b64decode(password).decode('utf-8')
            q_user = self.DALDatabase(self.DALDatabase.auth_user.email == email).select().first()
            if q_user:
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
                    content = {
                        'id': str(q_user.id),
                        'email': email
                    }
                    token_user = t_user.dumps(content)
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

                    if (q_user.two_factor_login or two_factor) and not used_temporary and not self.phanterpwa_form_identify=="user_locked":
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
                        email_password.text.formatter(keys_formatter)
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
                                self.logger_api.warning("Email from '{0}' to '{1}' -> Activation Code: {2}".format(
                                    self.projectConfig['EMAIL']['default_sender'],
                                    q_user.email,
                                    two_factor_code
                                ))
                                e_mail.send()
                        except Exception as e:
                            result = "Email from '{0}' to '{1}' don't send! -> Error: {2} -> password: {3}".format(
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
                    q_user.update_record(
                        temporary_password_expire=datetime.now() +
                            timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['default_time_temporary_password_expire']),
                        datetime_next_attempt_to_login=datetime.now() +
                            timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['timeout_to_next_login_attempt'])
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
                self.set_status(401)
                return self.write({
                    'status': 'Unauthorized',
                    'code': 401,
                    'message': 'Invalid password or email',
                    'i18n': {
                        'message': self.T('Invalid password or email')
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
                    msg = 'The client have a invalid client-token, a new one has been generated.'
                    token_content_client = None
                except SignatureExpired:
                    msg = 'The client have a expired client-token, a new one has been generated.'
                    token_content_client = None
                if token_content_client:
                    sessions = []
                    q_sessions = db(db.client.auth_user==self.phanterpwa_current_user.id).select(orderby=db.client.date_created)
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
                            except:
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
                                    agent = user_agent_parse(user_agent),
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

