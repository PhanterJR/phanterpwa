import phanterpwa.frontend.gatehandler as gatehandler
import phanterpwa.frontend.decorators as decorators
import phanterpwa.frontend.helpers as helpers
import phanterpwa.frontend.components.left_bar as left_bar
import phanterpwa.frontend.preloaders as preloaders
import phanterpwa.frontend.components.widgets as widgets
import phanterpwa.frontend.forms as forms
from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = M = js_undefined = window = setTimeout = document = console = this = \
    __new__ = FormData = console = localStorage = 0
__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")
I = helpers.XmlConstructor.tagger("i")
H2 = helpers.XmlConstructor.tagger("h2")
FORM = helpers.XmlConstructor.tagger("form")
SPAN = helpers.XmlConstructor.tagger("span")
IMG = helpers.XmlConstructor.tagger("img", True)
INPUT = helpers.XmlConstructor.tagger("input", True)
A = helpers.XmlConstructor.tagger("A")
OPTION = helpers.XmlConstructor.tagger("option")
SELECT = helpers.XmlConstructor.tagger("select")
UL = helpers.XmlConstructor.tagger("ul")
LI = helpers.XmlConstructor.tagger("li")
STRONG = helpers.XmlConstructor.tagger("strong")
XTABLE = widgets.Table
XML = helpers.XML
XTRD = widgets.TableData
XTRH = widgets.TableHead
XFOOTER = widgets.TableFooterPagination
I18N = helpers.I18N
CONCATENATE = helpers.CONCATENATE

__pragma__('kwargs')

