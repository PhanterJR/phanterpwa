import re
import json
from tornado import (
    websocket
)
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serialize,
    BadSignature,
    SignatureExpired
)
check_compilation = re.compile(r"check_compilation\[([0-9]*)\]")


class EchoWebSocket(websocket.WebSocketHandler):
    connections = set()

    def initialize(self, app_name, projectConfig, DALDatabase, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.i18nTranslator = i18nTranslator
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.phanterpwa_current_user = None

    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message(u"______  _                    _               ______  _    _   ___  ")
        self.write_message(u"| ___ \| |                  | |              | ___ \| |  | | / _ \ ")
        self.write_message(u"| |_/ /| |__    __ _  _ __  | |_   ___  _ __ | |_/ /| |  | |/ /_\ \\")
        self.write_message(u"|  __/ | '_ \  / _` || '_ \ | __| / _ \| '__||  __/ | |/\| ||  _  |")
        self.write_message(u"| |    | | | || (_| || | | || |_ |  __/| |   | |    \  /\  /| | | |")
        self.write_message(u"\_|    |_| |_| \__,_||_| |_| \__| \___||_|   \_|     \/  \/ \_| |_/")
        self.phanterpwa_current_user = None
        self.connections.add(self)

    def on_message(self, message):
        if message.startswith("{"):
            msg = None
            try:
                json_message = json.loads(message)
            except Exception as e:
                return self.write_message("JSON ERROR")
            else:
                id_user = None
                if "phanterpwa-authorization" in json_message and "message" in json_message:
                    msg = json_message["message"]
                    if json_message["phanterpwa-authorization"] is not "anonymous":
                        t = Serialize(
                            self.projectConfig['BACKEND'][self.app_name]['secret_key'],
                            self.projectConfig['BACKEND'][self.app_name]['default_time_user_token_expire']
                        )
                        token_content = None
                        try:
                            token_content = t.loads(json_message['phanterpwa-authorization'])
                        except BadSignature:
                            token_content = None
                        except SignatureExpired:
                            token_content = None
                        if token_content and 'id' in token_content:
                            id_user = token_content['id']
                    if id_user:
                        q_user = self.DALDatabase(self.DALDatabase.auth_user.id == id_user).select().first()
                        if q_user:
                            self.phanterpwa_current_user = q_user
                            if msg == "command_online":
                                print("{0} webSocket opened".format(self.phanterpwa_current_user.email))
                                q_user.update_record(websocket_opened=True)
                                self.DALDatabase.commit()
                                self.write_message(u"__ You're online")
                                return
                            elif msg == "command_offline":
                                q_user.update_record(websocket_opened=False)
                                self.DALDatabase.commit()
                                self.write_message(u"__ You're offline. Bye.")
                                return

        if message[:17] == "check_compilation":
            r = check_compilation.findall(message)
            if r:
                app_compilation = r[0]
                if str(self.projectConfig['PROJECT']['compilation']) == app_compilation:
                    self.write_message("Compilation: {0}".format(app_compilation))
                else:
                    self.write_message("reload")
        else:
            self.write_message(u"You said: " + message)

    def on_close(self):
        if self.phanterpwa_current_user:
            self.phanterpwa_current_user.update_record(websocket_opened=False)
            self.DALDatabase.commit()
            print("{0} webSocket closed".format(self.phanterpwa_current_user.email))
        else:
            print("Unknow webSocket closed")
        self.connections.remove(self)
