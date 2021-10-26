from phanterpwa.frontend import (
    helpers
)
from phanterpwa.frontend import fmasks as masks
# pragmas
from phanterpwa.frontend.components import datetimepicker as datetimepicker
from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = Array = document = localStorage = M = RegExp = setTimeout =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')

I18N = helpers.I18N
XML = helpers.XML
CONCATENATE = helpers.CONCATENATE
FORM = helpers.XmlConstructor.tagger("form", False)
SPAN = helpers.XmlConstructor.tagger("span", False)
DIV = helpers.XmlConstructor.tagger("div", False)
I = helpers.XmlConstructor.tagger("i", False)
INPUT = helpers.XmlConstructor.tagger("input", True)
HR = helpers.XmlConstructor.tagger("hr", True)
LABEL = helpers.XmlConstructor.tagger("label", False)
TEXTAREA = helpers.XmlConstructor.tagger("textarea", False)
SELECT = helpers.XmlConstructor.tagger("select", False)
OPTION = helpers.XmlConstructor.tagger("option", False)
UL = helpers.XmlConstructor.tagger("ul", False)
LI = helpers.XmlConstructor.tagger("li", False)
TH = helpers.XmlConstructor.tagger("th", False)
TD = helpers.XmlConstructor.tagger("td", False)
TR = helpers.XmlConstructor.tagger("tr", False)
SCRIPT = helpers.XmlConstructor.tagger("script", False)
TABLE = helpers.XmlConstructor.tagger("table", False)

__pragma__('kwargs')


class Widget(helpers.XmlConstructor):
    def __init__(self, identifier, *content, **attributes):
        self.actived = False
        self.identifier = identifier
        if self.identifier is js_undefined or self.identifier is None:
            raise ValueError("The identifier is invalid!")
        self._identifier = window.PhanterPWA.get_id(identifier)
        attributes["_id"] = "phanterpwa-widget-{0}".format(self.identifier)
        attributes["_phanterpwa-widget"] = self.identifier
        if "_class" in attributes:
            attributes["_class"] = "{0}{1}".format(attributes["_class"], " phanterpwa-widget")
        else:
            attributes["_class"] = "phanterpwa-widget"
        window.PhanterPWA._thewidgets[self._identifier] = self
        content.append(SCRIPT("window.PhanterPWA._thewidgets['{0}'].start()".format(self._identifier), _type="text/javascript"))
        helpers.XmlConstructor.__init__(self, 'phanterpwa-widget', False, *content, **attributes)
        self.target_selector = "#phanterpwa-widget-{0}".format(
            self.identifier
        )
        window.PhanterPWA.Request.add_widget(self)

    def _reload(self):
        if not window.PhanterPWA.check_event_namespace(
                jQuery(self.target_selector), "phanterpwa_widget", self.identifier):
            jQuery(
                self.target_selector
            ).off(
                "phanterpwa_widget.{0}".format(self.identifier)
            ).on(
                "phanterpwa_widget.{0}".format(self.identifier),
                lambda: self.reload()
            )
            jQuery(self.target_selector).trigger("phanterpwa_widget")

    def get_message_error(self):
        if self._message_error is not None:
            return self._message_error
        else:
            return ""

    def set_message_error(self, message_error):
        if message_error is not None:
            jQuery(self.target_selector).find(
                ".phanterpwa-widget-message_error").html(message_error)
            jQuery(self.target_selector).find(
                ".phanterpwa-widget-wrapper").addClass("has_error")
        self._message_error = message_error

    def del_message_error(self):
        self.set_message_error(None)
        jQuery(self.target_selector).find(
            ".phanterpwa-widget-wrapper").removeClass("has_error")

    def reload(self):
        if window.PhanterPWA.DEBUG:
            console.info("the reload not used")

    def start(self):
        if window.PhanterPWA.DEBUG:
            console.info("the start not used")


class Input(Widget):
    def __init__(self, identifier, **parameters):
        self._label = parameters.get("label", None)
        self._placeholder = parameters.get("placeholder", None)
        self._name = parameters.get("name", None)
        self._value = parameters.get("value", "")
        self._icon = parameters.get("icon", None)
        self._message_error = parameters.get("message_error", None)
        self._can_empty = parameters.get("can_empty", False)
        self._validator = parameters.get("validators", None)
        self._wear = parameters.get("wear", "material")
        self._kind = parameters.get("kind", "text")
        self._mask = parameters.get("mask", "")
        self._form = parameters.get("form", None)
        self._format = parameters.get("format", None)
        self._icon_on_click = parameters.get("icon_on_click", None)
        self._onload = parameters.get("onLoad", None)
        self._checker = parameters.get("checker", True)
        self._disabled = parameters.get("disabled", None)
        self._on_date_datetime_choice = parameters.get("onDateorDatetimeChoice", None)
        wrapper_attr = {
            "_class": "phanterpwa-widget-wrapper phanterpwa-widget-input-wrapper phanterpwa-widget-wear-{0}".format(
                self._wear)
        }
        parameters["_id"] = identifier
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-input")
        else:
            parameters['_class'] = "phanterpwa-widget-input"
        n_type = ["date", "datetime", "password", "hidden"]
        if self._kind in n_type:
            if self._kind == "datetime":
                self._type = "text"
                if self._format is None:
                    self._format = "yyyy-MM-dd HH:ss:mm"
                self._mask = masks.date_and_datetime_to_maks(self._format)
            elif self._kind == "date":
                self._type = "text"
                if self._format is None:
                    self._format = "yyyy-MM-dd"
                self._mask = masks.date_and_datetime_to_maks(self._format)
            elif self._kind == "password":
                self._type = "password"
            elif self._kind == "hidden":
                parameters["_class"] = "{0}{1}".format(parameters["_class"], " e-display_hidden")
        else:
            self._type = "text"
        if self._mask == "fone":
            self._maks = masks.maskFone(self._value)
        label = ""
        if self._label is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_label")
            label = LABEL(self._label, _for="phanterpwa-widget-input-input-{0}".format(identifier))

        if self._message_error is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_error")
        xml_icon = ""
        if self._icon is not None:
            xml_icon = DIV(self._icon, _class="phanterpwa-widget-icon-wrapper icon_button wave_on_click")
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_icon")
        if self._value is not "":
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_value")
        if self._mask is not "" and self._mask is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_mask")

        checker = ""
        if self._checker:
            checker = DIV(
                I(_class="fas fa-check"),
                _class="phanterpwa-widget-check"
            )
            if self._disabled is not None:
                checker = DIV(
                    I(_class="fas fa-lock"),
                    _class="phanterpwa-widget-check"
                )

        html = DIV(
            INPUT(**{
                "_id": "phanterpwa-widget-input-input-{0}".format(identifier),
                "_class": "phanterpwa-widget-input-input",
                "_name": self._name,
                "_value": self._value,
                "_placeholder": self._placeholder,
                "_disabled": self._disabled,
                "_type": self._type,
                "_data-validators": JSON.stringify(self._validator),
                "_data-form": self._form,
            }),
            label,
            checker,
            xml_icon,
            DIV(
                self.get_message_error(),
                _class="phanterpwa-widget-message_error phanterpwa-widget-input-message_error"
            ),
            **wrapper_attr
        )
        Widget.__init__(self, identifier, html, **parameters)

    def get_message_error(self):
        if self._message_error is not None:
            return self._message_error
        else:
            return ""

    def set_message_error(self, message_error):
        if message_error is not None:
            jQuery(self.target_selector).find(
                ".phanterpwa-widget-message_error").html(message_error)
            jQuery(self.target_selector).find(
                ".phanterpwa-widget-wrapper").addClass("has_error")
        self._message_error = message_error

    def del_message_error(self):
        self.set_message_error(None)
        jQuery(self.target_selector).find(
            ".phanterpwa-widget-wrapper").removeClass("has_error")

    def validate(self):
        if callable(self._validator):
            self._validator(self)

    def _add_div_animation(self, el):
        wrapper = el.find(".phanterpwa-widget-wrapper")
        if wrapper.hasClass("phanterpwa-widget-wear-material"):
            if wrapper.find(".material-widgets-animation-onfocus").length == 0:
                wrapper.find("input").after(
                    CONCATENATE(
                        HR(_class="material-widgets-animation-offfocus"),
                        DIV(_class="material-widgets-animation-onfocus")
                    ).jquery()
                )

    def _check_value(self, el):
        el = jQuery(el)
        p = el.parent()
        if el.val() is not "":
            p.addClass("has_value").trigger("keyup")
        else:
            p.removeClass("has_value")

    def _on_click_icon(self, el):
        if callable(self._icon_on_click):
            self._icon_on_click(el)
        elif self._kind == "date":
            self._datetimepicker = datetimepicker.Datepickers(
                self.target_selector,
                **{"date_type": "date", "format": self._format,
                "onChoice": self._on_date_datetime_choice,
                "id_input_target": jQuery(self.target_selector).find("input")}
            )
            self._datetimepicker.start()
        elif self._kind == "datetime":
            self._datetimepicker = datetimepicker.Datepickers(
                self.target_selector,
                **{"date_type": "datetime", "format": self._format,
                "onChoice": self._on_date_datetime_choice,
                "id_input_target": jQuery(self.target_selector).find("input")}
            )
            self._datetimepicker.start()
        elif self._kind == "password":
            el = jQuery("#phanterpwa-widget-input-input-{0}".format(self.identifier))
            if el.attr("type") == "password":
                el.attr("type", "text")
            else:
                el.attr("type", "password")

    def _on_click_label(self, el):
        el = jQuery(el)
        p = el.parent()
        if not p.hasClass("focus"):
            p.find("input").focus().trigger("focus")

    def _switch_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        p.removeClass("has_error")
        if el.js_is(":focus"):
            jQuery(".phanterpwa-widget-wrapper").removeClass("focus").removeClass("pre_focus")
            p.addClass("focus")
        else:
            p.removeClass("focus")
        self._check_value(el)

    def _remove_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        if el.js_is(":focus"):
            p.addClass("focus")
        else:
            p.removeClass("focus")
        self._check_value(el)

    def reload(self):

        self.start()

    def _binds(self):
        target = jQuery(self.target_selector)
        self._add_div_animation(target)

        target.find("input").off("focus.phanterpwa-event-input_materialize").on(
            "focus.phanterpwa-event-input_materialize",
            lambda: self._switch_focus(this)
        )
        target.find("input").off("focusout.phanterpwa-event-input_materialize").on(
            "focusout.phanterpwa-event-input_materialize",
            lambda: self._switch_focus(this)
        )
        target.find("input").off("change.phanterpwa-event-input_materialize").on(
            "change.phanterpwa-event-input_materialize",
            lambda: self._check_value(this)
        )
        target.find("label").off("click.phanterpwa-event-input_materialize, touchstart.phanterpwa-event-input_materialize").on(
            "click.phanterpwa-event-input_materialize, touchstart.phanterpwa-event-input_materialize",
            lambda: self._on_click_label(this)
        )
        if self._mask is not "" and self._mask is not None:
            if self._mask == "fone":
                masks.Mask(target.find("input")["selector"], lambda val: masks.maskFone(val))
            else:
                masks.Mask(target.find("input")["selector"], lambda val: masks.baseCustom(val, self._mask))

        if self._icon is not None:
            target.find(".phanterpwa-widget-icon-wrapper").off("click.phanterpwa-widget-icon-wrapper").on(
                "click.phanterpwa-widget-icon-wrapper",
                lambda: self._on_click_icon(this)
            )
        if callable(self._onload):
            self._onload(target)

    def set_disabled(self):
        jQuery("#phanterpwa-widget-input-input-{0}".format(self.identifier)).attr("disabled", "disabled").prop("disabled")
        self._disabled = "disabled"
        if self._checker:
            jQuery("#phanterpwa-widget-input-input-{0}".format(self.identifier)).parent().find(
                ".phanterpwa-widget-check"
            ).html(I(_class="fas fa-lock").jquery())

    def set_enabled(self):
        jQuery("#phanterpwa-widget-input-input-{0}".format(self.identifier)).removeAttr("disabled")
        self._disabled = None
        if self._checker:
            jQuery("#phanterpwa-widget-input-input-{0}".format(self.identifier)).parent().find(
                ".phanterpwa-widget-check"
            ).html(I(_class="fas fa-check").jquery())

    def start(self):
        self._binds()

    def value(self):
        self._value = jQuery("#phanterpwa-widget-input-input-{0}".format(self.identifier)).val()
        return self._value


