import asyncio
import sqlite3
from functools import wraps
from .security import (
    Serialize,
    SignatureExpired,
    BadSignature,
    URLSafeSerializer,
)
from inspect import currentframe, getframeinfo, getfile


def async_retry_on_locked(max_retries=3, delay=0.1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    if "locked" in str(e) and attempt < max_retries - 1:
                        await asyncio.sleep(delay * (2 ** attempt))  # ✅ Async sleep
                        continue
                    raise
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def check_application():
    def decorator(f):
        @wraps(f)
        def check_application_decorator(self, *args, **kargs):

            if not hasattr(self, "phanterpwa_client_application_checked"):
                self.phanterpwa_client_application_checked = None
                project_name = self.projectConfig['PROJECT']['name']
                project_version = self.projectConfig['PROJECT']['version']
                self.phanterpwa_application = self.request.headers.get('phanterpwa-application')
                self.phanterpwa_application_version = self.request.headers.get('phanterpwa-application-version')
                if self.phanterpwa_application == project_name:
                    if self.phanterpwa_application_version != project_version:
                        msg = 'The client needs update ({0}).'
                        dict_response = {
                            'status': 'Conflict',
                            'code': 409,
                            'specification': 'client needs update',
                            'message': msg.format(project_version),
                            'i18n': {
                                'message': self.i18nTranslator.T(msg).format(project_version)
                                    if self.i18nTranslator else msg.format(project_version)
                            }
                        }
                        fi = getframeinfo(currentframe())
                        if not self.projectConfig['PROJECT']['debug']:
                            help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                                getfile(self.__class__),
                                self.__class__.__name__,
                                f.__name__,
                                fi.filename,
                                fi.function,
                                fi.lineno + 19
                            )
                        else:
                            msg = "".join([msg.format(project_version),
                                " The client version '{0}' is different of project version '{1}'".format(
                                    self.phanterpwa_application_version, project_version)])
                            dict_response['message'] = msg
                            help_debug = "{0}.{1}@{2}:{3}".format(
                                self.__class__.__name__,
                                f.__name__,
                                fi.function,
                                fi.lineno + 19
                            )
                        dict_response['help_debug'] = help_debug
                        self.set_status(400)
                        return self.write(dict_response)
                else:
                    msg = 'The client is not compatible.'
                    dict_response = {
                        'status': 'Bad Request',
                        'code': 400,
                        'message': msg,
                        'i18n': {
                            'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                        },
                        'project_path': self.projectConfig['PROJECT']['path']
                    }
                    fi = getframeinfo(currentframe())
                    if not self.projectConfig['PROJECT']['debug']:
                        help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                            getfile(self.__class__),
                            self.__class__.__name__,
                            f.__name__,
                            fi.filename,
                            fi.function,
                            fi.lineno + 19
                        )
                    else:
                        msg = "".join([msg,
                            " The client name '{0}' is different of project name '{1}'".format(
                                self.phanterpwa_application, project_name)])
                        dict_response['message'] = msg
                        help_debug = "{0}.{1}@{2}:{3}".format(
                            self.__class__.__name__,
                            f.__name__,
                            fi.function,
                            fi.lineno + 19
                        )
                    dict_response['help_debug'] = help_debug
                    self.set_status(400)
                    return self.write(dict_response)
                self.phanterpwa_client_application_checked = {
                    'name': self.phanterpwa_application,
                    'version': self.phanterpwa_application_version
                }
                return f(self, *args, **kargs)
            else:
                return f(self, *args, **kargs)
        return check_application_decorator
    return decorator


