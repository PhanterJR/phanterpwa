import ast
import re
import json
from datetime import datetime
from tornado import (
    web
)
from phanterpwa.backend.decorators import (
    # check_client_token,
    # check_url_token,
    # check_public_csrf_token,
    check_private_csrf_token,
    check_user_token
)
from phanterpwa.i18n import browser_language
from phanterpwa.backend.security import (
    Serialize,
    SignatureExpired,
    BadSignature,
    URLSafeSerializer,
)
from pydal.validators import (
    IS_EMAIL
)

re_email_messages = re.compile(r"\$[0-9]{13}\:.+")

class Messages(web.RequestHandler):
    """
        /api/messages/(count|inbox|outbox)
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

    @check_user_token()
    def get(self, *args):
        arg0 = args[0]
        db = self.DALDatabase
        id_user = self.phanterpwa_current_user.id
        if arg0 == "count":
            q_messages = db(
                (db.internal_messages_recipients.message_read == False)
                & (db.internal_messages_recipients.recipients == id_user)
            )
            c_messages = q_messages.count()
            self.set_status(200)
            return self.write({
                'status': 'OK',
                'code': 200,
                'new_messages': c_messages,
            })
        elif arg0 == "inbox":
            message = 'list of available messages'
            i18nmessage = self.T(message)
            s_messages = db(
                (db.internal_messages_recipients.recipients == id_user)
                & (db.internal_messages_recipients.internal_messages == db.internal_messages.id)
                & (db.internal_messages.senders == db.auth_user.id)
            ).select(
                db.internal_messages.id,
                db.internal_messages.subject,
                db.internal_messages.send_on,
                db.internal_messages_recipients.message_read,
                db.auth_user.email,
                db.auth_user.id,
                db.auth_user.first_name,
                db.auth_user.last_name,
                groupby=db.internal_messages.id,
                orderby=~db.internal_messages_recipients.message_read | ~db.internal_messages.send_on,
                limitby=(0, 200)
            )
            self.set_status(200)
            return self.write({
                'status': 'OK',
                'code': 200,
                'message': message,
                'i18n': {'message': i18nmessage},
                'internal_messages': json.loads(s_messages.as_json()),
            })
        elif arg0 == "outbox":
            message = 'list of available messages'
            i18nmessage = self.T(message)
            s_messages = db(
                (db.internal_messages.senders == id_user)
            ).iterselect(
                db.internal_messages.id,
                db.internal_messages.subject,
                db.internal_messages.send_on,
                groupby=db.internal_messages.id,
                orderby=~db.internal_messages.send_on,
                limitby=(0, 200)
            )
            internal_messages = []
            for x in s_messages:
                dict_send = json.loads(x.as_json())
                dict_send['recipients_and_read_status'] = [
                    [
                        "{0} {1} <{2}>".format(
                            r.recipients.first_name,
                            r.recipients.last_name,
                            r.recipients.email
                        ),
                        r.message_read
                    ] for r in db(
                        db.internal_messages_recipients.internal_messages == x.id
                    ).select()
                ]
                internal_messages.append(dict_send)

            self.set_status(200)
            return self.write({
                'status': 'OK',
                'code': 200,
                'message': message,
                'i18n': {'message': i18nmessage},
                'internal_messages': internal_messages,
            })

        message = 'Bad Request'
        i18nmessage = self.T(message)
        self.set_status(400)
        return self.write({
            'status': 'Bad Request',
            'code': 400,
            'message': message,
            'i18n': {'message': i18nmessage},
        })


class Message(web.RequestHandler):
    """
        /api/message/([0-9]+)?/?
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
                "phanterpwa-authorization,"
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
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

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})

    @check_user_token()
    def get(self, *args):
        arg0 = args[0]
        db = self.DALDatabase
        id_user = self.phanterpwa_current_user.id
        r_message = db(
            (db.internal_messages_recipients.internal_messages == arg0)
            & (db.internal_messages_recipients.internal_messages == db.internal_messages.id)
            & (db.internal_messages_recipients.recipients == id_user)
        ).select(
            db.internal_messages.text_message,
            db.internal_messages_recipients.ALL,
        ).first()
        if r_message:
            r_message.internal_messages_recipients.update_record(
                message_read=True
            )
            db.commit()
            message = 'open message'
            i18nmessage = self.T(message)
            self.set_status(200)
            return self.write({
                'status': 'OK',
                'code': 200,
                'message': message,
                'i18n': {'message': i18nmessage},
                'internal_message': json.loads(r_message.internal_messages.as_json()),
            })

        message = 'Message not found'
        i18nmessage = self.T(message)
        self.set_status(400)
        return self.write({
            'status': 'Bad Request',
            'code': 400,
            'message': message,
            'i18n': {'message': i18nmessage},
        })

    @check_user_token()
    def post(self, *args):
        db = self.DALDatabase
        db(
            (db.internal_messages.senders == self.phanterpwa_current_user.id)
            & (db.internal_messages.subject == None)
            & (db.internal_messages.text_message == None)
            & (db.internal_messages.message_sent != True)
        ).delete()
        id_new_message = db.internal_messages.insert(
            senders=self.phanterpwa_current_user.id,
            written_on=datetime.now(),
            message_sent=False
        )
        id_client = int(self.phanterpwa_client_token_checked["id_client"])
        db((db.csrf.client == id_client) &
            (db.csrf.form_identify == "phanterpwa-form-send-messages")).delete()
        t = Serialize(
            "csrf-{0}".format(self.projectConfig['BACKEND'][self.app_name]['secret_key']),
            self.projectConfig['BACKEND'][self.app_name]['default_time_csrf_token_expire']
        )
        id_csrf = db.csrf.insert(
            form_identify="phanterpwa-form-send-messages",
            user_agent=self.phanterpwa_user_agent,
            ip=self.phanterpwa_remote_ip,
            client=id_client
        )
        sign_csrf = t.dumps({
            'id': str(id_csrf),
            'form_identify': "phanterpwa-form-send-messages",
            'user_agent': self.phanterpwa_user_agent,
            'ip': self.phanterpwa_remote_ip,
            'user': self.phanterpwa_current_user.id
        })
        q_csrf = db(db.csrf.id == id_csrf).select().first()
        q_csrf.update_record(token=sign_csrf)
        message = 'Create new message'
        i18nmessage = self.T(message)
        db.commit()
        self.set_status(200)
        return self.write({
            'status': 'OK',
            'code': 200,
            'csrf': sign_csrf,
            'id_new_message': id_new_message,
            'message': message,
            'i18n': {'message': i18nmessage},
        })

    @check_private_csrf_token(form_identify=["phanterpwa-form-send-messages"])
    def put(self, *args):
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        arg0 = args[0]
        db = self.DALDatabase
        r_message = db(db.internal_messages.id == arg0).select().first()
        if r_message and r_message.senders == self.phanterpwa_current_user.id:
            text_message = dict_arguments.get("text_message", None)
            subject = dict_arguments.get("subject", None)
            recipients = dict_arguments.get("recipients", None)
            if all([text_message, subject, recipients]):
                try:
                    list_recipients = ast.literal_eval(json.loads(recipients))
                except Exception:
                    list_recipients = ast.literal_eval(recipients)
                if isinstance(list_recipients, list):
                    set_recipients, no_pass, error = self.filter_recipients(list_recipients)
                    c_recipients = db(db.auth_user.id.belongs(set_recipients)).count()
                    if c_recipients == len(set_recipients):
                        for recips in set_recipients:
                            db.internal_messages_recipients.insert(
                                internal_messages= r_message.id,
                                recipients=recips,
                                message_read=False
                            )
                            r_message.update_record(
                                text_message=text_message,
                                message_sent=True,
                                subject=subject,
                                send_on=datetime.now()
                            )
                        message = 'The message has been sent.'
                        i18nmessage = self.T(message)
                        db.commit()

                        self.set_status(200)
                        return self.write({
                            'status': 'OK',
                            'code': 200,
                            'message': message,
                            'i18n': {'message': i18nmessage},
                        })
                    else:
                        message = 'Any recipient added does not exist'
                        i18nmessage = self.T(message)
                        self.set_status(400)
                        return self.write({
                            'status': 'Bad Request',
                            'code': 400,
                            'message': message,
                            'i18n': {'message': i18nmessage},
                        })

            message = 'Recipient cannot be empty'
            i18nmessage = self.T(message)
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': message,
                'i18n': {'message': i18nmessage},
            })
        message = 'The form has errors'
        i18nmessage = self.T(message)
        self.set_status(400)
        return self.write({
            'status': 'Bad Request',
            'code': 400,
            'message': message,
            'i18n': {'message': i18nmessage},
        })

    def filter_recipients(self, values):
        tests = []
        email_pass = []
        email_no_pass = []
        messages_error = self.T("Emails were not found: {0}")
        errors = None
        db = self.DALDatabase
        for x in values:
            if re_email_messages.match(x):
                t_email = x[15:]
                if t_email not in tests:
                    tests.append(t_email)
                    if not IS_EMAIL()(t_email)[1]:
                        r_auth_user = db(db.auth_user.email == t_email).select(db.auth_user.id).first()
                        if r_auth_user:
                            email_pass.append(r_auth_user.id)
                        else:
                            email_no_pass.append(t_email)
                    else:
                        email_no_pass.append(t_email)
            else:
                raise ValueError("The value is invalid! Given: {0}".format(x))
        if email_no_pass:
            errors = messages_error.format(str(email_no_pass)) 

        return (email_pass, email_no_pass, errors)
