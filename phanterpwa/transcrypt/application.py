from org.transcrypt.stubs.browser import __pragma__
import phanterpwa.transcrypt.server as server
import phanterpwa.transcrypt.progressbar as progressbar
import phanterpwa.transcrypt.i18n as i18n
import phanterpwa.transcrypt.helpers as helpers

__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = URL = M = FormData =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')


__pragma__('kwargs')


DIV = helpers.XmlConstructor.tagger("div")


class PhanterPWA():
    def __init__(self, config, routes, **parameters):
        self.initialize()
        if config is js_undefined or config is None:
            raise ValueError("The config is required")
        if routes is js_undefined or routes is None:
            raise ValueError("The config is required")
        self.CONFIG = config
        self.NAME = config.PROJECT.name
        self.TITLE = config.PROJECT.title
        self.VERSION = config.PROJECT.version
        self.COMPILATION = config.PROJECT.compilation
        self.AUTHOR = config.PROJECT.author
        self.DEBUG = config.PROJECT.debug
        self.Routes = dict(routes)
        self.ProgressBar = progressbar.ProgressBar("#main-progress-bar-container")
        self.Request = RequestRouter(self.Routes)
        self.route_links()
        self.Components = {}
        self.Response = None
        self.default_route = "home"
        self._after_route = None
        if "default_route" in parameters:
            self.default_route = parameters['default_route']
        if "after_route" in parameters:
            self._after_route = parameters["after_route"]

        def afterAjaxComplete(event, xhr, options):
            self.I18N.DOMTranslate("body")
            self.route_links()
            M.updateTextFields()

        jQuery(document).ajaxComplete(
            lambda event, xhr, options: afterAjaxComplete(event, xhr, options)
        )
        window.PhanterPWA = self
        self.ApiServer = server.ApiServer()
        self.ApiServer.getClientToken()
        self.I18N = i18n.I18NServer()
        self.DOMXmlWriter = helpers.DOMXmlWriter(after_write=self.I18N.DOMTranslate)

    def _after_ajax_complete(self, event, xhr, option):
        self.I18N.DOMTranslate("body")
        self.route_links()
        M.updateTextFields()

    def add_component(self, component):
        if isinstance(component, Component):
            self.Components[component.identifier] = component
            component.start()
        elif isinstance(component, list):
            for x in component:
                self.add_component(x)
        else:
            console.error("The component must be Component instance")

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
                localStorage.setItem("last_auth_user", JSON.stringify(auth_user))
        if self.DEBUG:
            console.log(data.status, json.i18n.message)
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
                localStorage.setItem("last_auth_user", JSON.stringify(auth_user))
        else:
            console.log(data.status)
        if self.DEBUG:
            console.log(json.i18n.message)
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
            console.log(data.status, json.i18n.message)
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
            console.log(data.status, json.i18n.message)
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
            console.log(data.status, json.i18n.message)
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
        sessionStorage.removeItem("phanterpwa-authorization")
        sessionStorage.removeItem("auth_user")
        localStorage.removeItem("phanterpwa-authorization")
        localStorage.removeItem("auth_user")
        self.open_default_route()
        if callback is not None:
            callback()

    def _after_get_csrf_token(self, data, ajax_status, callback=None):
        json = data.responseJSON
        if self.DEBUG:
            console.log(data.status, json.i18n.message)
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
    def xml_to_dom_element(xml, target, after_write=None):
        target = jQuery(target)
        console.log(target)
        if target.length == 0:
            console.error("The target element don't exists!")
        if isinstance(xml, helpers.XmlConstructor):
            target.html(xml.jquery())
        else:
            target.html(xml)
        if after_write is not None and after_write is not js_undefined:
            after_write(target)
        window.PhanterPWA.I18N.DOMTranslate(target)

    @staticmethod
    def get_current_route():
        current_route = sessionStorage.getItem("current_route")
        if current_route is None or current_route is js_undefined or current_route is "lock":
            current_route = "home"
        return current_route

    @staticmethod
    def open_code_route(self, code=500, request=None):
        code_routes = window.PhanterPWA.Routes.onCode
        if code not in code_routes:
            code_routes[500]()
        else:
            if isinstance(request, RequestRouter):
                code_routes[code](request)
            else:
                code_routes[500]()

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

    def open_route(self, route):
        self.Request = RequestRouter(self.Routes)
        self.Request.open_route(route)
        self._after_ajax_complete()
        if self._after_route is not None and self._after_route is not js_undefined:
            self._after_route(self.Request)

    def open_route_by_element(self, element=None):
        self.Request = RequestRouter(self.Routes)
        self.Request.element = element
        self.Request.open_route(jQuery(element).attr('phanterpwa_route'))
        self._after_ajax_complete()
        if self._after_route is not None and self._after_route is not js_undefined:
            self._after_route(self.Request)

    def open_current_route(self):
        self.open_route(self.get_current_route())

    def open_default_route(self):
        self.open_route(self.default_route)

    def start(self):
        if self.DEBUG:
            console.info("starting {0} application (version: {1}, compilation: {2})".format(
                self.CONFIG.PROJECT.title, self.CONFIG.PROJECT.version, self.CONFIG.PROJECT.compilation)
            )
        self.open_default_route()

    def initialize(self):
        if self.DEBUG:
            console.info("initializing...")

    def route_links(self, target=None):
        if jQuery("body").hasClass("phanterpwa-lock"):
            jQuery("[phanterpwa_route]").off("click.phanterpwa_route_link")
        else:
            if target is not None and target is not js_undefined:
                target = jQuery(target)
                if target.length > 0:
                    target.find("[phanterpwa_route]").off(
                        "click.phanterpwa_route_link"
                    ).on(
                        "click.phanterpwa_route_link",
                        lambda: self.open_route_by_element(this)
                    )
                else:
                    jQuery("[phanterpwa_route]").off(
                        "click.phanterpwa_route_link"
                    ).on(
                        "click.phanterpwa_route_link",
                        lambda: self.open_route_by_element(this)
                    )
            else:
                jQuery("[phanterpwa_route]").off(
                    "click.phanterpwa_route_link"
                ).on(
                    "click.phanterpwa_route_link",
                    lambda: self.open_route_by_element(this)
                )


