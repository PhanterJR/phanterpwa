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
        self.get_translations_on_server()

    @staticmethod
    def load_storage(self):
        result = dict(default_lang=None)
        t = localStorage.getItem("phanterpwa_i18n")
        if t is not None and t is not js_undefined:
            try:
                t = JSON.parse(t)
                result = t
            except Exception:
                localStorage.removeItem("phanterpwa_i18n")
                console.error("the phanterpwa_i18n is corrupted")
        else:
            localStorage.setItem("phanterpwa_i18n", JSON.stringify(window.PhanterPWA.CONFIG['I18N']))
            result = window.PhanterPWA.CONFIG['I18N']
        return result

    def save_storage(self):
        localStorage.setItem("phanterpwa_i18n", JSON.stringify(self.storage))

    def set_default_user_lang(self, lang):
        self.storage["default_lang"] = lang
        self.save_storage()

    @staticmethod
    def get_user_lang():
        userLang = navigator.language or navigator.userLanguage
        storage = I18NServer.load_storage()["default_lang"]
        if "default_lang" in storage:
            userLang = storage["default_lang"]
        return userLang

    def after_get_translations(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            default_lang = self.storage["default_lang"]
            self.storage = json
            if default_lang is None or default_lang is js_undefined:
                self.storage["default_lang"] = default_lang
            self.save_storage(self)

    def get_translations_on_server(self, new_word=None):
        if window.PhanterPWA is not js_undefined:
            if window.PhanterPWA.DEBUG:
                window.PhanterPWA.ApiServer.GET(**{
                    'url_args': ["api", "i18n"],
                    'url_vars': {
                        "lang": self.userLang,
                        "new_word": new_word
                    },
                    'onComplete': self.after_get_translations
                })

    def translate(self, wordkey):
        if self.userLang in self.storage:
            if wordkey in self.storage[self.userLang]:
                return self.storage[self.userLang][wordkey]
        self.get_translations_on_server(wordkey)
        return wordkey

    def DOMTranslate(self, target):
        self.target = jQuery(target)

        def eachElement(el):
            t_elem = jQuery(el)
            word = t_elem.attr("phanterpwa-i18n")
            if word is not None and word is not js_undefined:
                if t_elem[0].hasAttribute(self.userLang):
                    t_elem.text(t_elem.attr(self.userLang))
                else:
                    translate = self.translate(word)
                    t_elem.attr(self.userLang, translate)
                    t_elem.text(translate)

        if self.target[0] is not js_undefined:
            self.target.find("span[phanterpwa-i18n]").each(lambda: eachElement(this))
        return self.target


__pragma__('nokwargs')