def check_client_token(ignore_locked=True):
    def decorator(f):
        @wraps(f)
        @check_application()
        def check_client_token_decorator(self, *args, **kargs):
            if not hasattr(self, "phanterpwa_client_token_checked"):
                self.phanterpwa_current_client = None
                self.phanterpwa_client_token_checked = None
                self.phanterpwa_authorization_checked = None
                self.phanterpwa_client_token = self.request.headers.get('phanterpwa-client-token')
                self.phanterpwa_authorization = self.request.headers.get('phanterpwa-authorization')
                self.phanterpwa_user_agent = self.request.headers.get('User-Agent')
                if not self.phanterpwa_client_token:
                    msg = 'Client token is not in the header. "phanterpwa-client-token"'
                    dict_response = {
                        'status': 'Bad Request',
                        'code': 400,
                        'message': msg,
                        'i18n': {
                            'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                        }
                    }
                    fi = getframeinfo(currentframe())
                    if not self.projectConfig['PROJECT']['debug']:
                        help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                            getfile(self.__class__),
                            self.__class__.__name__,
                            f.__name__,
                            fi.filename,
                            fi.function,
                            fi.lineno + 19
                        )
                    else:
                        help_debug = "{0}.{1}@{2}:{3}".format(
                            self.__class__.__name__,
                            f.__name__,
                            fi.function,
                            fi.lineno + 19
                        )
                    dict_response['help_debug'] = help_debug
                    self.set_status(400)
                    return self.write(dict_response)
                t = Serialize(
                    self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                    self.projectConfig['BACKEND'][self.app_name]['default_time_client_token_expire']
                )
                self.DALDatabase._adapter.reconnect()
                q = self.DALDatabase(self.DALDatabase.client.token == self.phanterpwa_client_token).select().first()
                if q:
                    token_content = None
                    try:
                        token_content = t.loads(self.phanterpwa_client_token)
                    except BadSignature:
                        token_content = None
                    except SignatureExpired:
                        token_content = None
                    if token_content:
                        if "user_agent" in token_content and "id_client" in token_content:
                            if token_content['user_agent'] == self.phanterpwa_user_agent and\
                                int(token_content['id_client']) == q.id:
                                if self.phanterpwa_authorization:
                                    t_user = Serialize(
                                        self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                                        self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire']
                                    )
                                    token_content_user = None
                                    id_user = None
                                    try:
                                        token_content_user = t_user.loads(self.phanterpwa_authorization)
                                    except BadSignature:
                                        token_content_user = None
                                    except SignatureExpired:
                                        token_content_user = None
                                    if token_content_user and 'id' in token_content_user:
                                        self.phanterpwa_authorization_checked = token_content_user
                                        id_user = token_content_user['id']
                                    if id_user and 'id_user' in token_content and id_user == token_content['id_user']:
                                        self.phanterpwa_client_token_checked = token_content
                                else:
                                    self.phanterpwa_client_token_checked = token_content

                if self.phanterpwa_client_token_checked:
                    if q and q.locked and not ignore_locked:
                        msg = "The user has locked your session!"
                        dict_response = {
                            'status': 'Unauthorized',
                            'code': 401,
                            'specification': 'client locked',
                            'message': msg,
                            'i18n': {
                                'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                            }
                        }
                        fi = getframeinfo(currentframe())
                        if not self.projectConfig['PROJECT']['debug']:
                            help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                                getfile(self.__class__),
                                self.__class__.__name__,
                                f.__name__,
                                fi.filename,
                                fi.function,
                                fi.lineno + 19
                            )
                        else:
                            help_debug = "{0}.{1}@{2}:{3}".format(
                                self.__class__.__name__,
                                f.__name__,
                                fi.function,
                                fi.lineno + 19
                            )
                        dict_response['help_debug'] = help_debug
                        self.set_status(401)
                        return self.write(dict_response)
                    self.phanterpwa_current_client = q
                    return f(self, *args, **kargs)
                else:
                    if q:
                        q.delete_record()
                        self.DALDatabase.commit()
                    msg = "The phanterpwa-client-token is invalid!"
                    dict_response = {
                        'status': 'Unauthorized',
                        'code': 401,
                        'specification': 'client deleted',
                        'message': msg,
                        'i18n': {
                            'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                        }
                    }
                    fi = getframeinfo(currentframe())
                    if not self.projectConfig['PROJECT']['debug']:
                        help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                            getfile(self.__class__),
                            self.__class__.__name__,
                            f.__name__,
                            fi.filename,
                            fi.function,
                            fi.lineno + 19
                        )
                    else:
                        help_debug = "{0}.{1}@{2}:{3}".format(
                            self.__class__.__name__,
                            f.__name__,
                            fi.function,
                            fi.lineno + 19
                        )
                    dict_response['help_debug'] = help_debug
                    self.set_status(401)
                    return self.write(dict_response)
            else:
                return f(self, *args, **kargs)
        return check_client_token_decorator
    return decorator


