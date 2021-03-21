import os
import sys
import re
import importlib
import subprocess
import threading
import psutil
import phanterpwa
import configparser
from tornado import (
    web,
    ioloop,
    httpserver,
    autoreload
)
from phanterpwa.tools import config
from phanterpwa import compiler
from phanterpwa import configer

CURRENT_DIR = os.path.join(os.path.dirname(__file__))
PHANTERPWA_VERSION = phanterpwa.__version__

version_regex = re.compile(r"^[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}$")


class PhanterPWATornado(object):
    """docstring for PhanterPWATornado"""

    def __init__(self, projectPath):
        super(PhanterPWATornado, self).__init__()
        self.projectPath = projectPath
        self.projectConfig = configer.ProjectConfig(os.path.join(self.projectPath, "config.json"))
        self.apps_ports = []
        if self.projectConfig.get("FRONTEND") and \
            os.path.exists(os.path.join(self.projectConfig['PROJECT']['path'], "frontapps")):
            for x in self.projectConfig['FRONTEND']:
                current_port = self.projectConfig['FRONTEND'][x]['port']
                if current_port not in self.apps_ports:
                    self.apps_ports.append(current_port)
                else:
                    raise ValueError("The '{0}' frontend app port ({1}) is not valid".format(x, current_port))

        if self.projectConfig.get("BACKEND") and \
            os.path.exists(os.path.join(self.projectConfig['PROJECT']['path'], "backapps")):
            for x in self.projectConfig['BACKEND']:
                current_port = self.projectConfig['BACKEND'][x]['port']
                if current_port not in self.apps_ports:
                    self.apps_ports.append(current_port)
                else:
                    raise ValueError("The '{0}' backend app port ({1}) is not valid".format(x, current_port))

        self.debug = self.projectConfig["PROJECT"]["debug"]
        self.version = self.projectConfig["PROJECT"]["version"]
        self.oncli = False

    @property
    def oncli(self):
        return self._oncli

    @oncli.setter
    def oncli(self, oncli):
        if isinstance(oncli, bool):
            self._oncli = oncli
        else:
            raise "The oncli must be boolean. Given: {0}".format(type(oncli))

    def compile(self):
        c = compiler.Compiler(self.projectPath)
        c.compile()

    def run(self):
        sys.path.insert(0, self.projectPath)
        os.chdir(self.projectPath)
        print(self.projectPath)

        if self.apps_ports:
            for x in self.projectConfig['BACKEND']:
                current_port = self.projectConfig['BACKEND'][x]['port']
                handlers_app = importlib.import_module("backapps.{0}.handlers".format(x))
                if isinstance(handlers_app.HANDLER, (list, tuple)):
                    app = web.Application(
                        handlers_app.HANDLER,
                        **handlers_app.SETTINGS
                    )
                    app_http_server = httpserver.HTTPServer(app)
                    app_http_server.listen(int(current_port))
                else:
                    app = handlers_app.HANDLER
                    app_http_server = httpserver.HTTPServer(app)
                    app_http_server.listen(int(current_port))

            for x in self.projectConfig['FRONTEND']:
                current_port = self.projectConfig['FRONTEND'][x]['port']
                handlers_app = importlib.import_module("frontapps.{0}.handlers".format(x))
                if isinstance(handlers_app.HANDLER, (list, tuple)):
                    app = web.Application(
                        handlers_app.HANDLER,
                        **handlers_app.SETTINGS
                    )
                    app_http_server = httpserver.HTTPServer(app)
                    app_http_server.listen(int(current_port))
                else:
                    app = handlers_app.HANDLER
                    app_http_server = httpserver.HTTPServer(app)
                    app_http_server.listen(int(current_port))
        autoreload.watch(os.path.join(self.projectPath, "config.json"))
        ioloop.IOLoop.current().start()
        print("start stopped")
        ioloop.IOLoop.current().add_callback(lambda: ioloop.IOLoop.current().close(True))
        print("close? Don't know")

    def stop(self):
        ioloop.IOLoop.current().add_callback(
            lambda: (
                ioloop.IOLoop.current().stop()
            )
        )
        print("comando stop")


