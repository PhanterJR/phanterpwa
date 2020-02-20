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


class GateHandler():

    def __init__(self, request, **parameters):
        self._request = request
        self.debug = window.PhanterPWA.DEBUG
        self.requires_login = False
        self.autorized_roles = ["all"]
        self.autorized_ids = ["all"]
        self.way_on_back = window.PhanterPWA.get_current_way()
        self.on_status_code_error = None
        self.initialize()
        self._credentials = self.check_credentials()
        if self._credentials is True:
            self.request = request
            window.PhanterPWA.Response = self
            self.start()
            window.PhanterPWA.reload()
        else:
            if callable(self.on_status_code_error):
                self.on_status_code_error(self._credentials, self)
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

    def check_credentials(self):
        auth_user = window.PhanterPWA.get_auth_user()
        roles = []
        has_authentication = False
        if auth_user is not None:
            has_authentication = True
            roles = auth_user.roles
        if isinstance(self.autorized_roles, list) and isinstance(self.requires_login, bool):
            if self.requires_login is True and has_authentication:
                if "all" in self.autorized_roles and "all" in self.autorized_ids:
                    return True
                elif len(set(roles).intersection(set(self.autorized_roles))) > 0 and "all" in self.autorized_ids:
                    return True
                elif "all" in self.autorized_roles and int(auth_user.id) in self.autorized_ids:
                    return True
                elif len(set(roles).intersection(
                        set(self.autorized_roles))) > 0 and int(auth_user.id) in self.autorized_ids:
                    return True
                else:
                    return 403
            elif self.requires_login is True:
                return 401
            else:
                if "all" in self.autorized_roles and "all" in self.autorized_ids:
                    return True
                elif has_authentication:
                    if len(set(roles).intersection(set(self.autorized_roles))) > 0 and "all" in self.autorized_ids:
                        return True
                    elif "all" in self.autorized_roles and int(auth_user.id) in self.autorized_ids:
                        return True
                    elif len(set(roles).intersection(
                            set(self.autorized_roles))) > 0 and int(auth_user.id) in self.autorized_ids:
                        return True
                    else:
                        return 403
                elif "anonymous" in self.autorized_roles and "all" in self.autorized_ids:
                    if has_authentication:
                        return 403
                    else:
                        return True
                else:
                    return 401
        else:
            return 500

    def on_click_back_button(self):
        window.PhanterPWA.open_way(self.way_on_back)

    def _on_credentials_fail(self):
        window.PhanterPWA.open_code_way(self._credentials, self._request, self)

    def initialize(self):
        if window.PhanterPWA.DEBUG:
            console.info("method not used: RequestRouteHandler.initialize()")

    def start(self):
        if window.PhanterPWA.DEBUG:
            console.info("method not used: RequestRouteHandler.start()")


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
