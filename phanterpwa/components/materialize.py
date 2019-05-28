# -*- coding: utf-8 -*-

from ..helpers import (
    DIV,
    LABEL,
    INPUT,
    I,
    SPAN,
    TEXTAREA,
    SELECT,
    OPTION,
    CONCATENATE,
    UL,
    LI,
    A
)
from ..xmlconstructor import XmlConstructor


class MaterializeInputText(XmlConstructor):

    def __init__(self, inputname, label, id_input=None, default=None, error=None, **attributes):
        if not default:
            default = ""
        else:
            default = str(default)
        if not error:
            error = ""
        else:
            error = str(error)
        if not id_input:
            id_input = "input-%s" % inputname
        attributes["_phanterwebformvalidator_inputname"] = inputname
        attributes["_phanterweb-input"] = id_input
        if "_class" in attributes:
            new_class = " ".join([attributes["_class"].strip(), "materialize-input-text-xmlconstroi"])
            attributes["_class"] = new_class
        else:
            attributes["_class"] = "materialize-input-text-xmlconstroi"
        self.input = INPUT(
            _name=inputname,
            _id=id_input,
            _class="form-control",
            _value=default,
            _type="text"
        )
        new_content = [
            DIV(I("check", _class="material-icons"),
                _id="phanterwebformvalidator-input-check-%s" % inputname,
                _class="phanterwebformvalidator-input-check"),
            DIV(
                self.input,
                LABEL(
                    label,
                    _for=id_input),
                _class="input-field"),
            DIV(error,
                _title=error,
                _id="phanterwebformvalidator-input-error-%s" % inputname,
                _class="phanterwebformvalidator-input-error%s" % (" actived" if error != "" else " deactived")),
        ]
        XmlConstructor.__init__(self, 'div', False, *new_content, **attributes)

    def disable(self):
        self.input.attributes['_disabled'] = ""


class MaterializeChips(XmlConstructor):
    def __init__(self, inputname, label, id_input=None, default="[]", error=None, **attributes):
        if not default:
            default = ""
        else:
            default = str(default)
        if not error:
            error = ""
        else:
            error = str(error)
        if not id_input:
            id_input = "input-%s" % inputname
        attributes["_phanterwebformvalidator_inputname"] = inputname
        attributes["_phanterweb-input"] = id_input
        if "_id" not in attributes:
            attributes['_id'] = "phanterwebchips-jquery_plugin-%s" % inputname
        if "_class" in attributes:
            new_class = " ".join([attributes["_class"].strip(), "materialize-input-chips-xmlconstroi"])
            attributes["_class"] = new_class
        else:
            attributes["_class"] = "materialize-input-chips-xmlconstroi"

        new_content = [
            DIV(I("check", _class="material-icons"),
                _id="phanterwebformvalidator-input-check-%s" % inputname,
                _class="phanterwebformvalidator-input-check"),
            DIV(
                DIV(
                    _id="materialize-input-phanterwebformchips_%s" % inputname,
                    _class="materialize-input-phanterwebformchips"),
                INPUT(
                    _name=inputname,
                    _id=id_input,
                    _class="form-control",
                    _value=default,
                    _type="hidden"),
                LABEL(
                    label,
                    _for=id_input),
                _class="input-field"),
            DIV(error,
                _title=error,
                _id="phanterwebformvalidator-input-error-%s" % inputname,
                _class="phanterwebformvalidator-input-error%s" % (" actived" if error != "" else " deactived")),
            DIV(_id="materialize-input-chips-options-%s" % inputname, _class="materialize-input-chips-options")
        ]
        XmlConstructor.__init__(self, 'div', False, *new_content, **attributes)