class Select(Widget):
    def __init__(self, identifier, **parameters):
        self.identifier = identifier
        self._alias_value = ""
        self._value = parameters.get("value", "")
        self._data_set(parameters.get("data_set", []))
        self._label = parameters.get("label", None)
        self._placeholder = parameters.get("placeholder", None)
        self._name = parameters.get("name", None)
        self._editable = parameters.get("editable", False)
        self._icon = parameters.get("icon", None)
        self._message_error = parameters.get("message_error", None)
        self._can_empty = parameters.get("can_empty", False)
        self._validator = parameters.get("validators", None)
        self._wear = parameters.get("wear", "material")
        self._form = parameters.get("form", None)
        self._icon_option = parameters.get("icon_option", I(_class="far fa-circle"))
        self._icon_option_selected = parameters.get("icon_option_selected", I(_class="far fa-dot-circle"))
        self._icon_plus = parameters.get("icon_plus", I(_class="fas fa-plus"))
        self._icon_confirm = parameters.get("icon_confirm", I(_class="fas fa-check"))
        self._icon_check = parameters.get("icon_check", I(_class="fas fa-check"))
        self._on_click_new = parameters.get("on_click_new_button", None)
        self.set_z_index(parameters.get("z_index", None))
        self.set_recalc_on_scroll(parameters.get("recalc_on_scroll", True))
        xml_icon = ""
        if self._icon is not "":
            xml_icon = DIV(self._icon, _class="phanterpwa-widget-icon-wrapper")
        wrapper_attr = {
            "_class": "phanterpwa-widget-wrapper phanterpwa-widget-select-wrapper phanterpwa-widget-wear-{0}".format(
                self._wear)
        }
        parameters["_id"] = identifier
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-select")
        else:
            parameters['_class'] = "phanterpwa-widget-select"
        label = ""
        if self._label is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_label")
            label = LABEL(
                self._label, _for="phanterpwa-widget-select-input-{0}".format(identifier),
                _class="phanterpwa-widget-select-label"
            )

        if self._message_error is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_error")

        if self._icon is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_icon")
        if self._value is not "":
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_value")
        select = SELECT(_class="phanterpwa-widget-select-select", _name=self._name)
        table = TABLE(_class="phanterpwa-widget-select-options-wrapper")
        self._xml_modal = table
        self._xml_select = select
        self._create_xml_select()
        self._create_xml_modal()
        html = DIV(
            INPUT(**{
                "_id": "phanterpwa-widget-select-input-{0}".format(identifier),
                "_value": self._alias_value,
                "_placeholder": self._placeholder,
                "_disabled": "disabled",
                "_data-validators": JSON.stringify(self._validator),
                "_data-form": self._form,
                "_name": self._name
            }),
            label,
            DIV(
                I(_class="fas fa-angle-down"),
                _class="phanterpwa-widget-select-caret"
            ),
            xml_icon,
            DIV(
                I(_class="fas fa-check"),
                _class="phanterpwa-widget-check"
            ),
            DIV(_class="phanterpwa-widget-select-touchpad", _tabindex="0"),
            self._xml_select,
            DIV(
                self.get_message_error(),
                _class="phanterpwa-widget-message_error phanterpwa-widget-select-message_error"
            ),
            **wrapper_attr
        )
        Widget.__init__(self, identifier, html, **parameters)

    def set_recalc_on_scroll(self, value):
        if isinstance(value, bool):
            self._recalc_on_scroll = value
        else:
            console.error("The recalc_on_scroll must be boolean!")

    def set_z_index(self, value):
        if str(value).isdigit():
            self._z_index = value
        elif value is None:
            self._z_index = None
        else:
            self._z_index = None
            console.error("The z_index must be integer or None!")

    def _data_set(self, data):
        valid_data = True
        self._data = []
        self._data_dict = {}
        if isinstance(data, list):
            new_data = []
            for vdata in data:
                if isinstance(vdata, str):
                    if self._value == vdata:
                        self._alias_value = vdata
                    self._data_dict[vdata] = vdata
                    new_data.append([vdata, vdata])
                elif len(vdata) is not 2:
                    valid_data = False
                else:
                    if self._value == vdata[0]:
                        self._alias_value = vdata[1]
                    self._data_dict[vdata[0]] = vdata[1]
                    new_data.append([vdata[0], vdata[1]])
            if not valid_data:
                raise ValueError("The data parameter of widget \"{0}\" is invalid!".format(
                    self.identifier
                ))
            else:
                self._data = new_data
        elif isinstance(data, dict):
            new_data = []
            for vdata in data.keys():
                new_data.append([vdata, data[vdata]])
                if self._value == vdata:
                    self._alias_value = data[vdata]
            self._data = new_data
            self._data_dict = data

    def _create_xml_select(self):
        has_default = False
        select = SELECT(**{"_class": "phanterpwa-widget-select-select", "_name": self._name})
        if self._data is not []:
            for vdata in self._data:
                if self._value is not "":
                    if vdata[0] == self._value:
                        has_default = True
                        select.append(OPTION(vdata[1], _value=vdata[0], _selected="selected"))
                    else:
                        select.append(OPTION(vdata[1], _value=vdata[0]))
                else:
                    select.append(OPTION(vdata[1], _value=vdata[0]))
            if self._can_empty:
                if self._placeholder is not None:
                    select.insert(0, OPTION(
                        self._placeholder,
                        _value="",
                        _selected="selected" if not has_default else None))
                else:
                    select.insert(0, OPTION(
                        "",
                        _value="",
                        _selected="selected" if not has_default else None))
        self._xml_select = select

    def _create_xml_modal(self):
        table = TABLE(_class="phanterpwa-widget-select-options-wrapper")
        if self._data is not []:
            if self._can_empty:
                if self._value is "":
                    icon_empty = DIV(self._icon_option_selected, _class="phanterpwa-widget-select-li-icon")
                else:
                    icon_empty = DIV(self._icon_option, _class="phanterpwa-widget-select-li-icon")

                table.append(TR(TD(SPAN(I18N("Empty")),
                    icon_empty, **{
                        "_data-value": "",
                        "_data-target": "phanterpwa-widget-select-input-{0}".format(self.identifier),
                        "_data-text": "",
                        "_class": "phanterpwa-widget-select-li-option empty"
                })))
            for vdata in self._data:
                if self._value is not "":
                    if vdata[0] == self._value:
                        table.append(TR(TD(SPAN(vdata[1]),
                            DIV(self._icon_option_selected, _class="phanterpwa-widget-select-li-icon"), **{
                                "_data-value": vdata[0],
                                "_data-text": vdata[1],
                                "_data-target": "phanterpwa-widget-select-input-{0}".format(self.identifier),
                                "_class": "phanterpwa-widget-select-li-option selected"
                        })))

                    else:
                        table.append(TR(TD(SPAN(vdata[1]),
                            DIV(self._icon_option, _class="phanterpwa-widget-select-li-icon"), **{
                                "_data-value": vdata[0],
                                "_data-text": vdata[1],
                                "_data-target": "phanterpwa-widget-select-input-{0}".format(self.identifier),
                                "_class": "phanterpwa-widget-select-li-option"
                        })))
                else:
                    table.append(TR(TD(SPAN(vdata[1]),
                        DIV(self._icon_option, _class="phanterpwa-widget-select-li-icon"), **{
                            "_data-value": vdata[0],
                            "_data-text": vdata[1],
                            "_data-target": "phanterpwa-widget-select-input-{0}".format(self.identifier),
                            "_class": "phanterpwa-widget-select-li-option"
                    })))
            icon_placeholder = DIV(
                DIV(
                    DIV(self._icon_plus, _class="link phanterpwa-widget-select-li-icon_plus"),
                    DIV(
                        INPUT(_class="phanterpwa-widget-select-li-input"),
                        DIV(self._icon_confirm, _class="phanterpwa-widget-select-li-icon_confirm link"),
                        _class="phanterpwa-widget-select-li-input-editable"
                    ),
                    _class="phanterpwa-widget-select-li-input-editable-wrapper"
                ),
                _class="phanterpwa-widget-select-li-icon_plus-wrapper"
            )

            if self._placeholder is not None:
                if self._editable:
                    table.insert(0, TR(TD(SPAN(self._placeholder, _class="phanterpwa-widget-select-placeholder"),
                        icon_placeholder, **{
                            "_data-value": "",
                            "_data-target": "phanterpwa-widget-select-input-{0}".format(self.identifier),
                            "_data-text": "",
                            "_class": "phanterpwa-widget-select-li-title has_editable"
                    })))
                else:
                    table.insert(0, TR(TD(SPAN(self._placeholder, _class="phanterpwa-widget-select-placeholder"),
                        "", **{
                            "_data-value": "",
                            "_data-target": "phanterpwa-widget-select-input-{0}".format(self.identifier),
                            "_data-text": "",
                            "_class": "phanterpwa-widget-select-li-title"
                    })))
            else:
                if self._editable:
                    table.insert(0, TR(TD(SPAN(self._placeholder, _class="phanterpwa-widget-select-placeholder"),
                        icon_placeholder, **{
                            "_data-value": "",
                            "_data-target": "phanterpwa-widget-select-input-{0}".format(self.identifier),
                            "_data-text": "",
                            "_class": "phanterpwa-widget-select-li-title has_editable"
                    })))
        self._xml_modal = table

    # def get_message_error(self):
    #     if self._message_error is not None:
    #         return self._message_error
    #     else:
    #         return ""

    # def set_message_error(self, message_error):
    #     jQuery("#{0}".format(self.identifier)).find(".phanterpwa-widget-message_error").html(message_error)
    #     jQuery("#{0}".format(self.identifier)).addClass("has_error")
    #     self._message_error

    # def del_message_error(self):
    #     self.set_message_error("")
    #     jQuery("#{0}".format(self.identifier)).removeClass("has_error")

    def validate(self):
        if callable(self._validator):
            self._validator(self)
        self.focus = False
        self.has_val = None

    def _add_div_animation(self, el):
        wrapper = el.find(".phanterpwa-widget-wrapper")
        if wrapper.hasClass("phanterpwa-widget-wear-material"):
            if wrapper.find(".material-widgets-animation-onfocus").length == 0:
                wrapper.find("input").after(
                    CONCATENATE(
                        HR(_class="material-widgets-animation-offfocus"),
                        DIV(_class="material-widgets-animation-onfocus")
                    ).jquery()
                )

    def _check_value(self, el):
        el = jQuery(el)
        p = el.parent()
        if p.find("input").val() is not "":
            p.addClass("has_value")
        else:
            p.removeClass("has_value")
        p.find("input").trigger("keyup")

    def _on_click_label(self, el):
        el = jQuery(el)
        self._switch_focus(el)

    def _after_modal_close(self, p):
        parent = jQuery(p).removeClass("focus")
        self._check_value(parent.find("input"))

    def _switch_pre_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        p.removeClass("has_error")
        if p.hasClass("pre_focus"):
            p.removeClass("pre_focus")
        else:
            jQuery(".phanterpwa-widget-select-wrapper").removeClass("pre_focus")
            p.addClass("pre_focus")

    def open_modal(self, el):

        self.modal = PseudoModal(
            "#phanterpwa-widget-select-input-{0}".format(self.identifier),
            self._xml_modal,
            on_close=lambda: self._after_modal_close(el),
            width="100%",
            z_index=self._z_index,
            recalc_on_scroll=self._recalc_on_scroll
        )
        self.modal.start()
        self._binds_modal_content()

    def _switch_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        stat_modal = jQuery(
            "#phanterpwa-widget-select-input-{0}".format(self.identifier)).attr("phanterpwa-widget-pseudomodal")
        if p.hasClass("focus"):
            p.removeClass("focus")
            p.removeClass("pre_focus")
            if self.modal is not None and self.modal is not js_undefined:
                if callable(self.modal.close):
                    self.modal.close()
        else:
            if stat_modal != "enabled":
                jQuery(".phanterpwa-widget-select-wrapper").removeClass("focus").removeClass("pre_focus")
                p.addClass("focus")
                setTimeout(lambda: self.open_modal(p), 30)
        self._check_value(el)

    def _remove_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        if el.js_is(":focus"):
            p.addClass("focus")
        else:
            p.removeClass("focus")
        self._check_value(el)

    def reload(self):
        self.start()

    def add_new_value(self, value):
        new_value = value
        if new_value is not "":
            has_value = False
            for vdata in self._data:
                if vdata[1] == new_value:
                    has_value = True
                    break
            if not has_value:
                new_key = "${0}:{1}".format(__new__(Date().getTime()), new_value)
                self._data.append([new_key, new_value])
                self._value = new_key
                self._alias_value = new_value
                jQuery("#phanterpwa-widget-select-input-{0}".format(self.identifier)).val(new_value)
                jQuery("#phanterpwa-widget-select-input-{0}".format(self.identifier)).trigger("change")
                target = jQuery(self.target_selector)
                target.find("select.phanterpwa-widget-select-select").find("option").removeAttr("selected")

                target.find("select.phanterpwa-widget-select-select").append(
                    OPTION(new_value, _value=new_key, _selected="selected").jquery()
                )
                target.find("select.phanterpwa-widget-select-select").find(
                    "option[value='{0}']".format(new_key)).attr(
                        "selected", "selected").prop('selected', True).text(new_value)
                self._create_xml_modal()
                self._check_value()
        else:
            if self._can_empty:
                target = jQuery(self.target_selector)
                target.find("select.phanterpwa-widget-select-select").find("option").removeAttr("selected")
                target.find("select.phanterpwa-widget-select-select").find(
                        "option[value='']").attr("selected", "selected").prop('selected', True)

    def _add_new_option(self, el):
        inp = jQuery(el).parent().find("input")
        new_value = jQuery(inp).val()
        self.add_new_value(new_value)
        self.modal.close()

    def _process_option(self, el):
        p = jQuery(el).parent()
        p.find(".phanterpwa-widget-select-li-icon").html(XML(self._icon_option).jquery())
        jQuery(el).find(".phanterpwa-widget-select-li-icon").html(XML(self._icon_option_selected).jquery())
        t = jQuery(el).data("target")
        v = jQuery(el).data("value")
        h = jQuery(el).data("text")
        target = jQuery(self.target_selector)
        dkeys = {str(k[0]): k[1] for k in self._data}
        if str(v) in dkeys.keys():
            self._value = v
            target.find("select.phanterpwa-widget-select-select").find("option").removeAttr("selected")
            target.find("select.phanterpwa-widget-select-select").find(
                "option[value='{0}']".format(v)).attr("selected", "selected").prop('selected', True)
            jQuery("#{0}".format(t)).val(h)
            self._alias_value = h
        elif v is not "":
            target.find("select.phanterpwa-widget-select-select").find("option").removeAttr("selected")
            dkeys[v] = h
            target.find("select.phanterpwa-widget-select-select").append(
                OPTION(h, _value=v, _selected="selected").jquery()
            )
            target.find("select.phanterpwa-widget-select-select").find(
                "option[value='{0}']".format(v)).attr("selected", "selected").prop('selected', True)
            jQuery("#{0}".format(t)).val(h)
            self._value = v
            self._alias_value = h
        elif self._can_empty:
            target.find("select.phanterpwa-widget-select-select").find("option").removeAttr("selected")
            target.find("select.phanterpwa-widget-select-select").find(
                "option[value='']").attr("selected", "selected").prop('selected', True)
            self._value = ""
            jQuery("#{0}".format(t)).val("")
            self._alias_value = ""

        if self.modal is not None and self.modal is not js_undefined:
            if callable(self.modal.close):
                self.modal.close()
        self._create_xml_modal()
        self._check_value()
        jQuery("#{0}".format(t)).trigger("change")

    def _binds(self):
        target = jQuery(self.target_selector)
        self._add_div_animation(target)
        target.find(".phanterpwa-widget-select-touchpad").off("click.phanterpwa-event-input_materialize").on(
            "click.phanterpwa-event-input_materialize",
            lambda: self._switch_focus(this)
        )
        target.find(".phanterpwa-widget-select-touchpad").off("focus.phanterpwa-event-input_materialize").on(
            "focus.phanterpwa-event-input_materialize",
            lambda: self._switch_pre_focus(this)
        )
        target.find(".phanterpwa-widget-select-touchpad").off("focusout.phanterpwa-event-input_materialize").on(
            "focusout.phanterpwa-event-input_materialize",
            lambda: self._switch_pre_focus(this)
        )
        target.find("input").off("change.phanterpwa-event-input_materialize").on(
            "change.phanterpwa-event-input_materialize",
            lambda: self._check_value(this)
        )
        target.find("label").off("click.phanterpwa-event-input_materialize").on(
            "click.phanterpwa-event-input_materialize",
            lambda: target.find(".phanterpwa-widget-select-touchpad").trigger("click")
        )
        target.find(".phanterpwa-widget-select-touchpad").off("keydown.open_by_key").on(
            "keydown.open_by_key",
            lambda event: self._open_by_key(event, this)
        )

    def _open_by_key(self, event, el):
        code = event.keyCode or event.which
        p = jQuery(el).parent()
        stat_modal = jQuery(
            "#phanterpwa-widget-select-input-{0}".format(self.identifier)).attr("phanterpwa-widget-pseudomodal")
        if code == 40:
            event.preventDefault()
            #self.open_modal(p)
            if stat_modal != "enabled":
                jQuery(".phanterpwa-widget-select-wrapper").removeClass("focus").removeClass("pre_focus")
                p.addClass("focus")
                setTimeout(lambda: self.open_modal(p), 30)
        elif code == 27:
            p.addClass("pre_focus")
            if self.modal is not None and self.modal is not js_undefined:
                if callable(self.modal.close):
                    self.modal.close()
        elif code == 9:
            # if self.modal is not js_undefined:
            #     self.modal.close()
            p.removeClass("focus")
            p.removeClass("pre_focus")
            if self.modal is not None and self.modal is not js_undefined:
                if callable(self.modal.close):
                    self.modal.close()
        self._check_value(el)

    def set_on_click_new_button(self, value):
        if callable(value):
            self._on_click_new = value
        else:
            console.error("The 'on_click_new_butto' value must be callable.")

    def _switch_editable(self, el):
        if callable(self._on_click_new):
            self._on_click_new(self)
        else:
            p = jQuery(el).parent().parent()
            pp = p.parent()
            if p.hasClass("enabled"):
                p.removeClass("enabled")
                pp.removeClass("editable_enabled")
            else:
                jQuery(el).parent().find("input").focus()
                p.addClass("enabled")
                pp.addClass("editable_enabled")

    def _binds_modal_content(self):
        jQuery(".phanterpwa-component-pseudomodal-content").find(
            ".phanterpwa-widget-select-li-option"
        ).off(
            "click.option_select_modal_content"
        ).on(
            "click.option_select_modal_content",
            lambda: self._process_option(this)
        )
        if self._editable:
            jQuery(".phanterpwa-component-pseudomodal-content").find(
                ".phanterpwa-widget-select-li-icon_plus"
            ).off(
                "click.option_select_modal_content"
            ).on(
                "click.option_select_modal_content",
                lambda: self._switch_editable(this)
            )
            jQuery(".phanterpwa-component-pseudomodal-content").find(
                ".phanterpwa-widget-select-li-icon_confirm"
            ).off(
                "click.option_select_modal_content"
            ).on(
                "click.option_select_modal_content",
                lambda: self._add_new_option(this)
            )

    def start(self):
        self._binds()

    def value(self):
        return self._value

    def alias_value(self):
        return self._alias_value


class Autocomplete(Widget):
    def __init__(self, identifier, **parameters):
        self.identifier = identifier
        self._alias_value = ""
        self._value = parameters.get("value", "")
        self._data_set(parameters.get("data_set", []))
        self._label = parameters.get("label", None)
        self._placeholder = parameters.get("placeholder", None)
        self._name = parameters.get("name", None)
        self._editable = parameters.get("editable", False)
        self._icon = parameters.get("icon", None)
        self._message_error = parameters.get("message_error", None)
        self._can_empty = parameters.get("can_empty", False)
        self._validator = parameters.get("validators", None)
        self._wear = parameters.get("wear", "material")
        self._form = parameters.get("form", None)
        self._icon_option = parameters.get("icon_option", I(_class="far fa-circle"))
        self._icon_option_selected = parameters.get("icon_option_selected", I(_class="far fa-dot-circle"))
        self._icon_plus = parameters.get("icon_plus", I(_class="fas fa-plus"))
        self._icon_confirm = parameters.get("icon_confirm", I(_class="fas fa-check"))
        self._icon_check = parameters.get("icon_check", I(_class="fas fa-check"))
        self._on_click_new = parameters.get("on_click_new_button", None)
        self.set_z_index(parameters.get("z_index", None))
        self.set_recalc_on_scroll(parameters.get("recalc_on_scroll", True))
        xml_icon = ""
        if self._icon is not "":
            xml_icon = DIV(self._icon, _class="phanterpwa-widget-icon-wrapper")
        wrapper_attr = {
            "_class": "phanterpwa-widget-wrapper phanterpwa-widget-autocomplete-wrapper phanterpwa-widget-wear-{0}".format(
                self._wear)
        }
        parameters["_id"] = identifier
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-autocomplete")
        else:
            parameters['_class'] = "phanterpwa-widget-autocomplete"
        label = ""
        if self._label is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_label")
            label = LABEL(
                self._label, _for="phanterpwa-widget-autocomplete-input-{0}".format(identifier),
                _class="phanterpwa-widget-autocomplete-label"
            )

        if self._message_error is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_error")

        if self._icon is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_icon")
        if self._value is not "":
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_value")
        select = SELECT(_class="phanterpwa-widget-autocomplete-select", _name=self._name)
        table = TABLE(_class="phanterpwa-widget-autocomplete-options-wrapper")
        self._xml_modal = table
        self._xml_select = select
        self._create_xml_select()
        self._create_xml_modal()
        html = DIV(
            INPUT(**{
                "_id": "phanterpwa-widget-autocomplete-input-{0}".format(identifier),
                "_value": self._alias_value,
                "_placeholder": self._placeholder,
                "_disabled": "disabled",
                "_data-validators": JSON.stringify(self._validator),
                "_data-form": self._form,
                "_name": self._name
            }),
            label,
            DIV(
                I(_class="fab fa-sistrix"),
                _class="phanterpwa-widget-autocomplete-caret"
            ),
            xml_icon,
            DIV(
                I(_class="fas fa-check"),
                _class="phanterpwa-widget-check"
            ),
            DIV(_class="phanterpwa-widget-autocomplete-touchpad", _tabindex="0"),
            self._xml_select,
            DIV(
                self.get_message_error(),
                _class="phanterpwa-widget-message_error phanterpwa-widget-autocomplete-message_error"
            ),
            **wrapper_attr
        )
        Widget.__init__(self, identifier, html, **parameters)

    def set_recalc_on_scroll(self, value):
        if isinstance(value, bool):
            self._recalc_on_scroll = value
        else:
            console.error("The recalc_on_scroll must be boolean!")

    def set_z_index(self, value):
        if str(value).isdigit():
            self._z_index = value
        elif value is None:
            self._z_index = None
        else:
            self._z_index = None
            console.error("The z_index must be integer or None!")

    def _data_set(self, data):
        valid_data = True
        self._data = []
        self._data_dict = {}
        if isinstance(data, list):
            new_data = []
            for vdata in data:
                if isinstance(vdata, str):
                    if self._value == vdata:
                        self._alias_value = vdata
                    self._data_dict[vdata] = vdata
                    new_data.append([vdata, vdata])
                elif len(vdata) is not 2:
                    valid_data = False
                else:
                    if self._value == vdata[0]:
                        self._alias_value = vdata[1]
                    self._data_dict[vdata[0]] = vdata[1]
                    new_data.append([vdata[0], vdata[1]])
            if not valid_data:
                raise ValueError("The data parameter of widget \"{0}\" is invalid!".format(
                    self.identifier
                ))
            else:
                self._data = new_data
        elif isinstance(data, dict):
            new_data = []
            for vdata in data.keys():
                new_data.append([vdata, data[vdata]])
                if self._value == vdata:
                    self._alias_value = data[vdata]
            self._data = new_data
            self._data_dict = data

    def _create_xml_select(self):
        has_default = False
        select = SELECT(**{"_class": "phanterpwa-widget-autocomplete-select", "_name": self._name})
        if self._data is not []:
            for vdata in self._data:
                if self._value is not "":
                    if vdata[0] == self._value:
                        has_default = True
                        select.append(OPTION(vdata[1], _value=vdata[0], _selected="selected"))
                    else:
                        select.append(OPTION(vdata[1], _value=vdata[0]))
                else:
                    select.append(OPTION(vdata[1], _value=vdata[0]))
            if self._can_empty:
                if self._placeholder is not None:
                    select.insert(0, OPTION(
                        self._placeholder,
                        _value="",
                        _selected="selected" if not has_default else None))
                else:
                    select.insert(0, OPTION(
                        "",
                        _value="",
                        _selected="selected" if not has_default else None))
        self._xml_select = select

    def _create_xml_modal(self):
        table = TABLE(_class="phanterpwa-widget-autocomplete-options-wrapper")
        if self._data is not []:
            if self._can_empty:
                if self._value is "":
                    icon_empty = DIV(self._icon_option_selected, _class="phanterpwa-widget-autocomplete-li-icon")
                else:
                    icon_empty = DIV(self._icon_option, _class="phanterpwa-widget-autocomplete-li-icon")

                table.append(TR(TD(SPAN(I18N("Empty")),
                    icon_empty, **{
                        "_data-value": "",
                        "_data-target": "phanterpwa-widget-autocomplete-input-{0}".format(self.identifier),
                        "_data-text": "",
                        "_tabindex": "0",
                        "_class": "phanterpwa-widget-autocomplete-li-option empty"
                })))
            for vdata in self._data:
                if self._value is not "":
                    if vdata[0] == self._value:
                        table.append(TR(TD(SPAN(vdata[1]),
                            DIV(self._icon_option_selected, _class="phanterpwa-widget-autocomplete-li-icon"), **{
                                "_data-value": vdata[0],
                                "_data-text": vdata[1],
                                "_data-target": "phanterpwa-widget-autocomplete-input-{0}".format(self.identifier),
                                "_tabindex": "0",
                                "_class": "phanterpwa-widget-autocomplete-li-option selected"
                        })))

                    else:
                        table.append(TR(TD(SPAN(vdata[1]),
                            DIV(self._icon_option, _class="phanterpwa-widget-autocomplete-li-icon"), **{
                                "_data-value": vdata[0],
                                "_data-text": vdata[1],
                                "_data-target": "phanterpwa-widget-autocomplete-input-{0}".format(self.identifier),
                                "_tabindex": "0",
                                "_class": "phanterpwa-widget-autocomplete-li-option"
                        })))
                else:
                    table.append(TR(TD(SPAN(vdata[1]),
                        DIV(self._icon_option, _class="phanterpwa-widget-autocomplete-li-icon"), **{
                            "_data-value": vdata[0],
                            "_data-text": vdata[1],
                            "_data-target": "phanterpwa-widget-autocomplete-input-{0}".format(self.identifier),
                            "_tabindex": "0",
                            "_class": "phanterpwa-widget-autocomplete-li-option"
                    })))
            icon_placeholder = DIV(
                DIV(
                    DIV(self._icon_plus, _class="link phanterpwa-widget-autocomplete-li-icon_plus"),
                    DIV(
                        INPUT(_class="phanterpwa-widget-autocomplete-li-input"),
                        DIV(self._icon_confirm, _class="phanterpwa-widget-autocomplete-li-icon_confirm link"),
                        _class="phanterpwa-widget-autocomplete-li-input-editable"
                    ),
                    _class="phanterpwa-widget-autocomplete-li-input-editable-wrapper"
                ),
                _class="phanterpwa-widget-autocomplete-li-icon_plus-wrapper"
            )

            if self._placeholder is not None:
                if self._editable:
                    table.insert(0, TR(TD(SPAN(self._placeholder, _class="phanterpwa-widget-autocomplete-placeholder"),
                        icon_placeholder, **{
                            "_data-value": "",
                            "_data-target": "phanterpwa-widget-autocomplete-input-{0}".format(self.identifier),
                            "_data-text": "",
                            "_tabindex": "0",
                            "_class": "phanterpwa-widget-autocomplete-li-title has_editable"
                    })))
                else:
                    table.insert(0, TR(TD(SPAN(self._placeholder, _class="phanterpwa-widget-autocomplete-placeholder"),
                        "", **{
                            "_data-value": "",
                            "_data-target": "phanterpwa-widget-autocomplete-input-{0}".format(self.identifier),
                            "_data-text": "",
                            "_tabindex": "0",
                            "_class": "phanterpwa-widget-autocomplete-li-title"
                    })))
            else:
                if self._editable:
                    table.insert(0, TR(TD(SPAN(self._placeholder, _class="phanterpwa-widget-autocomplete-placeholder"),
                        icon_placeholder, **{
                            "_data-value": "",
                            "_data-target": "phanterpwa-widget-autocomplete-input-{0}".format(self.identifier),
                            "_data-text": "",
                            "_tabindex": "0",
                            "_class": "phanterpwa-widget-autocomplete-li-title has_editable"
                    })))
        self._xml_modal = table

    # def get_message_error(self):
    #     if self._message_error is not None:
    #         return self._message_error
    #     else:
    #         return ""

    # def set_message_error(self, message_error):
    #     jQuery("#{0}".format(self.identifier)).find(".phanterpwa-widget-message_error").html(message_error)
    #     jQuery("#{0}".format(self.identifier)).addClass("has_error")
    #     self._message_error

    # def del_message_error(self):
    #     self.set_message_error("")
    #     jQuery("#{0}".format(self.identifier)).removeClass("has_error")

    def validate(self):
        if callable(self._validator):
            self._validator(self)
        self.focus = False
        self.has_val = None

    def _add_div_animation(self, el):
        wrapper = el.find(".phanterpwa-widget-wrapper")
        if wrapper.hasClass("phanterpwa-widget-wear-material"):
            if wrapper.find(".material-widgets-animation-onfocus").length == 0:
                wrapper.find("input").after(
                    CONCATENATE(
                        HR(_class="material-widgets-animation-offfocus"),
                        DIV(_class="material-widgets-animation-onfocus")
                    ).jquery()
                )

    def _check_value(self, el):
        el = jQuery(el)
        p = el.parent()
        if p.find("input").val() is not "":
            p.addClass("has_value")
        else:
            p.removeClass("has_value")
        p.find("input").trigger("keyup")

    def _on_click_label(self, el):
        el = jQuery(el)
        self._switch_focus(el)

    def _after_modal_close(self, p):
        parent = jQuery(p).removeClass("focus")
        self._check_value(parent.find("input"))

    def _switch_pre_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        p.removeClass("has_error")
        if p.hasClass("pre_focus"):
            p.removeClass("pre_focus")
        else:
            jQuery(".phanterpwa-widget-autocomplete-wrapper").removeClass("pre_focus")
            p.addClass("pre_focus")

    def open_modal(self, el):

        self.modal = PseudoModal(
            "#phanterpwa-widget-autocomplete-input-{0}".format(self.identifier),
            self._xml_modal,
            on_close=lambda: self._after_modal_close(el),
            width="100%",
            z_index=self._z_index,
            recalc_on_scroll=self._recalc_on_scroll
        )
        self.modal.start()
        self._binds_modal_content()

    def _switch_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        stat_modal = jQuery(
            "#phanterpwa-widget-autocomplete-input-{0}".format(self.identifier)).attr("phanterpwa-widget-pseudomodal")
        if p.hasClass("focus"):
            p.removeClass("focus")
            p.removeClass("pre_focus")
            if self.modal is not None and self.modal is not js_undefined:
                if callable(self.modal.close):
                    self.modal.close()
        else:
            if stat_modal != "enabled":
                jQuery(".phanterpwa-widget-autocomplete-wrapper").removeClass("focus").removeClass("pre_focus")
                p.addClass("focus")
                setTimeout(lambda: self.open_modal(p), 30)
        self._check_value(el)

    def _remove_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        if el.js_is(":focus"):
            p.addClass("focus")
        else:
            p.removeClass("focus")
        self._check_value(el)

    def reload(self):
        self.start()

    def add_new_value(self, value):
        new_value = value
        if new_value is not "":
            has_value = False
            for vdata in self._data:
                if vdata[1] == new_value:
                    has_value = True
                    break
            if not has_value:
                new_key = "${0}:{1}".format(__new__(Date().getTime()), new_value)
                self._data.append([new_key, new_value])
                self._value = new_key
                self._alias_value = new_value
                jQuery("#phanterpwa-widget-autocomplete-input-{0}".format(self.identifier)).val(new_value)
                jQuery("#phanterpwa-widget-autocomplete-input-{0}".format(self.identifier)).trigger("change")
                target = jQuery(self.target_selector)
                target.find("select.phanterpwa-widget-autocomplete-select").find("option").removeAttr("selected")

                target.find("select.phanterpwa-widget-autocomplete-select").append(
                    OPTION(new_value, _value=new_key, _selected="selected").jquery()
                )
                target.find("select.phanterpwa-widget-autocomplete-select").find(
                    "option[value='{0}']".format(new_key)).attr(
                        "selected", "selected").prop('selected', True).text(new_value)
                self._create_xml_modal()
                self._check_value()
        else:
            if self._can_empty:
                target = jQuery(self.target_selector)
                target.find("select.phanterpwa-widget-autocomplete-select").find("option").removeAttr("selected")
                target.find("select.phanterpwa-widget-autocomplete-select").find(
                        "option[value='']").attr("selected", "selected").prop('selected', True)

    def _add_new_option(self, el):
        inp = jQuery(el).parent().find("input")
        new_value = jQuery(inp).val()
        self.add_new_value(new_value)
        self.modal.close()

    def _process_option(self, el):
        p = jQuery(el).parent()
        p.find(".phanterpwa-widget-autocomplete-li-icon").html(XML(self._icon_option).jquery())
        jQuery(el).find(".phanterpwa-widget-autocomplete-li-icon").html(XML(self._icon_option_selected).jquery())
        t = jQuery(el).data("target")
        v = jQuery(el).data("value")
        h = jQuery(el).data("text")
        target = jQuery(self.target_selector)
        dkeys = {str(k[0]): k[1] for k in self._data}
        if str(v) in dkeys.keys():
            self._value = v
            target.find("select.phanterpwa-widget-autocomplete-select").find("option").removeAttr("selected")
            target.find("select.phanterpwa-widget-autocomplete-select").find(
                "option[value='{0}']".format(v)).attr("selected", "selected").prop('selected', True)
            jQuery("#{0}".format(t)).val(h)
            self._alias_value = h
        elif v is not "":
            target.find("select.phanterpwa-widget-autocomplete-select").find("option").removeAttr("selected")
            dkeys[v] = h
            target.find("select.phanterpwa-widget-autocomplete-select").append(
                OPTION(h, _value=v, _selected="selected").jquery()
            )
            target.find("select.phanterpwa-widget-autocomplete-select").find(
                "option[value='{0}']".format(v)).attr("selected", "selected").prop('selected', True)
            jQuery("#{0}".format(t)).val(h)
            self._value = v
            self._alias_value = h
        elif self._can_empty:
            target.find("select.phanterpwa-widget-autocomplete-select").find("option").removeAttr("selected")
            target.find("select.phanterpwa-widget-autocomplete-select").find(
                "option[value='']").attr("selected", "selected").prop('selected', True)
            self._value = ""
            jQuery("#{0}".format(t)).val("")
            self._alias_value = ""

        if self.modal is not None and self.modal is not js_undefined:
            if callable(self.modal.close):
                self.modal.close()
        self._create_xml_modal()
        self._check_value()
        jQuery("#{0}".format(t)).trigger("change")

    def _binds(self):
        target = jQuery(self.target_selector)
        self._add_div_animation(target)
        target.find(".phanterpwa-widget-autocomplete-touchpad").off("click.phanterpwa-event-input_materialize").on(
            "click.phanterpwa-event-input_materialize",
            lambda: self._switch_focus(this)
        )
        target.find(".phanterpwa-widget-autocomplete-touchpad").off("focus.phanterpwa-event-input_materialize").on(
            "focus.phanterpwa-event-input_materialize",
            lambda: self._switch_pre_focus(this)
        )
        target.find(".phanterpwa-widget-autocomplete-touchpad").off("focusout.phanterpwa-event-input_materialize").on(
            "focusout.phanterpwa-event-input_materialize",
            lambda: self._switch_pre_focus(this)
        )
        target.find("input").off("change.phanterpwa-event-input_materialize").on(
            "change.phanterpwa-event-input_materialize",
            lambda: self._check_value(this)
        )
        target.find("label").off("click.phanterpwa-event-input_materialize").on(
            "click.phanterpwa-event-input_materialize",
            lambda: target.find(".phanterpwa-widget-autocomplete-touchpad").trigger("click")
        )
        target.find(".phanterpwa-widget-autocomplete-touchpad").off("keydown.open_by_key").on(
            "keydown.open_by_key",
            lambda event: self._open_by_key(event, this)
        )
    def _on_modal_keypress(self, event):
        code = event.keyCode or event.which
        console.log(code)

    def _open_by_key(self, event, el):
        code = event.keyCode or event.which
        console.log(code)
        p = jQuery(el).parent()
        stat_modal = jQuery(
            "#phanterpwa-widget-autocomplete-input-{0}".format(self.identifier)).attr("phanterpwa-widget-pseudomodal")
        if code == 40:
            event.preventDefault()
            #self.open_modal(p)
            if stat_modal != "enabled":
                jQuery(".phanterpwa-widget-autocomplete-wrapper").removeClass("focus").removeClass("pre_focus")
                p.addClass("focus")
                setTimeout(lambda: self.open_modal(p), 30)
        elif code == 27:
            p.addClass("pre_focus")
            if self.modal is not None and self.modal is not js_undefined:
                if callable(self.modal.close):
                    self.modal.close()
        elif code == 9:
            # if self.modal is not js_undefined:
            #     self.modal.close()
            p.removeClass("focus")
            p.removeClass("pre_focus")
            if self.modal is not None and self.modal is not js_undefined:
                if callable(self.modal.close):
                    self.modal.close()
        self._check_value(el)

    def set_on_click_new_button(self, value):
        if callable(value):
            self._on_click_new = value
        else:
            console.error("The 'on_click_new_butto' value must be callable.")

    def _switch_editable(self, el):
        if callable(self._on_click_new):
            self._on_click_new(self)
        else:
            p = jQuery(el).parent().parent()
            pp = p.parent()
            if p.hasClass("enabled"):
                p.removeClass("enabled")
                pp.removeClass("editable_enabled")
            else:
                jQuery(el).parent().find("input").focus()
                p.addClass("enabled")
                pp.addClass("editable_enabled")

    def _binds_modal_content(self):
        jQuery(".phanterpwa-component-pseudomodal-content").find(
            ".phanterpwa-widget-autocomplete-li-option"
        ).off(
            "click.option_select_modal_content"
        ).on(
            "click.option_select_modal_content",
            lambda: self._process_option(this)
        )
        if self._editable:
            jQuery(".phanterpwa-component-pseudomodal-content").find(
                ".phanterpwa-widget-autocomplete-li-icon_plus"
            ).off(
                "click.option_select_modal_content"
            ).on(
                "click.option_select_modal_content",
                lambda: self._switch_editable(this)
            )
            jQuery(".phanterpwa-component-pseudomodal-content").find(
                ".phanterpwa-widget-autocomplete-li-icon_confirm"
            ).off(
                "click.option_select_modal_content"
            ).on(
                "click.option_select_modal_content",
                lambda: self._add_new_option(this)
            )
        jQuery(
            jQuery(
                ".phanterpwa-component-pseudomodal-content"
            ).find(
                ".phanterpwa-widget-autocomplete-li-option"
            )[0]
        ).focus()

    def start(self):
        self._binds()

    def value(self):
        return self._value

    def alias_value(self):
        return self._alias_value


