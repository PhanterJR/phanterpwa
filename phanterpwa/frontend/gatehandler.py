#?from org.transcrypt.stubs.browser import __pragma__
from phanterpwa.frontend import (
    helpers,
    decorators,
    application
)
# __pragma__ ('ecom')
#?__pragma__('alias', "jQuery", "$")
#?__pragma__('skip')

# it is ignored on transcrypt
window = console = __new__ = Date = URL = sessionStorage = \
    js_undefined = jQuery = this = Object = JSON = 0

#?__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")
P = helpers.XmlConstructor.tagger("P")
H3 = helpers.XmlConstructor.tagger("h3")
H2 = helpers.XmlConstructor.tagger("h2")
IMG = helpers.XmlConstructor.tagger("img", True)
I18N = helpers.I18N
CONCATENATE = helpers.CONCATENATE

#?__pragma__('kwargs')


class RequestHandler():
    def __init__(self, request, **parameters):
        if not isinstance(request, application.WayRequest):
            raise ValueError()
        self.request = request
        self.current_user = window.PhanterPWA.get_auth_user()
        self.on_error = parameters.get("on_error", None)
        self._status_code = 200
        self._reason = "Unknown"
        self._settings = dict()
        self._preview()
        self._initialize()
        self._callbacks_on_error = []
        self._callbacks_on_finish = []

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, value):
        if str(value).isdigit():
            self._status_code = value
        else:
            raise ValueError("The status_code must be integer.")
    
    def set_status(self, status_code: int, reason: str = None) -> None:
        """Sets the status code for your response.

        :arg int status_code: Response status code.
        :arg str reason: Human-readable reason phrase describing the status

        """
        self.status_code = status_code
        if isinstance(reason, str):
            self._reason = reason
        else:
            self._reason = "Unknown"

    def get_status(self) -> int:
        """Returns the status code for your response."""
        return self._status_code

    def _error(self, code=200):
        if code != 200:
            self.status = code
            if callable(self.on_error):
                self.on_error(code, self)
            window.PhanterPWA.open_code_way(code, self, self.Request)

    def _preview(self):
        if window.PhanterPWA.DEBUG:
            console.info("method not used: RequestHandler._preview")
            console.info("call preview method")
        self.preview()

    def _initialize(self):
        if window.PhanterPWA.DEBUG:
            console.info("method not used: RequestHandler._initialize")
            console.info("call initialize method")
        self.initialize()

    def preview(self):
        if window.PhanterPWA.DEBUG:
            console.info("method not used: RequestHandler.preview")

    def initialize(self, *args, **kwargs):
        if window.PhanterPWA.DEBUG:
            console.info("method not used: RequestHandler.initialize")

    def finish(self):
        if self.status == 200:
            window.PhanterPWA.Response = self