class MaterializeSelectWithHideInput(XmlConstructor):
    def __init__(self, inputname, label, id_input=None, default=None, error=None, options=None, **attributes):
        if not default:
            default = ""
        else:
            default = str(default)
        if not error:
            error = ""
        else:
            error = str(error)
        if not id_input:
            id_input = "input-%s" % inputname
        attributes["_phanterwebformvalidator_inputname"] = inputname
        self.general_id = id_input
        self.general_name = inputname
        self.id_button_add_new = "button-%s" % id_input
        self.button_add_new = None
        attributes["_phanterweb-input"] = id_input
        if "_class" in attributes:
            new_class = " ".join([attributes["_class"].strip(), "materialize-input-text-xmlconstroi"])
            attributes["_class"] = new_class
        else:
            attributes["_class"] = "materialize-input-text-xmlconstroi"
        if options is None:
            options = []
        elif isinstance(options, (list, tuple)):
            for x in options:
                if not isinstance(x, (OPTION)):
                    raise TypeError("elements of options must is OPTION instance")
        elif isinstance(options, (dict)):
            new_options = [OPTION("Escolha uma opção", _value=" ", _disabled="", _selected="")]
            for x in options:
                new_options.append(OPTION(options[x], _value="%s" % x))
            options = new_options
        else:
            raise TypeError("options must is tuple, list or None")

        self._html_select = SELECT(
            *options,
            _id="select-%s" % id_input,
            _class="phanterwebformselect-withhiddeninput",
            _target_input=id_input)
        self._html_select_label = LABEL(label, _for="select-%s" % id_input)
        self._html_select_concatenate = CONCATENATE(
            self._html_select,
            self._html_select_label
        )
        self._html_check = DIV(
            I("check", _class="material-icons"),
            _id="phanterwebformvalidator-input-check-%s" % inputname,
            _class="phanterwebformvalidator-input-check actived-select")
        attr_btn_switch = {}
        attr_btn_switch["_target-switch"] = "switch-input-select-container-%s" % self.general_id
        attr_btn_switch["_target-check"] = "phanterwebformvalidator-input-check-%s" % self.general_name
        new_content = [
            self._html_check,
            DIV(
                DIV(
                    INPUT(
                        _name=inputname,
                        _id=id_input,
                        _class="form-control",
                        _value=default,
                        _type="text"),
                    LABEL(
                        label,
                        _for=id_input),
                    DIV(
                        I("details", _class="material-icons"),
                        _class="materilize-button-show-hidde-input-new doinput waves-effect waves-teal btn link",
                        **attr_btn_switch),
                    _id="switch-input-%s" % id_input,
                    _class="input-field switch-input"),
                DIV(
                    self._html_select_concatenate,
                    _id="switch-select-%s" % id_input,
                    _class="input-field switch-select"),
                _id="switch-input-select-container-%s" % id_input,
                _class="switch-input-select-container actived-select"),
            DIV(error,
                _title=error,
                _id="phanterwebformvalidator-input-error-%s" % inputname,
                _class="phanterwebformvalidator-input-error%s" % (" actived" if error != "" else " deactived")),
        ]
        XmlConstructor.__init__(self, 'div', False, *new_content, **attributes)

    def addOptionInSelect(self, value, label_value, **attributes):
        if "_value" in attributes:
            del attributes['_value']
        option = OPTION(label_value, _value=value, **attributes)
        self._html_select.content.append(option)

    def setButtonNew(self, label=None, **attributes):
        if label is None:
            label = I("add", _class="material-icons")
        attributes['_id'] = self.id_button_add_new
        attributes["_target-switch"] = "switch-input-select-container-%s" % self.general_id
        attributes["_target-check"] = "phanterwebformvalidator-input-check-%s" % self.general_name
        class_button = "materilize-button-show-hidde-input-new waves-effect waves-teal btn link"
        self._html_check.attributes["_class"] = " ".join(["hasbutton", self._html_check.attributes["_class"]])
        if "_class" in attributes:
            attributes["_class"] = " ".join([attributes["_class"], class_button])
        else:
            attributes["_class"] = class_button
        self._html_select_concatenate.content = [
            DIV(
                DIV(
                    self._html_select,
                    self._html_select_label,
                    _class="materialize-selectwithinput"),
                DIV(
                    DIV(label, **attributes),
                    _class="materialize-selectwithinput-button"),
                _class="materialize-select-and-button-container"
            )
        ]


class MaterializeInputTextMultiline(XmlConstructor):
    def __init__(self, inputname, label, id_input=None, default=None, error=None, **attributes):
        if not default:
            default = ""
        else:
            default = str(default)
        if not error:
            error = ""
        else:
            error = str(error)
        if not id_input:
            id_input = "input-%s" % inputname
        attributes["_phanterwebformvalidator_inputname"] = inputname
        attributes["_phanterweb-input"] = id_input
        if "_class" in attributes:
            new_class = " ".join([attributes["_class"].strip(), "materialize-input-text-xmlconstroi"])
            attributes["_class"] = new_class
        else:
            attributes["_class"] = "materialize-input-text-xmlconstroi"

        new_content = [
            DIV(I("check", _class="material-icons"),
                _id="phanterwebformvalidator-input-check-%s" % inputname,
                _class="phanterwebformvalidator-input-check"),
            DIV(
                TEXTAREA(
                    _name=inputname,
                    _id=id_input,
                    _class="form-control materialize-textarea",
                    _value=default,
                    _type="text"),
                LABEL(
                    label,
                    _for=id_input),
                _class="input-field"),
            DIV(error,
                _title=error,
                _id="phanterwebformvalidator-input-error-%s" % inputname,
                _class="phanterwebformvalidator-input-error%s" % (" actived" if error != "" else " deactived")),
        ]
        XmlConstructor.__init__(self, 'div', False, *new_content, **attributes)