class MultSelect(Widget):
    def __init__(self, identifier, **parameters):
        self.identifier = identifier
        self._alias_value = ""
        self._value = parameters.get("value", [])
        self._filter_value()
        self._data_set(parameters.get("data_set", []))
        self._label = parameters.get("label", None)
        self._placeholder = parameters.get("placeholder", None)
        self._name = parameters.get("name", None)
        self._editable = parameters.get("editable", False)
        self._icon = parameters.get("icon", None)
        self._message_error = parameters.get("message_error", None)
        self._can_empty = parameters.get("can_empty", False)
        self._validator = parameters.get("validators", None)
        self._wear = parameters.get("wear", "material")
        self._form = parameters.get("form", None)
        self._icon_option = parameters.get("icon_option", I(_class="far fa-square"))
        self._icon_option_selected = parameters.get("icon_option_selected", I(_class="far fa-check-square"))
        self._icon_plus = parameters.get("icon_plus", I(_class="fas fa-plus"))
        self._icon_confirm = parameters.get("icon_confirm", I(_class="fas fa-check"))
        self._icon_check = parameters.get("icon_check", I(_class="fas fa-check"))
        self._on_click_new = parameters.get("on_click_new_button", None)
        self.set_z_index(parameters.get("z_index", None))
        self.set_recalc_on_scroll(parameters.get("recalc_on_scroll", True))
        xml_icon = ""
        if self._icon is not "":
            xml_icon = DIV(self._icon, _class="phanterpwa-widget-icon-wrapper")
        wrapper_attr = {
            "_class": "phanterpwa-widget-wrapper phanterpwa-widget-wear-{0}{1}".format(
                self._wear,
                " phanterpwa-widget-multselect-wrapper"
            )
        }
        parameters["_id"] = identifier
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-multselect")
        else:
            parameters['_class'] = "phanterpwa-widget-multselect"
        label = ""
        if self._label is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_label")
            label = LABEL(
                self._label, _for="phanterpwa-widget-multselect-value-{0}".format(identifier),
                _class="phanterpwa-widget-multselect-label"
            )

        if self._message_error is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_error")

        if self._icon is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_icon")
        if len(self._value) > 0:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_value")
        select = SELECT(_class="phanterpwa-widget-multselect-select", _name="name_select_{0}".format(self._name))
        table = TABLE(_class="phanterpwa-widget-multselect-options-wrapper")
        self._xml_modal = table
        self._xml_select = select
        self._create_xml_select()
        self._create_xml_modal()
        self._create_xml_values()
        html = DIV(
            DIV(_class="phanterpwa-widget-multselect-touchpad", _tabindex="0"),
            DIV(
                self._xml_values,
                **{
                    "_id": "phanterpwa-widget-multselect-value-{0}".format(self.identifier),
                    "_class": "phanterpwa-widget-multselect-values"
                }
            ),
            INPUT(**{
                "_id": "phanterpwa-widget-multselect-input-{0}".format(identifier),
                "_class": "phanterpwa-widget-multselect-input",
                "_name": self._name,
                "_value": JSON.stringify(self._value),
                "_placeholder": self._placeholder,
                "_type": "hidden",
                "_data-validators": JSON.stringify(self._validator),
                "_data-form": self._form,
            }),

            label,
            DIV(
                I(_class="fas fa-angle-down"),
                _class="phanterpwa-widget-multselect-caret"
            ),
            xml_icon,
            DIV(
                I(_class="fas fa-check"),
                _class="phanterpwa-widget-check"
            ),
            self._xml_select,
            DIV(
                self.get_message_error(),
                _class="phanterpwa-widget-message_error phanterpwa-widget-multselect-message_error"
            ),
            **wrapper_attr
        )
        Widget.__init__(self, identifier, html, **parameters)

    def _filter_value(self):
        v = []
        if Array.isArray(self._value) or isinstance(self._value, list):
            for x in self._value:
                v.append(str(x))
            self._value = v
        else:
            self._value = [str(self._value)]

    def set_recalc_on_scroll(self, value):
        if isinstance(value, bool):
            self._recalc_on_scroll = value
        else:
            console.error("The recalc_on_scroll must be boolean!")

    def set_z_index(self, value):
        if str(value).isdigit():
            self._z_index = value
        elif value is None:
            self._z_index = None
        else:
            self._z_index = None
            console.error("The z_index must be integer or None!")

    def _data_set(self, data):
        valid_data = True
        self._data = []
        self._order_in = []
        self._data_dict = {}
        self._alias_value = {}
        if isinstance(data, list):
            for vdata in data:
                if len(vdata) is not 2:
                    valid_data = False
                else:
                    if str(vdata[0]) in self._value:
                        self._alias_value[str(vdata[0])] = vdata[1]
                self._data_dict[str(vdata[0])] = vdata[1]
                if str(vdata[0]) not in self._order_in:
                    self._order_in.append(str(vdata[0]))
            if not valid_data:
                raise ValueError("The data parameter of widget \"{0}\" is invalid!".format(
                    self.identifier
                ))
            else:
                self._data = data
        elif isinstance(data, dict):
            self._order_in = []
            new_data = []
            for vdata in data.keys():
                if str(vdata) not in self._order_in:
                    self._order_in.append(str(vdata))
                new_data.append([str(vdata), data[vdata]])
                if str(vdata) in self._value:
                    self._alias_value[str(vdata)] = data[vdata]
            self._data = new_data
            self._data_dict = data

    def _create_xml_values(self):
        values_op = CONCATENATE()
        if len(self._data_dict.keys()) > 0:
            for vdata in self._order_in:
                vdata = str(vdata)
                if len(self._value) > 0:
                    if vdata in self._value:
                        values_op.append(DIV(
                            DIV(self._data_dict[vdata], _class="phanterpwa-widget-multselect-value"),
                            DIV(I(_class="fas fa-times"),
                                _class="phanterpwa-widget-multselect-value-icon_close icon_button wave_on_click"),
                            **{
                                "_data-value": vdata,
                                "_class": "phanterpwa-widget-multselect-value-content",
                                "_tabindex": "0"
                            }
                        ))
        self._xml_values = values_op

    def _create_xml_select(self):
        select = SELECT(**{"_class": "phanterpwa-widget-multselect-select", "_name": "name_select_{0}".format(self._name), "_multiple": True})
        if len(self._data_dict.keys()) > 0:
            for vdata in self._order_in:
                vdata = str(vdata)
                if len(self._value) > 0:
                    if vdata in self._value:
                        select.append(OPTION(self._data_dict[vdata], _value=vdata, _selected="selected"))
                    else:
                        select.append(OPTION(self._data_dict[vdata], _value=vdata))
                else:
                    select.append(OPTION(self._data_dict[vdata], _value=vdata))
        self._xml_select = select

    def _create_xml_modal(self):
        ul = TABLE(_class="phanterpwa-widget-multselect-options-wrapper")
        if len(self._order_in) > 0:

            for vdata in self._order_in:
                vdata = str(vdata)
                if len(self._value) > 0:
                    if vdata in self._value:
                        ul.append(TR(TD(SPAN(self._data_dict[vdata]),
                            DIV(self._icon_option_selected, _class="phanterpwa-widget-multselect-li-icon"), **{
                                "_data-value": vdata,
                                "_data-text": self._data_dict[vdata],
                                "_data-target": "phanterpwa-widget-multselect-value-{0}".format(self.identifier),
                                "_class": "phanterpwa-widget-multselect-li-option selected",
                                "_phanterpwa-widget-multiselect-status": "enabled",
                        })))

                    else:
                        ul.append(TR(TD(SPAN(self._data_dict[vdata]),
                            DIV(self._icon_option, _class="phanterpwa-widget-multselect-li-icon"), **{
                                "_data-value": vdata,
                                "_data-text": self._data_dict[vdata],
                                "_data-target": "phanterpwa-widget-multselect-value-{0}".format(self.identifier),
                                "_class": "phanterpwa-widget-multselect-li-option"
                        })))
                else:
                    ul.append(TR(TD(SPAN(self._data_dict[vdata]),
                        DIV(self._icon_option, _class="phanterpwa-widget-multselect-li-icon"), **{
                            "_data-value": vdata,
                            "_data-text": self._data_dict[vdata],
                            "_data-target": "phanterpwa-widget-multselect-value-{0}".format(self.identifier),
                            "_class": "phanterpwa-widget-multselect-li-option"
                    })))
            icon_placeholder = DIV(
                DIV(
                    DIV(self._icon_plus, _class="link phanterpwa-widget-multselect-li-icon_plus"),
                    DIV(
                        INPUT(_class="phanterpwa-widget-multselect-li-input"),
                        DIV(self._icon_confirm, _class="phanterpwa-widget-multselect-li-icon_confirm link"),
                        _class="phanterpwa-widget-multselect-li-input-editable"
                    ),
                    _class="phanterpwa-widget-multselect-li-input-editable-wrapper"
                ),
                _class="phanterpwa-widget-multselect-li-icon_plus-wrapper"
            )

            if self._placeholder is not None:
                if self._editable:
                    ul.insert(0, TR(TD(SPAN(self._placeholder, _class="phanterpwa-widget-multselect-placeholder"),
                        icon_placeholder, **{
                            "_data-value": "",
                            "_data-target": "phanterpwa-widget-multselect-value-{0}".format(self.identifier),
                            "_data-text": "",
                            "_class": "phanterpwa-widget-multselect-li-title has_editable"
                    })))
                else:
                    ul.insert(0, TR(TD(SPAN(self._placeholder, _class="phanterpwa-widget-multselect-placeholder"),
                        "", **{
                            "_data-value": "",
                            "_data-target": "phanterpwa-widget-multselect-value-{0}".format(self.identifier),
                            "_data-text": "",
                            "_class": "phanterpwa-widget-multselect-li-title"
                    })))
            else:
                if self._editable:
                    ul.insert(0, TR(TD(SPAN(self._placeholder, _class="phanterpwa-widget-multselect-placeholder"),
                        icon_placeholder, **{
                            "_data-value": "",
                            "_data-target": "phanterpwa-widget-multselect-value-{0}".format(self.identifier),
                            "_data-text": "",
                            "_class": "phanterpwa-widget-multselect-li-title has_editable"
                    })))
        self._xml_modal = ul

    def validate(self):
        if callable(self._validator):
            self._validator(self)
        self.focus = False
        self.has_val = None

    def _add_div_animation(self, el):
        wrapper = el.find(".phanterpwa-widget-wrapper")
        if wrapper.hasClass("phanterpwa-widget-wear-material"):
            if wrapper.find(".material-widgets-animation-onfocus").length == 0:
                wrapper.find("input").after(
                    CONCATENATE(
                        HR(_class="material-widgets-animation-offfocus"),
                        DIV(_class="material-widgets-animation-onfocus")
                    ).jquery()
                )

    def _check_value(self):
        el = jQuery("#phanterpwa-widget-multselect-input-{0}".format(self.identifier))
        p = el.parent()
        if el.val() == "" or el.val() == "[]":
            p.removeClass("has_value")
        else:
            p.addClass("has_value")
        el.trigger("keyup")

    def _on_click_label(self, el):
        el = jQuery(el)
        self._switch_focus(el)

    def _after_modal_close(self, p):
        jQuery(p).removeClass("focus")
        self._check_value()

    def _switch_pre_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        p.removeClass("has_error")
        if p.hasClass("pre_focus"):
            p.removeClass("pre_focus")
        else:
            jQuery(".phanterpwa-widget-multselect-wrapper").removeClass("pre_focus")
            p.addClass("pre_focus")

    def open_modal(self, el):
        self.modal = PseudoModal(
            "#phanterpwa-widget-multselect-value-{0}".format(self.identifier),
            self._xml_modal,
            on_close=lambda: self._after_modal_close(el),
            width="100%",
            z_index=self._z_index,
            recalc_on_scroll=self._recalc_on_scroll
        )
        self.modal.start()
        self._binds_modal_content()

    def _switch_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        stat_modal = jQuery(
            "#phanterpwa-widget-multselect-value-{0}".format(self.identifier)).attr("phanterpwa-widget-pseudomodal")
        if p.hasClass("focus"):
            p.removeClass("focus")
            p.removeClass("pre_focus")
            if self.modal is not None and self.modal is not js_undefined:
                if callable(self.modal.close):
                    self.modal.close()
        else:
            if stat_modal != "enabled":
                jQuery(".phanterpwa-widget-multselect-wrapper").removeClass("focus").removeClass("pre_focus")
                p.addClass("focus")
                setTimeout(lambda: self.open_modal(p), 30)
        self._check_value()

    def _remove_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        if el.js_is(":focus"):
            p.addClass("focus")
        else:
            p.removeClass("focus")
        self._check_value()

    def reload(self):
        self.start()

    def add_new_value(self, value):
        new_value = value
        if new_value is not "":
            has_value = False
            key_find = None
            for vdata in self._data_dict.keys():
                if self._data_dict[vdata] == new_value:
                    self._alias_value[vdata] = new_value
                    key_find = vdata
                    has_value = True
                    break
            if not has_value:
                new_key = "${0}:{1}".format(__new__(Date().getTime()), new_value)
                self._order_in.append(new_key)
                self._data.append([new_key, new_value])
                self._data_dict[new_key] = new_value
                self._value.append(new_key)
                self._alias_value[new_key] = new_value
                jQuery("#phanterpwa-widget-multselect-input-{0}".format(self.identifier)).val(
                    JSON.stringify(self._value))
                target = jQuery(self.target_selector)
                # target.find("select.phanterpwa-widget-multselect-select").find("option").removeAttr("selected")
                target.find("select.phanterpwa-widget-multselect-select").append(
                    OPTION(new_value, _value=new_key, _selected="selected").jquery()
                )
                target.find("select.phanterpwa-widget-multselect-select").find(
                    "option[value='{0}']".format(new_key)).attr(
                        "selected", "selected").prop('selected', True).text(new_value)

                self._create_xml_modal()
                self._create_xml_values()
                self._xml_values.html_to("#phanterpwa-widget-multselect-value-{0}".format(self.identifier))
                self._binds_values_content()
                self._check_value()
            else:
                if key_find is not None and key_find not in self._value:
                    self._value.append(key_find)
                target = jQuery(self.target_selector)
                target.find("select.phanterpwa-widget-multselect-select").find(
                    "option[value='{0}']".format(key_find)).attr(
                        "selected", "selected").prop('selected', True).text(new_value)
                jQuery("#phanterpwa-widget-multselect-input-{0}".format(self.identifier)).val(
                    JSON.stringify(self._value))
                self._create_xml_modal()
                self._create_xml_values()
                self._xml_values.html_to("#phanterpwa-widget-multselect-value-{0}".format(self.identifier))
                self._binds_values_content()
                self._check_value()
        else:
            self._binds_values_content()

    def _add_new_option(self, el):
        inp = jQuery(el).parent().find("input")
        new_value = jQuery(inp).val()
        self.add_new_value(new_value)
        self.modal.close()

    def _on_enter_key_press_to_new_input(self, event, el):
        code = event.keyCode or event.which
        if code == 13:
            inp = jQuery(el)
            new_value = jQuery(inp).val()
            self.add_new_value(new_value)
            self.modal.close()
        elif code == 27:
            self.modal.close()

    def _switch_option(self, el):
        op = jQuery(el).find(".phanterpwa-widget-multselect-li-icon")
        t = jQuery(el).data("target")
        v = str(jQuery(el).data("value"))
        h = jQuery(el).data("text")
        target = jQuery(self.target_selector)
        stat = jQuery(el).attr("phanterpwa-widget-multiselect-status")
        if stat == "enabled":
            jQuery(el).attr("phanterpwa-widget-multiselect-status", "disabled").removeClass("selected")
            op.html(XML(self._icon_option).jquery())
            t_op = target.find("select.phanterpwa-widget-multselect-select").find(
                "option[value='{0}']".format(v))
            t_op.prop('selected', False)
            t_op.removeAttr("selected")
            if v in self._alias_value:
                del self._alias_value[v]
                self._value = [str(x) for x in self._alias_value.keys()]
        else:
            op.html(XML(self._icon_option_selected).jquery())
            jQuery(el).attr("phanterpwa-widget-multiselect-status", "enabled").addClass("selected")
            target.find("select.phanterpwa-widget-multselect-select").find(
                "option[value='{0}']".format(v)).attr("selected", "selected").prop('selected', True)
            self._alias_value[v] = h
            self._value = [str(x) for x in self._alias_value.keys()]
        jQuery("#phanterpwa-widget-multselect-input-{0}".format(self.identifier)).val(JSON.stringify(self._value))
        self._create_xml_modal()
        self._create_xml_values()
        self._xml_values.html_to("#phanterpwa-widget-multselect-value-{0}".format(self.identifier))
        self._binds_values_content()
        self._check_value()

    def _binds(self):
        target = jQuery(self.target_selector)
        self._add_div_animation(target)
        target.find(".phanterpwa-widget-multselect-touchpad").off("click.phanterpwa-event-input_materialize").on(
            "click.phanterpwa-event-input_materialize",
            lambda: self._switch_focus(this)
        )
        target.find(".phanterpwa-widget-multselect-touchpad").off("focus.phanterpwa-event-input_materialize").on(
            "focus.phanterpwa-event-input_materialize",
            lambda: self._switch_pre_focus(this)
        )
        target.find(".phanterpwa-widget-multselect-touchpad").off("focusout.phanterpwa-event-input_materialize").on(
            "focusout.phanterpwa-event-input_materialize",
            lambda: self._switch_pre_focus(this)
        )
        target.find("input").off("change.phanterpwa-event-input_materialize").on(
            "change.phanterpwa-event-input_materialize",
            lambda: self._check_value()
        )
        target.find("label").off("click.phanterpwa-event-input_materialize").on(
            "click.phanterpwa-event-input_materialize",
            lambda: target.find(".phanterpwa-widget-multselect-touchpad").trigger("click")
        )
        target.find(
            ".phanterpwa-widget-multselect-caret, .phanterpwa-widget-check"
        ).off(
            "click.phanterpwa-event-input_materialize"
        ).on(
            "click.phanterpwa-event-input_materialize",
            lambda: target.find(".phanterpwa-widget-multselect-touchpad").trigger("click")
        )
        target.find(".phanterpwa-widget-multselect-touchpad").off("keydown.open_by_key").on(
            "keydown.open_by_key",
            lambda event: self._open_by_key(event, this)
        )
        self._binds_values_content()

    def _open_by_key(self, event, el):
        code = event.keyCode or event.which
        p = jQuery(el).parent()
        stat_modal = jQuery(
            "#phanterpwa-widget-multselect-value-{0}".format(self.identifier)).attr("phanterpwa-widget-pseudomodal")
        if code == 40:
            event.preventDefault()
            #self.open_modal(p)
            if stat_modal != "enabled":
                jQuery(".phanterpwa-widget-multselect-wrapper").removeClass("focus").removeClass("pre_focus")
                p.addClass("focus")
                setTimeout(lambda: self.open_modal(p), 30)
        elif code == 27:
            p.addClass("pre_focus")
            if self.modal is not None and self.modal is not js_undefined:
                if callable(self.modal.close):
                    self.modal.close()
        elif code == 9:
            # if self.modal is not js_undefined:
            #     self.modal.close()
            p.removeClass("focus")
            p.removeClass("pre_focus")
            if self.modal is not None and self.modal is not js_undefined:
                if callable(self.modal.close):
                    self.modal.close()
        self._check_value()

    def set_on_click_new_button(self, value):
        if callable(value):
            self._on_click_new = value
        else:
            console.error("The 'on_click_new_butto' value must be callable.")

    def _switch_editable(self, el):
        if callable(self._on_click_new):
            self._on_click_new(self)
        else:
            p = jQuery(el).parent().parent()
            pp = p.parent()
            if p.hasClass("enabled"):
                p.removeClass("enabled")
                pp.removeClass("editable_enabled")
            else:
                jQuery(el).parent().find("input").focus()
                p.addClass("enabled")
                pp.addClass("editable_enabled")

    def _del_value(self, el):
        p = jQuery(el).parent()
        v = p.data("value")
        if str(v) in self._alias_value.keys():
            del self._alias_value[str(v)]
            self._value = [str(x) for x in self._alias_value.keys()]
            jQuery("#phanterpwa-widget-multselect-input-{0}".format(self.identifier)).val(JSON.stringify(self._value))
            self._create_xml_modal()
            self._create_xml_values()
            self._xml_values.html_to("#phanterpwa-widget-multselect-value-{0}".format(self.identifier))
            self._binds_values_content()
            self._check_value()

    def _binds_values_content(self):
        jQuery(self.target_selector).find(
            ".phanterpwa-widget-multselect-value-icon_close"
        ).off(
            "click.del_value_multselect"
        ).on(
            "click.del_value_multselect",
            lambda: self._del_value(this)
        )

    def _binds_modal_content(self):
        jQuery(".phanterpwa-component-pseudomodal-content").find(
            ".phanterpwa-widget-multselect-li-option"
        ).off(
            "click.option_select_modal_content"
        ).on(
            "click.option_select_modal_content",
            lambda: self._switch_option(this)
        )
        if self._editable:
            jQuery(".phanterpwa-component-pseudomodal-content").find(
                ".phanterpwa-widget-multselect-li-icon_plus"
            ).off(
                "click.option_select_modal_content"
            ).on(
                "click.option_select_modal_content",
                lambda: self._switch_editable(this)
            )
            jQuery(".phanterpwa-component-pseudomodal-content").find(
                ".phanterpwa-widget-multselect-li-icon_confirm"
            ).off(
                "click.option_select_modal_content"
            ).on(
                "click.option_select_modal_content",
                lambda: self._add_new_option(this)
            )
            jQuery(".phanterpwa-component-pseudomodal-content").find(
                ".phanterpwa-widget-multselect-li-input"
            ).off(
                "keydown.key_option_select_modal_content"
            ).on(
                "keydown.key_option_select_modal_content",
                lambda event: self._on_enter_key_press_to_new_input(event, this)
            )

    def start(self):
        self._binds()

    def value(self):
        return self._value

    def alias_value(self):
        return self._alias_value