def check_cas_token(ignore_locked=True):
    def decorator(f):
        @wraps(f)
        def check_cas_token_decorator(self, *args, **kargs):
            self.phanterpwa_cas_token_checked = None
            self.phanterpwa_cas_authorization = self.request.headers.get('phanterpwa-cas-authorization')
            if not self.phanterpwa_cas_authorization:
                msg = 'CAS authorization is not in the header. "phanterpwa-cas-authorization"'
                dict_response = {
                    'status': 'Bad Request',
                    'code': 400,
                    'message': msg,
                    'i18n': {
                        'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                    }
                }
                fi = getframeinfo(currentframe())
                if not self.projectConfig['PROJECT']['debug']:
                    help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                        getfile(self.__class__),
                        self.__class__.__name__,
                        f.__name__,
                        fi.filename,
                        fi.function,
                        fi.lineno + 19
                    )
                else:
                    help_debug = "{0}.{1}@{2}:{3}".format(
                        self.__class__.__name__,
                        f.__name__,
                        fi.function,
                        fi.lineno + 19
                    )
                dict_response['help_debug'] = help_debug
                self.set_status(400)
                return self.write(dict_response)
            t = Serialize(
                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                self.projectConfig['BACKEND'][self.app_name]['default_time_cas_token_expire']
            )
            self.DALDatabase._adapter.reconnect()
            q = self.DALDatabase(self.DALDatabase.apps_authorization.authorization == self.phanterpwa_cas_authorization).select().first()
            if q:
                token_content = None
                try:
                    token_content = t.loads(self.phanterpwa_cas_authorization)
                except BadSignature:
                    token_content = None
                except SignatureExpired:
                    token_content = None
                if token_content:
                    if "user_agent" in token_content and "id_client" in token_content:
                        if token_content['app_name'] == q.app_name:
                            self.phanterpwa_cas_token_checked = token_content

            if self.phanterpwa_cas_token_checked:
                return f(self, *args, **kargs)
            else:
                if q:
                    q.delete_record()
                    self.DALDatabase.commit()
                msg = "The phanterpwa-cas-authorization is invalid!"
                dict_response = {
                    'status': 'Unauthorized',
                    'code': 401,
                    'specification': 'cas deleted',
                    'message': msg,
                    'i18n': {
                        'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                    }
                }
                fi = getframeinfo(currentframe())
                if not self.projectConfig['PROJECT']['debug']:
                    help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                        getfile(self.__class__),
                        self.__class__.__name__,
                        f.__name__,
                        fi.filename,
                        fi.function,
                        fi.lineno + 19
                    )
                else:
                    help_debug = "{0}.{1}@{2}:{3}".format(
                        self.__class__.__name__,
                        f.__name__,
                        fi.function,
                        fi.lineno + 19
                    )
                dict_response['help_debug'] = help_debug
                self.set_status(401)
                return self.write(dict_response)

        return check_cas_token_decorator
    return decorator


def check_url_token(ignore_user_agent=False):
    def decorator(f):
        @wraps(f)
        def check_url_token_decorator(self, *args, **kargs):

            dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
            self.phanterpwa_url_token_checked = None
            self.phanterpwa_url_token = dict_arguments.get('sign')
            self.phanterpwa_user_agent = self.request.headers.get('User-Agent')
            if not self.phanterpwa_url_token:
                msg = 'The URL token is not valid.'
                dict_response = {
                    'status': 'Bad Request',
                    'code': 400,
                    'message': msg,
                    'i18n': {
                        'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                    }
                }
                fi = getframeinfo(currentframe())
                if not self.projectConfig['PROJECT']['debug']:
                    help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                        getfile(self.__class__),
                        self.__class__.__name__,
                        f.__name__,
                        fi.filename,
                        fi.function,
                        fi.lineno + 19
                    )
                else:
                    help_debug = "{0}.{1}@{2}:{3}".format(
                        self.__class__.__name__,
                        f.__name__,
                        fi.function,
                        fi.lineno + 19
                    )
                dict_response['help_debug'] = help_debug
                self.set_status(400)
                return self.write(dict_response)
            t = URLSafeSerializer(
                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                salt="url_secret_key"
            )
            self.DALDatabase._adapter.reconnect()
            token_content = None
            try:
                token_content = t.loads(self.phanterpwa_url_token)
            except BadSignature:
                token_content = None
            if token_content:
                if "user_agent" in token_content:
                    if ignore_user_agent:
                        self.phanterpwa_url_token_checked = token_content
                        q_user = self.DALDatabase(self.DALDatabase.auth_user.id == token_content.get("id_user")).select().first()
                        self.phanterpwa_current_user = q_user
                    else:
                        if token_content['user_agent'] == self.phanterpwa_user_agent:
                            q_user = self.DALDatabase(self.DALDatabase.auth_user.id == token_content.get("id_user")).select().first()
                            self.phanterpwa_current_user = q_user
                            self.phanterpwa_url_token_checked = token_content
            if self.phanterpwa_url_token_checked:
                return f(self, *args, **kargs)
            else:
                msg = "The URL token is invalid!"
                dict_response = {
                    'status': 'Forbidden',
                    'code': 403,
                    'message': msg,
                    'i18n': {
                        'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                    }
                }
                fi = getframeinfo(currentframe())
                if not self.projectConfig['PROJECT']['debug']:
                    help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                        getfile(self.__class__),
                        self.__class__.__name__,
                        f.__name__,
                        fi.filename,
                        fi.function,
                        fi.lineno + 19
                    )
                else:
                    help_debug = "{0}.{1}@{2}:{3}".format(
                        self.__class__.__name__,
                        f.__name__,
                        fi.function,
                        fi.lineno + 19
                    )
                dict_response['help_debug'] = help_debug
                self.set_status(403)
                return self.write(dict_response)
        return check_url_token_decorator
    return decorator


