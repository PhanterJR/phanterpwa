from org.transcrypt.stubs.browser import __pragma__
import phanterpwa.apptools.server as server
import phanterpwa.apptools.progressbar as progressbar
import phanterpwa.apptools.i18n as i18n
import phanterpwa.apptools.helpers as helpers
import phanterpwa.apptools.forms as forms
import phanterpwa.apptools.components.widgets as widgets
import phanterpwa.apptools.components.events as events
import phanterpwa.apptools.handler as handler
import phanterpwa.apptools.components.modal as modal
import phanterpwa.apptools.websocket as websocket

__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = URL = M = FormData = setTimeout =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

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
        if config is js_undefined or config is None:
            raise ValueError("The config is required")
        if gates is js_undefined or gates is None:
            raise ValueError("The gates is required")
        self.CONFIG = config
        self.NAME = config.PROJECT.name
        self.TITLE = config.PROJECT.title
        self.VERSION = config.PROJECT.version
        self.COMPILATION = config.PROJECT.compilation
        self.AUTHOR = config.PROJECT.author
        self.DEBUG = config.PROJECT.debug
        self.Gates = dict(gates)
        self.ProgressBar = progressbar.ProgressBar("#main-progress-bar-container")
        self.Request = WayRequest(self.Gates)
        self.Components = {}
        self.Events = {}
        self.Cache = {}
        self.Response = None
        self.default_way = parameters.get("default_way", "home")
        self._after_open_way = parameters.get("after_open_way", None)
        self.counter = 0
        self.states = dict()
        self._social_login_icons = {
            "google": I(_class="fab fa-google"),
            "facebook": I(_class="fab fa-facebook"),
            "twitter": I(_class="fab fa-twitter")
        }

        jQuery(document).ajaxComplete(
            lambda event, xhr, options: self._after_ajax_complete(event, xhr, options)
        )
        window.PhanterPWA = self
        if self.DEBUG:
            console.info("starting {0} application (version: {1}, compilation: {2})".format(
                self.CONFIG.PROJECT.title, self.CONFIG.PROJECT.version, self.CONFIG.PROJECT.compilation)
            )
        self.add_event(events.Waves())
        self.add_event(events.WidgetsInput())
        self.add_event(events.WayHiperlinks())
        self.ApiServer = server.ApiServer()
        self.ApiServer.getClientToken()
        self.I18N = i18n.I18NServer()
        self.WS = websocket.WebSocketPhanterPWA(self.CONFIG["CONFIGJS"]["api_websocket_address"])
        if self.DEBUG:
            self.add_component(Developer_Toolbar())

    def get_inicial_config_uri(self):
        initial_config = __new__(URL(window.location.href))
        params = initial_config.searchParams
        authorization = params.js_get("authorization")
        client_token = params.js_get("client_token")
        url_token = params.js_get("url_token")
        auth_user = params.js_get("auth_user")
        redirect = params.js_get("redirect")
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
            localStorage.setItem("last_auth_user", JSON.stringify(auth_user))
        if redirect is not None:
            window.location = redirect

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

    def social_login_list(self):
        social_logins = window.PhanterPWA["CONFIG"]["SOCIAL_LOGINS"]
        s_logins = dict()
        if social_logins is not None and social_logins is not js_undefined:
            s_logins = dict(social_logins)
        list_login = social_logins.keys()
        l = []
        for x in list_login:
            if x in self._social_login_icons:
                l.append([x, self._social_login_icons[x]])
            else:
                l.append([x, I(_class="fas fa-at")])
        return l

    @staticmethod
    def get_app_name(self):
        return window.PhanterPWA.CONFIG["APP"]["name"]

    @staticmethod
    def get_api_address(self):
        return window.PhanterPWA.CONFIG["CONFIGJS"]["api_server_address"]

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

    def reload_events(self, **context):
        for c in self.Events.keys():
            if callable(self.Events[c].reload):
                if self.DEBUG:
                    console.info("Reload Event {0}".format(c))
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

    def remove_last_auth_user(self):
        localStorage.removeItem("last_auth_user")

    def _after_submit_login(self, data, ajax_status, callback=None):
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
                localStorage.setItem("last_auth_user", JSON.stringify(auth_user))
            window.PhanterPWA.open_current_way()
        if self.DEBUG:
            console.info(data.status, json.i18n.message)
        if callback is not None:
            callback(data, ajax_status)

    def login(self, csrf_token, username, password, remember_me, **parameters):
        callback = None

        if remember_me is None or remember_me is js_undefined:
            remember_me = False
        if "callback" in parameters:
            callback = parameters["callback"]
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
        window.PhanterPWA.ApiServer.POST(**{
            'url_args': ["api", "auth"],
            'form_data': formdata,
            'onComplete': lambda data, ajax_status: self._after_submit_login(
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
            console.log(json)
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
                localStorage.setItem("last_auth_user", JSON.stringify(auth_user))
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
            localStorage.setItem("last_auth_user", JSON.stringify(auth_user))
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
        callback = None
        if "callback" in parameters:
            callback = parameters["callback"]
        self.WS.send("command_offline")
        sessionStorage.removeItem("phanterpwa-authorization")
        sessionStorage.removeItem("auth_user")
        localStorage.removeItem("phanterpwa-authorization")
        localStorage.removeItem("auth_user")
        self.open_default_way()
        if callback is not None:
            callback()

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
    def get_current_way():
        current_way = sessionStorage.getItem("current_way")
        if current_way is None or current_way is js_undefined or current_way is "lock":
            current_way = "home"
        return current_way

    @staticmethod
    def open_code_way(code=500, request=None, response=None):
        if str(code).isdigit():
            code = int(code)
        if code not in window.PhanterPWA.Gates:
            if window.PhanterPWA.DEBUG:
                console.info(code, request, response)
            if code == 401:
                handler.Error_401(request, response)
            elif code == 403:
                handler.Error_403(request, response)
            elif code == 404:
                handler.Error_404(request, response)
            else:
                handler.Error_502(request, response)
        else:
            if isinstance(request, WayRequest):
                window.PhanterPWA.Gates[code](request, response)
            else:
                if window.PhanterPWA.DEBUG:
                    console.error("The request must be WayRequest instance.")
                handler.Error_500(request, response)

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
            return JSON.parse(auth_user)
        else:
            window.PhanterPWA.WS.send("command_offline")
            localStorage.removeItem("phanterpwa-authorization")
            sessionStorage.removeItem("phanterpwa-authorization")
            return None

    @staticmethod
    def update_auth_user(auth_user):
        if auth_user is not None and auth_user is not js_undefined:
            if auth_user["remember_me"] is True:
                localStorage.setItem("auth_user", JSON.stringify(auth_user))
                sessionStorage.removeItem("auth_user")
            else:
                sessionStorage.setItem("auth_user", JSON.stringify(auth_user))
                localStorage.removeItem("auth_user")
            localStorage.setItem("last_auth_user", JSON.stringify(auth_user))

    @staticmethod
    def get_auth_user_image():
        image_user = "/static/{0}/images/user.png".format(
            window.PhanterPWA.CONFIG.PROJECT.version)
        auth_user = window.PhanterPWA.get_auth_user()
        if auth_user is not None and auth_user['image'] is not None:
            url_token = localStorage.getItem("phanterpwa-url-token")
            server = window.PhanterPWA.CONFIG["CONFIGJS"]["api_server_address"]
            image_user = "{0}/api/auth/image/{1}?sign={2}".format(
                server,
                auth_user['image'],
                url_token
            )
        return image_user

    @staticmethod
    def get_last_auth_user_image():
        image_user = "/static/{0}/images/user.png".format(
            window.PhanterPWA.CONFIG.PROJECT.version)
        auth_user = window.PhanterPWA.get_last_auth_user()
        if auth_user is not None and auth_user['image'] is not None:
            url_token = localStorage.getItem("phanterpwa-url-token")
            server = window.PhanterPWA.CONFIG["CONFIGJS"]["api_server_address"]
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
            return JSON.parse(last_auth_user)
        else:
            return None

    def open_way(self, way):
        self.Request = WayRequest()
        self.Request.open_way(way)
        self._after_ajax_complete()
        if self._after_open_way is not None and self._after_open_way is not js_undefined:
            self._after_open_way(self.Request)

    def open_current_way(self):
        self.open_way(self.get_current_way())

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
        if "?" in way or "/" in way:
            url = "{0}/{1}".format(window.PhanterPWA.CONFIG.CONFIGJS.api_server_address, way)
            return self.parse_url(url)
        else:
            return {gate, [], {}, way}

    def GET(self, **parameters):
        self.ApiServer(**parameters)

    def DELETE(self, **parameters):
        self.ApiServer(**parameters)

    def POST(self, **parameters):
        self.ApiServer(**parameters)

    def PUT(self, **parameters):
        self.ApiServer(**parameters)

    def LOAD(self, **parameters):
        Loads(**parameters)


class Loads():
    def __init__(self, **parameters):
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
        self.error = None

    def add_widget(self, widget):
        if isinstance(widget, widgets.Widget):
            self.widgets[widget.identifier] = widget
            if callable(widget.start):
                widget.start()

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
            l = "{0}/{1}".format(window.PhanterPWA.CONFIG.CONFIGJS.api_server_address, self.way)
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

                def add_in_p(k, v):
                    p[k] = v
                t_params = l.searchParams
                t_params.forEach(lambda v, k: add_in_p(k, v))
                self.params = p

    def get_arg(self, arg):
        if arg is not None and arg is not js_undefined:
            if len(self.args) >= int(arg) + 1:
                return self.args[arg]
            else:
                return None
        else:
            return None

    def get_param(self, k):
        return self.params.get(k, None)

    def open_way(self, way):
        self.timestamp = __new__(Date().getTime())
        self._process_way(way)
        last_way = window.PhanterPWA.get_current_way()
        self.last_way = last_way
        if self.gate in window.PhanterPWA.Gates:
            sessionStorage.setItem("current_way", self.way)
            window.PhanterPWA.Gates[self.gate](self)
        else:
            self.error = 404
            window.PhanterPWA.Gates[404](self)
        if self.DEBUG:
            if self._element is not None:
                console.info(
                    "Using the element ", self._element, "to try way '{0}'. ".format(self.way), "request: ", self)
            else:
                console.info("Try programatically way to '{0}'. ".format(self.way), "request: ", self)


__pragma__('nokwargs')