class Handler():

    def __init__(self, request, **parameters):
        self._request = request
        self.debug = window.PhanterPWA.DEBUG
        self.config = window.PhanterPWA.CONFIG
        self._authorized_roles = "all"
        self._authorized_users = "all"
        self._back = window.PhanterPWA.get_current_way()
        self._status = 401
        self._on_error = parameters.get("on_error", None)
        self._current_user = window.PhanterPWA.get_auth_user()
        self._initialize()

    @property
    def auth_user(self):
        self._current_user = window.PhanterPWA.get_auth_user()
        return self._current_user    

    @property
    def current_user(self):
        self._current_user = window.PhanterPWA.get_auth_user()
        return self._current_user

    def stringify(self):
        seen = []
        def f(k, v):
            #?is_obj = __pragma__("js", "{}", "typeof v == 'object'")
            is_obj = isinstance(v, object) #__: skip
            if v is not None and is_obj:
                test = v in seen #__: skip
                #?test = __pragma__("js", "{}", "seen.indexOf(v) >= 0")
                if k.startswith("_"):
                    return
                elif test:
                    return
                seen.append(v)
            return v

        return JSON.stringify(self, lambda k, v: f(k, v))

    def _check_authorized_users(self):
        if self._authorized_users == "all":
            return True
        elif self._authorized_users == "login":
            if self.auth_user is not None:
                return True
        elif self._authorized_users == "nologin":
            if self.auth_user is None:
                return True
        elif isinstance(self._authorized_users, list):
            if self.auth_user is not None and int(self.auth_user.id) in self._authorized_users:
                return True
        return False

    def _check_authorized_roles(self):
        if self._authorized_roles == "all":
            return True
        elif isinstance(self._authorized_roles, str) and self.auth_user is not None:
            if self._authorized_roles in self.auth_user.roles:
                return True
        elif isinstance(self._authorized_roles, list):
            if self.auth_user is not None and len(
                    set(self.auth_user.roles).intersection(set(self.autorized_roles))) > 0:
                return True
        return False

    def check_has_authorization(self):
        self.auth_user = window.PhanterPWA.get_auth_user()
        if self._check_authorized_users() and self._check_authorized_roles():
            return True
        elif self.auth_user is not None:
            if self._authorized_users == "nologin":
                return 400
            else:
                return 403
        return 401

    def on_click_back_button(self):
        window.PhanterPWA.open_way(self._back)

    def _on_credentials_fail(self):
        window.PhanterPWA.open_code_way(self._has_authorization, self._request, self)

    def _initialize(self):
        if window.PhanterPWA.DEBUG:
            console.info("method not used: RequestHandler._initialize")
            console.info("call initialize method")
        self.request = self._request
        self.initialize()
        window.PhanterPWA.reload_components()
        self._has_authorization = self.check_has_authorization()
        if self._has_authorization is True:
            window.PhanterPWA.Response = self
            self.set_title()
        else:
            if callable(self._on_error):
                self._on_error(self._has_authorization, self)
            else:
                self._on_credentials_fail()

    def initialize(self):
        if window.PhanterPWA.DEBUG:
            console.info("method not used: Handler.initialize")

    def widgets_initialize(self):
        for x in self.request.widgets.keys():
            pass
            #self.request.widgets[x].start()

    def set_title(self, value=None):
        if value is None:
            title = jQuery("title").text()
            if window.PhanterPWA.CONFIG.PROJECT.title != title:
                jQuery("title").text(window.PhanterPWA.CONFIG.PROJECT.title)
        else:
            jQuery("title").text(value)



class ErrorHandler():
    def __init__(self, request, response=None, reasons=None):
        self._request = request
        self.reasons = reasons
        self.debug = window.PhanterPWA.DEBUG
        self.requires_login = False
        self.autorized_roles = ["all"]
        self.autorized_ids = ["all"]
        self.way_on_back = window.PhanterPWA.get_current_way()
        self.initialize()
        self._credentials = True
        if self._credentials is True:
            window.PhanterPWA.Response = response
            self.start()
        else:
            self.on_credentials_fail()

    def on_click_back_button(self):
        window.PhanterPWA.open_way(self.way_on_back)

    def on_credentials_fail(self):
        if self.debug:
            console.info('method not used: ErrorHandler.on_credentials_fail()')

    def initialize(self):
        if self.debug:
            console.info("method not used: ErrorHandler.initialize()")

    def start(self):
        if self.debug:
            console.info("method not used: ErrorHandler.start()")


html_base = CONCATENATE(
    DIV(
        DIV(
            DIV(
                DIV(I18N("Ops!!!", **{"_pt-br": "Ops!!!"}), _class="phanterpwa-breadcrumb"),
                _class="phanterpwa-breadcrumb-wrapper"
            ),
            _class="phanterpwa-container container"),
        _class='title_page_container card'
    ),
    DIV(
        DIV(
            DIV(
                DIV(
                    DIV(
                        DIV(
                            IMG(
                                _class='image-warnings'
                            ),
                            _class="image-warnings-container"
                        ),
                        DIV(_id='content-warning'),
                        _class='content-warnings'
                    ),
                    _class='warnings-container phanterpwa-card-container'
                ),
                _class="card"
            ),
            _class="new-container"
        ),
        _class="phanterpwa-container container"
    )
)


