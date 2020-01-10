import phanterpwa.transcrypt.helpers as helpers
import phanterpwa.transcrypt.application as application
from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = window = Hammer = this = js_undefined = window = console = 0
__pragma__('noskip')


DIV = helpers.XmlConstructor.tagger("div")
I = helpers.XmlConstructor.tagger("i")
IMG = helpers.XmlConstructor.tagger("img", True)
CONCATENATE = helpers.CONCATENATE
I18N = helpers.I18N

__pragma__('kwargs')


class LeftBar(application.Component):
    def __init__(self, element_target, **parameters):
        self.element_target = jQuery(element_target)
        self.identifier = "LeftBar"
        if "_id" not in parameters:
            parameters['_id'] = "phanterpwa-component-left_bar"
        if "_class" in parameters:
            parameters["_class"] = "{0} {1}".format(
                parameters["_class"], "phanterpwa-component-left_bar-wrapper"
            )
        else:
            parameters["_class"] = "phanterpwa-component-left_bar-wrapper"
        tcontent = [
            DIV(_id="phanterpwa-component-left_bar-top"),
            DIV(_id="phanterpwa-component-left_bar-middle"),
            DIV(_id="phanterpwa-component-left_bar-bottom")
        ]
        self.all_buttons = list()
        self.xml = DIV(*tcontent, **parameters)

    def add_button(self, button, **parameters):
        if isinstance(button, (LeftBarMenu, LeftBarButton, LeftBarUserMenu)):
            id_button = button.identifier
            has_button = False
            for b in self.all_buttons:
                if b.identifier == id_button:
                    has_button = True

            if not has_button:
                self.all_buttons.append(button)
            self.reload()

    def start(self):
        window.PhanterPWA.xml_to_dom_element(
            self.xml,
            self.element_target
        )
        self.reload()

    def reload(self):
        for x in self.all_buttons:
            id_button = "phanterpwa-component-left_bar-menu_button-{0}".format(x.identifier)

            if all([self._check_button_requires_login(x),
                self._check_button_routes(x),
                self._check_button_roles(x)]):
                position = self._get_button_position(x)
                b = self.element_target.find(
                    "#phanterpwa-component-left_bar-{0}".format(position)
                ).find("#{0}".format(id_button))

                if b.length > 0:
                    b.parent().remove()
                self.element_target.find(
                    "#phanterpwa-component-left_bar-{0}".format(position)
                ).append(x.jquery())
                x.start()
            else:
                self.element_target.find("#{0}".format(id_button)).parent().remove()

    def _get_button_position(self, button):
        pos = button.position
        if pos is not None and pos is not js_undefined:
            if pos in ['middle', 'top']:
                return pos
        return "bottom"

    def _check_button_requires_login(self, button):
        requires_login = button.requires_login
        if requires_login is not None and requires_login is not js_undefined:
            if requires_login is True:
                authorization = window.PhanterPWA.get_authorization()
                if authorization is not None:
                    return True
            else:
                return True
        return False

    def _check_button_roles(self, button):
        roles = button.autorized_roles
        if roles is not None and roles is not js_undefined:
            if isinstance(roles, list):
                if "all" in roles:
                    return True
                auth_user = window.PhanterPWA.get_auth_user()
                if auth_user is not None:
                    if isinstance(auth_user.roles, list) and isinstance(roles, list):
                        if len(set(auth_user.roles) & set(roles)) > 0:
                            return True
                else:
                    if "anonymous" in roles:
                        return True

        return False

    def _check_button_routes(self, button):
        current_route = window.PhanterPWA.get_current_route()
        routes = button.routes
        if routes is not None and routes is not js_undefined:
            if isinstance(routes, list):
                if "all" in routes:
                    return True
                elif current_route in routes:
                    return True
        return False

    @staticmethod
    def _open():
        element = jQuery("#phanterpwa-component-left_bar").addClass("enabled")

    def open(self):
        self._open()

    @staticmethod
    def _close():
        element = jQuery("#phanterpwa-component-left_bar").removeClass("enabled").removeClass("enabled_submenu").find(
            ".phanterpwa-component-left_bar-menu_button-wrapper"
        ).removeClass("enabled")

    def close(self):
        self._close()


