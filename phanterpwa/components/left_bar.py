
from ..helpers import DIV, I, IMG
from ..xmlconstructor import XmlConstructor


class LeftBarSubMenu(XmlConstructor):
    def __init__(self, _id, label, **attributes):
        self._id = _id
        self.label = label
        self.initial_class = "phanterpwa-component-left_bar-submenu-button link"
        attributes["_id"] = "phanterpwa-component-left_bar-submenu-button-%s" % _id
        if "_class" in attributes:
            self.initial_class = " ".join(
                [attributes['_class'].strip(), "phanterpwa-component-left_bar-submenu-button link"])
        attributes['_class'] = self.initial_class
        content = [
            DIV(I(_class="fas fa-angle-right"), _class="phanterpwa-component-left_bar-submenu-icon-container"),
            DIV(self.label, _class="phanterpwa-component-left_bar-submenu-label"),
        ]
        XmlConstructor.__init__(self, 'div', False, *content, **attributes)


class LeftBarMenu(XmlConstructor):
    def __init__(self, _id, label, icon_class, **attributes):
        self._id = _id
        self.label = label
        self.icon_class = icon_class
        self.submenus = []
        self.componentSubmenu = LeftBarSubMenu
        initial_class = "phanterpwa-component-left_bar"
        initial_id = "phanterpwa-component-left_bar-%s" % _id
        self.button_attributes = attributes
        if "_class" in self.button_attributes:
            self.button_attributes["_class"] = " ".join([
                self.button_attributes['_class'].strip(),
                "phanterpwa-component-left_bar-menu link"])
        else:
            self.button_attributes["_class"] = "phanterpwa-component-left_bar-menu link"
        XmlConstructor.__init__(self, 'div', False, _id=initial_id, _class=initial_class)
        self._update_content()

    def addSubmenu(self, _id, label, **attributes):
        self.submenus.append(self.componentSubmenu(_id=_id, label=label, **attributes))
        self._update_content()

    def _update_content(self):
        html_submenus = ""
        attributes = self.button_attributes
        if self.submenus:
            attributes["_target_submenu"] = "phanterpwa-component-left_bar-submenu-from-%s" % self._id
            html_submenus = DIV(
                *self.submenus,
                _id=attributes["_target_submenu"],
                _class="phanterpwa-component-left_bar-submenu-container")
        self.content = [
            DIV(
                DIV(I(_class=self.icon_class),
                    _class="phanterpwa-component-left_bar-icon-container"),
                DIV(self.label, _class="phanterpwa-component-left_bar-label"),
                **attributes),
            html_submenus
        ]


class LeftBarButton(XmlConstructor):
    def __init__(self, _id, label, icon_class, **attributes):
        self._id = _id
        self.label = label
        self.icon_class = icon_class
        self.submenus = []
        initial_class = "phanterpwa-component-left_bar"
        initial_id = "phanterpwa-component-left_bar-%s" % _id
        self.button_attributes = attributes
        if "_class" in self.button_attributes:
            self.button_attributes["_class"] = " ".join([
                self.button_attributes['_class'].strip(),
                "phanterpwa-component-left_bar-button link"])
        else:
            self.button_attributes["_class"] = "phanterpwa-component-left_bar-button link"
        XmlConstructor.__init__(self, 'div', False, _id=initial_id, _class=initial_class)
        self.content = [
            DIV(
                DIV(I(_class=self.icon_class),
                    _class="phanterpwa-component-left_bar-icon-container"),
                DIV(self.label, _class="phanterpwa-component-left_bar-label"),
                **self.button_attributes)
        ]


class LeftBarUserMenu(XmlConstructor):
    def __init__(self, _id, name_user="Nome usuário", url_image_user="/static/images/user.png", **attributes):
        self._id = _id
        self.name_user = name_user
        self.url_image_user = url_image_user
        self.submenus = []
        self._image = IMG(_id="phanterpwa-component-left_bar-url-imagem-user",
            _src=url_image_user,
            _alt="user avatar")
        self.componentSubmenu = LeftBarSubMenu
        initial_class = "phanterpwa-component-left_bar"
        initial_id = "phanterpwa-component-left_bar-%s" % _id
        self.button_attributes = attributes
        if "_class" in self.button_attributes:
            self.button_attributes["_class"] = " ".join([
                self.button_attributes['_class'].strip(),
                "phanterpwa-component-left_bar-button-user cmp-bar-user-img link"])
        else:
            self.button_attributes["_class"] = "phanterpwa-component-left_bar-menu link"
        XmlConstructor.__init__(self, 'div', False, _id=initial_id, _class=initial_class)
        self._update_content()

    def addSubmenu(self, _id, label, **attributes):
        self.submenus.append(self.componentSubmenu(_id=_id, label=label, **attributes))
        self._update_content()

    def _update_content(self):
        html_submenus = ""
        attributes = self.button_attributes
        if self.submenus:
            attributes["_target_submenu"] = "phanterpwa-component-left_bar-submenu-from-%s" % self._id
            html_submenus = DIV(
                *self.submenus,
                _id=attributes["_target_submenu"],
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
                **attributes),
            html_submenus
        ]