class Component(helpers.DOMXmlWriter):
    def __init__(self, identifier, target_element):
        self.identifier = identifier
        self.target_element = jQuery(target_element)
        self.xml = DIV("xml content component", _style="color: red;")

    def start(self):
        if window.PhanterPWA is not js_undefined:
            if window.PhanterPWA.DEBUG:
                console.log("The Component {0} starts".format(self.identifier))
        PhanterPWA.xml_to_dom_element(self.xml, self.target_element)


__pragma__('nokwargs')


class RequestRouter():
    def __init__(self, routes):
        self.timestamp = __new__(Date().getTime())
        self.client = None
        self.authorization = None
        self.auth_user = None
        self._Routes = dict(routes)
        self.route = "home"
        self.phanterpwa_route = "home"
        self.params = None
        self.args = None
        self.last_route = "home"
        self.element = None

    def _process_phanterpwa_route(self, phanterpwa_route):
        self.route = phanterpwa_route
        self.phanterpwa_route = phanterpwa_route
        if "?" in phanterpwa_route or "/" in phanterpwa_route:
            l = "{0}/{1}".format(window.PhanterPWA.CONFIG.CONFIGJS.api_server_address, phanterpwa_route)
            l = __new__(URL(l))
            t_args = l.pathname.split("/")[1:]
            self.route = t_args[0]
            c_args = t_args[1:]
            n_args = list()
            for c in c_args:
                if c is not "":
                    n_args.append(c)

            if len(n_args) > 0:
                self.args = n_args

            if l.search is not "":
                __pragma__("jsiter")
                p = {}
                __pragma__("nojsiter")

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

    def open_route(self, phanterpwa_route):
        self.timestamp = __new__(Date().getTime())
        self._process_phanterpwa_route(phanterpwa_route)
        if self.route in self._Routes:
            last_route = window.PhanterPWA.get_current_route()
            self.last_route = last_route
            sessionStorage.setItem("current_route", self.phanterpwa_route)
            self._Routes[self.route](self)
        else:
            self._Routes.onCode["404"](self)
        if self.DEBUG:
            if self.element is not None:
                console.info(
                    "Using the element ", self.element, "to try route '{0}'. ".format(self.route), "request: ", self)
            else:
                console.info("Try programatically route to '{0}'. ".format(self.route), "request: ", self)