class ListString(Widget):
    def __init__(self, identifier, **parameters):
        self._label = parameters.get("label", None)
        self._placeholder = parameters.get("placeholder", None)
        self._editable = parameters.get("editable", True)
        self._name = parameters.get("name", None)
        self._value = parameters.get("value", [])
        self._data_set(parameters.get("data_set", []))
        self._fixed = parameters.get("fixed", [])
        self._icon = parameters.get("icon", None)
        self._message_error = parameters.get("message_error", None)
        self._can_empty = parameters.get("can_empty", False)
        self._validator = parameters.get("validators", None)
        self._wear = parameters.get("wear", "material")
        self._kind = parameters.get("kind", "text")
        self._form = parameters.get("form", None)
        self._on_click_new = parameters.get("on_click_new_button", None)
        self._xml_list_string = ""
        self._input_value = []
        wrapper_attr = {
            "_class": "phanterpwa-widget-wrapper {0} phanterpwa-widget-wear-{1}".format(
                "phanterpwa-widget-list_string-wrapper",
                self._wear
            )
        }
        parameters["_id"] = identifier
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-list_string")
        else:
            parameters['_class'] = "phanterpwa-widget-list_string"

        label = ""
        if self._label is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_label")
            label = LABEL(self._label, _for="phanterpwa-widget-list_string-input-{0}".format(identifier))

        if self._message_error is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_error")
        xml_icon = ""
        if self._icon is not None:
            xml_icon = DIV(self._icon, _class="phanterpwa-widget-icon-wrapper icon_button wave_on_click")
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_icon")
        if isinstance(self._value, (list, tuple, dict)):
            if len(self._value) > 0:
                wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_value")
        else:
            console.error("The list_string value must be list, tuple or dict")
        if self._mask is not "" and self._mask is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_mask")
        self._process_list_string()
        self._process_list_predefinition_string()

        html = DIV(
            DIV(
                self._xml_list_string,
                _id="phanterpwa-widget-list_string-list_values-{0}".format(identifier),
                _class="phanterpwa-widget-list_string-list_values",
                _tabindex=0
            ),
            INPUT(**{
                "_id": "phanterpwa-widget-list_string-input-{0}".format(identifier),
                "_class": "phanterpwa-widget-list_string-input",
                "_name": self._name,
                "_value": JSON.stringify(self._input_value),
                "_placeholder": self._placeholder,
                "_type": "hidden",
                "_data-validators": JSON.stringify(self._validator),
                "_data-form": self._form,
            }),
            label,
            DIV(
                self._xml_list_predefinition_string,
                _class="phanterpwa-widget-list_string-list_predefinitions_values"
            ),
            DIV(
                I(_class="fas fa-check"),
                _class="phanterpwa-widget-check"
            ),
            xml_icon,
            DIV(
                self.get_message_error(),
                _class="phanterpwa-widget-message_error phanterpwa-widget-list_string-message_error"
            ),
            **wrapper_attr
        )
        Widget.__init__(self, identifier, html, **parameters)

    def _process_list_string(self):
        new_value = []
        self._input_value = []
        self._dict_input_value = {}
        if isinstance(self._value, (list, tuple, dict)):
            if isinstance(self._value, (list, tuple)):
                xml = CONCATENATE()
                for x in self._value:
                    if isinstance(x, (list, tuple)) and len(x) == 2:
                        self._input_value.append(str(x[0]))
                        self._dict_input_value[str(x[0])] = x[1]
                        new_value.append([str(x[0]), x[1]])
                        xml.append(
                            DIV(
                                x[1],
                                DIV(I(_class="fas fa-times"),
                                    _class="phanterpwa-widget-list_string-value-icon_close icon_button wave_on_click") if x[1] not in self._fixed else "",
                                **{
                                    "_data-value": str(x[0]),
                                    "_class": "phanterpwa-widget-list_string-value-content{0}".format(
                                        "" if x[1] not in self._fixed else " widget-liststring-fixed"),
                                    "_tabindex": "0"
                                }
                            )
                        )
                    else:
                        self._input_value.append(x)
                        self._dict_input_value[str(x)] = x
                        new_value.append([str(x), x])
                        xml.append(
                            DIV(
                                x,
                                DIV(I(_class="fas fa-times"),
                                    _class="phanterpwa-widget-list_string-value-icon_close icon_button wave_on_click") if x not in self._fixed else "",
                                **{
                                    "_data-value": x,
                                    "_class": "phanterpwa-widget-list_string-value-content{0}".format(
                                        "" if x not in self._fixed else " widget-liststring-fixed"),
                                    "_tabindex": "0"
                                }
                            )
                        )
            elif isinstance(self._value, dict):
                for x in self._value.keys():
                    self._input_value.append(str(x))
                    new_value.append([str(x), self._value[str(x)]])
                    self._dict_input_value[str(x)] = self._value[str(x)]
                    xml.append(
                        DIV(
                            self._value[str(x)],
                            DIV(I(_class="fas fa-times"),
                                _class="phanterpwa-widget-list_string-value-icon_close icon_button wave_on_click") if self._value[str(x)] not in self._fixed else "",
                            **{
                                "_data-value": x,
                                "_class": "phanterpwa-widget-list_string-value-content{0}".format(
                                    "" if self._value[str(x)] not in self._fixed else " widget-liststring-fixed"),
                                "_tabindex": "0"
                            }
                        )
                    )
            if self._editable:
                xml.append(DIV(
                    DIV(
                        I(_class="fas fa-plus"),
                        _class="icon_button wave_on_click phanterpwa-widget-list_string-value-icon_plus"
                    ),
                    _class="phanterpwa-widget-list_string-plus_icon-container",
                    _tabindex=0
                ))
            self._xml_list_string = xml
        else:
            self._input_value = []
            if self._editable:
                self._xml_list_string = DIV(
                    DIV(
                        I(_class="fas fa-plus"),
                        _class="icon_button wave_on_click phanterpwa-widget-list_string-value-icon_plus"
                    ),
                    _class="phanterpwa-widget-list_string-plus_icon-container",
                    _tabindex=0
                )
            else:
                self._xml_list_string = CONCATENATE()
        self._value = new_value

    def _data_set(self, data):
        valid_data = True
        self._data = []
        self._data_dict = {}
        if isinstance(data, list):
            new_data = []
            for vdata in data:
                if isinstance(vdata, list) and len(vdata) == 2:
                    self._data_dict[str(vdata[0])] = vdata[1]
                    new_data.append([str(vdata[0]), vdata[1]])
                else:
                    self._data_dict[str(vdata)] = vdata
                    new_data.append([str(vdata), vdata])
                self._data = new_data
        elif isinstance(data, dict):
            new_data = []
            for vdata in data.keys():
                new_data.append([str(vdata), data[str(vdata)]])
                if self._value == str(vdata):
                    self._alias_value = data[str(vdata)]
            self._data = new_data
            self._data_dict = data

    def _process_list_predefinition_string(self):
        xml = CONCATENATE()
        data_dict_keys = self._data_dict.keys()
        for x in self._input_value:
            if str(x) not in data_dict_keys:
                self._data_dict[str(x)] = self._dict_input_value[str(x)]
                self._data.append([str(x), self._dict_input_value[x]])
        data_dict_keys = self._data_dict.keys()
        for x in data_dict_keys:
            if str(x) not in self._input_value:
                xml.append(
                    DIV(
                        self._data_dict[str(x)],
                        DIV(I(_class="fas fa-plus"),
                            _class="phanterpwa-widget-list_string-value-icon_plus_predifinition icon_button wave_on_click"),
                        **{
                            "_data-value": x,
                            "_class": "phanterpwa-widget-list_string-value-predefinition-content",
                            "_tabindex": "0"
                        }
                    )
                )

        self._xml_list_predefinition_string = xml

    def _add_value_predefinition(self, el):
        p = jQuery(el).parent()
        val = p.data("value")
        alias_val = p.text()
        del self._data_dict[val]
        self.add_new_value([val, alias_val])

    def get_message_error(self):
        if self._message_error is not None:
            return self._message_error
        else:
            return ""

    def set_on_click_new_button(self, value):
        if callable(value):
            self._on_click_new = value
        else:
            console.error("The 'on_click_new_butto' value must be callable.")

    def set_message_error(self, message_error):
        jQuery("#phanterpwa-widget-{0}".format(self.identifier)).find(
            ".phanterpwa-widget-message_error").html(message_error)
        jQuery("#phanterpwa-widget-{0}".format(self.identifier)).addClass("has_error")
        self._message_error

    def del_message_error(self):
        self.set_message_error("")
        jQuery("#phanterpwa-widget-{0}".format(self.identifier)).removeClass("has_error")

    def validate(self):
        if callable(self._validator):
            self._validator(self)

    def add_new_value(self, value):
        if isinstance(value, (list, tuple)):
            if len(value) == 2:
                self._value.append(value)
            else:
                console.error("New value must be list, tuple (length == 2) or string")
        elif isinstance(value, str):
            self._value.append(["${0}:{1}".format(__new__(Date().getTime()), value), value])
        self._process_list_string()
        self._process_list_predefinition_string()
        target = jQuery(self.target_selector)
        self._xml_list_predefinition_string.html_to(
            target.find(".phanterpwa-widget-list_string-list_predefinitions_values")
        )

        target.find(".phanterpwa-widget-list_string-value-predefinition-content").find(
            ".phanterpwa-widget-list_string-value-icon_plus_predifinition"
        ).off("click.plus_predefinition_liststring").on(
            "click.plus_predefinition_liststring",
            lambda: self._add_value_predefinition(this)
        )
        jQuery("#phanterpwa-widget-list_string-input-{0}".format(
            self.identifier)).val(JSON.stringify(JSON.stringify(self._input_value)))
        jQuery("#phanterpwa-widget-list_string-list_values-{0}".format(self.identifier)).html(
            self._xml_list_string.jquery()
        ).find(".phanterpwa-widget-list_string-plus_icon-container").find(
            ".phanterpwa-widget-list_string-value-icon_plus"
        ).off(
            "click.icon_plus_lstr"
        ).on(
            "click.icon_plus_lstr",
            lambda: self._on_click_icon_plus(this)
        )
        jQuery("#phanterpwa-widget-list_string-list_values-{0}".format(self.identifier)).find(
            ".phanterpwa-widget-list_string-value-icon_close").off("click.remove_lstr_item").on(
            "click.remove_lstr_item",
            lambda: self._on_click_remove(this)
        )
        self._check_value()

    def _add_div_animation(self, el):
        wrapper = el.find(".phanterpwa-widget-wrapper")
        if wrapper.hasClass("phanterpwa-widget-wear-material"):
            if wrapper.find(".material-widgets-animation-onfocus").length == 0:
                wrapper.find("input").after(
                    CONCATENATE(
                        HR(_class="material-widgets-animation-offfocus"),
                        DIV(_class="material-widgets-animation-onfocus")
                    ).jquery()
                )

    def _check_value(self):
        target = jQuery(self.target_selector)
        if len(self._value) > 0:
            target.find(".phanterpwa-widget-list_string-wrapper").addClass("has_value")
        else:
            target.find(".phanterpwa-widget-list_string-wrapper").removeClass("has_value")

    def _save_new(self):
        jQuery("body").off("click.close_input_plus_lstr")
        target = jQuery(self.target_selector)
        val = target.find('.phanterpwa-widget-list_string-new_value-container').find("input").val()
        if val is not "":
            key_value = "${0}:{1}".format(__new__(Date().getTime()), val)
            new_value = val
            self._value.append([key_value, new_value])
        self._process_list_string()
        jQuery("#phanterpwa-widget-list_string-input-{0}".format(
            self.identifier)).val(JSON.stringify(self._input_value))
        jQuery("#phanterpwa-widget-list_string-list_values-{0}".format(self.identifier)).html(
            self._xml_list_string.jquery()
        ).find(".phanterpwa-widget-list_string-plus_icon-container").find(
            ".phanterpwa-widget-list_string-value-icon_plus"
        ).off(
            "click.icon_plus_lstr"
        ).on(
            "click.icon_plus_lstr",
            lambda: self._on_click_icon_plus(this)
        )
        jQuery("#phanterpwa-widget-list_string-list_values-{0}".format(self.identifier)).find(
            ".phanterpwa-widget-list_string-value-icon_close").off("click.remove_lstr_item").on(
            "click.remove_lstr_item",
            lambda: self._on_click_remove(this)
        )
        self._check_value()

    def _on_click_icon_save(self, el):
        self._save_new()

    def _on_enter_key_press(self, event, el):
        code = event.keyCode or event.which
        if code == 13:
            self._save_new()

    def _on_click_remove(self, el):
        p = jQuery(el).parent()
        val = str(p.data("value"))
        new_value = []
        self._dict_input_value = {}
        for x in self._value:
            if x[0] is not val:
                self._dict_input_value[str(x[0])] = x[1]
                new_value.append([str(x[0]), x[1]])
            else:
                self._data_dict[str(x[0])] = x[1]
        self._value = new_value
        self._process_list_string()
        self._process_list_predefinition_string()
        target = jQuery(self.target_selector)
        self._xml_list_predefinition_string.html_to(
            target.find(".phanterpwa-widget-list_string-list_predefinitions_values")
        )
        target.find(".phanterpwa-widget-list_string-value-predefinition-content").find(
            ".phanterpwa-widget-list_string-value-icon_plus_predifinition"
        ).off("click.plus_predefinition_liststring").on(
            "click.plus_predefinition_liststring",
            lambda: self._add_value_predefinition(this)
        )
        jQuery("#phanterpwa-widget-list_string-input-{0}".format(
            self.identifier)).val(JSON.stringify(self._input_value))
        jQuery("#phanterpwa-widget-list_string-list_values-{0}".format(self.identifier)).html(
            self._xml_list_string.jquery()
        ).find(
            ".phanterpwa-widget-list_string-plus_icon-container"
        ).find(
            ".phanterpwa-widget-list_string-value-icon_plus"
        ).off(
            "click.icon_plus_lstr"
        ).on(
            "click.icon_plus_lstr",
            lambda: self._on_click_icon_plus(this)
        )
        jQuery("#phanterpwa-widget-list_string-list_values-{0}".format(self.identifier)).find(
            ".phanterpwa-widget-list_string-value-icon_close").off("click.remove_lstr_item").on(
            "click.remove_lstr_item",
            lambda: self._on_click_remove(this)
        )
        self._check_value()

    def _on_click_icon_plus(self, el):
        if callable(self._on_click_new):
            self._on_click_new(self)
        else:
            target = jQuery(self.target_selector)
            p_cont = target.find(
                ".phanterpwa-widget-list_string-plus_icon-container"
            ).addClass(
                "has_input"
            )
            p_cont.html(CONCATENATE(
                DIV(
                    INPUT(),
                    _class="phanterpwa-widget-list_string-new_value-container"
                ),
                DIV(
                    I(_class="fas fa-check"),
                    _class="icon_button wave_on_click phanterpwa-widget-list_string-value-save"
                )
            ).jquery())
            p_cont.find(".phanterpwa-widget-list_string-value-save").off("click.on_icon_save_lstr").on(
                "click.on_icon_save_lstr",
                lambda: self._on_click_icon_save(this)
            )
            p_cont.find('input').focus().off("keypress.map_enter_lstr").on(
                "keypress.map_enter_lstr",
                lambda event: self._on_enter_key_press(event, this)
            )
            setTimeout(lambda: jQuery("body").off("click.close_input_plus_lstr").on(
                "click.close_input_plus_lstr",
                lambda ev: self._close_on_click_out(ev, this)
            ), 300)

    def _on_click_label(self, el):
        el = jQuery(el)
        p = el.parent()
        if not p.hasClass("focus"):
            p.find("input").focus().trigger("focus")

    def _switch_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        p.removeClass("has_error")
        if el.js_is(":focus"):
            jQuery(".phanterpwa-widget-wrapper").removeClass("focus").removeClass("pre_focus")
            p.addClass("focus")
        # else:
        #     if p.find(":focus").length == 0:
        #         p.removeClass("focus")
        self._check_value(el)

    def reload(self):
        self.start()

    def _close_on_click_out(self, event, el):
        target = jQuery(self.target_selector)
        if jQuery(event.target).closest(".phanterpwa-widget-list_string-plus_icon-container").length == 0:

            target.find(".phanterpwa-widget-list_string-plus_icon-container").html(
                DIV(
                    I(_class="fas fa-plus"),
                    _class="icon_button wave_on_click phanterpwa-widget-list_string-value-icon_plus"
                ).jquery()
            )
            jQuery("body").off("click.close_input_plus_lstr")
            target.find(".phanterpwa-widget-list_string-plus_icon-container").removeClass("has_input").find(
                ".phanterpwa-widget-list_string-value-icon_plus"
            ).off("click.icon_plus_lstr").on(
                "click.icon_plus_lstr",
                lambda: self._on_click_icon_plus(this)
            )

    def _binds(self):
        target = jQuery(self.target_selector)
        self._add_div_animation(target)

        target.find(".phanterpwa-widget-list_string-list_values").off("focusin.list_string_vals").on(
            "focusin.list_string_vals",
            lambda: self._switch_focus(this),
        )

        target.find(".phanterpwa-widget-list_string-list_values").off("focusout.list_string_vals").on(
            "focusout.list_string_vals",
            lambda: self._switch_focus(this),
        )

        target.find(".phanterpwa-widget-list_string-plus_icon-container").find(
            ".icon_button"
        ).off("click.icon_plus_lstr").on(
            "click.icon_plus_lstr",
            lambda: self._on_click_icon_plus(this)
        )
        target.find("label").off("click.phanterpwa-event-input_materialize").on(
            "click.phanterpwa-event-input_materialize",
            lambda: target.find(".phanterpwa-widget-list_string-list_values").focus()
        )
        jQuery("#phanterpwa-widget-list_string-list_values-{0}".format(self.identifier)).find(
            ".phanterpwa-widget-list_string-value-icon_close").off("click.remove_lstr_item").on(
            "click.remove_lstr_item",
            lambda: self._on_click_remove(this)
        )
        target.find(".phanterpwa-widget-list_string-value-predefinition-content").find(
            ".phanterpwa-widget-list_string-value-icon_plus_predifinition"
        ).off("click.plus_predefinition_liststring").on(
            "click.plus_predefinition_liststring",
            lambda: self._add_value_predefinition(this)
        )

    def start(self):
        target = jQuery(self.target_selector)
        self._add_div_animation(target)
        self._binds()

    def value(self):
        return self._value