def check_public_csrf_token(form_identify=None, ignore_locked=True):
    def decorator(f):
        @wraps(f)
        @check_client_token(ignore_locked=ignore_locked)
        def check_csrf_token_decorator(self, *args, **kargs):
            dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
            self.phanterpwa_csrf_token_content = None
            self.phanterpwa_csrf_token = dict_arguments.get("csrf_token")
            self.phanterpwa_user_agent = self.request.headers.get('User-Agent')
            self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
                self.request.headers.get("X-Forwarded-For") or \
                self.request.remote_ip
            if not self.phanterpwa_csrf_token:
                msg = 'The CSRF token is not in form. "csrf_token"'
                dict_response = {
                    'status': 'Bad Request',
                    'code': 400,
                    'message': msg,
                    'i18n': {
                        'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                    }
                }
                fi = getframeinfo(currentframe())
                if not self.projectConfig['PROJECT']['debug']:
                    help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                        getfile(self.__class__),
                        self.__class__.__name__,
                        f.__name__,
                        fi.filename,
                        fi.function,
                        fi.lineno + 19
                    )
                else:
                    help_debug = "{0}.{1}@{2}:{3}".format(
                        self.__class__.__name__,
                        f.__name__,
                        fi.function,
                        fi.lineno + 19
                    )
                dict_response['help_debug'] = help_debug
                self.set_status(400)
                return self.write(dict_response)
            t = Serialize(
                "csrf-{0}".format(self.projectConfig['BACKEND'][self.app_name]['secret_key']),
                self.projectConfig['BACKEND'][self.app_name]['default_time_csrf_token_expire']
            )
            token_content = None
            try:
                token_content = t.loads(self.phanterpwa_csrf_token)
            except BadSignature:
                token_content = None
            except SignatureExpired:
                token_content = None
            if token_content:
                if 'id' in token_content:
                    self.DALDatabase._adapter.reconnect()
                    q = self.DALDatabase(self.DALDatabase.csrf.id == token_content["id"]).select().first()
                    if q:
                        if (q.token == self.phanterpwa_csrf_token) and\
                                self.phanterpwa_user_agent == q.user_agent and\
                                self.phanterpwa_remote_ip == q.ip:
                            self.phanterpwa_csrf_token_content = token_content
                            q.delete_record()
                            self.DALDatabase.commit()
                            if form_identify:
                                self.phanterpwa_form_identify = token_content["form_identify"]
                                if isinstance(form_identify, str) and form_identify == self.phanterpwa_form_identify:
                                    return f(self, *args, **kargs)
                                elif isinstance(form_identify, (list, tuple)) and \
                                        self.phanterpwa_form_identify in form_identify:
                                    return f(self, *args, **kargs)
                                else:
                                    msg = "".join(["The crsf token is invalid! ",
                                        "The csrf token created for \"{0}\"",
                                        " is being used for a request that only accepts \"{1}\"."
                                        ])
                                    
                                    trans_msg = self.i18nTranslator.T(msg)
                                    msg = msg.format(str(self.phanterpwa_form_identify), str(form_identify))
                                    trans_msg = trans_msg.format(str(self.phanterpwa_form_identify), str(form_identify))
                                    dict_response = {
                                        'status': 'Bad Request',
                                        'code': 400,
                                        'message': msg,
                                        'i18n': {
                                            'message': trans_msg
                                        }
                                    }
                                    fi = getframeinfo(currentframe())
                                    if not self.projectConfig['PROJECT']['debug']:
                                        help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                                            getfile(self.__class__),
                                            self.__class__.__name__,
                                            f.__name__,
                                            fi.filename,
                                            fi.function,
                                            fi.lineno + 19
                                        )
                                    else:
                                        help_debug = "{0}.{1}@{2}:{3}".format(
                                            self.__class__.__name__,
                                            f.__name__,
                                            fi.function,
                                            fi.lineno + 19
                                        )
                                    dict_response['help_debug'] = help_debug
                                    self.set_status(400)
                                    return self.write(dict_response)
                            return f(self, *args, **kargs)
                        else:
                            msg = "The crsf token is invalid! The client has an unstable address."
                            dict_response = {
                                'status': 'Bad Request',
                                'code': 400,
                                'message': msg,
                                'i18n': {
                                    'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                                }
                            }
                            fi = getframeinfo(currentframe())
                            if not self.projectConfig['PROJECT']['debug']:
                                help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                                    getfile(self.__class__),
                                    self.__class__.__name__,
                                    f.__name__,
                                    fi.filename,
                                    fi.function,
                                    fi.lineno + 19
                                )
                            else:
                                help_debug = "{0}.{1}@{2}:{3}".format(
                                    self.__class__.__name__,
                                    f.__name__,
                                    fi.function,
                                    fi.lineno + 19
                                )
                            dict_response['help_debug'] = help_debug
                            self.set_status(400)
                            return self.write(dict_response)
                    else:
                        if self.phanterpwa_user_agent == token_content.get("user_agent") and\
                                self.phanterpwa_remote_ip == token_content.get("ip"):
                            if form_identify:
                                self.phanterpwa_form_identify = token_content["form_identify"]
                                if (isinstance(form_identify, str) and form_identify == self.phanterpwa_form_identify) or \
                                        (isinstance(form_identify, (list, tuple)) and self.phanterpwa_form_identify in form_identify):

                                    msg = "The form has already been processed"
                                    trans_msg = self.i18nTranslator.T(msg)
                                    dict_response = {
                                        'status': 'Accepted',
                                        'code': 202,
                                        'message': msg,
                                        'i18n': {
                                            'message': trans_msg
                                        }
                                    }
                                    fi = getframeinfo(currentframe())
                                    if not self.projectConfig['PROJECT']['debug']:
                                        help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                                            getfile(self.__class__),
                                            self.__class__.__name__,
                                            f.__name__,
                                            fi.filename,
                                            fi.function,
                                            fi.lineno + 19
                                        )
                                    else:
                                        help_debug = "{0}.{1}@{2}:{3}".format(
                                            self.__class__.__name__,
                                            f.__name__,
                                            fi.function,
                                            fi.lineno + 19
                                        )
                                    dict_response['help_debug'] = help_debug
                                    self.set_status(202)
                                    return self.write(dict_response)
                            return f(self, *args, **kargs)
                        else:
                            msg = "The crsf token is invalid! The client has an unstable address."
                            dict_response = {
                                'status': 'Bad Request',
                                'code': 400,
                                'message': msg,
                                'i18n': {
                                    'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                                }
                            }
                            fi = getframeinfo(currentframe())
                            if not self.projectConfig['PROJECT']['debug']:
                                help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                                    getfile(self.__class__),
                                    self.__class__.__name__,
                                    f.__name__,
                                    fi.filename,
                                    fi.function,
                                    fi.lineno + 19
                                )
                            else:
                                help_debug = "{0}.{1}@{2}:{3}".format(
                                    self.__class__.__name__,
                                    f.__name__,
                                    fi.function,
                                    fi.lineno + 19
                                )
                            dict_response['help_debug'] = help_debug
                            self.set_status(400)
                            return self.write(dict_response)
            msg = "The crsf token is invalid!"
            dict_response = {
                'status': 'Bad Request',
                'code': 400,
                'message': msg,
                'i18n': {
                    'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                }
            }
            fi = getframeinfo(currentframe())
            if not self.projectConfig['PROJECT']['debug']:
                help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                    getfile(self.__class__),
                    self.__class__.__name__,
                    f.__name__,
                    fi.filename,
                    fi.function,
                    fi.lineno + 19
                )
            else:
                help_debug = "{0}.{1}@{2}:{3}".format(
                    self.__class__.__name__,
                    f.__name__,
                    fi.function,
                    fi.lineno + 19
                )
            dict_response['help_debug'] = help_debug
            self.set_status(400)
            return self.write(dict_response)
        return check_csrf_token_decorator
    return decorator


