import os
from tornado import (
    web
)
# from core import (
#     projectConfig,
#     Translator,
# )
from phanterpwa.i18n import (
    browser_language,
    Translator
)


class I18N(web.RequestHandler):
    def initialize(self, app_name, projectConfig):
        self.app_name = app_name
        self.projectConfig = projectConfig
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

    def check_origin(self, origin):
        return True

    def options(self, *args):
        self.set_status(200)
        return self.write({"status": "OK"})

    def get(self, *args):
        app = args[0]
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        lang = dict_arguments.get("lang", self.phanterpwa_language)
        word = dict_arguments.get("new_word", None)
        current_dir = self.projectConfig['PROJECT']['path']
        translator_instance = Translator(
            os.path.join(current_dir, "backapps", self.app_name, "languages", app),
            identifier=lang,
            debug=self.projectConfig['PROJECT']['debug']
        )

        if translator_instance:
            if word and lang:
                translator_instance.add_language(lang)
                translator_instance.direct_translation = lang
                translator_instance.translator(word, lang)
            if self.projectConfig["PROJECT"]["debug"]:
                return self.write(translator_instance.languages)
            else:
                return self.set_status(503)
        else:
            return self.set_status(404)
