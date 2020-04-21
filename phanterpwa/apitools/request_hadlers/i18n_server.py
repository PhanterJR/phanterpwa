
from tornado import (
    web
)
# from core import (
#     projectConfig,
#     Translator,
# )
from phanterpwa.i18n import browser_language


class I18N(web.RequestHandler):
    def initialize(self, projectConfig, DALDatabase, i18nTranslator=None, logger_api=None):
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
                "phanterpwa-authorization,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = str(self.request.remote_ip)

    def check_origin(self, origin):
        return True

    def options(self, *args):
        self.set_status(200)
        return self.write({"status": "OK"})

    def get(self, *args):
        app = args[0]
        translator_instance = self.i18nTranslator.get_instance("{0}-{1}".format(self.projectConfig["PROJECT"]["name"], app))
        if translator_instance:
            translator_instance.direct_translation = self.phanterpwa_language
            if self.projectConfig["PROJECT"]["debug"]:
                T = translator_instance.T
                dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
                word = dict_arguments.get("new_word")
                lang = dict_arguments.get("lang")
                if word and lang:
                    translator_instance.translator(word, lang)
                return self.write(translator_instance.languages)
            else:
                return self.set_status(503)
        else:
            return self.set_status(404)
