from phanterpwa.frontend import helpers
from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = Hammer =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')


INPUT = helpers.XmlConstructor.tagger("input", True)
I = helpers.XmlConstructor.tagger("i")
DIV = helpers.XmlConstructor.tagger("div")
SELECT = helpers.XmlConstructor.tagger("select")
OPTION = helpers.XmlConstructor.tagger("option")
FORM = helpers.XmlConstructor.tagger("form")
XML = helpers.XML


class phanterpwaSelect():
    def __init__(self, el, parameters=None):
        self.element = jQuery(el)
        self.json_select = None
        self.placeholder = self.element.attr("placeholder")
        self.onButtonClick = None
        if parameters is not None:
            self.element = el
            self.json_select = parameters['json_select']

            if 'placeholder' in parameters:
                self.placeholder = parameters['placeholder']

            if 'onButtonClick' in parameters:
                self.onButtonClick = parameters['onButtonClick']

            self.input_select = self.element.attr('phanterpwa-input-select')
        if self.json_select is None or self.json_select is js_undefined:
            if window.phanterpwaJsonSelects is not None and window.phanterpwaJsonSelects is not js_undefined:
                self.json_select = window.phanterpwaJsonSelects[self.input_select]
        if self.placeholder is None or self.placeholder is js_undefined:
            self.placeholder = ""

    def start(self):
        if self.input_select is not None and self.input_select is not js_undefined and \
                self.json_select is not None and self.json_select is not js_undefined:
            if self.onButtonClick is not None and self.onButtonClick is not js_undefined:
                jQuery(
                    "#phanterpwa-container-input-text-{0} .phanterpwa_input_icon_button".format(self.input_select)
                ).off(
                    "click.phanterpwa_input_icon_button"
                ).on(
                    "click.phanterpwa_input_icon_button",
                    lambda: self.onButtonClick(self.element)
                )
            input_name = self.input_select
            json_select = self.json_select
            placeholder = self.placeholder
            label = json_select['label']
            dft = json_select['default']
            data = json_select['data']
            jQuery("#phanterpwa-container-input-text-{0} .select-wrapper".format(input_name)).remove()
            vselect = SELECT(
            )
            has_default = False
            for x in data:
                if dft == x[0]:
                    has_default = True
                    vselect.append(
                        OPTION(x[1], _value=x[0], _selected="selected")
                    )
                else:
                    vselect.append(
                        OPTION(x[1], _value=x[0])
                    )
            phanterpwa_form_validator = self.element.attr("phanterpwa_form_validator")
            disabled = None
            if phanterpwa_form_validator is not None and phanterpwa_form_validator is not js_undefined:
                ppwa_fv = JSON.parse(phanterpwa_form_validator)
                if "IS_NOT_EMPTY" in ppwa_fv:
                    disabled = "disabled"

            if has_default:
                self.element.val(dft)
                vselect.insert(
                    0,
                    OPTION(placeholder, _value="", _disabled=disabled)
                )
            else:
                vselect.insert(
                    0,
                    OPTION(placeholder, _value="", _selected="selected", _disabled=disabled)
                )
            self.element.after(vselect.xml())
            value = jQuery(self.element).val()
            if value is None or value is js_undefined or value == "":
                jQuery("#phanterpwa-container-input-text-{0}".format(input_name)).addClass('input_is_empty')
            else:
                jQuery("#phanterpwa-container-input-text-{0}".format(input_name)).removeClass('input_is_empty')
            jQuery("#phanterpwa-container-input-text-{0}".format(input_name)).addClass('has_select')
            jQuery(
                "#phanterpwa-container-input-text-{0} .input-field>label".format(input_name)
            ).removeAttr("for").text(label)
            jQuery('#phanterpwa-container-input-text-{0} select'.format(input_name)).formSelect()

            def add_on_input(el):
                value = jQuery(el).val()
                if value is None or value is js_undefined or value == "":
                    jQuery("#phanterpwa-container-input-text-{0}".format(input_name)).addClass('input_is_empty')
                else:
                    jQuery("#phanterpwa-container-input-text-{0}".format(input_name)).removeClass('input_is_empty')
                self.element.val(value).trigger("change")
            jQuery(
                '#phanterpwa-container-input-text-{0} .select-wrapper select'.format(input_name)
            ).off(
                'change.change_{0}'.format(input_name),
            ).on(
                'change.change_{0}'.format(input_name),
                lambda: add_on_input(this)
            )
        return self.element
