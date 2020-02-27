from phanterpwa.apptools import (
    helpers,
    preloaders,
    validations,
    i18n
)
from phanterpwa.apptools.components import (
    widgets
)

# pragmas

from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = M = RegExp =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')

I18N = helpers.I18N
FORM = helpers.XmlConstructor.tagger("form", False)
SPAN = helpers.XmlConstructor.tagger("span", False)
DIV = helpers.XmlConstructor.tagger("div", False)
I = helpers.XmlConstructor.tagger("i", False)
INPUT = helpers.XmlConstructor.tagger("input", True)
LABEL = helpers.XmlConstructor.tagger("label", False)
TEXTAREA = helpers.XmlConstructor.tagger("textarea", False)
SELECT = helpers.XmlConstructor.tagger("select", False)
OPTION = helpers.XmlConstructor.tagger("option", False)
XSECTION = helpers.XSECTION

__pragma__('kwargs')


class SignForm():
    def __init__(self, target_selector, **parameters):
        self.target_selector = target_selector
        self.element_target = jQuery(target_selector)
        self.table_name = self.element_target.attr("phanterpwa-form")
        self.has_captcha = None
        self.after_sign = None
        self.preload = preloaders.android
        self.element_csrf_token = jQuery(self.element_target).find(
            "#phanterpwa-widget-input-{0}-csrf_token".format(self.table_name)
        )
        if self.element_csrf_token.length == 0:
            self.element_target.prepend(CSRFInput(self.table_name).jquery())
            self.element_csrf_token = jQuery(self.element_target).find(
                "#phanterpwa-widget-input-{0}-csrf_token".format(self.table_name)
            )
        self.element_captcha_container = jQuery(self.element_target).find(
            "#phanterpwa-widget-{0}-captcha-container".format(self.table_name)
        )
        if "has_captcha" in parameters:
            self.has_captcha = parameters["has_captcha"]
        if "after_sign" in parameters:
            self.after_sign = parameters["after_sign"]
        if "preload" in parameters:
            self.preload = parameters["preload"]
        if self.has_captcha is True:
            self.signCaptchaForm()
        else:
            self.signForm()

    def after_try_sign(self, data, ajax_status):
        if ajax_status == "success":
            csrf = data.responseJSON.csrf
            self.element_csrf_token.val(csrf).trigger("keyup")
        if self.after_sign is not None and self.after_sign is not js_undefined:
            self.after_sign(data, ajax_status)

    def signForm(self):
        self.element_csrf_token.val("").trigger("keyup")

        window.PhanterPWA.ApiServer.GET(
            **{
                "url_args": ["api", "signforms", "phanterpwa-form-{0}".format(self.table_name)],
                "onComplete": self.after_try_sign
            }
        )

    def on_captcha_fail(self):
        self.element_captcha_container.html(DIV(
            DIV(
                I18N("Conection Fail!").jquery().attr("pt-BR", "Conexão Falhou!"),
                _id="captcha_reload_conection_fail_messagem"
            ),
            DIV(
                DIV(I(_class="fas fa-redo-alt"), _id="captcha_reload_conection_icon"),
                DIV(
                    I18N("Try again!").jquery().attr("pt-BR", "Tente Novamente"),
                    _id="captcha_reload_conection_try_again_messagem"
                ),
                _class="captcha_reload_conection_button link"
            ),
            _class="captcha_reload_conection_container"
        ).jquery())
        self.element_captcha_container.find(".captcha_reload_conection_button").off(
            "click.captcha_reload_conection_button_{0}".format(self.table_name)
        ).on(
            "click.captcha_reload_conection_button_{0}".format(self.table_name),
            lambda: (
                self.element_captcha_container.html(self.preload),
                self.signCaptchaForm()
            )
        )

    def after_get_captcha_html(self, data, ajax_status):
        if ajax_status == "success":
            if data.responseJSON.status == "OK":
                signature = data.responseJSON.signature
                html = data.responseJSON.captcha
                self.add_html_Captcha(html, signature)
        else:
            if data.status == 0:
                self.on_captcha_fail()

    def add_html_Captcha(self, html, signature):
        self.element_captcha_container.html(html)
        self.element_captcha_container.find(
            ".captcha-option"
        ).off(
            "click.captcha-option-{0}".format(self.table_name)
        ).on(
            "click.captcha-option-{0}".format(self.table_name),
            lambda: self.on_click_captcha_option(this, signature)
        )

    def after_post_captcha_option(self, data, ajax_status):
        if ajax_status == "success":
            html = data.responseJSON.captcha
            csrf = data.responseJSON.csrf
            self.element_csrf_token.val(csrf).trigger("keyup")
            self.element_captcha_container.html(html)
        else:
            if data.status == 0:
                self.on_captcha_fail()
            else:
                signature = data.responseJSON.signature
                html = data.responseJSON.captcha
                if signature is not js_undefined and html is not js_undefined:
                    self.add_html_Captcha(html, signature)
                else:
                    self.signCaptchaForm()
            self.element_csrf_token.val("").trigger("keyup")

    def on_click_captcha_option(self, el, signature):
        user_choice = jQuery(el).attr("token_option")
        signature = signature
        id_form = jQuery(el).attr("id_captcha")
        __pragma__('jsiter')
        captcha_vars = {
            'user_choice': user_choice,
            'signature': signature,
            'id_form': id_form,
        }
        __pragma__('nojsiter')

        self.element_captcha_container.html(self.preload)

        window.PhanterPWA.ApiServer.POST(
            **{
                "url_args": ["api", "signcaptchaforms", id_form],
                "form_data": captcha_vars,
                "onComplete": self.after_post_captcha_option
            }
        )

    def signCaptchaForm(self):
        self.element_target = jQuery(self.target_selector)
        if self.element_target.length == 0:
            console.error("The {0} not exist".format(self.target_selector))
        else:
            self.element_csrf_token = jQuery(self.element_target).find(
                "#phanterpwa-widget-input-{0}-csrf_token".format(self.table_name)
            )
            self.element_csrf_token.val("").trigger("keyup")

            window.PhanterPWA.ApiServer.GET(
                **{
                    "url_args": ["api", "signcaptchaforms", "phanterpwa-form-{0}".format(
                        self.table_name)
                    ],
                    "onComplete": self.after_get_captcha_html
                }
            )