class Textarea(Widget):
    def __init__(self, identifier, **parameters):
        self._label = parameters.get("label", None)
        self._placeholder = parameters.get("placeholder", None)
        self._name = parameters.get("name", None)
        self._value = parameters.get("value", "")
        self._icon = parameters.get("icon", None)
        self._message_error = parameters.get("message_error", None)
        self._can_empty = parameters.get("can_empty", False)
        self._validator = parameters.get("validators", None)
        self._wear = parameters.get("wear", "material")
        self._form = parameters.get("form", None)
        wrapper_attr = {
            "_class": "phanterpwa-widget-wrapper phanterpwa-widget-textarea-wrapper phanterpwa-widget-wear-{0}".format(
                self._wear)
        }
        parameters["_id"] = identifier
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-textarea")
        else:
            parameters['_class'] = "phanterpwa-widget-textarea"
        label = ""
        if self._label is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_label")
            label = LABEL(self._label, _for="phanterpwa-widget-textarea-textarea-{0}".format(identifier))

        if self._message_error is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_error")

        if self._icon is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_icon")

        if self._value is not "":
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_value")

        html = DIV(
            TEXTAREA(
                self._value,
                **{
                    "_id": "phanterpwa-widget-textarea-textarea-{0}".format(identifier),
                    "_class": "phanterpwa-widget-textarea-textarea",
                    "_name": self._name,
                    "_placeholder": self._placeholder,
                    "_data-validators": JSON.stringify(self._validator),
                    "_data-form": self._form
            }),
            label,
            DIV(
                I(_class="fas fa-check"),
                _class="phanterpwa-widget-check"
            ),
            DIV(
                self.get_message_error(),
                _class="phanterpwa-widget-message_error phanterpwa-widget-textarea-message_error"
            ),
            **wrapper_attr
        )
        Widget.__init__(self, identifier, html, **parameters)

    def get_message_error(self):
        if self._message_error is not None:
            return self._message_error
        else:
            return ""

    def set_message_error(self, message_error):
        jQuery("#phanterpwa-widget-{0}".format(self.identifier)).find(
            ".phanterpwa-widget-message_error").html(message_error)
        jQuery("#phanterpwa-widget-{0}".format(self.identifier)).addClass("has_error")
        self._message_error

    def del_message_error(self):
        self.set_message_error("")
        jQuery("#phanterpwa-widget-{0}".format(self.identifier)).removeClass("has_error")

    def validate(self):
        if callable(self._validator):
            self._validator(self)

    def _add_div_animation(self, el):
        wrapper = el.find(".phanterpwa-widget-wrapper")
        if wrapper.hasClass("phanterpwa-widget-wear-material"):
            if wrapper.find(".material-widgets-animation-onfocus").length == 0:
                wrapper.find("textarea").after(
                    CONCATENATE(
                        HR(_class="material-widgets-animation-offfocus"),
                        DIV(_class="material-widgets-animation-onfocus")
                    ).jquery()
                )

    def _check_value(self, el):
        el = jQuery(el)
        p = el.parent()
        if el.val() is not "":
            p.addClass("has_value")
        else:
            p.removeClass("has_value")

    def _on_click_label(self, el):
        el = jQuery(el)
        p = el.parent()
        if not p.hasClass("focus"):
            p.find("textarea").focus().trigger("focus")

    def _switch_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        p.removeClass("has_error")
        if el.js_is(":focus"):
            jQuery(".phanterpwa-widget-wrapper").removeClass("focus").removeClass("pre_focus")
            p.addClass("focus")
        else:
            p.removeClass("focus")
        self._check_value(el)

    def _remove_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        if el.js_is(":focus"):
            p.addClass("focus")
        else:
            p.removeClass("focus")
        self._check_value(el)

    def reload(self):
        self.start()

    def _autoresize(self, el):
        h = jQuery(el).prop("scrollHeight")
        text = jQuery(el).val()
        split_ = text.split("\n")
        if text == "":
            jQuery(el).css("height", 34)
        elif len(split_) == 2:
            s = 50
            if jQuery(el).prop("scrollHeight") > s:
                jQuery(el).css("height", jQuery(el).prop("scrollHeight"))
            else:
                jQuery(el).css("height", 50)
        elif len(split_) > 2:
            jQuery(el).css("height", "auto").css("height", jQuery(el).prop("scrollHeight"))
        else:
            jQuery(el).css("height", jQuery(el).prop("scrollHeight"))
        # this.style.height = (this.scrollHeight) + 'px';

    def _binds(self):
        target = jQuery(self.target_selector)
        self._add_div_animation(target)

        target.find("textarea").off("focus.phanterpwa-event-textarea_materialize").on(
            "focus.phanterpwa-event-textarea_materialize",
            lambda: self._switch_focus(this)
        )
        target.find("textarea").off("focusout.phanterpwa-event-textarea_materialize").on(
            "focusout.phanterpwa-event-textarea_materialize",
            lambda: self._switch_focus(this)
        )
        target.find("textarea").off("change.phanterpwa-event-textarea_materialize").on(
            "change.phanterpwa-event-textarea_materialize",
            lambda: self._check_value(this)
        )
        target.off("click.phanterpwa-event-textarea_materialize").on(
            "click.phanterpwa-event-textarea_materialize",
            lambda: self._on_click_label(this)
        )

        target.find("textarea").attr("style", "height: auto; overflow-y:hidden").off("input.textarea_autoresize").on(
            "input.textarea_autoresize",
            lambda: self._autoresize(this)
        )
        size = target.find("textarea").css("height", 31).prop('scrollHeight')
        target.find("textarea").css("height", size)
        #   this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
        # }).on('input', function () {
        #   this.style.height = 'auto';
        #   this.style.height = (this.scrollHeight) + 'px';
        # });

    def start(self):
        self._binds()


class Inert(Widget):
    def __init__(self, identifier, **parameters):
        self._label = parameters.get("label", None)
        self._name = parameters.get("name", None)
        self._value = parameters.get("value", "")
        self._wear = parameters.get("wear", "material")
        self._form = parameters.get("form", None)
        wrapper_attr = {
            "_class": "phanterpwa-widget-wrapper its_disabled phanterpwa-widget-wear-{0} {1}".format(
                self._wear,
                "phanterpwa-widget-inert-wrapper"
            )
        }
        parameters["_id"] = identifier
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-inert")
        else:
            parameters['_class'] = "phanterpwa-widget-inert"
        label = ""
        if self._label is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_label")
            label = LABEL(self._label, _for="phanterpwa-widget-inert-inert-{0}".format(identifier))
        if self._value is not "":
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_value")

        html = DIV(
            INPUT(**{
                "_id": "phanterpwa-widget-inert-input-{0}".format(identifier),
                "_class": "phanterpwa-widget-inert-input",
                "_name": self._name,
                "_value": self._value,
                "_data-form": self._form,
                "_disabled": "disabled"
            }),
            HR(_class="material-widgets-animation-offfocus"),
            label,
            **wrapper_attr
        )
        Widget.__init__(self, identifier, html, **parameters)


class CheckBox(Widget):
    def __init__(self, identifier, **parameters):
        self._label = parameters.get("label", None)
        self._name = parameters.get("name", None)
        self._value = parameters.get("value", False)
        self._can_empty = parameters.get("can_empty", False)
        self._wear = parameters.get("wear", "material")
        self._form = parameters.get("form", None)
        self._disabled = parameters.get("disabled", False)

        wrapper_attr = {
            "_class": "phanterpwa-widget-wrapper phanterpwa-widget-checkbox-wrapper phanterpwa-widget-wear-{0}".format(
                self._wear)
        }
        parameters["_id"] = identifier
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-checkbox")
        else:
            parameters['_class'] = "phanterpwa-widget-checkbox"
        label = ""
        if self._label is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_label")
            label = LABEL(self._label, _for="phanterpwa-widget-checkbox-input-{0}".format(identifier))
        if self._disabled is True:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " disabled")
        _checked = None
        if self._value is True or self._Value is "true":
            _checked = "checked"
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_true")

        html = DIV(
            INPUT(**{
                "_id": "phanterpwa-widget-checkbox-input-{0}".format(identifier),
                "_class": "phanterpwa-widget-checkbox-input",
                "_name": self._name,
                "_value": self._value,
                "_placeholder": self._placeholder,
                "_type": "checkbox",
                "_checked": _checked,
                "_data-form": self._form
            }),
            DIV(
                DIV(
                    I(_class="fas fa-check"),
                    _class="phanterpwa-widget-checkbox-true"),
                DIV(_class="phanterpwa-widget-checkbox-option-container"),
                _class="phanterpwa-widget-checkbox-checkbox",
                _tabindex=0
            ),
            label,
            **wrapper_attr
        )
        Widget.__init__(self, identifier, html, **parameters)

    def set_value(self, value):
        if not self._disabled:
            if value:
                self._value = True
                jQuery(self.target_selector).find(".phanterpwa-widget-checkbox-wrapper").addClass("has_true")
            else:
                self._value = True
                jQuery(self.target_selector).find(".phanterpwa-widget-checkbox-wrapper").removeClass("has_true")
            jQuery(self.target_selector).find("input").prop("checked", self._value).val(self._value)

    def set_disabled(self):
        self._disabled = True
        jQuery(self.target_selector).find(".phanterpwa-widget-wrapper").addClass("disabled")

    def set_enabled(self):
        self._disabled = False
        jQuery(self.target_selector).find(".phanterpwa-widget-wrapper").removeClass("disabled")

    def _switch_value(self, el):
        if not self._disabled:
            el = jQuery(el)
            p = el.parent()
            if p.hasClass("has_true"):
                p.removeClass("has_true")
                self._value = False
            else:
                p.addClass("has_true")
                self._value = True
            p.find("input").prop("checked", self._value).val(self._value)

    def _switch_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        if el.js_is(":focus"):
            jQuery(".phanterpwa-widget-wrapper").removeClass("focus").removeClass("pre_focus")
            p.addClass("focus")
        else:
            p.removeClass("focus")
        #self._check_value(el)

    def reload(self):
        self.start()

    def _binds(self):
        target = jQuery(self.target_selector)
        target.find(".phanterpwa-widget-checkbox-checkbox").off("click.phanterpwa-event-checkbox-switch").on(
            "click.phanterpwa-event-checkbox-switch",
            lambda: self._switch_value(this)
        )
        target.find(".phanterpwa-widget-checkbox-checkbox").off("focusin.phanterpwa-event-checkbox-focus").on(
            "focusin.phanterpwa-event-checkbox-focus",
            lambda: self._switch_focus(this)
        )
        target.find(".phanterpwa-widget-checkbox-checkbox").off("focusout.phanterpwa-event-checkbox-focus").on(
            "focusout.phanterpwa-event-checkbox-focus",
            lambda: self._switch_focus(this)
        )


    def start(self):
        self._binds()
        if jQuery("#phanterpwa-widget-checkbox-input-{0}".format(self.identifier)).prop("checked"):
            jQuery(self.target_selector).find(".phanterpwa-widget-checkbox-wrapper").addClass("has_true")


class RadioBox(Widget):
    def __init__(self, identifier, **parameters):
        self._label = parameters.get("label", None)
        self._name = parameters.get("name", None)
        self._value = parameters.get("value", False)
        self._can_empty = parameters.get("can_empty", False)
        self._wear = parameters.get("wear", "material")
        self._form = parameters.get("form", None)
        self._group = parameters.get("group", None)

        wrapper_attr = {
            "_class": "phanterpwa-widget-wrapper phanterpwa-widget-radio-wrapper phanterpwa-widget-wear-{0}".format(
                self._wear)
        }
        parameters["_id"] = identifier
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-radio")
        else:
            parameters['_class'] = "phanterpwa-widget-radio"
        label = ""
        if self._label is not None:
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_label")
            label = LABEL(self._label, _for="phanterpwa-widget-radio-input-{0}".format(identifier))
        _checked = None
        if self._value is True or self._Value is "true":
            _checked = "checked"
            wrapper_attr["_class"] = "{0}{1}".format(wrapper_attr["_class"], " has_true")

        html = DIV(
            INPUT(**{
                "_id": "phanterpwa-widget-radio-input-{0}".format(identifier),
                "_class": "phanterpwa-widget-radio-input",
                "_name": self._name,
                "_value": self._value,
                "_placeholder": self._placeholder,
                "_type": "radio",
                "_checked": _checked,
                "_data-instance": self.identifier,
                "_data-form": self._form
            }),
            DIV(
                DIV(
                    self._xml_radio(),
                    _class="phanterpwa-widget-radio-option-container"
                ),
                _class="phanterpwa-widget-radio-radio",
                _tabindex=0
            ),
            label,
            **wrapper_attr
        )
        Widget.__init__(self, identifier, html, **parameters)

    def _change_xml_radio(self):
        el = jQuery("#phanterpwa-widget-radio-input-{0}".format(self.identifier))
        value = el.prop("checked")
        p = el.parent()
        
        if value is True:
            p.addClass("has_true")
            jQuery("#phanterpwa-widget-radio-input-{0}".format(self.identifier)).val(value)
            self._value = True

        else:
            p.removeClass("has_true")
            jQuery("#phanterpwa-widget-radio-input-{0}".format(self.identifier)).val(value)
            self._value = False

        self._xml_radio().html_to(jQuery(self.target_selector).find(".phanterpwa-widget-radio-option-container"))

    def _xml_radio(self):
        if self._value is True:
            return DIV(
                I(_class="far fa-dot-circle"),
                _class="phanterpwa-widget-radio-true"
            )
        return DIV(
            I(_class="far fa-circle"),
            _class="phanterpwa-widget-radio-false"
        )

    def _set_radio_value(self, el):
        el = jQuery(el)
        p = el.parent()
        p.addClass("has_true")
        jQuery(".phanterpwa-widget-wrapper").removeClass("focus").removeClass("pre_focus")
        p.addClass("focus")
        self._value = True
        p.find("input").prop("checked", self._value).val(self._value)
        jQuery(".phanterpwa-widget-radio-input").trigger("change")

    def _switch_focus(self, el):
        el = jQuery(el)
        p = el.parent()
        if el.js_is(":focus"):
            jQuery(".phanterpwa-widget-wrapper").removeClass("focus").removeClass("pre_focus")
            p.addClass("focus")
        else:
            p.removeClass("focus")

    def reload(self):
        self.start()

    def _binds(self):
        target = jQuery(self.target_selector)
        target.find(".phanterpwa-widget-radio-radio").off("click.phanterpwa-event-radio-switch").on(
            "click.phanterpwa-event-radio-switch",
            lambda: self._set_radio_value(this)
        )
        target.find("label").off("click.phanterpwa-event-radio-switch").on(
            "click.phanterpwa-event-radio-switch",
            lambda: self._set_radio_value(this)
        )
        target.find("input").off("change.phanterpwa-event-radio-switch").on(
            "change.phanterpwa-event-radio-switch",
            lambda: self._change_xml_radio()
        )


    def start(self):
        self._binds()


class MenuBox(Widget):
    def __init__(self, identifier, button, *options, **parameters):
        class_button = ""
        if button is js_undefined or button is None:
            self._button = I(_class="fas fa-ellipsis-v")
            class_button = " icon_button"
        else:
            if isinstance(button, helpers.XmlConstructor) and button.tag.upper() == "I":
                class_button = " icon_button"
            self._button = button
        self._custom_menu = parameters.get("custom_menu", None)
        self._xml_menu = []
        self._onreload = parameters.get('onReload', None)
        self._onopen = parameters.get('onOpen', None)
        self._options = options
        for x in self._options:
            self.add_option(x)

        self.set_z_index(parameters.get("z_index", None))
        self._close_after_click_in = parameters.get("close_after_click_in", True)
        self.set_recalc_on_scroll(parameters.get("recalc_on_scroll", True))
        self._width = parameters.get('width', None)

        html = DIV(
            self._button,
            _class="phanterpwa-widget-menubox-button{0}".format(class_button),
            _phanterpwa_dowpdown_target="drop_{0}".format(identifier)
        )
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-menubox")
        else:
            parameters['_class'] = "phanterpwa-widget-menubox"
        Widget.__init__(self, identifier, html, **parameters)

    def add_option(self, option):
        if isinstance(option, MenuOption):
            self._xml_menu.append(option)
        elif isinstance(option, helpers.XmlConstructor) and option.tag.upper() == "HR":
            self._xml_menu.append(option)
        else:
            self._xml_menu.append(DIV(option, _class="phanterpwa-widget-menubox-option wave_on_click"))

    def _on_click(self, el):
        if self._custom_menu is None:
            content = self._xml_menu
        else:
            content = [self._custom_menu]
        self.modal = PseudoModal(
            self.target_selector,
            DIV(
                *content,
                _id="phanterpwa-widget-menubox-options-content-{0}".format(self.identifier),
                _class="phanterpwa-widget-menubox-options-content",
                _style=None if self._width is None else "width: {0}px".format(self._width)
            ),
            vertical=True,
            width=self._width,
            z_index=self._z_index,
            recalc_on_scroll=self._recalc_on_scroll,
            on_open=self._onopen
        )
        self.modal.start()
        if self._close_after_click_in is True:
            jQuery("#phanterpwa-widget-menubox-options-content-{0}".format(
                self.identifier)).find(".phanterpwa-widget-menubox-option").off(
                "click.close_pseudo_modal"
            ).on(
                "click.close_pseudo_modal",
                lambda: self.modal.close()
            )
            jQuery("#phanterpwa-widget-menubox-options-content-{0}".format(
                self.identifier)).find("ul>li").off(
                "click.close_pseudo_modal"
            ).on(
                "click.close_pseudo_modal",
                lambda: self.modal.close()
            )
            jQuery("#phanterpwa-widget-menubox-options-content-{0}".format(
                self.identifier)).find("ul>span").off(
                "click.close_pseudo_modal"
            ).on(
                "click.close_pseudo_modal",
                lambda: self.modal.close()
            )

    def set_recalc_on_scroll(self, value):
        if isinstance(value, bool):
            self._recalc_on_scroll = value
        else:
            console.error("The recalc_on_scroll must be boolean!")

    def set_z_index(self, value):
        if str(value).isdigit():
            self._z_index = value
        elif value is None:
            self._z_index = None
        else:
            self._z_index = None
            console.error("The z_index must be integer or None!")

    def reload(self):
        self.start()

    def start(self):
        target = jQuery(self.target_selector)
        target.off("click.open_menu_phanterpwa").on(
            "click.open_menu_phanterpwa",
            lambda: self._on_click(this)
        )
        if callable(self._onreload):
            self._onreload(target)