def check_user_token(ignore_activation=False):
    def decorator(f):
        @wraps(f)
        @check_client_token(ignore_locked=False)
        def check_user_token_decorator(self, *args, **kargs):
            def phanterpwa_current_user_has_role(obj, role):
                if not obj.phanterpwa_current_user_groups:
                    return False
                if isinstance(role, (list, tuple, set)):
                    if isinstance(role, (list, tuple)):
                        role = set(role)
                    auth_user_roles = set([x.role for x in obj.phanterpwa_current_user_groups])
                    if role.intersection(auth_user_roles):
                        return True
                    else:
                        return False
                elif isinstance(role, str):
                    return phanterpwa_current_user_has_role(obj, set([role]))
            self.phanterpwa_current_user_has_role = lambda role: phanterpwa_current_user_has_role(self, role)

            def add_role(obj, role):
                db = obj.DALDatabase()
                if not obj.phanterpwa_current_user_has_role(role) and obj.phanterpwa_current_user:
                    s_role = db(db.auth_group.role == role).select().first()
                    if s_role:
                        id_role = s_role.id
                    else:
                        id_role = db.auth_group.insert(
                            role=role,
                            grade=1
                        )
                    db.auth_membership.insert(
                        auth_user=obj.phanterpwa_current_user.id,
                        auth_group=id_role
                    )
                    db.commit()
                q_user_groups = db(
                    (db.auth_membership.auth_user == obj.phanterpwa_current_user.id) &
                    (db.auth_membership.auth_group == db.auth_group.id)
                ).select(
                    db.auth_group.id,
                    db.auth_group.role,
                    orderby=~db.auth_group.grade
                )
                if q_user_groups:
                    obj.phanterpwa_current_user_groups = q_user_groups
                else:
                    obj.phanterpwa_current_user_groups = None
                return obj.phanterpwa_current_user_groups
            self.add_role = lambda role: add_role(self, role)

            if not hasattr(self, "phanterpwa_user_token_checked"):
                self.phanterpwa_user_token_checked = None
                self.phanterpwa_current_user = None
                self.phanterpwa_current_user_groups = None
                self.phanterpwa_client_token = self.request.headers.get('phanterpwa-client-token')
                self.phanterpwa_authorization = self.request.headers.get('phanterpwa-authorization')
                id_user = None
                if self.phanterpwa_client_token and self.phanterpwa_authorization:
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
                        self.phanterpwa_user_token_checked = token_content
                if id_user:
                    self.DALDatabase._adapter.reconnect()
                    q_user = self.DALDatabase(self.DALDatabase.auth_user.id == id_user).select().first()
                    self.phanterpwa_current_user = q_user
                    q_user_groups = self.DALDatabase(
                        (self.DALDatabase.auth_membership.auth_user == self.phanterpwa_current_user.id) &
                        (self.DALDatabase.auth_membership.auth_group == self.DALDatabase.auth_group.id)
                    ).select(
                        self.DALDatabase.auth_group.id,
                        self.DALDatabase.auth_group.role,
                        orderby=~self.DALDatabase.auth_group.grade
                    )
                    if q_user_groups:
                        self.phanterpwa_current_user_groups = q_user_groups
                    q_client = self.DALDatabase(
                        (self.DALDatabase.client.auth_user == id_user) &
                        (self.DALDatabase.client.token == self.phanterpwa_client_token)
                    ).select().first()
                    if q_user and q_client:
                        if not q_user.activated and not ignore_activation:
                            msg = "The user token is invalid!"
                            dict_response = {
                                'status': 'Forbidden',
                                'code': 403,
                                'message': msg,
                                'i18n': {
                                    'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                                }
                            }
                            fi = getframeinfo(currentframe())
                            if not self.projectConfig['PROJECT']['debug']:
                                help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                                    getfile(self.__class__),
                                    self.__class__.__name__,
                                    f.__name__,
                                    fi.filename,
                                    fi.function,
                                    fi.lineno + 19
                                )
                            else:
                                help_debug = "{0}.{1}@{2}:{3}".format(
                                    self.__class__.__name__,
                                    f.__name__,
                                    fi.function,
                                    fi.lineno + 19
                                )
                            dict_response['help_debug'] = help_debug
                            self.set_status(403)
                            return self.write(dict_response)
                        else:

                            if not q_user.permit_mult_login:
                                r_client = self.DALDatabase(
                                    (self.DALDatabase.client.auth_user == id_user) &
                                    (self.DALDatabase.client.token != self.phanterpwa_client_token)
                                ).select()
                                if r_client:
                                    r_client = self.DALDatabase(
                                        (self.DALDatabase.client.auth_user == id_user) &
                                        (self.DALDatabase.client.token != self.phanterpwa_client_token)
                                    ).delete()
                            self.DALDatabase.commit()
                            return f(self, *args, **kargs)
                    else:
                        if q_client:
                            q_client.delete_record()
                        self.DALDatabase.commit()
                        msg = "The user token is invalid!"
                        dict_response = {
                            'status': 'Forbidden',
                            'code': 403,
                            'message': msg,
                            'i18n': {
                                'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                            }
                        }
                        fi = getframeinfo(currentframe())
                        if not self.projectConfig['PROJECT']['debug']:
                            help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                                getfile(self.__class__),
                                self.__class__.__name__,
                                f.__name__,
                                fi.filename,
                                fi.function,
                                fi.lineno + 19
                            )
                        else:
                            help_debug = "{0}.{1}@{2}:{3}".format(
                                self.__class__.__name__,
                                f.__name__,
                                fi.function,
                                fi.lineno + 19
                            )
                        dict_response['help_debug'] = help_debug
                        self.set_status(403)
                        return self.write(dict_response)
                else:
                    msg = "The user token is invalid!"
                    dict_response = {
                        'status': 'Forbidden',
                        'code': 403,
                        'message': msg,
                        'i18n': {
                            'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                        }
                    }
                    fi = getframeinfo(currentframe())
                    if not self.projectConfig['PROJECT']['debug']:
                        help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                            getfile(self.__class__),
                            self.__class__.__name__,
                            f.__name__,
                            fi.filename,
                            fi.function,
                            fi.lineno + 19
                        )
                    else:
                        help_debug = "{0}.{1}@{2}:{3}".format(
                            self.__class__.__name__,
                            f.__name__,
                            fi.function,
                            fi.lineno + 19
                        )
                    dict_response['help_debug'] = help_debug
                    self.set_status(403)
                    return self.write(dict_response)
            else:
                return f(self, *args, **kargs)
        return check_user_token_decorator
    return decorator