class SignLockForm():
    def __init__(self):
        self.element_target = jQuery("[phanterpwa-form='lock']")
        self.element_csrf_token = jQuery("[phanterpwa-form='lock'] #phanterpwa-widget-input-lock-csrf_token")
        if self.element_csrf_token.length == 0:
            self.element_target.prepend(CSRFInput("lock").jquery())
            self.element_csrf_token = jQuery("[phanterpwa-form='lock'] #phanterpwa-widget-input-lock-csrf_token")
        self.element_csrf_token.val("").trigger("keyup")
        window.PhanterPWA.ApiServer.GET(
            **{
                "url_args": ["api", "signlockform"],
                "onComplete": self.after_sign
            }
        )

    def after_sign(self, data, ajax_status):
        if ajax_status == "success":
            csrf = data.responseJSON.csrf
            self.element_csrf_token.val(csrf).trigger("keyup")
        else:
            window.PhanterPWA.logout()


class CaptchaContainer(helpers.XmlConstructor):
    def __init__(self, table_name, *content, **attributes):
        self.table_name = table_name
        attributes["_id"] = "phanterpwa-widget-{0}-captcha-container".format(
            self.table_name
        )
        if "_class" in attributes:
            attributes["_class"] = "{0}{1}".format(
                attributes["_class"].strip(),
                " phanterpwa-widget-captcha-container"
            )
        else:
            attributes["_class"] = "phanterpwa-widget-captcha-container"
        helpers.XmlConstructor.__init__(self, "div", False, *content, **attributes)