class Administration(gatehandler.Handler):

    @decorators.check_authorization(lambda: window.PhanterPWA.auth_user_has_role("root"))
    def initialize(self):
        self.auth_user = window.PhanterPWA.get_last_auth_user()
        arg = self.request.get_arg(0)
        arg1 = self.request.get_arg(1)
        arg2 = self.request.get_arg(2)
        if arg == "users":
            html = CONCATENATE(
                DIV(
                    DIV(
                        DIV(
                            DIV("USERS", _class="phanterpwa-breadcrumb"),
                            _class="phanterpwa-breadcrumb-wrapper"
                        ),
                        _class="p-container"),
                    _class='title_page_container card'
                ),
                DIV(
                    DIV(
                        DIV(
                            DIV(preloaders.android, _style="width: 300px; height: 300px; overflow: hidden; margin: auto;"),
                            _style="text-align:center; padding: 50px 0;"
                        ),
                        _id="content-users",
                        _class='p-row card e-padding_20'
                    ),

                    _class="phanterpwa-container p-container"
                )
            )
            html.html_to("#main-container")
            if arg1 == "new":
                BackButton = left_bar.LeftBarButton(
                    "back_admin_user",
                    "Voltar",
                    I(_class="fas fa-arrow-circle-left"),
                    **{"_phanterpwa-way": "admin/users",
                        "position": "top",
                        "show_if": lambda: True if window.PhanterPWA.get_current_way() == "admin/users/new"
                            and window.PhanterPWA.auth_user_has_role("root") else False
                    }
                )

                window.PhanterPWA.Components['left_bar'].add_button(BackButton)
                self.User = User(self, "new")
            elif arg2 == "edit" and str(arg1).isdigit():
                BackButton = left_bar.LeftBarButton(
                    "back_admin_user_edit",
                    "Voltar",
                    I(_class="fas fa-arrow-circle-left"),
                    **{"_phanterpwa-way": "admin/users",
                        "position": "top",
                        "show_if": lambda: True if window.PhanterPWA.get_current_way() == "admin/users/{0}/edit".format(arg1)
                            and window.PhanterPWA.auth_user_has_role("root") else False
                    }
                )

                window.PhanterPWA.Components['left_bar'].add_button(BackButton)
                self.User = User(self, arg1, arg2)
            elif arg2 == "impersonate" and str(arg1).isdigit():
                BackButton = left_bar.LeftBarButton(
                    "back_admin_user_edit",
                    "Voltar",
                    I(_class="fas fa-arrow-circle-left"),
                    **{"_phanterpwa-way": "admin/users",
                        "position": "top",
                        "show_if": lambda: True if window.PhanterPWA.get_current_way() == "admin/users/{0}/edit".format(arg1)
                            and window.PhanterPWA.auth_user_has_role("root") else False
                    }
                )

                window.PhanterPWA.Components['left_bar'].add_button(BackButton)
                self.Impersonate = Impersonate(self, arg1, arg2)
            elif arg2 == "delete" and str(arg1).isdigit():
                self.User = User(self, arg1, arg2)
            else:
                BackButton = left_bar.LeftBarButton(
                    "back_admin",
                    "Voltar",
                    I(_class="fas fa-arrow-circle-left"),
                    **{"_phanterpwa-way": "admin",
                        "position": "top",
                        "show_if": lambda: True if window.PhanterPWA.get_current_way() == "admin/users"
                            and window.PhanterPWA.auth_user_has_role("root") else False
                    }
                )

                window.PhanterPWA.Components['left_bar'].add_button(BackButton)
                self.UsersList = UsersList(self)

        elif arg == "roles":
            html = CONCATENATE(
                DIV(
                    DIV(
                        DIV(
                            DIV("ROLES", _class="phanterpwa-breadcrumb"),
                            _class="phanterpwa-breadcrumb-wrapper"
                        ),
                        _class="p-container"),
                    _class='title_page_container card'
                ),
                DIV(
                    DIV(
                        DIV(
                            DIV(preloaders.android, _style="width: 300px; height: 300px; overflow: hidden; margin: auto;"),
                            _style="text-align:center; padding: 50px 0;"
                        ),
                        _id="content-roles",
                        _class='p-row card e-padding_20'
                    ),

                    _class="phanterpwa-container p-container"
                )
            )
            html.html_to("#main-container")
            if arg1 == "new":
                BackButton = left_bar.LeftBarButton(
                    "back_admin_user",
                    "Voltar",
                    I(_class="fas fa-arrow-circle-left"),
                    **{"_phanterpwa-way": "admin/users",
                        "position": "top",
                        "show_if": lambda: True if window.PhanterPWA.get_current_way() == "admin/users/new"
                            and window.PhanterPWA.auth_user_has_role("root") else False
                    }
                )

                window.PhanterPWA.Components['left_bar'].add_button(BackButton)
                self.Role = Role(self, "new")

            elif arg2 == "edit" and str(arg1).isdigit():
                BackButton = left_bar.LeftBarButton(
                    "back_admin_user_edit",
                    "Voltar",
                    I(_class="fas fa-arrow-circle-left"),
                    **{"_phanterpwa-way": "admin/users",
                        "position": "top",
                        "show_if": lambda: True if window.PhanterPWA.get_current_way() == "admin/users/{0}/edit".format(arg1)
                            and window.PhanterPWA.auth_user_has_role("root") else False
                    }
                )

                window.PhanterPWA.Components['left_bar'].add_button(BackButton)
                self.Role = Role(self, arg1, arg2)

            else:
                BackButton = left_bar.LeftBarButton(
                    "back_localizar_roles",
                    "Voltar",
                    I(_class="fas fa-arrow-circle-left"),
                    **{"_phanterpwa-way": "admin",
                        "position": "top",
                        "show_if": lambda: True if window.PhanterPWA.get_current_way() == "admin/roles"
                            and window.PhanterPWA.auth_user_has_role("root") else False
                    }
                )

                window.PhanterPWA.Components['left_bar'].add_button(BackButton)
                self.RolesList = RolesList(self)

        else:

            html = CONCATENATE(
                DIV(
                    DIV(
                        DIV(
                            DIV("USERS ADMINISTRATION", _class="phanterpwa-breadcrumb"),
                            _class="phanterpwa-breadcrumb-wrapper"
                        ),
                        _class="p-container"),
                    _class='title_page_container card'
                ),
                DIV(
                    DIV(
                        DIV(
                            DIV(
                                DIV(
                                    I(
                                        **{
                                            "_class": "fas fa-user-cog promo-icon",
                                        }
                                    ),
                                    H2("USERS", _class="promo-title"),
                                    **{
                                        "_class": "link",
                                        "_phanterpwa-way": "admin/users"
                                    }
                                ),
                                DIV(
                                    I18N(
                                        "Users Administration",
                                        **{"_pt-br": "Administração de Usuários"}
                                    ),
                                    _class='promo-content'
                                ),
                                **{"_class": "promo-container"}
                            ),
                            _class='p-col w1p100 w3p50 w4p25'
                        ),
                        DIV(
                            DIV(
                                DIV(
                                    I(
                                        **{
                                            "_class": "fas fa-user-tag promo-icon",
                                        }
                                    ),
                                    H2("ROLES", _class="promo-title"),
                                    **{
                                        "_class": "link",
                                        "_phanterpwa-way": "admin/roles"
                                    }
                                ),
                                DIV("Roles users Administration", _class='promo-content'),
                                **{"_class": "promo-container"}
                            ),
                            _class='p-col w1p100 w3p50 w4p25'
                        ),
                        _class='p-row card e-padding_20'
                    ),

                    _class="phanterpwa-container p-container"
                )
            )
            html.html_to("#main-container")


