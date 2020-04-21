import phanterpwa.apptools.handler as handler
import phanterpwa.apptools.helpers as helpers
import phanterpwa.apptools.forms as forms
import phanterpwa.apptools.preloaders as preloaders
from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = window = 0
__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")
FORM = helpers.XmlConstructor.tagger("form")
SPAN = helpers.XmlConstructor.tagger("span")
IMG = helpers.XmlConstructor.tagger("img", True)
I = helpers.XmlConstructor.tagger("I")
I18N = helpers.I18N
CONCATENATE = helpers.CONCATENATE
H3 = helpers.XmlConstructor.tagger("h3")

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
                        IMG(
                            _class='image-warnings'
                        ),
                        _class="image-warnings-container"
                    ),
                    DIV(_id='content-warning'),
                    _class='content-warnings'
                ),
                _class='warnings-container phanterpwa-card-container card'
            ),
            _class="new-container"
        ),
        _class="phanterpwa-container container"
    )
)


class Error_404(handler.ErrorHandler):
    def start(self):
        html = html_base.jquery()
        html.find(".image-warnings").attr(
            "src", "/static/{0}/images/warning.png".format(window.PhanterPWA.VERSION))
        html.find("#content-warning").html("ERROR 404")
        jQuery("#main-container").html(html)


class Error_401(handler.ErrorHandler):
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
                                    _src="/static/{0}/images/warning.png".format(window.PhanterPWA.VERSION)
                                ),
                            ),
                            _class="image-warnings-container"
                        ),
                        DIV(
                            I18N(
                                "You need authentication to access this feature.",
                                **{
                                    "_pt-br": "Você precisa autenticar-se para tentar acessar este recurso."
                                }
                            ),
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



class Error_403(handler.ErrorHandler):
    def start(self):
        html = html_base.jquery()
        html.find(".image-warnings").attr(
            "src", "/static/{0}/images/warning.png".format(window.PhanterPWA.VERSION))
        html.find("#content-warning").html("ERROR 403")
        jQuery("#main-container").html(html)