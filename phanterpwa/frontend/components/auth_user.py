import phanterpwa.frontend.components.modal as modal
import phanterpwa.frontend.components.top_slide as top_slide
import phanterpwa.frontend.components.left_bar as left_bar
import phanterpwa.frontend.components.gallery as gallery
import phanterpwa.frontend.helpers as helpers
import phanterpwa.frontend.forms as forms
import phanterpwa.frontend.preloaders as preloaders
import phanterpwa.frontend.application as application
import phanterpwa.frontend.gatehandler as gatehandler
import phanterpwa.frontend.decorators as decorators
import phanterpwa.frontend.components.widgets as widgets
from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = M = js_undefined = window = setTimeout = document = console = this = \
    __new__ = FormData = console = Date = localStorage = 0
__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")
FORM = helpers.XmlConstructor.tagger("form")
SPAN = helpers.XmlConstructor.tagger("span")
IMG = helpers.XmlConstructor.tagger("img", True)
HR = helpers.XmlConstructor.tagger("hr", True)
BR = helpers.XmlConstructor.tagger("br", True)
I = helpers.XmlConstructor.tagger("i")
H2 = helpers.XmlConstructor.tagger("h2")
P = helpers.XmlConstructor.tagger("p")
LABEL = helpers.XmlConstructor.tagger("label")
STRONG = helpers.XmlConstructor.tagger("strong")
I18N = helpers.I18N
CONCATENATE = helpers.CONCATENATE
XSECTION = helpers.XSECTION
Table = widgets.Table
TableHead = widgets.TableHead
TableData = widgets.TableData

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
        window.PhanterPWA.AuthUserCmp = self
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
        else:
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

    def modal_login(self, **parameters):
        self.close_menu()
        self.Modal = ModalLogin(
            "#modal-container",
            social_logins=window.PhanterPWA.social_login_list(),
            **parameters
        )
        self.Modal.open()
        forms.SignForm("#form-login", has_captcha=True, after_sign=lambda: forms.ValidateForm("#form-login"))
        if parameters.get("other_account", False):
            self.Modal.other_account()

    def modal_register(self, **parameters):
        self.close_menu()
        self.Modal = ModalRegister(
            "#modal-container",
            **parameters
        )
        self.Modal.open()
        forms.SignForm("#form-register", has_captcha=True, after_sign=lambda: forms.ValidateForm("#form-register"))

    def modal_request_password(self, **parameters):
        self.close_menu()
        self.Modal = ModalRequestPassword(
            "#modal-container",
            **parameters
        )
        self.Modal.open()
        forms.SignForm("#form-request_password", has_captcha=True, after_sign=lambda: forms.ValidateForm("#form-request_password"))

    def modal_change_password(self, temporary_password=None):
        self.close_menu()
        self.Modal = ModalChangePassword(
            "#modal-container",
            temporary_password=temporary_password
        )
        self.Modal.open()
        forms.SignForm("#form-change_password", after_sign=lambda: forms.ValidateForm("#form-change_password"))

    def logout(self):
        window.PhanterPWA.logout()
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
                complete_name = "{0} {1}".format(
                    first_name,
                    last_name
                )
            if jQuery("#toggle-cmp-bar_user").lenght == 1:
                jQuery("#user_first_and_last_name_login").text(complete_name)
                jQuery("#user_role_login").html(role)
                src_image = jQuery("#url_image_user").attr("src")
                if src_image != user_image:
                    jQuery("#url_image_user").attr("src", user_image)
            else:
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
                                    complete_name,
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
    def __init__(self, target_element, **parameters):
        self.element_target = jQuery(target_element)
        self._social_logins = parameters.get("social_logins", [])
        self.user_mobile_number = parameters.get("user_mobile_number", None)
        self.mask_mobile_number = parameters.get("mask_mobile_number", "+## (##) # ####-####")
        self.prefix_mobile_number = parameters.get("prefix_mobile_number", 55)
        self.prefix_mobile_list = parameters.get("prefix_mobile_list", [self.prefix_mobile_number])
        self.ignore_last_user = parameters.get("ignore_last_user", False)
        if not isinstance(self._social_logins, list):
            self._social_logins = []
        self.last_auth_user = window.PhanterPWA.get_last_auth_user()
        first_name = ""
        last_name = ""
        email = ""
        fone_number = self.prefix_mobile_number
        role = I18N("User")
        user_image = window.PhanterPWA.get_last_auth_user_image()
        remember_me = False

        if self.last_auth_user is not None and self.last_auth_user is not js_undefined:
            first_name = self.last_auth_user.first_name
            last_name = self.last_auth_user.last_name
            email = self.last_auth_user.email
            fone_number = self.last_auth_user.fone_number if self.last_auth_user.fone_number is not js_undefined else ""
            remember_me = self.last_auth_user.remember_me
            role = I18N(self.last_auth_user.role)

        if self.user_mobile_number is None and str(email).endswith(".mobile@phanterpwa.com"):
            self.user_mobile_number = True
        if all([
                self.mask_mobile_number is not js_undefined,
                self.mask_mobile_number is not None,
                str(self.prefix_mobile_number).isdigit(),
                "SMS" in window.PhanterPWA.CONFIG
            ]):
            if self.user_mobile_number:
                self._social_logins.append(['email', I(_class="fas fa-envelope")])
            else:
                self._social_logins.append(['mobile', I(_class="fas fa-mobile-alt")])
        self._has_social_logins = True if len(self._social_logins) > 0 else False
        AuthUserCmp = window.PhanterPWA.Components["auth_user"]
        self.AuthUser = None
        if AuthUserCmp is not None and AuthUserCmp is not js_undefined and not isinstance(AuthUserCmp, AuthUser):
            console.error("Need AuthUser instance on window.PhanterPWA.Components")
        else:
            self.AuthUser = AuthUserCmp

        self.xml_social_logins = []
        self._icons_social_login = {}
        if self.user_mobile_number is True:
            email_mobile_input = forms.FormWidget(
                "login",
                "mobile",
                **{
                    "type": "string",
                    "label": I18N("Mobile number"),
                    "value": fone_number,
                    "validators": ["IS_NOT_EMPTY", ""],
                    "mask": self.mask_mobile_number
                }
            )
        else:
            email_mobile_input = forms.FormWidget(
                "login",
                "email",
                **{
                    "type": "string",
                    "label": I18N("E-mail"),
                    "value": email,
                    "validators": ["IS_NOT_EMPTY", "IS_EMAIL"]
                }
            )
        if self._has_social_logins:
            for x in self._social_logins:
                icon = ""
                social_name = x
                if isinstance(x, list) and len(x) == 2:
                    icon = x[1]
                    social_name = x[0]
                    self._icons_social_login[social_name] = icon
                self.xml_social_logins.append(
                    DIV(
                        icon,
                        _class="btn-social_login icon_button link",
                        _title="Login with {0}".format(str(social_name).capitalize()),
                        **{
                            "_phanterpwa-i18n-title": "Login with {0}".format(str(social_name).capitalize()),
                            "_data-social_login": social_name
                        }
                    )
                )

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
                            email,
                            _id='form-login-profile-user-email',
                            _class="form-profile-user-email"
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
            email_mobile_input,
            DIV(
                forms.FormWidget(
                    "login",
                    "password",
                    **{
                        "label": I18N("Password", **{"_pt-br": "Senha"}),
                        "type": "password",
                        "validators": ["IS_NOT_EMPTY"],
                        "icon": I(_class="fas fa-eye")

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
        if self._has_social_logins:
            tcontent.addClass("has_social_logins")
        button_login_by_social = ""

        if self.last_auth_user is not None and self.last_auth_user is not js_undefined:
            tcontent.addClass("has_auth_user")
            if self.last_auth_user['social_login'] is not None and self.last_auth_user['social_login'] is not js_undefined:
                icon = self._icons_social_login.get(self.last_auth_user['social_login'], "")

                tcontent.addClass("auth_user_logged_by_social_login")
                current_social_name = self.last_auth_user['social_login']
                button_login_by_social = forms.FormButton(
                    "social_login-{0}".format(current_social_name),
                    CONCATENATE(icon, I18N(
                        "Continue using {0}".format(str(current_social_name).capitalize()),
                        **{"_pt-br": "Continuar com {0}".format(str(current_social_name).capitalize())}
                    )),
                    **{
                        "_class": "btn-social_login wave_on_click waves-phanterpwa",
                        "_data-social_login": current_social_name
                    }
                )

        tfooter = DIV(
            forms.CaptchaContainer(
                "login",
                preloaders.android
            ),
            DIV(
                DIV(
                    forms.SubmitButton(
                        "login",
                        I18N("Login", **{"_pt-br": "Login"}),
                        _class="btn-autoresize wave_on_click waves-phanterpwa"
                    ),
                    _class="hidden_on_its_social_login"
                ),
                DIV(
                    button_login_by_social,
                    _class="hidden_on_not_has_auth_user"
                ),
                _class='phanterpwa-form-buttons-container'
            ),
            _class="p-col w1p100"
        ).jquery()
        if self.last_auth_user is not None and self.last_auth_user is not js_undefined:
            tfooter.addClass("has_auth_user")
            if self.last_auth_user['social_login'] is not None and \
                    self.last_auth_user['social_login'] is not js_undefined:
                tfooter.addClass("its_social_login")
        modal.Modal.__init__(
            self,
            self.element_target,
            **{
                "_phanterpwa-form": "login",
                "_id": "form-login",
                "header_height": 50,
                "footer_height": 200,
                "title": I18N("Login"),
                "buttons_panel": DIV(
                    *self.xml_social_logins,
                    DIV(
                        I(_class="fas fa-sign-in-alt"),
                        _id="phanterpwa-widget-form-form_button-register",
                        _class="icon_button",
                        _title="Create an account",
                        **{"_phanterpwa-i18n-title": "Create an account", "_pt-br": "Criar uma Conta"}
                    ),
                    DIV(
                        I(
                            DIV(
                                DIV(
                                    SPAN(I(_class="fas fa-key"), _class="icombine-container-first"),
                                    SPAN(I(_class="fas fa-sync"), _class="icombine-container-last"),
                                    _class="icombine-container"
                                ),
                                _class="phanterpwa-snippet-icombine"
                            ),
                        ),
                        _id="phanterpwa-widget-form-form_button-password",
                        _title="Recover password",
                        _class="icon_button",
                        **{"_phanterpwa-i18n-title": "Recover password", "_pt-br": "Esqueci a Senha"}
                    )
                ),
                "content": tcontent,
                "footer": tfooter,
                "after_open": self.binds
            }
        )

    def other_account(self):
        self.element_target.find(".phanterpwa-auth_user-form-inputs").removeClass("has_auth_user")
        self.element_target.find(
            ".phanterpwa-component-modal-footer-container").find(".has_auth_user").removeClass("has_auth_user")

    def open_modal_register(self):
        self.close()
        if self.user_mobile_number is True:
            window.PhanterPWA.Components['auth_user'].modal_register(
                user_mobile_number=True
            )
        else:
            window.PhanterPWA.Components['auth_user'].modal_register(
                user_mobile_number=False
            )

    def open_modal_request_password(self):
        self.close()
        if self.user_mobile_number is True:
            window.PhanterPWA.Components['auth_user'].modal_request_password(
                user_mobile_number=True
            )
        else:
            window.PhanterPWA.Components['auth_user'].modal_request_password(
                user_mobile_number=False
            )

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
        self.element_target.find(
            ".btn-social_login"
        ).off(
            "click.social_button"
        ).on(
            "click.social_button",
            lambda: self._on_click_social_button(this)
        )
        self.element_target.find("#phanterpwa-widget-input-input-login-mobile").trigger("keyup")
        email = jQuery("#phanterpwa-widget-input-input-login-email").val()
        if str(email).endswith(".mobile@phanterpwa.com"):
            jQuery("#phanterpwa-widget-input-input-login-email").val("")

        self.element_target.find("#phanterpwa-widget-input-input-login-mobile").off(
            "change.fix_prefix, keyup.fix_prefix"
        ).on(
            "change.fix_prefix, keyup.fix_prefix",
            lambda: self.fix_prefix(this)
        )

    def fix_prefix(self, el):
        console.log(el)
        value = jQuery(el).val()
        numbers = [str(x) for x in range(10)]
        cont = 0
        for x in str(value):
            if x in numbers:
                cont += 1

        size = len(str(self.prefix_mobile_number))
        if cont < size:
            jQuery(el).val(self.prefix_mobile_number).trigger("keyup")

    def _on_click_social_button(self, el):
        social = jQuery(el).data("social_login")
        if social == "mobile":
            self.Modal = ModalLogin(
                "#modal-container",
                social_logins=window.PhanterPWA.social_login_list(),
                user_mobile_number=True,
            )
            self.Modal.open()
            self.other_account()
            forms.SignForm("#form-login", has_captcha=True, after_sign=lambda: forms.ValidateForm("#form-login"))
        elif social == "email":
            self.Modal = ModalLogin(
                "#modal-container",
                social_logins=window.PhanterPWA.social_login_list(),
                user_mobile_number=False
            )
            self.Modal.open()
            self.other_account()
            forms.SignForm("#form-login", has_captcha=True, after_sign=lambda: forms.ValidateForm("#form-login"))

        else:
            window.PhanterPWA.social_login(social)

    def clear_errors(self):
        jQuery("#form-{0}".format(self._form)).find(".phanterpwa-widget-error").removeClass("enabled").html("")

    def after_submit(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            self.close()
            if data.status == 200:
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
            elif data.status == 206:
                window.PhanterPWA.flash(**{'html': json.i18n.message})
                window.PhanterPWA.open_way("two_factor/{0}".format(json.authorization_url))

        else:
            if data.status == 400:
                json = data.responseJSON
                window.PhanterPWA.flash(**{'html': json.i18n.message})
                forms.SignForm("#form-login", has_captcha=True)
                errors = dict(json.i18n['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        wg = window.PhanterPWA.get_widget("login-{0}".format(x))
                        if wg is not None:
                            wg.set_message_error(SPAN(errors[x]).xml())
                # errors = dict(json['errors'])
                # if errors is not js_undefined:
                #     for x in errors.keys():
                #         id_error = "#phanterpwa-widget-login-{0} .phanterpwa-widget-error".format(x)
                #         message = SPAN(errors[x]).xml()
                #         jQuery("#form-{0}".format(self._form)).find(id_error).html(message).addClass("enabled")
            elif data.status == 401:
                json = data.responseJSON
                window.PhanterPWA.flash(**{'html': json.i18n.message})
                forms.SignForm("#form-login", has_captcha=True)
                if json.reasons == "Mobile number does not exist":
                    self.Modal = ModalRegister(
                        "#modal-container",
                        user_mobile_number=True,
                        mobile=json.fone_number,
                        password=json.password
                    )
                    self.Modal.open()
                    forms.SignForm("#form-register", has_captcha=True, after_sign=lambda: forms.ValidateForm("#form-register"))

                elif json.reasons == "Email does not exist":
                    self.Modal = ModalRegister(
                        "#modal-container",
                        email=json.email,
                        password=json.password
                    )
                    self.Modal.open()
                    forms.SignForm("#form-register", has_captcha=True, after_sign=lambda: forms.ValidateForm("#form-register"))

    def submit(self):
        self.clear_errors()
        if self.user_mobile_number is True:
            window.PhanterPWA.login(
                jQuery("#phanterpwa-widget-input-input-login-csrf_token").val(),
                jQuery("#phanterpwa-widget-input-input-login-mobile").val(),
                jQuery("#phanterpwa-widget-input-input-login-password").val(),
                jQuery("#phanterpwa-widget-checkbox-input-login-remember_me").prop("checked"),
                callback=self.after_submit,
                user_mobile_number=True
            )
        else:
            window.PhanterPWA.login(
                jQuery("#phanterpwa-widget-input-input-login-csrf_token").val(),
                jQuery("#phanterpwa-widget-input-input-login-email").val(),
                jQuery("#phanterpwa-widget-input-input-login-password").val(),
                jQuery("#phanterpwa-widget-checkbox-input-login-remember_me").prop("checked"),
                callback=self.after_submit
            )


class ModalPersonalInformation(modal.Modal):
    def __init__(self, target_element, **parameters):
        AuthUserCmp = window.PhanterPWA.Components['auth_user']
        self.AuthUser = None
        if AuthUserCmp is not None and AuthUserCmp is not js_undefined and not isinstance(AuthUserCmp, AuthUser):
            console.error("Need AuthUser instance on window.PhanterPWA.Components")
        else:
            self.AuthUser = AuthUserCmp
        self.element_target = jQuery(target_element)
        self.auth_user = window.PhanterPWA.get_last_auth_user()
        first_name = ""
        last_name = ""
        email = ""
        two_factor = False
        multiple_login = False
        if self.auth_user is not None and self.auth_user is not js_undefined:
            first_name = self.auth_user.first_name
            last_name = self.auth_user.last_name
            email = self.auth_user.email
            two_factor = self.auth_user.two_factor
            multiple_login = self.auth_user.multiple_login
        hidden_fields = parameters.get("hidden_fields", None)
        information = parameters.get('information', "")
        first_name_hidden = None
        last_name_hidden = None
        email_hidden = None
        two_factor_hidden = None
        multiple_login_hidden = None
        if hidden_fields is not None:
            if "first_name" in hidden_fields:
                first_name_hidden = " e-hidden"
            if "last_name" in hidden_fields:
                last_name_hidden = " e-hidden"
            if "email" in hidden_fields:
                email_hidden = " e-hidden"
            if "two_factor" in hidden_fields:
                two_factor_hidden = " e-hidden"
            if "multiple_login" in hidden_fields:
                multiple_login_hidden = " e-hidden"

        tcontent = DIV(
            P(information),
            DIV(
                DIV(
                    DIV(
                        forms.FormWidget(
                            "change_account",
                            "first_name",
                            **{
                                "type": "string",
                                "label": I18N("First Name"),
                                "value": first_name,
                                "validators": ["IS_NOT_EMPTY"],
                                "_class": "p-col w1p100 w3p50"
                            },
                        ),
                        _class=first_name_hidden
                    ),
                    DIV(
                        forms.FormWidget(
                            "change_account",
                            "last_name",
                            **{
                                "type": "string",
                                "label": I18N("Last Name"),
                                "value": last_name,
                                "validators": ["IS_NOT_EMPTY"],
                                "_class": "p-col w1p100 w3p50"
                            },
                        ),
                        _class=last_name_hidden
                    ),
                    DIV(
                        forms.FormWidget(
                            "change_account",
                            "email",
                            **{
                                "type": "string",
                                "label": I18N("E-Mail"),
                                "value": email,
                                "validators": ["IS_EMAIL"],
                                "_class": "p-col w1p100"
                            }
                        ),
                        _class=email_hidden
                    ),
                    DIV(
                        forms.FormWidget(
                            "change_account",
                            "two_factor",
                            **{
                                "value": two_factor,
                                "label": I18N("Two-step authentication", **{"_pt-br": "Autenticação em duas etapas"}),
                                "type": "boolean"
                            }
                        ),
                        _class=two_factor_hidden
                    ),
                    DIV(
                        forms.FormWidget(
                            "change_account",
                            "multiple_login",
                            **{
                                "value": multiple_login,
                                "label": I18N("Multiple logins", **{"_pt-br": "Múltiplos logins"}),
                                "type": "boolean"
                            }
                        ),
                        _class=multiple_login_hidden
                    ),
                    _class="p-row change_account_inputs_container"
                ),
                _class="p-col w1p100"
            ),

            _class="phanterpwa-change_account-form-inputs p-row"
        ).jquery()
        if self.auth_user is not None and self.auth_user is not js_undefined:
            tcontent.addClass("has_auth_user")

        tfooter = DIV(
            DIV(
                forms.SubmitButton(
                    "change_account",
                    I18N("Save Changes", **{"_pt-br": "Salvar Mudanças"}),
                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                ),
                # forms.FormButton(
                #     "change_password",
                #     I18N("Change Password", **{"_pt-br": "Mudar Senha"}),
                #     _class="btn-autoresize wave_on_click waves-phanterpwa"
                # ),
                _class='phanterpwa-form-buttons-container'
            ),
            _class="p-col w1p100"
        ).jquery()
        modal.Modal.__init__(
            self,
            self.element_target,
            **{
                "form": "change_account",
                "header_height": 50,
                "title": I18N("Personal Information", **{"_pt-br": "Informações Pessoais"}),
                "content": tcontent,
                "footer": tfooter,
                "after_open": self.binds
            }
        )

    def after_submit(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            message = json.i18n.message
            window.PhanterPWA.flash(**{'html': message})
            if data.status == 200:
                jQuery(".phanterpwa-gallery-upload-input-file").val('')
                auth_user = json.auth_user
                window.PhanterPWA.store_auth_user(auth_user)
                self.reload()
                self.close()
                if self.AuthUser is not None:
                    self.AuthUser.AlertActivationAccount.check_activation()
            else:
                forms.SignForm("#form-change_account")

        else:
            forms.SignForm("#form-change_account")
            json = data.responseJSON
            message = json.i18n.message
            window.PhanterPWA.flash(**{'html': message})

    def submit(self):
        formdata = __new__(FormData(jQuery("#form-change_account")[0]))
        window.PhanterPWA.ApiServer.PUT(**{
            'url_args': ["api", "auth", "change"],
            'form_data': formdata,
            'onComplete': self.after_submit
        })

    def binds(self):
        forms.ValidateForm("#form-change_account")
        jQuery(
            "#phanterpwa-widget-form-submit_button-change_account"
        ).off(
            "click.profile_button_save"
        ).on(
            "click.profile_button_save",
            self.submit
        )
        # jQuery(
        #     "#phanterpwa-widget-form-form_button-change_password"
        # ).off(
        #     "click.profile_button_change_password"
        # ).on(
        #     "click.profile_button_change_password",
        #     self.open_modal_change_password
        # )

    def reload(self):
        forms.SignForm("#form-change_account")
        self.auth_user = window.PhanterPWA.get_last_auth_user()
        first_name = ""
        last_name = ""
        email = ""
        two_factor = False
        multiple_login = False
        if self.auth_user is not None and self.auth_user is not js_undefined:
            first_name = self.auth_user.first_name
            last_name = self.auth_user.last_name
            email = self.auth_user.email
            two_factor = self.auth_user.two_factor
            multiple_login = self.auth_user.multiple_login

        two_factor_represent = I(_class="fas fa-times")
        multiple_login_represent = I(_class="fas fa-times")
        if self.auth_user.two_factor is not None and self.auth_user.two_factor is not js_undefined: 
            two_factor = self.auth_user.two_factor
            if two_factor:
                two_factor_represent = I(_class="fas fa-check")


        if self.auth_user.multiple_login is not None and self.auth_user.multiple_login is not js_undefined: 
            multiple_login = self.auth_user.multiple_login
            if multiple_login:
                multiple_login_represent = I(_class="fas fa-check")

        jQuery("#phanterpwa-widget-input-input-profile-first_name").val(first_name)
        jQuery("#phanterpwa-widget-input-input-profile-last_name").val(last_name)
        jQuery("#phanterpwa-widget-input-input-profile-email").val(email)
        jQuery("#phanterpwa-tagger-span-first_name").text(first_name)
        jQuery("#phanterpwa-tagger-span-last_name").text(last_name)
        jQuery("#phanterpwa-tagger-span-email").text(email)
        jQuery("#phanterpwa-tagger-span-two_factor").html(two_factor_represent.jquery())
        jQuery("#phanterpwa-tagger-span-multiple_login").html(multiple_login_represent.jquery())
        window.PhanterPWA.Request.widgets['profile-two_factor'].set_value(two_factor)
        window.PhanterPWA.Request.widgets['profile-multiple_login'].set_value(multiple_login)


class ModalRegister(modal.Modal):
    def __init__(self, target_element, **parameters):
        self.element_target = jQuery(target_element)
        AuthUserCmp = window.PhanterPWA.Components['auth_user']
        self.AuthUser = None
        if AuthUserCmp is not None and AuthUserCmp is not js_undefined and not isinstance(AuthUserCmp, AuthUser):
            console.error("Need AuthUser instance on window.PhanterPWA.Components")
        else:
            self.AuthUser = AuthUserCmp
        self.user_mobile_number = parameters.get("user_mobile_number", None)
        self.mask_mobile_number = parameters.get("mask_mobile_number", "+## (##) # ####-####")
        self.prefix_mobile_number = parameters.get("prefix_mobile_number", 55)
        self.prefix_mobile_list = parameters.get("prefix_mobile_list", [self.prefix_mobile_number])
        if self.user_mobile_number is True:
            mobile = parameters.get("mobile", self.prefix_mobile_number)
            input_name = forms.FormWidget(
                "register",
                "mobile",
                **{
                    "type": "string",
                    "label": I18N("Mobile Number"),
                    "validators": ["IS_NOT_EMPTY"],
                    "value": mobile,
                    "mask": self.mask_mobile_number,
                    "_class": "p-col w1p100"
                }
            )
        else:
            email = parameters.get("email", "")
            input_name = forms.FormWidget(
                "register",
                "email",
                **{
                    "type": "string",
                    "value": email,
                    "label": I18N("E-Mail"),
                    "validators": ["IS_EMAIL"],
                    "_class": "p-col w1p100"
                }
            )
        password = parameters.get("password", "")
        self._xml_button = []
        if "SMS" in window.PhanterPWA.CONFIG:
            if self.user_mobile_number is True:
                self._xml_button.append(
                    DIV(
                        I(_class="fas fa-envelope"),
                        _class="btn-social_login icon_button link",
                        _title="Register with {0}".format(str("email").capitalize()),
                        **{
                            "_phanterpwa-i18n-title": "Register with {0}".format(str("email").capitalize()),
                            "_data-social_login": "email",
                            "_pt-br": "Registrar com o {0}".format(str("email").capitalize())
                        }
                    )
                )
            else:
                self._xml_button.append(
                    DIV(
                        I(_class="fas fa-mobile-alt"),
                        _class="btn-social_login icon_button link",
                        _title="Register with {0}".format(str("mobile").capitalize()),
                        **{
                            "_phanterpwa-i18n-title": "Register with {0}".format(str("mobile").capitalize()),
                            "_data-social_login": "mobile",
                            "_pt-br": "Registrar com o {0}".format(str("mobile").capitalize())
                        }
                    )
                )

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
            input_name,
            forms.FormWidget(
                "register",
                "password",
                **{
                    "type": "password",
                    "label": I18N("Password"),
                    "value": password,
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
                "buttons_panel": DIV(
                    *self._xml_button,
                    DIV(
                        I(_class="fas fa-user-circle"),
                        _id="phanterpwa-widget-form-form_button-login",
                        _class="icon_button",
                        _title="Login",
                        **{"_phanterpwa-i18n-title": "Login", "_pt-br": "Logar-se"}
                    ),
                    DIV(
                        I(
                            DIV(
                                DIV(
                                    SPAN(I(_class="fas fa-key"), _class="icombine-container-first"),
                                    SPAN(I(_class="fas fa-sync"), _class="icombine-container-last"),
                                    _class="icombine-container"
                                ),
                                _class="phanterpwa-snippet-icombine"
                            ),
                        ),
                        _id="phanterpwa-widget-form-form_button-password",
                        _title="Recover password",
                        _class="icon_button",
                        **{"_phanterpwa-i18n-title": "Recover password", "_pt-br": "Esqueci a Senha"}
                    )
                ),
                "content": tcontent,
                "footer": tfooter,
                "after_open": self.binds
            }
        )

    def open_modal_login(self):
        self.close()
        if self.user_mobile_number:
            window.PhanterPWA.Components['auth_user'].modal_login(
                user_mobile_number=True,
                other_account=True
            )
        else:
            window.PhanterPWA.Components['auth_user'].modal_login(
                user_mobile_number=False,
                other_account=True
            )

    def open_modal_request_password(self):
        self.close()
        if self.user_mobile_number:
            window.PhanterPWA.Components['auth_user'].modal_request_password(
                user_mobile_number=True
            )
        else:
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
        self.element_target.find(
            ".btn-social_login"
        ).off(
            "click.social_button"
        ).on(
            "click.social_button",
            lambda: self._on_click_social_button(this)
        )
        self.element_target.find("#phanterpwa-widget-input-input-register-mobile").trigger("keyup")
        email = jQuery("#phanterpwa-widget-input-input-register-email").val()
        if str(email).endswith(".mobile@phanterpwa.com"):
            jQuery("#phanterpwa-widget-input-input-register-email").val("")

        self.element_target.find("#phanterpwa-widget-input-input-register-mobile").off(
            "change.fix_prefix, keyup.fix_prefix"
        ).on(
            "change.fix_prefix, keyup.fix_prefix",
            lambda: self.fix_prefix(this)
        )

    def fix_prefix(self, el):
        value = jQuery(el).val()
        numbers = [str(x) for x in range(10)]
        cont = 0
        for x in str(value):
            if x in numbers:
                cont += 1

        size = len(str(self.prefix_mobile_number))
        if cont < size:
            jQuery(el).val(self.prefix_mobile_number).trigger("keyup")

    def _on_click_social_button(self, el):
        social = jQuery(el).data("social_login")
        if social == "mobile":
            window.PhanterPWA.Components['auth_user'].modal_register(
                user_mobile_number=True
            )
        elif social == "email":
            window.PhanterPWA.Components['auth_user'].modal_register(
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
                errors = dict(json.i18n['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        wg = window.PhanterPWA.get_widget("register-{0}".format(x))
                        if wg is not None:
                            wg.set_message_error(SPAN(errors[x]).xml())
                        # id_error = "#phanterpwa-widget-register-{0} .phanterpwa-widget-error".format(x)
                        # message = SPAN(errors[x]).xml()
                        # jQuery("#form-{0}".format(self._form)).find(id_error).html(message).addClass("enabled")

    def submit(self):
        self.clear_errors()
        if self.user_mobile_number:
            window.PhanterPWA.register(
                jQuery("#phanterpwa-widget-input-input-register-csrf_token").val(),
                jQuery("#phanterpwa-widget-input-input-register-first_name").val(),
                jQuery("#phanterpwa-widget-input-input-register-last_name").val(),
                jQuery("#phanterpwa-widget-input-input-register-mobile").val(),
                jQuery("#phanterpwa-widget-input-input-register-password").val(),
                jQuery("#phanterpwa-widget-input-input-register-password_repeat").val(),
                callback=self.after_submit,
                user_mobile_number=True
            )
        else:
            window.PhanterPWA.register(
                jQuery("#phanterpwa-widget-input-input-register-csrf_token").val(),
                jQuery("#phanterpwa-widget-input-input-register-first_name").val(),
                jQuery("#phanterpwa-widget-input-input-register-last_name").val(),
                jQuery("#phanterpwa-widget-input-input-register-email").val(),
                jQuery("#phanterpwa-widget-input-input-register-password").val(),
                jQuery("#phanterpwa-widget-input-input-register-password_repeat").val(),
                callback=self.after_submit
            )


class ModalRequestPassword(modal.Modal):
    def __init__(self, target_element, **parameters):
        self.element_target = jQuery(target_element)
        AuthUserCmp = window.PhanterPWA.Components['auth_user']
        self.AuthUser = None
        if AuthUserCmp is not None and AuthUserCmp is not js_undefined and not isinstance(AuthUserCmp, AuthUser):
            console.error("Need AuthUser instance on window.PhanterPWA.Components")
        else:
            self.AuthUser = AuthUserCmp
        self.user_mobile_number = parameters.get("user_mobile_number", None)
        self.mask_mobile_number = parameters.get("mask_mobile_number", "+## (##) # ####-####")
        self.prefix_mobile_number = parameters.get("prefix_mobile_number", 55)
        self.prefix_mobile_list = parameters.get("prefix_mobile_list", [self.prefix_mobile_number])

        self.last_auth_user = window.PhanterPWA.get_last_auth_user()
        email = ""
        fone_number = self.prefix_mobile_number
        if self.last_auth_user is not None and self.last_auth_user is not js_undefined:
            email = self.last_auth_user.email
            fone_number = self.last_auth_user.fone_number if self.last_auth_user.fone_number is not js_undefined else ""

        if self.user_mobile_number:
            widget_email = forms.FormWidget(
                "request_password",
                "mobile",
                **{
                    "type": "string",
                    "label": I18N("Mobile number"),
                    "validators": ["IS_NOT_EMPTY"],
                    "value": fone_number,
                    "mask": self.mask_mobile_number,
                    "_class": "p-col w1p100"
                }
            )
        else:
            widget_email = forms.FormWidget(
                "request_password",
                "email",
                **{
                    "type": "string",
                    "label": I18N("E-Mail"),
                    "validators": ["IS_EMAIL"],
                    "value": email,
                    "_class": "p-col w1p100"
                }
            )

        self._xml_button = []
        if "SMS" in window.PhanterPWA.CONFIG:
            if self.user_mobile_number is True:
                self._xml_button.append(
                    DIV(
                        I(_class="fas fa-envelope"),
                        _class="btn-social_login icon_button link",
                        _title="Recover with {0}".format(str("email").capitalize()),
                        **{
                            "_phanterpwa-i18n-title": "Register with {0}".format(str("email").capitalize()),
                            "_data-social_login": "email",
                            "_pt-br": "Recuperar com o {0}".format(str("email").capitalize())
                        }
                    )
                )
            else:
                self._xml_button = [
                    DIV(
                        I(_class="fas fa-mobile-alt"),
                        _class="btn-social_login icon_button link",
                        _title="Recover with {0}".format(str("mobile").capitalize()),
                        **{
                            "_phanterpwa-i18n-title": "Register with {0}".format(str("mobile").capitalize()),
                            "_data-social_login": "mobile",
                            "_pt-br": "Recuperar com o {0}".format(str("mobile").capitalize())
                        }
                    )
                ]

        tcontent = DIV(
            BR(),
            widget_email,
            DIV(_style="min-height: 35px;display: table;width: 10px;"),
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
                "buttons_panel": DIV(
                    *self._xml_button,
                    DIV(
                        I(_class="fas fa-user-circle"),
                        _id="phanterpwa-widget-form-form_button-login",
                        _class="icon_button",
                        _title="Login",
                        **{"_phanterpwa-i18n-title": "Login", "_pt-br": "Logar-se"}
                    ),
                    DIV(
                        I(_class="fas fa-sign-in-alt"),
                        _id="phanterpwa-widget-form-form_button-register",
                        _class="icon_button",
                        _title="Create an account",
                        **{"_phanterpwa-i18n-title": "Create an account", "_pt-br": "Criar uma Conta"}
                    ),
                ),

                "content": tcontent,
                "footer": tfooter,
                "after_open": self.binds
            }
        )

    def open_modal_login(self):
        self.close()
        if self.user_mobile_number:
            window.PhanterPWA.Components['auth_user'].modal_login(
                user_mobile_number=True,
                other_account=True
            )
        else:
            window.PhanterPWA.Components['auth_user'].modal_login(
                other_account=True
            )

    def open_modal_register(self):
        self.close()
        if self.user_mobile_number:
            window.PhanterPWA.Components['auth_user'].modal_register(
                user_mobile_number=True,
            )
        else:
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
        self.element_target.find(
            ".btn-social_login"
        ).off(
            "click.social_button"
        ).on(
            "click.social_button",
            lambda: self._on_click_social_button(this)
        )
        self.element_target.find("#phanterpwa-widget-input-input-request_password-mobile").trigger("keyup")

        email = jQuery("#phanterpwa-widget-input-input-request_password-email").val()
        if str(email).endswith(".mobile@phanterpwa.com"):
            jQuery("#phanterpwa-widget-input-input-request_password-email").val("")

        self.element_target.find("#phanterpwa-widget-input-input-request_password-mobile").off(
            "change.fix_prefix, keyup.fix_prefix"
        ).on(
            "change.fix_prefix, keyup.fix_prefix",
            lambda: self.fix_prefix(this)
        )

    def fix_prefix(self, el):
        console.log(el)
        value = jQuery(el).val()
        numbers = [str(x) for x in range(10)]
        cont = 0
        for x in str(value):
            if x in numbers:
                cont += 1

        size = len(str(self.prefix_mobile_number))
        if cont < size:
            jQuery(el).val(self.prefix_mobile_number).trigger("keyup")

    def _on_click_social_button(self, el):
        social = jQuery(el).data("social_login")
        if social == "mobile":
            window.PhanterPWA.Components['auth_user'].modal_register(
                user_mobile_number=True
            )
        elif social == "email":
            window.PhanterPWA.Components['auth_user'].modal_register(
            )

    def _on_click_social_button(self, el):
        social = jQuery(el).data("social_login")
        if social == "mobile":
            window.PhanterPWA.Components['auth_user'].modal_request_password(
                user_mobile_number=True
            )
        elif social == "email":
            window.PhanterPWA.Components['auth_user'].modal_request_password(
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
                errors = dict(json.i18n['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        wg = window.PhanterPWA.get_widget("request_password-{0}".format(x))
                        if wg is not None:
                            wg.set_message_error(SPAN(errors[x]).xml())

                # errors = dict(json['errors'])
                # if errors is not js_undefined:
                #     for x in errors.keys():
                #         id_error = "#phanterpwa-widget-request_password-{0} .phanterpwa-widget-error".format(x)
                #         message = SPAN(errors[x]).xml()
                #         jQuery("#form-{0}".format(self._form)).find(id_error).html(message).addClass("enabled")

    def submit(self):
        self.clear_errors()
        if self.user_mobile_number:
            window.PhanterPWA.request_password(
                jQuery("#phanterpwa-widget-input-input-request_password-csrf_token").val(),
                jQuery("#phanterpwa-widget-input-input-request_password-mobile").val(),
                callback=self.after_submit,
                user_mobile_number=True
            )
        else:
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
        forms.SignForm("#form-activation", after_sign=lambda: forms.ValidateForm("#form-activation"))
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
        email = PhanterPWA.get_auth_user().email
        if str(email).endswith(".mobile@phanterpwa.com"):
            html = CONCATENATE(
                DIV(
                    I18N(
                        "{0}{1}{2}".format("Your account has not yet been activated,",
                        " when you created it, the activation code was sent by sms to",
                        " the your mobile number. Add the code received in the field below.")
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
        else:
            html = CONCATENATE(
                DIV(
                    I18N(
                        "{0}{1}{2}".format("Your account has not yet been activated,",
                        " when you created it, the activation code was sent to",
                        " the registered email address. Check your email and add the code in the field below."),
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
                errors = dict(json.i18n['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        wg = window.PhanterPWA.get_widget("activation-{0}".format(x))
                        if wg is not None:
                            wg.set_message_error(SPAN(errors[x]).xml())
                # errors = dict(json['errors'])
                # if errors is not js_undefined:
                #     for x in errors.keys():
                #         id_error = "#phanterpwa-widget-activation-{0} .phanterpwa-widget-error".format(x)
                #         message = SPAN(errors[x]).xml()
                #         self.element_target.find(id_error).html(message).addClass("enabled")

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
                errors = dict(json.i18n['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        wg = window.PhanterPWA.get_widget("activation-{0}".format(x))
                        if wg is not None:
                            wg.set_message_error(SPAN(errors[x]).xml())

                # errors = dict(json['errors'])
                # if errors is not js_undefined:
                #     for x in errors.keys():
                #         id_error = "#phanterpwa-widget-activation-{0} .phanterpwa-widget-error".format(x)
                #         message = SPAN(errors[x]).xml()
                #         jQuery("#form-{0}".format(self._form)).find(id_error).html(message).addClass("enabled")

    def submit(self):
        self.element_target = jQuery(self.target_selector)
        self.clear_errors()
        window.PhanterPWA.activation_account(
            self.element_target.find("#phanterpwa-widget-input-input-activation-csrf_token").val(),
            self.element_target.find("#phanterpwa-widget-input-input-activation-activation_code").val(),
            callback=self.after_submit
        )

    def check_activation(self):
        auth_user = window.PhanterPWA.get_auth_user()
        _phanterpwa_user_try_activation = sessionStorage.getItem("_phanterpwa-user-try-activation")

        if auth_user is not None:
            if window.PhanterPWA.DEBUG:
                console.info("cheking", auth_user)
            if not auth_user.activated:
                if not(_phanterpwa_user_try_activation == "true" or _phanterpwa_user_try_activation is True):
                    self.request_new_activation_code_to_send_to_email()
                    sessionStorage.setItem("_phanterpwa-user-try-activation", "true")
                self.open()
                return False
            else:
                return True


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
                errors = dict(json.i18n['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        wg = window.PhanterPWA.get_widget("change_password-{0}".format(x))
                        if wg is not None:
                            wg.set_message_error(SPAN(errors[x]).xml())

                # errors = dict(json['errors'])
                # if errors is not js_undefined:
                #     for x in errors.keys():
                #         id_error = "#phanterpwa-widget-change_password-{0} .phanterpwa-widget-error".format(x)
                #         message = SPAN(errors[x]).xml()
                #         jQuery("#form-{0}".format(self._form)).find(id_error).html(message).addClass("enabled")

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
                **{"tag": "a",
                    "_href": "#_phanterpwa:/home",
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
            **{"_phanterpwa-way": "lock",
                "_class": "command_user"}
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
        window.PhanterPWA.logout()
        self.start()
        window.PhanterPWA.logout()
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
        if element.find("#phanterpwa-component-left_bar-url-imagem-user").attr("src") != user_image:
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
            "#modal-container",
            social_logins=window.PhanterPWA.social_login_list()
        )
        self.Modal.open()
        forms.SignForm("#form-login", has_captcha=True, after_sign=lambda: forms.ValidateForm("#form-login"))

    def modal_register(self):
        self.close_all()
        self.Modal = ModalRegister(
            "#modal-container"
        )
        self.Modal.open()
        forms.SignForm("#form-register", has_captcha=True, after_sign=lambda: forms.ValidateForm("#form-register"))

    def modal_request_password(self):
        self.close_all()
        self.Modal = ModalRequestPassword(
            "#modal-container"
        )
        self.Modal.open()
        forms.SignForm("#form-request_password", has_captcha=True, after_sign=lambda: forms.ValidateForm("#form-request_password"))

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


class Profile(gatehandler.Handler):

    @decorators.check_authorization(lambda: window.PhanterPWA.logged())
    def initialize(self):
        self.auth_user = window.PhanterPWA.get_last_auth_user()
        first_name = ""
        last_name = ""
        email = ""
        locale = "Automatic"
        two_factor = False
        two_factor_represent = I(_class="fas fa-times")
        multiple_login = False
        multiple_login_represent = I(_class="fas fa-times")
        if self.auth_user is not None and self.auth_user is not js_undefined:
            first_name = self.auth_user.first_name
            last_name = self.auth_user.last_name
            email = self.auth_user.email
            if self.auth_user.locale is not None and self.auth_user.locale is not js_undefined:
                locale = self.auth_user.locale

            if self.auth_user.two_factor is not None and self.auth_user.two_factor is not js_undefined:
                two_factor = self.auth_user.two_factor
                if two_factor:
                    two_factor_represent = I(_class="fas fa-check")

            if self.auth_user.multiple_login is not None and self.auth_user.multiple_login is not js_undefined:
                multiple_login = self.auth_user.multiple_login
                if multiple_login:
                    multiple_login_represent = I(_class="fas fa-check")

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
                    XSECTION(
                        LABEL(I18N("Personal Information", **{"_pt-br": "Informações Pessoais"})),
                        FORM(
                            DIV(
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
                                        DIV(
                                            STRONG(I18N("First Name")),
                                            SPAN(
                                                first_name,
                                                _id="phanterpwa-tagger-span-first_name"
                                            ),
                                            DIV(
                                                I(_class="fas fa-pen"),
                                                _class="e-tagger-button e-link open-model-edit-personal_information"
                                            ),
                                            _class="e-tagger-wrapper"
                                        ),
                                        _class="p-col w1p100"
                                    ),
                                    _class="p-row"
                                ),
                                DIV(
                                    DIV(
                                        DIV(
                                            STRONG(I18N("Last Name")),
                                            SPAN(
                                                last_name,
                                                _id="phanterpwa-tagger-span-last_name"
                                            ),
                                            DIV(
                                                I(_class="fas fa-pen"),
                                                _class="e-tagger-button e-link open-model-edit-personal_information"
                                            ),
                                            _class="e-tagger-wrapper"
                                        ),
                                        _class="p-col w1p100"
                                    ),
                                    _class="p-row"
                                ),
                                DIV(
                                    DIV(
                                        DIV(
                                            STRONG(I18N("E-Mail")),
                                            SPAN(
                                                email,
                                                _id="phanterpwa-tagger-span-email"
                                            ),
                                            DIV(
                                                I(_class="fas fa-pen"),
                                                _class="e-tagger-button e-link open-model-edit-change_email"
                                            ),
                                            _class="e-tagger-wrapper"
                                        ),
                                        _class="p-col w1p100"
                                    ),
                                    _class="p-row"
                                ),
                                _class="e-padding_20"
                            ),
                            DIV(
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
                                        forms.FormWidget(
                                            "profile",
                                            "two_factor",
                                            **{
                                                "value": two_factor,
                                                "label": I18N("Two-step authentication", **{"_pt-br": "Autenticação em duas etapas"}),
                                                "type": "boolean"
                                            }
                                        ),
                                        forms.FormWidget(
                                            "profile",
                                            "multiple_login",
                                            **{
                                                "value": multiple_login,
                                                "label": I18N("Multiple logins", **{"_pt-br": "Múltiplos logins"}),
                                                "type": "boolean"
                                            }
                                        ),
                                        _class="p-row profile_inputs_container"
                                    ),

                                    _class="p-col w1p100"
                                ),
                                _class="e-padding_20 e-hidden"
                            ),
                            **{
                                "_phanterpwa-form": "profile",
                                "_id": "form-profile",
                                "_class": "p-row",
                                "_autocomplete": "off"
                            }
                        ),
                    ),
                    XSECTION(
                        LABEL(I18N("Segurity", **{"_pt-br": "Segurança"})),
                        FORM(
                            DIV(
                                DIV(
                                    DIV(
                                        DIV(
                                            STRONG(I18N("Two-step authentication")),
                                            SPAN(
                                                two_factor_represent,
                                                _id="phanterpwa-tagger-span-two_factor"
                                            ),
                                            DIV(
                                                I(_class="fas fa-pen"),
                                                _class="e-tagger-button e-link open-model-edit-two_factor"
                                            ),
                                            _class="e-tagger-wrapper"
                                        ),
                                        _class="p-col w1p100"
                                    ),
                                    _class="p-row"
                                ),
                                DIV(
                                    DIV(
                                        DIV(
                                            STRONG(I18N("Password")),
                                            SPAN(
                                                I(_class="fas fa-ellipsis-h", _style="margin-right: 1px;"),
                                                I(_class="fas fa-ellipsis-h", _style="margin-right: 1px;"),
                                                I(_class="fas fa-ellipsis-h"),
                                                _id="phanterpwa-tagger-span-password"
                                            ),
                                            DIV(
                                                I(_class="fas fa-pen"),
                                                _class="e-tagger-button e-link open-model-edit-password"
                                            ),
                                            _class="e-tagger-wrapper"
                                        ),
                                        _class="p-col w1p100"
                                    ),
                                    _class="p-row"
                                ),
                                DIV(
                                    DIV(
                                        DIV(
                                            STRONG(I18N("Multiple logins")),
                                            SPAN(
                                                multiple_login_represent,
                                                _id="phanterpwa-tagger-span-multiple_login"
                                            ),
                                            DIV(
                                                I(_class="fas fa-pen"),
                                                _class="e-tagger-button e-link open-model-edit-multiple_login"
                                            ),
                                            _class="e-tagger-wrapper"
                                        ),
                                        _class="p-col w1p100"
                                    ),
                                    DIV(
                                        HR(),
                                        H2(I18N("Active sessions")),
                                        DIV(
                                            DIV(
                                                preloaders.android,
                                                _style="text-align:center; overflow: hidden;"
                                            ),
                                            _id="active_sessions_wrapper"
                                        ),
                                        _class="p-col w1p100"
                                    ),
                                    DIV(
                                        HR(),
                                        H2(I18N("Your Activity")),
                                        DIV(
                                            DIV(
                                                preloaders.android,
                                                _style="text-align:center; overflow: hidden;"
                                            ),
                                            _id="user_activity_wrapper"
                                        ),
                                        _class="p-col w1p100"
                                    ),
                                    _class="p-row"
                                ),
                                _class="e-padding_20"
                            ),
                            **{
                                "_phanterpwa-form": "security",
                                "_id": "form-security",
                                "_class": "p-row",
                                "_autocomplete": "off"
                            }
                        ),
                    ),
                    _class='e-margin_bottom_20 phanterpwa-card-container e-padding_20 card'
                ),
                _class="phanterpwa-container container"
            )
        )
        xml_content.html_to("#main-container")

        self.reload()
        self.get_active_sessions()
        self.get_activity()

    def after_submit(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            message = json.i18n.message
            window.PhanterPWA.flash(**{'html': message})
            if data.status == 200:
                jQuery(".phanterpwa-gallery-upload-input-file").val('')
                auth_user = json.auth_user
                window.PhanterPWA.store_auth_user(auth_user)
                self.reload()

        else:
            forms.SignForm("#form-profile")
            json = data.responseJSON
            message = json.i18n.message
            window.PhanterPWA.flash(**{'html': message})

    def get_active_sessions(self):
        window.PhanterPWA.ApiServer.GET(**{
            'url_args': ["api", "auth"],
            'onComplete': self._active_sessions_xml
        })

    def _active_sessions_xml(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            if json.sessions is not None and json.sessions is not js_undefined:
                MyTable = Table(
                    "session_table"
                )
                cont = 0
                for x in json.sessions:
                    cont += 1
                    date_created = __new__(Date(x["date_created"]))
                    date_created = date_created.toLocaleDateString(
                        window.PhanterPWA.I18N.load_storage(), {
                            "year": "numeric",
                            "month": "2-digit",
                            "day": "numeric"
                        }
                    )
                    identify = x["identify"]
                    if x["this_session"]:
                        agent = STRONG(x["agent"])
                        date_created = STRONG(date_created)
                        remote_addr = STRONG(x["remote_addr"])
                        this_session = DIV(
                            STRONG(I18N("This Session", **{"_pt-br": "Esta sessão"})),
                            _class="btn",
                            **{"_data-session_id": identify, "_disabled": "disabled"}
                        )

                    else:
                        agent = x["agent"]
                        date_created = date_created
                        remote_addr = x["remote_addr"]
                        this_session = DIV(
                            I18N("Cancel", **{"_pt-br": "Cancelar"}),
                            _class="phanterpwa_cancel_session e-link btn wave_on_click",
                            **{"_data-session_id": identify}
                        )
                    MyTable.append(
                        TableData(
                            "data_{0}".format(cont),
                            agent, date_created, remote_addr, this_session, drag_and_drop=False)
                    )
                MyTable.html_to("#active_sessions_wrapper")
                jQuery(
                    ".phanterpwa_cancel_session"
                ).off(
                    "click.cancel_session"
                ).on(
                    "click.cancel_session",
                    lambda: self.delete_session(jQuery(this).attr("data-session_id"))
                )

    def _after_delete_session(self, data, ajax_status):
        json = data.responseJSON
        if ajax_status == "success":
            self._active_sessions_xml(data, ajax_status)
        window.PhanterPWA.flash(**{'html': json.i18n.message})

    def delete_session(self, identify):
        window.PhanterPWA.ApiServer.DELETE(**{
            'url_args': ["api", "auth", identify],
            'onComplete': self._after_delete_session
        })

    def submit(self):
        formdata = __new__(FormData(jQuery("#form-profile")[0]))
        window.PhanterPWA.ApiServer.PUT(**{
            'url_args': ["api", "auth", "change"],
            'form_data': formdata,
            'onComplete': self.after_submit
        })

    def open_modal_change_password(self):
        window.PhanterPWA.Components['auth_user'].modal_change_password()

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
            "#profile-image-user-container", **{
                "cutter": True,
                "current_image": user_image,
                "afterCut": lambda: self.submit()
            }
        )
        if not jQuery("#phanterpwa-component-left_bar-url-imagem-user").lenght == 0:
            jQuery("#phanterpwa-component-left_bar-url-imagem-user").attr(
                "src", user_image)
        jQuery("#url_image_user").attr("src", user_image)
        jQuery("#phanterpwa-component-left_bar-url-imagem-user").attr(
            "src", user_image)
        jQuery("#phanterpwa-widget-input-input-profile-first_name").val(first_name)
        jQuery("#phanterpwa-widget-input-input-profile-last_name").val(last_name)
        jQuery("#phanterpwa-widget-input-input-profile-email").val(email).trigger("keyup")
        jQuery(
            ".open-model-edit-personal_information"
        ).off(
            "click.open-model-edit-personal_information"
        ).on(
            "click.open-model-edit-personal_information",
            lambda: self.modal_personal_information()
        )
        jQuery(
            ".open-model-edit-change_email"
        ).off(
            "click.open-model-edit-change_email"
        ).on(
            "click.open-model-edit-change_email",
            lambda: self.modal_change_email()
        )
        jQuery(
            ".open-model-edit-two_factor"
        ).off(
            "click.open-model-edit-two_factor"
        ).on(
            "click.open-model-edit-two_factor",
            lambda: self.modal_change_two_factor()
        )
        jQuery(
            ".open-model-edit-multiple_login"
        ).off(
            "click.open-model-edit-multiple_login"
        ).on(
            "click.open-model-edit-multiple_login",
            lambda: self.modal_change_multiple_login()
        )
        jQuery(
            ".open-model-edit-password"
        ).off(
            "click.open-model-edit-password"
        ).on(
            "click.open-model-edit-password",
            lambda: self.open_modal_change_password()
        )

    def modal_personal_information(self):
        self.Modal = ModalPersonalInformation(
            "#modal-container",
            hidden_fields=["email", "two_factor", "multiple_login"]
        )
        self.Modal.open()
        forms.SignForm("#form-change_account", after_sign=lambda: forms.ValidateForm("#form-change_account"))

    def modal_change_email(self):
        self.Modal = ModalPersonalInformation(
            "#modal-container",
            hidden_fields=["first_name", "last_name", "two_factor", "multiple_login"]
        )
        self.Modal.open()
        forms.SignForm("#form-change_account", after_sign=lambda: forms.ValidateForm("#form-change_account"))

    def modal_change_two_factor(self):
        self.Modal = ModalPersonalInformation(
            "#modal-container",
            hidden_fields=["first_name", "last_name", "email", "multiple_login"],
            information=I18N("When activated, upon login, a code will be sent to the" +
                " registered email. The login will only be effective if the correct " +
                "code is added in the appropriate place."),
        )
        self.Modal.open()
        forms.SignForm("#form-change_account", after_sign=lambda: forms.ValidateForm("#form-change_account"))

    def modal_change_multiple_login(self):
        self.Modal = ModalPersonalInformation(
            "#modal-container",
            hidden_fields=["first_name", "last_name", "email", "two_factor"],
            information=I18N("When enabled, it allows you to log in and stay logged" +
                " in on several different devices. When deactivated, when you " +
                "log in to a certain device, you are automatically logged out of the others.")
        )
        self.Modal.open()
        forms.SignForm("#form-change_account", after_sign=lambda: forms.ValidateForm("#form-change_account"))

    def get_activity(self):
        window.PhanterPWA.GET(
            "api",
            "auth",
            "activity",
            onComplete=self._after_get_activity,
        )

    def _after_get_activity(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            if json.data is not None and json.data is not js_undefined:
                MyTable = Table(
                    "activity_table"
                )
                cont = 0
                for x in json.data:
                    cont += 1
                    date_created = __new__(Date(x.date_activity))
                    date_created = date_created.toLocaleDateString(
                        window.PhanterPWA.I18N.load_storage(), {
                            "year": "numeric",
                            "month": "2-digit",
                            "day": "numeric"
                        }
                    )
                    activity = x.activity
                    MyTable.append(
                        TableData(
                            "data_activity_{0}".format(x.id),
                            date_created, activity, drag_and_drop=False)
                    )
                MyTable.html_to("#user_activity_wrapper")


class Oauth(gatehandler.Handler):

    def initialize(self):
        arg0 = self.request.get_arg(0)
        arg1 = self.request.get_arg(1)
        xml_content = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV("Oauth", _class="phanterpwa-breadcrumb"),
                        _class="phanterpwa-breadcrumb-wrapper"
                    ),
                    _class="container"),
                _class='title_page_container card'
            ),
            DIV(
                DIV(
                    DIV(
                        DIV(preloaders.android, _style="width: 300px; height: 300px; overflow: hidden; margin: auto;"),
                        _style="text-align:center; padding: 50px 0;"
                    ),
                    _id="content-alunos",
                    _class='p-row card e-padding_20'
                ),

                _class="phanterpwa-container p-container"
            )
        )
        xml_content.html_to("#main-container")
        if arg0 is not None and arg1 is not None:
            window.PhanterPWA.oauth(arg0, arg1)
        else:
            window.PhanterPWA.open_way("home")


class Lock(gatehandler.Handler):
    def initialize(self):
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
                errors = dict(json.i18n['errors'])
                if errors is not js_undefined:
                    for x in errors.keys():
                        wg = window.PhanterPWA.get_widget("login-{0}".format(x))
                        if wg is not None:
                            wg.set_message_error(SPAN(errors[x]).xml())
                # errors = dict(json['errors'])
                # if errors is not js_undefined:
                #     for x in errors.keys():
                #         id_error = "#phanterpwa-widget-login-{0} .phanterpwa-widget-error".format("lock")
                #         message = SPAN(errors[x]).xml()
                #         jQuery(id_error).html(message).addClass("enabled")

    def submit(self):
        jQuery("#user_locked .phanterpwa-materialize-input-error").removeClass('enabled').text("")
        formdata = __new__(FormData())
        formdata.append(
            "csrf_token",
            jQuery("#form-lock #phanterpwa-widget-input-input-lock-csrf_token").val()
        )
        login_password = "{0}:{1}".format(
            window.btoa(jQuery("#form-lock #phanterpwa-widget-input-input-lock-email").val()),
            window.btoa(jQuery("#form-lock #phanterpwa-widget-input-input-lock-password").val())
        )
        formdata.append("edata", login_password)
        remember_me = False
        if jQuery("#form-lock #phanterpwa-widget-checkbox-input-lock-remember_me").prop("checked"):
            remember_me = True
        formdata.append(
            jQuery("#form-lock #phanterpwa-widget-checkbox-input-lock-remember_me").attr("name"),
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
                            DIV(I18N("Locked", **{"_pt-br": "Bloqueado"}), _class="phanterpwa-breadcrumb"),
                            _class="phanterpwa-breadcrumb-wrapper"
                        ),
                        _class="container"),
                    _class='title_page_container card'
                ),
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
            jQuery("#form-lock #phanterpwa-widget-input-input-lock-email").val(self.last_auth_user.email)
            if self.last_auth_user.remember_me:
                # jQuery("#form-lock #phanterpwa-widget-checkbox-input-lock-remember_me").attr("checked", "checked").val(True)
                PhanterPWA.Request.widgets["lock-remember_me"].set_value(True)
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


class TwoFactor(gatehandler.Handler):
    def initialize(self):
        self._authorization_url_two_factor = self._request.get_arg(0)
        AuthUserCmp = window.PhanterPWA.Components["auth_user"]
        self.AuthUser = None
        if AuthUserCmp is not None and AuthUserCmp is not js_undefined and not isinstance(AuthUserCmp, AuthUser):
            console.error("Need AuthUser instance on window.PhanterPWA.Components")
        else:
            self.AuthUser = AuthUserCmp
        last_way = self._request["last_way"]
        if last_way is not None and last_way is not js_undefined and not last_way.startswith("two_factor"):
            self.way_before_two_factor = last_way
        else:
            self.way_before_two_factor = window.PhanterPWA.default_way
        self.start()

    def after_submit(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            self.AuthUser.start()
            self.AuthUser.AlertActivationAccount.check_activation()
            window.PhanterPWA.flash(**{'html': json.i18n.message})
            LeftBar = window.PhanterPWA.Components['left_bar']
            if LeftBar is not None and LeftBar is not js_undefined:
                LeftBar.reload()
            window.PhanterPWA.open_way(self.way_before_two_factor)

    def submit(self):
        window.PhanterPWA.two_factor(
            self._authorization_url_two_factor,
            jQuery("#phanterpwa-widget-input-input-confirmation-code-code").val(),
            callback=self.after_submit
        )

    def binds(self):
        forms.ValidateForm("#form-confirmation-code")
        jQuery(
            "#phanterpwa-widget-form-submit_button-confirmation-code"
        ).off(
            "click.confirmation-code_button_save"
        ).on(
            "click.confirmation-code_button_save",
            self.submit
        )

    def reload(self):
        self.start()

    def start(self):
        xml_content = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV(
                            I18N(
                                "Two Factor Authentication",
                                **{"_pt-br": "Autenticação de duas etapas"}
                            ),
                            _class="phanterpwa-breadcrumb"
                        ),
                        _class="phanterpwa-breadcrumb-wrapper"
                    ),
                    _class="container"),
                _class='title_page_container card'
            ),
            DIV(
                DIV(
                    FORM(
                        H2(
                            I18N("Login Confirmation Code", **{"_pt-br": "Código de confirmação do login"})
                        ),
                        P(
                            I18N(
                                "The two-factor confirmation code has ",
                                "been sent to your email, add it below and confirm.",
                                **{"_pt-br":
                                    "Um código de confirmação foi enviado ao seu email, digite-o abaixo e confirme"}
                            )
                        ),
                        DIV(
                            DIV(
                                forms.FormWidget(
                                    "confirmation-code",
                                    "code",
                                    **{
                                        "type": "string",
                                        "label": I18N("Confirmation code", **{"_pt-br": "Código de Confirmação"}),
                                        "validators": ["IS_NOT_EMPTY", "IS_ACTIVATION_CODE"],
                                        "_class": "p-col w1p100"
                                    },
                                ),
                                _class="p-row profile_inputs_container"
                            ),
                            DIV(
                                forms.SubmitButton(
                                    "confirmation-code",
                                    I18N("Confirm", **{"_pt-br": "Confirmar"}),
                                    _class="btn-autoresize wave_on_click waves-phanterpwa"
                                ),
                                _class='phanterpwa-form-buttons-container'
                            ),
                            _class="p-col w1p100"
                        ),
                        **{
                            "_phanterpwa-form": "confirmation-code",
                            "_id": "form-confirmation-code",
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
        self.binds()


__pragma__('nokwargs')
