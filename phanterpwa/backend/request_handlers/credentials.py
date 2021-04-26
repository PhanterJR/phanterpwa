from phanterpwa.backend.decorators import (
    check_application,
    check_client_token,
    check_user_token
)
from phanterpwa.i18n import browser_language
from phanterpwa.third_parties.xss import xssescape as E
from phanterpwa.captchasvg.captcha import Captcha
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

from datetime import (
    datetime,
    timedelta
)


class SignClient(web.RequestHandler):
    """
        /api/client/
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
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
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

    @check_application()
    def get(self, *args, **kargs):
        self.phanterpwa_client_token = self.request.headers.get('phanterpwa-client-token')
        self.phanterpwa_authorization = self.request.headers.get('phanterpwa-authorization')
        t_client = Serialize(
            self.projectConfig['BACKEND'][self.app_name]['secret_key'],
            self.projectConfig['BACKEND'][self.app_name]['default_time_client_token_expire']
        )
        t_url = URLSafeSerializer(
            self.projectConfig['BACKEND'][self.app_name]['secret_key'],
            salt="url_secret_key"
        )
        msg = 'The client does not have a client-token, a new one has been generated.'
        q = None
        if self.phanterpwa_client_token:
            q = self.DALDatabase(self.DALDatabase.client.token == self.phanterpwa_client_token).select().first()
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
                    if token_content_client['user_agent'] == self.phanterpwa_user_agent:
                        if 'id_user' in token_content_client:
                            token_url = t_url.dumps({**token_content_client})
                            if self.phanterpwa_authorization:
                                t_user = Serialize(
                                    self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                                    self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire']
                                )
                                token_content_user = None
                                try:
                                    token_content_user = t_user.loads(self.phanterpwa_authorization)
                                except BadSignature:
                                    token_content_user = None
                                except SignatureExpired:
                                    token_content_user = None
                                if token_content_user and 'id' in token_content_user:
                                    id_user = token_content_user['id']
                                    q_user = self.DALDatabase(self.DALDatabase.auth_user.id == id_user).select().first()
                                    q_client = self.DALDatabase(
                                        (self.DALDatabase.client.auth_user == id_user) &
                                        (self.DALDatabase.client.token == self.phanterpwa_client_token)
                                    ).select().first()
                                    if q_user and q_client:
                                        msg = "".join(['The client-token is valid and belongs ',
                                            'to a login user, will be reused.'])
                                        time_resing_client = int(
                                            self.projectConfig['BACKEND'][self.app_name]['default_time_client_token_expire'] * 0.8) + 1
                                        if q_client.date_created +\
                                                timedelta(seconds=time_resing_client) < datetime.now():
                                            new_client = self.DALDatabase.client.insert(
                                                auth_user=q_client.auth_user,
                                                remember_me=q_client.remember_me,
                                                last_resign=datetime.now(),
                                                date_created=datetime.now()
                                            )
                                            content = {
                                                'id_user': str(q_user.id),
                                                "id_client": str(new_client),
                                                'user_agent': self.phanterpwa_user_agent,
                                                'remote_addr': self.phanterpwa_remote_ip,
                                            }
                                            token_url = t_url.dumps(content)
                                            token_client = t_client.dumps(content)
                                            token_client = token_client.decode("utf-8")
                                            q_client.delete_record()
                                            q_client = self.DALDatabase(
                                                self.DALDatabase.client.id == new_client).select().first()
                                            q_client.update_record(
                                                token=token_client
                                            )
                                            self.phanterpwa_client_token = token_client
                                            msg = "".join(['The client-token is valid and belongs ',
                                                'to a login user, but a new one has been generated.'])
                                        if not q_user.permit_mult_login:
                                            self.DALDatabase(
                                                (self.DALDatabase.client.auth_user == id_user) &
                                                (self.DALDatabase.client.token != self.phanterpwa_client_token)
                                            ).delete()
                                        q_role = self.DALDatabase(
                                            (self.DALDatabase.auth_membership.auth_user == q_user.id) &
                                            (self.DALDatabase.auth_group.id ==
                                                self.DALDatabase.auth_membership.auth_group)
                                        ).select(
                                            self.DALDatabase.auth_group.id,
                                            self.DALDatabase.auth_group.role,
                                            orderby=self.DALDatabase.auth_group.grade
                                        )
                                        roles = [x.role for x in q_role]
                                        dict_roles = {x.id: x.role for x in q_role}
                                        role = None
                                        if roles:
                                            role = roles[-1]
                                        self.DALDatabase.commit()
                                        user_image = PhanterpwaGalleryUserImage(
                                            q_user.id, self.DALDatabase, self.projectConfig)
                                        self.set_status(200)
                                        return self.write({
                                            'status': 'OK',
                                            'code': 200,
                                            'message': msg,
                                            'auth_user': {
                                                'id': q_user.id,
                                                'first_name': E(q_user.first_name),
                                                'last_name': E(q_user.last_name),
                                                'email': q_user.email,
                                                'remember_me': q_client.remember_me,
                                                'roles': roles,
                                                'role': role,
                                                'dict_roles': dict_roles,
                                                'activated': q_user.activated,
                                                'image': user_image.id_image,
                                                'two_factor': q_user.two_factor_login,
                                                'multiple_login': q_user.permit_mult_login,
                                                'locale': q_user.locale,
                                                'social_login': None
                                            },
                                            'i18n': {
                                                'message': self.T(msg),
                                                'auth_user': {
                                                    'role': self.T(role)
                                                }
                                            },
                                            'client_token': self.phanterpwa_client_token,
                                            'url_token': token_url,
                                        })
                            else:
                                msg = "".join(['The client-token is valid and belongs ',
                                    'to a logout user, will be reused.'])
                                self.set_status(200)
                                return self.write({
                                    'status': 'OK',
                                    'code': 200,
                                    'message': msg,
                                    'auth_user': 'logout',
                                    'i18n': {
                                        'message': self.T(msg),
                                        'auth_user': self.T('logout')
                                    },
                                    'client_token': self.phanterpwa_client_token,
                                    'url_token': token_url,
                                })
                        else:
                            msg = 'The client-token is valid and anonymous, will be reused'
                            self.set_status(200)
                            return self.write({
                                'status': 'OK',
                                'code': 200,
                                'message': msg,
                                'auth_user': 'anonymous',
                                'i18n': {
                                    'message': self.T(msg),
                                    'auth_user': self.T('anonymous')
                                },
                                'client_token': self.phanterpwa_client_token
                            })
                    else:
                        msg = "".join(['The client-token is valid but appears to ',
                            'belong to another client, a new one has been generated.'])
                else:
                    if self.phanterpwa_authorization:
                        t_user = Serialize(
                            self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                            self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire']
                        )
                        token_content_user = None
                        try:
                            token_content_user = t_user.loads(self.phanterpwa_authorization)
                        except BadSignature:
                            token_content_user = None
                        except SignatureExpired:
                            token_content_user = None
                        if token_content_user and 'id' in token_content_user:
                            id_user = token_content_user['id']
                            if int(token_content_user['id']) == int(id_user):
                                q_user = self.DALDatabase(self.DALDatabase.auth_user.id == id_user).select().first()
                                if q_user:
                                    content = {
                                        'id_user': str(q_user.id),
                                        "id_client": str(q.id),
                                        'user_agent': self.phanterpwa_user_agent,
                                        'remote_addr': self.phanterpwa_remote_ip,
                                    }
                                    token_url = t_url.dumps(content)
                                    token_client = t_client.dumps(content)
                                    token_client = token_client.decode('utf-8')
                                    q.update_record(
                                        token=token_client,
                                        id_user=q_user.id,
                                        date_created=datetime.now()
                                    )
                                    if not q_user.permit_mult_login:
                                        self.DALDatabase(
                                            (self.DALDatabase.client.auth_user == id_user) &
                                            (self.DALDatabase.client.token != self.phanterpwa_client_token)
                                        ).delete()
                                    q_role = self.DALDatabase(
                                        (self.DALDatabase.auth_membership.auth_user == q_user.id) &
                                        (self.DALDatabase.auth_group.id == self.DALDatabase.auth_membership.auth_group)
                                    ).select(
                                        self.DALDatabase.auth_group.id,
                                        self.DALDatabase.auth_group.role,
                                        orderby=self.DALDatabase.auth_group.grade
                                    )
                                    roles = [x.role for x in q_role]
                                    dict_roles = {x.id: x.role for x in q_role}
                                    role = None
                                    if roles:
                                        role = roles[-1]
                                    self.DALDatabase.commit()
                                    msg = "".join(['The client token is valid but expired, ',
                                        'a new one has been generated.'])
                                    user_image = PhanterpwaGalleryUserImage(
                                        q_user.id, self.DALDatabase, self.projectConfig)
                                    self.set_status(200)
                                    return self.write({
                                        'status': 'OK',
                                        'code': 200,
                                        'message': msg,
                                        'auth_user': {
                                            'id': q_user.id,
                                            'first_name': E(q_user.first_name),
                                            'last_name': E(q_user.last_name),
                                            'email': q_user.email,
                                            'remember_me': q.remember_me,
                                            'roles': roles,
                                            'role': role,
                                            'dict_roles': dict_roles,
                                            'activated': q_user.activated,
                                            'image': user_image.id_image,
                                            'two_factor': q_user.two_factor_login,
                                            'multiple_login': q_user.permit_mult_login,
                                            'locale': q_user.locale,
                                            'social_login': None
                                        },
                                        'i18n': {
                                            'message': self.T(msg),
                                            'auth_user': {
                                                'role': self.T(role)
                                            }
                                        },
                                        'client_token': token_client,
                                        'url_token': token_url
                                    })
                    else:
                        msg = 'The client have a invalid client-token, a new one has been generated.'
                        q.delete_record()
            else:
                msg = 'The client have a invalid client-token, not found, a new one has been generated.'

        if q:
            id_client = q.id
        else:
            id_client = self.DALDatabase.client.insert(date_created=datetime.now())

        content = {
            "id_client": id_client,
            'user_agent': self.phanterpwa_user_agent,
            'remote_addr': self.phanterpwa_remote_ip
        }
        token_client = t_client.dumps(content)
        token_client = token_client.decode('utf-8')
        q_client = self.DALDatabase(self.DALDatabase.client.id == id_client).select(self.DALDatabase.client.id).first()
        if q_client:
            q_client.update_record(token=token_client)
        self.DALDatabase.commit()
        self.set_status(200)
        return self.write({
            'status': 'OK',
            'code': 200,
            'message': msg,
            'auth_user': 'anonymous',
            'i18n': {
                'message': self.T(msg),
                'auth_user': self.T('anonymous')
            },
            'client_token': token_client
        })

    def options(self, *args):
        self.set_status(200)
        return self.write({"status": "OK"})


class SignForms(web.RequestHandler):
    """
        url: '/api/signforms/<form_identify>'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, i18nTranslator=None, logger_api=None, list_forms=[]):
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
        self.list_forms = [*{
            "phanterpwa-form-activation",
            "phanterpwa-form-profile",
            "phanterpwa-form-change_password",
            "phanterpwa-form-change_account",
            "phanterpwa-form-auth_user",
            "phanterpwa-form-auth_group",
            *list_forms
        }]

    def check_origin(self, origin):
        return True

    @check_user_token(ignore_activation=True)
    def get(self, *args, **kargs):
        """
        Receive request to create and response with a token csrf or captcha
        """
        form_identify = args[0]
        list_forms = self.list_forms

        id_client = int(self.phanterpwa_client_token_checked["id_client"])
        if form_identify in list_forms:
            self.DALDatabase((self.DALDatabase.csrf.client == id_client) &
                (self.DALDatabase.csrf.form_identify == form_identify)).delete()
            t = Serialize(
                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                self.projectConfig['BACKEND'][self.app_name]['default_time_csrf_token_expire']
            )
            id_csrf = self.DALDatabase.csrf.insert(
                form_identify=form_identify,
                user_agent=self.phanterpwa_user_agent,
                ip=self.phanterpwa_remote_ip,
                client=id_client
            )
            if id_csrf:
                sign_captha = t.dumps({
                    'id': str(id_csrf),
                    'form_identify': form_identify,
                    'user_agent': self.phanterpwa_user_agent,
                    'ip': self.phanterpwa_remote_ip,
                    'user': self.phanterpwa_current_user.id
                })
                sign_captha = sign_captha.decode("utf-8")
                q_csrf = self.DALDatabase(self.DALDatabase.csrf.id == id_csrf).select().first()
                q_csrf.update_record(token=sign_captha)
                msg = "Form signed"
                self.DALDatabase.commit()
                self.set_status(200)
                return self.write({
                    "status": "OK",
                    "code": 200,
                    "message": msg,
                    "i18n": {
                        "message": self.T(msg)
                    },
                    "csrf": sign_captha
                })
        self.DALDatabase.commit()
        msg = "The form can't sign"
        self.set_status(400)
        return self.write({
            "status": "Bad Request",
            "code": 400,
            "message": msg,
            "i18n": {
                "message": self.T(msg)
            }
        })

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})


