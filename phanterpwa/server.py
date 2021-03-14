import os
import sys
import importlib
import subprocess
import threading
import psutil
from tornado import (
    web,
    ioloop,
    httpserver,
    autoreload
)
from phanterpwa import compiler
from phanterpwa import configer

CURRENT_DIR = os.path.join(os.path.dirname(__file__))


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

    @property
    def projects(self):
        self._projects()
        return self._projects_dict

    def run(self, project_path, compile=False, thread=False):
        if compile:
            from phanterpwa import compiler
            c = compiler.Compiler(project_path)
            c.compile()
        target = os.path.normpath(os.path.join(self.path_phanterpwa, "server.py {0}".format(project_path)))
        self.stop(project_path)
        command = " ".join([self.env_python, "-X utf8", target])
        print()
        print("=" * 79)
        print("Starting server..........")
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
