
import phanterpwa.apptools.components.modal as modal
import phanterpwa.apptools.components.top_slide as top_slide
import phanterpwa.apptools.components.left_bar as left_bar
import phanterpwa.apptools.components.gallery as gallery
import phanterpwa.apptools.helpers as helpers
import phanterpwa.apptools.forms as forms
import phanterpwa.apptools.preloaders as preloaders
import phanterpwa.apptools.application as application
import phanterpwa.apptools.handler as handler
from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = M = js_undefined = window = setTimeout = document = console = this = \
    __new__ = FormData = console = localStorage = 0
__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")
FORM = helpers.XmlConstructor.tagger("form")
SPAN = helpers.XmlConstructor.tagger("span")
IMG = helpers.XmlConstructor.tagger("img", True)
I = helpers.XmlConstructor.tagger("I")
I18N = helpers.I18N
CONCATENATE = helpers.CONCATENATE

__pragma__('kwargs')


class AuthUser(application.Component):
    def __init__(self, target_selector, **parameters):
        self.target_selector = target_selector
        self.element_target = jQuery(self.target_selector)
        self.callback = None
        self.Modal = None
        self.AlertActivationAccount = AlertActivationAccount("#layout-top_slide-container")
        self.auth_user = None
        self.authorization = None
        if "callback" in parameters:
            self.callback = parameters["callback"]
        html = DIV(
            DIV(
                _class="link phanterpwa-component-auth_user-button-toggle"
            ),
            DIV(
                _class="phanterpwa-component-auth_user-button-toggle-options"),
            _id="phanterpwa-component-auth_user-container",
            _class="phanterpwa-component-auth_user-container"
        )

        application.Component.__init__(self, "auth_user", html)
        self.html_to(target_selector)

    def switch_menu(self):
        self.element_target = jQuery(self.target_selector)
        if self.element_target.find(".phanterpwa-component-auth_user-container").hasClass("enabled"):
            self.close_menu()
        else:
            self.open_menu()

    def bind_menu_button(self):
        self.element_target = jQuery(self.target_selector)
        self.element_target.find(".phanterpwa-component-auth_user-button-toggle").off(
            "click.components-auth_user-button"
        ).on(
            "click.components-auth_user-button",
            lambda: self.switch_menu()
        )

    def reload(self, **context):
        if "ajax" in context:
            if context["ajax"][1][0] == "client" or context["ajax"][1][0] == "auth":
                self.element_target = jQuery(self.target_selector)
                self.start()

    @staticmethod
    def _open_menu():
        jQuery("#phanterpwa-component-auth_user-container").addClass("enabled")

    def open_menu(self):
        self._open_menu()
        LeftBarAuthUserLogin._open_menu()
        LeftBarAuthUserNoLogin._open_menu()

    def _close_menu():
        jQuery("#phanterpwa-component-auth_user-container").removeClass("enabled")

    def close_menu(self):
        self._close_menu()
        LeftBarAuthUserLogin._close_menu()
        LeftBarAuthUserNoLogin._close_menu()

    def _close_on_click_out(self, event):
        self.element_target = jQuery(self.target_selector)
        if jQuery(event.target).closest(self.element_target).length == 0:
            if jQuery(event.target).closest(
                    jQuery(".phanterpwa-component-left_bar-menu_button-wrapper-auth_user")).length == 0:
                self.close_menu()

    def modal_login(self):
        self.close_menu()
        self.Modal = ModalLogin(
            "#modal-container"
        )
        self.Modal.open()
        forms.SignForm("#form-login", has_captcha=True)
        forms.ValidateForm("#form-login")

    def modal_register(self):
        self.close_menu()
        self.Modal = ModalRegister(
            "#modal-container"
        )
        self.Modal.open()
        forms.SignForm("#form-register", has_captcha=True)
        forms.ValidateForm("#form-register")

    def modal_request_password(self):
        self.close_menu()
        self.Modal = ModalRequestPassword(
            "#modal-container"
        )
        self.Modal.open()
        forms.SignForm("#form-request_password", has_captcha=True)
        forms.ValidateForm("#form-request_password")

    def modal_change_password(self, temporary_password=None):
        self.close_menu()
        self.Modal = ModalChangePassword(
            "#modal-container",
            temporary_password=temporary_password
        )
        self.Modal.open()
        forms.SignForm("#form-change_password")
        forms.ValidateForm("#form-change_password")

    def logout(self):
        sessionStorage.removeItem("phanterpwa-authorization")
        sessionStorage.removeItem("auth_user")
        localStorage.removeItem("phanterpwa-authorization")
        localStorage.removeItem("auth_user")
        window.PhanterPWA.open_default_way()
        LeftBar = window.PhanterPWA.Components['left_bar']
        if LeftBar is not None and LeftBar is not js_undefined:
            LeftBar.reload()
        window.PhanterPWA.Components["auth_user"].start()

    def start(self):
        self.element_target = jQuery(self.target_selector)
        jQuery(
            document
        ).off(
            "click.main_container"
        ).on(
            "click.main_container",
            lambda event: self._close_on_click_out(event)
        )
        self.auth_user = window.PhanterPWA.get_auth_user()
        self.authorization = window.PhanterPWA.get_authorization()
        self.AlertActivationAccount.close()
        if self.auth_user is not None and self.auth_user is not js_undefined and\
                self.authorization is not None and self.authorization is not js_undefined:
            self.AlertActivationAccount.check_activation()
            first_name = ""
            last_name = ""
            role = I18N("User")
            user_image = window.PhanterPWA.get_auth_user_image()
            if self.auth_user is not None and self.auth_user is not js_undefined:
                first_name = self.auth_user.first_name
                last_name = self.auth_user.last_name
                role = I18N(self.auth_user.role)
            self.xml_button_login = DIV(
                DIV(
                    DIV(
                        DIV(
                            IMG(
                                _id="url_image_user",
                                _src=user_image,
                                _alt='user avatar'
                            ),
                            _class='cmp-bar_user-img'),
                        _class='cmp-bar_user-img-container'),
                    DIV(
                        DIV(
                            DIV(
                                "{0} {1}".format(
                                    first_name,
                                    last_name
                                ),
                                _id="user_first_and_last_name_login", _class='cmp-bar_user-name'
                            ),
                            DIV(role, _id="user_role_login", _class='cmp-bar_user-role'),
                            _class='cmp-bar_user-name-role'),
                        _class='cmp-bar_user-name-role-container'),
                    DIV(
                        DIV(
                            DIV(_class="led"),
                            _class="cmd-bar_user-expands"),
                        _class="cmd-bar_user-expand-container"),
                    _class="cmp-bar_user-info-container"),
                _id="toggle-cmp-bar_user",
                _class="cmp-bar_user-container black link wave_on_click waves-phanterpwa"
            )

            self.xml_button_login_options = CONCATENATE(
                DIV(
                    DIV(
                        I(_class="fas fa-user-circle"),
                        I18N("Profile", **{"_pt-br": "Perfil"}),
                        **{"_phanterpwa-way": "profile",
                            "_class": "option-label-menu"}
                    ),
                    _id="component-auth_user-option-profile",
                    _class='component-auth_user-option link wave_on_click waves-phanterpwa'
                ),
                DIV(
                    DIV(
                        I(_class="fas fa-unlock"),
                        I18N("Lock", **{"_pt-br": "Bloquear"}),
                        **{"_phanterpwa-way": "lock",
                            "_class": "option-label-menu"}
                    ),
                    _id="component-auth_user-option-lock",
                    _class='component-auth_user-option link wave_on_click waves-phanterpwa'
                ),
                DIV(
                    DIV(
                        I(_class="fas fa-power-off"),
                        I18N("Logout", **{"_pt-br": "Sair"}),
                        _class="option-label-menu"
                    ),
                    _id="component-auth_user-option-logout",
                    _class='component-auth_user-option link wave_on_click waves-phanterpwa'
                )
            )

            self.xml_button_login.html_to(self.element_target.find(
                ".phanterpwa-component-auth_user-button-toggle"
            ))

            self.xml_button_login_options.html_to(self.element_target.find(
                ".phanterpwa-component-auth_user-button-toggle-options"
            ))

            self.element_target.find("#component-auth_user-option-logout").off("click.auth_user-option-logout").on(
                "click.auth_user-option-logout",
                lambda: self.logout()
            )
        else:
            self.xml_button_no_login = DIV(
                SPAN(
                    DIV(
                        DIV(
                            DIV(_class="led"),
                            _class="phanterpwa-component-auth_user-nologin-led"
                        ),
                        DIV(
                            I18N("START"),
                            _class="phanterpwa-component-auth_user-nologin-start"
                        ),
                        _class="phanterpwa-component-auth_user-nologin-led_and_start"
                    ),
                    _class="phanterpwa-component-auth_user-nologin-led_and_start-wrapper"
                ),
                _class="phanterpwa-component-auth_user-nologin-wrapper link wave_on_click"
            )

            self.xml_button_no_login_options = CONCATENATE(
                DIV(
                    DIV(
                        I(_class="fas fa-power-off"),
                        I18N("Login", **{"_pt-br": "Login"}),
                        _class="option-label-menu"
                    ),
                    _id="component-auth_user-option-login",
                    _class='component-auth_user-option link wave_on_click waves-phanterpwa'
                ),
                DIV(
                    DIV(
                        I(_class="fas fa-user-plus"),
                        I18N("Create an account", **{"_pt-br": "Criar uma conta"}),
                        _class="option-label-menu"
                    ),
                    _id="component-auth_user-option-register",
                    _class='component-auth_user-option link wave_on_click waves-phanterpwa'
                ),
                DIV(
                    DIV(
                        I(_class="fas fa-lock"),
                        I18N("Recover password", **{"_pt-br": "Esqueci a senha"}),
                        _class="option-label-menu"
                    ),
                    _id="component-auth_user-option-request_password",
                    _class='component-auth_user-option link wave_on_click waves-phanterpwa'
                )
            )

            self.xml_button_no_login.html_to(self.element_target.find(
                ".phanterpwa-component-auth_user-button-toggle"
            ))

            self.xml_button_no_login_options.html_to(self.element_target.find(
                ".phanterpwa-component-auth_user-button-toggle-options"
            ))

            self.element_target.find(
                "#component-auth_user-option-login"
            ).off(
                "click.component-auth_user-option-login"
            ).on(
                "click.component-auth_user-option-login", self.modal_login
            )
            self.element_target.find(
                "#component-auth_user-option-register"
            ).off(
                "click.component-auth_user-option-register"
            ).on(
                "click.component-auth_user-option-register", self.modal_register
            )
            self.element_target.find(
                "#component-auth_user-option-request_password"
            ).off(
                "click.component-auth_user-option-request_password"
            ).on(
                "click.component-auth_user-option-request_password", self.modal_request_password
            )
        self.element_target.find(".component-auth_user-option").off("click.close_on_click").on(
            "click.close_on_click",
            lambda: self.close_menu()
        )
        self.bind_menu_button()


