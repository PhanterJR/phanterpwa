import phanterpwa.frontend.gatehandler as gatehandler
import phanterpwa.frontend.helpers as helpers
import phanterpwa.frontend.components.widgets as widgets
import phanterpwa.frontend.components.left_bar as left_bar
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
XTABLE = widgets.Table
XML = helpers.XML
XTRD = widgets.TableData
XTRH = widgets.TableHead
XFOOTER = widgets.TableFooterPagination


__pragma__('kwargs')


class Index(gatehandler.Handler):
    def __init__(self, request):
        gatehandler.Handler.__init__(self, request)
        self.admin_authorization = localStorage.getItem("admin_authorization")

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
                            widgets.Preloaders("preload_android"),
                            _style="width:100%; text-align: center; padding-top: 100px; padding-bottom: 100px;"
                        ),
                        _id="requeriments_container"),
                    _class="card p-row e-padding_10"
                ),
                _class="phanterpwa-container p-container"
            )
        )
        html.html_to("#main-container")
        BackButton = left_bar.LeftBarButton(
            "back_developer",
            "Voltar",
            I(_class="fas fa-arrow-circle-left"),
            **{
                "_phanterpwa-way": "developer",
                "position": "top",
                "ways": [lambda: window.PhanterPWA.get_current_way().startswith("check_requeriments")]
            }
        )
        window.PhanterPWA.Components['left_bar'].add_button(BackButton)
        window.PhanterPWA.GET(**{
            'url_args': ['api', 'automation', 'requeriment_list'],
            'onComplete': self._after_get_requeriment_list
        })

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

    def _xml_requeriment_list(self, json):
        table = XTABLE(
            "requeriments-table",
            XTRH(
                "requeriments-table-head",
                *["Requeriment", "status"]
            )
        )
        for x in json.requeriment_list:
            if ">" in x or "<" in x or "=" in x:
                x = x.split(">")[0]
                x = x.split("=")[0]
                x = x.split("<")[0]
            table.append(
                XTRD(
                    "requeriments-table-data-{0}".format(x),
                    x.capitalize(),
                    DIV(
                        SPAN("Cheking...", _style="color: orange;"),
                        **{
                            "_data-test": x,
                            "_class": "requeriments_phanterpwa_status"
                        }
                    ),
                )
            )

        table.html_to("#requeriments_container")
        window.PhanterPWA.WS.onMessage = lambda ev: self._onwsmessage(ev)
        window.PhanterPWA.WS.send({
            "authorization": self.admin_authorization,
            "command": "requeriments_phanterpwa"
        })

    def _onwsmessage(self, ev):
        json = JSON.parse(ev.data)
        if json.command == "requeriments_phanterpwa":
            if json.status == 206:
                jQuery(".requeriments_phanterpwa_status[data-test='{0}']".format(json.check)).html(
                    "<span style='color: green'>PASS</span>" if json.result else "<span style='color: red'>FAIL</span>"
                )
            elif json.status == 200:
                window.PhanterPWA.flash("Test finished!")

    def _after_get_requeriment_list(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            if data.status == 200:
                window.PhanterPWA.flash(**{'html': json.i18n.message})
                self._xml_requeriment_list(json)
            self._binds()
        else:
            window.PhanterPWA.flash("Problem on server: {0}".format(str(data.status)))


__pragma__('nokwargs')
