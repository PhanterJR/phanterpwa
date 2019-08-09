import os
import sys
import importlib
from phanterpwa.app_compiler import (
    compiler
)
from phanterpwa.tools import (
    config,
    url_pattern_relative_paths,
    interpolate
)
from tornado import (
    web,
    ioloop,
    httpserver
)


CURRENT_DIR = os.path.join(os.path.dirname(__file__))


class PhanterPWATornado(object):
    """docstring for PhanterPWATornado"""

    def __init__(self, projectPath):
        super(PhanterPWATornado, self).__init__()
        self.projectPath = projectPath
        self.projectConfig = config(os.path.join(self.projectPath, "config.json"))
        self.api_port = self.projectConfig['API_SERVER']["port"]
        self.app_port = self.projectConfig['APP_SERVER']["port"]
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
        compiler(self.projectPath)

    def run(self):
        if self.oncli:
            with open(os.path.join(CURRENT_DIR, "samples", "art_cli"), "r") as f:
                print(f.read())
        else:
            with open(os.path.join(CURRENT_DIR, "samples", "art"), "r") as f:
                print(f.read())
        sys.path.append(self.projectPath)
        os.chdir(self.projectPath)
        handlers_app = importlib.import_module("app.handlers")
        handlers_api = importlib.import_module("api.handlers")
        if all([isinstance(handlers_api.HANDLER, (list, tuple)),
            isinstance(handlers_app.HANDLER, (list, tuple)),
            self.api_port == self.app_port]):

            print("".join(["The APP and API are running on the same port, so the urls",
                " will start (will be added) by '/app' and '/api' respectively."]))
            new_handler = []
            for a in handlers_app.HANDLER:
                t = list(a)
                n = "".join([r"/app", t[0]])
                t[0] = n
                new_handler.append(tuple(t))
            for a in handlers_api.HANDLER:
                t = list(a)
                n = "".join([r"/api", t[0]])
                t[0] = n
                new_handler.append(tuple(t))

            new_setting = {}
            for s in handlers_app.SETTINGS:
                new_setting[s] = handlers_app.SETTINGS[s]
            for s in handlers_api.SETTINGS:
                new_setting[s] = handlers_api.SETTINGS[s]
            app = web.Application(
                new_handler,
                **new_setting
            )
        else:
            if isinstance(handlers_app.HANDLER, (list, tuple)):
                app = web.Application(
                    handlers_app.HANDLER,
                    **handlers_app.SETTINGS
                )
                app_http_server = httpserver.HTTPServer(app)
                app_http_server.listen(int(self.app_port))
            else:
                app = handlers_app.HANDLER
                app_http_server = httpserver.HTTPServer(app)
                app_http_server.listen(int(self.app_port))

            if isinstance(handlers_api.HANDLER, (list, tuple)):
                api = web.Application(
                    handlers_api.HANDLER,
                    **handlers_api.SETTINGS
                )
                api_http_server = httpserver.HTTPServer(api)
                api_http_server.listen(int(self.api_port))
            else:
                api = handlers_api.HANDLER
                api_http_server = httpserver.HTTPServer(api)
                api_http_server.listen(int(self.api_port))
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


if __name__ == "__main__":
    import os
    projectPath = os.getcwd()
    print(projectPath)
    AppRunv = PhanterPWATornado(projectPath)
    try:
        AppRunv.run()
    except KeyboardInterrupt:
        AppRunv.stop()