class MaterializeInputHidden(XmlConstructor):
    def __init__(self, inputname, label, id_input=None, default=None, error=None, **attributes):
        if not default:
            default = ""
        else:
            default = str(default)
        if not error:
            error = ""
        else:
            error = str(error)
        if not id_input:
            id_input = "input-%s" % inputname
        attributes["_phanterwebformvalidator_inputname"] = inputname
        attributes["_phanterweb-input"] = id_input
        if "_class" in attributes:
            new_class = " ".join([attributes["_class"].strip(), "materialize-input-hidden-xmlconstroi"])
            attributes["_class"] = new_class
        else:
            attributes["_class"] = "materialize-input-hidden-xmlconstroi"

        new_content = [
            DIV(I("check", _class="material-icons"),
                _id="phanterwebformvalidator-input-check-%s" % inputname,
                _class="phanterwebformvalidator-input-check"),
            DIV(
                INPUT(
                    _name=inputname,
                    _id=id_input,
                    _class="form-control",
                    _value=default,
                    _type="hidden"),
                LABEL(
                    label,
                    _for=id_input),
                _class="input-field"),
            DIV(error,
                _title=error,
                _id="phanterwebformvalidator-input-error-%s" % inputname,
                _class="phanterwebformvalidator-input-error%s" % (" actived" if error != "" else " deactived")),
        ]
        XmlConstructor.__init__(self, 'div', False, *new_content, **attributes)


class MaterializeInputPassword(XmlConstructor):
    def __init__(self, inputname, label, id_input=None, default=None, error="", **attributes):
        if not default:
            default = ""
        else:
            default = str(default)
        if not error:
            error = ""
        else:
            error = str(error)
        if not id_input:
            id_input = "input-%s" % inputname
        attributes["_phanterwebformvalidator_inputname"] = inputname
        attributes["_phanterweb-input"] = id_input
        if "_class" in attributes:
            new_class = " ".join([attributes["_class"].strip(), "materialize-input-password-xmlconstroi"])
            attributes["_class"] = new_class
        else:
            attributes["_class"] = "materialize-input-password-xmlconstroi"

        new_content = [
            DIV(I("check", _class="material-icons"),
                _id="phanterwebformvalidator-input-check-%s" % inputname,
                _class="phanterwebformvalidator-input-check"),
            DIV(
                INPUT(
                    _name=inputname,
                    _id=id_input,
                    _class="form-control",
                    _value=default,
                    _type="password"),
                LABEL(
                    label,
                    _for=id_input),
                _class="input-field"),
            DIV(error,
                _title=error,
                _id="phanterwebformvalidator-input-error-%s" % inputname,
                _class="phanterwebformvalidator-input-error%s" % (" actived" if error != "" else " deactived")),
        ]
        XmlConstructor.__init__(self, 'div', False, *new_content, **attributes)


class MaterializeInputCheckBox(XmlConstructor):
    def __init__(self, inputname, label, id_input=None, disabled=False, checked=False, filledIn=False, **attributes):
        if not id_input:
            id_input = "input-%s" % inputname
        attributes["_phanterwebformvalidator_inputname"] = inputname
        if "_class" in attributes:
            new_class = " ".join([attributes["_class"].strip(), "materialize-input-checkbox-xmlconstroi"])
            attributes["_class"] = new_class
        else:
            attributes["_class"] = "materialize-input-checkbox-xmlconstroi"
        new_content = [
            DIV(
                LABEL(
                    INPUT(
                        _name=inputname,
                        _id=id_input,
                        _class="form-control%s" % (" filled-in" if filledIn else ""),
                        _checked="checked" if checked else None,
                        _disabled="disabled" if disabled else None,
                        _type="checkbox"),
                    SPAN(label),
                ),
                _class="input-field-checkbox"),
        ]
        XmlConstructor.__init__(self, 'div', False, *new_content, **attributes)


class MaterializeButtonForm(XmlConstructor):
    def __init__(self, _id, label, **attributes):
        self.label = label
        initial_class = "phanterweb-materialize-button-form-container"
        attributes["_id"] = _id
        self.button_attributes = attributes
        if "_class" in self.button_attributes:
            self.button_attributes["_class"] = " ".join([
                self.button_attributes['_class'].strip(),
                "btn phanterweb-materialize-button-form link"])
        else:
            self.button_attributes["_class"] = "btn phanterweb-materialize-button-form link"
        if "_title" not in self.button_attributes:
            self.button_attributes["_title"] = self.label

        XmlConstructor.__init__(self, 'div', False, _class=initial_class)
        self._update_content()

    def _update_content(self):
        attributes = self.button_attributes
        self.content = [
            DIV(
                DIV(self.label, **attributes),
                _class="button-form")
        ]