class FormButton(helpers.XmlConstructor):
    def __init__(self, name, label, **attributes):
        self.label = label
        initial_class = "phanterpwa-widget-form-form_button-container"
        if ["_id"] not in attributes:
            attributes["_id"] = "phanterpwa-widget-form-form_button-{0}".format(name)
        self.button_attributes = attributes
        if "_class" in self.button_attributes:
            self.button_attributes["_class"] = " ".join([
                self.button_attributes['_class'].strip(),
                "btn phanterpwa-widget-form-form_button link"])
        else:
            self.button_attributes["_class"] = "btn phanterpwa-widget-form-form_button link"
        if "_title" not in self.button_attributes:
            if isinstance(self.label, str):
                self.button_attributes["_title"] = self.label
        helpers.XmlConstructor.__init__(self, 'div', False, _class=initial_class)
        self._update_content()

    def _update_content(self):
        attributes = self.button_attributes
        self.content = [
            DIV(
                DIV(self.label, **attributes),
                _class="button-form")
        ]


class SubmitButton(FormButton):
    def __init__(self, form, label, **attributes):
        attributes["_phanterpwa_widget_submit_button"] = form
        if ["_id"] not in attributes:
            attributes["_id"] = "phanterpwa-widget-form-submit_button-{0}".format(form)
        FormButton.__init__(self, None, label, **attributes)


class CSRFInput(helpers.XmlConstructor):
    def __init__(self, table_name, **attributes):
        self.table_name = table_name
        if ["_id"] not in attributes:
            attributes["_id"] = "phanterpwa-widget-container-{0}-csrf_token".format(self.table_name)
        self.button_attributes = attributes
        if "_class" in self.button_attributes:
            self.button_attributes["_class"] = " ".join([
                self.button_attributes['_class'].strip(),
                "phanterpwa-widget phanterpwa-widget-hidden e-display_hidden"])
        else:
            self.button_attributes["_class"] = "phanterpwa-widget phanterpwa-widget-hidden e-display_hidden"

        helpers.XmlConstructor.__init__(
            self,
            'div',
            False,
            DIV(
                I(
                    _class="fas fa-check"
                ),
                _id="phanterpwa-widget-check-{0}-csrf_token".format(self.table_name),
                _class="phanterpwa-widget-check"
            ),
            DIV(
                INPUT(
                    _id="phanterpwa-widget-input-{0}-csrf_token".format(self.table_name),
                    _name="csrf_token",
                    _phanterpwa_widget_validator=JSON.stringify(['IS_NOT_EMPTY']),
                    _phanterpwa_widget_table_name=self.table_name,
                    _type="hidden"
                ),
                LABEL(
                    "CSRF Token",
                    _for="phanterpwa-widget-input-{0}-csrf_token".format(self.table_name),
                ),
                _class='input-field'
            ),
            DIV(_class="phanterpwa-widget-error"),
            **attributes
        )


