from phanterpwa.transcrypt import (
    helpers,
    preloaders,
    validations,
    i18n
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

__pragma__('kwargs')


class SignForm():
    def __init__(self, table_name, **parameters):
        self.has_captcha = None
        self.after_sign = None
        self.element_form = jQuery("[phanterpwa-jsonform='{0}']".format(table_name))
        self.table_name = table_name
        self.preload = preloaders.android
        self.element_csrf_token = jQuery(self.element_form).find(
            "#phanterpwa-widget-input-{0}-csrf_token".format(self.table_name)
        )
        if self.element_csrf_token.length == 0:
            self.element_form.prepend(CSRFInput(self.table_name).jquery())
            self.element_csrf_token = jQuery(self.element_form).find(
                "#phanterpwa-widget-input-{0}-csrf_token".format(self.table_name)
            )
        self.element_captcha_container = jQuery(self.element_form).find(
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
                "url_args": ["api", "signforms", "phanterpwa-jsonform-{0}".format(self.table_name)],
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
        self.element_csrf_token = jQuery(self.element_form).find(
            "#phanterpwa-widget-input-{0}-csrf_token".format(self.table_name)
        )
        self.element_csrf_token.val("").trigger("keyup")

        window.PhanterPWA.ApiServer.GET(
            **{
                "url_args": ["api", "signcaptchaforms", "phanterpwa-jsonform-{0}".format(
                    self.table_name)
                ],
                "onComplete": self.after_get_captcha_html
            }
        )


class SignLockForm():
    def __init__(self):
        self.element_form = jQuery("[phanterpwa-jsonform='lock']")
        self.element_csrf_token = jQuery("[phanterpwa-jsonform='lock'] #phanterpwa-widget-input-lock-csrf_token")
        if self.element_csrf_token.length == 0:
            self.element_form.prepend(CSRFInput("lock").jquery())
            self.element_csrf_token = jQuery("[phanterpwa-jsonform='lock'] #phanterpwa-widget-input-lock-csrf_token")
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
        initial_class = "phanterpwa-materialize-button-form-container"
        if ["_id"] not in attributes:
            attributes["_id"] = "phanterpwa-widget-form_button-{0}".format(name)
        self.button_attributes = attributes
        if "_class" in self.button_attributes:
            self.button_attributes["_class"] = " ".join([
                self.button_attributes['_class'].strip(),
                "btn phanterpwa-materialize-button-form link"])
        else:
            self.button_attributes["_class"] = "btn phanterpwa-materialize-button-form link"
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
    def __init__(self, table_name, label, **attributes):
        attributes["_phanterpwa_widget_submit_button"] = table_name
        if ["_id"] not in attributes:
            attributes["_id"] = "phanterpwa-widget-submit_button-{0}".format(table_name)
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
                "phanterpwa-widget phanterpwa-widget-hidden easy_forced_hidden"])
        else:
            self.button_attributes["_class"] = "phanterpwa-widget phanterpwa-widget-hidden easy_forced_hidden"

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


