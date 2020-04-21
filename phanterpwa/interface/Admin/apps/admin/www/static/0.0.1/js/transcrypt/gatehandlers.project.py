import phanterpwa.apptools.gatehandler as gatehandler
import phanterpwa.apptools.helpers as helpers
import phanterpwa.apptools.forms as forms
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
FORM = helpers.XmlConstructor.tagger("form")
LABEL = helpers.XmlConstructor.tagger("label")
HR = helpers.XmlConstructor.tagger("hr", True)
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
        self.projects_data = localStorage.getItem("admin_projects_data")

    def initialize(self):
        html = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV("PROJECT", _class="phanterpwa-breadcrumb"),
                        DIV(self.request.get_arg(0), _class="phanterpwa-breadcrumb"),
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
                        _id="applications_container"),
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
                "ways": [lambda: window.PhanterPWA.get_current_way().startswith("project")]
            }
        )
        window.PhanterPWA.Components['left_bar'].add_button(BackButton)
        if self.request.get_arg(1) == "view":

            ConfigProject = left_bar.LeftBarButton(
                "config_project",
                "Configurar Projeto e Api",
                I(_class="fas fa-tools"),
                **{
                    "_phanterpwa-way": "project/{0}/config".format(self.request.get_arg(0)),
                    "position": "top",
                    "ways": [lambda: window.PhanterPWA.get_current_way().startswith("project")]
                }
            )
            window.PhanterPWA.Components['left_bar'].add_button(ConfigProject)
            window.PhanterPWA.GET(**{
                'url_args': ['api', 'projects', self.request.get_arg(0)],
                'onComplete': self._after_get_applications
            })
        elif self.request.get_arg(1) == "config":
            window.PhanterPWA.GET(**{
                'url_args': ['api', 'config', self.request.get_arg(0)],
                'onComplete': self._after_get_config
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

    def _bind_open_api(self, app_name, url):

        jQuery("#phanterpwa-component-left_bar-menu_button-view_api").off(
            "click.open_href_play"
        ).on(
            "click.open_href_play",
            lambda: window.open(url, "_blank")
        )

    def _xml_projects_list(self, json):
        table = XTABLE(
            "applications-table",
            XTRH(
                "applications-table-head",
                *["Application Name", "Build Folder"],
                DIV(
                    I(_class="fas fa-plus"),
                    **{
                        "_phanterpwa-way": "application/new",
                        "_class": "icon_button wave_on_click"
                    }
                )
            )
        )
        apps_dict = dict(json.config.APPS)
        for x in apps_dict.keys():
            table.append(
                XTRD(
                    "applications-table-data-{0}".format(x),
                    x,
                    apps_dict[x]["build_folder"],
                    widgets.MenuBox(
                        "drop_2_{0}".format(x),
                        xml_menu=UL(
                            LI("Compile", **{
                                "_id": "btn_compile_app_project_{0}".format(x),
                                "_class": "btn_compile_app_project",
                                "_data-path": json.config['PROJECT']['path'],
                                "_data-app": x
                            }),
                            LI("View", **{
                                "_class": "botao_editar_role",
                                "_phanterpwa-way": "application/{0}/view".format(x)
                            }),
                            LI("Delete", **{
                                "_class": "botao_editar_role",
                                "_phanterpwa-way": "application/{0}/delete".format(x)
                            }),
                            **{
                                "data-menubox": "drop_2_{0}".format(x),
                                "_class": 'dropdown-content'
                            },
                        )
                    )
                )
            )
        if json.config.PROJECT.debug:
            url = json.config.API.remote_address_on_development
        else:
            url = json.config.API.remote_address_on_production
        ShowApi = left_bar.LeftBarButton(
            "view_api",
            "Open Api",
            I(_class="fas fa-globe"),
            **{
                "position": "top",
                "ways": [lambda: True if json.running is True and
                    window.PhanterPWA.get_current_way().startswith("project/{0}".format(self.request.get_arg(0))) else False],
                "onStart": lambda: self._bind_open_api(self.request.get_arg(0), url)
            }
        )
        window.PhanterPWA.Components['left_bar'].add_button(ShowApi)

        html = DIV(
            XSECTION(
                LABEL("Summary"),
                DIV(
                    DIV(
                        DIV(
                            DIV(
                                STRONG("PROJECT PATH"),
                                SPAN(json.config['PROJECT']['path']),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p100"
                        ),
                        _class="p-row"
                    ),
                    DIV(
                        DIV(
                            DIV(
                                STRONG("IDENTIFIER NAME"),
                                SPAN(json.config['PROJECT']['name']),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p100"
                        ),
                        _class="p-row"
                    ),
                    DIV(
                        DIV(
                            DIV(
                                STRONG("TITLE"),
                                SPAN(json.config['PROJECT']['title']),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p100"
                        ),
                        _class="p-row"
                    ),
                    DIV(
                        DIV(
                            DIV(
                                STRONG("AUTHOR"),
                                SPAN(json.config['PROJECT']['author']),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p100"
                        ),
                        _class="p-row"
                    ),
                    DIV(
                        DIV(
                            DIV(
                                STRONG("VERSION"),
                                SPAN(json.config['PROJECT']['version']),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p100 w3p50"
                        ),
                        DIV(
                            DIV(
                                STRONG("COMPILATION"),
                                SPAN(json.config['PROJECT']['compilation']),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p100 w3p50"
                        ),
                        _class="p-row"
                    ),
                    DIV(
                        DIV(
                            DIV(
                                STRONG("DEBUG"),
                                SPAN(json.config['PROJECT']['debug']),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p100 w3p50"
                        ),
                        DIV(
                            DIV(
                                STRONG("STATUS"),
                                SPAN("Running" if json.running else "Stopped", _style="color: {0};".format(
                                    "green" if json.running else "red")),
                                _class="e-tagger-wrapper"
                            ),
                            _class="p-col w1p100 w3p50"
                        ),
                        _class="p-row"
                    ),
                    _class="e-padding_20"
                )
            ),
            table
        )
        html.html_to("#applications_container")

    def _xml_config_project(self, json):
        project_config = dict(json.project_config['PROJECT'])
        email_config = dict(json.project_config['EMAIL'])
        email_contents_config = dict(json.project_config['CONTENT_EMAILS'])
        api_config = dict(json.api_config['API'])
        project_default = [
            "title",
            "version",
            "author",
            "debug",
            "packaged"
        ]
        email_secret_default = [
            "password"
        ]
        email_default = [
            "server",
            "username",
            "default_sender",
            "port",
            "use_tls",
            "use_ssl"
        ]
        content_email_default = [
            "copyright",
            "link_to_your_site"
        ]
        html = FORM(H2("PROJECT"), HR(), **{"_phanterpwa-form": "config_project"})
        for x in project_config.keys():
            if x == "debug" or x == "packaged":
                html.append(widgets.CheckBox("project_{0}".format(x), **{
                    "value": project_config[x],
                    "name": x,
                    "label": x.replace("_", " ").capitalize(),
                    "form": "config_project"
                }))
            else:
                html.append(widgets.Input("project_{0}".format(x), **{
                    "value": project_config[x],
                    "name": x,
                    "label": x.replace("_", " ").capitalize(),
                    "form": "config_project"
                }))
        html.append(CONCATENATE(H2("EMAIL"), HR()))
        for x in email_config.keys():
            if x == "use_tls" or x == "use_ssl":
                html.append(widgets.CheckBox("emai_{0}".format(x), **{
                    "value": email_config[x],
                    "name": x,
                    "label": x.replace("_", " ").capitalize(),
                    "form": "config_project"
                }))
            else:
                html.append(widgets.Input("emai_{0}".format(x), **{
                    "value": email_config[x],
                    "name": x,
                    "label": x.replace("_", " ").capitalize(),
                    "form": "config_project"
                }))
        html.append(CONCATENATE(H2("CONTENT EMAILS"), HR()))
        for x in email_contents_config.keys():
            html.append(widgets.Input("content_emails_{0}".format(x), **{
                "value": email_contents_config[x],
                "name": x,
                "label": x.replace("_", " ").capitalize(),
                "form": "config_project"
            }))
        html.append(CONCATENATE(H2("API"), HR()))
        for x in api_config.keys():
            if x == "secret_key" or x == "url_secret_key":
                html.append(widgets.Input("api_{0}".format(x), **{
                    "value": api_config[x],
                    "name": x,
                    "label": x.replace("_", " ").capitalize(),
                    "form": "config_project",
                    "icon": I(_class="fab fa-sistrix"),
                    "icon_on_click": lambda: window.PhanterPWA.flash(**{"html": I18N("Fui Clicado!")})
                }))
            else:
                html.append(widgets.Input("api_{0}".format(x), **{
                    "value": api_config[x],
                    "name": x,
                    "label": x.replace("_", " ").capitalize(),
                    "form": "config_project"
                }))
        html.append(forms.SubmitButton("config_project", "Save Config"))
        html.html_to("#applications_container")

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

    def _after_get_config(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            if data.status == 200:
                window.PhanterPWA.flash(**{'html': json.i18n.message})
                self._xml_config_project(json)

        else:
            window.PhanterPWA.flash("Problem on server: {0}".format(str(data.status)))


__pragma__('nokwargs')
