import phanterpwa.frontend.gatehandler as gatehandler
import phanterpwa.frontend.helpers as helpers

from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = M = js_undefined = window = setTimeout = \
    __new__ = FormData = console = localStorage = document = this = 0
__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")
I = helpers.XmlConstructor.tagger("i")
H1 = helpers.XmlConstructor.tagger("h1")
H2 = helpers.XmlConstructor.tagger("h2")
H3 = helpers.XmlConstructor.tagger("h3")
STRONG = helpers.XmlConstructor.tagger("strong")
SPAN = helpers.XmlConstructor.tagger("span")
A = helpers.XmlConstructor.tagger("a")
UL = helpers.XmlConstructor.tagger("ul")
LI = helpers.XmlConstructor.tagger("li")
LABEL = helpers.XmlConstructor.tagger("label")
XSECTION = helpers.XSECTION
I18N = helpers.I18N
CONCATENATE = helpers.CONCATENATE


__pragma__('kwargs')


class Index(gatehandler.Handler):
    def __init__(self, request):
        gatehandler.Handler.__init__(self, request)

    def initialize(self):
        html = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV("TEST REQUERIMENTS", _class="phanterpwa-breadcrumb"),
                        _class="phanterpwa-breadcrumb-wrapper"
                    ),
                    _class="p-container"),
                _class='title_page_container card'
            ),
            DIV(
                DIV(
                    DIV(
                        DIV(
                            _style="width:100%; text-align: center; padding-top: 100px; padding-bottom: 100px;"
                        ),
                        _id="requeriments_container"),
                    _class="card p-row e-padding_10"
                ),
                _class="phanterpwa-container p-container"
            )
        )
        html.html_to("#main-container")

    def _binds(self):
        jQuery("#phanterpwa-component-left_bar-menu_button-change_projects_folder").off(
            "click.change_projects_folder"
        ).on(
            "click.change_projects_folder",
            self.change_projects_folder,
        )

    def reload(self):
        self._binds()

    def _bind_open_api(self, app_name, url):

        jQuery("#phanterpwa-component-left_bar-menu_button-view_api").off(
            "click.open_href_play"
        ).on(
            "click.open_href_play",
            lambda: window.open(url, "_blank")
        )



__pragma__('nokwargs')
