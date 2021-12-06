import phanterpwa.frontend.server as server
import phanterpwa.frontend.progressbar as progressbar
import phanterpwa.frontend.i18n as i18n
import phanterpwa.frontend.helpers as helpers
import phanterpwa.frontend.components.widgets as widgets
import phanterpwa.frontend.components.events as events
import phanterpwa.frontend.gatehandler as gatehandler
import phanterpwa.frontend.components.modal as modal
import phanterpwa.frontend.websocket as websocket
import phanterpwa.frontend.validations as validations
from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = URL = M = FormData = setTimeout = RegExp = caches =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = __except0__ = Date = 0

__pragma__('noskip')


__pragma__('kwargs')


DIV = helpers.XmlConstructor.tagger("div")
H2 = helpers.XmlConstructor.tagger("h2")
XML = helpers.XML
TEXTAREA = helpers.XmlConstructor.tagger("textarea")
I = helpers.XmlConstructor.tagger("i")


class PhanterPWA():
    def __init__(self, config, gates, **parameters):

        self.get_inicial_config_uri()
        self.initialize()
        self._thewidgets = dict()
        if config is js_undefined or config is None:
            raise ValueError("The config is required")
        if gates is js_undefined or gates is None:
            raise ValueError("The gates is required")
        self.CONFIG = config
        self.NAME = config.PROJECT.name
        self.TITLE = config.PROJECT.title
        self.VERSION = config.PROJECT.version
        self.VERSIONING = config.PROJECT.versioning
        self.COMPILATION = config.PROJECT.compilation
        self.AUTHOR = config.PROJECT.author
        self.DEBUG = config.PROJECT.debug
        self.Gates = dict(gates)
        self.ProgressBar = progressbar.ProgressBar("#main-progress-bar-container")
        self.Request = WayRequest()
        self.Components = {}
        self.Events = {}
        self.Cache = {}
        self.Response = None
        self.default_way = parameters.get("default_way", "home")
        self._after_open_way = parameters.get("after_open_way", None)
        self._after_login = parameters.get("after_login", None)
        self._after_logout = parameters.get("after_logout", None)
        self._send_global_error = parameters.get("send_global_error", False)
        self.counter = 0
        self.states = dict()
        self._social_login_icons = {
            "google": I(_class="fab fa-google"),
            "facebook": I(_class="fab fa-facebook"),
            "twitter": I(_class="fab fa-twitter")
        }

        # jQuery(document).ajaxComplete(
        #     lambda event, xhr, options: self._after_ajax_complete(event, xhr, options)
        # )
        window.PhanterPWA = self
        test_bool = __pragma__("js", "{}", "'serviceWorker' in navigator")
        if test_bool:
            caches.js_keys().then(lambda names: self._clear_cache(names))
            navigator.serviceWorker.register(
                '/sw.js', {'scope': '/'}
            ).then(
                lambda reg: self._swregister(reg, "register")
            ).catch(
                lambda error: console.error('Registration failed with {0}'.format(error))
            )

        window.onpopstate = self._onPopState
        self._onPopState()

        if self.DEBUG:
            console.info("starting {0} application (version: {1}, compilation: {2})".format(
                self.CONFIG.PROJECT.title, self.CONFIG.PROJECT.version, self.CONFIG.PROJECT.compilation)
            )
        self.add_event(events.Waves())
        # self.add_event(events.WidgetsInput())
        self.add_event(events.WayHiperlinks())
        self.ApiServer = server.ApiServer()
        self.ApiServer.getClientToken()
        self.I18N = i18n.I18NServer()
        self.I18N.get_translations()
        self.WS = websocket.WebSocketPhanterPWA(self.CONFIG["APP"]["websocket_address"])
        if self.DEBUG:
            self.add_component(Developer_Toolbar())
        self.Valider = validations.Valid

        window.onerror = self.onGlobalError

    def _clear_cache(self, names):
        for x in names:
            if x != self.versioning:
                if window.PhanterPWA.DEBUG:
                    console.info("cache {0} deleted".format(x))
                caches.delete(x)
            else:
                if window.PhanterPWA.DEBUG:
                    console.info("current cache:", x)

    def _swregister(self, reg):
        if window.PhanterPWA.DEBUG:
            if reg.installing:
                console.info('Service worker installing')
            elif reg.waiting:
                console.info('Service worker installed')
            elif reg.active:
                console.info('Service worker active')

    def onGlobalError(self, message, source, lineno, colno, error):
        if self._send_global_error and self.ApiServer is not js_undefined:

            formdata = __new__(FormData())
            auth_user = window.PhanterPWA.get_auth_user()
            if auth_user is not js_undefined and auth_user is not None:
                formdata.append("email_user", auth_user.email)
            formdata.append("current_way", self.get_current_way())           
            formdata.append("message", message)
            formdata.append("source", source)
            formdata.append("lineno", lineno)
            formdata.append("colno", colno)
            formdata.append("error", JSON.stringify(error))

            self.POST(
                "api",
                "error",
                form_data=formdata
            )

    @staticmethod
    def check_event_namespace(el, event_name, namespace):
        element = jQuery(el)
        if element.length > 0:
            if element.length == 1:
                obj_events = jQuery._data(element[0], 'events')
                if obj_events is not js_undefined:
                    event_list = obj_events[event_name]
                    if isinstance(event_list, list):
                        for x in event_list:
                            ns = x.namespace
                            if ns is not js_undefined and ns == namespace:
                                return True
            else:
                console.error("check_event_namespace must be used in jquery selectors with",
                    "an element like when using the id selector")
        return False

    @staticmethod
    def ibind(el, event_name, namespace, callback):
        if not window.PhanterPWA.check_event_namespace(el, event_name, namespace) and callable(callback):
            ns = "{0}.{1}".format(event_name, namespace)
            jQuery(el).off(ns).on(ns, lambda event: callback(this, event))

    def get_inicial_config_uri(self):
        initial_config = __new__(URL(window.location.href))
        params = initial_config.searchParams
        authorization = params.js_get("authorization")
        client_token = params.js_get("client_token")
        url_token = params.js_get("url_token")
        auth_user = params.js_get("auth_user")
        redirect = params.js_get("redirect")
        way = params.js_get('way')
        if auth_user is not None and auth_user is not js_undefined:
            auth_user = JSON.parse(auth_user)

        if (authorization is not None) and (url_token is not None) and\
                (auth_user is not None) and (client_token is not None):
            localStorage.setItem('phanterpwa-client-token', client_token)
            localStorage.setItem('phanterpwa-url-token', url_token)
            if auth_user["remember_me"] is True:
                localStorage.setItem("phanterpwa-authorization", authorization)
                localStorage.setItem("auth_user", JSON.stringify(auth_user))
                sessionStorage.removeItem("phanterpwa-authorization")
                sessionStorage.removeItem("auth_user")
            else:
                sessionStorage.setItem("phanterpwa-authorization", authorization)
                sessionStorage.setItem("auth_user", JSON.stringify(auth_user))
                localStorage.removeItem("phanterpwa-authorization")
                localStorage.removeItem("auth_user")
            window.PhanterPWA.set_last_auth_user(auth_user)
        if redirect is not None and redirect is not js_undefined:
            window.location = redirect
        if way is not None and way is not js_undefined:
            self.open_way(way)

    def _after_ajax_complete(self, event, xhr, option):
        if option is not js_undefined:
            p_url = self.parse_url(option.url)
            self.reload_components(ajax=p_url)
            self.reload_events(ajax=p_url)

    def get_id(self, salt="phanterpwa"):
        self.counter += 1
        timestamp = __new__(Date().getTime())
        if salt is None or salt is js_undefined:
            console.error("The salt of method get_id is invalid! given:", salt)
            salt = "phanterpwa"
        return "{0}-{1}-{2}".format(salt, self.counter, timestamp)

    def get_widget(self, widget_identifier):
        return self.Request.widgets.get(widget_identifier, None)

    def social_login_list(self):
        social_logins = window.PhanterPWA["CONFIG"]["SOCIAL_LOGINS"]
        if social_logins is not None and social_logins is not js_undefined:
            list_login = social_logins.keys()
            l = []
            for x in list_login:
                if x in self._social_login_icons:
                    l.append([x, self._social_login_icons[x]])
                else:
                    l.append([x, I(_class="fas fa-at")])
            return l

    def _xway(self, *args, **kargs):
        all_args = self.ApiServer._process_args(args)
        url_vars = self.ApiServer._process_parameters(kargs)
        all_vars = self.ApiServer._serialize_vars(url_vars)
        current_uri = "{0}{1}".format(all_args, all_vars)
        return current_uri

    def XWAY(self, *args, **kargs):
        current_uri = "/#_phanterpwa:/{0}".format(self._xway(*args, **kargs))
        return current_uri

    @staticmethod
    def get_app_name(self):
        return window.PhanterPWA.CONFIG["APP"]["name"]

    @staticmethod
    def get_api_address(self):
        return window.PhanterPWA.CONFIG["APP"]["http_address"]

    @staticmethod
    def flash(msg=None, **parameters):
        timeout = parameters.get("timeout", 3000)
        timestamp = __new__(Date().getTime())
        msg_id = "phanterpwa-flash-wrapper-{0}".format(timestamp)
        target = jQuery("#phanterpwa-flash-container")
        if target.length == 0:
            jQuery("body").prepend(DIV(_id="phanterpwa-flash-container").jquery())

        def remove_msg():
            jQuery("#{0}".format(msg_id)).removeClass("enabled").slideUp(500)
            setTimeout(lambda: jQuery("#{0}".format(msg_id)).remove(), 2000)
        if "html" in parameters:
            msg = parameters.get("html", None)
            if msg is not None:
                html = DIV(
                    XML(msg),
                    _id=msg_id,
                    _class="phanterpwa-flash-wrapper enabled",
                    _style="opacity: 0; margin-top:-20px"
                )
                html.append_to("#phanterpwa-flash-container")
                jQuery("#{0}".format(msg_id)).addClass("enabled").animate({'opacity': 1, 'margin-top': '0px'})
                setTimeout(remove_msg, timeout)
        elif msg is not None and msg is not js_undefined:
            html = DIV(
                msg,
                _id=msg_id,
                _class="phanterpwa-flash-wrapper",
                _style="opacity: 0; margin-top:-20px"
            )
            html.append_to("#phanterpwa-flash-container").find(
                "#{0}".format(msg_id)).addClass("enabled").animate({'opacity': 1, 'margin-top': '0px'})
            setTimeout(remove_msg, timeout)

    def reload(self, **context):
        self.reload_components(**context)
        self.reload_events(**context)

    def reload_components(self, **context):
        for c in self.Components.keys():
            if callable(self.Components[c].reload):
                if self.DEBUG:
                    console.info("Reload Components {0}".format(c))
                self.Components[c].reload(**context)

    def reload_component(self, component):
        comp = self.Components[component]
        if comp is not js_undefined:
            if self.DEBUG:
                console.info("Reload Component: {0}".format(component))
            comp.reload()

    def reload_events(self, **context):
        for c in self.Events.keys():
            if callable(self.Events[c].reload):

                self.Events[c].reload(**context)
        target = context.get("selector", None)
        ajax = context.get("ajax", None)
        if target is not None:
            self.I18N.DOMTranslate(target)
        elif ajax is not None and len(ajax[1]) > 0 and ajax[1][0] == "signcaptchaforms":
            self.I18N.DOMTranslate(".phanterpwa-widget-captcha-container")

    def async_function(self, callback, delay=0, **context):
        def f():
            if self.DEBUG:
                console.info("Async Callback", callback)
            callback()
            self.reload_components(**context)
            self.reload_events(**context)

        if callable(callback):
            setTimeout(f, delay)

    def save_state(self, key_state):
        """Save complete body html on specific key"""
        body_html = jQuery('body').html()
        self.states[key_state] = body_html

    def load_state(self, key_state, callback):
        page = self.states.get(key_state, None)
        body = None
        if page is not None:
            body = jQuery('body').html(page)
            self.reload_components()
        else:
            console.error("The key_state do not exist")
        if callable(callback):
            callback(body)

    def add_component(self, component):
        if isinstance(component, Component):
            self.Components[component.identifier] = component
            component.start()
        elif isinstance(component, list):
            for x in component:
                self.add_component(x)
        else:
            console.error("The component must be Component instance")

    def add_event(self, event):
        if isinstance(event, events.Event):
            self.Events[event.identifier] = event
            event.start()
        elif isinstance(event, list):
            for x in event:
                self.add_event(x)
        else:
            console.error("The event must be Event instance")

    @staticmethod
    def remove_last_auth_user():
        localStorage.removeItem("last_auth_user")

    def reload_auth_user():
        pass

    def _after_submit_login(self, data, ajax_status, callback=None):
        json = data.responseJSON
        if ajax_status == "success":
            if data.status == 200:
                authorization = json.authorization
                auth_user = json.auth_user
                client_token = json.client_token
                url_token = json.url_token
                if (authorization is not js_undefined) and\
                        (auth_user is not js_undefined) and (client_token is not js_undefined):
                    localStorage.setItem('phanterpwa-client-token', client_token)
                    localStorage.setItem('phanterpwa-url-token', url_token)
                    if auth_user["remember_me"] is True:
                        localStorage.setItem("phanterpwa-authorization", authorization)
                        localStorage.setItem("auth_user", JSON.stringify(auth_user))
                        sessionStorage.removeItem("phanterpwa-authorization")
                        sessionStorage.removeItem("auth_user")
                    else:
                        sessionStorage.setItem("phanterpwa-authorization", authorization)
                        sessionStorage.setItem("auth_user", JSON.stringify(auth_user))
                        localStorage.removeItem("phanterpwa-authorization")
                        localStorage.removeItem("auth_user")
                    self.WS.send("command_online")
                    window.PhanterPWA.set_last_auth_user(auth_user)
                    if callable(self._after_login):
                        self._after_login(self, json)
                window.PhanterPWA.open_current_way()
            elif data.status == 206:
                client_token = json.client_token
                if client_token is not js_undefined:
                    localStorage.setItem('phanterpwa-client-token', client_token)
                    sessionStorage.removeItem("phanterpwa-authorization")
                    sessionStorage.removeItem("auth_user")
                    localStorage.removeItem("phanterpwa-authorization")
                    localStorage.removeItem("auth_user")
        if self.DEBUG:
            if json.i18n is not js_undefined and json.i18n is not None:
                console.info(data.status, json.i18n.message)
        if callable(callback):
            callback(data, ajax_status)

    def _after_oauth(self, data, ajax_status, callback=None):
        json = data.responseJSON
        if ajax_status == "success":
            if data.status == 200:
                authorization = json.authorization
                auth_user = json.auth_user
                client_token = json.client_token
                url_token = json.url_token
                if (authorization is not js_undefined) and\
                        (auth_user is not js_undefined) and (client_token is not js_undefined):
                    localStorage.setItem('phanterpwa-client-token', client_token)
                    localStorage.setItem('phanterpwa-url-token', url_token)
                    if auth_user["remember_me"] is True:
                        localStorage.setItem("phanterpwa-authorization", authorization)
                        localStorage.setItem("auth_user", JSON.stringify(auth_user))
                        sessionStorage.removeItem("phanterpwa-authorization")
                        sessionStorage.removeItem("auth_user")
                    else:
                        sessionStorage.setItem("phanterpwa-authorization", authorization)
                        sessionStorage.setItem("auth_user", JSON.stringify(auth_user))
                        localStorage.removeItem("phanterpwa-authorization")
                        localStorage.removeItem("auth_user")
                    self.WS.send("command_online")
                    window.PhanterPWA.set_last_auth_user(auth_user)
                window.PhanterPWA.open_way("home")
            elif data.status == 206:
                client_token = json.client_token
                if client_token is not js_undefined:
                    localStorage.setItem('phanterpwa-client-token', client_token)
                    sessionStorage.removeItem("phanterpwa-authorization")
                    sessionStorage.removeItem("auth_user")
                    localStorage.removeItem("phanterpwa-authorization")
                    localStorage.removeItem("auth_user")
        if self.DEBUG:
            if json.i18n is not js_undefined and json.i18n is not None:
                console.info(data.status, json.i18n.message)
        if callable(callback):
            callback(data, ajax_status)

    def login(self, csrf_token, username, password, remember_me, **parameters):
        if remember_me is None or remember_me is js_undefined:
            remember_me = False
        callback = parameters.get("callback", None)
        formdata = __new__(FormData())
        formdata.append(
            "csrf_token",
            csrf_token
        )
        login_password = "{0}:{1}".format(
            window.btoa(username),
            window.btoa(password)
        )
        formdata.append("edata", login_password)
        formdata.append(
            "remember_me",
            remember_me
        )
        user_mobile_number = parameters.get("user_mobile_number", False)
        if user_mobile_number:
            formdata.append(
                "mobile",
                True
            )
        window.PhanterPWA.ApiServer.POST(**{
            'url_args': ["api", "auth"],
            'form_data': formdata,
            'onComplete': lambda data, ajax_status: self._after_submit_login(
                data, ajax_status, callback)
        })

    def oauth(self, social_name, state):
        formdata = __new__(FormData())
        formdata.append(
            "state",
            state
        )

        window.PhanterPWA.POST(
            'api',
            'oauth',
            'prompt',
            social_name,
            form_data=formdata,
            onComplete=self._after_oauth
        )

    def _after_submit_two_factor(self, data, ajax_status, callback=None):
        json = data.responseJSON
        if ajax_status == "success":
            if data.status == 200:
                authorization = json.authorization
                auth_user = json.auth_user
                client_token = json.client_token
                url_token = json.url_token
                if (authorization is not js_undefined) and\
                        (auth_user is not js_undefined) and (client_token is not js_undefined):
                    localStorage.setItem('phanterpwa-client-token', client_token)
                    localStorage.setItem('phanterpwa-url-token', url_token)
                    if auth_user["remember_me"] is True:
                        localStorage.setItem("phanterpwa-authorization", authorization)
                        localStorage.setItem("auth_user", JSON.stringify(auth_user))
                        sessionStorage.removeItem("phanterpwa-authorization")
                        sessionStorage.removeItem("auth_user")
                    else:
                        sessionStorage.setItem("phanterpwa-authorization", authorization)
                        sessionStorage.setItem("auth_user", JSON.stringify(auth_user))
                        localStorage.removeItem("phanterpwa-authorization")
                        localStorage.removeItem("auth_user")
                    self.WS.send("command_online")
                    window.PhanterPWA.set_last_auth_user(auth_user)
                window.PhanterPWA.open_current_way()
        if self.DEBUG:
            console.info(data.status, json.i18n.message)
        if callable(callback):
            callback(data, ajax_status)

    def two_factor(self, url_authorization, code, **parameters):
        callback = parameters.get("callback", None)
        formdata = __new__(FormData())
        formdata.append(
            "code",
            code
        )
        window.PhanterPWA.ApiServer.PUT(**{
            'url_args': ["api", "auth", "two-factor", url_authorization],
            'form_data': formdata,
            'onComplete': lambda data, ajax_status: self._after_submit_two_factor(
                data, ajax_status, callback)
        })

    def social_login(self, social_name, callback=None):
        window.PhanterPWA.ApiServer.GET(**{
            'url_args': ['api', 'oauth', 'prompt', social_name],
            'onComplete': lambda data, ajax_status: self._after_get_social_login(
                data, ajax_status, callback
            )
        })

    def _after_get_social_login(self, data, ajax_status, callback=None):
        json = data.responseJSON
        if ajax_status == "success":
            window.location = json.redirect
        if callable(callback):
            callback(data, ajax_status)

    def _after_submit_register(self, data, ajax_status, callback=None):
        json = data.responseJSON
        if ajax_status == "success":
            authorization = json.authorization
            auth_user = json.auth_user
            client_token = json.client_token
            url_token = json.url_token
            if (authorization is not js_undefined) and\
                    (auth_user is not js_undefined) and (client_token is not js_undefined):
                localStorage.setItem('phanterpwa-client-token', client_token)
                localStorage.setItem('phanterpwa-url-token', url_token)
                if auth_user["remember_me"] is True:
                    localStorage.setItem("phanterpwa-authorization", authorization)
                    localStorage.setItem("auth_user", JSON.stringify(auth_user))
                    sessionStorage.removeItem("phanterpwa-authorization")
                    sessionStorage.removeItem("auth_user")
                else:
                    sessionStorage.setItem("phanterpwa-authorization", authorization)
                    sessionStorage.setItem("auth_user", JSON.stringify(auth_user))
                    localStorage.removeItem("phanterpwa-authorization")
                    localStorage.removeItem("auth_user")
                self.WS.send("command_online")
                window.PhanterPWA.set_last_auth_user(auth_user)
        else:
            console.info(data.status)
        if self.DEBUG:
            console.info(json.i18n.message)
        if callback is not None:
            callback(data, ajax_status)

    def register(self, csrf_token, first_name, last_name, email, password, password_repeat, **parameters):
        callback = None
        if "callback" in parameters:
            callback = parameters["callback"]
        formdata = __new__(FormData())
        formdata.append(
            "csrf_token",
            csrf_token
        )
        formdata.append(
            "first_name",
            first_name
        )
        formdata.append(
            "last_name",
            last_name
        )
        if parameters.get("user_mobile_number", False):
            formdata.append(
                "mobile",
                email
            )
        else:
            formdata.append(
                "email",
                email
            )
        passwords = "{0}:{1}".format(
            window.btoa(password),
            window.btoa(password_repeat)
        )
        formdata.append(
            "edata",
            passwords
        )
        window.PhanterPWA.ApiServer.POST(**{
            'url_args': ["api", "auth", "create"],
            'form_data': formdata,
            'onComplete': lambda data, ajax_status: self._after_submit_register(
                data, ajax_status, callback)
        })

    def _after_submit_request_password(self, data, ajax_status, callback=None):
        json = data.responseJSON
        if self.DEBUG:
            console.info(data.status, json.i18n.message)
        if callback is not None:
            callback(data, ajax_status)

    def request_password(self, csrf_token, email, **parameters):
        last_auth_user = self.get_last_auth_user()
        if last_auth_user is not None:
            if email != last_auth_user.email:
                self.remove_last_auth_user()
        callback = None
        if "callback" in parameters:
            callback = parameters["callback"]
        formdata = __new__(FormData())
        formdata.append(
            "csrf_token",
            csrf_token
        )
        if parameters.get("user_mobile_number", False):
            formdata.append(
                "mobile",
                email
            )
        else:
            formdata.append(
                "email",
                email
            )
        window.PhanterPWA.ApiServer.POST(**{
            'url_args': ["api", "auth", "request-password"],
            'form_data': formdata,
            'onComplete': lambda data, ajax_status: self._after_submit_request_password(
                data, ajax_status, callback)
        })

    def _after_submit_activation_account(self, data, ajax_status, callback=None):
        json = data.responseJSON
        if ajax_status == "success":
            auth_user = json.auth_user
            sessionStorage.setItem("auth_user", JSON.stringify(auth_user))
            window.PhanterPWA.set_last_auth_user(auth_user)
            self.update_current_way()
        if self.DEBUG:
            console.info(data.status, json.i18n.message)
        if callback is not None:
            callback(data, ajax_status)

    def activation_account(self, csrf_token, activation_code, **parameters):
        callback = None
        if "callback" in parameters:
            callback = parameters["callback"]
        formdata = __new__(FormData())
        formdata.append(
            "csrf_token",
            csrf_token
        )
        formdata.append(
            "activation_code",
            activation_code
        )
        window.PhanterPWA.ApiServer.POST(**{
            'url_args': ["api", "auth", "active-account"],
            'form_data': formdata,
            'onComplete': lambda data, ajax_status: self._after_submit_activation_account(
                data, ajax_status, callback)
        })

    def _after_submit_change_password(self, data, ajax_status, callback=None):
        json = data.responseJSON
        if self.DEBUG:
            console.info(data.status, json.i18n.message)
        if callback is not None:
            callback(data, ajax_status)

    def change_password(self, csrf_token, password, new_password, new_password_repeat, **parameters):
        callback = None
        if "callback" in parameters:
            callback = parameters["callback"]
        formdata = __new__(FormData())
        formdata.append(
            "csrf_token",
            csrf_token
        )
        formdata.append(
            "edata",
            "{0}:{1}:{2}".format(
                window.btoa(password),
                window.btoa(new_password),
                window.btoa(new_password_repeat),
            )
        )
        window.PhanterPWA.ApiServer.POST(**{
            'url_args': ["api", "auth", "change-password"],
            'form_data': formdata,
            'onComplete': lambda data, ajax_status: self._after_submit_change_password(
                data, ajax_status, callback)
        })

    def logout(self, **parameters):
        callback = parameters.get("callback", None)
        self.WS.send("command_offline")
        sessionStorage.removeItem("phanterpwa-authorization")
        sessionStorage.removeItem("auth_user")
        sessionStorage.removeItem("_phanterpwa-user-try-activation")
        localStorage.removeItem("phanterpwa-authorization")
        localStorage.removeItem("auth_user")
        self.open_default_way()
        AuthUser = self.Components['auth_user']
        if AuthUser is not None and AuthUser is not js_undefined:
            AuthUser.start()
        LeftBar = self.Components['left_bar']
        if LeftBar is not None and LeftBar is not js_undefined:
            LeftBar.reload()
        if callable(callback):
            callback(self)
        if callable(self._after_logout):
            self._after_logout(self)

    def _after_get_csrf_token(self, data, ajax_status, callback=None):
        json = data.responseJSON
        if self.DEBUG:
            console.info(data.status, json.i18n.message)
        if callback is not None:
            callback(data, ajax_status)

    def get_csrf_token(self, table_name, **parameters):
        callback = None
        headers = None
        if "callback" in parameters:
            callback = parameters["callback"]
        if "headers" in parameters:
            headers = parameters["headers"]

        window.PhanterPWA.ApiServer.GET(**{
            "url_args": ["api", "signforms", table_name],
            "onComplete": lambda data, ajax_status: self._after_get_csrf_token(
                data, ajax_status, callback),
            "headers": headers
        })

    @staticmethod
    def xml_to_dom_element(xml, target, callback=None):
        target = jQuery(target)
        if target.length == 0:
            console.error("The target element don't exists!")
        if isinstance(xml, helpers.XmlConstructor):
            target.html(xml.jquery())
        else:
            target.html(xml)
        if callable(callback):
            callback(target)
        window.PhanterPWA.I18N.DOMTranslate(target)

    @staticmethod
    def get_consolided_way():
        current_way = sessionStorage.getItem("current_way")
        if current_way is None or current_way is js_undefined or current_way is "lock":
            current_way = "home"
        return current_way

    def get_current_way(self):
        current_way = self._get_way_from_url_hash()
        # current_way = sessionStorage.getItem("current_way")
        if current_way is None or current_way is js_undefined or current_way is "lock":
            current_way = "home"
        return current_way

    @staticmethod
    def get_current_gate():
        return str(window.PhanterPWA.get_current_way()).split("/")[0]

    @staticmethod
    def open_code_way(code=500, request=None, response=None, reasons=None):
        if str(code).isdigit():
            code = int(code)
        if code not in window.PhanterPWA.Gates:
            auth_user = window.PhanterPWA.Components.auth_user
            if window.PhanterPWA.DEBUG:
                console.info(code, request, response, reasons)
            if code == 401:
                if auth_user is not None and auth_user is not js_undefined:
                    auth_user.start()
                gatehandler.Error_401(request, response, reasons)
            elif code == 403:
                if auth_user is not None and auth_user is not js_undefined:
                    auth_user.start()
                gatehandler.Error_403(request, response, reasons)
            elif code == 404:
                gatehandler.Error_404(request, response, reasons)
            else:
                gatehandler.Error_502(request, response, reasons)
        else:
            if isinstance(request, WayRequest):
                if window.PhanterPWA.DEBUG:
                    console.info(code, request, response, reasons)
                if callable(window.PhanterPWA.Gates[code]):
                    window.PhanterPWA.Gates[code](request, response, reasons)
                else:
                    gatehandler.Error_500(request, response, reasons)
            else:
                if window.PhanterPWA.DEBUG:
                    console.error("The request must be WayRequest instance.")
                gatehandler.Error_500(request, response, reasons)

    @staticmethod
    def get_client_token():
        client_token = localStorage.getItem("phanterpwa-client-token")
        if client_token is not None and client_token is not js_undefined:
            return client_token
        else:
            return None

    @staticmethod
    def get_url_token():
        url_token = localStorage.getItem("phanterpwa-url-token")
        if url_token is not None and url_token is not js_undefined:
            return url_token
        else:
            return None

    @staticmethod
    def get_authorization():
        authorization = sessionStorage.getItem("phanterpwa-authorization")
        if authorization is None or authorization is js_undefined:
            authorization = localStorage.getItem("phanterpwa-authorization")
        else:
            localStorage.removeItem("phanterpwa-authorization")
        if authorization is not None and authorization is not js_undefined:
            return authorization
        else:
            localStorage.removeItem("auth_user")
            sessionStorage.removeItem("auth_user")
            return None

    @staticmethod
    def get_auth_user():
        auth_user = sessionStorage.getItem("auth_user")
        if auth_user is None or auth_user is js_undefined:
            auth_user = localStorage.getItem("auth_user")
        else:
            localStorage.removeItem("auth_user")
        if auth_user is not None and auth_user is not js_undefined:
            parsed_user = JSON.parse(auth_user)
            if str(parsed_user.id).isdigit():
                return parsed_user
            else:

                return None
        else:
            window.PhanterPWA.WS.send("command_offline")
            localStorage.removeItem("phanterpwa-authorization")
            sessionStorage.removeItem("phanterpwa-authorization")
            return None

    @staticmethod
    def logged():
        if window.PhanterPWA.get_auth_user() is None:
            return False
        else:
            return True

    @staticmethod
    def auth_user_has_id(ids):
        if window.PhanterPWA.logged():
            auth_user = window.PhanterPWA.get_auth_user()
            if isinstance(ids, int):
                if int(auth_user.id) == ids:
                    return True
            elif isinstance(ids, str) and ids.isdigit() and str(auth_user.id) == ids:
                return True
            elif isinstance(ids, list):
                for x in ids:
                    if window.PhanterPWA.auth_user_has_id(x):
                        return True
        return False

    @staticmethod
    def auth_user_has_role(roles):
        if window.PhanterPWA.logged():
            auth_user = window.PhanterPWA.get_auth_user()
            if isinstance(roles, str) and roles in auth_user.roles:
                return True
            elif isinstance(roles, list) and len(
                    set(auth_user.roles).intersection(set(roles))) > 0:
                return True
        return False

    def store_auth_user(self, auth_user=None):
        if auth_user is not None and auth_user is not js_undefined:
            if auth_user["remember_me"] is True:
                localStorage.setItem("auth_user", JSON.stringify(auth_user))
                sessionStorage.removeItem("auth_user")
            else:
                sessionStorage.setItem("auth_user", JSON.stringify(auth_user))
                localStorage.removeItem("auth_user")
            window.PhanterPWA.set_last_auth_user(auth_user)
        AuthUser = self.Components['auth_user']
        if AuthUser is not None and AuthUser is not js_undefined:
            AuthUser.start()
        LeftBar = self.Components['left_bar']
        if LeftBar is not None and LeftBar is not js_undefined:
            LeftBar.reload()

    def update_auth_user(self, callback=None):
        window.PhanterPWA.GET(
            **{
                'url_args':['api', 'auth'],
                "onComplete": lambda data, ajax_status: self._after_get_auth_user(data, ajax_status, callback)
            }
        )

    def _after_get_auth_user(self, data, ajax_status, callback=None):
        json = data.responseJSON
        if ajax_status == "success":
            if data.status == 200:
                authorization = json.authorization
                auth_user = json.auth_user
                client_token = json.client_token
                url_token = json.url_token
                if (auth_user is not js_undefined) and (auth_user is not None):
                    localStorage.setItem('phanterpwa-client-token', client_token)
                    localStorage.setItem('phanterpwa-url-token', url_token)
                    self.store_auth_user(auth_user)
                    if auth_user["remember_me"] is True:
                        localStorage.setItem("phanterpwa-authorization", authorization)
                        sessionStorage.removeItem("phanterpwa-authorization")
                    else:
                        sessionStorage.setItem("phanterpwa-authorization", authorization)
                        localStorage.removeItem("phanterpwa-authorization")
                    self.WS.send("command_online")
                    window.PhanterPWA.set_last_auth_user(auth_user)
        if self.DEBUG:
            console.info(data.status, json.i18n.message)
        if callable(callback):
            callback(data, ajax_status)

    @staticmethod
    def set_last_auth_user(auth_user):
        if str(auth_user.id).isdigit():
            localStorage.setItem("last_auth_user", JSON.stringify(auth_user))

    @staticmethod
    def get_auth_user_image():
        image_user = "/static/{0}/images/user.png".format(
            window.PhanterPWA.VERSIONING)
        auth_user = window.PhanterPWA.get_auth_user()
        if auth_user is not None and auth_user['image'] is not None:
            url_token = localStorage.getItem("phanterpwa-url-token")
            server = window.PhanterPWA.CONFIG["APP"]["http_address"]
            image_user = "{0}/api/auth/image/{1}?sign={2}".format(
                server,
                auth_user['image'],
                url_token
            )
        return image_user

    @staticmethod
    def get_last_auth_user_image():
        image_user = "/static/{0}/images/user.png".format(
            window.PhanterPWA.VERSIONING)
        auth_user = window.PhanterPWA.get_last_auth_user()
        if auth_user is not None and auth_user['image'] is not None:
            url_token = localStorage.getItem("phanterpwa-url-token")
            server = window.PhanterPWA.CONFIG["APP"]["http_address"]
            image_user = "{0}/api/auth/image/{1}?sign={2}".format(
                server,
                auth_user['image'],
                url_token
            )
        return image_user

    @staticmethod
    def get_last_auth_user():
        last_auth_user = localStorage.getItem("last_auth_user")
        if last_auth_user is not None and last_auth_user is not js_undefined:
            parsed_last_auth_user = JSON.parse(last_auth_user)
            if str(parsed_last_auth_user.id).isdigit():
                return parsed_last_auth_user
            else:
                return None
        else:
            return None

    def open_xway(self, *args, **kargs):
        self.open_way(self._xway(*args, **kargs))

    def open_way(self, way):
        if way == self.get_current_way():
            self.open_current_way()
        elif way == "" or way is None or way is js_undefined:
            window.location = "#_phanterpwa:/404".format(way)
        else:
            window.location = "#_phanterpwa:/{0}".format(way)

    def _onPopState(self):
        way = self._get_way_from_url_hash()
        self.Request = WayRequest()
        self.Request.open_way(way)
        # self._after_ajax_complete()
        if self._after_open_way is not None and self._after_open_way is not js_undefined:
            self._after_open_way(self.Request)

    def open_current_way(self):
        way = self._get_way_from_url_hash()
        self.Request = WayRequest()
        self.Request.open_way(way)

    def update_current_way(self):
        window.location.reload()

    def open_default_way(self):
        self.open_way(self.default_way)

    def initialize(self):
        if self.DEBUG:
            console.info("initializing...")

    def parse_url(self, url):
        l = __new__(URL(url))
        t_args = l.pathname.split("/")[1:]
        gate = t_args[0]
        c_args = t_args[1:]
        n_args = list()
        for c in c_args:
            if c is not "":
                n_args.append(c)

        params = dict()
        if l.search is not "":

            def add_in_p(k, v):
                params[k] = v
            t_params = l.searchParams
            t_params.forEach(lambda v, k: add_in_p(k, v))
        return [gate, n_args, params, url]

    def parse_way(self, way):
        gate = way
        origin = window.location.origin
        url = "{0}/{1}".format(origin, way)
        tway = self.parse_url(url)
        tway[3] = "{0}/#_phanterpwa:/{1}".format(origin, way)
        return tway

    def _get_way_from_url_hash(self):
        url_hash = window.location.hash
        way = self.default_way
        if url_hash is not js_undefined and url_hash is not None and url_hash != "":
            if url_hash.startswith("#_phanterpwa:/"):
                way = url_hash[14:]
        return way

    def _set_way_to_url_hash(self, way):
        current = self._get_way_from_url_hash()
        if way != current:
            window.history.pushState("", self.TITLE, "#_phanterpwa:/{0}".format(way))

    def set_push_way(self, way):
        sessionStorage.setItem("current_way", way)
        self._set_way_to_url_hash(way)

    def check_duplicates_ids(self):
        def check(el):
            ids = jQuery("[id='{0}']".format(el.id))
            if ids.length > 1 and ids[0] == el:
                console.warn('Multiple IDs #{0}'.format(el.id))
        jQuery('[id]').each(lambda: check(this))

    def onPopState(self):
        self.open_way(self._get_way_from_url_hash())

    def GET(self, *args, **parameters):
        self.ApiServer.GET(*args, **parameters)

    def DELETE(self, *args, **parameters):
        self.ApiServer.DELETE(*args, **parameters)

    def POST(self, *args, **parameters):
        self.ApiServer.POST(*args, **parameters)

    def PUT(self, *args, **parameters):
        self.ApiServer.PUT(*args, **parameters)

    def LOAD(self, *args, **parameters):
        Loads(*args, **parameters)


