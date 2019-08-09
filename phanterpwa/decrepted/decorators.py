from functools import wraps
from pydal import Field
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serialize,
    BadSignature,
    SignatureExpired
)
from api.models import db
from .config import CONFIG

project_name = CONFIG['PROJECT']['name']
project_version = CONFIG['PROJECT']['version']


def check_application(f):
    @wraps(f)
    def f_intern(self, *args, **kargs):
        self.request.headers.get('Application')
        parser.add_argument('Application-version', location='headers')
        parse_args = parser.parse_args()
        try:
            kargs['Application'] = parse_args['Application']
            kargs['Application-version'] = parse_args['Application-version']
        except KeyError:
            return {
                'status': 'Bad Request',
                'code': 400,
                'message': 'Application name and version are not in the header. ["Application", "Application-version"]'
            }, 400
        if parse_args['Application'] == project_name:
            if not parse_args['Application-version'] == project_version:
                return {
                    'status': 'Bad Request',
                    'code': 400,
                    'message': 'The client needs update (%s)' % project_version
                }, 400
        else:
            return {
                'status': 'Bad Request',
                'code': 400,
                'message': 'The client is not compatible'
            }, 400
        return f(*args, **kargs)
    return f_intern


def check_client_token(f):
    @wraps(f)
    def f_intern(*args, **kargs):
        parser.add_argument('Client-token', location='headers')
        parse_args = parser.parse_args()
        try:
            kargs['Client-token'] = parse_args['Client-token']
        except KeyError:
            return {
                'status': 'Bad Request',
                'code': 400,
                'message': 'Client token is not in the header. ["Client-token"]'
            }, 400
        t = Serialize(
            flask_app.config['SECRET_KEY_USERS'],
            flask_app.config['DEFAULT_TIME_CLIENT_TOKEN_EXPIRES']
        )
        db._adapter.reconnect()
        q = db(db.client.token == parse_args['Client-token']).select().first()
        is_valid_token = False
        if q:
            token_content = None
            try:
                token_content = t.loads(parse_args['Client-token'])
            except BadSignature:
                token_content = None
            except SignatureExpired:
                token_content = None
            if token_content:
                if "user_agent" in token_content:
                    if token_content['user_agent'] == str(request.user_agent):
                        is_valid_token = True
        if is_valid_token:
            return f(*args, **kargs)
        else:
            return {
                'status': 'Unauthorized',
                'code': 401,
                'message': "The Client-token is invalid!"
            }, 401
    return f_intern


def check_csrf_token(f):
    @wraps(f)
    def f_intern(*args, **kargs):
        parser.add_argument('csrf_token', location='form')
        parse_args = parser.parse_args()
        try:
            kargs['Client-token'] = parse_args['csrf_token']
        except KeyError:
            return {
                'status': 'Bad Request',
                'code': 400,
                'message': 'The CSRF token is not in form. ["csrf_token"]'
            }, 400
        t = Serialize(
            flask_app.config['SECRET_KEY_USERS'],
            flask_app.config['DEFAULT_TIME_CSRF_TOKEN_EXPIRES']
        )
        token_content = None
        try:
            token_content = t.loads(parse_args['csrf_token'].encode("utf-8"))
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
                    if (q.token == parse_args['csrf_token']) and\
                            str(request.user_agent) == q.user_agent and\
                            str(request.remote_addr) == q.ip:
                        q.delete_record()
                        db.commit()
                        return f(*args, **kargs)
                    else:
                        return {
                            'status': 'Bad Request',
                            'code': 400,
                            'message': "The crsf token is invalid!"
                        }, 400
        return {
            'status': 'Bad Request',
            'code': 400,
            'message': "The crsf token is invalid!"
        }, 400
    return f_intern


def check_user_token(f):
    @wraps(f)
    def f_intern(*args, **kargs):
        parser.add_argument('Authorization', location='headers')
        parser.add_argument('Client-token', location='headers')
        parse_args = parser.parse_args()
        id_user = None
        if all(['Authorization' in parse_args,
                'Client-token' in parse_args,
                parse_args['Client-token'],
                parse_args['Authorization']]):
            t = Serialize(
                flask_app.config['SECRET_KEY_USERS'],
                flask_app.config['DEFAULT_TIME_TOKEN_EXPIRES']
            )
            token_content = None
            try:
                token_content = t.loads(parse_args['Authorization'])
            except BadSignature:
                token_content = None
            except SignatureExpired:
                token_content = None
            if token_content and 'id' in token_content:
                id_user = token_content['id']
        if id_user:
            db._adapter.reconnect()
            q_user = db(db.auth_user.id == id_user).select().first()
            q_client = db(
                (db.client.id_user == id_user) &
                (db.client.token == parse_args['Client-token'])
            ).select().first()
            if q_user and q_client:
                if not q_user.permit_mult_login:
                    r_client = db(
                        (db.client.id_user == id_user) &
                        (db.client.token != parse_args['Client-token'])
                    ).select()
                    if r_client:
                        r_client = db(
                            (db.client.id_user == id_user) &
                            (db.client.token != parse_args['Client-token'])
                        ).remove()
                db.commit()
                return f(*args, **kargs)
            else:
                return {
                    'status': 'Unauthorized',
                    'code': 401,
                    'message': "The user token is invalid!"
                }, 401
        else:
            return {
                'status': 'Unauthorized',
                'code': 401,
                'message': "The user token is invalid!"
            }, 401
    return f_intern