class MenuOption(helpers.XmlConstructor):
    def __init__(self, *content, **attributes):
        if "_class" in attributes:
            attributes['_class'] = "phanterpwa-widget-menubox-option {0}".format(attributes['_class'])
        else:
            attributes['_class'] = "phanterpwa-widget-menubox-option"
        tag = "div"
        if "_href" in attributes:
            tag = "a"
        helpers.XmlConstructor.__init__(self, tag, False, *content, **attributes)


class PseudoModal():
    def __init__(self, source_selector, xml, **parameters):
        self.source_selector = source_selector
        self._xml = xml
        self._identifier = window.PhanterPWA.get_id("pseudomodal")
        self.pX = parameters.get("pX", 0)
        self.pY = parameters.get("pY", 0)
        self.data = parameters.get("data", None)
        self.value = parameters.get("value", None)
        self.on_close = parameters.get("on_close", None)
        self._width = parameters.get("width", "auto")
        self.placeholder = parameters.get("placeholder", None)
        self._is_select = parameters.get("is_select", False)
        self._to_top = False
        self._to_left = False
        self._vertical_position = parameters.get("vertical", False)
        self._z_index = parameters.get("z_index", None)
        self._recalc_on_scroll = parameters.get("recalc_on_scroll", False)
        self.on_open = parameters.get("on_open", None)

    def close(self):
        jQuery("#{0}".format(self._identifier)).fadeOut()
        target = jQuery(self.source_selector)
        target.attr("phanterpwa-widget-pseudomodal", "disabled")
        if not window.PhanterPWA.DEBUG:
            setTimeout(lambda: jQuery("#{0}".format(self._identifier)).remove(), 3000)
        if self.on_close is not None and callable(self.on_close):
            self.on_close()

    def _close_on_click_out(self, event):
        if jQuery(event.target).closest(".phanterpwa-component-pseudomodal-content").length == 0:
            if jQuery(event.target).closest(self.source_selector).length == 0:
                if jQuery(event.target).parent().length > 0:
                    self.close()

    def _get_source_dimentions(self):
        self.viewport = [jQuery(window).width(), jQuery(window).height()]
        self.document_size = [jQuery(document).width(), jQuery(document).height()]
        self.scroll_top = jQuery(document).scrollTop()
        self.scroll_left = jQuery(document).scrollLeft()
        self.theight = jQuery(self.source_selector).height()
        self.twidth = jQuery(self.source_selector).width()
        self.toffset = jQuery(self.source_selector).offset()
        self.space_bottom = self.viewport[1] - self.toffset['top'] - self.theight + self.scroll_top
        self.space_top = self.toffset['top'] - self.scroll_top
        if self._vertical_position:
            self.space_right = self.viewport[0] - self.toffset['left'] - self.twidth + self.scroll_left
            self.space_left = self.toffset['left'] - self.scroll_left

    def _get_wside_show(self):
        if self.space_left > self.space_right:
            self._to_left = True
        else:
            self._to_left = False

    def _get_side_show(self):
        if self.space_top > self.space_bottom:
            self._to_top = True
        else:
            self._to_top = False

    def _calc_position(self):
        if jQuery(self.source_selector).length == 0:
            jQuery(document).off(
                "scroll.recalc_on_scroll{0}".format(self._identifier)
            )
            jQuery(window).off(
                "resize.recalc_on_resize{0}".format(self._identifier)
            )
        else:
            self._get_source_dimentions()
            self._get_side_show()
            self._get_wside_show()
            if self._vertical_position:
                jQuery(
                    "#{0}-wrapper".format(self._identifier)
                ).css(
                    "left", self.toffset["left"]
                ).css(
                    "top", self.toffset["top"]
                ).css(
                    "width", self.twidth
                )
                if self._to_top and self._to_left:  # to_top to_left
                    jQuery(
                        "#{0}-wrapper".format(self._identifier)
                    ).find(
                        ".phanterpwa-component-pseudomodal-content-wrapper"
                    ).css(
                        "bottom", 0
                    ).css(
                        "top", "auto"
                    ).css(
                        "margin-top", "auto"
                    ).css(
                        "margin-bottom", self.theight / -2
                    ).css(
                        "right", 0
                    ).css(
                        "left", "auto"
                    ).css(
                        "margin-left", "auto"
                    ).css(
                        "margin-right", self.twidth / 2
                    ).css(
                        "width", self._width
                    ).parent().addClass("to_top").removeClass("to_bottom").addClass("to_left").removeClass("to_right")
                elif self._to_top:  # to_top to_right
                    jQuery(
                        "#{0}-wrapper".format(self._identifier)
                    ).find(
                        ".phanterpwa-component-pseudomodal-content-wrapper"
                    ).css(
                        "bottom", 0
                    ).css(
                        "top", "auto"
                    ).css(
                        "margin-top", "auto"
                    ).css(
                        "margin-bottom", self.theight / -2
                    ).css(
                        "right", "auto"
                    ).css(
                        "left", 0
                    ).css(
                        "margin-left", self.twidth / 2
                    ).css(
                        "width", self._width
                    ).parent().addClass("to_top").removeClass("to_bottom").addClass("to_right").removeClass("to_left")
                elif self._to_left:  # to_bottom to_left
                    jQuery(
                        "#{0}-wrapper".format(self._identifier)
                    ).find(
                        ".phanterpwa-component-pseudomodal-content-wrapper"
                    ).css(
                        "bottom", "auto"
                    ).css(
                        "top", 0
                    ).css(
                        "margin-top", self.theight / 2
                    ).css(
                        "right", 0
                    ).css(
                        "left", "auto"
                    ).css(
                        "margin-left", "auto"
                    ).css(
                        "margin-right", self.twidth / 2
                    ).css(
                        "width", self._width
                    ).parent().addClass("to_bottom").removeClass("to_top").addClass("to_left").removeClass("to_right")
                else:  # to_bottom to_right
                    jQuery(
                        "#{0}-wrapper".format(self._identifier)
                    ).find(
                        ".phanterpwa-component-pseudomodal-content-wrapper"
                    ).css(
                        "bottom", "auto"
                    ).css(
                        "top", 0
                    ).css(
                        "margin-top", self.theight / 2
                    ).css(
                        "right", "auto"
                    ).css(
                        "left", 0
                    ).css(
                        "margin-left", self.twidth / 2
                    ).css(
                        "width", self._width
                    ).parent().addClass("to_bottom").removeClass("to_top").addClass("to_right").removeClass("to_left")
            else:
                jQuery(
                    "#{0}-wrapper".format(self._identifier)
                ).css(
                    "left", self.toffset["left"]
                ).css(
                    "top", self.toffset["top"]
                ).css(
                    "width", self.twidth
                )
                if self._to_top:
                    jQuery(
                        "#{0}-wrapper".format(self._identifier)
                    ).find(
                        ".phanterpwa-component-pseudomodal-content-wrapper"
                    ).css(
                        "bottom", 0
                    ).css(
                        "top", "auto"
                    ).css(
                        "margin-top", "auto"
                    ).css(
                        "width", self._width
                    ).parent().addClass("to_top").removeClass("to_bottom")
                else:
                    jQuery(
                        "#{0}-wrapper".format(self._identifier)
                    ).find(
                        ".phanterpwa-component-pseudomodal-content-wrapper"
                    ).css(
                        "bottom", "auto"
                    ).css(
                        "top", 0
                    ).css(
                        "margin-top", self.theight
                    ).css(
                        "width", self._width
                    ).parent().addClass("to_bottom").removeClass("to_top")

    def start(self):
        style = "display: none;"
        if self._z_index is not None:
            style = "display: none; z-index: {0} !important;".format(self._z_index)
        html = DIV(
            DIV(
                DIV(
                    DIV(
                        self._xml,
                        _class="phanterpwa-component-pseudomodal-content"
                    ),
                    _class="phanterpwa-component-pseudomodal-content-wrapper"
                ),
                _id="{0}-wrapper".format(self._identifier),
                _class="phanterpwa-component-pseudomodal-wrapper"
            ),
            _id=self._identifier,
            _class="phanterpwa-component-pseudomodal-container",
            _style=style
        )
        jQuery(".phanterpwa-component-pseudomodal-container").remove()

        html.append_to("body")
        jQuery("#{0}".format(self._identifier)).fadeIn()
        self._calc_position()
        if self._recalc_on_scroll is not False:
            jQuery(document).off(
                "scroll.recalc_on_scroll{0}".format(self._identifier)
            ).on(
                "scroll.recalc_on_scroll{0}".format(self._identifier),
                self._calc_position
            )
        # jQuery(window).resize(lambda: self._calc_position())
        jQuery(window).off(
            "resize.recalc_on_resize{0}".format(self._identifier)
        ).on(
            "resize.recalc_on_resize{0}".format(self._identifier)
        )
        jQuery(
            document
        ).off(
            "click.close_pseudomodal"
        ).on(
            "click.close_pseudomodal",
            lambda event: self._close_on_click_out(event)
        )
        target = jQuery(self.source_selector)
        target.attr("phanterpwa-widget-pseudomodal", "enabled")
        if callable(self.on_open):
            self.on_open(jQuery("#{0}".format(self._identifier)))


class FloatButton(helpers.XmlConstructor):
    def __init__(self, *content, **attributes):
        if "_class" in attributes:
            attributes['_class'] = "wave_on_click phanterpwa-widget-floatbutton {0}".format(attributes['_class'])
        else:
            attributes['_class'] = "wave_on_click phanterpwa-widget-floatbutton"
        if len(content) == 1 and isinstance(content[0], helpers.XmlConstructor) and content[0].tag.upper() == "I":
            attributes['_class'] = "icon_button {0}".format(attributes['_class'])
        tag = "div"
        if "_href" in attributes:
            tag = "a"
        helpers.XmlConstructor.__init__(self, tag, False, *content, **attributes)


class FloatMenu(Widget):
    def __init__(self, identifier, button, *options, **parameters):
        class_button = ""
        if button is js_undefined or button is None:
            self._button = I(_class="fas fa-ellipsis-v")
            class_button = " icon_button"
        else:
            if isinstance(button, helpers.XmlConstructor) and button.tag.upper() == "I":
                class_button = " icon_button"
            self._button = button
        self._xml_menu = []
        self._onopen = parameters.get('onOpen', None)
        self._options = options
        for x in self._options:
            self.add_option(x)

        html = DIV(
            self._button,
            DIV(_class="phanterpwa-widget-floatmenu-options-content"),
            _class="phanterpwa-widget-floatmenu-button{0}".format(class_button),
            _phanterpwa_dowpdown_target="drop_{0}".format(identifier)
        )
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-floatmenu")
        else:
            parameters['_class'] = "phanterpwa-widget-floatmenu"
        Widget.__init__(self, identifier, html, **parameters)

    def add_option(self, option):
        if isinstance(option, FloatButton):
            self._xml_menu.append(option)
        elif isinstance(option, helpers.XmlConstructor) and option.tag.upper() == "I":
            self._xml_menu.append(DIV(option, _class="phanterpwa-widget-floatbutton icon_button wave_on_click"))
        else:
            self._xml_menu.append(DIV(option, _class="phanterpwa-widget-floatbutton wave_on_click"))

    def _on_click(self, el):
        element = jQuery(el).find(".phanterpwa-widget-floatmenu-options-content")
        if element.hasClass("enabled"):
            element.removeClass("enabled")
        else:
            element.addClass("enabled")

    def reload(self):
        self.start()

    def start(self):
        target = jQuery(self.target_selector)
        target.find(".phanterpwa-widget-floatmenu-options-content").html(
            self._xml_menu.jquery()
        )
        target.off("click.open_floatmenu_phanterpwa").on(
            "click.open_floatmenu_phanterpwa",
            lambda: self._on_click(this)
        )
        if callable(self._onreload):
            self._onreload(target)


class Preloaders(Widget):
    def __init__(self, identifier, **parameters):
        plist = [
            "android"
        ]
        preloader = parameters.get("preloader", "android")
        if preloader not in plist:
            self._preloader = "android"
            if window.PhanterPWA.DEBUG:
                console.error("The preload '{0}' not exist! 'Android used'".format(preloader))
        else:
            self._preloader = preloader

        Widget.__init__(self, identifier, self["_{0}".format(self._preloader)](), **parameters)

    def _android(self):
        android = DIV(
            DIV(
                DIV(
                    DIV(
                        DIV(
                            DIV(
                                DIV(
                                    _class='phanterpwa_circle'
                                ),
                                _class='phanterpwa_circle_clipper left'
                            ),
                            DIV(
                                DIV(
                                    _class='phanterpwa_circle'
                                ),
                                _class='phanterpwa_gap-patch'
                            ),
                            DIV(
                                DIV(
                                    _class='phanterpwa_circle'
                                ),
                                _class='phanterpwa_circle_clipper right'
                            ),
                            _class='spinner-layer spinner-one'
                        ),
                        DIV(
                            DIV(
                                DIV(
                                    _class='phanterpwa_circle'
                                ),
                                _class='phanterpwa_circle_clipper left'
                            ),
                            DIV(
                                DIV(
                                    _class='phanterpwa_circle'
                                ),
                                _class='phanterpwa_gap-patch'
                            ),
                            DIV(
                                DIV(
                                    _class='phanterpwa_circle'
                                ),
                                _class='phanterpwa_circle_clipper right'
                            ),
                            _class='spinner-layer spinner-two'
                        ),
                        DIV(
                            DIV(
                                DIV(
                                    _class='phanterpwa_circle'
                                ),
                                _class='phanterpwa_circle_clipper left'
                            ),
                            DIV(
                                DIV(
                                    _class='phanterpwa_circle'
                                ),
                                _class='phanterpwa_gap-patch'
                            ),
                            DIV(
                                DIV(
                                    _class='phanterpwa_circle'
                                ),
                                _class='phanterpwa_circle_clipper right'
                            ),
                            _class='spinner-layer spinner-three'
                        ),
                        DIV(
                            DIV(
                                DIV(
                                    _class='phanterpwa_circle'
                                ),
                                _class='phanterpwa_circle_clipper left'
                            ),
                            DIV(
                                DIV(
                                    _class='phanterpwa_circle'
                                ),
                                _class='phanterpwa_gap-patch'
                            ),
                            DIV(
                                DIV(
                                    _class='phanterpwa_circle'
                                ),
                                _class='phanterpwa_circle_clipper right'
                            ),
                            _class='spinner-layer spinner-four'
                        ),
                        _class='phanterpwa_android'
                    ),
                    _class='preloader-wrapper enabled'
                ),
                _class="preload-wrapper"),
            _class="phanterpwa-components-preloaders-android"
        ).jquery()
        return android


class Table(Widget):
    def __init__(self, identifier, *content, **parameters):
        self._head = None
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-table-container")
        else:
            parameters["_class"] = "phanterpwa-widget-table-container"
        for c in content:
            if isinstance(c, TableHead):
                self._head = c
                c._table = self
            elif isinstance(c, TableData):
                c._table = self
            elif isinstance(c, TableFooterPagination):
                c._table = self
                if self._head is not None:
                    colspan = self._head.len_head()
                    c._colspan = colspan
                    c._create_footer()
                self._footer = c

        self.__child_html = TABLE(
            *content,
            _class="phanterpwa-widget-table p-row"
        )
        Widget.__init__(self, identifier, self.__child_html, **parameters)

    def append(self, value):
        if isinstance(value, (TableHead, TableData, TableFooterPagination)):
            value._table = self
            if isinstance(value, TableHead):
                self._head = value
            elif isinstance(value, TableFooterPagination):
                if self._head is not None:
                    colspan = self._head.len_head()
                    value._colspan = colspan
                    value._create_footer()
                self._footer = value
        self.__child_html.content.append(value)

    def insert(self, pos, value):
        if isinstance(value, (TableHead, TableData, TableFooterPagination)):
            value._table = self
            if isinstance(value, TableHead):
                self._head = value
            elif isinstance(value, TableFooterPagination):
                if self._head is not None:
                    colspan = self._head.len_head()
                    value._colspan = colspan
                    value._create_footer()
                self._footer = value
        self.__child_html.content.insert(pos, value)

    def sorted_field(self):
        if self._head is not None:
            return self._head.sorted_field()
        else:
            console.error("The table not have TableHead instance!")


class TableHead(Widget):
    def __init__(self, identifier, *content, **parameters):
        self._table = None
        self._count_th = 0
        self._sortable = parameters.get("sortable", [])
        self._sort_by = parameters.get("sort_by", None)
        self._sort_order = parameters.get("sort_order", "asc")
        self._on_click_sortable = parameters.get("on_click_sortable", None)
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-table-head")
        else:
            parameters["_class"] = "phanterpwa-widget-table-head"
        self._create_head(content)
        Widget.__init__(self, identifier, self.__child_html, **parameters)
        self.tag = "tr"

    def _create_head(self, content):
        self.__child_html = CONCATENATE()
        self._count_th = len(content)
        if isinstance(self._sortable, list) and len(self._sortable) > 0:
            if self._sort_order == "desc":
                sort_order = "desc"
            else:
                sort_order = "asc"
            for x in content:

                if isinstance(x, str):
                    if x in self._sortable:
                        if self._sort_by == x:
                            self.__child_html.append(TH(DIV(
                                    x,
                                    **{"_class": "phanterpwa-widget-table-head-th-sortable",
                                    "_data-value": x}
                                ),
                                _class="phanterpwa-widget-table-head-th enabled {0}".format(sort_order)))
                        else:
                            self.__child_html.append(TH(DIV(
                                    x,
                                    **{"_class": "phanterpwa-widget-table-head-th-sortable",
                                    "_data-value": x}
                                ),
                                _class="phanterpwa-widget-table-head-th"))

                    else:
                        self.__child_html.append(TH(x,
                            _class="phanterpwa-widget-table-head-th"))

                elif isinstance(x, helpers.XmlConstructor) and (str(x._tag).upper() == "TD" or str(x._tag).upper() == "TH"):
                    if str(x._tag).upper() == "TH":
                        class_base = "phanterpwa-widget-table-head-th"
                    else:
                        class_base = "phanterpwa-widget-table-head-td"
                    if "_class" in x.attributes:

                        if class_base not in x.attributes['_class']:
                            x.attributes['_class'] = "{0} {1}".format(x.attributes['_class'], class_base)
                    else:
                        x.attributes['_class'] = class_base
                        self.__child_html.append(x)
                elif isinstance(x, (list, tuple)):
                    if x[0] in self._sortable:
                        if self._sort_by == x[0]:
                            self.__child_html.append(TH(DIV(
                                    x[1],
                                    **{"_class": "phanterpwa-widget-table-head-th-sortable",
                                    "_data-value": x[0]}
                                ),
                                _class="phanterpwa-widget-table-head-th enabled {0}".format(sort_order)))
                        else:
                            self.__child_html.append(TH(DIV(
                                    x[1],
                                    **{"_class": "phanterpwa-widget-table-head-th-sortable",
                                    "_data-value": x[0]}
                                ),
                                _class="phanterpwa-widget-table-head-th"))

                    else:
                        self.__child_html.append(TH(x[1],
                            _class="phanterpwa-widget-table-head-th")
                        )
                else:
                    self.__child_html.append(TH(x,
                            _class="phanterpwa-widget-table-head-th"))
        else:
            for x in content:
                if isinstance(x, helpers.XmlConstructor) and (str(x._tag).upper() == "TD" or str(x._tag).upper() == "TH"):
                    if str(x._tag).upper() == "TH":
                        class_base = "phanterpwa-widget-table-head-th"
                    else:
                        class_base = "phanterpwa-widget-table-head-td"
                    if "_class" in x.attributes:

                        if class_base not in x.attributes['_class']:
                            x.attributes['_class'] = "{0} {1}".format(x.attributes['_class'], class_base)
                    else:
                        x.attributes['_class'] = class_base
                    self.__child_html.append(x)
                else:
                    self.__child_html.append(TH(x,
                        _class="phanterpwa-widget-table-head-th"))

    def len_head(self):
        return self._count_th

    def sorted_field(self):
        target = jQuery(self.target_selector)
        enabled = target.find(".phanterpwa-widget-table-head-th.enabled")
        container = enabled.find(".phanterpwa-widget-table-head-th-sortable")
        sort = "asc"
        if enabled.hasClass("desc"):
            sort = "desc"
        return [container.data("value"), sort]

    def append(self, value):
        self.__child_html.content.append(TH(value, _class="phanterpwa-widget-table-head-th"))

    def insert(self, pos, value):
        self.__child_html.content.insert(pos, TH(value, _class="phanterpwa-widget-table-head-th"))

    def _after_click_sortable(self, ev, el):
        el = jQuery(el)
        p = el.parent()
        if p.hasClass("asc"):
            jQuery(self.target_selector).find(
                ".phanterpwa-widget-table-head-th").removeClass("asc")
            p.addClass("desc")
        elif p.hasClass("desc"):
            jQuery(self.target_selector).find(
                ".phanterpwa-widget-table-head-th").removeClass("desc")
            p.addClass("asc")
        else:
            jQuery(self.target_selector).find(
                ".phanterpwa-widget-table-head-th").removeClass("asc").removeClass("desc").removeClass("enabled")
            p.addClass("asc").addClass("enabled")
        if callable(self._on_click_sortable):
            self._on_click_sortable(self)

    def reload(self):
        self.start()

    def start(self):
        target = jQuery(self.target_selector)
        container = target.find(".phanterpwa-widget-table-head-th").find(".phanterpwa-widget-table-head-th-sortable")
        container.off("click.widget-table-sortable").on(
            "click.widget-table-sortable",
            lambda ev: self._after_click_sortable(ev, this)
        )


