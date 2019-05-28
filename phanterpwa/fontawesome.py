# -*- coding: utf-8 -*-
from .helpers import DIV, I, IMG
from .xmlconstructor import XmlConstructor


class FontawesomeButtonLeftSubMenu(XmlConstructor):
    def __init__(self, _id, label, **attributes):
        self._id = _id
        self.label = label
        self.initial_class = "fontawesome-component-left-menu-submenu-button link"
        attributes["_id"] = "fontawesome-component-left-menu-submenu-button-%s" % _id
        if "_class" in attributes:
            self.initial_class = " ".join(
                [attributes['_class'].strip(), "fontawesome-component-left-menu-submenu-button link"])
        attributes['_class'] = self.initial_class
        content = [
            DIV(I(_class="fas fa-angle-right"), _class="fontawesome-component-left-menu-submenu-icon-container"),
            DIV(self.label, _class="fontawesome-component-left-menu-submenu-label"),
        ]
        XmlConstructor.__init__(self, 'div', False, *content, **attributes)


class FontawesomeButtonLeftMenu(XmlConstructor):
    def __init__(self, _id, label, icon_class, **attributes):
        self._id = _id
        self.label = label
        self.icon_class = icon_class
        self.submenus = []
        self.componentSubmenu = FontawesomeButtonLeftSubMenu
        initial_class = "fontawesome-component-left-menu"
        initial_id = "fontawesome-component-left-menu-%s" % _id
        self.button_attributes = attributes
        self.button_attributes["_cmd_left_menu"] = "link"
        if "_class" in self.button_attributes:
            self.button_attributes["_class"] = " ".join([
                self.button_attributes['_class'].strip(),
                "fontawesome-component-left-menu-button link"])
        else:
            self.button_attributes["_class"] = "fontawesome-component-left-menu-button link"
        XmlConstructor.__init__(self, 'div', False, _id=initial_id, _class=initial_class)
        self._update_content()

    def addSubmenu(self, _id, label, **attributes):
        self.submenus.append(self.componentSubmenu(_id=_id, label=label, **attributes))
        self._update_content()

    def _update_content(self):
        html_submenus = ""
        attributes = self.button_attributes
        if self.submenus:
            attributes["_target_submenu"] = "fontawesome-component-left-menu-submenu-from-%s" % self._id
            html_submenus = DIV(
                *self.submenus,
                _id=attributes["_target_submenu"],
                _class="fontawesome-component-left-menu-submenu-container")
        self.content = [
            DIV(
                DIV(I(_class=self.icon_class),
                    _class="fontawesome-component-left-menu-icon-container"),
                DIV(self.label, _class="fontawesome-component-left-menu-label"),
                **attributes),
            html_submenus
        ]


class FontawesomeButtonLeftMenuPlus(XmlConstructor):
    def __init__(self, _id, label, icon_class, **attributes):
        self._id = _id
        self.label = label
        self.icon_class = icon_class
        self.submenus = []
        self.componentSubmenu = FontawesomeButtonLeftSubMenu
        initial_class = "fontawesome-component-left-menu"
        initial_id = "fontawesome-component-left-menu-%s" % _id
        self.button_attributes = attributes
        self.button_attributes["_cmd_left_menu"] = "link"
        if "_class" in self.button_attributes:
            self.button_attributes["_class"] = " ".join([
                self.button_attributes['_class'].strip(),
                "fontawesome-component-left-menu-button link"])
        else:
            self.button_attributes["_class"] = "fontawesome-component-left-menu-button link"
        XmlConstructor.__init__(self, 'div', False, _id=initial_id, _class=initial_class)
        self._update_content()

    def addSubmenu(self, _id, label, **attributes):
        self.submenus.append(self.componentSubmenu(_id=_id, label=label, **attributes))
        self._update_content()

    def _update_content(self):
        html_submenus = ""
        attributes = self.button_attributes
        if self.submenus:
            attributes["_target_submenu"] = "fontawesome-component-left-menu-submenu-from-%s" % self._id
            html_submenus = DIV(
                *self.submenus,
                _id=attributes["_target_submenu"],
                _class="fontawesome-component-left-menu-submenu-container")
        self.content = [
            DIV(
                DIV(
                    DIV(
                        I(_class=self.icon_class),
                        DIV(
                            I(_class="fas fa-plus"),
                            _class="fontawesome-component-left-menu-icon-plus"),
                        _class="fontawesome-component-left-menu-icon-plus-container"),
                    _class="fontawesome-component-left-menu-icon-container"),
                DIV(self.label, _class="fontawesome-component-left-menu-label"),
                **attributes),
            html_submenus
        ]