class SignLockForm(web.RequestHandler):
    """
        url: '/api/signlockform/'
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
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip

    def check_origin(self, origin):
        return True

    @check_client_token()
    def get(self, *args, **kargs):
        """
        Receive request to create and response with a token csrf or captcha
        """
        form_identify = "user_locked"
        id_client = int(self.phanterpwa_client_token_checked["id_client"])
        if self.phanterpwa_current_client and self.phanterpwa_current_client.locked:
            self.DALDatabase((self.DALDatabase.csrf.client == id_client) &
                (self.DALDatabase.csrf.form_identify == form_identify)).delete()
            t = Serialize(
                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                self.projectConfig['BACKEND'][self.app_name]['default_time_csrf_token_expire']
            )
            id_csrf = self.DALDatabase.csrf.insert(
                form_identify=form_identify,
                user_agent=self.phanterpwa_user_agent,
                ip=self.phanterpwa_remote_ip,
                client=id_client
            )
            if id_csrf:
                sign_captha = t.dumps({
                    'id': str(id_csrf),
                    'form_identify': form_identify,
                    'user_agent': self.phanterpwa_user_agent,
                    'ip': self.phanterpwa_remote_ip
                })
                sign_captha = sign_captha.decode("utf-8")
                q_csrf = self.DALDatabase(self.DALDatabase.csrf.id == id_csrf).select().first()
                q_csrf.update_record(token=sign_captha)
            msg = "Form signed"
            self.DALDatabase.commit()
            self.set_status(200)
            return self.write({
                "status": "OK",
                "code": 200,
                "message": msg,
                "i18n": {
                    "message": self.T(msg)
                },
                "csrf": sign_captha
            })
        else:
            self.DALDatabase.commit()
            msg = "The form can't sign, the user is not locked."
            self.set_status(400)
            return self.write({
                "status": "Bad Request",
                "code": 400,
                "message": msg,
                "i18n": {
                    "message": self.T(msg)
                }
            })

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})


class SignCaptchaForms(web.RequestHandler):
    """
        url: '/api/signcaptchaforms/<form_identify>'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, Translator_captcha, i18nTranslator=None, logger_api=None, list_forms=[]):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.i18nTranslator = i18nTranslator
        self.Translator_captcha = Translator_captcha
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
        if self.Translator_captcha:
            self.Translator_captcha.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip
        self.list_forms = [*{
            "phanterpwa-form-login",
            "phanterpwa-form-register",
            "phanterpwa-form-request_password",
            "phanterpwa-form-login401",
            *list_forms
        }]

    def check_origin(self, origin):
        return True

    @check_client_token()
    def get(self, *args, **kargs):
        """
        Receive request to create and response with a token csrf or captcha
        """

        form_identify = args[0]
        list_forms = self.list_forms
        id_client = int(self.phanterpwa_client_token_checked["id_client"])
        if form_identify in list_forms:
            self.DALDatabase((self.DALDatabase.captcha.client == id_client) &
                (self.DALDatabase.captcha.form_identify == form_identify)).delete()
            captcha = Captcha(
                form_identify,
                secret_key=self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                time_token_expire=self.projectConfig['BACKEND'][self.app_name]['default_time_csrf_token_expire'],
                translator=self.Translator_captcha
            )
            html_captcha = captcha.html.xml()
            signature = captcha.signature
            self.DALDatabase.captcha.insert(
                token=signature,
                form_identify=form_identify,
                user_agent=self.phanterpwa_user_agent,
                ip=self.phanterpwa_remote_ip,
                date_created=datetime.now(),
                client=id_client
            )
            self.DALDatabase.commit()
            self.set_status(200)
            return self.write({
                "status": "OK",
                "code": 200,
                "captcha": html_captcha,
                "signature": signature,
                "message": "Captcha send",
                "i18n": {
                    "message": self.T("Captcha send")
                }
            })
        else:
            self.DALDatabase.commit()
            self.set_status(400)
            return self.write({
                "status": "Bad Request",
                "code": 400,
                "message": "The form can't sign",
                "i18n": {
                    "message": self.T("The form can't sign")
                }
            })

    @check_client_token()
    def post(self, *args, **kargs):
        """
        Receive captcha user choice and response with csrf token
        """
        form_identify = args[0]
        list_forms = self.list_forms
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        choice = dict_arguments['user_choice']
        sign = dict_arguments['signature']
        id_client = int(self.phanterpwa_client_token_checked["id_client"])
        q_captcha = self.DALDatabase(self.DALDatabase.captcha.token == sign).select().first()
        if q_captcha:
            self.DALDatabase((self.DALDatabase.captcha.client == id_client) &
                (self.DALDatabase.captcha.form_identify == form_identify)).delete()
            self.DALDatabase((self.DALDatabase.csrf.client == id_client) &
                (self.DALDatabase.csrf.form_identify == form_identify)).delete()
            q_captcha.delete_record()
            captcha = Captcha(
                form_identify,
                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                self.projectConfig['BACKEND'][self.app_name]['default_time_csrf_token_expire'],
                translator=self.Translator_captcha
            )

            if captcha.check(sign, choice):
                id_csrf = self.DALDatabase.csrf.insert(
                    form_identify=form_identify,
                    user_agent=self.phanterpwa_user_agent,
                    ip=self.phanterpwa_remote_ip,
                    client=id_client
                )
                if id_csrf:
                    t = Serialize(
                        self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                        self.projectConfig['BACKEND'][self.app_name]['default_time_csrf_token_expire']
                    )
                    sign_captha = t.dumps({
                        'id': str(id_csrf),
                        'form_identify': form_identify,
                        'user_agent': self.phanterpwa_user_agent,
                        'ip': self.phanterpwa_remote_ip
                    })
                    sign_captha = sign_captha.decode("utf-8")
                    q_csrf = self.DALDatabase(self.DALDatabase.csrf.id == id_csrf).select().first()
                    q_csrf.update_record(token=sign_captha)
                self.DALDatabase.commit()
                self.set_status(200)
                return self.write({
                    "status": "OK",
                    "code": 200,
                    "message": "Captcha resolved",
                    "i18n": {
                        "message": self.T("Captcha resolved")
                    },
                    "captcha": captcha.html_ok.xml(),
                    "csrf": sign_captha
                })
            else:

                id_client = int(self.phanterpwa_client_token_checked["id_client"])
                if form_identify in list_forms:
                    self.DALDatabase((self.DALDatabase.captcha.client == id_client) &
                        (self.DALDatabase.captcha.form_identify == form_identify)).delete()
                    captcha = Captcha(
                        form_identify,
                        secret_key=self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                        time_token_expire=self.projectConfig['BACKEND'][self.app_name]['default_time_csrf_token_expire'],
                        translator=self.Translator_captcha
                    )
                    html_captcha = captcha.html.xml()
                    signature = captcha.signature
                    self.DALDatabase.captcha.insert(
                        token=signature,
                        form_identify=form_identify,
                        user_agent=self.phanterpwa_user_agent,
                        ip=self.phanterpwa_remote_ip,
                        date_created=datetime.now(),
                        client=id_client
                    )
                    self.DALDatabase.commit()
                    self.set_status(400)
                    return self.write({
                        "status": "Bad Request",
                        "code": 400,
                        "captcha": html_captcha,
                        "signature": signature,
                        "message": "Incorrect captcha",
                        "i18n": {
                            "message": self.T("Incorrect captcha")
                        }
                    })
                else:
                    self.DALDatabase.commit()
                    self.set_status(400)
                    return self.write({
                        "status": "Bad Request",
                        "code": 400,
                        "message": "Incorrect captcha",
                        "i18n": {
                            "message": self.T("Incorrect captcha")
                        }
                    })
        else:
            self.DALDatabase.commit()
            self.set_status(400)
            return self.write({
                "status": "Bad Request",
                "code": 400,
                "message": "Incorrect captcha, not found.",
                "i18n": {
                    "message": self.T("Incorrect captcha, not found.")
                }
            })

    def options(self, *args, **kargs):
        self.set_status(200)
        return self.write({"status": "OK"})


