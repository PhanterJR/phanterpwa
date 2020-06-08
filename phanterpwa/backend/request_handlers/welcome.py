import re
import json
from tornado import (
    web
)


class Welcome(web.RequestHandler):
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

    def get(self):
        self.write({
            "status": "OK",
            "message": "Hello World!",
            "project": self.projectConfig["PROJECT"]
        })