class FormWidget(helpers.XmlConstructor):
    def __init__(self, table_name, input_name, **json_widget):
        self.table_name = table_name
        self.input_name = input_name
        self.json_widget = json_widget
        self.placeholder = None
        self.icon_button = None
        self.validators = json_widget.get("validators", None)
        self._value = json_widget.get("value", None)
        self._editable = json_widget.get("editable", False)
        self._can_empty = json_widget.get("can_empty", False)
        self._mask = json_widget.get("mask", None)
        self.fmt = json_widget.get("format", None)
        self._cutter = json_widget.get("cutter", False)
        self._url = json_widget.get("url", None)
        self._nocache = json_widget.get("no-cache", False)
        if "_id" not in json_widget:
            json_widget["_id"] = "phanterpwa-widget-wrapper-{0}-{1}".format(self.table_name, self.input_name)
        if "type" not in json_widget:
            json_widget["type"] = "string"
        self._widget_type = json_widget["type"]
        if "_class" in json_widget:
            json_widget["_class"] = "{0}{1}".format(
                json_widget["_class"].strip(),
                " phanterpwa-widget-wrapper"
            )
        else:
            json_widget["_class"] = "phanterpwa-widget-wrapper-{0}".format(json_widget["type"])
        if 'phanterpwa' in self.json_widget:
            obj_pwa = dict(self.json_widget['phanterpwa'])
            for a in obj_pwa.keys():
                if a.startswith("_"):
                    self.extra_attr[a] = self.json_widget['phanterpwa'][a]
            if 'icon_button' in self.json_widget['phanterpwa']:
                self.icon_button = DIV(
                    I(_class=self.json_widget['phanterpwa']['icon_button']),
                    _id='phanterpwa-widget-icon_button-{0}-{1}'.format(self.table_name, self.input_name),
                    _class='phanterpwa-widget-icon_button link btn',
                    _table_name=self.table_name,
                    _input_name=self.input_name
                )
            if self.validators is not None:
                self.validators = JSON.stringify(self.validators)
            if 'mask' in self.json_widget['phanterpwa']:
                self._mask = self.json_widget['phanterpwa']['mask']
            if 'format' in self.json_widget['phanterpwa']:
                self.fmt = self.json_widget['phanterpwa']['format']
            if 'placeholder' in self.json_widget['phanterpwa']:
                self.placeholder = self.json_widget['phanterpwa']['placeholder']
            if 'type' in self.json_widget['phanterpwa']:
                self._widget_type = self.json_widget['phanterpwa']['type']
        helpers.XmlConstructor.__init__(self, 'div', False, **json_widget)
        self._process()

    def _process(self):
        if self._widget_type == "date" or self._widget_type == "datetime":
            dformat = "yyyy-MM-dd"
            dvalue = self.json_widget['value']
            if self._widget_type == "datetime":
                dformat = "{0} HH:mm:ss".format(dformat)
            if self.fmt is not None and self.fmt is not js_undefined:
                dformat = self.fmt
                if isinstance(dvalue, str):
                    dvalue = validations.format_iso_date_datetime(dvalue, dformat, self._widget_type)

            w = widgets.Input(
                "{0}-{1}".format(self.table_name, self.input_name),
                label=self.json_widget['label'],
                name=self.input_name,
                value=dvalue,
                format=dformat,
                kind=self._widget_type,
                mask=dformat,
                form=self.table_name,
                icon=I(_class="fas fa-calendar-alt"),
                validators=self.validators
            )

        elif self._widget_type == "reference" or self._widget_type == "select":
            w = widgets.Select(
                "{0}-{1}".format(self.table_name, self.input_name),
                label=self.json_widget['label'],
                name=self.input_name,
                editable=self._editable,
                can_empty=self._can_empty,
                value=self._value,
                data_set=self.json_widget['data_set'],
                form=self.table_name,
                validators=self.validators
            )
        elif self._widget_type == "list_string":
            w = widgets.ListString(
                "{0}-{1}".format(self.table_name, self.input_name),
                label=self.json_widget['label'],
                name=self.input_name,
                #editable=self._editable,
                #can_empty=self._can_empty,
                value=self._value,
                #mask=self._mask,
                form=self.table_name,
                #validators=self.validators
            )
        elif self._widget_type == "text":
            w = widgets.Textarea(
                "{0}-{1}".format(self.table_name, self.input_name),
                label=self.json_widget['label'],
                name=self.input_name,
                editable=self._editable,
                can_empty=self._can_empty,
                value=self._value,
                mask=self._mask,
                form=self.table_name,
                validators=self.validators
            )

        elif self._widget_type == "id":
            w = widgets.Inert(
                "{0}-{1}".format(self.table_name, self.input_name),
                label=self.json_widget['label'],
                name=self.input_name,
                value=self._value,
                form=self.table_name,
            )

        elif self._widget_type == "boolean":
            w = widgets.CheckBox(
                "{0}-{1}".format(self.table_name, self.input_name),
                label=self.json_widget['label'],
                name=self.input_name,
                value=self._value is True,
                form=self.table_name
            )

        elif self._widget_type == "password":
            w = widgets.Input(
                "{0}-{1}".format(self.table_name, self.input_name),
                label=self.json_widget['label'],
                name=self.input_name,
                value=self._value,
                form=self.table_name,
                validators=self.validators,
                kind="password"
            )

        elif self._widget_type == "hidden":
            w = widgets.Input(
                "{0}-{1}".format(self.table_name, self.input_name),
                label=self.json_widget['label'],
                name=self.input_name,
                value=self._value,
                editable=self._editable,
                can_empty=self._can_empty,                
                mask=self._mask,
                form=self.table_name,
                kind="hidden",
                validators=self.validators
            )

        elif self._widget_type == "image":

            w = widgets.Image(
                "{0}-{1}".format(self.table_name, self.input_name),
                label=self.json_widget['label'],
                name=self.input_name,
                value=self._url,
                form=self.table_name,
                cutter=self._cutter,
                nocache=self._nocache
            )

        else:
            w = widgets.Input(
                "{0}-{1}".format(self.table_name, self.input_name),
                label=self.json_widget['label'],
                name=self.input_name,
                value=self._value,
                editable=self._editable,
                can_empty=self._can_empty,                
                mask=self._mask,
                form=self.table_name,
                validators=self.validators
            )
        self.append(w)