class Error_401(ErrorHandler):
    def start(self):
        html = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV(I18N("Authentication required", **{"_pt-br": "Necessário Autenticar-se"}), _class="phanterpwa-breadcrumb"),
                        _class="phanterpwa-breadcrumb-wrapper"
                    ),
                    _class="phanterpwa-container container"),
                _class='title_page_container card'
            ),
            DIV(
                DIV(
                    DIV(
                        DIV(
                            DIV(
                                IMG(
                                    _class='image-warnings',
                                    _src="/static/{0}/images/warning.png".format(window.PhanterPWA.VERSIONING)
                                ),
                            ),
                            _class="image-warnings-container"
                        ),
                        DIV(
                            H3(I18N(
                                "You need authentication to access this feature.",
                                **{
                                    "_pt-br": "Você precisa autenticar-se para tentar acessar este recurso."
                                }
                            )),
                            H3(self.reasons) if self.reasons is not None else "",
                            _id='content-warning',
                            _class='content-warnings'
                        ),
                        DIV(
                            DIV(
                                I18N("Login"),
                                _id="alternative_login_button",
                                _class="btn wave_on_click link"
                            ),
                            _class="button-container"
                        ),
                        _class='warnings-container card phanterpwa-card-container'
                    ),
                    _class="new-container"
                ),
                _class="phanterpwa-container container"
            )
        )
        html.html_to("#main-container")
        jQuery("#alternative_login_button").off("click.alternative_login_button").on(
            "click.alternative_login_button",
            lambda: window.PhanterPWA.Components["auth_user"].modal_login()
        )


class Error_403(ErrorHandler):
    def start(self):
        html = html_base.jquery()
        html.find(".image-warnings").attr(
            "src", "/static/{0}/images/warning.png".format(window.PhanterPWA.VERSIONING))
        html_warning = CONCATENATE(
            H3("ERROR 403 - Forbidden"),
            P(self.reasons) if self.reasons is not None else ""
        )
        html.find("#content-warning").html(html_warning.jquery())
        jQuery("#main-container").html(html)


class Error_404(ErrorHandler):
    def start(self):
        html = html_base.jquery()
        html.find(".image-warnings").attr(
            "src", "/static/{0}/images/warning.png".format(window.PhanterPWA.VERSIONING))
        html_warning = CONCATENATE(
            H3("ERROR 404 - Not Found"),
            P(self.reasons) if self.reasons is not None else ""
        )
        html.find("#content-warning").html(html_warning.jquery())
        jQuery("#main-container").html(html)


class Error_409(ErrorHandler):
    def start(self):
        html = html_base.jquery()
        html.find(".image-warnings").attr(
            "src", "/static/{0}/images/warning.png".format(window.PhanterPWA.VERSIONING))
        html_warning = CONCATENATE(
            H3("ERROR 404 - Not Found"),
            P(self.reasons) if self.reasons is not None else ""
        )
        html.find("#content-warning").html(html_warning.jquery())
        jQuery("#main-container").html(html)

class Error_500(ErrorHandler):
    def start(self):
        html = html_base.jquery()
        html.find(".image-warnings").attr(
            "src", "/static/{0}/images/warning.png".format(window.PhanterPWA.VERSIONING))
        html_warning = CONCATENATE(
            H3("ERROR 500 - Internal Error"),
            P(self.reasons) if self.reasons is not None else ""
        )
        html.find("#content-warning").html(html_warning.jquery())
        jQuery("#main-container").html(html)

class Error_502(ErrorHandler):
    def start(self):
        html = html_base.jquery()
        html.find(".image-warnings").attr(
            "src", "/static/{0}/images/warning.png".format(window.PhanterPWA.VERSIONING))
        html_warning = CONCATENATE(
            H3("ERROR 502 - Bad Gateway"),
            P(self.reasons) if self.reasons is not None else ""
        )
        html.find("#content-warning").html(html_warning.jquery())
        jQuery("#main-container").html(html)



#?__pragma__('nokwargs')
# __pragma__ ('noecom')