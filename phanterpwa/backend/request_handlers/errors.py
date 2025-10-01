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
from phanterpwa.backend.security import (
    Serialize,
    SignatureExpired,
    BadSignature,
    URLSafeSerializer,
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
from phanterpwa.backend.decorators import (
    check_client_token
)

class Errors(web.RequestHandler):
    """
        url: url: 'api/errors/'
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

    @check_client_token()
    def post(self, *args, **kargs):
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        email_user = dict_arguments.get("email_user", None)
        current_way = dict_arguments.get("current_way", None)
        message = dict_arguments.get("message", None)
        error = dict_arguments.get("error", None)
        source = dict_arguments.get("source", None)
        lineno = dict_arguments.get("lineno", None)
        colno = dict_arguments.get("colno", None)
        if error:
            self.logger_api.error("CLIENT ERROR: {0}\n\t{1}\n\t{2}\n\t{3}\n\t{4}\nt{5}\nt{6}\n".format(
                error,
                "{0}: {1}".format("Email user", email_user),
                "{0}: {1}".format("Current way", current_way),
                "{0}: {1}".format("Message", message),
                "{0}: {1}".format("File", source),
                "{0}: {1}".format("Line", lineno),
                "{0}: {1}".format("Col", colno),

            )
        )

        message = "Received error."
        self.set_status(200)
        return self.write({
            'status': 'OK',
            'code': 200,
            'message': message,
            'i18n': {
                'message': self.T(message)
            }
        })


