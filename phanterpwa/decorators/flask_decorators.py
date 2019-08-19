from functools import wraps
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serialize,
    BadSignature,
    SignatureExpired
)
from inspect import currentframe, getframeinfo, getfile
from flask import request
from flask_restful import reqparse
parser = reqparse.RequestParser()


def check_application(projectConfig, i18n=None):
    def decorator(f):
        @wraps(f)
        def check_application_decorator(self, *args, **kargs):
            if not hasattr(self, "phanterpwa_client_application_checked"):
                parser.add_argument('phanterpwa-application', location='headers', default=None)
                parser.add_argument('phanterpwa-application-version', location='headers', default=None)
                parse_args = parser.parse_args()
                self.phanterpwa_client_application_checked = None
                project_name = projectConfig['PROJECT']['name']
                project_version = projectConfig['PROJECT']['version']
                self.phanterpwa_application = parse_args['phanterpwa-application']
                self.phanterpwa_application_version = parse_args['phanterpwa-application-version']
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


def check_client_token(projectConfig, db, i18n=None):
    def decorator(f):
        @wraps(f)
        @check_application(projectConfig, i18n)
        def check_client_token_decorator(self, *args, **kargs):
            if not hasattr(self, "phanterpwa_client_token_checked"):
                self.phanterpwa_client_token_checked = None
                parser.add_argument('phanterpwa-client-token', location='headers', default=None)
                parser.add_argument('phanterpwa-authorization', location='headers', default=None)
                parse_args = parser.parse_args()
                self.phanterpwa_client_token = parse_args['phanterpwa-client-token']
                self.phanterpwa_authorization = parse_args['phanterpwa-authorization']
                self.phanterpwa_user_agent = request.user_agent
                self.phanterpwa_remote_ip = request.remote_addr
                user_agent = str(self.phanterpwa_user_agent)
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
                is_valid_token = False
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
                            if token_content['user_agent'] == user_agent and\
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
                                        id_user = token_content_user['id']
                                    if id_user and 'id_user' in token_content and id_user == token_content['id_user']:
                                        is_valid_token = True
                                else:
                                    is_valid_token = True
                                self.phanterpwa_client_token_checked = token_content
                if is_valid_token:
                    self.phanterpwa_client_token_checked = True
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


def check_csrf_token(projectConfig, db, i18n=None):
    def decorator(f):
        @wraps(f)
        @check_client_token(projectConfig, db, i18n)
        def check_csrf_token_decorator(self, *args, **kargs):
            self.phanterpwa_csrf_token_content = None
            dict_arguments = {x: request.form[x] for x in request.form}
            self.phanterpwa_csrf_token = dict_arguments["csrf_token"]
            self.phanterpwa_user_agent = request.user_agent
            self.phanterpwa_remote_ip = request.remote_addr
            user_agent = str(self.phanterpwa_user_agent)
            remote_addr = str(self.phanterpwa_remote_ip)
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
                        q.update_record(used=True)
                        db.commit()
                        if (q.token == self.phanterpwa_csrf_token) and\
                                user_agent == q.user_agent and\
                                remote_addr == q.ip:
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
        @check_client_token(projectConfig, db, i18n)
        def check_user_token_decorator(self, *args, **kargs):
            if not hasattr(self, "phanterpwa_user_token_checked"):
                self.phanterpwa_user_token_checked = None
                self.phanterpwa_current_user = None
                parser.add_argument('phanterpwa-client-token', location='headers', default=None)
                parser.add_argument('phanterpwa-authorization', location='headers', default=None)
                parse_args = parser.parse_args()
                self.phanterpwa_client_token = parse_args['phanterpwa-client-token']
                self.phanterpwa_authorization = parse_args['phanterpwa-authorization']
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
                        (db.client.id_user == id_user) &
                        (db.client.token == self.phanterpwa_client_token)
                    ).select().first()
                    if q_user and q_client:
                        if not q_user.permit_mult_login:
                            r_client = db(
                                (db.client.id_user == id_user) &
                                (db.client.token != self.phanterpwa_client_token)
                            ).select()
                            if r_client:
                                r_client = db(
                                    (db.client.id_user == id_user) &
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