class Loads():
    def __init__(self, *args, **parameters):
        if len(args) > 0:
            self.url_args = args
        else:
            self.url_args = parameters.get("args", None)
        self.url_vars = parameters.get("vars", {})
        self.onComplete = parameters.get("onComplete", None)
        pro_args = self._process_args()
        location = __new__(URL(window.location))
        origin = location.origin
        url = "{0}/{1}".format(origin, pro_args)
        jQuery.js_get(url, self._after_load)

    def _after_load(self, data, ajax_status):
        context = self._process_vars()
        for x in context.keys():
            k = "".join(["{{", x, "}}"])
            ls = data.split(k)
            ns = str(context[x]).join(ls)
            data = ns
        if callable(self.onComplete):
            self.onComplete(data)
            window.PhanterPWA.reload()

    def _process_args(self):
        s_args = ""
        if isinstance(self.url_args, list):
            s_args = "/".join(self.url_args)
        else:
            console.error("LOAD url_args must be list(array).")
        if s_args != "":
            s_args = "{0}".format(s_args)
        return s_args

    def _process_vars(self):
        try:
            _vars = dict(self.url_vars)
        except Exception as e:
            console.error("LOAD url_vars must be dict object")
        if isinstance(_vars, dict):
            return _vars
        else:
            return {}


