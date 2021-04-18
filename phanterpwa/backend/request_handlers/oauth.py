import os
import urllib.request
import json
from passlib.hash import pbkdf2_sha512
from urllib.parse import quote, urlencode
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from phanterpwa.backend.decorators import (
    requires_no_authentication
)
from phanterpwa.backend.dataforms import FieldsDALValidateDictArgs
from phanterpwa.i18n import browser_language

from phanterpwa.gallery.integrationDAL import PhanterpwaGalleryUserImage
from tornado import (
    web
)
from phanterpwa.third_parties.xss import xssescape as E
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serialize,
    URLSafeSerializer
)

from datetime import (
    datetime
)
from phanterpwa.helpers import (
    HTML,
    HEAD,
    BODY,
    SCRIPT
)


class Prompt(web.RequestHandler):
    """
        url: url: 'api/oauth/prompt/<social_name>'
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
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip
        self.phanterpwa_origin = self.request.headers.get('Origin')

    def check_origin(self, origin):
        return True

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})

    @requires_no_authentication()
    def get(self, *args, **kargs):
        social_name = args[0]
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        url_base = self.projectConfig['BACKEND'][self.app_name]['http_address']
        if social_name == "google":
            client_id = self.projectConfig['OAUTH_{0}'.format(social_name.upper())]['client_id']
            client_secret = self.projectConfig['OAUTH_{0}'.format(social_name.upper())]['client_secret']
            redirect_uri = '{0}/api/oauth/redirect/{1}'.format(url_base, social_name)
            scope = ['openid', 'https://www.googleapis.com/auth/userinfo.email',
                 'https://www.googleapis.com/auth/userinfo.profile']
            oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
                              scope=scope)
            authorization_url, state = oauth.authorization_url(
                'https://accounts.google.com/o/oauth2/auth',
                access_type="offline",
                prompt="select_account"
            )
            self.DALDatabase.social_auth.insert(
                social_name=social_name,
                request_state=state,
                client_token=self.phanterpwa_client_token,
                origin=self.phanterpwa_origin
            )
            self.DALDatabase.commit()
            self.set_status(200)
            return self.write({
                "status": "OK",
                "origin": self.phanterpwa_origin if self.phanterpwa_origin else None,
                "redirect": authorization_url,
                "state": state
            })
        elif social_name == "facebook":
            client_id = self.projectConfig['OAUTH_{0}'.format(social_name.upper())]['client_id']
            client_secret = self.projectConfig['OAUTH_{0}'.format(social_name.upper())]['client_secret']
            redirect_uri = '{0}/api/oauth/redirect/{1}'.format(url_base, social_name)
            oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope='email')
            oauth = facebook_compliance_fix(oauth)
            authorization_url, state = oauth.authorization_url(
                'https://www.facebook.com/dialog/oauth',
            )
            self.DALDatabase.social_auth.insert(
                social_name=social_name,
                request_state=state,
                client_token=self.phanterpwa_client_token,
                origin=self.phanterpwa_origin
            )
            self.DALDatabase.commit()
            self.set_status(200)
            return self.write({
                "status": "OK",
                "origin": self.phanterpwa_origin if self.phanterpwa_origin else None,
                "redirect": authorization_url,
                "state": state
            })

        message = "An error occurred while trying to authenticate."
        self.set_status(400)
        return self.write({
            'status': 'Bad Request',
            'code': 400,
            'message': message,
            'i18n': {
                'message': self.T(message)
            }
        })


class Redirect(web.RequestHandler):
    """
        url: 'api/oauth/redirect/<social_name>'
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
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip
        self.phanterpwa_origin = self.request.headers.get('Origin')

    def check_origin(self, origin):
        return True

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})

    def get(self, *args, **kargs):
        social_name = args[0]
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}

        url_base = self.projectConfig['BACKEND'][self.app_name]['http_address']
        if social_name == "google":
            state = dict_arguments.get("state")
            q_state = self.DALDatabase(
                (self.DALDatabase.social_auth.social_name == "google") and (self.DALDatabase.social_auth.request_state == state)).select().first()
            origin = None
            if not q_state:
                message = "The authentication request has already been used."
                return self.write({
                    'status': 'Bad Request',
                    'code': 400,
                    'message': message,
                    'i18n': {
                        'message': self.T(message)
                    }
                })
            else:
                self.phanterpwa_client_token = q_state.client_token
                origin = q_state.origin
                q_state.delete_record()
            self.DALDatabase.commit()
            uri = "{0}{1}".format(url_base, self.request.uri)
            client_id = self.projectConfig['OAUTH_{0}'.format(social_name.upper())]['client_id']
            client_secret = self.projectConfig['OAUTH_{0}'.format(social_name.upper())]['client_secret']
            redirect_uri = '{0}/api/oauth/redirect/{1}'.format(url_base, social_name)
            scope = ['openid', 'https://www.googleapis.com/auth/userinfo.email',
                 'https://www.googleapis.com/auth/userinfo.profile']
            oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
                              scope=scope)
            try:
                token = oauth.fetch_token(
                    'https://accounts.google.com/o/oauth2/token',
                    authorization_response=uri,
                    client_secret=client_secret)
            except Exception as e:
                self.logger_api.warning(e)
                message = "There was a problem trying to authenticate using a google account."
                return self.write({
                    'status': 'Bad Request',
                    'code': 400,
                    'uri': uri,
                    'message': message,
                    'i18n': {
                        'message': self.T(message)
                    }
                })
            else:

                url_consult = self.projectConfig['OAUTH_{0}'.format(social_name.upper())]['http_address']
                googleapi = "{0}?access_token={1}".format(
                    url_consult, quote(token['access_token']))
                try:
                    with urllib.request.urlopen(googleapi) as req:
                        googleapi_user = req.read()
                        googleapi_user = json.loads(googleapi_user)
                except Exception as e:
                    self.logger_api.warning(e)
                    message = "There was a problem trying to load user information on google api."
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'uri': googleapi,
                        'message': message,
                        'i18n': {
                            'message': self.T(message)
                        }
                    })
                else:
                    email_verified = googleapi_user.get("email_verified", False)
                    if not email_verified:
                        message = "The google email has not been verified."
                        self.set_status(400)
                        return self.write({
                            'status': 'Bad Request',
                            'code': 400,
                            'message': message,
                            'google_api': googleapi_user,
                            'i18n': {
                                'message': self.T(message)
                            }
                        })
                    email = googleapi_user.get('email', None)

                    if email:
                        q_user = self.DALDatabase(self.DALDatabase.auth_user.email == email).select().first()
                        if q_user:
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
                            token_user = token_user.decode('utf-8')
                            q_role = self.DALDatabase(
                                (self.DALDatabase.auth_membership.auth_user == q_user.id) &
                                (self.DALDatabase.auth_group.id == self.DALDatabase.auth_membership.auth_group)
                            ).select(self.DALDatabase.auth_group.role, orderby=self.DALDatabase.auth_group.grade)
                            roles = [x.role for x in q_role]
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
                            r_client = self.DALDatabase(self.DALDatabase.client.token == self.phanterpwa_client_token).select().first()
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
                                remember_me=True,
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
                            social_image = googleapi_user.get("picture", None)

                            redirect = "#_phanterpwa:/{0}?{1}".format(
                                origin if origin else "",
                                urlencode({
                                    'authorization': token_user,
                                    'client_token': token_client,
                                    'url_token': token_url,
                                    'auth_user': json.dumps({
                                        'id': str(q_user.id),
                                        'first_name': E(q_user.first_name),
                                        'last_name': E(q_user.last_name),
                                        'email': email,
                                        'remember_me': q_client.remember_me,
                                        'roles': roles,
                                        'role': role,
                                        'activated': q_user.activated,
                                        'image': user_image.id_image,
                                        'social_image': social_image,
                                        'social_login': social_name
                                    })
                                })

                            )
                            self.set_status(200)
                            return self.write(
                                str(HTML(HEAD(), BODY(SCRIPT("window.location = '{0}'".format(redirect))))))
                    else:
                        new_password = os.urandom(3).hex()
                        password_hash = pbkdf2_sha512.hash("password{0}{1}".format(
                            new_password, self.projectConfig['BACKEND'][self.app_name]['secret_key']))
                        table = self.DALDatabase.auth_user
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
                        r = result.validate_and_insert(self.DALDatabase.auth_user)
                        if r and r.id:
                            q_user = self.DALDatabase(self.DALDatabase.auth_user.id == r.id).select().first()
                            if r.id == 1:
                                role = "root"
                                id_role = self.DALDatabase(self.DALDatabase.auth_group.role == 'root').select().first()
                                if id_role:
                                    self.DALDatabase.auth_membership.insert(auth_user=1,
                                    auth_group=id_role.id)
                            else:
                                role = "user"
                                self.DALDatabase.auth_membership.insert(auth_user=r.id, auth_group=3)
                            t_user = Serialize(
                                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                                self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire']
                            )
                            content_user = {
                                'id': str(r.id),
                                'email': dict_arguments['email']
                            }
                            token_user = t_user.dumps(content_user)
                            token_user = token_user.decode('utf-8')
                            token_client = self.phanterpwa_client_token
                            id_client = self.DALDatabase.client.update_or_insert(auth_user=r.id)
                            t_client = Serialize(
                                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                                self.projectConfig['BACKEND'][self.app_name]['default_time_client_token_expire']
                            )
                            t_url = URLSafeSerializer(
                                self.projectConfig['BACKEND'][self.app_name]["secret_key"],
                                salt="url_secret_key"
                            )
                            content_client = {
                                'id_user': str(r.id),
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
                                    (self.DALDatabase.client.auth_user == id_user) &
                                    (self.DALDatabase.client.token != self.phanterpwa_client_token)
                                ).select()
                                if r_client:
                                    r_client = self.DALDatabase(
                                        (self.DALDatabase.client.auth_user == id_user) &
                                        (self.DALDatabase.client.token != self.phanterpwa_client_token)
                                    ).remove()
                            self.DALDatabase.commit()
                            user_image = PhanterpwaGalleryUserImage(r.id, self.DALDatabase, self.projectConfig)
                            self.set_status(201)
                            roles = ["user"]
                            role = "user"
                            redirect = "#_phanterpwa:/{0}?{1}".format(
                                origin if origin else "",
                                urlencode({
                                    'authorization': token_user,
                                    'client_token': token_client,
                                    'url_token': token_url,
                                    'auth_user': json.dumps({
                                        'id': str(q_user.id),
                                        'first_name': E(q_user.first_name),
                                        'last_name': E(q_user.last_name),
                                        'email': email,
                                        'remember_me': q_client.remember_me,
                                        'roles': roles,
                                        'role': role,
                                        'activated': q_user.activated,
                                        'image': user_image.id_image,
                                        'social_image': social_image,
                                        'social_login': social_name
                                    })
                                })
                            )
                            self.write(
                                str(HTML(HEAD(),BODY(SCRIPT("window.location = '{0}'".format(redirect))))))
        elif social_name == "facebook":
            state = dict_arguments.get("state")
            q_state = self.DALDatabase(
                (self.DALDatabase.social_auth.social_name == "facebook") and (self.DALDatabase.social_auth.request_state == state)).select().first()
            origin = None
            if not q_state:
                message = "The authentication request has already been used."
                return self.write({
                    'status': 'Bad Request',
                    'code': 400,
                    'message': message,
                    'i18n': {
                        'message': self.T(message)
                    }
                })
            else:
                self.phanterpwa_client_token = q_state.client_token
                origin = q_state.origin
                q_state.delete_record()
            self.DALDatabase.commit()
            uri = "{0}{1}".format(url_base, self.request.uri)
            client_id = self.projectConfig['OAUTH_{0}'.format(social_name.upper())]['client_id']
            client_secret = self.projectConfig['OAUTH_{0}'.format(social_name.upper())]['client_secret']
            redirect_uri = '{0}/api/oauth/redirect/{1}'.format(url_base, social_name)
            oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope='email')
            try:
                token = oauth.fetch_token(
                    'https://graph.facebook.com/oauth/access_token',
                    authorization_response=uri,
                    client_secret=client_secret)
            except Exception as e:
                self.logger_api.warning(e)
                message = "There was a problem trying to authenticate using a facebook account."
                return self.write({
                    'status': 'Bad Request',
                    'code': 400,
                    'uri': uri,
                    'message': message,
                    'i18n': {
                        'message': self.T(message)
                    }
                })
            else:
                try:
                    facebook_user = oauth.get(
                        'https://graph.facebook.com/me?fields=name,first_name,last_name,email,picture')
                    facebookapi_user = json.loads(facebook_user.content)

                except Exception as e:
                    self.logger_api.warning(e)
                    message = "There was a problem trying to load user information on facebook api."
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': message,
                        'i18n': {
                            'message': self.T(message)
                        }
                    })
                else:
                    email = facebookapi_user.get('email', None)
                    social_image = None
                    try:
                        social_image = facebookapi_user["picture"]["data"]["url"]
                    except Exception as e:
                        self.logger_api.warning(e)
                    if email:
                        q_user = self.DALDatabase(self.DALDatabase.auth_user.email == email).select().first()
                        if q_user:
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
                            token_user = token_user.decode('utf-8')
                            q_role = self.DALDatabase(
                                (self.DALDatabase.auth_membership.auth_user == q_user.id) &
                                (self.DALDatabase.auth_group.id == self.DALDatabase.auth_membership.auth_group)
                            ).select(self.DALDatabase.auth_group.role, orderby=self.DALDatabase.auth_group.grade)
                            roles = [x.role for x in q_role]
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
                            r_client = self.DALDatabase(self.DALDatabase.client.token == self.phanterpwa_client_token).select().first()
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
                                remember_me=True,
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

                            redirect = "#_phanterpwa:/{0}?{1}".format(
                                origin if origin else "",
                                urlencode({
                                    'authorization': token_user,
                                    'client_token': token_client,
                                    'url_token': token_url,
                                    'auth_user': json.dumps({
                                        'id': str(q_user.id),
                                        'first_name': E(q_user.first_name),
                                        'last_name': E(q_user.last_name),
                                        'email': email,
                                        'remember_me': q_client.remember_me,
                                        'roles': roles,
                                        'role': role,
                                        'activated': q_user.activated,
                                        'image': user_image.id_image,
                                        'social_image': social_image,
                                        'social_login': social_name
                                    })
                                })

                            )
                            self.set_status(200)
                            return self.write(
                                str(HTML(HEAD(), BODY(SCRIPT("window.location = '{0}'".format(redirect))))))
                    else:
                        new_password = os.urandom(3).hex()
                        password_hash = pbkdf2_sha512.hash("password{0}{1}".format(
                            new_password, self.projectConfig['BACKEND'][self.app_name]['secret_key']))
                        table = self.DALDatabase.auth_user
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
                        r = result.validate_and_insert(self.DALDatabase.auth_user)
                        if r and r.id:
                            q_user = self.DALDatabase(self.DALDatabase.auth_user.id == r.id).select().first()
                            if r.id == 1:
                                role = "root"
                                id_role = self.DALDatabase(self.DALDatabase.auth_group.role == 'root').select().first()
                                if id_role:
                                    self.DALDatabase.auth_membership.insert(auth_user=1,
                                    auth_group=id_role.id)
                            else:
                                role = "user"
                                self.DALDatabase.auth_membership.insert(auth_user=r.id, auth_group=3)
                            t_user = Serialize(
                                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                                self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire']
                            )
                            content_user = {
                                'id': str(r.id),
                                'email': dict_arguments['email']
                            }
                            token_user = t_user.dumps(content_user)
                            token_user = token_user.decode('utf-8')
                            token_client = self.phanterpwa_client_token
                            id_client = self.DALDatabase.client.update_or_insert(auth_user=r.id)
                            t_client = Serialize(
                                self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                                self.projectConfig['BACKEND'][self.app_name]['default_time_client_token_expire']
                            )
                            t_url = URLSafeSerializer(
                                self.projectConfig['BACKEND'][self.app_name]["secret_key"],
                                salt="url_secret_key"
                            )
                            content_client = {
                                'id_user': str(r.id),
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
                                    (self.DALDatabase.client.auth_user == id_user) &
                                    (self.DALDatabase.client.token != self.phanterpwa_client_token)
                                ).select()
                                if r_client:
                                    r_client = self.DALDatabase(
                                        (self.DALDatabase.client.auth_user == id_user) &
                                        (self.DALDatabase.client.token != self.phanterpwa_client_token)
                                    ).remove()
                            self.DALDatabase.commit()
                            user_image = PhanterpwaGalleryUserImage(r.id, self.DALDatabase, self.projectConfig)
                            self.set_status(201)
                            roles = ["user"]
                            role = "user"
                            redirect = "#_phanterpwa:/{0}?{1}".format(
                                origin if origin else "",
                                urlencode({
                                    'authorization': token_user,
                                    'client_token': token_client,
                                    'url_token': token_url,
                                    'auth_user': json.dumps({
                                        'id': str(q_user.id),
                                        'first_name': E(q_user.first_name),
                                        'last_name': E(q_user.last_name),
                                        'email': email,
                                        'remember_me': q_client.remember_me,
                                        'roles': roles,
                                        'role': role,
                                        'activated': q_user.activated,
                                        'image': user_image.id_image,
                                        'social_image': social_image,
                                        'social_login': social_name
                                    })
                                })
                            )
                            self.write(
                                str(HTML(HEAD(), BODY(SCRIPT("window.location = '{0}'".format(redirect))))))

            
        message = "An error occurred while trying to authenticate."
        self.set_status(400)
        return self.write({
            'status': 'Bad Request',
            'code': 400,
            'message': message,
            'i18n': {
                'message': self.T(message)
            }
        })