class ModalLogin(modal.Modal):
    def __init__(self, target_element):
        self.element_target = jQuery(target_element)

        AuthUserCmp = window.PhanterPWA.Components["auth_user"]
        self.AuthUser = None
        if AuthUserCmp is not None and AuthUserCmp is not js_undefined and not isinstance(AuthUserCmp, AuthUser):
            console.error("Need AuthUser instance on window.PhanterPWA.Components")
        else:
            self.AuthUser = AuthUserCmp
        self.auth_user = window.PhanterPWA.get_last_auth_user()
        first_name = ""
        last_name = ""
        email = ""
        role = I18N("User")
        user_image = window.PhanterPWA.get_last_auth_user_image()
        remember_me = False
        if self.auth_user is not None and self.auth_user is not js_undefined:
            first_name = self.auth_user.first_name
            last_name = self.auth_user.last_name
            email = self.auth_user.email
            remember_me = self.auth_user.remember_me
            role = I18N(self.auth_user.role)

        tcontent = DIV(
            DIV(
                DIV(
                    DIV(
                        DIV(
                            IMG(
                                _src=user_image,
                                _id="form-login-image-user-url"),
                            _class="form-image-user-img"),
                        _class="form-image-user-img-container"),
                    DIV(
                        DIV(
                            "{0} {1}".format(first_name, last_name),
                            _id='form-login-profile-user-name',
                            _class="form-profile-user-name"
                        ),
                        DIV(
                            role,
                            _id='form-login-profile-user-role',
                            _class="form-profile-user-role"
                        ),
                        _class="form-profile-user-info"),
                    _class="form-profile-container"),
                _id="form-login-image-user-container",
                _class="form-image-user-container"
            ),
            DIV(
                DIV(
                    forms.FormButton(
                        "form-login-button-other-user",
                        I18N("Other account", **{"_pt-br": "Outra Conta"}),
                        _class="wave_on_click waves-phanterpwa btn-s"
                    ),
                    _class='buttons-form-container'
                ),
                _id="form-login-button-other-user-container",
                _class="p-col w1p100"
            ),
            forms.FormWidget(
                "login",
                "email",
                **{
                    "type": "string",
                    "label": I18N("E-mail"),
                    "value": email,
                    "validators": ["IS_NOT_EMPTY", "IS_EMAIL"],
                }
            ),
            DIV(
                forms.FormWidget(
                    "login",
                    "password",
                    **{
                        "label": I18N("Password", **{"_pt-br": "Senha"}),
                        "type": "password",
                        "validators": ["IS_NOT_EMPTY"],

                    }
                ),
                _class="p-col w1p100"
            ),
            DIV(
                forms.FormWidget(
                    "login",
                    "remember_me",
                    **{
                        "value": remember_me,
                        "label": I18N("Remember-me", **{"_pt-br": "Lembre-me"}),
                        "type": "boolean"
                    }
                ),
                _class="input-field p-col w1p100"
            ),
            _class="phanterpwa-auth_user-form-inputs"
        ).jquery()
        if self.auth_user is not None and self.auth_user is not js_undefined:
            tcontent.addClass("has_auth_user")

        tfooter = DIV(
            forms.CaptchaContainer(
                "login",
                preloaders.android
            ),
            DIV(
                forms.SubmitButton(
                    "login",
                    I18N("Login", **{"_pt-br": "Login"}),
                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                ),
                forms.FormButton(
                    "register",
                    I18N("Create an account", **{"_pt-br": "Criar uma conta"}),
                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                ),
                forms.FormButton(
                    "password",
                    I18N("Recover password", **{"_pt-br": "Esqueci a senha"}),
                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                ),
                _class='phanterpwa-form-buttons-container'
            ),
            _class="p-col w1p100"
        ).jquery()
        modal.Modal.__init__(
            self,
            self.element_target,
            **{
                "_phanterpwa-form": "login",
                "_id": "form-login",
                "header_height": 50,
                "footer_height": 200,
                "title": I18N("Login"),
                "content": tcontent,
                "footer": tfooter,
                "after_open": self.binds
            }
        )

    def other_account(self):
        self.element_target.find(".phanterpwa-auth_user-form-inputs").removeClass("has_auth_user")

    def open_modal_register(self):
        self.close()
        window.PhanterPWA.Components['auth_user'].modal_register()

    def open_modal_request_password(self):
        self.close()
        window.PhanterPWA.Components['auth_user'].modal_request_password()

    def binds(self):
        self.element_target.find("#phanterpwa-widget-form-submit_button-login").off('click.modal_submit_login').on(
            'click.modal_submit_login',
            lambda: self.submit()
        )
        self.element_target.find("#phanterpwa-widget-form-form_button-form-login-button-other-user").off(
            "click.other_account_button"
        ).on(
            "click.other_account_button",
            lambda: self.other_account()
        )
        self.element_target.find("#phanterpwa-widget-form-form_button-register").off("click.form_button_register").on(
            "click.form_button_register",
            self.open_modal_register
        )
        self.element_target.find(
            "#phanterpwa-widget-form-form_button-password"
        ).off(
            "click.form_button_request_password"
        ).on(
            "click.form_button_request_password",
            self.open_modal_request_password
        )

    def clear_errors(self):
        jQuery("#form-{0}".format(self._form)).find(".phanterpwa-widget-error").removeClass("enabled").html("")

    def after_submit(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            self.close()
            if self.AuthUser is not None and self.AuthUser is not js_undefined:
                self.AuthUser.start()
                self.AuthUser.AlertActivationAccount.check_activation()
                if json.used_temporary is not None and json.used_temporary is not js_undefined:
                    if window.PhanterPWA.DEBUG:
                        console.error(json.used_temporary)
                    self.AuthUser.modal_change_password(temporary_password=json.used_temporary)
            window.PhanterPWA.flash(**{'html': json.i18n.message})
            LeftBar = window.PhanterPWA.Components['left_bar']
            if LeftBar is not None and LeftBar is not js_undefined:
                LeftBar.reload()

        else:
            if data.status == 400:
                json = data.responseJSON
                window.PhanterPWA.flash(**{'html': json.i18n.message})
                forms.SignForm("#form-login", has_captcha=True)
                errors = dict(json['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        id_error = "#phanterpwa-widget-login-{0} .phanterpwa-widget-error".format(x)
                        message = SPAN(errors[x]).xml()
                        jQuery("#form-{0}".format(self._form)).find(id_error).html(message).addClass("enabled")

    def submit(self):
        self.clear_errors()
        window.PhanterPWA.login(
            jQuery("#phanterpwa-widget-input-login-csrf_token").val(),
            jQuery("#phanterpwa-widget-input-input-login-email").val(),
            jQuery("#phanterpwa-widget-input-input-login-password").val(),
            jQuery("#phanterpwa-widget-checkbox-input-login-remember_me").prop("checked"),
            callback=self.after_submit
        )


class ModalRegister(modal.Modal):
    def __init__(self, target_element):
        self.element_target = jQuery(target_element)
        AuthUserCmp = window.PhanterPWA.Components['auth_user']
        self.AuthUser = None
        if AuthUserCmp is not None and AuthUserCmp is not js_undefined and not isinstance(AuthUserCmp, AuthUser):
            console.error("Need AuthUser instance on window.PhanterPWA.Components")
        else:
            self.AuthUser = AuthUserCmp
        tcontent = DIV(
            forms.FormWidget(
                "register",
                "first_name",
                **{
                    "type": "string",
                    "label": I18N("First Name"),
                    "validators": ["IS_NOT_EMPTY"],
                    "_class": "p-col w1p100 w3p50"
                },
            ),
            forms.FormWidget(
                "register",
                "last_name",
                **{
                    "type": "string",
                    "label": I18N("Last Name"),
                    "validators": ["IS_NOT_EMPTY"],
                    "_class": "p-col w1p100 w3p50"
                },
            ),
            forms.FormWidget(
                "register",
                "email",
                **{
                    "type": "string",
                    "label": I18N("E-Mail"),
                    "validators": ["IS_EMAIL"],
                    "_class": "p-col w1p100"
                }
            ),
            forms.FormWidget(
                "register",
                "password",
                **{
                    "type": "password",
                    "label": I18N("Password"),
                    "validators": ["IS_NOT_EMPTY", "IS_EQUALS:#phanterpwa-widget-input-input-register-password_repeat"],
                    "_class": "p-col w1p100 w3p50"
                }
            ),
            forms.FormWidget(
                "register",
                "password_repeat",
                **{
                    "type": "password",
                    "label": I18N("Repeat Password"),
                    "validators": ["IS_NOT_EMPTY", "IS_EQUALS:#phanterpwa-widget-input-input-register-password"],
                    "_class": "p-col w1p100 w3p50"
                }
            ),
            _class="phanterpwa-register-form-inputs p-row"
        ).jquery()
        if self.auth_user is not None and self.auth_user is not js_undefined:
            tcontent.addClass("has_auth_user")

        tfooter = DIV(
            forms.CaptchaContainer(
                "register",
                preloaders.android
            ),
            DIV(
                forms.SubmitButton(
                    "register",
                    I18N("Create", **{"_pt-br": "Criar"}),
                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                ),
                forms.FormButton(
                    "login",
                    I18N("Login", **{"_pt-br": "Login"}),
                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                ),
                forms.FormButton(
                    "password",
                    I18N("Recover password", **{"_pt-br": "Esqueci a senha"}),
                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                ),
                _class='phanterpwa-form-buttons-container'
            ),
            _class="p-col w1p100"
        ).jquery()
        modal.Modal.__init__(
            self,
            self.element_target,
            **{
                "_phanterpwa-form": "register",
                "_id": "form-register",
                "header_height": 50,
                "footer_height": 200,
                "title": I18N("Register", **{"_pt-br": "Registrar"}),
                "content": tcontent,
                "footer": tfooter,
                "after_open": self.binds
            }
        )

    def open_modal_login(self):
        self.close()
        window.PhanterPWA.Components['auth_user'].modal_login()

    def open_modal_request_password(self):
        self.close()
        window.PhanterPWA.Components['auth_user'].modal_request_password()

    def binds(self):
        self.element_target = jQuery(self.target_selector)
        self.element_target.find(
            "#phanterpwa-widget-form-form_button-login"
        ).off(
            "click.form_button_login"
        ).on(
            "click.form_button_login",
            self.open_modal_login
        )
        self.element_target.find(
            "#phanterpwa-widget-form-form_button-password"
        ).off(
            "click.form_button_request_password"
        ).on(
            "click.form_button_request_password",
            self.open_modal_request_password
        )
        self.element_target.find(
            "#phanterpwa-widget-form-submit_button-register"
        ).off(
            'click.modal_submit_register'
        ).on(
            'click.modal_submit_register',
            lambda: self.submit()
        )

    def clear_errors(self):
        jQuery("#form-{0}".format(self._form)).find(".phanterpwa-widget-error").removeClass("enabled").html("")

    def after_submit(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            if self.AuthUser is not None and self.AuthUser is not js_undefined:
                self.AuthUser.start()
            self.close()
            window.PhanterPWA.flash(**{'html': json.i18n.message})
            LeftBar = window.PhanterPWA.Components['left_bar']
            if LeftBar is not None and LeftBar is not js_undefined:
                LeftBar.reload()

        else:
            if data.status == 400:
                json = data.responseJSON
                window.PhanterPWA.flash(**{'html': json.i18n.message})
                forms.SignForm("#form-register", has_captcha=True)
                errors = dict(json['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        id_error = "#phanterpwa-widget-register-{0} .phanterpwa-widget-error".format(x)
                        message = SPAN(errors[x]).xml()
                        jQuery("#form-{0}".format(self._form)).find(id_error).html(message).addClass("enabled")

    def submit(self):
        self.clear_errors()
        window.PhanterPWA.register(
            jQuery("#phanterpwa-widget-input-register-csrf_token").val(),
            jQuery("#phanterpwa-widget-input-input-register-first_name").val(),
            jQuery("#phanterpwa-widget-input-input-register-last_name").val(),
            jQuery("#phanterpwa-widget-input-input-register-email").val(),
            jQuery("#phanterpwa-widget-input-input-register-password").val(),
            jQuery("#phanterpwa-widget-input-input-register-password_repeat").val(),
            callback=self.after_submit
        )


class ModalRequestPassword(modal.Modal):
    def __init__(self, target_element):
        self.element_target = jQuery(target_element)
        AuthUserCmp = window.PhanterPWA.Components['auth_user']
        self.AuthUser = None
        if AuthUserCmp is not None and AuthUserCmp is not js_undefined and not isinstance(AuthUserCmp, AuthUser):
            console.error("Need AuthUser instance on window.PhanterPWA.Components")
        else:
            self.AuthUser = AuthUserCmp
        widget_email = forms.FormWidget(
            "request_password",
            "email",
            **{
                "type": "string",
                "label": I18N("E-Mail"),
                "phanterpwa": {
                    "validators": ["IS_EMAIL"],
                },
                "_class": "p-col w1p100"
            }
        )
        last_auth_user = window.PhanterPWA.get_last_auth_user()
        if last_auth_user is not None:
            widget_email = forms.FormWidget(
                "request_password",
                "email",
                **{
                    "type": "string",
                    "label": I18N("E-Mail"),
                    "phanterpwa": {
                        "validators": ["IS_EMAIL"],
                    },
                    "value": last_auth_user.email,
                    "_class": "p-col w1p100"
                }
            )
        tcontent = DIV(
            widget_email,
            _class="phanterpwa-request_password-form-inputs p-row"
        ).jquery()
        if self.auth_user is not None and self.auth_user is not js_undefined:
            tcontent.addClass("has_auth_user")

        tfooter = DIV(
            forms.CaptchaContainer(
                "request_password",
                preloaders.android
            ),
            DIV(
                forms.SubmitButton(
                    "request_password",
                    I18N("Recover", **{"_pt-br": "Recuperar"}),
                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                ),
                forms.FormButton(
                    "register",
                    I18N("Create an Account", **{"_pt-br": "Criar uma Conta"}),
                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                ),
                forms.FormButton(
                    "login",
                    I18N("Login", **{"_pt-br": "Login"}),
                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                ),
                _class='phanterpwa-form-buttons-container'
            ),
            _class="p-col w1p100"
        ).jquery()
        modal.Modal.__init__(
            self,
            self.element_target,
            **{
                "_phanterpwa-form": "request_password",
                "_id": "form-request_password",
                "header_height": 50,
                "footer_height": 200,
                "title": I18N("Recover Password", **{"_pt-br": "Recuperar Senha"}),
                "content": tcontent,
                "footer": tfooter,
                "after_open": self.binds
            }
        )

    def open_modal_login(self):
        self.close()
        window.PhanterPWA.Components['auth_user'].modal_login()

    def open_modal_register(self):
        self.close()
        window.PhanterPWA.Components['auth_user'].modal_register()

    def binds(self):
        self.element_target.find(
            "#phanterpwa-widget-form-submit_button-request_password"
        ).off(
            'click.modal_submit_request'
        ).on(
            'click.modal_submit_request',
            lambda: self.submit()
        )
        self.element_target.find("#phanterpwa-widget-form-form_button-register").off("click.form_button_register").on(
            "click.form_button_register",
            self.open_modal_register
        )
        self.element_target.find("#phanterpwa-widget-form-form_button-login").off("click.form_button_login").on(
            "click.form_button_login",
            self.open_modal_login
        )

    def clear_errors(self):
        jQuery("#form-{0}".format(self._form)).find(".phanterpwa-widget-error").removeClass("enabled").html("")

    def after_submit(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            self.close()
            window.PhanterPWA.flash(**{'html': json.i18n.message})
            LeftBar = window.PhanterPWA.Components['left_bar']
            if LeftBar is not None and LeftBar is not js_undefined:
                LeftBar.reload()
        else:
            if data.status == 400:
                json = data.responseJSON
                window.PhanterPWA.flash(**{'html': json.i18n.message})
                forms.SignForm("#form-request_password", has_captcha=True)
                errors = dict(json['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        id_error = "#phanterpwa-widget-request_password-{0} .phanterpwa-widget-error".format(x)
                        message = SPAN(errors[x]).xml()
                        jQuery("#form-{0}".format(self._form)).find(id_error).html(message).addClass("enabled")

    def submit(self):
        self.clear_errors()
        window.PhanterPWA.request_password(
            jQuery("#phanterpwa-widget-input-input-request_password-csrf_token").val(),
            jQuery("#phanterpwa-widget-input-input-request_password-email").val(),
            callback=self.after_submit
        )


class AlertActivationAccount(top_slide.TopSlide):
    def __init__(self, target_element):
        content = DIV(
            _id="phanterpwa-top-slide-auth_user-activation-container",
            _class="phanterpwa-auth_user-activation-container"
        )
        parameters = dict(after_open=self.binds)
        top_slide.TopSlide.__init__(self, target_element, content, **parameters)

    def binds(self):
        self._process_alert_content()
        forms.SignForm("#form-activation")
        forms.ValidateForm("#form-activation")
        self.element_target = jQuery(self.target_selector)
        self.element_target.find("#phanterpwa-widget-form-submit_button-activation").off(
            'click.modal_submit_activation'
        ).on(
            'click.modal_submit_activation',
            lambda: self.submit()
        )
        self.element_target.find("#phanterpwa-widget-form-form_button-activation_new_code").off(
            'click.modal_submit_activation_new_code'
        ).on(
            'click.modal_submit_activation_new_code',
            lambda: self.request_new_activation_code_to_send_to_email()
        )

    def _process_alert_content(self):
        html = CONCATENATE(
            DIV(
                I18N(
                    "{0}{1}{2}".format("Your account has not yet been activated,",
                    " when you created it, the activation code was sent to",
                    " the registered email address. Check your email and add",
                    " the code in the field below."),
                    **{"_pt-br": "{0}{1}{2}".format(
                        "Sua conta ainda não foi ativada, ao criá-la foi enviado",
                        " ao email cadastrado o código de ativação. Check seu ",
                        "email e adicione o código no campo abaixo."
                    )}
                ),
                _class="phanterpwa-auth_user-activation-text"
            ),
            FORM(
                DIV(
                    DIV(
                        forms.FormWidget(
                            "activation",
                            "activation_code",
                            **{
                                "type": "string",
                                "label": I18N("Activation Code", **{"_pt-br": "Código de Ativação"}),
                                "validators": ["IS_NOT_EMPTY", "IS_ACTIVATION_CODE"],
                            }
                        ),
                        _class="phanterpwa-auth_user-activation-action-input"
                    ),
                    DIV(
                        forms.SubmitButton(
                            "activation",
                            I18N("Activate", **{"_pt-br": "Ativar"}),
                            _class="btn-autoresize wave_on_click waves-phanterpwa"
                        ),
                        forms.FormButton(
                            "activation_new_code",
                            I18N("Request Activation Code", **{"_pt-br": "Requisitar novo código"}),
                            _class="btn-autoresize wave_on_click waves-phanterpwa"
                        ),
                        _class='phanterpwa-form-buttons-container'
                    ),
                    _class="phanterpwa-auth_user-activation-actions-activate"
                ),
                **{
                    "_class": "phanterpwa-auth_user-activation-actions-container",
                    "_phanterpwa-form": "activation",
                    "_id": "form-activation"
                }
            )
        )
        html.html_to("#phanterpwa-top-slide-auth_user-activation-container")

    def after_activation_code_send(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            message = json.i18n.message
            window.PhanterPWA.flash(**{'html': message})
        else:
            if data.status == 400:
                json = data.responseJSON
                window.PhanterPWA.flash(**{'html': json.i18n.message})
                forms.SignForm("#form-activation", has_captcha=True)
                errors = dict(json['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        id_error = "#phanterpwa-widget-activation-{0} .phanterpwa-widget-error".format(x)
                        message = SPAN(errors[x]).xml()
                        self.element_target.find(id_error).html(message).addClass("enabled")

    def request_new_activation_code_to_send_to_email(self):
        window.PhanterPWA.ApiServer.GET(**{
            'url_args': ["api", "auth", "active-account"],
            'onComplete': self.after_activation_code_send
        })

    def clear_errors(self):
        self.element_target = jQuery(self.target_selector)
        self.element_target.find(".phanterpwa-widget-error").removeClass("enabled").html("")

    def after_submit(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            self.close()
            window.PhanterPWA.flash(**{'html': json.i18n.message})
        else:
            if data.status == 400:
                json = data.responseJSON
                window.PhanterPWA.flash(**{'html': json.i18n.message})
                forms.SignForm("#form-activation")
                errors = dict(json['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        id_error = "#phanterpwa-widget-activation-{0} .phanterpwa-widget-error".format(x)
                        message = SPAN(errors[x]).xml()
                        jQuery("#form-{0}".format(self._form)).find(id_error).html(message).addClass("enabled")

    def submit(self):
        self.element_target = jQuery(self.target_selector)
        self.clear_errors()
        window.PhanterPWA.activation_account(
            self.element_target.find("#phanterpwa-widget-input-activation-csrf_token").val(),
            self.element_target.find("#phanterpwa-widget-input-input-activation-activation_code").val(),
            callback=self.after_submit
        )

    def check_activation(self):
        auth_user = window.PhanterPWA.get_auth_user()
        if auth_user is not None:
            if not auth_user.activated:
                if window.PhanterPWA.DEBUG:
                    console.info("cheking", auth_user)
                self.open()


class ModalChangePassword(modal.Modal):
    def __init__(self, target_selector, **parameters):
        self.target_selector = target_selector
        self.element_target = jQuery(self.target_selector)
        AuthUserCmp = window.PhanterPWA.Components['auth_user']
        self.AuthUser = None
        if AuthUserCmp is not None and AuthUserCmp is not js_undefined and not isinstance(AuthUserCmp, AuthUser):
            console.error("Need AuthUser instance on window.PhanterPWA.Components")
        else:
            self.AuthUser = AuthUserCmp
        widget_password = forms.FormWidget(
            "change_password",
            "password",
            **{
                "type": "password",
                "label": I18N("Current Password"),
                "validators": ["IS_NOT_EMPTY"],
                "_class": "p-col w1p100"
            }
        )
        if "temporary_password" in parameters:
            if parameters["temporary_password"] is not None and parameters["temporary_password"] is not js_undefined:
                widget_password = forms.FormWidget(
                    "change_password",
                    "password",
                    **{
                        "type": "password",
                        "label": I18N("Current Password"),
                        "validators": ["IS_NOT_EMPTY"],
                        "value": parameters["temporary_password"],
                        "_class": "p-col w1p100",
                        "_style": "display: none;"
                    },
                )
        tcontent = DIV(
            widget_password,
            forms.FormWidget(
                "change_password",
                "new_password",
                **{
                    "type": "password",
                    "label": I18N("New password"),
                    "validators": [
                        "IS_NOT_EMPTY",
                        "IS_EQUALS:#phanterpwa-widget-input-input-change_password-new_password_repeat"
                    ],
                    "_class": "p-col w1p100"
                }
            ),
            forms.FormWidget(
                "change_password",
                "new_password_repeat",
                **{
                    "type": "password",
                    "label": I18N("Password Repeat"),
                    "validators": [
                        "IS_NOT_EMPTY",
                        "IS_EQUALS:#phanterpwa-widget-input-input-change_password-new_password"
                    ],
                    "_class": "p-col w1p100"
                }
            ),
            _class="phanterpwa-change_password-form-inputs p-row"
        ).jquery()
        if self.auth_user is not None and self.auth_user is not js_undefined:
            tcontent.addClass("has_auth_user")

        tfooter = DIV(
            DIV(
                forms.SubmitButton(
                    "change_password",
                    I18N("Change password", **{"_pt-br": "Mudar a senha"}),
                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                ),
                _class='phanterpwa-form-buttons-container'
            ),
            _class="p-col w1p100"
        ).jquery()
        modal.Modal.__init__(
            self,
            self.element_target,
            **{
                "_phanterpwa-form": "change_password",
                "_id": "form-change_password",
                "header_height": 50,
                "title": I18N("Change Password"),
                "content": tcontent,
                "footer": tfooter,
                "after_open": self.binds
            }
        )

    def binds(self):
        self.element_target = jQuery(self.target_selector)
        self.element_target.find("#phanterpwa-widget-form-submit_button-change_password").off(
            'click.modal_submit_request'
        ).on(
            'click.modal_submit_request',
            lambda: self.submit()
        )

    def clear_errors(self):
        jQuery("#form-{0}".format(self._form)).find(".phanterpwa-widget-error").removeClass("enabled").html("")

    def after_submit(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            self.close()
            window.PhanterPWA.flash(**{'html': json.i18n.message})
            LeftBar = window.PhanterPWA.Components['left_bar']
            if LeftBar is not None and LeftBar is not js_undefined:
                LeftBar.reload()

        else:
            if data.status == 400:
                json = data.responseJSON
                window.PhanterPWA.flash(**{'html': json.i18n.message})
                forms.SignForm("#form-change_password")
                errors = dict(json['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        id_error = "#phanterpwa-widget-change_password-{0} .phanterpwa-widget-error".format(x)
                        message = SPAN(errors[x]).xml()
                        jQuery("#form-{0}".format(self._form)).find(id_error).html(message).addClass("enabled")

    def submit(self):
        self.clear_errors()
        window.PhanterPWA.change_password(
            jQuery("#phanterpwa-widget-input-input-change_password-csrf_token").val(),
            jQuery("#phanterpwa-widget-input-input-change_password-password").val(),
            jQuery("#phanterpwa-widget-input-input-change_password-new_password").val(),
            jQuery("#phanterpwa-widget-input-input-change_password-new_password_repeat").val(),
            callback=self.after_submit
        )


class LeftBarMainButton(left_bar.LeftBarMainButton):
    def __init__(self, target_selector):
        left_bar.LeftBarMainButton.__init__(self, target_selector)

    def switch_leftbar(self):
        self.element_target = jQuery(self.target_selector)
        el = self.element_target.find("#phanterpwa-component-left_bar-main_button")
        if el.hasClass("enabled") and el.hasClass("enabled_submenu"):
            self.close_leftbar()
        elif el.hasClass("enabled_submenu"):
            LeftBarAuthUserLogin._close_menu()
            LeftBarAuthUserNoLogin._close_menu()
            AuthUser._close_menu()
            self.open_leftbar()
        elif el.hasClass("enabled"):
            self.close_leftbar()
        else:
            self.open_leftbar()

    @staticmethod
    def _close():
        jQuery("#phanterpwa-component-left_bar-main_button").removeClass("enabled").removeClass("enabled_submenu")

    def close_leftbar(self):
        AuthUser._close_menu()
        self._close()
        left_bar.LeftBar._close()

    @staticmethod
    def _open():
        jQuery("#phanterpwa-component-left_bar-main_button").addClass("enabled")

    def open_leftbar(self):
        self._open()
        left_bar.LeftBar._open()


class LeftBar(left_bar.LeftBar):
    def __init__(self, target_selector, **parameters):
        left_bar.LeftBar.__init__(self, target_selector, **parameters)
        self.add_button(LeftBarAuthUserLogin())
        self.add_button(LeftBarAuthUserNoLogin())
        self.add_button(
            left_bar.LeftBarButton(
                "home",
                I18N("Home", **{"_pt-br": "Principal"}),
                I(_class="fas fa-home"),
                **{"_phanterpwa-way": "home",
                    "position": "top"}
            )
        )


class LeftBarAuthUserLogin(left_bar.LeftBarUserMenu):
    def __init__(self):
        left_bar.LeftBarUserMenu.__init__(self)
        self.position = "top"
        self.addSubmenu(
            "profile",
            I18N("Profile", **{"_pt-br": "Perfil"}),
            **{"_class": "command_user",
                "_phanterpwa-way": "profile"}
        )

        self.addSubmenu(
            "lock",
            I18N("Lock", **{"_pt-br": "Bloquear"}),
            _class="command_user"
        )

        self.addSubmenu(
            "logout",
            I18N("Logout", **{"_pt-br": "Sair"}),
            _class="command_user"
        )

    def switch_menu(self):
        el = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        ).parent()
        if el.hasClass("enabled"):
            self.close_menu()
        else:
            self.open_menu()

    @staticmethod
    def _open_menu(self):
        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-auth_user_login"
        ).parent()
        element.addClass("enabled")
        jQuery("#phanterpwa-component-left_bar").addClass("enabled_submenu")
        jQuery("#phanterpwa-component-left_bar-main_button").addClass("enabled_submenu")

    def open_menu(self):
        AuthUser._open_menu()
        self._open_menu()

    @staticmethod
    def _close_menu(self):
        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-auth_user_login"
        ).parent()
        element.removeClass("enabled")
        if jQuery("#phanterpwa-component-left_bar").find(
                ".phanterpwa-component-left_bar-menu_button-wrapper.enabled").length == 0:
            jQuery("#phanterpwa-component-left_bar").removeClass("enabled_submenu")
            jQuery("#phanterpwa-component-left_bar-main_button").removeClass("enabled_submenu")

    def close_menu(self):
        AuthUser._close_menu()
        self._close_menu()

    def logout(self):
        sessionStorage.removeItem("phanterpwa-authorization")
        sessionStorage.removeItem("auth_user")
        window.PhanterPWA.open_default_way()
        LeftBar = window.PhanterPWA.Components['left_bar']
        if LeftBar is not None and LeftBar is not js_undefined:
            LeftBar.reload()
        window.PhanterPWA.Components['auth_user'].start()

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
        user_image = window.PhanterPWA.get_auth_user_image()
        if self.auth_user is not None:
            first_name = self.auth_user.first_name
            last_name = self.auth_user.last_name
            user_name = "{0} {1}".format(first_name, last_name)
            role = I18N(self.auth_user.role)
        element.find("#phanterpwa-component-left_bar-url-imagem-user").attr("src", user_image)
        element.find("#phanterpwa-component-left_bar-name-user").text(user_name)
        jQuery("#phanterpwa-component-left_bar-submenu-button-logout").off("click.left_bar_buton_logout").on(
            "click.left_bar_buton_logout",
            lambda: self.logout()
        )


class LeftBarAuthUserNoLogin(left_bar.LeftBarMenu):
    def __init__(self):

        left_bar.LeftBarMenu.__init__(
            self,
            "auth_user_no_login",
            I18N("Start", **{"_pt-br": "Início"}),
            I(_class="fas fa-user"),
        )
        self.attributes = dict(_class="{0} {1}".format(
            "phanterpwa-component-left_bar-menu_button-wrapper-auth_user",
            "phanterpwa-component-left_bar-menu_button-wrapper"
        ))
        self.addSubmenu(
            "login",
            I18N("Login", **{"_pt-br": "Logar-se"}),
            _class="command_user"
        )

        self.addSubmenu(
            "register",
            I18N("Create an account", **{"_pt-br": "Criar Conta"}),
            _class="command_user"
        )

        self.addSubmenu(
            "request_password",
            I18N("Recover password", **{"_pt-br": "Esqueci a Senha"}),
            _class="command_user"
        )
        self.position = "top"
        self.autorized_roles = ["anonymous"]

    def switch_menu(self):
        el = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-auth_user_no_login"
        ).parent()
        if el.hasClass("enabled"):
            self.close_menu()
        else:
            self.open_menu()

    @staticmethod
    def _open_menu():
        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-auth_user_no_login"
        ).parent()
        element.addClass("enabled")
        jQuery("#phanterpwa-component-left_bar").addClass("enabled_submenu")
        jQuery("#phanterpwa-component-left_bar-main_button").addClass("enabled_submenu")

    def open_menu(self):
        AuthUser._open_menu()
        self._open_menu()

    def _close_menu(self):
        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-auth_user_no_login"
        ).parent()
        element.removeClass("enabled")
        if jQuery("#phanterpwa-component-left_bar").find(
                ".phanterpwa-component-left_bar-menu_button-wrapper.enabled").length == 0:
            jQuery("#phanterpwa-component-left_bar").removeClass("enabled_submenu")
            jQuery("#phanterpwa-component-left_bar-main_button").removeClass("enabled_submenu")

    def close_menu(self):
        AuthUser._close_menu()
        self._close_menu()

    def close_all(self):
        AuthUser._close_menu()
        LeftBarAuthUserLogin._close_menu()
        LeftBarAuthUserNoLogin._close_menu()
        LeftBarMainButton._close()
        left_bar.LeftBar._close()

    def modal_login(self):
        self.close_all()
        self.Modal = ModalLogin(
            "#modal-container"
        )
        self.Modal.open()
        forms.SignForm("#form-login", has_captcha=True)
        forms.ValidateForm("#form-login")

    def modal_register(self):
        self.close_all()
        self.Modal = ModalRegister(
            "#modal-container"
        )
        self.Modal.open()
        forms.SignForm("#form-register", has_captcha=True)
        forms.ValidateForm("#form-register")

    def modal_request_password(self):
        self.close_all()
        self.Modal = ModalRequestPassword(
            "#modal-container"
        )
        self.Modal.open()
        forms.SignForm("#form-request_password", has_captcha=True)
        forms.ValidateForm("#form-request_password")

    def start(self):

        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        )
        element.off("click.open_leftbar_menu").on(
            "click.open_leftbar_menu",
            lambda: self.switch_menu()
        )
        sub_element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-submenu-from-{0} .phanterpwa-component-left_bar-submenu-button".format(
                self.identifier
            )
        )
        sub_element.off("click.close_leftbar_submenu").on(
            "click.close_leftbar_submenu",
            lambda: self.close_menu()
        )
        jQuery("#phanterpwa-component-left_bar-submenu-button-login").off("click.left_bar_login_button").on(
            "click.left_bar_login_button",
            lambda: self.modal_login()
        )
        jQuery("#phanterpwa-component-left_bar-submenu-button-register").off("click.left_bar_register_button").on(
            "click.left_bar_register_button",
            lambda: self.modal_register()
        )
        jQuery("#phanterpwa-component-left_bar-submenu-button-request_password").off("click.left_bar_request_btn").on(
            "click.left_bar_request_btn",
            lambda: self.modal_request_password()
        )


class Profile(handler.GateHandler):
    def after_submit(self, data, ajax_status):
            if ajax_status == "success":
                json = data.responseJSON
                message = json.i18n.message
                window.PhanterPWA.flash(**{'html': message})
                if data.status == 200:
                    jQuery(".phanterpwa-gallery-upload-input-file").val('')
                    auth_user = json.auth_user
                    window.PhanterPWA.update_auth_user(auth_user)
                    self.reload()

            else:
                forms.SignForm("#form-profile")
                json = data.responseJSON
                message = json.i18n.message
                window.PhanterPWA.flash(**{'html': message})

    def submit(self):
        formdata = __new__(FormData(jQuery("#form-profile")[0]))
        window.PhanterPWA.ApiServer.PUT(**{
            'url_args': ["api", "auth", "change"],
            'form_data': formdata,
            'onComplete': self.after_submit
        })

    def open_modal_change_password(self):
        window.PhanterPWA.Components['auth_user'].modal_change_password()

    def binds(self):
        forms.ValidateForm("#form-profile")
        jQuery(
            "#phanterpwa-widget-form-submit_button-profile"
        ).off(
            "click.profile_button_save"
        ).on(
            "click.profile_button_save",
            self.submit
        )
        jQuery(
            "#phanterpwa-widget-form-form_button-change_password"
        ).off(
            "click.profile_button_change_password"
        ).on(
            "click.profile_button_change_password",
            self.open_modal_change_password
        )

    def reload(self):
        forms.SignForm("#form-profile")
        self.auth_user = window.PhanterPWA.get_last_auth_user()
        first_name = ""
        last_name = ""
        email = ""
        user_image = window.PhanterPWA.get_last_auth_user_image()
        if self.auth_user is not None and self.auth_user is not js_undefined:
            first_name = self.auth_user.first_name
            last_name = self.auth_user.last_name
            email = self.auth_user.email

        self.GalleryInput = gallery.GalleryInput(
            "#profile-image-user-container", **{"cutter": True, "current_image": user_image})
        if not jQuery("#phanterpwa-component-left_bar-url-imagem-user").lenght == 0:
            jQuery("#phanterpwa-component-left_bar-url-imagem-user").attr(
                "src", user_image)
        jQuery("#url_image_user").attr("src", user_image)
        jQuery("#phanterpwa-component-left_bar-url-imagem-user").attr(
            "src", user_image)
        jQuery("#phanterpwa-widget-input-profile-first_name").val(first_name)
        jQuery("#phanterpwa-widget-input-profile-last_name").val(last_name)
        jQuery("#phanterpwa-widget-input-profile-email").val(email).trigger("keyup")

    def start(self):
        self.auth_user = window.PhanterPWA.get_last_auth_user()
        first_name = ""
        last_name = ""
        email = ""
        if self.auth_user is not None and self.auth_user is not js_undefined:
            first_name = self.auth_user.first_name
            last_name = self.auth_user.last_name
            email = self.auth_user.email
        xml_content = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV(I18N("Profile", **{"_pt-br": "Perfil"}), _class="phanterpwa-breadcrumb"),
                        _class="phanterpwa-breadcrumb-wrapper"
                    ),
                    _class="container"),
                _class='title_page_container card'
            ),
            DIV(
                DIV(
                    FORM(
                        DIV(
                            DIV(
                                DIV(
                                    preloaders.android,
                                    _style="text-align:center;"
                                ),
                                _id="profile-image-user-container",
                                _class='p-row'
                            ),
                            _class="p-col w1p100 l4"
                        ),
                        DIV(
                            DIV(
                                forms.FormWidget(
                                    "profile",
                                    "first_name",
                                    **{
                                        "type": "string",
                                        "label": I18N("First Name"),
                                        "value": first_name,
                                        "validators": ["IS_NOT_EMPTY"],
                                        "_class": "p-col w1p100 w3p50"
                                    },
                                ),
                                forms.FormWidget(
                                    "profile",
                                    "last_name",
                                    **{
                                        "type": "string",
                                        "label": I18N("Last Name"),
                                        "value": last_name,
                                        "validators": ["IS_NOT_EMPTY"],
                                        "_class": "p-col w1p100 w3p50"
                                    },
                                ),
                                forms.FormWidget(
                                    "profile",
                                    "email",
                                    **{
                                        "type": "string",
                                        "label": I18N("E-Mail"),
                                        "value": email,
                                        "validators": ["IS_EMAIL"],
                                        "_class": "p-col w1p100"
                                    }
                                ),
                                _class="p-row profile_inputs_container"
                            ),
                            DIV(
                                forms.SubmitButton(
                                    "profile",
                                    I18N("Save Changes", **{"_pt-br": "Salvar Mudanças"}),
                                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                                ),
                                forms.FormButton(
                                    "change_password",
                                    I18N("Change Password", **{"_pt-br": "Mudar Senha"}),
                                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                                ),
                                _class='phanterpwa-form-buttons-container'
                            ),
                            _class="p-col w1p100"
                        ),
                        **{
                            "_phanterpwa-form": "profile",
                            "_id": "form-profile",
                            "_class": "p-row",
                            "_autocomplete": "off"
                        }
                    ),
                    _class='e-margin_bottom_20 phanterpwa-card-container e-padding_20 card'
                ),
                _class="phanterpwa-container container"
            )
        )
        xml_content.html_to("#main-container")
        self.reload()
        self.binds()


class Lock(handler.GateHandler):
    def on_other_user_click(self):
        jQuery("body").removeClass("phanterpwa-lock")
        localStorage.removeItem("last_auth_user")
        localStorage.removeItem("current_way")
        localStorage.removeItem("way_before_lock")
        window.PhanterPWA.Components['auth_user'].logout()

    def after_submit(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            authorization = json.authorization
            auth_user = json.auth_user
            client_token = json.client_token
            url_token = json.url_token
            if (authorization is not js_undefined) and\
                    (auth_user is not js_undefined) and (client_token is not js_undefined):
                localStorage.setItem('phanterpwa-client-token', client_token)
                localStorage.setItem('phanterpwa-url-token', url_token)
                if auth_user["remember_me"] is True:
                    localStorage.setItem("phanterpwa-authorization", authorization)
                    localStorage.setItem("auth_user", JSON.stringify(auth_user))
                    sessionStorage.removeItem("phanterpwa-authorization")
                    sessionStorage.removeItem("auth_user")
                else:
                    sessionStorage.setItem("phanterpwa-authorization", authorization)
                    sessionStorage.setItem("auth_user", JSON.stringify(auth_user))
                    localStorage.removeItem("phanterpwa-authorization")
                    localStorage.removeItem("auth_user")
                localStorage.setItem("last_auth_user", JSON.stringify(auth_user))
            way_before_lock = sessionStorage.getItem("way_before_lock")
            if way_before_lock is not None and way_before_lock is not js_undefined:
                window.PhanterPWA.open_way(way_before_lock)
            else:
                window.PhanterPWA.open_default_way()
            self.AuthUser = window.PhanterPWA.Components['auth_user']
            if self.AuthUser is not None and self.AuthUser is not js_undefined:
                self.AuthUser.start()
                self.AuthUser.AlertActivationAccount.check_activation()
            LeftBar = window.PhanterPWA.Components['left_bar']
            if LeftBar is not None and LeftBar is not js_undefined:
                LeftBar.reload()
            jQuery("body").removeClass("phanterpwa-lock")
            window.PhanterPWA.flash(**{'html': json.i18n.message})
        else:
            if data.status == 400:
                json = data.responseJSON
                window.PhanterPWA.flash(**{'html': json.i18n.message})
                forms.SignLockForm()
                errors = dict(json['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        id_error = "#phanterpwa-widget-login-{0} .phanterpwa-widget-error".format("lock")
                        message = SPAN(errors[x]).xml()
                        jQuery(id_error).html(message).addClass("enabled")

    def submit(self):
        jQuery("#user_locked .phanterpwa-materialize-input-error").removeClass('enabled').text("")
        formdata = __new__(FormData())
        formdata.append(
            "csrf_token",
            jQuery("#form-lock #phanterpwa-widget-input-lock-csrf_token").val()
        )
        login_password = "{0}:{1}".format(
            window.btoa(jQuery("#form-lock #phanterpwa-widget-input-lock-email").val()),
            window.btoa(jQuery("#form-lock #phanterpwa-widget-input-lock-password").val())
        )
        formdata.append("authorization", login_password)
        remember_me = False
        if jQuery("#form-lock #phanterpwa-widget-input-lock-remember_me").prop("checked"):
            remember_me = True
        formdata.append(
            jQuery("#form-lock #phanterpwa-widget-input-lock-remember_me").attr("name"),
            remember_me
        )
        window.PhanterPWA.ApiServer.POST(**{
            'url_args': ["api", "auth"],
            'form_data': formdata,
            'onComplete': self.after_submit
        })

    def binds(self):
        forms.SignLockForm()
        jQuery(
            "#phanterpwa-widget-form-form_button-other"
        ).off(
            "click.other_user_unlock"
        ).on(
            "click.other_user_unlock",
            self.on_other_user_click
        )
        jQuery(
            "#phanterpwa-widget-form-submit_button-lock"
        ).off(
            "click.login_user_unlock"
        ).on(
            "click.login_user_unlock",
            self.submit
        )

    def after_confirm_lock(self, data, ajax_status):
        if ajax_status == "success":
            html = CONCATENATE(
                DIV(
                    DIV(
                        DIV(
                            DIV(
                                DIV(
                                    FORM(
                                        DIV(
                                            DIV(
                                                DIV(
                                                    DIV(
                                                        IMG(
                                                            _id="form-lock-image-user-url"
                                                        ),
                                                        _class="form-image-user-img"
                                                    ),
                                                    _class="form-image-user-img-container"
                                                ),
                                                DIV(
                                                    DIV(
                                                        _id='form-lock-profile-user-name',
                                                        _class="form-profile-user-name"
                                                    ),
                                                    DIV(
                                                        _id='form-lock-profile-user-role',
                                                        _class="form-profile-user-role"
                                                    ),
                                                    _class="form-profile-user-info"
                                                ),
                                                _class="form-profile-container"
                                            ),
                                            _id="form-lock-image-user-container",
                                            _class="form-image-user-container"
                                        ),
                                        forms.FormWidget(
                                            "lock",
                                            "email",
                                            **{
                                                "type": "string",
                                                "label": I18N("E-mail"),
                                                "validators": ["IS_NOT_EMPTY", "IS_EMAIL"],
                                                "_class": "e-display_hidden"
                                            }
                                        ),
                                        DIV(
                                            forms.FormWidget(
                                                "lock",
                                                "password",
                                                **{
                                                    "label": I18N("Password", **{"_pt-br": "Senha"}),
                                                    "type": "password",
                                                    "validators": ["IS_NOT_EMPTY"],

                                                }
                                            ),
                                            _class="p-col w1p100"
                                        ),
                                        DIV(
                                            forms.FormWidget(
                                                "lock",
                                                "remember_me",
                                                **{
                                                    "label": I18N("Remember-me", **{"_pt-br": "Lembre-me"}),
                                                    "type": "boolean"
                                                }
                                            ),
                                            _class="input-field p-col w1p100"
                                        ),
                                        DIV(
                                            DIV(
                                                forms.SubmitButton(
                                                    "lock",
                                                    I18N("Unlock", **{"_pt-br": "Desbloquear"}),
                                                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                                                ),
                                                forms.FormButton(
                                                    "other",
                                                    I18N("Use other account", **{"_pt-br": "Usar outra conta"}),
                                                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                                                ),
                                                _class='phanterpwa-form-buttons-container'
                                            ),
                                            _class="input-field p-col w1p100"
                                        ),
                                        **{
                                            "_phanterpwa-form": "lock",
                                            "_id": "form-lock",
                                            "_class": "p-row",
                                            "_autocomplete": "off"
                                        }
                                    ),
                                    _class="p-col w1p100"
                                ),
                                _class="p-row"
                            ),
                            _class='lock-container'
                        ),
                        _class="card"
                    ),
                    _class="container"
                )
            )
            sessionStorage.removeItem("phanterpwa-authorization")
            sessionStorage.removeItem("auth_user")
            localStorage.removeItem("phanterpwa-authorization")
            localStorage.removeItem("auth_user")
            jQuery("body").addClass("phanterpwa-lock")
            # jQuery("#main-container").html(html.jquery())
            html.html_to("#main-container")
            jQuery("#form-lock #phanterpwa-widget-input-lock-email").val(self.last_auth_user.email)
            if self.last_auth_user.remember_me:
                jQuery("#form-lock #phanterpwa-widget-input-lock-remember_me").attr("checked", "checked")
            jQuery(
                "#form-lock-profile-user-name"
            ).text(
                "{0} {1}".format(self.last_auth_user['first_name'], self.last_auth_user['last_name'])
            )
            jQuery("#form-lock-profile-user-role").text(self.last_auth_user['role'])
            jQuery("#form-lock-image-user-url").attr("src", self.last_auth_user_image)
            self.binds()
        else:
            self.on_other_user_click()
        json = data.responseJSON
        window.PhanterPWA.flash(**{'html': json.i18n.message})

    def start(self):
        request = self.request
        last_way = request["last_way"]
        if last_way is not None and last_way is not js_undefined and last_way is not "lock":
            sessionStorage.setItem("way_before_lock", last_way)
        else:
            sessionStorage.setItem("way_before_lock", window.PhanterPWA.default_way)
        self.last_auth_user = window.PhanterPWA.get_last_auth_user()
        self.last_auth_user_image = window.PhanterPWA.get_last_auth_user_image()
        if self.last_auth_user is not None:
            window.PhanterPWA.ApiServer.GET(**{
                'url_args': ["api", "auth", "lock"],
                'onComplete': self.after_confirm_lock
            })
        else:
            self.on_other_user_click()


__pragma__('nokwargs')
