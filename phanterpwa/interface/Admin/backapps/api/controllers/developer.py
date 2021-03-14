import os
import sys
import appdirs
import urllib.request
import base64
import json
import unittest
import phanterpwa
from phanterpwa.backend.decorators import (
    check_application
)
from phanterpwa import __install_requeriments__ as requeriments
from phanterpwa.configer import ProjectConfig
from phanterpwa.server import ProjectRunner
from phanterpwa.compiler import Compiler
from phanterpwa.tools import (
    humanize_seconds,
    temporary_password,
    config,
    interpolate,
    check_requeriments,
    interpolate,
)
from interface.admin_tk import ProjectsFolderTk
from phanterpwa.i18n import browser_language
from phanterpwa.third_parties.xss import xssescape as E
from tornado import (
    web,
    websocket
)
from pydal import Field
from pydal.validators import (
    IS_EQUAL_TO,
    IS_EMAIL
)
from datetime import (
    datetime,
    timedelta
)
from phanterpwa.tests.tests import test_list
from phanterpwa.tests import (
    test_cli,
    test_components_preloaders,
    test_helpers,
    test_i18n,
    test_reversexml,
    test_tools,
    test_configer
)
from phanterpwa.interface.cli import Projects as ProjectsList
ENV_PYTHON = os.path.normpath(sys.executable)
ENV_PATH = os.path.normpath(os.path.dirname(ENV_PYTHON))
PY_VERSION = "{0}.{1}.{2}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])

import re


