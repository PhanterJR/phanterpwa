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
VERSION_PYTHON = "{0}.{1}.{2}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])
PATH_PHANTERPWA = dirname(phanterpwa.__file__)
VERSION_PHANTERPWA = phanterpwa.__version__


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
    def project_secret_ini(self):
        """returns the configparser instance of the "secret.ini" file
        """
        return self._ini_secret

    @property
    def backend_ini(self):
        """returns a dictionary with the configparser instances of the "app.ini" files for each backend application.
        The keys are the folder name for each application.
        """
        return self._ini_apps_backend

    @property
    def frontend_ini(self):
        """returns a dictionary with the configparser instances of the "app.ini" files for each frontend application.
        The keys are the folder name for each application.
        """
        return self._ini_apps_frontend

    @property
    def backend_secret_ini(self):
        """returns a dictionary with the configparser instances of the "app.ini" files for each backend application.
        The keys are the folder name for each application.
        """
        return self._ini_secret_apps_backend

    @property
    def frontend_secret_ini(self):
        """returns a dictionary with the configparser instances of the "app.ini" files for each frontend application.
        The keys are the folder name for each application.
        """
        return self._secret_ini_apps_frontend

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
                "path": normpath(dirname(ENV_PYTHON)),
                "python_version": VERSION_PYTHON,
                "phanterpwa_version": VERSION_PHANTERPWA
            }
            self._ini_secret = configparser.ConfigParser()
            self._ini_secret.read(join(cfg["PROJECT"]["path"], 'secret.ini'), encoding='utf-8')
            sections_secret = self._ini_secret.sections()

            self._ini_project = configparser.ConfigParser()
            self._ini_project.read(join(cfg["PROJECT"]["path"], 'project.ini'), encoding='utf-8')
            sections_project = self._ini_project.sections()
            required_on_ini = [
                "title",
                "version",
                "author",
                "debug",
                "minify",
                "packaged"
            ]
            if "PROJECT" in sections_project:
                cfg["PROJECT"]["path"] = normpath(dirname(join(self._file)))
                cfg["PROJECT"]["name"] = basename(cfg["PROJECT"]["path"])
                sections_project.pop(sections_project.index("PROJECT"))
                for k in required_on_ini:
                    if k == "debug" or k == "packaged" or k == "minify":
                        cfg["PROJECT"][k] = self._ini_project["PROJECT"].getboolean(
                            k, self.project_config_sample["PROJECT"][k])
                    elif k == "baseport":
                        v = self._ini_project["PROJECT"].get(
                            k, self.project_config_sample["PROJECT"][k])
                        if str(v).isdigit():
                            cfg["PROJECT"][k] = int(v)
                    else:
                        cfg["PROJECT"][k] = self._ini_project["PROJECT"].get(
                            k, self.project_config_sample["PROJECT"][k])
                for i in self._ini_project.items("PROJECT"):
                    cfg["PROJECT"][i[0]] = self._dict_value(i[1])
            else:
                cfg["PROJECT"] = self.project_config_sample["PROJECT"]
                cfg["PROJECT"]["path"] = normpath(dirname(join(self._file)))
                cfg["PROJECT"]["name"] = basename(cfg["PROJECT"]["path"])
                self._ini_project["PROJECT"] = {}
            for k in required_on_ini:
                self._ini_project["PROJECT"][k] = str(cfg["PROJECT"][k])
            if "compilation" not in cfg["PROJECT"]:
                cfg["PROJECT"]["compilation"] = 0
                cfg["PROJECT"]["versioning"] = "{0}.{1}".format(
                    cfg["PROJECT"].get("version", "0.0.1"),
                    0
                )
            if "baseport" not in cfg["PROJECT"]:
                cfg["PROJECT"]["baseport"] = self.project_config_sample["PROJECT"]["baseport"]
            if "basehost" not in cfg["PROJECT"]:
                cfg["PROJECT"]["basehost"] = self.project_config_sample["PROJECT"]["basehost"]

            current_port = cfg["PROJECT"]["baseport"]
            ports = set()

            self._ini_apps_backend = dict()
            self._ini_secret_apps_backend = dict()
            apps_backend_list = []
            for a in glob(join(cfg["PROJECT"]["path"], "backapps", "*")):
                if isdir(a):
                    app_name = basename(a)
                    apps_backend_list.append(app_name)
                    if isfile(join(a, "app.ini")):
                        ini_app = configparser.ConfigParser()
                        ini_app.read(join(a, "app.ini"), encoding='utf-8')
                        app_sections = ini_app.sections()
                        required_on_ini = [
                            "title"
                        ]
                        if "APP" in app_sections:
                            cfg["BACKEND"][app_name] = {}

                            for k in required_on_ini:
                                v = ini_app["APP"].get(k, None)
                                if v is None:
                                    if k == "port" or k == "host":
                                        pass
                                    else:
                                        cfg["BACKEND"][app_name][k] = self.project_config_sample["BACKEND"]["sample_app"][k]
                                        ini_app["APP"][k] = cfg["BACKEND"][app_name][k]
                                else:
                                    if v.isdigit():
                                        if k == "port" or k == "host":
                                            pass
                                        else:
                                            cfg["BACKEND"][app_name][k] = int(v)
                                    elif v == "false":
                                        cfg["BACKEND"][app_name][k] = False
                                    elif v == "true":
                                        cfg["BACKEND"][app_name][k] = True
                                    else:
                                        cfg["BACKEND"][app_name][k] = v
                            for i in ini_app.items("APP"):
                                cfg["BACKEND"][app_name][i[0]] = self._dict_value(i[1])
                        else:
                            ini_app["APP"] = {}
                            cfg["BACKEND"][app_name] = self.project_config_sample["BACKEND"]["sample_app"]
                        for k in required_on_ini:
                            ini_app["APP"][k] = str(cfg["BACKEND"][app_name][k])
                        cfg["BACKEND"][app_name]["host"] = cfg["PROJECT"]["basehost"] or "127.0.0.1"
                        while current_port in ports:
                            current_port += 1
                        else:
                            ports.add(current_port)
                            cfg["BACKEND"][app_name]["port"] = current_port
                        with open(join(a, "app.ini"), 'w', encoding="utf-8") as configfile:
                            ini_app.write(configfile)

                        self._ini_apps_backend[app_name] = ini_app

                    if isfile(join(a, "secret.ini")):
                        ini_secret_app = configparser.ConfigParser()
                        ini_secret_app.read(join(a, "secret.ini"), encoding='utf-8')
                        app_sections = ini_secret_app.sections()
                        if "APP" in app_sections:
                            if app_name in cfg["BACKEND"] and isinstance(cfg["BACKEND"][app_name], dict):
                                for i in ini_secret_app.items("APP"):
                                    cfg["BACKEND"][app_name][i[0]] = self._dict_value(i[1])
                        else:
                            ini_secret_app["APP"] = {}
                        with open(join(a, "secret.ini"), 'w', encoding="utf-8") as configfile:
                            ini_secret_app.write(configfile)

                        self._ini_secret_apps_backend[app_name] = ini_secret_app
                    else:
                        ini_secret_app = configparser.ConfigParser()
                        ini_secret_app["APP"] = {
                            'secret_key': os.urandom(12).hex()
                        }
                        with open(join(a, "secret.ini"), 'w', encoding="utf-8") as configfile:
                            ini_secret_app.write(configfile)

            current_apps = list(cfg['BACKEND'].keys())
            for ha in current_apps:
                if ha not in apps_backend_list:
                    del cfg['BACKEND'][ha]

            self._ini_apps_frontend = dict()
            self._ini_secret_apps_frontend = dict()
            apps_frontend_list = []

            for a in glob(join(cfg["PROJECT"]["path"], "frontapps", "*")):
                if isdir(a):
                    app_name = basename(a)
                    apps_frontend_list.append(app_name)
                    if isfile(join(a, "app.ini")):
                        ini_app = configparser.ConfigParser()
                        ini_app.read(join(a, "app.ini"), encoding='utf-8')
                        app_sections = ini_app.sections()
                        required_on_ini = [
                            "title",
                            "transcrypt_main_file",
                            "styles_main_file",
                            "views_main_file"
                        ]
                        if "APP" in app_sections:
                            cfg["FRONTEND"][app_name] = {"build_folder":
                                normpath(join(cfg["PROJECT"]["path"], "frontapps", app_name, "www"))}

                            for k in required_on_ini:
                                v = ini_app["APP"].get(k, None)
                                if v is None:
                                    if k == "port" or k == "host":
                                        pass
                                    else:
                                        cfg["FRONTEND"][app_name][k] = self.project_config_sample["FRONTEND"]["sample_app"][k]
                                        ini_app["APP"][k] = cfg["FRONTEND"][app_name][k]
                                else:
                                    if v.isdigit():
                                        if k == "port" or k == "host":
                                            pass
                                        else:
                                            cfg["FRONTEND"][app_name][k] = int(v)
                                    elif v == "false":
                                        cfg["FRONTEND"][app_name][k] = False
                                    elif v == "true":
                                        cfg["FRONTEND"][app_name][k] = True
                                    else:
                                        cfg["FRONTEND"][app_name][k] = v
                            for i in ini_app.items("APP"):
                                cfg["FRONTEND"][app_name][i[0]] = self._dict_value(i[1])
                        else:
                            ini_app["APP"] = {}
                            cfg["FRONTEND"][app_name] = self.project_config_sample["FRONTEND"]["sample_app"]
                            cfg["FRONTEND"][app_name]["build_folder"] = \
                                normpath(join(cfg["PROJECT"]["path"], "frontapps", app_name, "www"))
                        for k in required_on_ini:
                            ini_app["APP"][k] = str(cfg["FRONTEND"][app_name][k])

                        cfg["FRONTEND"][app_name]["host"] = cfg["PROJECT"]["basehost"] or "127.0.0.1"
                        while current_port in ports:
                            current_port += 1
                        else:
                            ports.add(current_port)
                            cfg["FRONTEND"][app_name]["port"] = current_port
                        with open(join(a, "app.ini"), 'w', encoding="utf-8") as configfile:
                            ini_app.write(configfile)

                        self._ini_apps_frontend[app_name] = ini_app

                    if isfile(join(a, "secret.ini")):
                        ini_secret_app = configparser.ConfigParser()
                        ini_secret_app.read(join(a, "secret.ini"), encoding='utf-8')
                        app_sections = ini_secret_app.sections()
                        if "APP" in app_sections:
                            if app_name in cfg["FRONTEND"] and isinstance(cfg["FRONTEND"][app_name], dict):
                                for i in ini_secret_app.items("APP"):
                                    cfg["FRONTEND"][app_name][i[0]] = self._dict_value(i[1])
                        else:
                            ini_secret_app["APP"] = {}

                        with open(join(a, "secret.ini"), 'w', encoding="utf-8") as configfile:
                            ini_secret_app.write(configfile)

                        self._ini_secret_apps_frontend[app_name] = ini_secret_app


            current_apps = list(cfg['FRONTEND'].keys())
            for ha in current_apps:
                if ha not in apps_frontend_list:
                    del cfg['FRONTEND'][ha]

            for p in sections_project:
                if p not in ["PROJECT"]:
                    cfg[p] = self._dict_value(dict(self._ini_project[p]))
            for p in sections_secret:
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
              "BACKEND": {
              },
              "FRONTEND": {
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

        for x in self.project_secret_ini.sections():
            for y in self.project_secret_ini.items(x):
                v = str(self._config[x][y[0]])
                self.project_secret_ini[x][y[0]] = v

        with open(join(self._config["PROJECT"]["path"], 'project.ini'), 'w', encoding="utf-8") as configfile:
            self._ini_project.write(configfile)

        with open(join(self._config["PROJECT"]["path"], 'secret.ini'), 'w', encoding="utf-8") as configfile:
            self._ini_secret.write(configfile)

        for a in self.backend_ini:
            for x in self.backend_ini[a].sections():
                if x == "APP":
                    for y in self.backend_ini[a].items(x):
                        v = str(self._config['BACKEND'][a][y[0]])
                        self.backend_ini[a][x][y[0]] = v
            with open(join(self._config["PROJECT"]["path"], "backapps", a, 'app.ini'), 'w', encoding="utf-8") as configfile:
                self.backend_ini[a].write(configfile)

        for a in self.frontend_ini:
            for x in self.frontend_ini[a].sections():
                if x == "APP":
                    for y in self.frontend_ini[a].items(x):
                        v = str(self._config['FRONTEND'][a][y[0]])
                        self.frontend_ini[a][x][y[0]] = v
            with open(join(self._config["PROJECT"]["path"], "frontapps", a, 'app.ini'), 'w', encoding="utf-8") as configfile:
                self.frontend_ini[a].write(configfile)

        # for a in self.backend_secret_ini:
        #     for x in self.backend_secret_ini[a].sections():
        #         if x == "APP":
        #             for y in self.backend_secret_ini[a].items(x):
        #                 v = str(self._config['BACKEND'][a][y[0]])
        #                 self.backend_secret_ini[a][x][y[0]] = v
        #     with open(join(self._config["PROJECT"]["path"], "backapps", a, 'secret.ini'), 'w', encoding="utf-8") as configfile:
        #         self.backend_secret_ini[a].write(configfile)

        # for a in self.frontend_secret_ini:
        #     for x in self.frontend_secret_ini[a].sections():
        #         if x == "APP":
        #             for y in self.frontend_secret_ini[a].items(x):
        #                 v = str(self._config['FRONTEND'][a][y[0]])
        #                 self.frontend_secret_ini[a][x][y[0]] = v
        #     with open(join(self._config["PROJECT"]["path"], "frontapps", a, 'secret.ini'), 'w', encoding="utf-8") as configfile:
        #         self.frontend_secret_ini[a].write(configfile)

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