class MaterializePreloaderCircle(XmlConstructor):
    def __init__(self, _id, size=None, color=None, **attributes):
        self.size = size
        self.color = color
        self.initial_class = ""
        if "_class" in attributes:
            self.initial_class = attributes['_class'].strip()
        XmlConstructor.__init__(self, 'div', False, **attributes)
        self._update_content()

    def _update_content(self):
        new_size = ""
        if self.size:
            new_size = " %s" % self.size
        attr = self.attributes
        if self.initial_class:
            attr['_class'] = "".join([self.initial_class, " preloader-wrapper active", new_size])
        else:
            attr['_class'] = "preloader-wrapper active%s" % new_size
        self.attributes = attr
        if self.color:
            if self.color == "red":
                self.content = [self._base_spinner("spinner-red-only")]
            elif self.color == "blue":
                self.content = [self._base_spinner("spinner-blue-only")]
            elif self.color == "yellow":
                self.content = [self._base_spinner("spinner-yellow-only")]
            elif self.color == "green":
                self.content = [self._base_spinner("spinner-green-only")]
        else:
            content = []
            default_colors = ["spinner-blue", "spinner-red", "spinner-yellow", "spinner-green"]
            for x in default_colors:
                content.append(self._base_spinner(x))
            self.content = content
        return self.content

    @staticmethod
    def _base_spinner(class_color):
        html_base = DIV(
            DIV(
                DIV(_class="circle"),
                _class="circle-clipper left"),
            DIV(
                DIV(_class="circle"),
                _class="gap-patch"),
            DIV(
                DIV(_class="circle"),
                _class="circle-clipper right"),
            _class="spinner-layer %s" % class_color)
        return html_base

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if (value is None) or (value == "medium"):
            self._size = ""
        elif value == "big":
            self._size = "big"
        elif value == "small":
            self._size = "smal"
        else:
            raise ValueError("The size must is big, small or medium (or None Type)")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if (value is None) or (value == "multicolor"):
            self._color = None
        elif value == "red":
            self._color = "red"
        elif value == "blue":
            self._color = "blue"
        elif value == "green":
            self._color = "green"
        elif value == "yellow":
            self._color = "yellow"
        else:
            raise ValueError("The color must is big, small or medium (or None Type)")


class MaterializeSearchBar(XmlConstructor):
    def __init__(
            self,
            inputname,
            fields_to_select=None,
            label="Pesquisar",
            field_select_label="Campo de pesquisa",
            **attributes
        ):
        self.field_select = field_select_label
        self.inputname = inputname
        id_input = "materialize-searchbar-input-%s" % inputname

        if "_class" in attributes:
            new_class = " ".join([attributes["_class"].strip(), "materialize-searchbar-xmlconstroi"])
            attributes["_class"] = new_class
        else:
            attributes["_class"] = "materialize-searchbar-xmlconstroi"
        self.select_search_container = CONCATENATE()
        self.select_search = None
        self.input_search = DIV(
            DIV(
                INPUT(
                    _name=inputname,
                    _id=id_input,
                    _class="form-control",
                    _type="text"),
                LABEL(
                    label,
                    _for=id_input),
                _class="input-field"),
            DIV(
                I("search", _class="material-icons"),
                _source_search=id_input,
                _source_select="materialize-select-search-%s" % inputname,
                _id="materialize-searchbar-button-%s" % inputname,
                _class="waves-effect waves-teal btn link materialize-searchbar-button"),

            _id='materialize-searchbar-input-and-button-%s' % inputname,
            _class='materialize-searchbar-input-and-button'
        )
        new_content = [
            CONCATENATE(
                DIV(
                    self.input_search,
                    self.select_search_container,
                    _class="row")
            )
        ]
        XmlConstructor.__init__(self, 'div', False, *new_content, **attributes)

    def addOptionInSelect(self, value, label_value, **attributes):
        if not self.select_search_container.content:
            self.input_search.attributes["_class"] = " ".join([
                "has_select col s12 m8 l8",
                self.input_search.attributes["_class"]])
            self.select_search = SELECT(
                _id="materialize-select-search-%s" % self.inputname,
                _class="materialize-select-search")
            select_container = DIV(
                self.select_search,
                LABEL(self.field_select, _for="materialize-select-search-%s" % self.inputname),
                _class="input-field")
            self.select_search_container.content = [
                DIV(
                    select_container,
                    _class="materialize-searchbar-select col s12 m4 l4")
            ]
        self.select_search.append(OPTION(label_value, _value=value, **attributes))

    def showSelect(self):
        if not self.select_search_container.content and self.select_search is None:
            self.input_search.attributes["_class"] = " ".join([
                "has_select col s12 m8 l8",
                self.input_search.attributes["_class"]])
            self.select_search = SELECT(
                _id="materialize-select-search-%s" % self.inputname,
                _class="materialize-select-search")
            select_container = DIV(
                self.select_search,
                LABEL(self.field_select, _for="materialize-select-search-%s" % self.inputname),
                _class="input-field")
            self.select_search_container.content = [
                DIV(
                    select_container,
                    _class="materialize-searchbar-select col s12 m4 l4")
            ]


