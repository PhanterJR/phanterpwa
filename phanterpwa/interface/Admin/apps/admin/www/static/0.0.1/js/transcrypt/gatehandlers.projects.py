import phanterpwa.apptools.handler as handler
import phanterpwa.apptools.helpers as helpers
import phanterpwa.apptools.components.widgets as widgets
import phanterpwa.apptools.components.left_bar as left_bar
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


class Index(handler.GateHandler):
    def __init__(self, request):
        handler.GateHandler.__init__(self, request)
        self.projects_data = localStorage.getItem("admin_projects_data")

    def start(self):
        html = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV("DEVELOPMENT", _class="phanterpwa-breadcrumb"),
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
                        _id="projects_container"),
                    _class="card p-row e-padding_10"
                ),
                _class="phanterpwa-container p-container"
            )
        )
        html.html_to("#main-container")
        if self.request.get_arg(1) == "view":

            BackButton = left_bar.LeftBarButton(
                "back_developer",
                "Voltar",
                I(_class="fas fa-arrow-circle-left"),
                **{"_phanterpwa-way": "developer",
                    "position": "top",
                    "ways": [lambda: window.PhanterPWA.get_current_way().startswith("projects")]
                }
            )

            window.PhanterPWA.Components['left_bar'].add_button(BackButton)


    def _binds(self):
        jQuery("#phanterpwa-component-left_bar-menu_button-change_projects_folder").off(
            "click.change_projects_folder"
        ).on(
            "click.change_projects_folder",
            self.change_projects_folder,
        )

    def reload(self):
        self._binds()

    def change_projects_folder(self):
        admin_authorization = localStorage.getItem("admin_authorization")
        window.PhanterPWA.WS.onMessage = lambda ev: self._after_get_projects_folder(ev)
        window.PhanterPWA.WS.send({
            "authorization": admin_authorization, "command": "change_project_folder"
        })

    def _after_get_projects_folder(self, evt):
        str_json = JSON.parse(evt.data)
        if str_json.status == 200:
            window.PhanterPWA.open_way("developer")

    def _xml_projects_list(self, json):
        table = XTABLE(
            "projects-table",
            XTRH(
                "projects-table-head",
                *["Project Name", "Diretory"],
                DIV(
                    I(_class="fas fa-plus"),
                    **{
                        "_phanterpwa-way": "project/novo",
                        "_class": "icon_button wave_on_click"
                    }
                )
            )
        )
        for x in json.projects_list:
            table.append(
                XTRD(
                    "projects-table-data-{0}".format(x[0]),
                    x[0],
                    x[1],
                    widgets.MenuBox(
                        "drop_{0}".format(x[0]),
                        xml_menu=UL(
                            LI("View", **{
                                "_class": "botao_editar_role",
                                "_phanterpwa-way": "project/{0}/view".format(x[0])
                            }),
                            LI("Delete", **{
                                "_class": "botao_editar_role",
                                "_phanterpwa-way": "project/{0}/delete".format(x[0])
                            }),
                            **{"data-menubox": "drop_{0}".format(x[0]),
                            "_class": 'dropdown-content'},
                        )
                    )
                )
            )
        html = DIV(
            XSECTION(
                LABEL("Enviroment"),
                DIV(
                    DIV(
                        DIV(
                            DIV(
                                STRONG("PYTHON EXECUTABLE"),
                                SPAN(json.enviroment.python_executable),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p100"
                        ),
                        _class="p-row"
                    ),
                    DIV(
                        DIV(
                            DIV(
                                STRONG("PYTHON PATH"),
                                SPAN(json.enviroment.python_path),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p100"
                        ),
                        _class="p-row"
                    ),
                    DIV(
                        DIV(
                            DIV(
                                STRONG("PYTHON VERSION"),
                                SPAN(json.enviroment.python_version),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p50"
                        ),
                        DIV(
                            DIV(
                                STRONG("PHANTERPWA VERSION"),
                                SPAN(json.enviroment.phanterpwa_version),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p50"
                        ),
                        _class="p-row"
                    ),
                    DIV(
                        DIV(
                            DIV(
                                STRONG("PROJECTS FOLDER"),
                                SPAN(json.enviroment.projects_folder),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p100"
                        ),
                        _class="p-row"
                    ),
                    _class="e-padding_20"
                )
            ),
            table
        )
        html.html_to("#projects_container")

    def _after_get_applications(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            if data.status == 200:
                localStorage.setItem("admin_projects_data", JSON.stringify(json))
                self.admin_projects_data = json
                window.PhanterPWA.flash(**{'html': json.i18n.message})

                self._xml_projects_list(json)

            elif data.status == 202:
                window.PhanterPWA.flash(**{'html': json.i18n.message})
            localStorage.setItem("admin_authorization", json.authorization)
            self.admin_authorization = json.authorization
            self._binds()
        else:
            window.PhanterPWA.flash("Problem on server: {0}".format(str(data.status)))


__pragma__('nokwargs')
