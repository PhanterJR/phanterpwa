import re
import json
from tornado import (
    websocket
)
from phanterpwa.backend.security import (
    Serialize,
    SignatureExpired,
    BadSignature,
    URLSafeSerializer,
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
        self.write_message(MSG)
        self.phanterpwa_current_user = None
        self.add_connection(self)

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
                            try:
                                new_set = set(self._online_users[self.phanterpwa_current_user.id])
                            except KeyError:
                                new_set = set([self])
                            else:
                                new_set.add(self)
                            to_remove = []
                            for con in new_set:
                                if not con.ws_connection:
                                    to_remove.append(con)
                            for con in to_remove:
                                new_set.remove(con)
                            self._online_users[self.phanterpwa_current_user.id] = new_set

                            if msg == "command_online":
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

    @classmethod
    def get_online_users(cls):
        user_cons = cls.get_connections()
        new_dict = dict()
        for con in user_cons:
            if con.phanterpwa_current_user and con.ws_connection:
                try:
                    new_set = set(new_dict[con.phanterpwa_current_user.id])
                except KeyError:
                    new_set = set()
                new_set.add(con)
                new_dict[con.phanterpwa_current_user.id] = new_set
        return new_dict

    @classmethod
    def check_user_is_online(cls, id_user):
        if id_user in cls.get_online_users():
            return True
        else:
            return False

    @classmethod
    def get_connections(cls):
        return tuple(cls._connections)

    @classmethod
    def add_connection(cls, connection):
        cls._connections.add(connection)

    @classmethod
    def remove_connection(cls, connection):
        try:
            cls._connections.remove(connection)
        except KeyError:
            pass

    def on_close(self):
        if self.phanterpwa_current_user:
            try:
                del self._online_users[self.phanterpwa_current_user.id]
            except KeyError:
                pass
        self.remove_connection(self)