class Widget(helpers.XmlConstructor):
    def __init__(self, table_name, input_name, **json_widget):
        self.table_name = table_name
        # console.error(self.table_name, " - ", input_name,":", json_widget)
        self.input_name = input_name
        self.json_widget = json_widget
        self.placeholder = None
        self.icon_button = None
        self.validators = None
        self.mask = None
        self.fmt = None
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
            # console.log(self.json_widget['phanterpwa'])
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
            if 'validators' in self.json_widget['phanterpwa']:
                self.validators = JSON.stringify(self.json_widget['phanterpwa']['validators'])
            if 'mask' in self.json_widget['phanterpwa']:
                self.mask = self.json_widget['phanterpwa']['mask']
            if 'format' in self.json_widget['phanterpwa']:
                self.fmt = self.json_widget['phanterpwa']['format']
            if 'placeholder' in self.json_widget['phanterpwa']:
                self.placeholder = self.json_widget['phanterpwa']['placeholder']
            if 'type' in  self.json_widget['phanterpwa']:
                 self._widget_type = self.json_widget['phanterpwa']['type']

        helpers.XmlConstructor.__init__(self, 'div', False, **json_widget)
        self._process()

    def _process(self):
        if self._widget_type == "date" or self._widget_type == "datetime":
            dformat = "yyyy-MM-dd"
            dtype = self._widget_type
            dvalue = self.json_widget['default']
            if dtype == "datetime":
                dformat = "{0} HH:mm:ss".format(dformat)
            if self.fmt is not None and self.fmt is not js_undefined:
                dformat = self.fmt
                dvalue = validations.format_iso_date_datetime(dvalue, dformat, dtype)

            extra_class = " phanterpwa-widget-has_icon_button"
            icon_button = DIV(
                I(_class="fas fa-calendar-alt"),
                _id='phanterpwa-widget-icon_button-{0}-{1}'.format(self.table_name, self.input_name),
                _class='phanterpwa-widget-icon_button link btn'
            ).jquery()
            mask = self._widget_type
            if self.icon_button is not None and self.icon_button is not js_undefined:
                icon_button = self.icon_button.jquery()

            if self.mask is not None and self.mask is not js_undefined:
                mask = self.mask

            inp = INPUT(
                _id="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                _name=self.input_name,
                _value=dvalue,
                _phanterpwa_widget_validator=self.validators,
                _phanterpwa_widget_mask=mask,
                _phanterpwa_widget_table_name=self.table_name,
                _type="text"
            ).jquery()
            w = DIV(
                icon_button,
                DIV(
                    I(
                        _class="fas fa-check"
                    ),
                    _id="phanterpwa-widget-check-{0}-{1}".format(self.table_name, self.input_name),
                    _class="phanterpwa-widget-check"
                ),
                DIV(
                    inp,
                    LABEL(
                        self.json_widget['label'],
                        _for="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                    ),
                    _class='input-field'
                ),
                DIV(_class="phanterpwa-widget-error"),
                _id='phanterpwa-widget-{0}-{1}'.format(self.table_name, self.input_name),
                _class='phanterpwa-widget phanterpwa-widget-{0}{1}'.format(self._widget_type, extra_class)
            ).jquery()

            def onChoice(data):
                formated = data['formated']
                inp.val(formated).trigger("keyup")
                M.updateTextFields()

            def onClickButtonCalendar():
                input_value = jQuery(inp).val()
                checked_date = validations.check_datetime(input_value, dformat, dtype)
                if checked_date:
                    jQuery(
                        w
                    ).phanterpwaDateTimePicker(
                        {
                            "current_date": input_value,
                            "date_type": dtype,
                            "format": dformat,
                            "onChoice": lambda data: onChoice(data)
                        }
                    )
                else:
                    jQuery(
                        w
                    ).phanterpwaDateTimePicker(
                        {
                            "date_type": dtype,
                            "format": dformat,
                            "onChoice": lambda data: onChoice(data)
                        }
                    )
            icon_button.off(
                'click.icon_button-{0}-{1}'.format(self.table_name, self.input_name)
            ).on(
                'click.icon_button-{0}-{1}'.format(self.table_name, self.input_name),
                onClickButtonCalendar
            )

        elif self._widget_type == "reference":
            extra_class = ""
            icon_button = ""
            mask = None
            if self.mask is not None and self.mask is not js_undefined:
                mask = self.mask
            if self.icon_button is not None and self.icon_button is not js_undefined:
                extra_class = " phanterpwa-widget-has_icon_button"
                icon_button = self.icon_button
            if self.json_widget['default'] is None or\
                    self.json_widget['default'] is js_undefined or self.json_widget['default'] == "":
                extra_class = "{0}{1}".format(extra_class, " input_is_empty")
            inp = INPUT(
                _id="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                _name=self.input_name,
                _value=self.json_widget['default'],
                _phanterpwa_widget_validator=self.validators,
                _phanterpwa_widget_mask=mask,
                _phanterpwa_widget_table_name=self.table_name,
                _type="hidden",
                _placeholder=self.placeholder
            ).jquery()
            dft = self.json_widget['default']
            vselect = SELECT(
            )
            has_default = False
            s_elements = self.json_widget['data']
            if "formatted" in self.json_widget:
                s_elements = self.json_widget['formatted']
            if s_elements is not None:
                for x in s_elements:
                    if dft == x[0]:
                        has_default = True
                        vselect.append(
                            OPTION(x[1], _value=x[0], _selected="selected")
                        )
                    else:
                        vselect.append(
                            OPTION(x[1], _value=x[0])
                        )
            disabled = None
            if self.validators is not None and self.validators is not js_undefined:
                ppwa_fv = self.validators
                if "IS_NOT_EMPTY" in ppwa_fv:
                    disabled = "disabled"
            if has_default:
                jQuery(inp).val(dft)
                vselect.insert(
                    0,
                    OPTION(self.placeholder, _value="", _disabled=disabled)
                )
            else:
                vselect.insert(
                    0,
                    OPTION(self.placeholder, _value="", _selected="selected", _disabled=disabled)
                )
            vselect = vselect.jquery()
            w = DIV(
                icon_button,
                DIV(
                    I(
                        _class="fas fa-check"
                    ),
                    _id="phanterpwa-widget-check-{0}-{1}".format(self.table_name, self.input_name),
                    _class="phanterpwa-widget-check"
                ),
                DIV(
                    inp,
                    vselect,
                    LABEL(
                        self.json_widget['label']
                    ),
                    _class='input-field'
                ),
                DIV(_class="phanterpwa-widget-error"),
                _id='phanterpwa-widget-{0}-{1}'.format(self.table_name, self.input_name),
                _class='phanterpwa-widget phanterpwa-widget-{0}{1}'.format(self._widget_type, extra_class)
            )

            def add_on_input(el):
                value = jQuery(el).val()
                if value is None or value is js_undefined or value == "":
                    jQuery(w.jquery()).addClass('input_is_empty')
                else:
                    jQuery(w.jquery()).removeClass('input_is_empty')
                jQuery(inp).val(value).trigger("change")
            jQuery(
                vselect,
            ).off(
                'change.change_{0}-{1}'.format(self.table_name, self.input_name),
            ).on(
                'change.change_{0}-{1}'.format(self.table_name, self.input_name),
                lambda: add_on_input(this)
            )

        elif self._widget_type == "text":
            extra_class = ""
            icon_button = ""
            mask = None
            if self.mask is not None and self.mask is not js_undefined:
                mask = self.mask
            if self.icon_button is not None and self.icon_button is not js_undefined:
                extra_class = " phanterpwa-widget-has_icon_button"
                icon_button = self.icon_button
            w = DIV(
                icon_button,
                DIV(
                    I(
                        _class="fas fa-check"
                    ),
                    _id="phanterpwa-widget-check-{0}-{1}".format(self.table_name, self.input_name),
                    _class="phanterpwa-widget-check"
                ),
                DIV(
                    TEXTAREA(
                        _id="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                        _name=self.input_name,
                        _class="materialize-textarea",
                        _value=self.json_widget['default'],
                        _phanterpwa_widget_validator=self.validators,
                        _phanterpwa_widget_table_name=self.table_name,
                        _phanterpwa_widget_mask=mask
                    ),
                    LABEL(
                        self.json_widget['label'],
                        _for="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                    ),
                    _class='input-field'
                ),
                DIV(_class="phanterpwa-widget-error"),
                _id='phanterpwa-widget-{0}-{1}'.format(self.table_name, self.input_name),
                _class='phanterpwa-widget phanterpwa-widget-{0}{1}'.format(self._widget_type, extra_class)
            )

        elif self._widget_type == "id":
            extra_class = ""
            icon_button = ""
            mask = None
            if self.mask is not None and self.mask is not js_undefined:
                mask = self.mask
            if self.icon_button is not None and self.icon_button is not js_undefined:
                extra_class = " phanterpwa-widget-has_icon_button"
                icon_button = self.icon_button
            w = DIV(

                DIV(
                    INPUT(
                        _id="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                        _name=self.input_name,
                        _value=self.json_widget['default'],
                        _phanterpwa_widget_validator=self.validators,
                        _phanterpwa_widget_mask=mask,
                        _phanterpwa_widget_table_name=self.table_name,
                        _type="text",
                        _disabled=True
                    ),
                    LABEL(
                        self.json_widget['label'],
                        _for="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                    ),
                    _class='input-field'
                ),
                DIV(_class="phanterpwa-widget-error"),
                _id='phanterpwa-widget-{0}-{1}'.format(self.table_name, self.input_name),
                _class='phanterpwa-widget phanterpwa-widget-{0}{1}'.format(self._widget_type, extra_class)
            )

        elif self._widget_type == "boolean":
            extra_class = ""
            w = DIV(
                DIV(
                    LABEL(
                        INPUT(
                            _id="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                            _name=self.input_name,
                            _type="checkbox",
                            _phanterpwa_widget_table_name=self.table_name,
                        ),
                        SPAN(self.json_widget['label']),
                        _for="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                    ),
                    _class='phanterpwa-widget-{0}-wrapper'.format(self._widget_type)
                ),
                DIV(_class="phanterpwa-widget-error"),
                _id='phanterpwa-widget-{0}-{1}'.format(self.table_name, self.input_name),
                _class='phanterpwa-widget phanterpwa-widget-{0}{1}'.format(self._widget_type, extra_class)
            ).jquery()
            if self.json_widget["default"] is True:
                w.find("#phanterpwa-widget-input-{0}-{1}".format(
                    self.table_name, self.input_name)).prop('checked', True)

        elif self._widget_type == "password":
            extra_class = ""
            icon_button = ""
            mask = None
            if self.mask is not None and self.mask is not js_undefined:
                mask = self.mask
            if self.icon_button is not None and self.icon_button is not js_undefined:
                extra_class = " phanterpwa-widget-has_icon_button"
                icon_button = self.icon_button
            w = DIV(
                icon_button,
                DIV(
                    I(
                        _class="fas fa-check"
                    ),
                    _id="phanterpwa-widget-check-{0}-{1}".format(self.table_name, self.input_name),
                    _class="phanterpwa-widget-check"
                ),
                DIV(
                    INPUT(
                        _id="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                        _name=self.input_name,
                        _value=self.json_widget['default'],
                        _phanterpwa_widget_validator=self.validators,
                        _phanterpwa_widget_mask=mask,
                        _phanterpwa_widget_table_name=self.table_name,
                        _type="password"
                    ),
                    LABEL(
                        self.json_widget['label'],
                        _for="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                    ),
                    _class='input-field'
                ),
                DIV(_class="phanterpwa-widget-error"),
                _id='phanterpwa-widget-{0}-{1}'.format(self.table_name, self.input_name),
                _class='phanterpwa-widget phanterpwa-widget-{0}{1}'.format(self._widget_type, extra_class)
            )

        else:
            extra_class = ""
            icon_button = ""
            mask = None
            if self.mask is not None and self.mask is not js_undefined:
                mask = self.mask
            if self.icon_button is not None and self.icon_button is not js_undefined:
                extra_class = " phanterpwa-widget-has_icon_button"
                icon_button = self.icon_button
            w = DIV(
                icon_button,
                DIV(
                    I(
                        _class="fas fa-check"
                    ),
                    _id="phanterpwa-widget-check-{0}-{1}".format(self.table_name, self.input_name),
                    _class="phanterpwa-widget-check"
                ),
                DIV(
                    INPUT(
                        _id="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                        _name=self.input_name,
                        _value=self.json_widget['default'],
                        _phanterpwa_widget_validator=self.validators,
                        _phanterpwa_widget_mask=mask,
                        _phanterpwa_widget_table_name=self.table_name,
                        _type="text"
                    ),
                    LABEL(
                        self.json_widget['label'],
                        _for="phanterpwa-widget-input-{0}-{1}".format(self.table_name, self.input_name),
                    ),
                    _class='input-field'
                ),
                DIV(_class="phanterpwa-widget-error"),
                _id='phanterpwa-widget-{0}-{1}'.format(self.table_name, self.input_name),
                _class='phanterpwa-widget phanterpwa-widget-{0}{1}'.format(self._widget_type, extra_class)
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
                " phanterpwa-jsonform"
            )
        else:
            parameters["_class"] = "phanterpwa-jsonform"
        if "_id" not in parameters:
            parameters["_id"] = "phanterpwa-jsonform-{0}".format(self.table_name)
        parameters["_phanterpwa_jsonform"] = self.table_name
        self.json_widgets = dict(json_form["json_widgets"])
        self.widgets = dict()
        self.fields = fields

        self.table_name = json_form["table"]
        helpers.XmlConstructor.__init__(
            self,
            'form',
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

    def _process(self):
        for x in self.json_widgets.keys():
            w = Widget(self.table_name, x, self.json_widgets[x])
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
        M.updateTextFields()
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
        # console.log(el)
        self.element.html(el)
        M.updateTextFields()
        jQuery(el).find('select').formSelect()
        jQuery(el).phanterpwaFormValidator()
        self.signForm()
        return self.element


class ValidateForm():

    def __init__(self, table_name, **parameters):
        self.element_form = jQuery("[phanterpwa-jsonform='{0}']".format(table_name))
        self.table_name = table_name
        self.submit_button = self.element_form.find(
            "#phanterpwa-widget-submit_button-{0}".format(self.table_name))
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
        validate_test = list(JSON.parse(jQuery(el).attr("phanterpwa_widget_validator")))
        input_name = jQuery(el).attr("name")
        table_name = jQuery(el).attr("phanterpwa_widget_table_name")
        value_for_validate = self.element_form.find("input[name='" + input_name + "']").val()
        for x in validate_test:
            if x.startswith("IS_EMPTY_OR_"):
                if (value_for_validate is js_undefined) or \
                    (value_for_validate is None) or (value_for_validate == ""):
                    validate_test_pass.append(True)
                else:
                    validate_test_pass.append(self._validates(x[12:], value_for_validate, el))
            else:
                validate_test_pass.append(self._validates(x, value_for_validate, el))
        console.log(validate_test_pass)
        if all(validate_test_pass):
            self.formtests.append(True)
            jQuery("#phanterpwa-widget-check-{0}-{1}".format(table_name, input_name)).removeClass("no_pass")
        else:
            jQuery("#phanterpwa-widget-check-{0}-{1}".format(table_name, input_name)).addClass("no_pass")
            self.formtests.append(False)
        console.log(self.formtests)
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
        console.log("validade_element", el)
        console.log("validate_name", validate_name)
        console.log("value_for_validate", value_for_validate)
        validate_test_pass = list()
        if validate_name == "PROGRAMMATICALLY":
            if jQuery(el)[0].hasAttribute("phanterpwa-validate-programmatically"):
                validate_test_pass.append(True)
            else:
                validate_test_pass.append(False)
        if validate_name == "IS_IN_SET":
            res = False
            if jQuery(el)[0].hasAttribute("phanterpwa-validate-is_in_set"):
                list_options = jQuery(el).attr("phanterpwa-validate-is_in_set")
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
        inputs_for_validate = self.element_form.find(
            "[phanterpwa_widget_validator]"
        )
        inputs_for_validate.each(lambda: self._init_validate(this))

    def reload(self):
        self.element_form.off(
            'change.phanterpwaformvalidator, keyup.phanterpwaformvalidator',
        ).on(
            'change.phanterpwaformvalidator, keyup.phanterpwaformvalidator',
            lambda: self._on_input_change()
        )
        self._on_input_change()
        return self.element_form


__pragma__('nokwargs')