class TableData(Widget):
    def __init__(self, identifier, *content, **parameters):
        self.__dropable = parameters.get("drag_and_drop", True)
        self._after_drop = parameters.get("after_drop", None)
        self._drop_if = parameters.get("drop_if", None)
        if self.__dropable:
            parameters["_draggable"] = "true"
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-table-data")
        else:
            parameters["_class"] = "phanterpwa-widget-table-data"
        self.__child_html = CONCATENATE()
        for x in content:
            if isinstance(x, helpers.XmlConstructor) and (str(x._tag).upper() == "TD" or str(x._tag).upper() == "TH"):
                if str(x._tag).upper() == "TH":
                    class_base = "phanterpwa-widget-table-data-th"
                else:
                    class_base = "phanterpwa-widget-table-data-td"
                if "_class" in x.attributes:

                    if class_base not in x.attributes['_class']:
                        x.attributes['_class'] = "{0} {1}".format(x.attributes['_class'], class_base)
                else:
                    x.attributes['_class'] = class_base
                self.__child_html.append(x)
            else:
                self.__child_html.append(TD(x, _class="phanterpwa-widget-table-data-td"))
        Widget.__init__(self, identifier, self.__child_html, **parameters)
        self.tag = "tr"

    def _ondrop(self, ev, el):
        can_drop = True
        if callable(self._drop_if):
            if not self._drop_if(window.PhanterPWA.drag["el"], el):
                can_drop = False
        if can_drop:
            posY = ev.screenY
            if posY > window.PhanterPWA.drag["posY"]:
                jQuery(window.PhanterPWA.drag["el"]).insertAfter(el)
            else:
                jQuery(window.PhanterPWA.drag["el"]).insertBefore(el)
            if callable(self._after_drop):
                self._after_drop(ev, el)

    def _ondragstart(self, ev, el):
        window.PhanterPWA.drag = {"el": el, "posY": ev.screenY}

    def reload(self):
        self.start()

    def start(self):
        target = jQuery(self.target_selector)
        target.off("drop.widget-table-drop").on(
            "drop.widget-table-drop",
            lambda ev: self._ondrop(ev, this)
        )
        target.off("dragstart.widget-table-dragstart").on(
            "dragstart.widget-table-dragstart",
            lambda ev: self._ondragstart(ev, this)
        )
        target.off("dragover.widget-table-dropover").on(
            "dragover.widget-table-dropover",
            lambda ev: ev.preventDefault()
        )