class Component(helpers.XmlConstructor):
    def __init__(self, identifier, *content, **attributes):
        self.actived = False
        self.identifier = identifier
        self._identifier = window.PhanterPWA.get_id(identifier)
        attributes["_phanterpwa-component"] = self._identifier
        attributes["_id"] = identifier
        if len(content) == 0:
            content = [DIV("xml content component", _style="color: red;")]
        helpers.XmlConstructor.__init__(self, "phanterpwa-component", False, *content, **attributes)
        window.PhanterPWA.add_component(self)

    def _onload(self):
        self.start()

    def reload(self, **context):
        if window.PhanterPWA.DEBUG:
            console.info("The Component {0} reload with context {1}".format(self.identifier, context))

    def start(self):
        if window.PhanterPWA.DEBUG:
            console.info("The Component {0} starts".format(self.identifier))


class Developer_Toolbar(Component):
    def __init__(self):
        Component.__init__(self, "developer_toolbar")

    def _switch_panel_objects(self):
        t = jQuery("#p-developer_toolbar")
        if t.hasClass("enabled"):
            t.removeClass("enabled")
        else:
            t.addClass("enabled")

    def _get_beautify(self):
        seen = []

        def f(k, v):
            if v is not None and __pragma__("js", "{}", "typeof v == 'object'"):
                test = __pragma__("js", "{}", "seen.indexOf(v) >= 0")
                if test:
                    return
                seen.append(v)
            return v
        response = JSON.stringify(window.PhanterPWA.Response, lambda k, v: f(k, v))
        n = JSON.parse(response)
        if n is not None and n is not js_undefined:
            request = JSON.stringify(n._request, None, 4)
            del n._request
            response = JSON.stringify(n, None, 4)
        else:
            response = None
            request = None

        return [response, request]

    def _open_modal(self):
        rr = self._get_beautify()
        request = TEXTAREA(rr[1])
        response = TEXTAREA(rr[0])
        content_ = DIV(
            DIV(
                H2("Request"),
                request,
                _class='phanterpwa-developer_toolbar phanterpwa-developer_toolbar-request'
            ),
            DIV(
                H2("Response"),
                response,
                _class='phanterpwa-developer_toolbar phanterpwa-developer_toolbar-response'
            ),
            _class="phanterpwa-developer_toolbar-objects"
        )
        self.m_modal = modal.Modal(
            "#p-developer_toolbar",
            **{
                "title": "Developer Toolbar",
                "content": content_
            }
        )
        self.m_modal.open()

    def check_duplicates_ids(self):
        def check(el):
            ids = jQuery("[id='{0}']".format(el.id))
            if ids.length > 1 and ids[0] == el:
                console.warn('Developer_Toolbar: Multiple IDs #{0}'.format(el.id))
        jQuery('[id]').each(lambda: check(this))

    def _binds(self):
        t = jQuery("#p-developer_toolbar")
        t.find(".button_developer").off("click.developer_toolbar_button").on(
            "click.developer_toolbar_button",
            self._open_modal
        )
        jQuery(window).resize(lambda: self._window_size())
        self.check_duplicates_ids()
        self._window_size()

    def _window_size(self):
        w = jQuery(window).width()
        h = jQuery(window).height()
        jQuery("#p-developer_toolbar").find(".current-size").html("{0}x{1} - ".format(w, h))

    def start(self):
        if jQuery("#p-developer_toolbar").length == 0:
            xml = DIV(
                _id="p-developer_toolbar"
            )
            xml.append_to(
                "body"
            )
        self._binds()