def check_private_csrf_token(form_identify=None, ignore_activation=False):
    def decorator(f):
        @wraps(f)
        @check_user_token(ignore_activation)
        @check_public_csrf_token(form_identify)
        def check_csrf_token_decorator(self, *args, **kargs):
            current_user = self.phanterpwa_csrf_token_content.get("user", None)
            if current_user and current_user == self.phanterpwa_current_user.id:
                return f(self, *args, **kargs)

            msg = "The crsf token is invalid!"
            dict_response = {
                'status': 'Bad Request',
                'code': 400,
                'message': msg,
                'i18n': {
                    'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                }
            }
            fi = getframeinfo(currentframe())
            if not self.projectConfig['PROJECT']['debug']:
                help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                    getfile(self.__class__),
                    self.__class__.__name__,
                    f.__name__,
                    fi.filename,
                    fi.function,
                    fi.lineno + 19
                )
            else:
                help_debug = "{0}.{1}@{2}:{3}".format(
                    self.__class__.__name__,
                    f.__name__,
                    fi.function,
                    fi.lineno + 19
                )
            dict_response['help_debug'] = help_debug
            self.set_status(400)
            return self.write(dict_response)
        return check_csrf_token_decorator
    return decorator


def requires_authentication(users_id=None, users_email=None, roles_id=None, roles_name=None):
    def decorator(f):
        @wraps(f)
        @check_user_token()
        def requires_authentication_decorator(self, *args, **kargs):
            if any([users_id, users_email, roles_id, roles_name]):
                msg = "User does not have sufficient privileges!"
                if isinstance(users_id, (list, tuple)):
                    if self.phanterpwa_current_user.id in users_id:
                        return f(self, *args, **kargs)
                if isinstance(users_id, int):
                    if self.phanterpwa_current_user.id == users_id:
                        return f(self, *args, **kargs)
                if isinstance(users_email, (list, tuple)):
                    if self.phanterpwa_current_user.email in users_email:
                        return f(self, *args, **kargs)
                if isinstance(users_email, str):
                    if users_email == self.phanterpwa_current_user.email:
                        return f(self, *args, **kargs)
                if self.phanterpwa_current_user_groups:
                    if isinstance(roles_id, int):
                        for x in self.phanterpwa_current_user_groups:
                            if x.id == roles_id:
                                return f(self, *args, **kargs)
                    if isinstance(roles_name, str):
                        for x in self.phanterpwa_current_user_groups:
                            if x.role == roles_name:
                                return f(self, *args, **kargs)
                    if isinstance(roles_id, (list, tuple)):
                        for x in self.phanterpwa_current_user_groups:
                            if x.id in roles_id:
                                return f(self, *args, **kargs)
                    if isinstance(roles_name, (list, tuple)):
                        for x in self.phanterpwa_current_user_groups:
                            if x.role in roles_name:
                                return f(self, *args, **kargs)

                msg = "User does not have sufficient privileges!"
                fi = getframeinfo(currentframe())
                dict_response = {
                    'status': 'Unauthorized',
                    'code': 403,
                    'message': msg,
                    'i18n': {
                        'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                    }
                }
                fi = getframeinfo(currentframe())
                if not self.projectConfig['PROJECT']['debug']:
                    help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                        getfile(self.__class__),
                        self.__class__.__name__,
                        f.__name__,
                        fi.filename,
                        fi.function,
                        fi.lineno
                    )
                else:
                    help_debug = "{0}.{1}@{2}:{3}".format(
                        self.__class__.__name__,
                        f.__name__,
                        fi.function,
                        fi.lineno
                    )
                dict_response['help_debug'] = help_debug
                self.set_status(403)
                return self.write(dict_response)
            else:
                return f(self, *args, **kargs)

        return requires_authentication_decorator
    return decorator


