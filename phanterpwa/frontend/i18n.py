from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')
window = jQuery = console = document = localStorage = URL =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0
__pragma__('noskip')


__pragma__('kwargs')


class I18NServer():
    def __init__(self):
        self.storage = self.load_storage()
        self.userLang = self.get_user_lang()
        self._get_translations_on_server()

    @staticmethod
    def load_storage(self):
        result = window.PhanterPWA.CONFIG['I18N']
        return result

    def save_storage(self):
        window.PhanterPWA.CONFIG['I18N'] = self.storage

    def set_default_user_lang(self, lang):
        self.storage["default_lang"] = lang
        self.save_storage()

    @staticmethod
    def get_user_lang():
        userLang = navigator.language or navigator.userLanguage
        storage = I18NServer.load_storage()
        if "default_lang" in storage and storage['default_lang'] is not None:
            userLang = storage["default_lang"]
        return userLang

    def after_get_translations(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            default_lang = self.storage["default_lang"]
            self.storage = json
            if default_lang is None or default_lang is js_undefined:
                self.storage["default_lang"] = default_lang
            self.save_storage()

    def _get_translations_on_server(self, new_word=None):
        if window.PhanterPWA is not js_undefined:
            if window.PhanterPWA.DEBUG and self.userLang is not None:
                window.PhanterPWA.ApiServer.GET(**{
                    'url_args': ["api", "i18n", window.PhanterPWA.get_app_name()],
                    'url_vars': {
                        "lang": self.userLang,
                        "new_word": new_word
                    },
                    'onComplete': self.after_get_translations
                })

    def get_translations(self):
        if window.PhanterPWA is not js_undefined and self.userLang is not None:
            window.PhanterPWA.ApiServer.GET(**{
                'url_args': ["api", "i18n", window.PhanterPWA.get_app_name()],
                'url_vars': {
                    "lang": self.userLang
                },
                'onComplete': self.after_get_translations
            })

    def translate(self, wordkey):
        if self.userLang in self.storage:
            if wordkey in self.storage[self.userLang]:
                return self.storage[self.userLang][wordkey]
        self._get_translations_on_server(wordkey)
        return wordkey

    def DOMTranslate(self, target):
        self.target = jQuery(target)

        def eachElement(el):
            t_elem = jQuery(el)
            sanitize = t_elem.attr("phanterpwa-i18n-sanitize")
            word = t_elem.attr("phanterpwa-i18n")
            if word is not None and word is not js_undefined:
                if t_elem[0].hasAttribute(self.userLang):
                    if sanitize is not None and sanitize is not js_undefined and str(sanitize).upper() == "FALSE":
                        t_elem.html(t_elem.attr(self.userLang))
                    else:
                        t_elem.text(t_elem.attr(self.userLang))
                else:
                    translate = self.translate(word)
                    t_elem.attr(self.userLang, translate)
                    if sanitize is not None and sanitize is not js_undefined and str(sanitize).upper() == "FALSE":
                        t_elem.html(translate)
                    else:
                        t_elem.text(translate)

        if self.target[0] is not js_undefined:
            self.target.find("span[phanterpwa-i18n]").each(lambda: eachElement(this))
        return self.target


__pragma__('nokwargs')