class TableFooterPagination(Widget):
    def __init__(self, identifier, *content, **parameters):
        self.identifier = identifier
        self._table = None
        self._page = parameters.get("page", 1)
        self._total_pages = parameters.get("total_pages", 1)
        self._colspan = parameters.get("colspan", 1)
        self._on_click_page = parameters.get("on_click_page", None)
        self._modal = None
        self.set_z_index(parameters.get("z_index", None))
        self.set_recalc_on_scroll(parameters.get("recalc_on_scroll", True))
        if str(self._page).isdigit():
            self._page = int(self._page)
        else:
            self._page = 1
        if str(self._total_pages).isdigit():
            self._total_pages = int(self._total_pages)
        else:
            self._total_pages = 1
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-table-pagination")
        else:
            parameters["_class"] = "phanterpwa-widget-table-pagination"
        self._create_footer(content)
        Widget.__init__(self, identifier, self.__child_html, **parameters)
        self.tag = "tr"

    def _create_footer(self):
        first_button = DIV(
            I(_class="fas fa-angle-double-left"),
            **{"_data-page": 1,
                "_class": "phanterpwa-widget-pagination-first_button{0}".format(
                    " disabled" if self._page == 1 else "")
            }
        )
        previous_button = DIV(
            I(_class="fas fa-angle-left"),
            **{"_data-page": self._page - 1,
                "_class": "phanterpwa-widget-pagination-previous_button{0}".format(
                    " disabled" if self._page == 1 else "")
            }
        )
        status_button = DIV(
            I18N("Page "), self._page, I18N(" of "), self._total_pages,
            **{"_id": "phanterpwa-widget-pagination-status_button-{0}".format(self.identifier),
                "_class": "phanterpwa-widget-pagination-status_button"
            }
        )
        next_button = DIV(
            I(_class="fas fa-angle-right"),
            **{"_data-page": self._page + 1,
                "_class": "phanterpwa-widget-pagination-next_button{0}".format(
                    " disabled" if self._page == self._total_pages else "")
            }
        )
        last_button = DIV(
            I(_class="fas fa-angle-double-right"),
            **{"_data-page": self._total_pages,
                "_class": "phanterpwa-widget-pagination-last_button{0}".format(
                    " disabled" if self._page == self._total_pages else "")
            }
        )

        self.__child_html = TD(
            DIV(
                first_button,
                previous_button,
                status_button,
                next_button,
                last_button,
                _id="phanterpwa-widget-pagination-container-{0}".format(self.identifier),
                _class="phanterpwa-widget-pagination-container"
            ),
            _id="phanterpwa-widget-table-pagination-td-{0}".format(self.identifier),
            _colspan = self._colspan
        )

    def set_recalc_on_scroll(self, value):
        if isinstance(value, bool):
            self._recalc_on_scroll = value
        else:
            console.error("The recalc_on_scroll must be boolean!")

    def set_z_index(self, value):
        if str(value).isdigit():
            self._z_index = value
        elif value is None:
            self._z_index = None
        else:
            self._z_index = None
            console.error("The z_index must be integer or None!")

    def append(self, value):
        self.__child_html.content.append(TH(value, _class="phanterpwa-widget-table-head-th"))

    def insert(self, pos, value):
        self.__child_html.content.insert(pos, TH(value, _class="phanterpwa-widget-table-head-th"))

    def _pages_panel(self):
        pages_panel = DIV(
            _class="phanterpwa-widget-pagination-pages_panel p-row"
        )
        mid = 13
        if self.page > mid:
            if self.page < (self._total_pages // 2) or ((self.page + 12) < self._total_pages):
                for x in range(self.page - 13, self.page - 1):
                    buttom_page = x + 1
                    pages_panel.append(DIV(DIV(buttom_page, 
                            **{"_class": "icon_button wave_on_click",
                            "_data-page": buttom_page}),
                        _class="p-col w1p20"))
                buttom_page = self.page
                pages_panel.append(DIV(DIV(buttom_page, 
                        **{"_class": "icon_button wave_on_click",
                        "_data-page": buttom_page}),
                    _class="p-col w1p20 current_page"))
                if self._total_pages > (self.page + 12):
                    for z in range(self.page, self.page + 12):
                        buttom_page = z + 1
                        pages_panel.append(DIV(DIV(buttom_page, 
                                **{"_class": "icon_button wave_on_click",
                                "_data-page": buttom_page}),
                            _class="p-col w1p20"))
                else:
                    for z in range(self.page, self._total_pages):
                        buttom_page = z + 1
                        pages_panel.append(DIV(DIV(buttom_page, 
                                **{"_class": "icon_button wave_on_click",
                                "_data-page": buttom_page}),
                            _class="p-col w1p20"))
            else:
                if self._total_pages >= 25:
                    for x in range(self._total_pages - 24, self._total_pages + 1):
                        buttom_page = x
                        if x == self.page:
                            pages_panel.append(DIV(DIV(buttom_page,
                                    **{"_class": "icon_button wave_on_click",
                                    "_data-page": buttom_page}),
                                _class="p-col w1p20 current_page"))
                        else:
                            pages_panel.append(DIV(DIV(buttom_page,
                                    **{"_class": "icon_button wave_on_click",
                                    "_data-page": buttom_page}),
                                _class="p-col w1p20"))
                else:
                    for x in range(1, self._total_pages):
                        buttom_page = x
                        if x == self.page:
                            pages_panel.append(DIV(DIV(buttom_page,
                                    **{"_class": "icon_button wave_on_click",
                                    "_data-page": buttom_page}),
                                _class="p-col w1p20 current_page"))
                        else:
                            pages_panel.append(DIV(DIV(buttom_page,
                                    **{"_class": "icon_button wave_on_click",
                                    "_data-page": buttom_page}),
                                _class="p-col w1p20"))
        else:
            for z in range(25):
                if z < (self._total_pages):
                    buttom_page = z + 1
                    if (z + 1) == self.page:
                        pages_panel.append(DIV(DIV(buttom_page,
                                **{"_class": "icon_button wave_on_click",
                                "_data-page": buttom_page}),
                            _class="p-col w1p20 current_page"))
                    else:
                        pages_panel.append(DIV(DIV(buttom_page,
                                **{"_class": "icon_button wave_on_click",
                                "_data-page": buttom_page}),
                            _class="p-col w1p20"))
        self._modal = PseudoModal(
            "#phanterpwa-widget-pagination-container-{0}".format(self.identifier),
            pages_panel,
            z_index=self._z_index,
            recalc_on_scroll=self._recalc_on_scroll
        )
        self._modal.start()
        self._bind_panel_pages()

    def _bind_panel_pages(self):
        target = jQuery("#{0}".format(self._modal._identifier))
        target.find(".icon_button").off("click.icon_buttom_pagination").on(
            "click.icon_buttom_pagination",
            lambda: (self._on_click_buttom_page(this), self._modal.close())
        )

    def _open_panel_pages(self, el):
        p = jQuery(el).parent()
        p.addClass("enabled")
        self._pages_panel()

    def _on_click_buttom_page(self, el):
        page = jQuery(el).data("page")
        self._page = page
        if callable(self._on_click_page):
            self._on_click_page(self)

    def page(self):
        return self._page

    def reload(self):
        self.start()

    def start(self):
        target = jQuery(self.target_selector)
        container = target.find(".phanterpwa-widget-table-head-th").find(".phanterpwa-widget-table-head-th-sortable")
        container.off("click.widget-table-sortable").on(
            "click.widget-table-sortable",
            lambda ev: self._after_click_sortable(ev, this)
        )
        jQuery("#phanterpwa-widget-table-pagination-td-{0}".format(self.identifier)).attr("colspan", self._colspan)
        target.find("#phanterpwa-widget-pagination-status_button-{0}".format(self.identifier)).off(
            "click.table_pagination"
        ).on(
            "click.table_pagination",
            lambda: self._open_panel_pages(this)
        )
        pre = target.find(".phanterpwa-widget-pagination-previous_button")
        if not pre.hasClass("disabled"):
            pre.off("click.btn_pagination").on("click.btn_pagination", lambda: self._on_click_buttom_page(this))
        nex = target.find(".phanterpwa-widget-pagination-next_button")
        if not nex.hasClass("disabled"):
            nex.off("click.btn_pagination").on("click.btn_pagination", lambda: self._on_click_buttom_page(this))
        fir = target.find(".phanterpwa-widget-pagination-first_button")
        if not fir.hasClass("disabled"):
            fir.off("click.btn_pagination").on("click.btn_pagination", lambda: self._on_click_buttom_page(this))
        las = target.find(".phanterpwa-widget-pagination-last_button")
        if not las.hasClass("disabled"):
            las.off("click.btn_pagination").on("click.btn_pagination", lambda: self._on_click_buttom_page(this))


class Image(Widget):
    def __init__(self, identifier, **parameters):
        self._name = parameters.get("name", None)
        self._value = parameters.get("value", None)
        self._icon = parameters.get("icon", None)
        self._form = parameters.get("form", None)
        self._cutter = parameters.get("cutter", False)
        self._nocache = parameters.get("nocache", False)
        self._width = parameters.get("width", 190)
        self._height = parameters.get("height", 200)
        self._data_view = parameters.get("data_view", False)
        self.identifier = identifier
        self.__child_html = DIV(
            _id="phanterpwa-widget-image-wrapper-{0}".format(identifier),
            _class="phanterpwa-widget-image-wrapper"
        )
        self.iniciate = False
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-widget-image")
        else:
            parameters['_class'] = "phanterpwa-widget-image"
        if self._nocache and (self._value is not "" and self._value is not None):
            now = __new__(Date().getTime())
            self._value = "{0}?nocache={1}".format(self._value, now)
        Widget.__init__(self, identifier, self.__child_html, **parameters)

    def _binds(self):
        GalleryInput(
            "#phanterpwa-widget-image-wrapper-{0}".format(self.identifier),
            **{
                "name": self._name,
                "cutter": self._cutter,
                "current_image": self._value,
                "img_name": "Image_{0}".format(self.identifier),
                "width": self._width,
                "height": self._height,
                "data_view": self._data_view
            }
        )

    def reload(self):
        if not self.iniciate:
            self.iniciate = True
            self.start()

    def start(self):
        self._binds()


class GalleryInput():
    def __init__(self, target_selector, **parameters):
        self.target_selector = target_selector
        self.config = parameters
        self.namespace = window.PhanterPWA.get_id("namespace")
        self.conf_default = {
            "name": None,
            "button-upload": I(_class="fas fa-cloud-upload-alt").xml(),
            "width": 190,
            "height": 200,
            "view-width": None,
            "view-height": None,
            "cutter": False,
            "z-index": 1005,
            "current_image": None,
            "put_in_form": True,
            "img_name": "PhanterpwaGalleryFile",
            "hammerconf": {
                'inputClass': Hammer.PointerEventInput if Hammer.SUPPORT_POINTER_EVENTS else Hammer.TouchInput
            },
            "onError": None,
            "beforeCut": None,
            "afterCut": None,
            "data_view": False
        }
        if self.config is js_undefined:
            self.config = dict()
        for d in self.conf_default.keys():
            if d not in self.config:
                self.config[d] = self.conf_default[d]
        self.config["namespace"] = self.namespace
        self.config["element"] = jQuery(self.target_selector)
        if self.config["view-width"] is None or self.config["view-width"] is js_undefined:
            self.config["view-width"] = self.config["width"]
        if self.config["view-height"] is None or self.config["view-height"] is js_undefined:
            self.config["view-height"] = self.config["height"]
        self._data_view = self.config.get("data_view", False)
        self.addInputPanel()

    def getNewImage(self):

        def inputChange(el):
            is_to_cut = self.config['cutter']
            blob = jQuery(el)[0].files
            fileslength = blob.length
            for i in range(fileslength):
                img_type = blob[i]['type']
                img_name = blob[i]['name']
                self.config["img_type"] = img_type
                self.config["img_name"] = img_name
                if img_type == "image/png" or\
                        img_type == "image/bmp" or\
                        img_type == "image/gif" or\
                        img_type == "image/jpeg":
                    def onloadend(reader, img_name, img_type):
                        base64data = reader.result
                        img1 = document.createElement("IMG")
                        img1.src = base64data
                        img1.alt = img_name + " (" + img_type + ")"
                        if is_to_cut:
                            def onImageLoad(img):
                                if window.PhanterPWA.DEBUG:
                                    console.info(img.width, img.height)

                            img1.onload = lambda: onImageLoad(this)

                            __new__(GalleryCutter(
                                base64data, self
                            ))
                        else:
                            self.simpleView(base64data)

                    reader = __new__(FileReader())
                    reader.readAsDataURL(blob[0])
                    reader.onloadend = lambda: onloadend(reader, img_name, img_type)
                else:
                    console.error("The file has invalid type. It must be png, bmp, gif, jpeg type.")
        el_input = jQuery("#phanterpwa-gallery-input-file-{0}".format(self.namespace))
        el_input.trigger(
            "click"
        ).off(
            "change.phanterpwa_gallery_input_{0}".format(self.namespace)
        ).on(
            "change.phanterpwa_gallery_input_{0}".format(self.namespace),
            lambda: inputChange(this, self.config)
        )

    def _afterRead(self):
        if self.config['current_image'] is not None and self.config['current_image'] is not js_undefined:
            self.simpleView(self.config['current_image'])
        else:
            jQuery(
                "#phanterpwa-gallery-upload-image-button-{0}".format(self.namespace)
            ).on(
                "click",
                lambda: self.getNewImage()
            )

    def addInputPanel(self):

        other_inputs = ""
        if self.config['cutter']:
            cutter_vars = [
                INPUT(
                    _id='phanterpwa-gallery-input-cutterSizeX{0}'.format(self.namespace),
                    _name='phanterpwa-gallery-input-cutterSizeX',
                    _value="",
                    _type="text"
                ),
                INPUT(
                    _id='phanterpwa-gallery-input-cutterSizeY{0}'.format(self.namespace),
                    _name='phanterpwa-gallery-input-cutterSizeY',
                    _value="",
                    _type="text"
                ),
                INPUT(
                    _id='phanterpwa-gallery-input-positionX{0}'.format(self.namespace),
                    _name='phanterpwa-gallery-input-positionX',
                    _value="",
                    _type="text"
                ),
                INPUT(
                    _id='phanterpwa-gallery-input-positionY{0}'.format(self.namespace),
                    _name='phanterpwa-gallery-input-positionY',
                    _value="",
                    _type="text"
                ),
                INPUT(
                    _id='phanterpwa-gallery-input-newSizeX{0}'.format(self.namespace),
                    _name='phanterpwa-gallery-input-newSizeX',
                    _value="",
                    _type="text"
                ),
                INPUT(
                    _id='phanterpwa-gallery-input-newSizeY{0}'.format(self.namespace),
                    _name='phanterpwa-gallery-input-newSizeY',
                    _value="",
                    _type="text"
                ),
                INPUT(
                    _id='phanterpwa-gallery-input-rotation{0}'.format(self.namespace),
                    _name='phanterpwa-gallery-input-rotation',
                    _value="",
                    _type="text"
                )
            ]
            other_inputs = DIV(
                *cutter_vars,
                _class="phanterpwa-gallery-inputs-container-{0}".format(self.namespace),
                _style="display: none"
            )
        input_gallery = DIV(
            DIV(
                DIV(
                    XML(self.config['button-upload']),
                    _id="phanterpwa-gallery-upload-image-button-{0}".format(self.namespace),
                    _class="phanterpwa-gallery-upload-image-button link",
                    _phanterpwa_input="phanterpwa-gallery-input-file-{0}".format(self.namespace)
                ),
                _id="phanterpwa-gallery-upload-image-default-{0}".format(self.namespace),
                _class="phanterpwa-gallery-upload-image-default"
            ),
            INPUT(
                _accept="image/png, image/jpeg, image/gif, image/bmp",
                _class="phanterpwa-gallery-upload-input-file",
                _type="file",
                _id="phanterpwa-gallery-input-file-{0}".format(self.namespace),
                _name="phanterpwa-gallery-file-input"
            ),
            _id="phanterpwa-gallery-input-container-{0}".format(self.namespace),
            _class="phanterpwa-gallery-input-container"
        )
        wrapper_gallery = DIV(
            input_gallery,
            other_inputs,
            _id="phanterpwa-gallery-wrapper-{0}".format(self.namespace),
            _class="phanterpwa-gallery-wrapper"
        )

        html = DIV(
            DIV(
                DIV(
                    DIV(
                        wrapper_gallery,
                        _class="phanterpwa-centralizer-center"
                    ),
                    _class="phanterpwa-centralizer-horizontal"
                ),
                _class="phanterpwa-centralizer-vertical"
            ),
            _class="phanterpwa-centralizer-wrapper",
            _style="width: {0}px; height: {1}px;".format(self.config['view-width'], self.config['view-height'])
        )
        jQuery(self.target_selector).html(
            html.xml()
        ).promise().then(
            lambda: self._afterRead()
        )

    def simpleView(self, url):
        namespace = self.config['namespace']
        width = self.config["width"]
        height = self.config["height"]
        img_name = self.config["img_name"]

        cutted_img = document.createElement("IMG")
        cutted_img.src = url
        cutted_img.alt = img_name

        def onImageLoad(img, namespace, width, height):
            width_view = width
            height_view = height
            if width_view == height_view:
                if img.width > img.height:
                    jQuery(
                        "#phanterpwa-gallery-upload-image-simple-view-{0}".format(namespace)
                    ).css(
                        "background-size", "100% auto"
                    )
                else:
                    jQuery(
                        "#phanterpwa-gallery-upload-image-simple-view-{0}".format(namespace)
                    ).css(
                        "background-size", "auto 100%"
                    )
            elif width_view > height_view:
                if img.width > img.height:
                    rate = float(height_view) / img.height
                    width = img.width * rate
                    if width < width_view:
                        jQuery(
                            "#phanterpwa-gallery-upload-image-simple-view-{0}".format(namespace)
                        ).css(
                            "background-size", "100% auto"
                        )
                    else:
                        jQuery(
                            "#phanterpwa-gallery-upload-image-simple-view-{0}".format(namespace)
                        ).css(
                            "background-size", "auto 100%"
                        )
                else:
                    jQuery(
                        "#phanterpwa-gallery-upload-image-simple-view-{0}".format(namespace)
                    ).css(
                        "background-size", "100% auto"
                    )
            elif width_view < height_view:
                if img.width < img.height:
                    rate = float(height_view) / img.height
                    width = img.width * rate
                    if width > width_view:
                        jQuery(
                            "#phanterpwa-gallery-upload-image-simple-view-{0}".format(namespace)
                        ).css(
                            "background-size", "auto 100%"
                        )
                    else:
                        jQuery(
                            "#phanterpwa-gallery-upload-image-simple-view-{0}".format(namespace)
                        ).css(
                            "background-size", "100% auto"
                        )
                else:
                    jQuery(
                        "#phanterpwa-gallery-upload-image-simple-view-{0}".format(namespace)
                    ).css(
                        "background-size", "auto 100%"
                    )
        cutted_img.onload = lambda: onImageLoad(this, namespace, width, height)
        xml_icons_view = ""
        if not self._data_view:
            xml_icons_view = DIV(
                DIV(
                    I(_class="fas fa-sync"),
                    _id="phanterpwa-gallery-upload-image-simple-view-button-reload-{0}".format(namespace),
                    _class="phanterpwa-gallery-upload-image-simple-view-button {0}".format(
                        "phanterpwa-gallery-upload-image-simple-view-button-reload"
                    )
                ),
                DIV(
                    I(_class="fas fa-trash-alt"),
                    _id="phanterpwa-gallery-upload-image-simple-view-button-delete-{0}".format(namespace),
                    _class="phanterpwa-gallery-upload-image-simple-view-button {0}".format(
                        "phanterpwa-gallery-upload-image-simple-view-button-delete"
                    )
                ),
                _class="phanterpwa-gallery-upload-image-simple-view-buttons"
            )
        html_simple_view = DIV(
            xml_icons_view,
            _id="phanterpwa-gallery-upload-image-simple-view-{0}".format(namespace),
            _class="phanterpwa-gallery-upload-image-simple-view",
            _alt=img_name,
            _style="width: {0}px; height: {1}px; background-image: url('{2}'); {3}".format(
                width,
                height,
                url,
                "background-position: center; overflow: hidden;"
            )
        )

        def activeButtonsView():
            jQuery(
                "#phanterpwa-gallery-upload-image-simple-view-button-reload-{0}".format(namespace)
            ).off(
                "click.button-reload-view"
            ).on(
                "click.button-reload-view",
                lambda: self.getNewImage()
            )
            jQuery(
                "#phanterpwa-gallery-upload-image-simple-view-button-delete-{0}".format(namespace)
            ).off(
                "click.button-reload-view"
            ).on(
                "click.button-reload-view",
                lambda: self.resetInputPanel()
            )

        jQuery("#phanterpwa-gallery-upload-image-default-{0}".format(namespace)).html(html_simple_view.xml()).promise().then(
            lambda: activeButtonsView()
        )

    def resetInputPanel(self):
        self.config["current_image"] = None
        self.addInputPanel()


class GalleryCutter():
    def __init__(self, base64data, galleryinput):
        self.base64data = base64data

        if isinstance(galleryinput, GalleryInput):
            self.galleryinput = galleryinput
        else:
            raise ValueError("The galleryinput must be GalleryInput instance")
        self.config = galleryinput.config
        __pragma__('jsiter')
        self.hammerconf = {}
        __pragma__('nojsiter')
        if self.config["hammerconf"] is not None or self.config["hammerconf"] is not js_undefined:
            for x in self.config["hammerconf"].keys():
                self.hammerconf[x] = self.config["hammerconf"][x]
        self.namespace = self.galleryinput.namespace
        self.cutterSizeX = self.config['width']
        self.cutterSizeY = self.config['height']
        self.originalWidthImg = 0
        self.originalHeightImg = 0
        self.widthImg = 0
        self.heightImg = 0
        self.widthScreen = 0
        self.heightScreen = 0
        self.widthCutter = 0
        self.heightCutter = 0
        self.inicialPositionXBackground = 0
        self.inicialPositionYBackground = 0
        self.inicialPositionXImgToCut = 0
        self.inicialPositionYImgToCut = 0
        self.deslocationPositionXBackground = 0
        self.deslocationPositionYBackground = 0
        self.deslocationPositionXImgToCut = 0
        self.deslocationPositionYImgToCut = 0
        self.deslocationPositionZoom = 0
        self.positionDefaultZoom = 89.0
        self.widthImgAfterZoom = 0
        self.heightImgAfterZoom = 0
        self.positionXAfterZoom = 0
        self.positionYAfterZoom = 0
        self.activeViewImage = False
        self.addCutterPanel()

    def addCutterPanel(self):
        z_index = self.config["z-index"]
        cutter_panel = DIV(
            DIV(
                _id="phanterpwa-gallery-cutter-background-{0}".format(self.namespace),
                _class="phanterpwa-gallery-cutter-background"),
            DIV(
                _id="phanterpwa-gallery-cutter-shadow-{0}".format(self.namespace),
                _class="phanterpwa-gallery-cutter-shadow"),
            DIV(
                DIV(
                    DIV(
                        _class="phanterpwa-gallery-panel-cutter-image",
                        _id='phanterpwa-gallery-panel-cutter-image-{0}'.format(self.namespace)),
                    _style="overflow: hidden; width: {0}px; height: {1}px;".format(
                        self.cutterSizeX, self.cutterSizeY
                    ),
                    _id='phanterpwa-gallery-panel-cutter-size-container-{0}'.format(self.namespace),
                    _class="phanterpwa-gallery-panel-cutter-size-container"
                ),
                _class="phanterpwa-gallery-panel-cutter"
            ),
            DIV(
                _id='phanterpwa-gallery-cutter-pad-{0}'.format(self.namespace),
                _class="phanterpwa-gallery-cutter-pad"),
            DIV(
                DIV(
                    I(_class="fas fa-times-circle close-circle"),
                    _id='phanterpwa-gallery-cutter-control-close-{0}'.format(self.namespace),
                    _class="phanterpwa-gallery-cutter-control"),
                DIV(
                    I(_class="fas fa-eye image-view"),
                    _id='phanterpwa-gallery-cutter-control-view-{0}'.format(self.namespace),
                    _class="phanterpwa-gallery-cutter-control"),
                DIV(
                    I(_class="fas fa-cut image-cut"),
                    _id='phanterpwa-gallery-cutter-control-cut-{0}'.format(self.namespace),
                    _class="phanterpwa-gallery-cutter-control"),
                _class='phanterpwa-gallery-cutter-controls-container'),
            DIV(
                DIV(
                    I(_class="far fa-image image-decrease"),
                    DIV(
                        DIV(_id='phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace),
                            _class="phanterpwa-gallery-cutter-zoom-control"),
                        _id="phanterpwa-gallery-cutter-zoom-control-container-{0}".format(self.namespace),
                        _class="phanterpwa-gallery-cutter-zoom-control-container"
                    ),
                    I(_class="far fa-image image-increase"),
                    _class='phanterpwa-gallery-cutter-zoom-controls'),
                _class='phanterpwa-gallery-cutter-zoom-container'),
            _id='phanterpwa-gallery-panel-cutter-container-{0}'.format(self.namespace),
            _class="phanterpwa-gallery-panel-cutter-container",
            _style="z-index: {0};".format(z_index)
        )
        jQuery(
            "#phanterpwa-gallery-wrapper-{0}".format(self.namespace)
        ).append(
            cutter_panel.xml()
        ).promise().then(self._chargeEvents)

    def _chargeEvents(self):
        self.img1 = document.createElement("IMG")
        self.img2 = document.createElement("IMG")
        self.img1.onload = lambda: self.onLoadImage(self.img1)
        self.img1.src = self.base64data
        self.img2.src = self.base64data
        self.img1.onerror = lambda: self.setError(True)

    def prepareGestureMove(self, event):
        event.preventDefault()
        jQuery(
            '#phanterpwa-gallery-cutter-pad-{0}'.format(self.namespace)
        ).on(
            "panmove.phanterpwa-gallery-moving",
            lambda event: self.gestureMoving(event)
        )

        jQuery(
            '#phanterpwa-gallery-cutter-pad-{0}'.format(self.namespace)
        ).on(
            "panend.phanterpwa-gallery-moving",
            lambda event: self.stopGestureMove(event)
        )

    def gestureMoving(self, event):
        self.deslocationPositionXBackground = event.gesture.deltaX * (-1)
        self.deslocationPositionYBackground = event.gesture.deltaY * (-1)
        self.deslocationPositionXImgToCut = event.gesture.deltaX * (-1)
        self.deslocationPositionYImgToCut = event.gesture.deltaY * (-1)
        self.calcPosition()

    def stopGestureMove(self, event):
        event.preventDefault()
        jQuery(
            '#phanterpwa-gallery-cutter-pad-{0}'.format(self.namespace)
        ).off(
            "panmove.phanterpwa-gallery-moving"
        )
        self.saveinicialPosition()

    def gestureSizing(self, event, inicialPosition, width, height):
        event.preventDefault()
        xDeslocamento = event.gesture.deltaX
        if (((inicialPosition + xDeslocamento) > 0) and (inicialPosition + xDeslocamento) < 179):
            self.movecutterZoom(xDeslocamento, inicialPosition, width, height)

    def stopGestureSize(self, event):
        event.preventDefault()
        self.savePositionZoom()
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace)
        ).off(
            'panmove.phanterpwa-gallery-sizing'
        )

    def prepareGestureSize(self, event):
        event.preventDefault()
        
        inicialPosition = self.positionDefaultZoom
        width = self.widthImg
        height = self.heightImg
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace)
        ).on(
            'panmove.phanterpwa-gallery-sizing',
            lambda event: self.gestureSizing(event, inicialPosition, width, height)
        )
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace)
        ).on(
            'panend.phanterpwa-gallery-sizing',
            lambda event: self.stopGestureSize(event)
        )

    def calcMidPosition(self, sizeContainer, sizeContent, positionContent):
        midsize1 = sizeContainer / 2.0
        midsize2 = sizeContent / 2.0
        relativeposition = midsize1 - midsize2
        finalPosition = relativeposition - positionContent
        return finalPosition

    def moveImage(self, x, y):
        self.deslocationPositionXBackground = x * (-1)
        self.deslocationPositionYBackground = y * (-1)
        self.deslocationPositionXImgToCut = x * (-1)
        self.deslocationPositionYImgToCut = y * (-1)
        self.calcPosition()

    def viewImage(self):
        if (self.activeViewImage):
            self.activeViewImage = False
            jQuery("#phanterpwa-gallery-cutter-control-view-{0}".format(self.namespace)).removeClass("enable")
            jQuery("#phanterpwa-gallery-cutter-shadow-{0}".format(self.namespace)).removeClass("enable")
        else:
            self.activeViewImage = True
            jQuery("#phanterpwa-gallery-cutter-control-view-{0}".format(self.namespace)).addClass("enable")
            jQuery("#phanterpwa-gallery-cutter-shadow-{0}".format(self.namespace)).addClass("enable")

    def closeImage(self):
        jQuery('#phanterpwa-gallery-panel-cutter-container-{0}'.format(self.namespace)).removeClass("enable")
        jQuery('#phanterpwa-gallery-panel-cutter-container-{0}'.format(self.namespace)).addClass("close")

    def cutImage(self):
        jQuery('#phanterpwa-gallery-panel-cutter-container-{0}'.format(self.namespace)).removeClass("enable")
        jQuery('#phanterpwa-gallery-panel-cutter-container-{0}'.format(self.namespace)).addClass("close")
        canvas = document.createElement("CANVAS")
        canvas.width = self.widthCutter
        canvas.height = self.heightCutter
        ctx = canvas.getContext('2d')
        ratio = self.originalWidthImg / float(self.widthImgAfterZoom)
        positionX = self.positionXAfterZoom * (-1) * ratio
        positionY = self.positionYAfterZoom * (-1) * ratio
        wX = self.cutterSizeX * ratio
        wY = self.cutterSizeY * ratio
        jQuery('#phanterpwa-gallery-input-cutterSizeX{0}'.format(self.namespace)).val(self.widthCutter)
        jQuery('#phanterpwa-gallery-input-cutterSizeY{0}'.format(self.namespace)).val(self.heightCutter)
        jQuery('#phanterpwa-gallery-input-positionX{0}'.format(self.namespace)).val(positionX)
        jQuery('#phanterpwa-gallery-input-positionY{0}'.format(self.namespace)).val(positionY)
        jQuery('#phanterpwa-gallery-input-newSizeX{0}'.format(self.namespace)).val(wX)
        jQuery('#phanterpwa-gallery-input-newSizeY{0}'.format(self.namespace)).val(wY)
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        ctx.drawImage(self.img1, positionX, positionY, wX, wY, 0, 0, self.widthCutter, self.heightCutter)
        self.config["current_image"] = canvas.toDataURL()
        self.galleryinput.config = self.config
        self.galleryinput.simpleView(self.config["current_image"])

    def movecutterZoom(self, x, zoominicial, width, height):
        self.deslocationPositionZoom = x * (-1)
        self.calcZoomPosition(zoominicial, width, height)

    def changeSizeImage(self, ratio, width, height):
        width = float(width) * ratio
        height = float(height) * ratio
        self.img1.style.width = width + "px"
        self.img1.style.height = height + "px"
        self.img2.style.width = width + "px"
        self.img2.style.height = height + "px"
        self.widthImg = width
        self.heightImg = height
        self.widthImgAfterZoom = width
        self.heightImgAfterZoom = height
        self.calcPosition()

    def calcZoomPosition(self, zoominicial, width, height):
        position = self.positionDefaultZoom - self.deslocationPositionZoom
        ratio = position / zoominicial
        self.changeSizeImage(ratio, width, height)
        jQuery('#phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace)).css("left", position + "px")

    def calcPosition(self):
        widthImg = self.widthImg
        heightImg = self.heightImg
        widthScreen = window.innerWidth
        heightScreen = window.innerHeight
        widthCutter = self.widthCutter
        heightCutter = self.heightCutter
        if((widthImg > 0) and (heightImg > 0) and (widthScreen > 0) and (heightScreen > 0)):
            fCalc = self.calcMidPosition
            iPXB = self.inicialPositionXBackground + self.deslocationPositionXBackground
            iPYB = self.inicialPositionYBackground + self.deslocationPositionYBackground
            iPXITC = self.inicialPositionXImgToCut + self.deslocationPositionXImgToCut
            iPYITC = self.inicialPositionYImgToCut + self.deslocationPositionYImgToCut
            relativePositionXBackground = fCalc(widthScreen, widthImg, iPXB)
            relativePositionYBackground = fCalc(heightScreen, heightImg, iPYB)
            relativePositionXImgToCut = fCalc(widthCutter, widthImg, iPXITC)
            relativePositionYImgToCut = fCalc(heightCutter, heightImg, iPYITC)
            jQuery('#phanterpwa-gallery-panel-cutter-size-container-{0}'.format(self.namespace)).css(
                "left", fCalc(widthScreen, widthCutter, 0) + "px")
            jQuery('#phanterpwa-gallery-panel-cutter-size-container-{0}'.format(self.namespace)).css(
                "top", fCalc(heightScreen, heightCutter, 0) + "px")
            jQuery("#phanterpwa-gallery-cutter-background-{0}".format(self.namespace)).css(
                "left", relativePositionXBackground + "px")
            jQuery("#phanterpwa-gallery-cutter-background-{0}".format(self.namespace)).css(
                "top", relativePositionYBackground + "px")
            jQuery('#phanterpwa-gallery-panel-cutter-image-{0}'.format(self.namespace)).css(
                "left", relativePositionXImgToCut + "px")
            jQuery('#phanterpwa-gallery-panel-cutter-image-{0}'.format(self.namespace)).css(
                "top", relativePositionYImgToCut + "px")
            self.positionXAfterZoom = relativePositionXImgToCut
            self.positionYAfterZoom = relativePositionYImgToCut

    def saveinicialPosition(self):
        self.inicialPositionXBackground += self.deslocationPositionXBackground
        self.inicialPositionYBackground += self.deslocationPositionYBackground
        self.inicialPositionXImgToCut += self.deslocationPositionXImgToCut
        self.inicialPositionYImgToCut += self.deslocationPositionYImgToCut
        self.deslocationPositionXBackground = 0
        self.deslocationPositionYBackground = 0
        self.deslocationPositionXImgToCut = 0
        self.deslocationPositionYImgToCut = 0

    def savePositionZoom(self):
        self.positionDefaultZoom -= self.deslocationPositionZoom
        self.deslocationPositionZoom = 0

    def setBase64(self, value):
        self.setBase64 = value

    def onLoadImage(self, img):
        jQuery("#phanterpwa-gallery-cutter-background-{0}".format(self.namespace)).html(self.img1)
        jQuery("#phanterpwa-gallery-panel-cutter-image-{0}".format(self.namespace)).html(self.img2)
        jQuery("#phanterpwa-gallery-cutter-control-view-{0}".format(self.namespace)).removeClass("enable")
        jQuery("#phanterpwa-gallery-cutter-shadow-{0}".format(self.namespace)).removeClass("enable")
        jQuery('#phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace)).css("left", "89px")
        jQuery("#phanterpwa-gallery-cutter-control-view-{0}".format(self.namespace)).on('click',
            lambda: self.viewImage()
        )

        jQuery(
            '#phanterpwa-gallery-cutter-control-close-{0}'.format(self.namespace)
        ).on(
            'click',
            lambda: self.closeImage()
        )

        jQuery(
            '#phanterpwa-gallery-cutter-control-cut-{0}'.format(self.namespace)
        ).on(
            'click',
            lambda: self.cutImage()
        )

        jQuery(
            window
        ).off(
            "resize.phanterpwa-gallery-{0}".format(self.namespace)
        ).on(
            "resize.phanterpwa-gallery-{0}".format(self.namespace),
            lambda: self.calcPosition()
        )

        jQuery(
            '#phanterpwa-gallery-cutter-pad-{0}'.format(self.namespace)
        ).on(
            'mousedown.phanterpwa-gallery-moving',
            lambda event: self.prepareMove(event)
        )

        jQuery(
            '#phanterpwa-gallery-cutter-pad-{0}'.format(self.namespace)
        ).hammer(
            self.hammerconf
        ).on(
            "touchstart.phanterpwa-gallery-moving",
            lambda event: self.prepareGestureMove(event)
        )

        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace)
        ).hammer(
            self.hammerconf
        ).on(
            'touchstart.phanterpwa-gallery-sizing',
            lambda event: self.prepareGestureSize(event)
        )

        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace)
        ).on(
            'mousedown.phanterpwa-gallery-sizing',
            lambda event: self.prepareSize(event)
        )
        imgWidth = img.width
        imgHeight = img.height
        self.widthImg = imgWidth
        self.heightImg = imgHeight
        self.originalWidthImg = imgWidth
        self.originalHeightImg = imgHeight
        self.widthImgAfterZoom = imgWidth
        self.heightImgAfterZoom = imgHeight

        self.widthCutter = float(self.cutterSizeX)
        self.heightCutter = float(self.cutterSizeY)
        if (self.error):
            console.error("has Error")
        else:
            self.calcPosition()
            jQuery('#phanterpwa-gallery-panel-cutter-container-{0}'.format(self.namespace)).removeClass("close")
            jQuery('#phanterpwa-gallery-panel-cutter-container-{0}'.format(self.namespace)).addClass("enable")

    def setError(self, bo):
        self.error = bo
        if self.config["onError"] is not None or self.config["onError"] is not js_undefined:
            self.config["onError"]()

    def moving(self, event, xInicial, yInicial):
        xDeslocamento = event.clientX - xInicial
        yDeslocamento = event.clientY - yInicial
        self.moveImage(xDeslocamento, yDeslocamento)

    def stopMove(self, event):
        self.saveinicialPosition()
        jQuery(
            '#phanterpwa-gallery-cutter-pad-{0}'.format(self.namespace)
        ).off(
            'mousemove.phanterpwa-gallery-moving'
        )

        jQuery(
            '#phanterpwa-gallery-cutter-pad-{0}'.format(self.namespace)
        ).off(
            'mouseleave.phanterpwa-gallery-moving'
        )

    def prepareMove(self, event):
        xInicial = event.clientX
        yInicial = event.clientY
        jQuery(
            '#phanterpwa-gallery-cutter-pad-{0}'.format(self.namespace)
        ).on(
            'mousemove.phanterpwa-gallery-moving',
            lambda event: self.moving(event, xInicial, yInicial)
        )
        jQuery(
            '#phanterpwa-gallery-cutter-pad-{0}'.format(self.namespace)
        ).on(
            'mouseup.phanterpwa-gallery-moving',
            lambda event: self.stopMove(event)
        )
        jQuery(
            '#phanterpwa-gallery-cutter-pad-{0}'.format(self.namespace)
        ).on(
            'mouseleave.phanterpwa-gallery-moving',
            lambda event: self.stopMove(event)
        )

    def sizing(self, event, xInicial, inicialPosition, width, height):
        xDeslocamento = event.clientX - xInicial
        if (((inicialPosition + xDeslocamento) > 0) and (inicialPosition + xDeslocamento) < 179):
            self.movecutterZoom(xDeslocamento, inicialPosition, width, height)

    def stopSize(self, event):
        self.savePositionZoom()
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace)
        ).off(
            'mousemove.phanterpwa-gallery-sizing'
        )
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace)
        ).off(
            'mouseleave.phanterpwa-gallery-sizing'
        )

    def prepareSize(self, event):
        xInicial = event.clientX
        inicialPosition = self.positionDefaultZoom
        width = self.widthImg
        height = self.heightImg
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace)
        ).on(
            'mousemove.phanterpwa-gallery-sizing',
            lambda event: self.sizing(event, xInicial, inicialPosition, width, height)
        )
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace)
        ).on(
            'mouseup.phanterpwa-gallery-sizing',
            lambda event: self.stopSize(event)
        )
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-{0}'.format(self.namespace)
        ).on(
            'mouseleave.phanterpwa-gallery-sizing',
            lambda event: self.stopSize(event)
        )


__pragma__('nokwargs')