class MaterializeFloatButton(XmlConstructor):
    def __init__(self, icon_name="build", **attributes):
        if "_class" in attributes:
            new_class = " ".join([
                attributes["_class"].strip(),
                "materialize-floating-action-button-xmlconstroi"
            ])
            attributes["_class"] = new_class
        else:
            attributes["_class"] = "materialize-floating-action-button-xmlconstroi"
        self.buttons_floating = UL()
        self.principal_icon = CONCATENATE(
            A(
                I(icon_name, _class="large material-icons"),
                _class="btn-floating btn-large blue waves-effect waves-light")
        )
        new_content = [
            DIV(
                self.principal_icon,
                self.buttons_floating,
                _class="fixed-action-btn click-to-toggle")
        ]
        XmlConstructor.__init__(self, 'div', False, *new_content, **attributes)

    def addMaterializeActionButton(self, material_icon_name, color="blue", **attributes):
        if '_class' in attributes:
            attributes['_class'] = " ".join(["btn-floating %s" % color, attributes['_class']])
        else:
            attributes['_class'] = "btn-floating %s" % color
        self.buttons_floating.append(LI(A(I(material_icon_name, _class="material-icons"), **attributes)))

    def changePrincipalMaterializeActionButton(self, material_icon_name, color="blue", **attributes):
        if '_class' in attributes:
            attributes['_class'] = " ".join(["btn-floating %s" % color, attributes['_class']])
        else:
            attributes['_class'] = "btn-floating %s" % color
        self.principal_icon.content = [
            A(I(material_icon_name, _class="material-icons"), **attributes)]

    def addActionButton(self, personal_icon, color="blue", **attributes):
        if '_class' in attributes:
            attributes['_class'] = " ".join(["btn-floating %s" % color, attributes['_class']])
        else:
            attributes['_class'] = "btn-floating %s" % color
        self.buttons_floating.append(LI(A(personal_icon, **attributes)))

    def changePrincipalActionButton(self, personal_icon, color="blue", **attributes):
        if '_class' in attributes:
            attributes['_class'] = " ".join(["btn-floating %s" % color, attributes['_class']])
        else:
            attributes['_class'] = "btn-floating %s" % color
        self.principal_icon.content = [
            A(personal_icon, **attributes)]


class MaterializeTabs(XmlConstructor):
    def __init__(self, **attributes):
        if "_class" in attributes:
            new_class = " ".join([attributes["_class"].strip(), "materialize-tabs-xmlconstroi row"])
            attributes["_class"] = new_class
        else:
            attributes["_class"] = "materialize-tabs-xmlconstroi row"
        self.tabs_menu = UL(_class="tabs")
        self.tabs = CONCATENATE()
        self.tabs_elements = []
        new_content = [
            CONCATENATE(
                DIV(
                    self.tabs_menu,
                    _class="col s12"),
                self.tabs
            )
        ]
        XmlConstructor.__init__(self, 'div', False, *new_content, **attributes)

    def addTab(self, id_tab, title, content, actived=False, disabled=False, **attributes):
        class_base = "materialize-tab-menu tab"
        if disabled:
            class_base = "materialize-tab-menu tab disabled"
        if "_class" in attributes:
            attributes["_class"] = " ".join([class_base, attributes["_class"]])
        else:
            attributes["_class"] = " ".join([class_base, attributes["_class"]])
        element_menu = LI(A(title, _href="#%s" % id_tab), **attributes)
        element_tab = DIV(content, _id=id_tab, _class="col s12")
        self.tabs_elements.append([element_menu, element_tab])
        self.tabs_menu.content = []
        self.tabs.content = []
        for x in self.tabs_elements:
            self.tabs_menu.append(x[0])
            self.tabs.append(x[1])