class Projects(web.RequestHandler):
    """
        url: 'api/projects/<?command>'
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
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = str(self.request.remote_ip)
        self._projectdata_dir = os.path.join(appdirs.user_data_dir(), "phanterpwa")
        self._projectdata_dir_gui = os.path.join(self._projectdata_dir, "gui")
        if not os.path.isdir(self._projectdata_dir):
            os.makedirs(self._projectdata_dir, exist_ok=True)
        if not os.path.isdir(self._projectdata_dir_gui):
            os.makedirs(self._projectdata_dir_gui, exist_ok=True)
        self._projects_path = None

    def check_origin(self, origin):
        return True

    @check_application()
    def get(self, *args, **kargs):
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        self.interfaceConfig = config(self._projectdata_dir_gui)
        if "authorization" in self.interfaceConfig:
            authorization = self.interfaceConfig["authorization"]
        else:
            authorization = os.urandom(12).hex()
            self.interfaceConfig = config(self._projectdata_dir_gui, {"authorization": authorization})
        enviroment = {
            "python_executable": ENV_PYTHON,
            "python_path": ENV_PATH,
            "python_version": PY_VERSION,
            "phanterpwa_version": phanterpwa.__version__,
            "projects_folder": None
        }
        if args and args[0]:
            self._projects_path = self.interfaceConfig["projects_folder"]
            running = ProjectRunner()
            its_running = running.check(os.path.join(self._projects_path, args[0]))
            if os.path.isfile(os.path.join(self._projects_path, args[0], "config.json")):
                config_project = ProjectConfig(os.path.join(self._projects_path, args[0], "config.json"))
                msg = 'Project Found'
                self.set_status(200)
                return self.write({
                    "status": "OK",
                    "message": msg,
                    'i18n': {
                        "message": self.T(msg)
                    },
                    "config": config_project.config,
                    "running": its_running
                })
            else:
                msg = 'Project not Found'
                self.set_status(400)
                return self.write({
                    "status": "Bad Request",
                    "message": msg,
                    'i18n': {
                        "message": self.T(msg)
                    }
                })

        else:
            if "projects_folder" in self.interfaceConfig:
                self._projects_path = self.interfaceConfig["projects_folder"]
                self.Projects = ProjectsList(self._projects_path)
                msg = "Application list"
                enviroment['projects_folder'] = self._projects_path
                running = ProjectRunner()
                self.set_status(200)
                return self.write({
                    "status": "OK",
                    "message": msg,
                    'i18n': {
                        "message": self.T(msg)
                    },
                    "projects_list": [[x[0], x[1], "running" if x[1] in running.projects else
                        "stopped", ProjectConfig(
                            os.path.join(x[1], "config.json"))['PROJECT']['baseport']] for x in self.Projects.projects_list],
                    "authorization": authorization,
                    "enviroment": enviroment,
                })
            else:
                msg = "Get project list"
                self.set_status(202)
                self.write({
                    "status": "Accepted",
                    "message": msg,
                    "authorization": authorization,
                    "enviroment": enviroment,
                    'i18n': {
                        "message": self.T(msg)
                    }
                })

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})


class Configs(web.RequestHandler):
    """
        url: 'api/config/<?command>'
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
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = str(self.request.remote_ip)
        self._projectdata_dir = os.path.join(appdirs.user_data_dir(), "phanterpwa")
        self._projectdata_dir_gui = os.path.join(self._projectdata_dir, "gui")
        if not os.path.isdir(self._projectdata_dir):
            os.makedirs(self._projectdata_dir, exist_ok=True)
        if not os.path.isdir(self._projectdata_dir_gui):
            os.makedirs(self._projectdata_dir_gui, exist_ok=True)
        self._projects_path = None

    def check_origin(self, origin):
        return True

    @check_application()
    def get(self, *args, **kargs):
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        self.interfaceConfig = config(self._projectdata_dir_gui)
        if "authorization" in self.interfaceConfig:
            authorization = self.interfaceConfig["authorization"]
        else:
            authorization = os.urandom(12).hex()
            self.interfaceConfig = config(self._projectdata_dir_gui, {"authorization": authorization})
        enviroment = {
            "python_executable": ENV_PYTHON,
            "python_path": ENV_PATH,
            "python_version": PY_VERSION,
            "phanterpwa_version": phanterpwa.__version__,
            "projects_folder": None
        }
        if args and args[0]:
            self._projects_path = self.interfaceConfig["projects_folder"]
            running = ProjectRunner()
            its_running = running.check(os.path.join(self._projects_path, args[0]))
            if os.path.isfile(os.path.join(self._projects_path, args[0], "config.json")):
                config_project = ProjectConfig(os.path.join(self._projects_path, args[0], "config.json"))
                project_ini = config_project.project_ini
                api_ini = config_project.backend_ini
                secret_ini = config_project.frontend_secret_ini
                secret_ini_api = config_project.backend_secret_ini
                project_dict = {}
                api_dict = {}
                secret_dict = {}
                secret_dict_api = {'API': {}}
                for x in project_ini.sections():
                    if x not in project_dict:
                        project_dict[x] = {}

                    for k in project_ini.items(x):
                        v = k[1]
                        if v.isdigit():
                            project_dict[x][k[0]] = int(v)
                        elif v.lower() == "false":
                            project_dict[x][k[0]] = False
                        elif v.lower() == "true":
                            project_dict[x][k[0]] = True
                        else:
                            project_dict[x][k[0]] = v
                for x in api_ini.sections():
                    if x not in api_dict:
                        api_dict[x] = {}
                    for k in api_ini.items(x):
                        v = k[1]
                        if v.isdigit():
                            api_dict[x][k[0]] = int(v)
                        elif v.lower() == "false":
                            api_dict[x][k[0]] = False
                        elif v.lower() == "true":
                            api_dict[x][k[0]] = True
                        else:
                            api_dict[x][k[0]] = v
                for x in secret_ini.sections():
                    if x not in secret_dict:
                        secret_dict[x] = {}
                    for k in secret_ini.items(x):
                        v = k[1]
                        if v.isdigit():
                            secret_dict[x][k[0]] = int(v)
                        elif v.lower() == "false":
                            secret_dict[x][k[0]] = False
                        elif v.lower() == "true":
                            secret_dict[x][k[0]] = True
                        else:
                            secret_dict[x][k[0]] = v

                for k in secret_ini_api.items('API'):
                    v = k[1]
                    if v.isdigit():
                        secret_dict_api['API'][k[0]] = int(v)
                    elif v.lower() == "false":
                        secret_dict_api['API'][k[0]] = False
                    elif v.lower() == "true":
                        secret_dict_api['API'][k[0]] = True
                    else:
                        secret_dict_api['API'][k[0]] = v

                for y in secret_dict:
                    for a in secret_dict[y]:
                        if y not in project_dict:
                            project_dict[y] = {}
                        project_dict[y][a] = secret_dict[y][a]
                for y in secret_dict_api:
                    for a in secret_dict_api[y]:
                        if y not in api_dict:
                            api_dict[y] = {}
                        api_dict[y][a] = secret_dict_api[y][a]
                msg = 'Project Found'
                self.set_status(200)
                return self.write({
                    "status": "OK",
                    "message": msg,
                    'i18n': {
                        "message": self.T(msg)
                    },
                    "project_config": project_dict,
                    "api_config": api_dict,
                    "secret_config": secret_dict
                })
            else:
                msg = 'Project not Found'
                self.set_status(400)
                return self.write({
                    "status": "Bad Request",
                    "message": msg,
                    'i18n': {
                        "message": self.T(msg)
                    }
                })

        else:
            if "projects_folder" in self.interfaceConfig:
                self._projects_path = self.interfaceConfig["projects_folder"]
                self.Projects = ProjectsList(self._projects_path)
                msg = "Application list"
                enviroment['projects_folder'] = self._projects_path
                running = ProjectRunner()
                self.set_status(200)
                return self.write({
                    "status": "OK",
                    "message": msg,
                    'i18n': {
                        "message": self.T(msg)
                    },
                    "projects_list": [[x[0], x[1], "running" if x[1] in running.projects else
                        "stopped"] for x in self.Projects.projects_list],
                    "authorization": authorization,
                    "enviroment": enviroment,
                })
            else:
                msg = "Get project list"
                self.set_status(202)
                self.write({
                    "status": "Accepted",
                    "message": msg,
                    "authorization": authorization,
                    "enviroment": enviroment,
                    'i18n': {
                        "message": self.T(msg)
                    }
                })

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})