class ReSing(web.RequestHandler):
    """
        url: '/api/resigncredentials/''
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

    @check_user_token()
    def get(self, *args, **kargs):
        q_client = self.DALDatabase(self.DALDatabase.client.token == self.phanterpwa_client_token).select().first()
        remember_me = q_client.remember_me
        timeout_to_resign = self.projectConfig['BACKEND'][self.app_name]["timeout_to_resign"]
        time_resing_client = int(
            self.projectConfig['BACKEND'][self.app_name]['default_time_client_token_expire'] * 0.8) + 1
        if remember_me:
            timeout_to_resign = int(
                self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire_remember_me'] * 0.8) + 1
        t_client = Serialize(
            self.projectConfig['BACKEND'][self.app_name]['secret_key'],
            self.projectConfig['BACKEND'][self.app_name]['default_time_client_token_expire']
        )
        t_url = URLSafeSerializer(
            self.projectConfig['BACKEND'][self.app_name]['secret_key'],
            salt="url_secret_key"
        )
        if q_client.last_resign is None or ((q_client.last_resign +
                    timedelta(seconds=timeout_to_resign)) < datetime.now()):
            timeout_token_user = self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire']
            if remember_me:
                timeout_token_user = self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire_remember_me']
            t_user = Serialize(
                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                timeout_token_user
            )
            content_client = {
                'id_user': str(self.phanterpwa_current_user.id),
                "id_client": str(q_client.id),
                'user_agent': self.phanterpwa_user_agent,
                'remote_addr': self.phanterpwa_remote_ip,
            }
            content_user = {
                'id': str(self.phanterpwa_current_user.id),
                'email': self.phanterpwa_current_user.email
            }
            token_user = t_user.dumps(content_user)
            token_user = token_user.decode('utf-8')
            token_client = self.phanterpwa_client_token
            token_url = t_url.dumps(content_client)
            msg = 'Re-sign just user token'
            q_client.update_record(
                last_resign=datetime.now()
            )
            if not self.phanterpwa_current_user.permit_mult_login:
                self.DALDatabase(
                    (self.DALDatabase.client.auth_user == self.phanterpwa_current_user.id) &
                    (self.DALDatabase.client.token != self.phanterpwa_client_token)
                ).delete()
            self.DALDatabase.commit()
            self.set_status(200)
            return self.write({
                "status": "OK",
                'message': msg,
                'authorization': token_user,
                'client_token': token_client,
                'url_token': token_url,
                "i18n": {
                    "message": self.T(msg)
                }
            })
        elif q_client.date_created +\
                timedelta(seconds=time_resing_client) < datetime.now():
            q_client.delete_record()
            timeout_token_user = self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire']
            if remember_me:
                timeout_token_user = self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire_remember_me']
            t_user = Serialize(
                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                timeout_token_user
            )
            new_client = self.DALDatabase.client.insert(
                auth_user=q_client.auth_user,
                remember_me=q_client.remember_me,
                last_resign=datetime.now(),
                date_created=datetime.now()
            )
            content = {
                'id_user': str(self.phanterpwa_current_user.id),
                "id_client": str(new_client),
                'user_agent': self.phanterpwa_user_agent,
                'remote_addr': self.phanterpwa_remote_ip,
            }
            content_user = {
                'id': str(self.phanterpwa_current_user.id),
                'email': self.phanterpwa_current_user.email
            }
            token_user = t_user.dumps(content_user)
            token_user = token_user.decode('utf-8')
            token_url = t_url.dumps(content)
            token_client = t_client.dumps(content)
            token_client = token_client.decode("utf-8")
            q_client.delete_record()
            q_client = self.DALDatabase(self.DALDatabase.client.id == new_client).select().first()
            q_client.update_record(
                token=token_client
            )
            self.phanterpwa_client_token = token_client
            msg = 'Re-sign client token, user token and url token'
            if not self.phanterpwa_current_user.permit_mult_login:
                self.DALDatabase(
                    (self.DALDatabase.client.auth_user == self.phanterpwa_current_user.id) &
                    (self.DALDatabase.client.token != self.phanterpwa_client_token)
                ).delete()
            self.DALDatabase.commit()
            self.set_status(200)
            return self.write({
                "status": "OK",
                'message': msg,
                'authorization': token_user,
                'client_token': token_client,
                'url_token': token_url,
                "i18n": {
                    "message": self.T(msg)
                }
            })
        else:
            msg = "This is not the time to re-sign"
            self.set_status(202)
            return self.write({
                'status': 'Accepted',
                'message': msg,
                "i18n": {
                    "message": self.T(msg)
                }
            })

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})
