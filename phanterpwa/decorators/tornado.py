from functools import wraps
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serialize,
    BadSignature,
    SignatureExpired
)


def check_application(projectConfig):
    def decorator(f):
        @wraps(f)
        def f_intern(self, *args, **kargs):
            project_name = projectConfig['PROJECT']['name']
            project_version = projectConfig['PROJECT']['version']
            self.pwa_application = self.request.headers.get('Application')
            self.pwa_application_version = self.request.headers.get('Application-version')
            if self.pwa_application == project_name:
                if self.pwa_application_version != project_version:
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': 'The client needs update (%s)' % project_version
                    })
            else:
                self.set_status(400)
                return self.write({
                    'status': 'Bad Request',
                    'code': 400,
                    'message': 'The client is not compatible'
                })

            return f(self, *args, **kargs)
        return f_intern
    return decorator


def check_client_token(projectConfig, db):
    def decorator(f):
        @wraps(f)
        def f_intern(self, *args, **kargs):

            self.pwa_cliente_token = self.request.headers.get('Client-token')
            if not self.pwa_cliente_token:
                self.set_status(400)
                return self.write({
                    'status': 'Bad Request',
                    'code': 400,
                    'message': 'Client token is not in the header. ["Client-token"]'
                })
            t = Serialize(
                projectConfig['API']['secret_key'],
                projectConfig['API']['default_time_token_expires']
            )
            db._adapter.reconnect()
            q = db(db.client.token == self.pwa_cliente_token).select().first()
            is_valid_token = False
            if q:
                token_content = None
                try:
                    token_content = t.loads(self.pwa_cliente_token)
                except BadSignature:
                    token_content = None
                except SignatureExpired:
                    token_content = None
                if token_content:
                    if "user_agent" in token_content:
                        if token_content['user_agent'] == str(self.request.headers.get('User-Agent')):
                            is_valid_token = True
            if is_valid_token:
                return f(self, *args, **kargs)
            else:
                self.set_status(401)
                return self.write({
                    'status': 'Unauthorized',
                    'code': 401,
                    'message': "The Client-token is invalid!"
                })
        return f_intern
    return decorator


def check_csrf_token(projectConfig, db):
    def decorator(f):
        @wraps(f)
        def f_intern(self, *args, **kargs):

            data = {
                'csrf_token': self.request.arguments.get("csrf_token")[0].decode('utf-8')
            }
            user_agent = str(self.request.headers.get('User-Agent'))
            remote_addr = str(self.request.remote_ip)
            if not data['csrf_token']:
                self.set_status(400)
                return self.write({
                    'status': 'Bad Request',
                    'code': 400,
                    'message': 'The CSRF token is not in form. ["csrf_token"]'
                })
            t = Serialize(
                projectConfig['API']['secret_key'],
                projectConfig['API']['default_time_token_expires']
            )
            token_content = None
            try:
                token_content = t.loads(data['csrf_token'].encode("utf-8"))
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
                        if (q.token == data['csrf_token']) and\
                                user_agent == q.user_agent and\
                                remote_addr == q.ip:
                            q.delete_record()
                            db.commit()
                            return f(self, *args, **kargs)
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
    return decorator