class Automation(web.RequestHandler):
    """
        url: 'api/projects/<?command>'
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
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = str(self.request.remote_ip)
        self._projectdata_dir = os.path.join(appdirs.user_data_dir(), "phanterpwa")
        self._projectdata_dir_gui = os.path.join(self._projectdata_dir, "gui")
        if not os.path.isdir(self._projectdata_dir):
            os.makedirs(self._projectdata_dir, exist_ok=True)
        if not os.path.isdir(self._projectdata_dir_gui):
            os.makedirs(self._projectdata_dir_gui, exist_ok=True)
        self._projects_path = None

    def check_origin(self, origin):
        return True

    @check_application()
    def get(self, *args, **kargs):
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        self.interfaceConfig = config(self._projectdata_dir_gui)
        if "authorization" in self.interfaceConfig:
            authorization = self.interfaceConfig["authorization"]
        else:
            authorization = os.urandom(12).hex()
            self.interfaceConfig = config(self._projectdata_dir_gui, {"authorization": authorization})
        if args[0] == "test_list":
            msg = 'Test List'
            self.set_status(200)
            return self.write({
                "status": "OK",
                "message": msg,
                "test_list": test_list,
                'i18n': {
                    "message": self.T(msg)
                }
            })
        elif args[0] == "requeriment_list":
            msg = 'Test Requeriments'
            self.set_status(200)
            return self.write({
                "status": "OK",
                "message": msg,
                "requeriment_list": requeriments,
                'i18n': {
                    "message": self.T(msg)
                }
            })

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})


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
        self._projectdata_dir = os.path.join(appdirs.user_data_dir(), "phanterpwa")
        self._projectdata_dir_gui = os.path.join(self._projectdata_dir, "gui")

    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket opened")
        self.write_message(u"______  _                    _               ______  _    _   ___  ")
        self.write_message(u"| ___ \| |                  | |              | ___ \| |  | | / _ \ ")
        self.write_message(u"| |_/ /| |__    __ _  _ __  | |_   ___  _ __ | |_/ /| |  | |/ /_\ \\")
        self.write_message(u"|  __/ | '_ \  / _` || '_ \ | __| / _ \| '__||  __/ | |/\| ||  _  |")
        self.write_message(u"| |    | | | || (_| || | | || |_ |  __/| |   | |    \  /\  /| | | |")
        self.write_message(u"\_|    |_| |_| \__,_||_| |_| \__| \___||_|   \_|     \/  \/ \_| |_/")
        self.interfaceConfig = config(self._projectdata_dir_gui)
        if "authorization" in self.interfaceConfig:
            self.admin_authorization = self.interfaceConfig["authorization"]
        else:
            self.admin_authorization = os.urandom(12).hex()
            self.interfaceConfig = config(self._projectdata_dir_gui, {"authorization": self.admin_authorization})
        self.connections.add(self)

    def on_message(self, message):
        if message.startswith("{"):
            msg = None
            try:
                json_message = json.loads(message)
            except Exception as e:
                return self.write_message(json.dumps({
                        "status": 400,
                        "error": "SyntaxError",
                        "message": "The message must be json type."
                }))
            else:
                cmd = json_message["command"]
                if "authorization" in json_message and json_message["authorization"] == self.admin_authorization and\
                        "command" in json_message:
                    if cmd == "change_project_folder":
                        current_path = self.interfaceConfig["projects_folder"]
                        ProjectsFolderTk()
                        self.interfaceConfig = config(self._projectdata_dir_gui)
                        if current_path == self.interfaceConfig["projects_folder"]:
                            return self.write_message(json.dumps({
                                "status": 202,
                                "message": "The path not changed.",
                                "command": cmd
                            }))
                        else:
                            return self.write_message(json.dumps({
                                "status": 200,
                                "message": "Changed.",
                                "command": cmd
                            }))
                    elif cmd == "requeriments_phanterpwa":
                        for x in check_requeriments():
                            self.write_message({
                                "status": 206,
                                "check": x[0],
                                "result": x[1],
                                "message": "Pip requeriment \"{0}\" checked".format(x[0]),
                                "command": cmd
                            })
                        self.write_message({
                            "status": 200,
                            "message": "Pip requeriment finished.",
                            "command": cmd
                        })
                    elif cmd == "test_phanterpwa":
                        suite = unittest.TestLoader().loadTestsFromModule(test_cli)
                        result = unittest.TextTestRunner(verbosity=2).run(suite)
                        test_exit_code = bool(int(not result.wasSuccessful()))
                        self.write_message({
                            "status": 206,
                            "test": "test_cli",
                            "result": test_exit_code,
                            "message": "Test cli",
                            "command": cmd
                        })
                        suite = unittest.TestLoader().loadTestsFromModule(test_components_preloaders)
                        result = unittest.TextTestRunner(verbosity=2).run(suite)
                        test_exit_code = bool(int(not result.wasSuccessful()))
                        self.write_message({
                            "status": 206,
                            "test": "test_components_preloaders",
                            "result": test_exit_code,
                            "message": "Test Proloaders",
                            "command": cmd
                        })
                        suite = unittest.TestLoader().loadTestsFromModule(test_helpers)
                        result = unittest.TextTestRunner(verbosity=2).run(suite)
                        test_exit_code = bool(int(not result.wasSuccessful()))
                        self.write_message({
                            "status": 206,
                            "test": "test_helpers",
                            "result": test_exit_code,
                            "message": "Test helpers",
                            "command": cmd
                        })
                        suite = unittest.TestLoader().loadTestsFromModule(test_i18n)
                        result = unittest.TextTestRunner(verbosity=2).run(suite)
                        test_exit_code = bool(int(not result.wasSuccessful()))
                        self.write_message({
                            "status": 206,
                            "test": "test_i18n",
                            "result": test_exit_code,
                            "message": "Test i18n",
                            "command": cmd
                        })
                        suite = unittest.TestLoader().loadTestsFromModule(test_reversexml)
                        result = unittest.TextTestRunner(verbosity=2).run(suite)
                        test_exit_code = bool(int(not result.wasSuccessful()))
                        self.write_message({
                            "status": 206,
                            "test": "test_reversexml",
                            "result": test_exit_code,
                            "message": "Test reversexml",
                            "command": cmd
                        })
                        suite = unittest.TestLoader().loadTestsFromModule(test_tools)
                        result = unittest.TextTestRunner(verbosity=2).run(suite)
                        test_exit_code = bool(int(not result.wasSuccessful()))
                        self.write_message({
                            "status": 206,
                            "test": "test_tools",
                            "result": test_exit_code,
                            "message": "Test tools",
                            "command": cmd
                        })
                        suite = unittest.TestLoader().loadTestsFromModule(test_configer)
                        result = unittest.TextTestRunner(verbosity=2).run(suite)
                        test_exit_code = bool(int(not result.wasSuccessful()))
                        self.write_message({
                            "status": 206,
                            "test": "test_configer",
                            "result": test_exit_code,
                            "message": "Test configer",
                            "command": cmd
                        })

                        self.write_message({
                            "status": 200,
                            "message": "Test Finished",
                            "command": cmd
                        })

                    elif cmd == "compile":
                        _project_path = json_message["project_path"]
                        _application = json_message["application"]
                        c = Compiler(_project_path)
                        has_error = False
                        for x in c.compile_by_step(_application):
                            if not x[1]:
                                has_error = True
                            self.write_message({
                                "status": 206,
                                "project_path": _project_path,
                                "message": x,
                                "command": cmd
                            })
                        return self.write_message({
                            "status": 200 if not has_error else 202,
                            "project_path": _project_path,
                            "message": "Compile complete!" if not has_error else "Has error(s) on compilation",
                            "command": cmd
                        })
                    elif cmd == "run" or cmd == "stop" or cmd == "check" or cmd == "stop_all" or cmd == "check_all":
                        _project_path = json_message["project_path"]
                        R = ProjectRunner()
                        if cmd == "run":
                            R.run(_project_path, thread=True, compile=True)
                        elif cmd == "stop":
                            R.stop(_project_path)

                        p = [x for x in R.projects.keys()]
                        if p:
                            r = {
                                'status': 200,
                                'message': 'Projects running',
                                'command': cmd,
                                'project_running': p
                            }

                            return self.write_message(json.dumps(r))
                        else:
                            return self.write_message({
                                'status': 202,
                                'message': 'All stopped!',
                                'command': cmd
                            })
                else:
                    return self.write_message(json.dumps({
                            "status": 401,
                            "error": "Unauthorized",
                            "message": "Authorization not found.",
                            "command": cmd
                    }))


    def on_close(self):
        self.connections.remove(self)
        print("WebSocket closed")