class Form(helpers.XmlConstructor):
    def __init__(self, json_form, **parameters):
        fields = None
        submit_button = None
        self.show_id = False
        self.has_captcha = None
        self.preload = preloaders.android
        self.after_sign = None
        self.element = None
        self.table_name = json_form.table
        if "fields" in parameters:
            fields = parameters["fields"]
        if "show_id" in parameters:
            self.show_id = parameters["show_id"]
        if "submit_button" in parameters:
            submit_button = parameters["submit_button"]
        if "has_captcha" in parameters:
            self.has_captcha = parameters["has_captcha"]
        if "preload" in parameters:
            self.preload = parameters["preload"]
        if "after_sign" in parameters:
            self.after_sign = parameters
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(
                parameters["_class"].strip(),
                " phanterpwa-form"
            )
        else:
            parameters["_class"] = "phanterpwa-form"
        if "_id" not in parameters:
            parameters["_id"] = "form-{0}".format(self.table_name)
        parameters["_phanterpwa-form"] = self.table_name
        self.json_widgets = json_form["widgets"]
        self.widgets = dict()
        self.fields = fields

        self.table_name = json_form["table"]
        helpers.XmlConstructor.__init__(
            self,
            'phanterpwa-form',
            False,
            CSRFInput(self.table_name),
            **parameters
        )
        self._captcha_container = CaptchaContainer(
            self.table_name,
            self.preload
        )
        if submit_button is not None and submit_button is not js_undefined:
            self._buttons_container = DIV(
                submit_button,
                _class='buttons-form-container'
            )
        else:
            self._buttons_container = DIV(
                SubmitButton(
                    self.table_name,
                    I18N("Submit")
                ),
                _class='buttons-form-container'
            )
        self._process()

    def extra_button(self, _id, label, **attributes):
        self._buttons_container.append(
            FormButton(
                _id,
                label,
                **attributes
            )
        )
        self.widget = dict()
        self.content = list()
        self._process()

    def _process_widget(self, wjson):
        if wjson[0] == "widget":
            return FormWidget(self.table_name, wjson[1][0], **dict(wjson[1][1]))
        elif wjson[0] == "section":
            content = [LABEL(wjson[1][0])]
            for x in wjson[1][1]:
                content.append(self._process_widget(x))
            return XSECTION(*content)
        elif wjson[0] == "group":
            content = []
            for x in wjson[1][1]:
                content.append(self._process_widget(x))
            return DIV(*content, _id=wjson[1][0], _class="phanterpwa-widget-form-group")

    def _process(self):
        for x in self.json_widgets:
            w = self._process_widget(x)
            self.widgets[x] = w
            if self.fields is not None and self.fields is not js_undefined:
                if x in self.fields:
                    self.append(w)
            else:
                if x == "id":
                    if self.show_id:
                        self.append(w)
                else:
                    self.append(w)

        if self.has_captcha is True:
            self.append(self._captcha_container)
        self.append(self._buttons_container)

    def signForm(self):
        self.Signer = SignForm(self.table_name, **{
            'preload': self.preload,
            'has_captcha': self.has_captcha,
            'after_sign': self.after_sign
        })

    def target(self, element):
        self.element = element
        el = self.jquery()
        self.element.html(el)
        jQuery(self.element).find('select').formSelect()
        jQuery(self.element).phanterpwaFormValidator()
        self.signForm()
        return self.element

    def custom(self, element, *content):
        self.content = content
        if self.has_captcha is True:
            self.append(self._captcha_container)
        self.append(self._buttons_container)
        el = self.jquery()
        self.element.html(el)
        jQuery(el).find('select').formSelect()
        jQuery(el).phanterpwaFormValidator()
        self.signForm()
        return self.element

    @staticmethod
    def process_api_response(data):
        if data.status == 400:
            if data.responseJSON.message is not js_undefined:
                window.PhanterPWA.flash(html=data.responseJSON.message)
            if data.responseJSON.errors is not js_undefined:
                errors = dict(data.responseJSON.errors)
                for x in errors.keys():
                    target = jQuery("#phanterpwa-widget-socios-{0}".format(x))
                    target.find(".phanterpwa-widget-message_error").text(data.responseJSON.errors[x])
                    target.find(".phanterpwa-widget-wrapper").addClass("has_error")
        elif data.status == 200:
            if data.responseJSON.message is not js_undefined:
                window.PhanterPWA.flash(html=data.responseJSON.message)