def requires_no_authentication(ids=None, ignore_locked=True):
    def decorator(f):
        @wraps(f)
        @check_client_token(ignore_locked=ignore_locked)
        def requires_no_authentication_decorator(self, *args, **kargs):
            self.phanterpwa_current_user = None
            self.phanterpwa_client_token = self.request.headers.get('phanterpwa-client-token')
            self.phanterpwa_authorization = self.request.headers.get('phanterpwa-authorization')
            id_user = None
            if self.phanterpwa_client_token and self.phanterpwa_authorization:
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
                    self.phanterpwa_user_token_checked = token_content
            if id_user:
                self.DALDatabase._adapter.reconnect()
                q_user = self.DALDatabase(self.DALDatabase.auth_user.id == id_user).select().first()
                self.phanterpwa_current_user = q_user
                q_client = self.DALDatabase(
                    (self.DALDatabase.client.auth_user == id_user) &
                    (self.DALDatabase.client.token == self.phanterpwa_client_token)
                ).select().first()
                if q_user and q_client:
                    if not q_user.permit_mult_login:
                        r_client = self.DALDatabase(
                            (self.DALDatabase.client.auth_user == id_user) &
                            (self.DALDatabase.client.token != self.phanterpwa_client_token)
                        ).select()
                        if r_client:
                            r_client = self.DALDatabase(
                                (self.DALDatabase.client.auth_user == id_user) &
                                (self.DALDatabase.client.token != self.phanterpwa_client_token)
                            ).delete()
                    self.DALDatabase.commit()
                    msg = "The user must logout!"
                    dict_response = {
                        'status': 'Forbidden',
                        'code': 403,
                        'message': msg,
                        'i18n': {
                            'message': self.i18nTranslator.T(msg) if self.i18nTranslator else msg
                        }
                    }
                    fi = getframeinfo(currentframe())
                    if not self.projectConfig['PROJECT']['debug']:
                        help_debug = "({0}){1}.{2}->({3})@{4}:{5}".format(
                            getfile(self.__class__),
                            self.__class__.__name__,
                            f.__name__,
                            fi.filename,
                            fi.function,
                            fi.lineno + 19
                        )
                    else:
                        help_debug = "{0}.{1}@{2}:{3}".format(
                            self.__class__.__name__,
                            f.__name__,
                            fi.function,
                            fi.lineno + 19
                        )
                    dict_response['help_debug'] = help_debug
                    self.set_status(403)
                    return self.write(dict_response)
                else:
                    return f(self, *args, **kargs)
            else:
                return f(self, *args, **kargs)
        return requires_no_authentication_decorator
    return decorator