class ProjectRunner():
    def __init__(self):
        self.path_phanterpwa = CURRENT_DIR
        self.env_python = os.path.normpath(sys.executable)
        self._projects_dict = {}
        self._ini_project = configparser.ConfigParser()

    @property
    def projects(self):
        self._projects()
        return self._projects_dict

    def run(self, project_path, compile=False, thread=False):
        temp_dir = os.path.join(project_path, "temp")
        ppwa_version_file = os.path.join(project_path, "temp", 'ppwa_version')
        ppwa_version = None
        project_version = "0.0.1"

        if os.path.isfile(ppwa_version_file):
            with open(ppwa_version_file, 'r', encoding="utf-8") as f:
                ppwa_version = f.read()
        elif os.path.isdir(temp_dir):
            ppwa_version = PHANTERPWA_VERSION
            with open(ppwa_version_file, 'w', encoding="utf-8") as f:
                f.write(ppwa_version)            
        # majors_version = majors_version_cfg = "0.0"
        if os.path.isfile(os.path.join(project_path, 'project.ini')):
            self._ini_project.read(
                os.path.join(project_path, 'project.ini'), encoding='utf-8')
            project_version = self._ini_project["PROJECT"].get("version", "0.0.1")
            # if version_regex.match(project_version):
            #     majors_version = ".".join(project_version.split(".")[0:2])

        if os.path.isfile(os.path.join(project_path, "config.json")):
            cfg_ini = config(os.path.join(project_path, "config.json"))
        else:
            cfg_ini = configer.ProjectConfig(project_path)
        project_version_cfg = cfg_ini["PROJECT"]["version"]
        # project_version_cfg = cfg_ini["PROJECT"]["version"]
        # if version_regex.match(project_version_cfg):
        #     majors_version_cfg = ".".join(project_version_cfg.split(".")[0:2])
        reset_compilation = False
        cfg = configer.ProjectConfig(project_path)
        if str(project_version).strip() != str(project_version_cfg).strip():
            reset_compilation = True
        # if majors_version != majors_version_cfg:
        #     reset_compilation = True
        #     new_version = ".".join([majors_version, str(0)])
        # elif project_version_cfg != project_version:
        #     new_version = ".".join([majors_version, str(cfg_ini["PROJECT"]['compilation'])])
        # else:
        #     new_version = project_version
        #     if compile or str(ppwa_version).strip() != str(PHANTERPWA_VERSION).strip():
        #         new_version = ".".join([majors_version, str(cfg_ini["PROJECT"]['compilation'])])
        # with open(os.path.join(project_path, 'project.ini'), 'w', encoding="utf-8") as configfile:
        #     self._ini_project["PROJECT"]["version"] = new_version
        #     self._ini_project.write(configfile)            

        if compile:
            c = compiler.Compiler(project_path, reset_compilation=reset_compilation)
            c.compile()
        else:
            f_comp = False
            if str(project_version).strip() != str(project_version_cfg).strip():
                f_comp=True
                print("Project version change:", str(project_version_cfg).strip(), "-->", str(project_version).strip())
            if str(ppwa_version).strip() != str(PHANTERPWA_VERSION).strip():
                f_comp=True
                print("PhanterPWA version change:",
                    str(ppwa_version).strip(), "-->", str(PHANTERPWA_VERSION).strip())
            if f_comp:
                c = compiler.Compiler(project_path, reset_compilation=reset_compilation)
                c.compile()
   
        with open(ppwa_version_file, 'w', encoding="utf-8") as f:
            f.write(PHANTERPWA_VERSION)
        target = os.path.normpath(os.path.join(self.path_phanterpwa, "server.py {0}".format(project_path)))
        self.stop(project_path)
        command = " ".join([self.env_python, "-X utf8", target])
        print()
        print("=" * 79)
        print("Starting server..........")
        if cfg['BACKEND']:
            print('BACKEND')
            for a in cfg['BACKEND']:
                print(" ", a)
                print("    HOST:", cfg['BACKEND'][a]['host'])
                print("    PORT:", cfg['BACKEND'][a]['port'])

        print()
        if cfg['FRONTEND']:
            print('FRONTEND')
            for a in cfg['FRONTEND']:
                print(" ", a)
                print("    HOST:", cfg['FRONTEND'][a]['host'])
                print("    PORT:", cfg['FRONTEND'][a]['port'])
        print()
        with open(os.path.join(self.path_phanterpwa, "samples", "art"), "r") as f:
            print(f.read())
        print()
        print("=" * 79)
        if thread:
            t = threading.Thread(target=lambda: subprocess.call(command, cwd=project_path, shell=True))
            t.start()
            return t
        else:
            try:
                subprocess.call(command, cwd=project_path, shell=True)
            except KeyboardInterrupt:
                self.stop(project_path)

    def stop_all(self):
        all_p = self.projects
        for p in all_p:
            for x in all_p[p]:
                x.terminate()

    def stop(self, project_path):
        has_running = False
        for x in self._project(project_path):
            has_running = True
            x.terminate()
        self._projects()
        if has_running:
            print("=" * 79)
            print("Stoping server....")
            cfg = configer.ProjectConfig(project_path)
            if cfg['BACKEND']:
                print('BACKEND')
                for a in cfg['BACKEND']:
                    print(" ", a)
                    print("    HOST:", cfg['BACKEND'][a]['host'])
                    print("    PORT:", cfg['BACKEND'][a]['port'])
            print()
            if cfg['FRONTEND']:
                print('FRONTEND')
                for a in cfg['FRONTEND']:
                    print(" ", a)
                    print("    HOST:", cfg['FRONTEND'][a]['host'])
                    print("    PORT:", cfg['FRONTEND'][a]['port'])
            print()
            print("Goodbye!")

    def check(self, project_path):
        self._projects()
        if project_path in self._projects_dict:
            return True
        else:
            return False

    def _project(self, project_path):
        self._projects()
        if project_path in self._projects_dict:
            return self._projects_dict[project_path]
        else:
            return []

    def _projects(self):
        target = os.path.normpath(os.path.join(self.path_phanterpwa, "server.py"))
        self._projects_dict = {}
        for p in psutil.process_iter():
            cmd_line = None
            try:
                cmd_line = p.cmdline()
            except Exception:
                pass
            if cmd_line:
                if self.env_python == cmd_line[0]:
                    if len(cmd_line) > 1 and target in cmd_line:
                        if cmd_line[-1] in self._projects_dict:
                            self._projects_dict[cmd_line[-1]].append(p)
                        else:
                            self._projects_dict[cmd_line[-1]] = [p]


if __name__ == "__main__":
    import os
    projectPath = os.getcwd()
    AppRunv = PhanterPWATornado(projectPath)
    try:
        AppRunv.run()
    except KeyboardInterrupt:
        AppRunv.stop()