class UsersList(helpers.XmlConstructor):
    """way: users"""

    def __init__(self, index_instance):
        self.index_instance = index_instance
        html = DIV(
            DIV(
                FORM(
                    DIV(
                        DIV(
                            DIV(
                                widgets.Input(
                                    "search_users",
                                    label="Search Email",
                                    placeholder="Email",
                                    icon=I(_class="fab fa-sistrix"),
                                    icon_on_click=lambda: self.search()
                                ),
                                _class="p-col w1p100 w3p50 w4p75",
                            ),
                            DIV(
                                widgets.Select(
                                    "users_field",
                                    label="Search Fields",
                                    placeholder="Choice a Field",
                                    value="email",
                                    data_set=[
                                        ["id", "ID"],
                                        ["first_name", "First Name"],
                                        ["last_name", "Last Name"],
                                        ['email', "E-mail"],
                                        ["permit_mult_login", "Allows Multiple Logins"],
                                        ["activated", "Activated"],
                                        ["online", "Online"]
                                    ]
                                ),
                                _id="phanterpwa-input-search_field",
                                _class="p-col w1p100 w3p50 w4p25"
                            ),
                            _class="p-row e-padding_20w"
                        ),
                        _class="phanterpwa-container-section"
                    ),
                    _action="#",
                    _id="search_users",
                    _class="form-search_users",
                    _enctype="multipart/form-data",
                    _method="post",
                    _autocomplete="off"
                ),
                _class="phanterpwa_tables_search_wrapper"
            ),
            DIV(_id='lista-users-subtitle', _class="phanterpwa-subtitle"),
            DIV(
                DIV(
                    DIV(preloaders.android, _style="width: 300px; height: 300px; overflow: hidden; margin: auto;"),
                    _style="text-align:center; padding: 50px 0;"
                ),
                _id='lista-users-container',
                _class="phanterpwa_tables_container"
            ),
            _class='users-container phanterpwa-card-container'
        )
        helpers.XmlConstructor.__init__(self, "div", False, html, _class="lista_de_users")
        self.html_to("#content-users")
        self._get_data_search(orderby="id")

    def after_get(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            if json.users is None:
                window.PhanterPWA.open_way("/users/new")
            else:
                self.process_data(json)

    def _on_sort(self, table_head_instance):
        widgets = window.PhanterPWA.Request.widgets
        page = widgets["users-table-footer"].page()
        search = widgets["search_users"].value()
        field = widgets["users_field"].value()
        sorted_field = widgets["users-table-head"].sorted_field()
        self._get_data_search(search=search, field=field, orderby=sorted_field[0], sort=sorted_field[1], page=page)

    def _on_page(self, table_pagination_instance):
        widgets = window.PhanterPWA.Request.widgets
        page = widgets["users-table-footer"].page()
        search = widgets["search_users"].value()
        field = widgets["users_field"].value()
        sorted_field = widgets["users-table-head"].sorted_field()
        self._get_data_search(search=search, field=field, orderby=sorted_field[0], sort=sorted_field[1], page=page)

    def process_data(self, json):
        if self.current_hash is not json.hash:
            self.current_hash = json.hash
            users = json.users
            jQuery("#lista-users-subtitle").text(json.message)
            new_select_widget = widgets.Select(
                "users_field",
                label=users.search_fields.label,
                placeholder="Choose a Field ",
                value=users.search_fields.value,
                data_set=users.search_fields.data_set
            )
            new_select_widget.html_to("#phanterpwa-input-search_field")
            new_select_widget.reload()
            table = XTABLE(
                "users-table",
                XTRH(
                    "users-table-head",
                    *users.searcher.data_set,
                    DIV(
                        I(_class="fas fa-plus"),
                        **{
                            "_phanterpwa-way": "admin/users/new",
                            "_class": "icon_button wave_on_click"
                        }
                    ),
                    sort_by=users.searcher.sort_by,
                    sort_order=users.searcher.sort_order,
                    sortable=users.searcher.sortable,
                    on_click_sortable=self._on_sort,
                )
            )
            if users.data is not js_undefined:
                for x in users.data:
                    table.append(
                        XTRD(
                            "users-table-data-{0}".format(x.id),
                            x.id,
                            x.first_name,
                            x.last_name,
                            x.email,
                            I(_class="fas fa-check-circle", _style="color:green;") if x.permit_mult_login else I(_class="fas fa-times-circle", _style="color: red;"),
                            I(_class="fas fa-check-circle", _style="color:green;") if x.activated else I(_class="fas fa-times-circle", _style="color: red;"),
                            I(_class="fas fa-check-circle", _style="color:green;") if x.websocket_opened else I(_class="fas fa-times-circle", _style="color: red;"),
                            widgets.MenuBox(
                                "drop_{0}".format(x.id),
                                I(_class="fas fa-ellipsis-v"),
                                widgets.MenuOption("View", **{
                                    "_class": "admin-button-user-edit wave_on_click",
                                    "_href": "#_phanterpwa:/admin/users/{0}/view".format(x.id)
                                }),
                                widgets.MenuOption("Edit", **{
                                    "_class": "admin-button-user-edit wave_on_click",
                                    "_href": "#_phanterpwa:/admin/users/{0}/edit".format(x.id)
                                }),
                                widgets.MenuOption("Impersonate", **{
                                    "_class": "admin-button-user-edit wave_on_click",
                                    "_href": "#_phanterpwa:/admin/users/{0}/impersonate".format(x.id)
                                }),
                                widgets.MenuOption("Delete", **{
                                    "_class": "admin-button-user-edit wave_on_click",
                                    "_href": "#_phanterpwa:/admin/users/{0}/delete".format(x.id)
                                }),
                            )
                        )
                    )
                table.append(
                    XFOOTER(
                        "users-table-footer",
                        page=users.searcher.page,
                        total_pages=users.searcher.total_pages,
                        on_click_page=self._on_page,
                    )
                )

            table.html_to("#lista-users-container")


            def change_attr_drop(el):
                targ = jQuery(el).attr("phanterpwa_dowpdown_target")
                jQuery(el).attr("data-target", targ)
                # jQuery(el).dropdown()

            jQuery("[phanterpwa_dowpdown_target]").each(lambda: change_attr_drop(this))

    def _get_data_search(self, search="", field="email", orderby="email", sort="asc", page=1):
        window.PhanterPWA.ApiServer.GET(**{
            'url_args': ["api", "admin", "usermanager"],
            'url_vars': {
                "search": search,
                "field": field,
                "orderby": orderby,
                "sort": sort,
                "page": page
            },
            'onComplete': self.after_get,
            'get_cache': self.process_data
        })

    def search(self):
        widgets = window.PhanterPWA.Request.widgets
        search = widgets["search_users"].value()
        field = widgets["users_field"].value()
        self._get_data_search(search=search, field=field, orderby=field, sort="asc", page=1)


class RolesList(helpers.XmlConstructor):
    """way: users"""

    def __init__(self, index_instance):
        self.index_instance = index_instance
        html = DIV(
            DIV(
                FORM(
                    DIV(
                        DIV(
                            DIV(
                                widgets.Input(
                                    "search_roles",
                                    label="Search Role",
                                    placeholder="Role",
                                    icon=I(_class="fab fa-sistrix"),
                                    icon_on_click=lambda: self.search()
                                ),
                                _class="p-col w1p100 w3p50 w4p75",
                            ),
                            DIV(
                                widgets.Select(
                                    "campos_roles",
                                    label="Search Fields",
                                    placeholder="Choice a Field",
                                    value="role",
                                    data_set=[
                                        ["id", "ID"],
                                        ["grade", "Grade"],
                                        ["role", "Role"],
                                        ["description", "Description"]
                                    ]
                                ),
                                _id="phanterpwa-input-search_field",
                                _class="p-col w1p100 w3p50 w4p25"
                            ),
                            _class="p-row e-padding_20w"
                        ),
                        _class="phanterpwa-container-section"
                    ),
                    _action="#",
                    _id="search_roles",
                    _class="form-search_roles",
                    _enctype="multipart/form-data",
                    _method="post",
                    _autocomplete="off"
                ),
                _class="phanterpwa_tables_search_wrapper"
            ),
            DIV(_id='lista-roles-subtitle', _class="phanterpwa-subtitle"),
            DIV(
                DIV(
                    DIV(preloaders.android, _style="width: 300px; height: 300px; overflow: hidden; margin: auto;"),
                    _style="text-align:center; padding: 50px 0;"
                ),
                _id='lista-roles-container',
                _class="phanterpwa_tables_container"
            ),
            _class='roles-container phanterpwa-card-container'
        )
        helpers.XmlConstructor.__init__(self, "div", False, html, _class="lista_de_roles")
        self.html_to("#content-roles")
        self._get_data_search()

    def after_get(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            if json.roles is None:
                window.PhanterPWA.open_way("/roles/new")
            else:
                self.process_data(json)

    def _on_sort(self, table_head_instance):
        widgets = window.PhanterPWA.Request.widgets
        page = widgets["roles-table-footer"].page()
        search = widgets["search_roles"].value()
        field = widgets["campos_roles"].value()
        sorted_field = widgets["roles-table-head"].sorted_field()
        self._get_data_search(search=search, field=field, orderby=sorted_field[0], sort=sorted_field[1], page=page)

    def _on_page(self, table_pagination_instance):
        widgets = window.PhanterPWA.Request.widgets
        page = widgets["roles-table-footer"].page()
        search = widgets["search_roles"].value()
        field = widgets["campos_roles"].value()
        sorted_field = widgets["roles-table-head"].sorted_field()
        self._get_data_search(search=search, field=field, orderby=sorted_field[0], sort=sorted_field[1], page=page)

    def process_data(self, json):
        if self.current_hash is not json.hash:
            self.current_hash = json.hash
            roles = json.groups
            jQuery("#lista-roles-subtitle").text(json.message)
            new_select_widget = widgets.Select(
                "campos_roles",
                label=roles.search_fields.label,
                placeholder="Escolha o Campo",
                value=roles.search_fields.value,
                data_set=roles.search_fields.data_set
            )
            new_select_widget.html_to("#phanterpwa-input-search_field")
            new_select_widget.reload()
            table = XTABLE(
                "roles-table",
                XTRH(
                    "roles-table-head",
                    *roles.searcher.data_set,
                    DIV(
                        I(_class="fas fa-plus"),
                        **{
                            "_phanterpwa-way": "admin/roles/new",
                            "_class": "icon_button wave_on_click"
                        }
                    ),
                    sort_by=roles.searcher.sort_by,
                    sort_order=roles.searcher.sort_order,
                    sortable=roles.searcher.sortable,
                    on_click_sortable=self._on_sort,
                )
            )
            if roles.data is not js_undefined:
                for x in roles.data:
                    table.append(
                        XTRD(
                            "roles-table-data-{0}".format(x.id),
                            x.id,
                            x.grade,
                            x.role,
                            x.description,
                            widgets.MenuBox(
                                "drop_{0}".format(x.id),
                                I(_class="fas fa-ellipsis-v"),
                                widgets.MenuOption("View", **{
                                    "_class": "admin-button-user-edit wave_on_click",
                                    "_href": "#_phanterpwa:/admin/roles/{0}/view".format(x.id)
                                }),
                                widgets.MenuOption("Edit", **{
                                    "_class": "admin-button-user-edit wave_on_click",
                                    "_href": "#_phanterpwa:/admin/roles/{0}/edit".format(x.id)
                                }),
                                widgets.MenuOption("Impersonate", **{
                                    "_class": "admin-button-user-edit wave_on_click",
                                    "_href": "#_phanterpwa:/admin/roles/{0}/impersonate".format(x.id)
                                }),
                            )
                        )
                    )
                table.append(
                    XFOOTER(
                        "roles-table-footer",
                        page=roles.searcher.page,
                        total_pages=roles.searcher.total_pages,
                        on_click_page=self._on_page,
                    )
                )
            def edit_role(el):
                id_role = jQuery(el).attr("register_target")
                roles_edit_new.start(id_role)

            def view_role(el):
                id_role = jQuery(el).attr("register_target")
                roles_view.start(id_role)

            table.html_to("#lista-roles-container")

            jQuery(
                ".botao_edit_role"
            ).off(
                "click.botao_edit_role"
            ).on(
                "click.botao_edit_role",
                lambda: edit_role(this)
            )
            jQuery(
                ".botao_view_role"
            ).off(
                "click.botao_view_role"
            ).on(
                "click.botao_view_role",
                lambda: view_role(this)
            )

            def change_attr_drop(el):
                targ = jQuery(el).attr("phanterpwa_dowpdown_target")
                jQuery(el).attr("data-target", targ)
                # jQuery(el).dropdown()

            jQuery("[phanterpwa_dowpdown_target]").each(lambda: change_attr_drop(this))

    def _get_data_search(self, search="", field="nome_completo", orderby="nome_completo", sort="asc", page=1):
        window.PhanterPWA.ApiServer.GET(**{
            'url_args': ["api", "admin", "rolemanager"],
            'url_vars': {
                "search": search,
                "field": field,
                "orderby": orderby,
                "sort": sort,
                "page": page
            },
            'onComplete': self.after_get,
            'get_cache': self.process_data
        })

    def search(self):
        widgets = window.PhanterPWA.Request.widgets
        search = widgets["search_roles"].value()
        field = widgets["campos_roles"].value()
        self._get_data_search(search=search, field=field, orderby=field, sort="asc", page=1)


class User():
    def __init__(self, index_instance, user_id=None, action=None):
        self.index_instance = index_instance
        html = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV("USERS ADMINISTRATION", _class="phanterpwa-breadcrumb"),
                        DIV("USER", _class="phanterpwa-breadcrumb"),
                        _class="phanterpwa-breadcrumb-wrapper"
                    ),
                    _class="p-container"),
                _class='title_page_container card'
            ),
            DIV(
                DIV(
                    DIV(
                        DIV(preloaders.android, _style="width: 300px; height: 300px; overflow: hidden; margin: auto;"),
                        _style="text-align:center; padding: 50px 0;"
                    ),
                    _id="content-users",
                    _class='p-row card e-padding_20'
                ),

                _class="phanterpwa-container p-container"
            )
        )
        html.html_to("#main-container")

        self.user_id = user_id
        self.action = action
        if user_id == "new":
            self.get_form_user(user_id)
        elif action == "edit":
            self.get_form_user(user_id, "edit")
        elif action == "view":
            self.view(user_id, index_instance.request.params)
        elif action == "delete":
            window.PhanterPWA.DELETE(**{
                'url_args': ["api", "admin", "usermanager", user_id],
                'onComplete': lambda: window.PhanterPWA.open_way("admin/users")
            })

    def view(self, user_id, params):
        url_image = "{0}/api/admin/usermanager/{1}/image".format(
            window.PhanterPWA.get_api_address(),
            user_id
        )
        nome_completo = params["nome_completo"]
        nome_da_mae = params["nome_da_mae"]
        matricula = params["matricula"]
        cpf = params["cpf"]
        qrcode = params["qrcode"]
        rg_string = params["rg_string"]
        data_de_nascimento = params["data_de_nascimento"]
        self._carteira = DIV(
            DIV(
                DIV(
                    DIV(
                        DIV(
                            DIV(
                                DIV(
                                    IMG(
                                        _src=url_image
                                    ),
                                    _class="carteira-image"
                                ),
                                DIV(
                                    DIV(
                                        DIV(
                                            DIV(
                                                "NOME",
                                                _class="carteira-data-field"
                                            ),
                                            DIV(
                                                nome_completo,
                                                _class="carteira-data-nome carteira-data-value"
                                            ),
                                            _class="carteira-data-col"
                                        ),
                                        _class="p-col w1p100"
                                    ),
                                    DIV(
                                        DIV(
                                            DIV(
                                                "NOME DA MÃE",
                                                _class="carteira-data-field"
                                            ),
                                            DIV(
                                                nome_da_mae,
                                                _class="carteira-data-nome_da_mae carteira-data-value"
                                            ),
                                            _class="carteira-data-col"
                                        ),
                                        _class="p-col w1p100"
                                    ),
                                    DIV(
                                        DIV(
                                            DIV(
                                                'MATRÍCULA',
                                                _class="carteira-data-field"
                                            ),
                                            DIV(
                                                matricula,
                                                _class="carteira-data-matricula carteira-data-value"
                                            ),
                                            _class="carteira-data-col"
                                        ),
                                        _class="p-col w1p40"
                                    ),
                                    DIV(
                                        DIV(
                                            DIV(
                                                "CPF",
                                                _class="carteira-data-field"
                                            ),
                                            DIV(cpf,
                                                _class="carteira-data-cpf carteira-data-value"),
                                            _class="carteira-data-col"
                                        ),
                                        _class="p-col w1p60"
                                    ),
                                    DIV(
                                        DIV(
                                            DIV(
                                                "DATA DE NASCIMENTO",
                                                _class="carteira-data-field"
                                            ),
                                            DIV(data_de_nascimento,
                                                _class="carteira-data-data_de_nascimento carteira-data-value"),
                                            _class="carteira-data-col"
                                        ),
                                        _class="p-col w1p40"
                                    ),
                                    DIV(
                                        DIV(
                                            DIV(
                                                "RG",
                                                _class="carteira-data-field"
                                            ),
                                            DIV(rg_string,
                                                _class="carteira-data-rg_string carteira-data-value"),
                                            _class="carteira-data-col"
                                        ),
                                        _class="p-col w1p60"
                                    ),
                                    _class="carteira-data-container p-row"
                                ),
                                _class="p-col w1p30"
                            ),
                            DIV(
                                DIV(
                                    _class="carteira-logo"
                                ),
                                DIV(_class="carteira-qrcode"),
                                _class="p-col w1p70"
                            ),
                            _class="p-row"
                        ),
                        _class="carteira_containar"
                    ),
                    _class="view_user_container a4"
                ),
                _class="phanterpwa-media-print"
            ),
            _class="phanterpwa-media-print-container"
        )

        self._carteira.html_to("#content-users")
        window.PhanterPWA.LOAD(**{
            "args": ["loads", "svg_logo.html"],
            "onComplete": lambda data: jQuery("#content-users").find(".carteira-logo").html(data),
        })
        url = "{0}/api/associado/{1}".format(
            window.PhanterPWA.ApiServer.remote_address,
            qrcode
        )
        qrcode = __new__(QRCode(jQuery("#content-users").find(".carteira-qrcode")[0], {
            "text": url,
            "width": 125,
            "height": 125,
            "colorDark": "#000000",
            "colorLight": "#ffffff",
            "correctLevel": QRCode.CorrectLevel.H
        }))

    def after_get(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            self.process_data(json)

    def process_data(self, json):
        self.form = forms.Form(json.data.auth_user)
        self.form.html_to("#content-users")
        self.binds()

    def binds(self):
        forms.SignForm("#form-auth_user")
        forms.ValidateForm("#form-auth_user")
        jQuery(
            "#phanterpwa-widget-form-submit_button-auth_user"
        ).off(
            "click.submit_users_button"
        ).on(
            "click.submit_users_button",
            lambda: self.submit(this)
        )
 
    def get_form_user(self, user_id, action=None):
        if action == "edit":
            window.PhanterPWA.ApiServer.GET(**{
                'url_args': ["api", "admin", "usermanager", user_id, "edit"],
                'onComplete': self.after_get,
                'get_cache': self.process_data
            })
        elif action == "view":
            window.PhanterPWA.ApiServer.GET(**{
                'url_args': ["api", "admin", "usermanager", user_id, "view"],
                'onComplete': self.after_get,
                'get_cache': self.process_data
            })
        elif user_id == "new":
            window.PhanterPWA.ApiServer.GET(**{
                'url_args': ["api", "admin", "usermanager", user_id],
                'onComplete': self.after_get,
                'get_cache': self.process_data
            })

    def submit(self, el):
        if jQuery(el)[0].hasAttribute("disabled"):
            window.PhanterPWA.flash(html=I18N("The form has errors!"))
        else:
            form_user = jQuery("#form-auth_user")[0]
            form_user = __new__(FormData(form_user))
            if self.user_id == "new":
                window.PhanterPWA.ApiServer.POST(**{
                    'url_args': ["api", "admin", "usermanager"],
                    'form_data': form_user,
                    'onComplete': self.after_submit
                })
            elif self.user_id.isdigit():
                window.PhanterPWA.ApiServer.PUT(**{
                    'url_args': ["api", "admin", "usermanager", self.user_id],
                    'form_data': form_user,
                    'onComplete': self.after_submit
                })

    def after_submit(self, data):
        forms.SignForm("#form-auth_user")
        self.form.process_api_response(data)
        if data.status == 200 and self.user_id == 'new':
            window.PhanterPWA.open_way("admin/users/new")
        elif data.status == 200:
            window.PhanterPWA.open_way("admin/users")


class Impersonate():
    def __init__(self, index_instance, user_id=None):
        self.user_id = user_id
        self.index_instance = index_instance
        window.PhanterPWA.GET("api", "admin", "impersonate", self.user_id, onComplete=self.after_get)

    def after_get(self, data, ajax_status):
        if ajax_status == "success":
            window.PhanterPWA.open_way("home")
            window.PhanterPWA._after_submit_login(data, ajax_status)
        else:
            window.PhanterPWA.flash(**{'html': "Impersonate Problem!"})

class Role():
    def __init__(self, index_instance, role_id=None, action=None):
        self.index_instance = index_instance
        html = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV("ROLES ADMINISTRATION", _class="phanterpwa-breadcrumb"),
                        _class="phanterpwa-breadcrumb-wrapper"
                    ),
                    _class="p-container"),
                _class='title_page_container card'
            ),
            DIV(
                DIV(
                    DIV(
                        DIV(preloaders.android, _style="width: 300px; height: 300px; overflow: hidden; margin: auto;"),
                        _style="text-align:center; padding: 50px 0;"
                    ),
                    _id="content-roles",
                    _class='p-row card e-padding_20'
                ),

                _class="phanterpwa-container p-container"
            )
        )
        html.html_to("#main-container")

        self.role_id = role_id
        self.action = action
        if role_id == "new":
            self.get_form_role(role_id)
        elif action == "edit":
            self.get_form_role(role_id, "edit")
        elif action == "view":
            self.view(role_id, index_instance.request.params)

    def view(self, role_id, params):
        url_image = "{0}/api/admin/rolemanager/{1}/image".format(
            window.PhanterPWA.get_api_address(),
            role_id
        )
        nome_completo = params["nome_completo"]
        nome_da_mae = params["nome_da_mae"]
        matricula = params["matricula"]
        cpf = params["cpf"]
        qrcode = params["qrcode"]
        rg_string = params["rg_string"]
        data_de_nascimento = params["data_de_nascimento"]
        self._carteira = DIV(
            DIV(
                DIV(
                    DIV(
                        DIV(
                            DIV(
                                DIV(
                                    IMG(
                                        _src=url_image
                                    ),
                                    _class="carteira-image"
                                ),
                                DIV(
                                    DIV(
                                        DIV(
                                            DIV(
                                                "NOME",
                                                _class="carteira-data-field"
                                            ),
                                            DIV(
                                                nome_completo,
                                                _class="carteira-data-nome carteira-data-value"
                                            ),
                                            _class="carteira-data-col"
                                        ),
                                        _class="p-col w1p100"
                                    ),
                                    DIV(
                                        DIV(
                                            DIV(
                                                "NOME DA MÃE",
                                                _class="carteira-data-field"
                                            ),
                                            DIV(
                                                nome_da_mae,
                                                _class="carteira-data-nome_da_mae carteira-data-value"
                                            ),
                                            _class="carteira-data-col"
                                        ),
                                        _class="p-col w1p100"
                                    ),
                                    DIV(
                                        DIV(
                                            DIV(
                                                'MATRÍCULA',
                                                _class="carteira-data-field"
                                            ),
                                            DIV(
                                                matricula,
                                                _class="carteira-data-matricula carteira-data-value"
                                            ),
                                            _class="carteira-data-col"
                                        ),
                                        _class="p-col w1p40"
                                    ),
                                    DIV(
                                        DIV(
                                            DIV(
                                                "CPF",
                                                _class="carteira-data-field"
                                            ),
                                            DIV(cpf,
                                                _class="carteira-data-cpf carteira-data-value"),
                                            _class="carteira-data-col"
                                        ),
                                        _class="p-col w1p60"
                                    ),
                                    DIV(
                                        DIV(
                                            DIV(
                                                "DATA DE NASCIMENTO",
                                                _class="carteira-data-field"
                                            ),
                                            DIV(data_de_nascimento,
                                                _class="carteira-data-data_de_nascimento carteira-data-value"),
                                            _class="carteira-data-col"
                                        ),
                                        _class="p-col w1p40"
                                    ),
                                    DIV(
                                        DIV(
                                            DIV(
                                                "RG",
                                                _class="carteira-data-field"
                                            ),
                                            DIV(rg_string,
                                                _class="carteira-data-rg_string carteira-data-value"),
                                            _class="carteira-data-col"
                                        ),
                                        _class="p-col w1p60"
                                    ),
                                    _class="carteira-data-container p-row"
                                ),
                                _class="p-col w1p30"
                            ),
                            DIV(
                                DIV(
                                    _class="carteira-logo"
                                ),
                                DIV(_class="carteira-qrcode"),
                                _class="p-col w1p70"
                            ),
                            _class="p-row"
                        ),
                        _class="carteira_containar"
                    ),
                    _class="view_role_container a4"
                ),
                _class="phanterpwa-media-print"
            ),
            _class="phanterpwa-media-print-container"
        )

        self._carteira.html_to("#content-roles")
        window.PhanterPWA.LOAD(**{
            "args": ["loads", "svg_logo.html"],
            "onComplete": lambda data: jQuery("#content-roles").find(".carteira-logo").html(data),
        })
        url = "{0}/api/associado/{1}".format(
            window.PhanterPWA.ApiServer.remote_address,
            qrcode
        )
        qrcode = __new__(QRCode(jQuery("#content-roles").find(".carteira-qrcode")[0], {
            "text": url,
            "width": 125,
            "height": 125,
            "colorDark": "#000000",
            "colorLight": "#ffffff",
            "correctLevel": QRCode.CorrectLevel.H
        }))

    def after_get(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            self.process_data(json)

    def process_data(self, json):
        self.form = forms.Form(json.data.auth_role)
        self.form.html_to("#content-roles")
        self.binds()

    def binds(self):
        forms.SignForm("#form-auth_group")
        forms.ValidateForm("#form-auth_group")
        jQuery(
            "#phanterpwa-widget-form-submit_button-auth_group"
        ).off(
            "click.submit_roles_button"
        ).on(
            "click.submit_roles_button",
            lambda: self.submit(this)
        )
 
    def get_form_role(self, role_id, action=None):
        if action == "edit":
            window.PhanterPWA.ApiServer.GET(**{
                'url_args': ["api", "admin", "rolemanager", role_id, "edit"],
                'onComplete': self.after_get,
                'get_cache': self.process_data
            })
        elif action == "view":
            window.PhanterPWA.ApiServer.GET(**{
                'url_args': ["api", "admin", "rolemanager", role_id, "view"],
                'onComplete': self.after_get,
                'get_cache': self.process_data
            })
        elif role_id == "new":
            window.PhanterPWA.ApiServer.GET(**{
                'url_args': ["api", "admin", "rolemanager", role_id],
                'onComplete': self.after_get,
                'get_cache': self.process_data
            })

    def submit(self, el):
        if jQuery(el)[0].hasAttribute("disabled"):
            window.PhanterPWA.flash(html=I18N("The form has errors!"))
        else:
            form_role = jQuery("#form-auth_group")[0]
            form_role = __new__(FormData(form_role))
            if self.role_id == "new":
                window.PhanterPWA.ApiServer.POST(**{
                    'url_args': ["api", "admin", "rolemanager"],
                    'form_data': form_role,
                    'onComplete': self.after_submit
                })
            elif self.role_id.isdigit():
                window.PhanterPWA.ApiServer.PUT(**{
                    'url_args': ["api", "admin", "rolemanager", self.role_id],
                    'form_data': form_role,
                    'onComplete': self.after_submit
                })

    def after_submit(self, data):
        forms.SignForm("#form-auth_group")
        self.form.process_api_response(data)
        if data.status == 200 and self.role_id == 'new':
            window.PhanterPWA.open_way("admin/roles/new")
        elif data.status == 200:
            window.PhanterPWA.open_way("admin/roles")


__pragma__('nokwargs')
