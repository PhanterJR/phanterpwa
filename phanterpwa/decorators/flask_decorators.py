from functools import wraps
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serialize,
    BadSignature,
    SignatureExpired,
    URLSafeSerializer
)
from inspect import currentframe, getframeinfo, getfile


def check_application(projectConfig, i18n=None):
    def decorator(f):
        @wraps(f)
        def check_application_decorator(self, *args, **kargs):
            if not hasattr(self, "phanterpwa_client_application_checked"):
                self.phanterpwa_client_application_checked = None
                project_name = projectConfig['PROJECT']['name']
                project_version = projectConfig['PROJECT']['version']
                self.phanterpwa_application = self.request.headers.get('phanterpwa-application')
                self.phanterpwa_application_version = self.request.headers.get('phanterpwa-application-version')
                if self.phanterpwa_application == project_name:
                    if self.phanterpwa_application_version != project_version:
                        msg = 'The client needs update ({0})'
                        dict_response = {
                            'status': 'Bad Request',
                            'code': 400,
                            'message': msg.format(project_version),
                            'i18n': {
                                'message': i18n.T(msg).format(project_version) if i18n else msg.format(project_version)
                            }
                        }
                        fi = getframeinfo(currentframe())
                        if not projectConfig['PROJECT']['debug']:
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
                        return dict_response, 400
                else:
                    msg = 'The client is not compatible'
                    dict_response = {
                        'status': 'Bad Request',
                        'code': 400,
                        'message': msg,
                        'i18n': {
                            'message': i18n.T(msg) if i18n else msg
                        }
                    }
                    fi = getframeinfo(currentframe())
                    if not projectConfig['PROJECT']['debug']:
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
                    return dict_response, 400
                self.phanterpwa_client_application_checked = {
                    'name': self.phanterpwa_application,
                    'version': self.phanterpwa_application_version
                }
                return f(self, *args, **kargs)
            else:
                return f(self, *args, **kargs)
        return check_application_decorator
    return decorator


def check_client_token(projectConfig, db, i18n=None, ignore_locked=True):
    def decorator(f):
        @wraps(f)
        @check_application(projectConfig, i18n)
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
                            'message': i18n.T(msg) if i18n else msg
                        }
                    }
                    fi = getframeinfo(currentframe())
                    if not projectConfig['PROJECT']['debug']:
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
                    return dict_response, 400
                t = Serialize(
                    projectConfig['API']['secret_key'],
                    projectConfig['API']['default_time_client_token_expire']
                )
                db._adapter.reconnect()
                q = db(db.client.token == self.phanterpwa_client_token).select().first()
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
                                        projectConfig['API']['secret_key'],
                                        projectConfig['API']['default_time_user_token_expire']
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
                            'message': msg,
                            'i18n': {
                                'message': i18n.T(msg) if i18n else msg
                            }
                        }
                        fi = getframeinfo(currentframe())
                        if not projectConfig['PROJECT']['debug']:
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
                        return dict_response, 401
                    self.phanterpwa_current_client = q
                    return f(self, *args, **kargs)
                else:
                    if q:
                        q.delete_record()
                        db.commit()
                    msg = "The phanterpwa-client-token is invalid!"
                    dict_response = {
                        'status': 'Forbidden',
                        'code': 403,
                        'message': msg,
                        'i18n': {
                            'message': i18n.T(msg) if i18n else msg
                        }
                    }
                    fi = getframeinfo(currentframe())
                    if not projectConfig['PROJECT']['debug']:
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
                    return dict_response, 403
            else:
                return f(self, *args, **kargs)
        return check_client_token_decorator
    return decorator