class LeftBarMainButton(application.Component):
    def __init__(self, element_target, **parameters):
        application.Component.__init__(self, "LeftBarMainButton", self.element)
        self.element_target = jQuery(element_target)
        self._icon = I(_class="fas fa-bars")
        if "_id" not in parameters:
            parameters['_id'] = "phanterpwa-component-left_bar-main_button"
        if "_class" in parameters:
            parameters["_class"] = "{0} {1}".format(
                parameters["_class"],
                "phanterpwa-component-left_bar-main_button-wrapper waves-effect waves-phanterpwa link"
            )
        else:
            parameters["_class"] = "{0} {1}".format(
                "phanterpwa-component-left_bar-main_button-wrapper",
                "waves-effect waves-phanterpwa link"
            )
        if "icon" in parameters:
            self._icon = parameters["icon"]
        self.xml = DIV(self._icon, **parameters)


    def switch_leftbar(self):
        el = self.element_target.find("#phanterpwa-component-left_bar-main_button")
        if el.hasClass("enabled") or el.hasClass("enabled_submenu"):
            self.close_leftbar()
        else:
            self.open_leftbar()

    def close_leftbar(self):
        el = self.element_target.find(
            "#phanterpwa-component-left_bar-main_button").removeClass("enabled").removeClass("enabled_submenu")
        LeftBar._close()

    def open_leftbar(self):
        self.element_target.find("#phanterpwa-component-left_bar-main_button").addClass("enabled")
        LeftBar._open()

    def start(self):
        window.PhanterPWA.xml_to_dom_element(
            self.xml,
            self.element_target
        )
        self.element_target.find("#phanterpwa-component-left_bar-main_button").off("click.mainbutton_leftbar").on(
            "click.mainbutton_leftbar",
            lambda: self.switch_leftbar()
        )


class LeftBarButton(helpers.XmlConstructor):
    def __init__(self, identifier, label, icon, **parameters):
        self.identifier = identifier
        self.label = label
        self.icon = icon
        self.requires_login = False
        self.autorized_roles = ["all"]
        self.routes = ["all"]
        self.position = "bottom"
        parameters["_id"] = "phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        if "_class" in parameters:
            parameters["_class"] = "{0} {1}".format(
                parameters['_class'],
                "phanterpwa-component-left_bar-button link")
        else:
            parameters["_class"] = "phanterpwa-component-left_bar phanterpwa-component-left_bar-button link"

        if "requires_login" in parameters:
            self.requires_login = parameters["requires_login"]

        if "autorized_roles" in parameters:
            if isinstance(parameters["autorized_roles"], list):
                self.autorized_roles = parameters["autorized_roles"]
            else:
                console.error("The parameter 'autorized_roles' must be type list")

        if "routes" in parameters:
            if isinstance(parameters["routes"], list):
                self.routes = parameters["routes"]
            else:
                console.error("The parameter 'routes' must be type list")

        if "position" in parameters:
            self.position = parameters["position"]

        content = [
            DIV(
                DIV(self.icon,
                    _class="phanterpwa-component-left_bar-icon-container"),
                DIV(self.label, _class="phanterpwa-component-left_bar-label"),
                **parameters
            )
        ]

        helpers.XmlConstructor.__init__(
            self, 'div', False, *content, _class="phanterpwa-component-left_bar-menu_button-wrapper"
        )

    def start(self):
        console.log("start this button")


class LeftBarSubMenu(helpers.XmlConstructor):
    def __init__(self, identifier, label, **parameters):
        self.identifier = identifier
        self.label = label
        self.initial_class = "phanterpwa-component-left_bar-submenu-button link"
        parameters["_id"] = "phanterpwa-component-left_bar-submenu-button-{0}".format(identifier)
        if "_class" in parameters:
            self.initial_class = " ".join(
                [parameters['_class'].strip(), "phanterpwa-component-left_bar-submenu-button link"])
        parameters['_class'] = self.initial_class
        content = [
            DIV(I(_class="fas fa-angle-right"), _class="phanterpwa-component-left_bar-submenu-icon-container"),
            DIV(self.label, _class="phanterpwa-component-left_bar-submenu-label"),
        ]
        helpers.XmlConstructor.__init__(self, 'div', False, *content, **parameters)