class FontawesomeButtonLeftMenuEdit(XmlConstructor):
    def __init__(self, _id, label, icon_class, **attributes):
        self._id = _id
        self.label = label
        self.icon_class = icon_class
        self.submenus = []
        self.componentSubmenu = FontawesomeButtonLeftSubMenu
        initial_class = "fontawesome-component-left-menu"
        initial_id = "fontawesome-component-left-menu-%s" % _id
        self.button_attributes = attributes
        self.button_attributes["_cmd_left_menu"] = "link"
        if "_class" in self.button_attributes:
            self.button_attributes["_class"] = " ".join([
                self.button_attributes['_class'].strip(),
                "fontawesome-component-left-menu-button link"])
        else:
            self.button_attributes["_class"] = "fontawesome-component-left-menu-button link"
        XmlConstructor.__init__(self, 'div', False, _id=initial_id, _class=initial_class)
        self._update_content()

    def addSubmenu(self, _id, label, **attributes):
        self.submenus.append(self.componentSubmenu(_id=_id, label=label, **attributes))
        self._update_content()

    def _update_content(self):
        html_submenus = ""
        attributes = self.button_attributes
        if self.submenus:
            attributes["_target_submenu"] = "fontawesome-component-left-menu-submenu-from-%s" % self._id
            html_submenus = DIV(
                *self.submenus,
                _id=attributes["_target_submenu"],
                _class="fontawesome-component-left-menu-submenu-container")
        self.content = [
            DIV(
                DIV(
                    DIV(
                        I(_class=self.icon_class),
                        DIV(
                            I(_class="fas fa-pen"),
                            _class="fontawesome-component-left-menu-icon-plus"),
                        _class="fontawesome-component-left-menu-icon-plus-container"),
                    _class="fontawesome-component-left-menu-icon-container"),
                DIV(self.label, _class="fontawesome-component-left-menu-label"),
                **attributes),
            html_submenus
        ]


class FontawesomeButtonLeftUserMenu(XmlConstructor):
    def __init__(self, _id, name_user="Nome usuário", url_image_user="/static/images/user.png", **attributes):
        self._id = _id
        self.name_user = name_user
        self.url_image_user = url_image_user
        self.submenus = []
        self._image = IMG(_id="fontawesome-component-left-menu-url-imagem-user",
            _src=url_image_user,
            _alt="user avatar")
        self.componentSubmenu = FontawesomeButtonLeftSubMenu
        initial_class = "fontawesome-component-left-menu"
        initial_id = "fontawesome-component-left-menu-%s" % _id
        self.button_attributes = attributes
        self.button_attributes["_cmd_left_menu"] = "link"
        if "_class" in self.button_attributes:
            self.button_attributes["_class"] = " ".join([
                self.button_attributes['_class'].strip(),
                "fontawesome-component-left-menu-button-user cmp-bar-user-img link"])
        else:
            self.button_attributes["_class"] = "fontawesome-component-left-menu-button link"
        XmlConstructor.__init__(self, 'div', False, _id=initial_id, _class=initial_class)
        self._update_content()

    def addSubmenu(self, _id, label, **attributes):
        self.submenus.append(self.componentSubmenu(_id=_id, label=label, **attributes))
        self._update_content()

    def _update_content(self):
        html_submenus = ""
        attributes = self.button_attributes
        if self.submenus:
            attributes["_target_submenu"] = "fontawesome-component-left-menu-submenu-from-%s" % self._id
            html_submenus = DIV(
                *self.submenus,
                _id=attributes["_target_submenu"],
                _class="fontawesome-component-left-menu-submenu-container")
        self.content = [
            DIV(
                DIV(
                    DIV(self._image,
                        _class="fontawesome-component-left-menu-image-user"),
                    _class="fontawesome-component-left-menu-image-user-container"),
                DIV(self.name_user,
                    _id="fontawesome-component-left-menu-name-user",
                    _class="fontawesome-component-left-menu-label"),
                **attributes),
            html_submenus
        ]
