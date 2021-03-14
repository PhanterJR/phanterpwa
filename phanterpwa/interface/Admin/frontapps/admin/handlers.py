import os
from urllib.parse import quote
from tornado import (
    web
)
from phanterpwa.configer import ProjectConfig
_current_dir = os.path.join(os.path.dirname(__file__))
folder_name = os.path.split(_current_dir)[-1]
projectConfig = ProjectConfig(os.path.normpath(os.path.join(_current_dir, "..", "..", "config.json")))
_targer_compiled_app = projectConfig["FRONTEND"][folder_name]['build_folder']
_version = projectConfig['PROJECT']['version']
_debug = projectConfig['PROJECT']['debug']


class AppMainPage(web.RequestHandler):
    def get(self):
        self.render(os.path.join(_targer_compiled_app, "{0}.html".format(
            projectConfig["FRONTEND"][folder_name]['views_main_file']
        )))


class AppPages(web.RequestHandler):
    def get(self, *args):
        self.render(os.path.join(_targer_compiled_app, args[0]))


SETTINGS = {
    'debug': _debug
}

HANDLER = [
    (r"/", AppMainPage),
    (r'/static/[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}/(.*\..*)', web.StaticFileHandler, {
        'path': os.path.join(_targer_compiled_app, "static", _version)
    }),
    (r"/([\w+\/\-]*?[\w+\-].html)", AppPages)
]