class LeftBarMenu(helpers.XmlConstructor):
    def __init__(self, identifier, label, icon, **parameters):
        self.identifier = identifier
        self.label = label
        self.icon = icon
        self.parameters = parameters
        self.submenus = []
        self.componentSubmenu = LeftBarSubMenu
        self.requires_login = False
        self.autorized_roles = ["all"]
        self.routes = ["all"]
        self.position = "bottom"
        parameters["_id"] = "phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        if "_class" in parameters:
            parameters["_class"] = "{0} {1}".format(
                parameters['_class'],
                "phanterpwa-component-left_bar-menu link")
        else:
            parameters["_class"] = "phanterpwa-component-left_bar phanterpwa-component-left_bar-menu link"

        if "requires_login" in parameters:
            self.requires_login = parameters["requires_login"]

        if "autorized_roles" in parameters:
            if isinstance(parameters["autorized_roles"], list):
                self.autorized_roles = parameters["autorized_roles"]
            else:
                console.error("The parameter 'autorized_roles' must be type list")
        if "routes" in parameters:
            if isinstance(parameters["routes"], list):
                self.routes = parameters["routes"]
            else:
                console.error("The parameter 'routes' must be type list")
        if "position" in parameters:
            self.position = parameters["position"]

        helpers.XmlConstructor.__init__(self, 'div', False, _class="phanterpwa-component-left_bar-menu_button-wrapper")
        self._update_content()

    def addSubmenu(self, identifier, label, **parameters):
        self.submenus.append(LeftBarSubMenu(identifier, label, **parameters))
        self._update_content()

    def _update_content(self):
        html_submenus = ""
        if self.submenus:
            self.parameters["_target_submenu"] = "phanterpwa-component-left_bar-submenu-from-{0}".format(
                self.identifier)
            html_submenus = DIV(
                *self.submenus,
                _id=self.parameters["_target_submenu"],
                _class="phanterpwa-component-left_bar-submenu-container")
        self.content = [
            DIV(
                DIV(self.icon,
                    _class="phanterpwa-component-left_bar-icon-container"),
                DIV(self.label, _class="phanterpwa-component-left_bar-label"),
                **self.parameters),
            html_submenus
        ]

    def switch_menu(self, el):
        if jQuery(el).parent().hasClass("enabled"):
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        ).parent()
        element.addClass("enabled")
        jQuery("#phanterpwa-component-left_bar").addClass("enabled_submenu").addClass("enabled")
        jQuery("#phanterpwa-component-left_bar-main_button").addClass("enabled")

    def close_menu(self):
        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        ).parent()
        element.removeClass("enabled")
        if jQuery("#phanterpwa-component-left_bar .phanterpwa-component-left_bar-menu_button-wrapper.enabled").length == 0:
            jQuery("#phanterpwa-component-left_bar").removeClass("enabled_submenu").removeClass("enabled")
            jQuery("#phanterpwa-component-left_bar-main_button").removeClass("enabled")

    def start(self):

        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        )
        console.log("achou", element)
        element.off("click.open_leftbar_menu").on(
            "click.open_leftbar_menu",
            lambda: self.switch_menu(this)
        )
        sub_element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-submenu-from-{0} .phanterpwa-component-left_bar-submenu-button".format(self.identifier))
        sub_element.off("click.close_leftbar_submenu").on(
            "click.close_leftbar_submenu",
            lambda: self.close_menu()
        )


