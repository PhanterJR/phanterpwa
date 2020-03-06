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
    def __init__(self, file):
        self.file = file

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        cfg = {}
        if all([isfile(join(value)),
                basename(join(value)) == "config.json"]):

            with open(value, 'r', encoding="utf-8") as f:
                cfg = json.load(f)
            if isinstance(cfg, dict):
                identify = cfg.get("CONFIG_INDENTIFY", None)

                if not identify:
                    raise ValueError("The config file don't have the CONFIG_INDENTIFY key.")
                required_keys = project_config_sample.keys()
                for r in required_keys:
                    if r not in cfg:
                        cfg[r] = {}
                cfg["CONFIG_INDENTIFY"] = "project_config"
                cfg["ENVIRONMENT"] = {
                    "python": ENV_PYTHON,
                    "path": normpath(dirname(ENV_PYTHON))
                }
                ini_project = configparser.ConfigParser()
                ini_project.read(join(cfg["PROJECT"]["path"], 'project.ini'), encoding='utf-8')
                sections_project = ini_project.sections()
                required_on_ini = [
                    "title",
                    "version",
                    "author",
                    "debug",
                    "packaged"
                ]
                if "PROJECT" in sections_project:
                    cfg["PROJECT"]["path"] = normpath(dirname(join(value)))
                    cfg["PROJECT"]["name"] = basename(cfg["PROJECT"]["path"])
                    sections_project.pop(sections_project.index("PROJECT"))
                    for k in required_on_ini:
                        if k == "debug" or k == "packaged":
                            cfg["PROJECT"][k] = ini_project["PROJECT"].getboolean(
                                k, project_config_sample["PROJECT"][k])
                        else:
                            cfg["PROJECT"][k] = ini_project["PROJECT"].get(
                                k, project_config_sample["PROJECT"][k])
                else:
                    cfg["PROJECT"] = project_config_sample["PROJECT"]
                    cfg["PROJECT"]["path"] = normpath(dirname(join(value)))
                    cfg["PROJECT"]["name"] = basename(cfg["PROJECT"]["path"])
                    ini_project["PROJECT"] = {}
                for k in required_on_ini:
                    ini_project["PROJECT"][k] = str(cfg["PROJECT"][k])

                ini_api = configparser.ConfigParser()
                ini_api.read(join(cfg["PROJECT"]["path"], 'api', 'api.ini'), encoding='utf-8')
                sections_api = ini_api.sections()

                secret_key = cfg["API"].get("secret_key", "{{secret_key}}")
                url_secret_key = cfg["API"].get("url_secret_key", "{{url_secret_key}}")
                required_on_ini = [
                    "default_time_user_token_expire",
                    "default_time_user_token_expire_remember_me",
                    "default_time_csrf_token_expire",
                    "default_time_temporary_password_expire",
                    "timeout_to_resend_temporary_password_mail",
                    "default_time_client_token_expire",
                    "default_time_activation_code_expire",
                    "wait_time_to_try_activate_again",
                    "timeout_to_resend_activation_email",
                    "timeout_to_resign",
                    "timeout_to_next_login_attempt",
                    "max_login_attempts",
                    "max_activation_attempts",
                    "host",
                    "port"
                ]
                if "API" in sections_api:
                    sections_api.pop(sections_api.index("API"))
                    for k in required_on_ini:
                        v = ini_api["API"].get(k, None)
                        if v is None:
                            cfg["API"][k] = project_config_sample["API"][k]
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
                    ini_api["API"] = {}
                    cfg["API"] = project_config_sample["API"]
                for k in required_on_ini:
                    ini_api["API"][k] = str(cfg["API"][k])
                if secret_key == "{{secret_key}}" or secret_key == "":
                    secret_key = os.urandom(12).hex()
                if url_secret_key == "{{url_secret_key}}" or secret_key == "":
                    url_secret_key = os.urandom(12).hex()
                cfg["API"]["secret_key"] = secret_key
                cfg["API"]["url_secret_key"] = url_secret_key

                if "DEVELOPMENT" in sections_api:
                    sections_api.pop(sections_api.index("DEVELOPMENT"))
                    v = ini_api["DEVELOPMENT"].get("remote_address", None)
                    if v is None:
                        cfg["API"]["remote_address_on_development"] = \
                            project_config_sample["API"]["remote_address_on_development"]
                    else:
                        cfg["API"]["remote_address_on_development"] = v

                    v = ini_api["DEVELOPMENT"].get("websocket_address", None)
                    if v is None:
                        cfg["API"]["websocket_address_on_development"] = \
                            project_config_sample["API"]["websocket_address_on_development"]
                    else:
                        cfg["API"]["websocket_address_on_development"] = v

                else:
                    ini_api["DEVELOPMENT"] = {}
                    cfg["API"]["remote_address_on_development"] = \
                        project_config_sample["API"]["remote_address_on_development"]
                    cfg["API"]["websocket_address_on_development"] = \
                        project_config_sample["API"]["websocket_address_on_development"]
                ini_api["DEVELOPMENT"]["remote_address"] = cfg["API"]["remote_address_on_development"]
                ini_api["DEVELOPMENT"]["websocket_address"] = cfg["API"]["websocket_address_on_development"]

                if "PRODUCTION" in sections_api:
                    sections_api.pop(sections_api.index("PRODUCTION"))
                    v = ini_api["PRODUCTION"].get("remote_address", None)
                    if v is None:
                        cfg["API"]["remote_address_on_production"] = \
                            project_config_sample["API"]["remote_address_on_production"]
                    else:
                        cfg["API"]["remote_address_on_production"] = v

                    v = ini_api["PRODUCTION"].get("websocket_address", None)
                    if v is None:
                        cfg["API"]["websocket_address_on_production"] = \
                            project_config_sample["API"]["websocket_address_on_production"]
                    else:
                        cfg["API"]["websocket_address_on_production"] = v

                else:
                    ini_api["PRODUCTION"] = {}
                    cfg["API"]["remote_address_on_production"] = \
                        project_config_sample["API"]["remote_address_on_production"]
                    cfg["API"]["websocket_address_on_production"] = \
                        project_config_sample["API"]["websocket_address_on_production"]
                ini_api["PRODUCTION"]["remote_address"] = cfg["API"]["remote_address_on_production"]
                ini_api["PRODUCTION"]["websocket_address"] = cfg["API"]["websocket_address_on_production"]

                with open(join(cfg["PROJECT"]["path"], 'api', 'api.ini'), 'w', encoding="utf-8") as configfile:
                    ini_api.write(configfile)

                current_port = cfg["API"]["port"]
                ports = set([cfg["API"]["port"]])
                for a in glob(join(cfg["PROJECT"]["path"], "apps", "*")):
                    if isdir(a) and isfile(join(a, "app.ini")):
                        app_name = basename(a)
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
                                        cfg["APPS"][app_name][k] = project_config_sample["APPS"]["app_01"][k]
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
                            cfg["APPS"][app_name] = project_config_sample["APPS"]["app_01"]
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

                required_on_ini = [
                    "server",
                    "username",
                    "default_sender",
                    "password",
                    "port",
                    "use_tls",
                    "use_ssl"
                ]
                if "EMAIL" in sections_project:
                    sections_project.pop(sections_project.index("EMAIL"))
                    for k in required_on_ini:
                        if k == "use_tls" or k == "use_ssl":
                            cfg["EMAIL"][k] = ini_project["EMAIL"].getboolean(
                                k, project_config_sample["EMAIL"][k])
                        elif ini_project["EMAIL"].get(k).isdigit():
                            cfg["EMAIL"][k] = int(ini_project["EMAIL"].get(k))
                        else:
                            cfg["EMAIL"][k] = ini_project["EMAIL"].get(
                                k, project_config_sample["EMAIL"][k])
                else:
                    ini_project["EMAIL"] = {}
                    cfg["EMAIL"] = project_config_sample["EMAIL"]
                for k in required_on_ini:
                    ini_project["EMAIL"][k] = str(cfg["EMAIL"][k])

                required_on_ini = [
                    "copyright",
                    "link_to_your_site"
                ]
                if "CONTENT_EMAILS" in sections_project:
                    sections_project.pop(sections_project.index("CONTENT_EMAILS"))
                    for k in required_on_ini:
                        cfg["CONTENT_EMAILS"][k] = ini_project["CONTENT_EMAILS"].get(
                            k, project_config_sample["CONTENT_EMAILS"][k])
                else:
                    ini_project["CONTENT_EMAILS"] = {}
                    cfg["CONTENT_EMAILS"] = project_config_sample["CONTENT_EMAILS"]
                for k in required_on_ini:
                    ini_project["CONTENT_EMAILS"][k] = str(cfg["CONTENT_EMAILS"][k])
                with open(join(cfg["PROJECT"]["path"], 'project.ini'), 'w', encoding="utf-8") as configfile:
                    ini_project.write(configfile)
                exclude = []
                if "SOCIAL_LOGIN" in sections_project:
                    d = dict(ini_project["SOCIAL_LOGIN"])
                    for k in d:
                        check_has_key = d[k]
                        if check_has_key in sections_project:
                            d[k] = dict(ini_project[check_has_key])
                            exclude.append(check_has_key)
                        else:
                            d[k] = None
                    cfg["SOCIAL_LOGIN"] = d
                for p in sections_project:
                    if p not in ["PROJECT", "EMAIL", "CONTENT_EMAILS", "SOCIAL_LOGIN", *exclude]:
                        cfg[p] = self._dict_value(dict(ini_project[p]))

            else:
                raise TypeError(
                    "The config file has incorrect content, expected dict type. Given: {0}".format(type(cfg)))

            self._config = cfg
            self._file = value
        else:
            raise IOError("The config file is invalid!. Given: {0}".format(value))

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
        return self._config

    def save(self):
        t = self.file
        with open(t, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=True, indent=4)

    def __iter__(self):
        for c in self.config:
            yield c

    def __getitem__(self, i):
        return self.config[i]

    def __setitem__(self, i, v):
        self.config[i] = v
        self.save()

    def get(self, k, default=None):
        return self.config.get(k, default)
