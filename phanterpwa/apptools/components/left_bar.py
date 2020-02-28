import phanterpwa.apptools.helpers as helpers
import phanterpwa.apptools.application as application
from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = window = Hammer = this = js_undefined = window = console = __new__ = RegExp = 0
__pragma__('noskip')


DIV = helpers.XmlConstructor.tagger("div")
I = helpers.XmlConstructor.tagger("i")
IMG = helpers.XmlConstructor.tagger("img", True)
CONCATENATE = helpers.CONCATENATE
I18N = helpers.I18N

__pragma__('kwargs')


class LeftBar(application.Component):
    def __init__(self, target_selector, **parameters):
        self.target_selector = target_selector
        self.element_target = jQuery(self.target_selector)
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
        self.html = DIV(*tcontent, **parameters)
        application.Component.__init__(self, "left_bar", self.html)
        self.html_to(target_selector)

    def add_button(self, button, **parameters):
        if isinstance(button, (LeftBarMenu, LeftBarButton, LeftBarUserMenu)):
            id_button = button.identifier
            has_button = False
            cont = 0
            position = None
            for b in self.all_buttons:
                if b.identifier == id_button:
                    has_button = True
                    position = cont
                cont += 1

            if not has_button:
                self.all_buttons.append(button)
            else:
                self.all_buttons[position] = button
        self.reload()

    def reload(self):
        self.start()

    def start(self):
        self.element_target = jQuery(self.target_selector)
        for x in self.all_buttons:
            id_button = "phanterpwa-component-left_bar-menu_button-{0}".format(x.identifier)

            if all([self._check_button_requires_login(x),
                self._check_button_ways(x),
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
        window.PhanterPWA.reload_events(**{"selector": "#phanterpwa-component-left_bar"})

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
                        if len(set(auth_user.roles).intersection(set(roles))) > 0:
                            return True
                else:
                    if "anonymous" in roles:
                        return True

        return False

    def _check_button_ways(self, button):
        current_way = window.PhanterPWA.get_current_way()
        ways = button.ways
        if ways is not None and ways is not js_undefined:
            if isinstance(ways, list):
                if "all" in ways:
                    return True
                elif current_way in ways:
                    return True
                else:
                    for x in ways:
                        if callable(x):
                            if x(current_way) is True:
                                return True
                        elif x.startswith("^"):
                            r = __new__(RegExp(x))
                            result = current_way.match(r)
                            if result is not None:
                                return True

        return False

    @staticmethod
    def _open():
        jQuery("#phanterpwa-component-left_bar").addClass("enabled")

    def open(self):
        self._open()

    @staticmethod
    def _close():
        jQuery("#phanterpwa-component-left_bar").removeClass("enabled").removeClass("enabled_submenu").find(
            ".phanterpwa-component-left_bar-menu_button-wrapper"
        ).removeClass("enabled")

    def close(self):
        self._close()


class LeftBarMainButton(application.Component):
    def __init__(self, target_selector, **parameters):
        self.target_selector = target_selector
        self.element_target = jQuery(self.target_selector)
        self._icon = I(_class="fas fa-bars")
        if "_id" not in parameters:
            parameters['_id'] = "phanterpwa-component-left_bar-main_button"
        if "_class" in parameters:
            parameters["_class"] = "{0} {1}".format(
                parameters["_class"],
                "phanterpwa-component-left_bar-main_button-wrapper wave_on_click waves-phanterpwa link"
            )
        else:
            parameters["_class"] = "{0} {1}".format(
                "phanterpwa-component-left_bar-main_button-wrapper",
                "wave_on_click waves-phanterpwa link"
            )
        if "icon" in parameters:
            self._icon = parameters["icon"]
        html = DIV(self._icon, **parameters)
        application.Component.__init__(self, "left_bar_main_button", html)
        self.html_to(target_selector)

    def switch_leftbar(self):
        self.element_target = jQuery(self.target_selector)
        el = self.element_target.find("#phanterpwa-component-left_bar-main_button")
        if el.hasClass("enabled") or el.hasClass("enabled_submenu"):
            self.close_leftbar()
        else:
            self.open_leftbar()

    def close_leftbar(self):
        self.element_target = jQuery(self.target_selector)
        self.element_target.find(
            "#phanterpwa-component-left_bar-main_button").removeClass("enabled").removeClass("enabled_submenu")
        LeftBar._close()

    def open_leftbar(self):
        self.element_target = jQuery(self.target_selector)
        self.element_target.find("#phanterpwa-component-left_bar-main_button").addClass("enabled")
        LeftBar._open()

    def _binds(self):
        self.element_target = jQuery(self.target_selector)
        self.element_target.find("#phanterpwa-component-left_bar-main_button").off("click.mainbutton_leftbar").on(
            "click.mainbutton_leftbar",
            lambda: self.switch_leftbar()
        )

    def reload(self):
        self._binds()

    def start(self):
        self._binds()


class LeftBarButton(helpers.XmlConstructor):
    def __init__(self, identifier, label, icon, **parameters):
        self.identifier = identifier
        self.label = label
        self.icon = icon
        self.requires_login = False
        self.autorized_roles = ["all"]
        self.ways = ["all"]
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
                if window.PhanterPWA.DEBUG:
                    console.error("The parameter 'autorized_roles' must be type list")

        if "ways" in parameters:
            if isinstance(parameters["ways"], list):
                self.ways = parameters["ways"]
            else:
                if window.PhanterPWA.DEBUG:
                    console.error("The parameter 'ways' must be type list")

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
        if window.PhanterPWA.DEBUG:
            console.info("start button {0}".format(self.identifier))


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
        self.ways = ["all"]
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
                if window.PhanterPWA.DEBUG:
                    console.error("The parameter 'autorized_roles' must be type list")
        if "ways" in parameters:
            if isinstance(parameters["ways"], list):
                self.ways = parameters["ways"]
            else:
                if window.PhanterPWA.DEBUG:
                    console.error("The parameter 'ways' must be type list")
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
        if jQuery("#phanterpwa-component-left_bar").find(
                ".phanterpwa-component-left_bar-menu_button-wrapper.enabled").length == 0:
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
            "#phanterpwa-component-left_bar-submenu-from-{0} {1}".format(
                self.identifier, ".phanterpwa-component-left_bar-submenu-button"))
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
        self.ways = ["all"]
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
                if window.PhanterPWA.DEBUG:
                    console.error("The parameter 'autorized_roles' must be type list")
        if "ways" in parameters:
            if isinstance(parameters["ways"], list):
                self.ways = parameters["ways"]
            else:
                if window.PhanterPWA.DEBUG:
                    console.error("The parameter 'ways' must be type list")
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
            self.parameters["_target_submenu"] = \
                "phanterpwa-component-left_bar-submenu-from-{0}".format(self.identifier)
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
        if jQuery("#phanterpwa-component-left_bar").find(
                ".phanterpwa-component-left_bar-menu_button-wrapper.enabled").length == 0:
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