class LeftBarUserMenu(helpers.XmlConstructor):
    def __init__(self, **parameters):
        self.identifier = "auth_user_login"
        self.submenus = []
        self.parameters = parameters
        self.requires_login = True
        self.autorized_roles = ["all"]
        self.routes = ["all"]
        self.position = "bottom"
        parameters["_id"] = "phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        if "_class" in parameters:
            parameters["_class"] = "{0} {1}".format(
                parameters['_class'],
                "phanterpwa-component-left_bar-menu link")
        else:
            parameters["_class"] = "phanterpwa-component-left_bar phanterpwa-component-left_bar-menu link"

        if "requires_login" in parameters:
            self.requires_login = parameters["requires_login"]

        if "autorized_roles" in parameters:
            if isinstance(parameters["autorized_roles"], list):
                self.autorized_roles = parameters["autorized_roles"]
            else:
                console.error("The parameter 'autorized_roles' must be type list")
        if "routes" in parameters:
            if isinstance(parameters["routes"], list):
                self.routes = parameters["routes"]
            else:
                console.error("The parameter 'routes' must be type list")
        if "position" in parameters:
            self.position = parameters["position"]

        self._image = IMG(_id="phanterpwa-component-left_bar-url-imagem-user",
            _src="/static/{0}/images/user.png".format(
                window.PhanterPWA.CONFIG.PROJECT.version),
            _alt="user avatar")

        helpers.XmlConstructor.__init__(
            self, 'div', False, _class="{0} {1}".format(
                "phanterpwa-component-left_bar-menu_button-wrapper-auth_user",
                "phanterpwa-component-left_bar-menu_button-wrapper"
            )
        )
        self._update_content()

    def addSubmenu(self, identifier, label, **parameters):
        self.submenus.append(LeftBarSubMenu(identifier, label, **parameters))
        self._update_content()

    def _update_content(self):
        html_submenus = ""
        self.parameters
        if self.submenus:
            self.parameters["_target_submenu"] = "phanterpwa-component-left_bar-submenu-from-{0}".format(self.identifier)
            html_submenus = DIV(
                *self.submenus,
                _id=self.parameters["_target_submenu"],
                _class="phanterpwa-component-left_bar-submenu-container")
        self.content = [
            DIV(
                DIV(
                    DIV(self._image,
                        _class="phanterpwa-component-left_bar-image-user"),
                    _class="phanterpwa-component-left_bar-image-user-container"),
                DIV(self.name_user,
                    _id="phanterpwa-component-left_bar-name-user",
                    _class="phanterpwa-component-left_bar-label"),
                **self.parameters),
            html_submenus
        ]

    def switch_menu(self, el):
        if jQuery(el).parent().hasClass("enabled"):
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        ).parent()
        element.addClass("enabled")
        jQuery("#phanterpwa-component-left_bar").addClass("enabled_submenu").addClass("enabled")
        jQuery("#phanterpwa-component-left_bar-main_button").addClass("enabled")

    def close_menu(self):
        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        ).parent()
        element.removeClass("enabled")
        if jQuery("#phanterpwa-component-left_bar .phanterpwa-component-left_bar-menu_button-wrapper.enabled").length == 0:
            jQuery("#phanterpwa-component-left_bar").removeClass("enabled_submenu").removeClass("enabled")
            jQuery("#phanterpwa-component-left_bar-main_button").removeClass("enabled")

    def start(self):

        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        )
        element.off("click.open_leftbar_menu").on(
            "click.open_leftbar_menu",
            lambda: self.switch_menu(this)
        )
        sub_element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-submenu-from-{0} .phanterpwa-component-left_bar-submenu-button".format(
                self.identifier))
        sub_element.off("click.close_leftbar_submenu").on(
            "click.close_leftbar_submenu",
            lambda: self.close_menu()
        )
        self.auth_user = window.PhanterPWA.get_auth_user()
        user_name = "Anonymous"
        role = I18N("User")
        user_image = "/static/{0}/images/user.png".format(
            window.PhanterPWA.CONFIG.PROJECT.version)
        if self.auth_user is not None:
            first_name = self.auth_user.first_name
            last_name = self.auth_user.last_name
            user_name = "{0} {1}".format(first_name, last_name)
            role = I18N(self.auth_user.role)
            if self.auth_user.image is not None and self.auth_user.image is not js_undefined:
                user_image = self.auth_user.image
        element.find("#phanterpwa-component-left_bar-url-imagem-user").attr("src", user_image)
        element.find("#phanterpwa-component-left_bar-name-user").text(user_name)


__pragma__('nokwargs')

# def close_menu():
#     jQuery("#left_bar").removeClass("enabled_submenu").removeClass("enabled")
#     jQuery("#menu-button-main-page").removeClass("enabled_submenu").removeClass("enabled")
#     jQuery(".phanterpwa-component-left_bar").removeClass("enabled")
#     jQuery(".cmp-bar_user_and_menu-container").removeClass("enabled")


# def open_menu():
#     jQuery("#left_bar").addClass("enabled")
#     jQuery("#menu-button-main-page").addClass("enabled")