def check_url_token(projectConfig, db, i18n=None):
    def decorator(f):
        @wraps(f)
        def check_url_token_decorator(self, *args, **kargs):

            dict_arguments = {x: self.request.args[x] for x in self.request.args}
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
                        'message': i18n.T(msg) if i18n else msg
                    }
                }
                fi = getframeinfo(currentframe())
                if not projectConfig['PROJECT']['debug']:
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

                return dict_response, 400
            t = URLSafeSerializer(
                projectConfig['API']['url_secret_key'],
                salt="url_secret_key"
            )
            db._adapter.reconnect()
            token_content = None
            try:
                token_content = t.loads(self.phanterpwa_url_token)
            except BadSignature:
                token_content = None
            if token_content:
                if "user_agent" in token_content and "id_client" in token_content:
                    if token_content['user_agent'] == self.phanterpwa_user_agent:
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
                        'message': i18n.T(msg) if i18n else msg
                    }
                }
                fi = getframeinfo(currentframe())
                if not projectConfig['PROJECT']['debug']:
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
                return dict_response, 403
        return check_url_token_decorator
    return decorator


def check_csrf_token(projectConfig, db, i18n=None):
    def decorator(f):
        @wraps(f)
        @check_client_token(projectConfig, db, i18n)
        def check_csrf_token_decorator(self, *args, **kargs):
            dict_arguments = {x: self.request.form[x] for x in self.request.form}
            self.phanterpwa_csrf_token_content = None
            self.phanterpwa_csrf_token = dict_arguments.get("csrf_token")
            self.phanterpwa_user_agent = self.request.headers.get('User-Agent')
            self.phanterpwa_remote_ip = str(self.request.remote_addr)
            if not self.phanterpwa_csrf_token:
                msg = 'The CSRF token is not in form. "csrf_token"'
                dict_response = {
                    'status': 'Bad Request',
                    'code': 400,
                    'message': msg,
                    'i18n': {
                        'message': i18n.T(msg) if i18n else msg
                    }
                }
                fi = getframeinfo(currentframe())
                if not projectConfig['PROJECT']['debug']:
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
                return dict_response, 400
            t = Serialize(
                projectConfig['API']['secret_key'],
                projectConfig['API']['default_time_user_token_expire']
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
                    db._adapter.reconnect()
                    q = db(db.csrf.id == token_content["id"]).select().first()
                    if q:
                        if (q.token == self.phanterpwa_csrf_token) and\
                                self.phanterpwa_user_agent == q.user_agent and\
                                self.phanterpwa_remote_ip == q.ip:
                            q.delete_record()
                            db.commit()
                            return f(self, *args, **kargs)
                        else:
                            msg = "The crsf token is invalid! The client has an unstable address."
                            dict_response = {
                                'status': 'Bad Request',
                                'code': 400,
                                'message': msg,
                                'i18n': {
                                    'message': i18n.T(msg) if i18n else msg
                                }
                            }
                            fi = getframeinfo(currentframe())
                            if not projectConfig['PROJECT']['debug']:
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
                            return dict_response, 400
            msg = "The crsf token is invalid!"
            dict_response = {
                'status': 'Bad Request',
                'code': 400,
                'message': msg,
                'i18n': {
                    'message': i18n.T(msg) if i18n else msg
                }
            }
            fi = getframeinfo(currentframe())
            if not projectConfig['PROJECT']['debug']:
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
            return dict_response, 400
        return check_csrf_token_decorator
    return decorator


def check_user_token(projectConfig, db, i18n=None):
    def decorator(f):
        @wraps(f)
        @check_client_token(projectConfig, db, i18n, ignore_locked=False)
        def check_user_token_decorator(self, *args, **kargs):
            if not hasattr(self, "phanterpwa_user_token_checked"):
                self.phanterpwa_user_token_checked = None
                self.phanterpwa_current_user = None
                self.phanterpwa_client_token = self.request.headers.get('phanterpwa-client-token')
                self.phanterpwa_authorization = self.request.headers.get('phanterpwa-authorization')
                id_user = None
                if self.phanterpwa_client_token and self.phanterpwa_authorization:
                    t = Serialize(
                        projectConfig['API']['secret_key'],
                        projectConfig['API']['default_time_user_token_expire']
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
                    db._adapter.reconnect()
                    q_user = db(db.auth_user.id == id_user).select().first()
                    self.phanterpwa_current_user = q_user
                    q_client = db(
                        (db.client.auth_user == id_user) &
                        (db.client.token == self.phanterpwa_client_token)
                    ).select().first()
                    if q_user and q_client:
                        if not q_user.permit_mult_login:
                            r_client = db(
                                (db.client.auth_user == id_user) &
                                (db.client.token != self.phanterpwa_client_token)
                            ).select()
                            if r_client:
                                r_client = db(
                                    (db.client.auth_user == id_user) &
                                    (db.client.token != self.phanterpwa_client_token)
                                ).remove()
                        db.commit()
                        return f(self, *args, **kargs)
                    else:
                        if q_client:
                            q_client.delete_record()
                        db.commit()
                        msg = "The user token is invalid!"
                        dict_response = {
                            'status': 'Forbidden',
                            'code': 403,
                            'message': msg,
                            'i18n': {
                                'message': i18n.T(msg) if i18n else msg
                            }
                        }
                        fi = getframeinfo(currentframe())
                        if not projectConfig['PROJECT']['debug']:
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
                        return dict_response, 403
                else:
                    msg = "The user token is invalid!"
                    dict_response = {
                        'status': 'Forbidden',
                        'code': 403,
                        'message': msg,
                        'i18n': {
                            'message': i18n.T(msg) if i18n else msg
                        }
                    }
                    fi = getframeinfo(currentframe())
                    if not projectConfig['PROJECT']['debug']:
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
                    return dict_response, 403
            else:
                return f(self, *args, **kargs)
        return check_user_token_decorator
    return decorator


def requires_authentication(projectConfig, db, i18n=None, ids=None):
    def decorator(f):
        @wraps(f)
        @check_user_token(projectConfig, db, i18n)
        def requires_authenticatio_decorator(self, *args, **kargs):
            if not ids:
                if self.phanterpwa_current_user.id in ids:
                    return f(self, *args, **kargs)
                else:
                    msg = "User cannot access this feature!"
                    dict_response = {
                        'status': 'Unauthorized',
                        'code': 401,
                        'message': msg,
                        'i18n': {
                            'message': i18n.T(msg) if i18n else msg
                        }
                    }
                    fi = getframeinfo(currentframe())
                    if not projectConfig['PROJECT']['debug']:
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
                    return dict_response, 401
            else:
                return f(self, *args, **kargs)
        return requires_authenticatio_decorator
    return decorator


def requires_authentication_group(projectConfig, db, i18n=None, roles=None, ids=None):
    def decorator(f):
        @wraps(f)
        @check_user_token(projectConfig, db, i18n)
        def requires_authentication_group_decorator(self, *args, **kargs):
            self.phanterpwa_current_user_groups = None
            if roles or ids:
                q_user_groups = db(
                    (db.auth_membership.auth_user == self.phanterpwa_current_user.id) &
                    (db.auth_membership.auth_group == db.auth_group.id)
                ).select(db.auth_group.id, db.auth_group.role, orderby=~db.auth_group.grade)
                user_roles = set([x.role for x in q_user_groups if x.role in roles or x.id in ids])
                if user_roles:
                    self.phanterpwa_current_user_groups = q_user_groups
                    return f(self, *args, **kargs)
                else:
                    msg = "User does not have sufficient privileges!"
                    dict_response = {
                        'status': 'Unauthorized',
                        'code': 401,
                        'message': msg,
                        'i18n': {
                            'message': i18n.T(msg) if i18n else msg
                        }
                    }
                    fi = getframeinfo(currentframe())
                    if not projectConfig['PROJECT']['debug']:
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
                    return dict_response, 401
            else:
                return f(self, *args, **kargs)

        return requires_authentication_group_decorator
    return decorator
