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

MSG = u"""______  _                    _               ______  _    _   ___  
| ___ \| |                  | |              | ___ \| |  | | / _ \ 
| |_/ /| |__    __ _  _ __  | |_   ___  _ __ | |_/ /| |  | |/ /_\ \\
|  __/ | '_ \  / _` || '_ \ | __| / _ \| '__||  __/ | |/\| ||  _  |
| |    | | | || (_| || | | || |_ |  __/| |   | |    \  /\  /| | | |
\_|    |_| |_| \__,_||_| |_| \__| \___||_|   \_|     \/  \/ \_| |_/

"""
class EchoWebSocket(websocket.WebSocketHandler):
    _connections = set()
    _online_users = {}

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
        # self.write_message(u"______  _                    _               ______  _    _   ___  ")
        # self.write_message(u"| ___ \| |                  | |              | ___ \| |  | | / _ \ ")
        # self.write_message(u"| |_/ /| |__    __ _  _ __  | |_   ___  _ __ | |_/ /| |  | |/ /_\ \\")
        # self.write_message(u"|  __/ | '_ \  / _` || '_ \ | __| / _ \| '__||  __/ | |/\| ||  _  |")
        # self.write_message(u"| |    | | | || (_| || | | || |_ |  __/| |   | |    \  /\  /| | | |")
        # self.write_message(u"\_|    |_| |_| \__,_||_| |_| \__| \___||_|   \_|     \/  \/ \_| |_/")
        self.write_message(MSG)
        self.phanterpwa_current_user = None
        self.get_connections().add(self)

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
                            if self.phanterpwa_current_user.id in self._online_users:
                                for con in self._online_users[self.phanterpwa_current_user.id]:
                                    if not con.ws_connection:
                                        self._online_users[self.phanterpwa_current_user.id].remove(con)
                                self._online_users[self.phanterpwa_current_user.id].add(self)
                            else:
                                self._online_users[self.phanterpwa_current_user.id] = set([self])
                            if msg == "command_online":
                                print("{0} webSocket opened".format(self.phanterpwa_current_user.email))
                                self.write_message(u"__ You're online")
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
                for con in self.get_connections():
                    print("usuario:", id(con))
                    con.write_message(
                        "O usuário {0} falou: {1}".format(id(self), message)
                    )

    @classmethod
    def get_online_user(cls, id_user):
        user_cons = cls.online_users().get(id_user, set())
        for con in user_cons:
            if not user_cons.ws_connection:
                user_cons.remove(con)
        return user_cons

    @classmethod
    def check_user_is_online(cls, id_user):
        if id_user in cls.get_online_user():
            return True
        else:
            return False

    @classmethod
    def get_connections(cls):
        return cls._connections

    def on_close(self):
        if self.phanterpwa_current_user:
            print(self.phanterpwa_current_user.email)
            try:
                del self._online_users[self.phanterpwa_current_user.id]
            except KeyError:
                pass
        else:
            print("Unknow webSocket closed")
        self.get_connections().remove(self)
