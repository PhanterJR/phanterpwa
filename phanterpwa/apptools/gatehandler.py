from org.transcrypt.stubs.browser import __pragma__
from phanterpwa.apptools import (
    helpers
)
__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = console = __new__ = Date = URL = sessionStorage = \
    js_undefined = jQuery = this = Object = JSON = 0

__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")
IMG = helpers.XmlConstructor.tagger("img", True)
I18N = helpers.I18N
CONCATENATE = helpers.CONCATENATE

__pragma__('kwargs')


class Handler():

    def __init__(self, request, **parameters):
        self._request = request
        self.debug = window.PhanterPWA.DEBUG
        self.config = window.PhanterPWA.CONFIG
        self._authorized_roles = parameters.get("authorized_roles", "all")
        self._authorized_users = parameters.get("authorized_users", "all")
        self._back = window.PhanterPWA.get_current_way()
        self._status = 401
        self._on_error = parameters.get("on_error", None)
        self.auth_user = window.PhanterPWA.get_auth_user()
        self._has_authorization = self.check_has_authorization()
        if self._has_authorization is True:
            self.request = request
            window.PhanterPWA.Response = self
            self.initialize()
            self.widgets_initialize()
        else:
            if callable(self._on_error):
                self._on_error(self._has_authorization, self)
            else:
                self._on_credentials_fail()

    def stringify(self):
        seen = []

        def f(k, v):
            if v is not None and __pragma__("js", "{}", "typeof v == 'object'"):
                test = __pragma__("js", "{}", "seen.indexOf(v) >= 0")
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

    def initialize(self):
        if window.PhanterPWA.DEBUG:
            console.info("method not used: Handler.initialize")

    def widgets_initialize(self):
        for x in self.request.widgets.keys():
            self.request.widgets[x].start()


class ErrorHandler():
    def __init__(self, request, response=None):
        self._request = request
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


class Error_404(ErrorHandler):
    def start(self):
        html = html_base.jquery()
        html.find(".image-warnings").attr(
            "src", "/static/{0}/images/warning.png".format(window.PhanterPWA.VERSION))
        html.find("#content-warning").html("ERROR 404 - Not Found")
        jQuery("#main-container").html(html)


class Error_401(ErrorHandler):
    def start(self):
        html = html_base.jquery()
        html.find(".image-warnings").attr(
            "src", "/static/{0}/images/warning.png".format(window.PhanterPWA.VERSION))
        html.find("#content-warning").html("ERROR 401 - Unauthorized")
        jQuery("#main-container").html(html)


class Error_403(ErrorHandler):
    def start(self):
        html = html_base.jquery()
        html.find(".image-warnings").attr(
            "src", "/static/{0}/images/warning.png".format(window.PhanterPWA.VERSION))
        html.find("#content-warning").html("ERROR 403 - Forbidden")
        jQuery("#main-container").html(html)


class Error_502(ErrorHandler):
    def start(self):
        html = html_base.jquery()
        html.find(".image-warnings").attr(
            "src", "/static/{0}/images/warning.png".format(window.PhanterPWA.VERSION))
        html.find("#content-warning").html("ERROR 502 - Bad Gateway")
        jQuery("#main-container").html(html)


class Error_500(ErrorHandler):
    def start(self):
        html = html_base.jquery()
        html.find(".image-warnings").attr(
            "src", "/static/{0}/images/warning.png".format(window.PhanterPWA.VERSION))
        html.find("#content-warning").html("ERROR 500 - Internal Error")
        jQuery("#main-container").html(html)


__pragma__('nokwargs')