class WayRequest():
    def __init__(self):
        self.timestamp = __new__(Date().getTime())
        self.application_info = None
        self.auth_user = None
        self.gate = "home"
        self.way = "home"
        self.params = None
        self.args = None
        self.last_way = "home"
        self._element = None
        self.widgets = {}
        self.js_params = None
        self.error = None

    @staticmethod
    def _body_flag(*new_flag):
        body = jQuery("body")
        lclass = body.attr("class")
        r = __new__(RegExp(r"/\s+/"))
        if lclass is not js_undefined:
            lclass = lclass.split(r)
            for x in lclass:
                if x.startswith("phanterpwa-flag-"):
                    body.removeClass(x)
        for f in new_flag:
            if f.startswith("phanterpwa-flag-"):
                f = f.replace("/", "_")
                body.addClass(f)
            else:
                f = f.replace("/", "_")
                body.addClass("phanterpwa-flag-{0}".format(f))

    def add_widget(self, widget):
        if isinstance(widget, widgets.Widget):
            self.widgets[widget.identifier] = widget
            if callable(widget.initialize):
                widget.initialize()

    def _process_way(self, way):
        self.application_info = "{0} (version: {1}, compilation: {2})".format(
            window.PhanterPWA.CONFIG.PROJECT.title,
            window.PhanterPWA.CONFIG.PROJECT.version,
            window.PhanterPWA.CONFIG.PROJECT.compilation
        )
        self.auth_user = window.PhanterPWA.get_auth_user()
        self.gate = way
        self.way = way
        if "?" in self.way or "/" in self.way:
            l = "{0}/{1}".format(window.PhanterPWA.CONFIG.APP.http_address, self.way)
            l = __new__(URL(l))
            t_args = l.pathname.split("/")[1:]
            self.gate = t_args[0]
            c_args = t_args[1:]
            n_args = list()
            for c in c_args:
                if c is not "":
                    n_args.append(c)

            if len(n_args) > 0:
                self.args = n_args

            if l.search is not "":
                p = dict()
                __pragma__("jsiter")
                o = {}
                __pragma__("nojsiter")

                def add_in_p(k, v):
                    p[k] = v
                    o[k] = v
                t_params = l.searchParams
                t_params.forEach(lambda v, k: add_in_p(k, v))
                self.params = p
                self.js_params = o
                self.str_params = t_params.toString()

    def get_arg(self, arg):
        if arg is not None and arg is not js_undefined:
            if len(self.args) >= int(arg) + 1:
                return self.args[arg]
            else:
                return None
        else:
            return None

    def get_param(self, k):
        if self.params is not None and self.params is not js_undefined:
            return self.params.get(k, None)
        else:
            return None

    def _open_way(self, way):
        self._process_way(way)
        self._body_flag(self.gate)
        last_way = window.PhanterPWA.get_current_way()
        self.last_way = last_way
        if self.gate in window.PhanterPWA.Gates:
            # if window.PhanterPWA.DEBUG:
            #     sessionStorage.setItem("current_way", self.way)

            #     window.PhanterPWA.Gates[self.gate](self)
            # else:
            try:
                window.PhanterPWA.Gates[self.gate](self)
            except:
                window.PhanterPWA.onGlobalError(__except0__.message, __except0__.fileName, __except0__.lineNumber, __except0__.columnNumber, __except0__.name)
                window.PhanterPWA.open_code_way(500, self)
                if window.PhanterPWA.DEBUG:
                    console.error(__except0__)
                else:
                    console.error("Error on try open '{0}'".format(way))
            else:
                sessionStorage.setItem("current_way", self.way)

        else:
            self.error = 404
            window.PhanterPWA.open_code_way(404, self)
        if self.DEBUG:
            if self._element is not None:
                console.info(
                    "Using the element ", self._element, "to try way '{0}'. ".format(self.way), "request: ", self)
            else:
                console.info("Try programatically way to '{0}'. ".format(self.way), "request: ", self)
        setTimeout(
            lambda: window.PhanterPWA.ProgressBar.removeEventProgressBar("OPEN_WAY_{0}".format(self.timestamp)), 300)

    def open_way(self, way):
        self.timestamp = __new__(Date().getTime())
        window.PhanterPWA.ProgressBar.addEventProgressBar("OPEN_WAY_{0}".format(self.timestamp))
        setTimeout(lambda: self._open_way(way), 30)


__pragma__('nokwargs')
