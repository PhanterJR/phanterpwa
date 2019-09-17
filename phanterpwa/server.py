import os
import sys
import importlib
from phanterpwa.tools import (
    config,
    url_pattern_relative_paths,
    interpolate,
    compiler
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
        self.api_port = self.projectConfig['API']["port"]
        self.apps_ports = []
        if self.projectConfig.get("APPS") and \
            os.path.exists(os.path.join(self.projectConfig['PROJECT']['path'], "apps")):
            for x in self.projectConfig['APPS']:
                current_port = self.projectConfig['APPS'][x]['port']
                if current_port not in self.apps_ports and current_port != self.api_port:
                    self.apps_ports.append(current_port)
                else:
                    raise ValueError("The '{0}' app port ({1}) is not valid".format(x, current_port))

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
        handlers_api = importlib.import_module("api.handlers")
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

        if self.apps_ports:
            for x in self.projectConfig['APPS']:
                current_port = self.projectConfig['APPS'][x]['port']
                handlers_app = importlib.import_module("apps.{0}.handlers".format(x))
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
    AppRunv = PhanterPWATornado(projectPath)
    try:
        AppRunv.run()
    except KeyboardInterrupt:
        AppRunv.stop()
