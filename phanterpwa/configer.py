import os
import sys
import json
import phanterpwa
import configparser
from glob import glob
from os.path import (
    normpath,
    join,
    isdir,
    isfile,
    dirname,
    basename
)
from phanterpwa.samples.project_config_sample import project_config_sample

ENV_PYTHON = normpath(sys.executable)
PATH_PHANTERPWA = dirname(phanterpwa.__file__)


class ProjectConfig():
    """
    Validates and creates a configuration file in json format based on api.ini and app.ini contained in the project's
    applications.

    To start when instantiating, enter the path to the file.

    :param dir_or_config_file: Project dir or config.json file

    Example:
        >>> import os
        >>> import phanterpwa
        >>> from phanterpwa.configer import ProjectConfig
        >>> test_folder = os.path.join(os.path.dirname(phanterpwa.__file__), "tests", "test_configer_path", "project01")
        >>> cfg = ProjectConfig(test_folder)
    """

    def __init__(self, dir_or_config_file):
        self.project_config_sample = self._new_dict(project_config_sample)
        self._set_file(dir_or_config_file)

    def _new_dict(self, d):
        for x in d:
            if isinstance(d[x], dict):
                d[x] = self._new_dict(d[x])
        return dict(d)

    @property
    def file(self):
        """gets the path of the current configuration file

        Example:
            >>> import os
            >>> import phanterpwa
            >>> from phanterpwa.configer import ProjectConfig
            >>> test_folder = os.path.join(os.path.dirname(phanterpwa.__file__), "tests", "test_configer_path", "project01")
            >>> cfg = ProjectConfig(test_folder)
            >>> cfg.file
            ../phanterpwa/tests/test_configer_path/project01/config.json
        """
        return self._file

    @property
    def project_ini(self):
        """returns the configparser instance of the "project.ini" file
        """
        return self._ini_project

    @property
    def api_ini(self):
        """returns the configparser instance of the "api.ini" file
        """

        return self._ini_api

    @property
    def secret_ini(self):
        """returns the configparser instance of the "secret.ini" file
        """
        return self._ini_secret

    @property
    def secret_ini_api(self):
        """returns the configparser instance of the "secret.ini" file
        """
        return self._ini_secret_api

    @property
    def apps_ini(self):
        """returns a dictionary with the configparser instances of the "app.ini" files for each application.
        The keys are the folder name for each application.
        """
        return self._ini_apps

    def _process(self):
        cfg = {}
        with open(self._file, 'r', encoding="utf-8") as f:
            cfg = json.load(f)
        if isinstance(cfg, dict):
            identify = cfg.get("CONFIG_INDENTIFY", None)

            if not identify:
                raise ValueError("The config file don't have the CONFIG_INDENTIFY key.")
            required_keys = self.project_config_sample.keys()
            for r in required_keys:
                if r not in cfg:
                    cfg[r] = {}
            cfg["CONFIG_INDENTIFY"] = "project_config"
            cfg["ENVIRONMENT"] = {
                "python": ENV_PYTHON,
                "path": normpath(dirname(ENV_PYTHON))
            }
            self._ini_secret = configparser.ConfigParser()
            self._ini_secret.read(join(cfg["PROJECT"]["path"], 'secret.ini'), encoding='utf-8')
            sections_secret = self._ini_secret.sections()

            self._ini_secret_api = configparser.ConfigParser()
            self._ini_secret_api.read(join(cfg["PROJECT"]["path"], "api", 'secret.ini'), encoding='utf-8')
            sections_secret_api = self._ini_secret_api.sections()

            self._ini_project = configparser.ConfigParser()
            self._ini_project.read(join(cfg["PROJECT"]["path"], 'project.ini'), encoding='utf-8')
            sections_project = self._ini_project.sections()
            required_on_ini = [
                "title",
                "version",
                "author",
                "debug",
                "packaged"
            ]
            if "PROJECT" in sections_project:
                cfg["PROJECT"]["path"] = normpath(dirname(join(self._file)))
                cfg["PROJECT"]["name"] = basename(cfg["PROJECT"]["path"])
                sections_project.pop(sections_project.index("PROJECT"))
                for k in required_on_ini:
                    if k == "debug" or k == "packaged":
                        cfg["PROJECT"][k] = self._ini_project["PROJECT"].getboolean(
                            k, self.project_config_sample["PROJECT"][k])
                    else:
                        cfg["PROJECT"][k] = self._ini_project["PROJECT"].get(
                            k, self.project_config_sample["PROJECT"][k])
            else:
                cfg["PROJECT"] = self.project_config_sample["PROJECT"]
                cfg["PROJECT"]["path"] = normpath(dirname(join(self._file)))
                cfg["PROJECT"]["name"] = basename(cfg["PROJECT"]["path"])
                self._ini_project["PROJECT"] = {}
            for k in required_on_ini:
                self._ini_project["PROJECT"][k] = str(cfg["PROJECT"][k])
            if "compilation" not in cfg["PROJECT"]:
                cfg["PROJECT"]["compilation"] = 0

            self._ini_api = configparser.ConfigParser()
            self._ini_api.read(join(cfg["PROJECT"]["path"], 'api', 'api.ini'), encoding='utf-8')
            sections_api = self._ini_api.sections()

            required_on_ini = [
                "default_time_user_token_expire",
                "default_time_user_token_expire_remember_me",
                "default_time_csrf_token_expire",
                "default_time_temporary_password_expire",
                "timeout_to_resend_temporary_password_mail",
                "default_time_client_token_expire",
                "default_time_activation_code_expire",
                "default_time_two_factor_code_expire",
                "wait_time_to_try_activate_again",
                "timeout_to_resend_activation_email",
                "timeout_to_resign",
                "timeout_to_next_login_attempt",
                "max_login_attempts",
                "max_activation_attempts",
                "remote_address_debug",
                "websocket_address_debug",
                "remote_address",
                "websocket_address",
                "host",
                "port"
            ]
            if "API" in sections_api:
                sections_api.pop(sections_api.index("API"))
                for k in required_on_ini:
                    v = self._ini_api["API"].get(k, None)
                    if v is None:
                        cfg["API"][k] = self.project_config_sample["API"][k]
                    else:
                        if v.isdigit():
                            cfg["API"][k] = int(v)
                        elif v.lower() == "false":
                            cfg["API"][k] = False
                        elif v.lower() == "true":
                            cfg["API"][k] = True
                        else:
                            cfg["API"][k] = v
            else:
                self._ini_api["API"] = {}
                cfg["API"] = self.project_config_sample["API"]
            for k in required_on_ini:
                self._ini_api["API"][k] = str(cfg["API"][k])

            required_on_ini = [
                "secret_key",
                "url_secret_key"
            ]

            if "API" in sections_secret_api:
                for k in required_on_ini:
                    cfg["API"][k] = self._ini_secret_api["API"].get(k, self.project_config_sample["API"][k])
            else:
                self._ini_secret_api["API"] = {}
                secret_key = cfg["API"].get("secret_key", os.urandom(12).hex())
                url_secret_key = cfg["API"].get("url_secret_key", os.urandom(12).hex())
                cfg["API"]["secret_key"] = secret_key
                cfg["API"]["url_secret_key"] = url_secret_key

            for k in required_on_ini:
                self._ini_secret_api["API"][k] = str(cfg["API"][k])

            with open(join(cfg["PROJECT"]["path"], 'api', 'api.ini'), 'w', encoding="utf-8") as configfile:
                self._ini_api.write(configfile)

            with open(join(cfg["PROJECT"]["path"], 'api', 'secret.ini'), 'w', encoding="utf-8") as configfile:
                self._ini_secret_api.write(configfile)

            current_port = cfg["API"]["port"]
            ports = set([cfg["API"]["port"]])
            self._ini_apps = dict()
            apps_list = []
            for a in glob(join(cfg["PROJECT"]["path"], "apps", "*")):
                if isdir(a) and isfile(join(a, "app.ini")):
                    app_name = basename(a)
                    apps_list.append(app_name)
                    ini_app = configparser.ConfigParser()
                    ini_app.read(join(a, "app.ini"), encoding='utf-8')
                    app_sections = ini_app.sections()
                    required_on_ini = [
                        "title",
                        "timeout_to_resign",
                        "transcrypt_main_file",
                        "styles_main_file",
                        "views_main_file"
                    ]
                    if "APP" in app_sections:
                        cfg["APPS"][app_name] = {"build_folder":
                            normpath(join(cfg["PROJECT"]["path"], "apps", app_name, "www"))}

                        for k in required_on_ini:
                            v = ini_app["APP"].get(k, None)
                            if v is None:
                                if k == "port" or k == "host":
                                    pass
                                else:
                                    cfg["APPS"][app_name][k] = self.project_config_sample["APPS"]["app_01"][k]
                                    ini_app["APP"][k] = cfg["APPS"][app_name][k]
                            else:
                                if v.isdigit():
                                    if k == "port" or k == "host":
                                        pass
                                    else:
                                        cfg["APPS"][app_name][k] = int(v)
                                elif v == "false":
                                    cfg["APPS"][app_name][k] = False
                                elif v == "true":
                                    cfg["APPS"][app_name][k] = True
                                else:
                                    cfg["APPS"][app_name][k] = v
                    else:
                        ini_app["APP"] = {}
                        cfg["APPS"][app_name] = self.project_config_sample["APPS"]["app_01"]
                        cfg["APPS"][app_name]["build_folder"] = \
                            normpath(join(cfg["PROJECT"]["path"], "apps", app_name, "www"))
                    for k in required_on_ini:
                        ini_app["APP"][k] = str(cfg["APPS"][app_name][k])
                    cfg["APPS"][app_name]["host"] = "127.0.0.1"
                    while current_port in ports:
                        current_port += 1
                    else:
                        ports.add(current_port)
                        cfg["APPS"][app_name]["port"] = current_port
                    with open(join(a, "app.ini"), 'w', encoding="utf-8") as configfile:
                        ini_app.write(configfile)

                    if "CONFIGJS" in app_sections:
                        cfg["APPS"][app_name]["CONFIGJS"] = {}

                        for v in ini_app.items("CONFIGJS"):
                            if v.isdigit():
                                cfg["APPS"][app_name]["CONFIGJS"][k] = int(v)
                            elif v.lower() == "false":
                                cfg["APPS"][app_name]["CONFIGJS"][k] = False
                            elif v.lower() == "true":
                                cfg["APPS"][app_name]["CONFIGJS"][k] = True
                            else:
                                cfg["APPS"][app_name]["CONFIGJS"][k] = v
                    self._ini_apps[app_name] = ini_app
            current_apps = list(cfg['APPS'].keys())
            for ha in current_apps:
                if ha not in apps_list:
                    del cfg['APPS'][ha]

            required_on_ini = [
                "server",
                "username",
                "default_sender",
                "port",
                "use_tls",
                "use_ssl"
            ]
            if "EMAIL" in sections_project:
                sections_project.pop(sections_project.index("EMAIL"))
                for k in required_on_ini:
                    if k == "use_tls" or k == "use_ssl":
                        cfg["EMAIL"][k] = self._ini_project["EMAIL"].getboolean(
                            k, self.project_config_sample["EMAIL"][k])
                    elif self._ini_project["EMAIL"].get(k).isdigit():
                        cfg["EMAIL"][k] = int(self._ini_project["EMAIL"].get(k))
                    else:
                        cfg["EMAIL"][k] = self._ini_project["EMAIL"].get(
                            k, self.project_config_sample["EMAIL"][k])
            else:
                self._ini_project["EMAIL"] = {}
                cfg["EMAIL"] = self.project_config_sample["EMAIL"]
            for k in required_on_ini:
                self._ini_project["EMAIL"][k] = str(cfg["EMAIL"][k])

            required_on_ini = [
                "password"
            ]

            if "EMAIL" in sections_secret:
                for k in required_on_ini:
                    cfg["EMAIL"][k] = self._ini_secret["EMAIL"].get(k, self.project_config_sample["EMAIL"][k])
            else:
                self._ini_secret["EMAIL"] = {}
                password = cfg["EMAIL"].get("password", "your_password")
                cfg["EMAIL"]["password"] = password
            for k in required_on_ini:
                self._ini_secret["EMAIL"][k] = str(cfg["EMAIL"][k])

            required_on_ini = [
                "copyright",
                "link_to_your_site"
            ]
            if "CONTENT_EMAILS" in sections_project:
                sections_project.pop(sections_project.index("CONTENT_EMAILS"))
                for k in required_on_ini:
                    cfg["CONTENT_EMAILS"][k] = self._ini_project["CONTENT_EMAILS"].get(
                        k, self.project_config_sample["CONTENT_EMAILS"][k])
            else:
                self._ini_project["CONTENT_EMAILS"] = {}
                cfg["CONTENT_EMAILS"] = self.project_config_sample["CONTENT_EMAILS"]
            for k in required_on_ini:
                self._ini_project["CONTENT_EMAILS"][k] = str(cfg["CONTENT_EMAILS"][k])
            with open(join(cfg["PROJECT"]["path"], 'project.ini'), 'w', encoding="utf-8") as configfile:
                self._ini_project.write(configfile)

            for p in sections_project:
                if p not in ["PROJECT", "EMAIL", "CONTENT_EMAILS"]:
                    cfg[p] = self._dict_value(dict(self._ini_project[p]))
            for p in sections_secret:
                if p not in ["API", "EMAIL"]:
                    if p in cfg:
                        secret_dict_values = self._dict_value(dict(self._ini_secret[p]))
                        for k in secret_dict_values:
                            cfg[p][k] = secret_dict_values[k]
                    else:
                        cfg[p] = self._dict_value(dict(self._ini_secret[p]))
        else:
            raise TypeError(
                "The config file has incorrect content, expected dict type. Given: {0}".format(type(cfg)))

        self._config = self._new_dict(cfg)

    def _set_file(self, value):
        if isfile(value) and basename(value) == "config.json":
            self._file = value
            self._process()
            self.save()
        elif isdir(value):
            if not isfile(os.path.join(value, "config.json")):
                with open(os.path.join(value, "config.json"), "w", encoding="utf-8") as f:
                    f.write(json.dumps(self.project_config_sample, ensure_ascii=True, indent=2))
            self._file = os.path.join(value, "config.json")
            self._process()
            self.save()
        else:
            raise ValueError("The config file must be config.json file or a valid dir. Given: {0}".format(value))

    def _dict_value(self, d):
        if isinstance(d, dict):
            for x in d:
                d[x] = self._dict_value(d[x])
            return d
        elif isinstance(d, str):
            if d.isdigit():
                return int(d)
            elif d.lower() == "false":
                return False
            elif d.lower() == "true":
                return True
            elif d.lower() == "none":
                return None
            else:
                return d
        else:
            return d

    @property
    def config(self):
        """returns the current setting

        Example:
            >>> import json
            >>> import os
            >>> import phanterpwa
            >>> from phanterpwa.configer import ProjectConfig
            >>> test_folder = os.path.join(os.path.dirname(phanterpwa.__file__), "tests", "test_configer_path", "project01")
            >>> cfg = ProjectConfig(test_folder)
            >>> string_cfg = json.dumps(cfg.config, indent=2)
            >>> print(string_cfg)
            {
              "CONFIG_INDENTIFY": "project_config",
              "ENVIRONMENT": {
                "path": "",
                "python": ""
              },
              "PROJECT": {
                "name": "PhanterPWA",
                "title": "PhanterPWA",
                "version": "0.0.1",
                "author": "PhanterJR<phanterjr@conexaodidata.com.br>",
                "debug": true,
                "packaged": true
              },
              "API": {
                "secret_key": "your_default_key",
                "url_secret_key": "your_default_key2",
                "default_time_user_token_expire": 7200,
                "default_time_user_token_expire_remember_me": 2592000,
                "default_time_csrf_token_expire": 4200,
                "default_time_temporary_password_expire": 4200,
                "timeout_to_resend_temporary_password_mail": 3900,
                "default_time_client_token_expire": 63072000,
                "default_time_activation_code_expire": 3600,
                "wait_time_to_try_activate_again": 3900,
                "timeout_to_resend_activation_email": 300,
                "timeout_to_resign": 600,
                "max_login_attempts": 5,
                "max_activation_attempts": 5
              },
              "APP": {
                "compiled_app_folder": "{{PROJECT_FOLDER}}\\app\\www",
                "address_in_development": "http://127.0.0.1:8882"
              },
              "PATH": {
                "project": "{{PROJECT_FOLDER}}",
                "api": "{{PROJECT_FOLDER}}\\api",
                "app": "{{PROJECT_FOLDER}}\\app"
              },
              "EMAIL": {
                "server": "mail.yourservermail.com",
                "username": "username@yourservermail.com",
                "default_sender": "contato@conexaodidata.com.br",
                "password": "password",
                "port": 465,
                "use_tls": true,
                "use_ssl": true
              },
              "TRANSCRYPT": {
                "main_files": [
                  "{{PROJECT_FOLDER}}\\app\\scripts\\application\\application.py",
                  "{{PROJECT_FOLDER}}\\app\\scripts\\websocket\\websocket.py"
                ]
              },
              "API_SERVER": {
                "host": "127.0.0.1",
                "port": 8881
              },
              "APP_SERVER": {
                "host": "127.0.0.1",
                "port": 8882
              },
              "CONFIGJS": {
                "api_server_address": "http://127.0.0.1:8881",
                "api_websocket_address": "ws://127.0.0.1:8881/websocket",
                "timeout_to_resign": 600
              },
              "CONTENT_EMAILS": {
                "copyright": "Conex\u00e3o Didata \u00a9 2011-{{now}}",
                "link_to_your_site": "https://phanterpwa.conexaodidata.com.br"
              }
            }
        """
        return self._config

    def save(self):
        """saves changes made to configuration files
            Example:
            >>> import json
            >>> import os
            >>> import phanterpwa
            >>> from phanterpwa.configer import ProjectConfig
            >>> test_folder = os.path.join(os.path.dirname(phanterpwa.__file__), "tests", "test_configer_path", "project01")
            >>> cfg = ProjectConfig(test_folder)
            >>> cfg['PROJECT']['title']
            PhanterPWA
            >>> cfg['PROJECT']['title'] = 'PhanterPWA2'
            >>> cfg.save()
            >>> with open(os.path.join(test_folder, "config.json"), encoding="utf-8") as f:
            ...     content = json.load(f)
            >>> content['PROJECT']['title']
            PhanterPWA2
        """
        t = self._file
        with open(t, "w", encoding="utf-8") as f:
            json.dump(self._config, f, ensure_ascii=True, indent=4)

        for x in self.project_ini.sections():
            for y in self.project_ini.items(x):
                v = str(self._config[x][y[0]])
                self.project_ini[x][y[0]] = v

        # for x in self.api_ini.sections():
        #     if x not in ['DEVELOPMENT', 'PRODUCTION']:
        #         for y in self.api_ini.items(x):
        #             v = str(self._config[x][y[0]])
        #             self.api_ini[x][y[0]] = v
        #     else:
        #         KX = x.lower()
        #         for y in self.api_ini.items(x):
        #             k = "{0}_on_{1}".format(y[0], KX)
        #             v = str(self._config['API'][k])
        #             self.api_ini[x][y[0]] = v

        for x in self.secret_ini.sections():
            for y in self.secret_ini.items(x):
                v = str(self._config[x][y[0]])
                self.secret_ini[x][y[0]] = v

        for x in self.secret_ini.sections():
            for y in self.secret_ini.items(x):
                v = str(self._config[x][y[0]])
                self.secret_ini[x][y[0]] = v

        with open(join(self._config["PROJECT"]["path"], 'project.ini'), 'w', encoding="utf-8") as configfile:
            self._ini_project.write(configfile)
        with open(join(self._config["PROJECT"]["path"], 'secret.ini'), 'w', encoding="utf-8") as configfile:
            self._ini_secret.write(configfile)
        with open(join(self._config["PROJECT"]["path"], 'api', 'api.ini'), 'w', encoding="utf-8") as configfile:
            self._ini_api.write(configfile)

        for a in self.apps_ini:
            for x in self.apps_ini[a].sections():
                if x == "APP":
                    for y in self.apps_ini[a].items(x):
                        v = str(self._config['APPS'][a][y[0]])
                        self.apps_ini[a][x][y[0]] = v
            with open(join(self._config["PROJECT"]["path"], 'apps', a, 'app.ini'), 'w', encoding="utf-8") as configfile:
                self.apps_ini[a].write(configfile)

    def __iter__(self):
        for c in self._config:
            yield c

    def __getitem__(self, i):
        return self._config[i]

    def __setitem__(self, i, v):
        self._config[i] = v
        self.save()

    def get(self, k, default=None):
        return self._config.get(k, default)