# def toggle_menu():
#     opened_menu = jQuery("#left_bar").hasClass("enabled")
#     opened_submenu = jQuery("#left_bar").hasClass("enabled_submenu")
#     if (opened_menu and opened_submenu):
#         jQuery("#left_bar").removeClass("enabled")
#         jQuery("#left_bar, #menu-button-main-page").removeClass("enabled_submenu")
#         jQuery("#menu-button-main-page").removeClass("enabled")
#         jQuery(".phanterpwa-component-left_bar, .cmp-bar_user_and_menu-container").removeClass("enabled")
#     elif (opened_menu):
#         jQuery("#left_bar").removeClass("enabled")
#         jQuery("#left_bar, #menu-button-main-page").removeClass("enabled_submenu")
#         jQuery("#menu-button-main-page").removeClass("enabled")
#         jQuery(".phanterpwa-component-left_bar, .cmp-bar_user_and_menu-container").removeClass("enabled")
#     elif (opened_submenu):
#         with_screen = jQuery(window).width()
#         if int(with_screen) < 992:
#             jQuery("#left_bar").removeClass("enabled")
#             jQuery("#left_bar, #menu-button-main-page").removeClass("enabled_submenu")
#             jQuery("#menu-button-main-page").removeClass("enabled")
#             jQuery(".phanterpwa-component-left_bar, .cmp-bar_user_and_menu-container").removeClass("enabled")
#         else:
#             jQuery("#left_bar").addClass("enabled")
#             jQuery("#menu-button-main-page").addClass("enabled")
#     else:
#         jQuery("#left_bar").addClass("enabled")
#         jQuery("#menu-button-main-page").addClass("enabled")


# __pragma__('kwargs')


# @decorators.check_if_has_role(roles=["administrator", "root"])
# def botoes_administrador(**kargs):
#     if kargs.has_role is True:
#         def after_load(data):
#             id_data = jQuery(data).attr("id")
#             has_button = list()

#             def open_submenu_administracao(el):
#                 parent = jQuery(el).parent()
#                 if jQuery(parent).hasClass('enabled'):
#                     jQuery(parent).removeClass('enabled')
#                 else:
#                     jQuery(parent).addClass('enabled')
#                     open_menu()
#                 jQuery(
#                     ".phanterpwa-component-left_bar-submenu-button, .phanterpwa-component-left_bar-button"
#                 ).off(
#                     "click.close_menu"
#                 ).on(
#                     "click.close_menu",
#                     lambda: close_menu()
#                 )

#             def check_has_button(el):

#                 id_check = jQuery(el).attr("id")
#                 if id_check == id_data:
#                     has_button.append(id_data)
#             jQuery("#options-bottom-main-bar-left>.phanterpwa-component-left_bar").each(
#                 lambda id, el: check_has_button(el)
#             )
#             if len(has_button) == 0:
#                 jQuery("#options-bottom-main-bar-left").append(data)
#                 jQuery(
#                     "#phanterpwa-component-left_bar-administracao>.phanterpwa-component-left_bar-menu"
#                 ).off(
#                     "click.administracao"
#                 ).on(
#                     "click.administracao",
#                     lambda: open_submenu_administracao(this)
#                 )
#         jQuery("<div></div>").load("./components/left_bar/botao_administracao.html", after_load)
#     else:
#         jQuery("#phanterpwa-component-left_bar-administracao").remove()


# __pragma__('nokwargs')


# def start():
#     jQuery(
#         "#menu-button-main-page"
#     ).off(
#         "click.button_menu_left"
#     ).on(
#         "click.button_menu_left",
#         toggle_menu
#     )
#     jQuery(
#         ".phanterpwa-component-left_bar-submenu-button, .phanterpwa-component-left_bar-button"
#     ).off(
#         "click.close_menu"
#     ).on(
#         "click.close_menu",
#         close_menu
#     )
#     __pragma__('jsiter')
#     hammerconf = {
#         'inputClass': Hammer.PointerEventInput if Hammer.SUPPORT_POINTER_EVENTS else Hammer.TouchInput
#     }
#     __pragma__('nojsiter')

#     def gesture_open_left_menu(ev):
#         if((ev.gesture.center.x - ev.gesture.deltaX) < 10):
#             open_menu()

#     jQuery("body").hammer(
#         hammerconf
#     ).off(
#         "swiperight.event_menu, tap.event_menu"
#     ).on(
#         "swiperight.event_menu",
#         lambda ev: gesture_open_left_menu(ev)
#     ).on(
#         "tap.event_menu",
#         close_menu
#     )
#     botoes_administrador()