class ValidateForm():

    def __init__(self, target_selector, **parameters):
        self.target_selector = target_selector
        self.element_target = jQuery(target_selector)
        self.table_name = self.element_target.attr("phanterpwa-form")
        self.submit_button = self.element_target.find(
            "#phanterpwa-widget-form-submit_button-{0}".format(self.table_name))
        if self.submit_button.length == 0:
            self.submit_button = None
        else:
            self.submit_button.attr("disabled", "disabled")
        if "submit_button" in parameters:
            self.submit_button = jQuery(parameters["submit_button"])
            if self.submit_button.length == 0:
                self.submit_button = None
            else:
                self.submit_button.attr("disabled", "disabled")
        self.formtests = list()
        self.formpass = False
        self.reload()

    def _init_validate(self, el):
        validate_test_pass = list()
        validate_test = list(jQuery(el).data("validators"))
        input_name = jQuery(el).attr("name")
        table_name = jQuery(el).data("form")
        value_for_validate = self.element_target.find("input[name='{0}']".format(input_name)).val()
        is_empty_or = False
        if "IS_EMPTY_OR" in validate_test:
            if (value_for_validate is js_undefined) or \
                (value_for_validate is None) or (value_for_validate == ""):
                validate_test_pass.append(True)
                validate_test.pop("IS_EMPTY_OR")
            else:
                if x is not None and x is not js_undefined:
                    validate_test_pass.append(self._validates(x, value_for_validate, el))  
        else:
            for x in validate_test:
                if x is not None and x is not js_undefined:
                    validate_test_pass.append(self._validates(x, value_for_validate, el))
        if all(validate_test_pass):
            self.formtests.append(True)
            jQuery("#phanterpwa-widget-{0}-{1}".format(
                table_name, input_name)).find(".phanterpwa-widget-wrapper").removeClass("no_pass")
        else:
            jQuery("#phanterpwa-widget-{0}-{1}".format(
                table_name, input_name)).find(".phanterpwa-widget-wrapper").addClass("no_pass").removeClass("has_error")
            self.formtests.append(False)
        if all(self.formtests):
            self.formpass = True

            if self.submit_button is not None and self.submit_button is not js_undefined:
                if self.formpass:
                    self.submit_button.removeAttr("disabled")
                else:
                    self.submit_button.attr("disabled", "disabled")
        else:
            if self.submit_button is not None and self.submit_button is not js_undefined:
                self.submit_button.attr("disabled", "disabled")

    def _validates(self, validate_name, value_for_validate, el):
        validate_test_pass = list()
        if validate_name == "PROGRAMMATICALLY":
            if jQuery(el)[0].hasAttribute("phanterpwa-validate-programmatically"):
                validate_test_pass.append(True)
            else:
                validate_test_pass.append(False)
        if validate_name.startswith("IS_IN_SET:"):
            res = False
            list_options = JSON.parse(validate_name[10:])
            if list_options is not None or list_options is not js_undefined:
                list_options = JSON.parse(list_options)
                if list_options.indexOf(value_for_validate) > -1:
                    res = True
            validate_test_pass.append(res)

        if validate_name == "IS_NOT_EMPTY":
            if (value_for_validate is js_undefined) or \
                (value_for_validate is None) or (value_for_validate == ""):
                validate_test_pass.append(False)
            else:
                validate_test_pass.append(True)
        if validate_name == "IS_ACTIVATION_CODE":
            is_activation_code = False
            res = validations.check_activation_code(value_for_validate)
            if res is not None:
                is_activation_code = True
            validate_test_pass.append(is_activation_code)
        if validate_name.startswith("IS_DATE"):
            if validate_name.startswith("IS_DATE:"):
                dformat = validate_name[8:]
                res = validations.check_datetime(value_for_validate, dformat, "date")
                validate_test_pass.append(res)
            elif validate_name.startswith("IS_DATETIME:"):
                dformat = validate_name[12:]
                res = validations.check_datetime(value_for_validate, dformat, "datetime")
                validate_test_pass.append(res)
            elif validate_name == "IS_DATETIME":
                dformat = validate_name[12:]
                res = validations.check_datetime(value_for_validate)
                validate_test_pass.append(res)
            else:
                dformat = validate_name[12:]
                res = validations.check_datetime(value_for_validate, "yyyy-MM-dd", "date")
                validate_test_pass.append(res)
        if validate_name.startswith("IS_EQUALS") and ":" in validate_name:
            comp = jQuery(validate_name[10:]).val()
            if comp is value_for_validate:
                validate_test_pass.append(True)
            else:
                validate_test_pass.append(False)
        if validate_name.startswith("MATCH:"):
            regex = __new__(RegExp(validate_name[6:]))

            if value_for_validate.match(regex) is not None:
                validate_test_pass.append(True)
            else:
                validate_test_pass.append(False)
        if validate_name == "IS_EMAIL":
            if "@" in value_for_validate:
                REGEX_BODY = __pragma__(
                    'js',
                    '{}',
                    r'/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([_a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/'
                )
                if REGEX_BODY.test(value_for_validate):
                    validate_test_pass.append(True)
                else:
                    validate_test_pass.append(False)
            else:
                validate_test_pass.append(False)
        if all(validate_test_pass):
            return True
        else:
            return False

    def _on_input_change(self):
        self.formtests = list()
        inputs_for_validate = self.element_target.find(
            "[data-validators]"
        )
        inputs_for_validate.each(lambda: self._init_validate(this))

    def reload(self):
        self.start()
        return self.element_target

    def start(self):
        self.element_target = jQuery(self.target_selector)
        if self.element_target.length == 0:
            console.error("The {0} not exist".format(self.target_selector))

        self.element_target.off(
            'change.phanterpwaformvalidator, keyup.phanterpwaformvalidator',
        ).on(
            'change.phanterpwaformvalidator, keyup.phanterpwaformvalidator',
            lambda: self._on_input_change()
        )
        self._on_input_change()
        return self.element_target


__pragma__('nokwargs')
