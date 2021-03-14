// Transcrypt'ed from Python, 2021-03-12 14:18:21
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as decorators from './phanterpwa.frontend.decorators.js';
import * as gatehandler from './phanterpwa.frontend.gatehandler.js';
import * as application from './phanterpwa.frontend.application.js';
import * as preloaders from './phanterpwa.frontend.preloaders.js';
import * as forms from './phanterpwa.frontend.forms.js';
import * as helpers from './phanterpwa.frontend.helpers.js';
import * as gallery from './phanterpwa.frontend.components.gallery.js';
import * as left_bar from './phanterpwa.frontend.components.left_bar.js';
import * as top_slide from './phanterpwa.frontend.components.top_slide.js';
import * as modal from './phanterpwa.frontend.components.modal.js';
var __name__ = 'phanterpwa.frontend.components.auth_user';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var FORM = helpers.XmlConstructor.tagger ('form');
export var SPAN = helpers.XmlConstructor.tagger ('span');
export var IMG = helpers.XmlConstructor.tagger ('img', true);
export var I = helpers.XmlConstructor.tagger ('i');
export var H2 = helpers.XmlConstructor.tagger ('h2');
export var P = helpers.XmlConstructor.tagger ('p');
export var LABEL = helpers.XmlConstructor.tagger ('label');
export var STRONG = helpers.XmlConstructor.tagger ('strong');
export var I18N = helpers.I18N;
export var CONCATENATE = helpers.CONCATENATE;
export var XSECTION = helpers.XSECTION;
export var AuthUser =  __class__ ('AuthUser', [application.Component], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, target_selector) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'target_selector': var target_selector = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		self.target_selector = target_selector;
		self.element_target = $ (self.target_selector);
		self.callback = null;
		self.Modal = null;
		self.AlertActivationAccount = AlertActivationAccount ('#layout-top_slide-container');
		self.auth_user = null;
		self.authorization = null;
		if (__in__ ('callback', parameters)) {
			self.callback = parameters ['callback'];
		}
		var html = DIV (DIV (__kwargtrans__ ({_class: 'link phanterpwa-component-auth_user-button-toggle'})), DIV (__kwargtrans__ ({_class: 'phanterpwa-component-auth_user-button-toggle-options'})), __kwargtrans__ ({_id: 'phanterpwa-component-auth_user-container', _class: 'phanterpwa-component-auth_user-container'}));
		application.Component.__init__ (self, 'auth_user', html);
		self.html_to (target_selector);
	});},
	get switch_menu () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target = $ (self.target_selector);
		if (self.element_target.find ('.phanterpwa-component-auth_user-container').hasClass ('enabled')) {
			self.close_menu ();
		}
		else {
			self.open_menu ();
		}
	});},
	get bind_menu_button () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target = $ (self.target_selector);
		self.element_target.find ('.phanterpwa-component-auth_user-button-toggle').off ('click.components-auth_user-button').on ('click.components-auth_user-button', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.switch_menu ();
		}));
	});},
	get reload () {return __get__ (this, function (self) {
		var context = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						default: context [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete context.__kwargtrans__;
			}
		}
		else {
		}
		if (__in__ ('ajax', context)) {
			if (context ['ajax'] [1] [0] == 'client' || context ['ajax'] [1] [0] == 'auth') {
				self.element_target = $ (self.target_selector);
				self.start ();
			}
		}
	});},
	get _open_menu () {return function () {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
				}
			}
		}
		else {
		}
		$ ('#phanterpwa-component-auth_user-container').addClass ('enabled');
	};},
	get open_menu () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self._open_menu ();
		LeftBarAuthUserLogin._open_menu ();
		LeftBarAuthUserNoLogin._open_menu ();
	});},
	get _close_menu () {return __get__ (this, function () {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
				}
			}
		}
		else {
		}
		$ ('#phanterpwa-component-auth_user-container').removeClass ('enabled');
	});},
	get close_menu () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self._close_menu ();
		LeftBarAuthUserLogin._close_menu ();
		LeftBarAuthUserNoLogin._close_menu ();
	});},
	get _close_on_click_out () {return __get__ (this, function (self, event) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target = $ (self.target_selector);
		if ($ (event.target).closest (self.element_target).length == 0) {
			if ($ (event.target).closest ($ ('.phanterpwa-component-left_bar-menu_button-wrapper-auth_user')).length == 0) {
				self.close_menu ();
			}
		}
	});},
	get modal_login () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close_menu ();
		self.Modal = ModalLogin ('#modal-container', __kwargtrans__ ({social_logins: window.PhanterPWA.social_login_list ()}));
		self.Modal.open ();
		forms.SignForm ('#form-login', __kwargtrans__ ({has_captcha: true}));
		forms.ValidateForm ('#form-login');
	});},
	get modal_register () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close_menu ();
		self.Modal = ModalRegister ('#modal-container');
		self.Modal.open ();
		forms.SignForm ('#form-register', __kwargtrans__ ({has_captcha: true}));
		forms.ValidateForm ('#form-register');
	});},
	get modal_request_password () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close_menu ();
		self.Modal = ModalRequestPassword ('#modal-container');
		self.Modal.open ();
		forms.SignForm ('#form-request_password', __kwargtrans__ ({has_captcha: true}));
		forms.ValidateForm ('#form-request_password');
	});},
	get modal_change_password () {return __get__ (this, function (self, temporary_password) {
		if (typeof temporary_password == 'undefined' || (temporary_password != null && temporary_password.hasOwnProperty ("__kwargtrans__"))) {;
			var temporary_password = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'temporary_password': var temporary_password = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close_menu ();
		self.Modal = ModalChangePassword ('#modal-container', __kwargtrans__ ({temporary_password: temporary_password}));
		self.Modal.open ();
		forms.SignForm ('#form-change_password');
		forms.ValidateForm ('#form-change_password');
	});},
	get logout () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		window.PhanterPWA.logout ();
		var LeftBar = window.PhanterPWA.Components ['left_bar'];
		if (LeftBar !== null && LeftBar !== undefined) {
			LeftBar.reload ();
		}
		window.PhanterPWA.Components ['auth_user'].start ();
	});},
	get start () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target = $ (self.target_selector);
		$ (document).off ('click.main_container').on ('click.main_container', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._close_on_click_out (event);
		}));
		self.auth_user = window.PhanterPWA.get_auth_user ();
		self.authorization = window.PhanterPWA.get_authorization ();
		self.AlertActivationAccount.close ();
		if (self.auth_user !== null && self.auth_user !== undefined && self.authorization !== null && self.authorization !== undefined) {
			self.AlertActivationAccount.check_activation ();
			var first_name = '';
			var last_name = '';
			var role = I18N ('User');
			var user_image = window.PhanterPWA.get_auth_user_image ();
			if (self.auth_user !== null && self.auth_user !== undefined) {
				var first_name = self.auth_user.first_name;
				var last_name = self.auth_user.last_name;
				var role = I18N (self.auth_user.role);
			}
			self.xml_button_login = DIV (DIV (DIV (DIV (IMG (__kwargtrans__ ({_id: 'url_image_user', _src: user_image, _alt: 'user avatar'})), __kwargtrans__ ({_class: 'cmp-bar_user-img'})), __kwargtrans__ ({_class: 'cmp-bar_user-img-container'})), DIV (DIV (DIV ('{0} {1}'.format (first_name, last_name), __kwargtrans__ ({_id: 'user_first_and_last_name_login', _class: 'cmp-bar_user-name'})), DIV (role, __kwargtrans__ ({_id: 'user_role_login', _class: 'cmp-bar_user-role'})), __kwargtrans__ ({_class: 'cmp-bar_user-name-role'})), __kwargtrans__ ({_class: 'cmp-bar_user-name-role-container'})), DIV (DIV (DIV (__kwargtrans__ ({_class: 'led'})), __kwargtrans__ ({_class: 'cmd-bar_user-expands'})), __kwargtrans__ ({_class: 'cmd-bar_user-expand-container'})), __kwargtrans__ ({_class: 'cmp-bar_user-info-container'})), __kwargtrans__ ({_id: 'toggle-cmp-bar_user', _class: 'cmp-bar_user-container black link wave_on_click waves-phanterpwa'}));
			self.xml_button_login_options = CONCATENATE (DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-user-circle'})), I18N ('Profile', __kwargtrans__ (dict ({'_pt-br': 'Perfil'}))), __kwargtrans__ (dict ({'_phanterpwa-way': 'profile', '_class': 'option-label-menu'}))), __kwargtrans__ ({_id: 'component-auth_user-option-profile', _class: 'component-auth_user-option link wave_on_click waves-phanterpwa'})), DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-unlock'})), I18N ('Lock', __kwargtrans__ (dict ({'_pt-br': 'Bloquear'}))), __kwargtrans__ (dict ({'_phanterpwa-way': 'lock', '_class': 'option-label-menu'}))), __kwargtrans__ ({_id: 'component-auth_user-option-lock', _class: 'component-auth_user-option link wave_on_click waves-phanterpwa'})), DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-power-off'})), I18N ('Logout', __kwargtrans__ (dict ({'_pt-br': 'Sair'}))), __kwargtrans__ ({_class: 'option-label-menu'})), __kwargtrans__ ({_id: 'component-auth_user-option-logout', _class: 'component-auth_user-option link wave_on_click waves-phanterpwa'})));
			self.xml_button_login.html_to (self.element_target.find ('.phanterpwa-component-auth_user-button-toggle'));
			self.xml_button_login_options.html_to (self.element_target.find ('.phanterpwa-component-auth_user-button-toggle-options'));
			self.element_target.find ('#component-auth_user-option-logout').off ('click.auth_user-option-logout').on ('click.auth_user-option-logout', (function __lambda__ () {
				if (arguments.length) {
					var __ilastarg0__ = arguments.length - 1;
					if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
						var __allkwargs0__ = arguments [__ilastarg0__--];
						for (var __attrib0__ in __allkwargs0__) {
						}
					}
				}
				else {
				}
				return self.logout ();
			}));
		}
		else {
			self.xml_button_no_login = DIV (SPAN (DIV (DIV (DIV (__kwargtrans__ ({_class: 'led'})), __kwargtrans__ ({_class: 'phanterpwa-component-auth_user-nologin-led'})), DIV (I18N ('START'), __kwargtrans__ ({_class: 'phanterpwa-component-auth_user-nologin-start'})), __kwargtrans__ ({_class: 'phanterpwa-component-auth_user-nologin-led_and_start'})), __kwargtrans__ ({_class: 'phanterpwa-component-auth_user-nologin-led_and_start-wrapper'})), __kwargtrans__ ({_class: 'phanterpwa-component-auth_user-nologin-wrapper link wave_on_click'}));
			self.xml_button_no_login_options = CONCATENATE (DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-power-off'})), I18N ('Login', __kwargtrans__ (dict ({'_pt-br': 'Login'}))), __kwargtrans__ ({_class: 'option-label-menu'})), __kwargtrans__ ({_id: 'component-auth_user-option-login', _class: 'component-auth_user-option link wave_on_click waves-phanterpwa'})), DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-user-plus'})), I18N ('Create an account', __kwargtrans__ (dict ({'_pt-br': 'Criar uma conta'}))), __kwargtrans__ ({_class: 'option-label-menu'})), __kwargtrans__ ({_id: 'component-auth_user-option-register', _class: 'component-auth_user-option link wave_on_click waves-phanterpwa'})), DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-lock'})), I18N ('Recover password', __kwargtrans__ (dict ({'_pt-br': 'Esqueci a senha'}))), __kwargtrans__ ({_class: 'option-label-menu'})), __kwargtrans__ ({_id: 'component-auth_user-option-request_password', _class: 'component-auth_user-option link wave_on_click waves-phanterpwa'})));
			self.xml_button_no_login.html_to (self.element_target.find ('.phanterpwa-component-auth_user-button-toggle'));
			self.xml_button_no_login_options.html_to (self.element_target.find ('.phanterpwa-component-auth_user-button-toggle-options'));
			self.element_target.find ('#component-auth_user-option-login').off ('click.component-auth_user-option-login').on ('click.component-auth_user-option-login', self.modal_login);
			self.element_target.find ('#component-auth_user-option-register').off ('click.component-auth_user-option-register').on ('click.component-auth_user-option-register', self.modal_register);
			self.element_target.find ('#component-auth_user-option-request_password').off ('click.component-auth_user-option-request_password').on ('click.component-auth_user-option-request_password', self.modal_request_password);
		}
		self.element_target.find ('.component-auth_user-option').off ('click.close_on_click').on ('click.close_on_click', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.close_menu ();
		}));
		self.bind_menu_button ();
	});}
});
export var ModalLogin =  __class__ ('ModalLogin', [modal.Modal], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, target_element) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'target_element': var target_element = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		self.element_target = $ (target_element);
		self._social_logins = parameters.py_get ('social_logins', []);
		if (!(isinstance (self._social_logins, list))) {
			self._social_logins = [];
		}
		self._has_social_logins = (len (self._social_logins) > 0 ? true : false);
		var AuthUserCmp = window.PhanterPWA.Components ['auth_user'];
		self.AuthUser = null;
		if (AuthUserCmp !== null && AuthUserCmp !== undefined && !(isinstance (AuthUserCmp, AuthUser))) {
			console.error ('Need AuthUser instance on window.PhanterPWA.Components');
		}
		else {
			self.AuthUser = AuthUserCmp;
		}
		self.last_auth_user = window.PhanterPWA.get_last_auth_user ();
		var first_name = '';
		var last_name = '';
		var email = '';
		var role = I18N ('User');
		var user_image = window.PhanterPWA.get_last_auth_user_image ();
		var remember_me = false;
		if (self.last_auth_user !== null && self.last_auth_user !== undefined) {
			var first_name = self.last_auth_user.first_name;
			var last_name = self.last_auth_user.last_name;
			var email = self.last_auth_user.email;
			var remember_me = self.last_auth_user.remember_me;
			var role = I18N (self.last_auth_user.role);
		}
		self.xml_social_logins = DIV (__kwargtrans__ ({_class: 'phanterpwa-modal-login-social-buttons-container'}));
		self._icons_social_login = dict ({});
		if (self._has_social_logins) {
			for (var x of self._social_logins) {
				var icon = '';
				var social_name = x;
				if (isinstance (x, list) && len (x) == 2) {
					var icon = x [1];
					var social_name = x [0];
					self._icons_social_login [social_name] = icon;
				}
				self.xml_social_logins.append (DIV (DIV (icon, I18N ('Login with {0}'.format (str (social_name).capitalize ()), __kwargtrans__ (dict ({'_pt-br': 'Login com o {0}'.format (str (social_name).capitalize ())}))), __kwargtrans__ (dict ({'_class': 'btn btn-social_login link', '_data-social_login': social_name}))), __kwargtrans__ ({_class: 'btn-social_login-wrapper'})));
			}
		}
		var tcontent = DIV (self.xml_social_logins, DIV (DIV (DIV (DIV (IMG (__kwargtrans__ ({_src: user_image, _id: 'form-login-image-user-url'})), __kwargtrans__ ({_class: 'form-image-user-img'})), __kwargtrans__ ({_class: 'form-image-user-img-container'})), DIV (DIV ('{0} {1}'.format (first_name, last_name), __kwargtrans__ ({_id: 'form-login-profile-user-name', _class: 'form-profile-user-name'})), DIV (role, __kwargtrans__ ({_id: 'form-login-profile-user-role', _class: 'form-profile-user-role'})), __kwargtrans__ ({_class: 'form-profile-user-info'})), __kwargtrans__ ({_class: 'form-profile-container'})), __kwargtrans__ ({_id: 'form-login-image-user-container', _class: 'form-image-user-container'})), DIV (DIV (forms.FormButton ('form-login-button-other-user', I18N ('Other account', __kwargtrans__ (dict ({'_pt-br': 'Outra Conta'}))), __kwargtrans__ ({_class: 'wave_on_click waves-phanterpwa btn-s'})), __kwargtrans__ ({_class: 'buttons-form-container'})), __kwargtrans__ ({_id: 'form-login-button-other-user-container', _class: 'p-col w1p100'})), forms.FormWidget ('login', 'email', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('E-mail'), 'value': email, 'validators': ['IS_NOT_EMPTY', 'IS_EMAIL']}))), DIV (forms.FormWidget ('login', 'password', __kwargtrans__ (dict ({'label': I18N ('Password', __kwargtrans__ (dict ({'_pt-br': 'Senha'}))), 'type': 'password', 'validators': ['IS_NOT_EMPTY']}))), __kwargtrans__ ({_class: 'p-col w1p100'})), DIV (forms.FormWidget ('login', 'remember_me', __kwargtrans__ (dict ({'value': remember_me, 'label': I18N ('Remember-me', __kwargtrans__ (dict ({'_pt-br': 'Lembre-me'}))), 'type': 'boolean'}))), __kwargtrans__ ({_class: 'input-field p-col w1p100'})), __kwargtrans__ ({_class: 'phanterpwa-auth_user-form-inputs'})).jquery ();
		if (self._has_social_logins) {
			tcontent.addClass ('has_social_logins');
		}
		var button_login_by_social = '';
		if (self.last_auth_user !== null && self.last_auth_user !== undefined) {
			tcontent.addClass ('has_auth_user');
			if (self.last_auth_user ['social_login'] !== null && self.last_auth_user ['social_login'] !== undefined) {
				var icon = self._icons_social_login.py_get (self.last_auth_user ['social_login'], '');
				tcontent.addClass ('auth_user_logged_by_social_login');
				var current_social_name = self.last_auth_user ['social_login'];
				var button_login_by_social = forms.FormButton ('social_login-{0}'.format (current_social_name), CONCATENATE (icon, I18N ('Continue using {0}'.format (str (current_social_name).capitalize ()), __kwargtrans__ (dict ({'_pt-br': 'Continuar com {0}'.format (str (current_social_name).capitalize ())})))), __kwargtrans__ (dict ({'_class': 'btn-social_login wave_on_click waves-phanterpwa', '_data-social_login': current_social_name})));
			}
		}
		var tfooter = DIV (forms.CaptchaContainer ('login', preloaders.android), DIV (DIV (forms.SubmitButton ('login', I18N ('Login', __kwargtrans__ (dict ({'_pt-br': 'Login'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), __kwargtrans__ ({_class: 'hidden_on_its_social_login'})), DIV (button_login_by_social, __kwargtrans__ ({_class: 'hidden_on_not_has_auth_user'})), forms.FormButton ('register', I18N ('Create an account', __kwargtrans__ (dict ({'_pt-br': 'Criar uma conta'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), forms.FormButton ('password', I18N ('Recover password', __kwargtrans__ (dict ({'_pt-br': 'Esqueci a senha'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), __kwargtrans__ ({_class: 'phanterpwa-form-buttons-container'})), __kwargtrans__ ({_class: 'p-col w1p100'})).jquery ();
		if (self.last_auth_user !== null && self.last_auth_user !== undefined) {
			tfooter.addClass ('has_auth_user');
			if (self.last_auth_user ['social_login'] !== null && self.last_auth_user ['social_login'] !== undefined) {
				tfooter.addClass ('its_social_login');
			}
		}
		modal.Modal.__init__ (self, self.element_target, __kwargtrans__ (dict ({'_phanterpwa-form': 'login', '_id': 'form-login', 'header_height': 50, 'footer_height': 200, 'title': I18N ('Login'), 'content': tcontent, 'footer': tfooter, 'after_open': self.binds})));
	});},
	get other_account () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target.find ('.phanterpwa-auth_user-form-inputs').removeClass ('has_auth_user');
		self.element_target.find ('.phanterpwa-component-modal-footer-container').find ('.has_auth_user').removeClass ('has_auth_user');
	});},
	get open_modal_register () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close ();
		window.PhanterPWA.Components ['auth_user'].modal_register ();
	});},
	get open_modal_request_password () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close ();
		window.PhanterPWA.Components ['auth_user'].modal_request_password ();
	});},
	get binds () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target.find ('#phanterpwa-widget-form-submit_button-login').off ('click.modal_submit_login').on ('click.modal_submit_login', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.submit ();
		}));
		self.element_target.find ('#phanterpwa-widget-form-form_button-form-login-button-other-user').off ('click.other_account_button').on ('click.other_account_button', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.other_account ();
		}));
		self.element_target.find ('#phanterpwa-widget-form-form_button-register').off ('click.form_button_register').on ('click.form_button_register', self.open_modal_register);
		self.element_target.find ('#phanterpwa-widget-form-form_button-password').off ('click.form_button_request_password').on ('click.form_button_request_password', self.open_modal_request_password);
		self.element_target.find ('.btn-social_login').off ('click.social_button').on ('click.social_button', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self._on_click_social_button (this);
		}));
	});},
	get _on_click_social_button () {return __get__ (this, function (self, el) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'el': var el = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var social = $ (el).data ('social_login');
		window.PhanterPWA.social_login (social);
	});},
	get clear_errors () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		$ ('#form-{0}'.format (self._form)).find ('.phanterpwa-widget-error').removeClass ('enabled').html ('');
	});},
	get after_submit () {return __get__ (this, function (self, data, ajax_status) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (ajax_status == 'success') {
			var json = data.responseJSON;
			self.close ();
			if (data.status == 200) {
				if (self.AuthUser !== null && self.AuthUser !== undefined) {
					self.AuthUser.start ();
					self.AuthUser.AlertActivationAccount.check_activation ();
					if (json.used_temporary !== null && json.used_temporary !== undefined) {
						if (window.PhanterPWA.DEBUG) {
							console.error (json.used_temporary);
						}
						self.AuthUser.modal_change_password (__kwargtrans__ ({temporary_password: json.used_temporary}));
					}
				}
				window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
				var LeftBar = window.PhanterPWA.Components ['left_bar'];
				if (LeftBar !== null && LeftBar !== undefined) {
					LeftBar.reload ();
				}
			}
			else if (data.status == 206) {
				window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
				window.PhanterPWA.open_way ('two_factor/{0}'.format (json.authorization_url));
			}
		}
		else if (data.status == 400) {
			var json = data.responseJSON;
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
			forms.SignForm ('#form-login', __kwargtrans__ ({has_captcha: true}));
			var errors = dict (json ['errors']);
			if (errors !== undefined) {
				for (var x of errors.py_keys ()) {
					var id_error = '#phanterpwa-widget-login-{0} .phanterpwa-widget-error'.format (x);
					var message = SPAN (errors [x]).xml ();
					$ ('#form-{0}'.format (self._form)).find (id_error).html (message).addClass ('enabled');
				}
			}
		}
	});},
	get submit () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.clear_errors ();
		window.PhanterPWA.login ($ ('#phanterpwa-widget-input-input-login-csrf_token').val (), $ ('#phanterpwa-widget-input-input-login-email').val (), $ ('#phanterpwa-widget-input-input-login-password').val (), $ ('#phanterpwa-widget-checkbox-input-login-remember_me').prop ('checked'), __kwargtrans__ ({callback: self.after_submit}));
	});}
});
export var ModalPersonalInformation =  __class__ ('ModalPersonalInformation', [modal.Modal], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, target_element) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'target_element': var target_element = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		self.element_target = $ (target_element);
		self.auth_user = window.PhanterPWA.get_last_auth_user ();
		var first_name = '';
		var last_name = '';
		var email = '';
		if (self.auth_user !== null && self.auth_user !== undefined) {
			var first_name = self.auth_user.first_name;
			var last_name = self.auth_user.last_name;
			var email = self.auth_user.email;
		}
		var tcontent = DIV (DIV (DIV (DIV (forms.FormWidget ('change_account', 'first_name', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('First Name'), 'value': first_name, 'validators': ['IS_NOT_EMPTY'], '_class': 'p-col w1p100 w3p50'}))), forms.FormWidget ('change_account', 'last_name', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('Last Name'), 'value': last_name, 'validators': ['IS_NOT_EMPTY'], '_class': 'p-col w1p100 w3p50'}))), forms.FormWidget ('change_account', 'email', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('E-Mail'), 'value': email, 'validators': ['IS_EMAIL'], '_class': 'p-col w1p100'}))), __kwargtrans__ ({_class: 'p-row change_account_inputs_container'})), __kwargtrans__ ({_class: 'p-col w1p100'}))), __kwargtrans__ ({_class: 'phanterpwa-change_account-form-inputs p-row'})).jquery ();
		if (self.auth_user !== null && self.auth_user !== undefined) {
			tcontent.addClass ('has_auth_user');
		}
		var tfooter = DIV (DIV (forms.SubmitButton ('change_account', I18N ('Save Changes', __kwargtrans__ (dict ({'_pt-br': 'Salvar Mudanças'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), __kwargtrans__ ({_class: 'phanterpwa-form-buttons-container'})), __kwargtrans__ ({_class: 'p-col w1p100'})).jquery ();
		modal.Modal.__init__ (self, self.element_target, __kwargtrans__ (dict ({'_phanterpwa-form': 'change_account', '_id': 'form-change_account', 'header_height': 50, 'title': I18N ('Personal Information', __kwargtrans__ (dict ({'_pt-br': 'Informações Pessoais'}))), 'content': tcontent, 'footer': tfooter, 'after_open': self.binds})));
	});},
	get after_submit () {return __get__ (this, function (self, data, ajax_status) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (ajax_status == 'success') {
			var json = data.responseJSON;
			var message = json.i18n.message;
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': message})));
			if (data.status == 200) {
				$ ('.phanterpwa-gallery-upload-input-file').val ('');
				var auth_user = json.auth_user;
				window.PhanterPWA.update_auth_user (auth_user);
				self.reload ();
			}
		}
		else {
			forms.SignForm ('#form-change_account');
			var json = data.responseJSON;
			var message = json.i18n.message;
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': message})));
		}
	});},
	get submit () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var formdata = new FormData ($ ('#form-change_account') [0]);
		window.PhanterPWA.ApiServer.PUT (__kwargtrans__ (dict ({'url_args': ['api', 'auth', 'change'], 'form_data': formdata, 'onComplete': self.after_submit})));
	});},
	get binds () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		forms.ValidateForm ('#form-change_account');
		$ ('#phanterpwa-widget-form-submit_button-change_account').off ('click.profile_button_save').on ('click.profile_button_save', self.submit);
	});}
});
export var ModalRegister =  __class__ ('ModalRegister', [modal.Modal], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, target_element) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'target_element': var target_element = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target = $ (target_element);
		var AuthUserCmp = window.PhanterPWA.Components ['auth_user'];
		self.AuthUser = null;
		if (AuthUserCmp !== null && AuthUserCmp !== undefined && !(isinstance (AuthUserCmp, AuthUser))) {
			console.error ('Need AuthUser instance on window.PhanterPWA.Components');
		}
		else {
			self.AuthUser = AuthUserCmp;
		}
		var tcontent = DIV (forms.FormWidget ('register', 'first_name', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('First Name'), 'validators': ['IS_NOT_EMPTY'], '_class': 'p-col w1p100 w3p50'}))), forms.FormWidget ('register', 'last_name', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('Last Name'), 'validators': ['IS_NOT_EMPTY'], '_class': 'p-col w1p100 w3p50'}))), forms.FormWidget ('register', 'email', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('E-Mail'), 'validators': ['IS_EMAIL'], '_class': 'p-col w1p100'}))), forms.FormWidget ('register', 'password', __kwargtrans__ (dict ({'type': 'password', 'label': I18N ('Password'), 'validators': ['IS_NOT_EMPTY', 'IS_EQUALS:#phanterpwa-widget-input-input-register-password_repeat'], '_class': 'p-col w1p100 w3p50'}))), forms.FormWidget ('register', 'password_repeat', __kwargtrans__ (dict ({'type': 'password', 'label': I18N ('Repeat Password'), 'validators': ['IS_NOT_EMPTY', 'IS_EQUALS:#phanterpwa-widget-input-input-register-password'], '_class': 'p-col w1p100 w3p50'}))), __kwargtrans__ ({_class: 'phanterpwa-register-form-inputs p-row'})).jquery ();
		if (self.auth_user !== null && self.auth_user !== undefined) {
			tcontent.addClass ('has_auth_user');
		}
		var tfooter = DIV (forms.CaptchaContainer ('register', preloaders.android), DIV (forms.SubmitButton ('register', I18N ('Create', __kwargtrans__ (dict ({'_pt-br': 'Criar'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), forms.FormButton ('login', I18N ('Login', __kwargtrans__ (dict ({'_pt-br': 'Login'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), forms.FormButton ('password', I18N ('Recover password', __kwargtrans__ (dict ({'_pt-br': 'Esqueci a senha'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), __kwargtrans__ ({_class: 'phanterpwa-form-buttons-container'})), __kwargtrans__ ({_class: 'p-col w1p100'})).jquery ();
		modal.Modal.__init__ (self, self.element_target, __kwargtrans__ (dict ({'_phanterpwa-form': 'register', '_id': 'form-register', 'header_height': 50, 'footer_height': 200, 'title': I18N ('Register', __kwargtrans__ (dict ({'_pt-br': 'Registrar'}))), 'content': tcontent, 'footer': tfooter, 'after_open': self.binds})));
	});},
	get open_modal_login () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close ();
		window.PhanterPWA.Components ['auth_user'].modal_login ();
	});},
	get open_modal_request_password () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close ();
		window.PhanterPWA.Components ['auth_user'].modal_request_password ();
	});},
	get binds () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target = $ (self.target_selector);
		self.element_target.find ('#phanterpwa-widget-form-form_button-login').off ('click.form_button_login').on ('click.form_button_login', self.open_modal_login);
		self.element_target.find ('#phanterpwa-widget-form-form_button-password').off ('click.form_button_request_password').on ('click.form_button_request_password', self.open_modal_request_password);
		self.element_target.find ('#phanterpwa-widget-form-submit_button-register').off ('click.modal_submit_register').on ('click.modal_submit_register', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.submit ();
		}));
	});},
	get clear_errors () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		$ ('#form-{0}'.format (self._form)).find ('.phanterpwa-widget-error').removeClass ('enabled').html ('');
	});},
	get after_submit () {return __get__ (this, function (self, data, ajax_status) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (ajax_status == 'success') {
			var json = data.responseJSON;
			if (self.AuthUser !== null && self.AuthUser !== undefined) {
				self.AuthUser.start ();
			}
			self.close ();
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
			var LeftBar = window.PhanterPWA.Components ['left_bar'];
			if (LeftBar !== null && LeftBar !== undefined) {
				LeftBar.reload ();
			}
		}
		else if (data.status == 400) {
			var json = data.responseJSON;
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
			forms.SignForm ('#form-register', __kwargtrans__ ({has_captcha: true}));
			var errors = dict (json ['errors']);
			if (errors !== undefined) {
				for (var x of errors.py_keys ()) {
					var id_error = '#phanterpwa-widget-register-{0} .phanterpwa-widget-error'.format (x);
					var message = SPAN (errors [x]).xml ();
					$ ('#form-{0}'.format (self._form)).find (id_error).html (message).addClass ('enabled');
				}
			}
		}
	});},
	get submit () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.clear_errors ();
		window.PhanterPWA.register ($ ('#phanterpwa-widget-input-input-register-csrf_token').val (), $ ('#phanterpwa-widget-input-input-register-first_name').val (), $ ('#phanterpwa-widget-input-input-register-last_name').val (), $ ('#phanterpwa-widget-input-input-register-email').val (), $ ('#phanterpwa-widget-input-input-register-password').val (), $ ('#phanterpwa-widget-input-input-register-password_repeat').val (), __kwargtrans__ ({callback: self.after_submit}));
	});}
});
export var ModalRequestPassword =  __class__ ('ModalRequestPassword', [modal.Modal], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, target_element) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'target_element': var target_element = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target = $ (target_element);
		var AuthUserCmp = window.PhanterPWA.Components ['auth_user'];
		self.AuthUser = null;
		if (AuthUserCmp !== null && AuthUserCmp !== undefined && !(isinstance (AuthUserCmp, AuthUser))) {
			console.error ('Need AuthUser instance on window.PhanterPWA.Components');
		}
		else {
			self.AuthUser = AuthUserCmp;
		}
		var widget_email = forms.FormWidget ('request_password', 'email', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('E-Mail'), 'validators': ['IS_EMAIL'], '_class': 'p-col w1p100'})));
		var last_auth_user = window.PhanterPWA.get_last_auth_user ();
		if (last_auth_user !== null) {
			var widget_email = forms.FormWidget ('request_password', 'email', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('E-Mail'), 'validators': ['IS_EMAIL'], 'value': last_auth_user.email, '_class': 'p-col w1p100'})));
		}
		var tcontent = DIV (widget_email, __kwargtrans__ ({_class: 'phanterpwa-request_password-form-inputs p-row'})).jquery ();
		if (self.auth_user !== null && self.auth_user !== undefined) {
			tcontent.addClass ('has_auth_user');
		}
		var tfooter = DIV (forms.CaptchaContainer ('request_password', preloaders.android), DIV (forms.SubmitButton ('request_password', I18N ('Recover', __kwargtrans__ (dict ({'_pt-br': 'Recuperar'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), forms.FormButton ('register', I18N ('Create an Account', __kwargtrans__ (dict ({'_pt-br': 'Criar uma Conta'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), forms.FormButton ('login', I18N ('Login', __kwargtrans__ (dict ({'_pt-br': 'Login'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), __kwargtrans__ ({_class: 'phanterpwa-form-buttons-container'})), __kwargtrans__ ({_class: 'p-col w1p100'})).jquery ();
		modal.Modal.__init__ (self, self.element_target, __kwargtrans__ (dict ({'_phanterpwa-form': 'request_password', '_id': 'form-request_password', 'header_height': 50, 'footer_height': 200, 'title': I18N ('Recover Password', __kwargtrans__ (dict ({'_pt-br': 'Recuperar Senha'}))), 'content': tcontent, 'footer': tfooter, 'after_open': self.binds})));
	});},
	get open_modal_login () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close ();
		window.PhanterPWA.Components ['auth_user'].modal_login ();
	});},
	get open_modal_register () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close ();
		window.PhanterPWA.Components ['auth_user'].modal_register ();
	});},
	get binds () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target.find ('#phanterpwa-widget-form-submit_button-request_password').off ('click.modal_submit_request').on ('click.modal_submit_request', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.submit ();
		}));
		self.element_target.find ('#phanterpwa-widget-form-form_button-register').off ('click.form_button_register').on ('click.form_button_register', self.open_modal_register);
		self.element_target.find ('#phanterpwa-widget-form-form_button-login').off ('click.form_button_login').on ('click.form_button_login', self.open_modal_login);
	});},
	get clear_errors () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		$ ('#form-{0}'.format (self._form)).find ('.phanterpwa-widget-error').removeClass ('enabled').html ('');
	});},
	get after_submit () {return __get__ (this, function (self, data, ajax_status) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (ajax_status == 'success') {
			var json = data.responseJSON;
			self.close ();
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
			var LeftBar = window.PhanterPWA.Components ['left_bar'];
			if (LeftBar !== null && LeftBar !== undefined) {
				LeftBar.reload ();
			}
		}
		else if (data.status == 400) {
			var json = data.responseJSON;
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
			forms.SignForm ('#form-request_password', __kwargtrans__ ({has_captcha: true}));
			var errors = dict (json ['errors']);
			if (errors !== undefined) {
				for (var x of errors.py_keys ()) {
					var id_error = '#phanterpwa-widget-request_password-{0} .phanterpwa-widget-error'.format (x);
					var message = SPAN (errors [x]).xml ();
					$ ('#form-{0}'.format (self._form)).find (id_error).html (message).addClass ('enabled');
				}
			}
		}
	});},
	get submit () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.clear_errors ();
		window.PhanterPWA.request_password ($ ('#phanterpwa-widget-input-input-request_password-csrf_token').val (), $ ('#phanterpwa-widget-input-input-request_password-email').val (), __kwargtrans__ ({callback: self.after_submit}));
	});}
});
export var AlertActivationAccount =  __class__ ('AlertActivationAccount', [top_slide.TopSlide], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, target_element) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'target_element': var target_element = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var content = DIV (__kwargtrans__ ({_id: 'phanterpwa-top-slide-auth_user-activation-container', _class: 'phanterpwa-auth_user-activation-container'}));
		var parameters = dict (__kwargtrans__ ({after_open: self.binds}));
		top_slide.TopSlide.__init__ (self, target_element, content, __kwargtrans__ (parameters));
	});},
	get binds () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self._process_alert_content ();
		forms.SignForm ('#form-activation');
		forms.ValidateForm ('#form-activation');
		self.element_target = $ (self.target_selector);
		self.element_target.find ('#phanterpwa-widget-form-submit_button-activation').off ('click.modal_submit_activation').on ('click.modal_submit_activation', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.submit ();
		}));
		self.element_target.find ('#phanterpwa-widget-form-form_button-activation_new_code').off ('click.modal_submit_activation_new_code').on ('click.modal_submit_activation_new_code', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.request_new_activation_code_to_send_to_email ();
		}));
	});},
	get _process_alert_content () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var html = CONCATENATE (DIV (I18N ('{0}{1}{2}'.format ('Your account has not yet been activated,', ' when you created it, the activation code was sent to', ' the registered email address. Check your email and add', ' the code in the field below.'), __kwargtrans__ (dict ({'_pt-br': '{0}{1}{2}'.format ('Sua conta ainda não foi ativada, ao criá-la foi enviado', ' ao email cadastrado o código de ativação. Check seu ', 'email e adicione o código no campo abaixo.')}))), __kwargtrans__ ({_class: 'phanterpwa-auth_user-activation-text'})), FORM (DIV (DIV (forms.FormWidget ('activation', 'activation_code', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('Activation Code', __kwargtrans__ (dict ({'_pt-br': 'Código de Ativação'}))), 'validators': ['IS_NOT_EMPTY', 'IS_ACTIVATION_CODE']}))), __kwargtrans__ ({_class: 'phanterpwa-auth_user-activation-action-input'})), DIV (forms.SubmitButton ('activation', I18N ('Activate', __kwargtrans__ (dict ({'_pt-br': 'Ativar'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), forms.FormButton ('activation_new_code', I18N ('Request Activation Code', __kwargtrans__ (dict ({'_pt-br': 'Requisitar novo código'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), __kwargtrans__ ({_class: 'phanterpwa-form-buttons-container'})), __kwargtrans__ ({_class: 'phanterpwa-auth_user-activation-actions-activate'})), __kwargtrans__ (dict ({'_class': 'phanterpwa-auth_user-activation-actions-container', '_phanterpwa-form': 'activation', '_id': 'form-activation'}))));
		html.html_to ('#phanterpwa-top-slide-auth_user-activation-container');
	});},
	get after_activation_code_send () {return __get__ (this, function (self, data, ajax_status) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (ajax_status == 'success') {
			var json = data.responseJSON;
			var message = json.i18n.message;
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': message})));
		}
		else if (data.status == 400) {
			var json = data.responseJSON;
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
			forms.SignForm ('#form-activation', __kwargtrans__ ({has_captcha: true}));
			var errors = dict (json ['errors']);
			if (errors !== undefined) {
				for (var x of errors.py_keys ()) {
					var id_error = '#phanterpwa-widget-activation-{0} .phanterpwa-widget-error'.format (x);
					var message = SPAN (errors [x]).xml ();
					self.element_target.find (id_error).html (message).addClass ('enabled');
				}
			}
		}
	});},
	get request_new_activation_code_to_send_to_email () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		window.PhanterPWA.ApiServer.GET (__kwargtrans__ (dict ({'url_args': ['api', 'auth', 'active-account'], 'onComplete': self.after_activation_code_send})));
	});},
	get clear_errors () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target = $ (self.target_selector);
		self.element_target.find ('.phanterpwa-widget-error').removeClass ('enabled').html ('');
	});},
	get after_submit () {return __get__ (this, function (self, data, ajax_status) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (ajax_status == 'success') {
			var json = data.responseJSON;
			self.close ();
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
		}
		else if (data.status == 400) {
			var json = data.responseJSON;
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
			forms.SignForm ('#form-activation');
			var errors = dict (json ['errors']);
			if (errors !== undefined) {
				for (var x of errors.py_keys ()) {
					var id_error = '#phanterpwa-widget-activation-{0} .phanterpwa-widget-error'.format (x);
					var message = SPAN (errors [x]).xml ();
					$ ('#form-{0}'.format (self._form)).find (id_error).html (message).addClass ('enabled');
				}
			}
		}
	});},
	get submit () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target = $ (self.target_selector);
		self.clear_errors ();
		window.PhanterPWA.activation_account (self.element_target.find ('#phanterpwa-widget-input-input-activation-csrf_token').val (), self.element_target.find ('#phanterpwa-widget-input-input-activation-activation_code').val (), __kwargtrans__ ({callback: self.after_submit}));
	});},
	get check_activation () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var auth_user = window.PhanterPWA.get_auth_user ();
		if (auth_user !== null) {
			if (!(auth_user.activated)) {
				if (window.PhanterPWA.DEBUG) {
					console.info ('cheking', auth_user);
				}
				self.open ();
			}
		}
	});}
});
export var ModalChangePassword =  __class__ ('ModalChangePassword', [modal.Modal], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, target_selector) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'target_selector': var target_selector = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		self.target_selector = target_selector;
		self.element_target = $ (self.target_selector);
		var AuthUserCmp = window.PhanterPWA.Components ['auth_user'];
		self.AuthUser = null;
		if (AuthUserCmp !== null && AuthUserCmp !== undefined && !(isinstance (AuthUserCmp, AuthUser))) {
			console.error ('Need AuthUser instance on window.PhanterPWA.Components');
		}
		else {
			self.AuthUser = AuthUserCmp;
		}
		var widget_password = forms.FormWidget ('change_password', 'password', __kwargtrans__ (dict ({'type': 'password', 'label': I18N ('Current Password'), 'validators': ['IS_NOT_EMPTY'], '_class': 'p-col w1p100'})));
		if (__in__ ('temporary_password', parameters)) {
			if (parameters ['temporary_password'] !== null && parameters ['temporary_password'] !== undefined) {
				var widget_password = forms.FormWidget ('change_password', 'password', __kwargtrans__ (dict ({'type': 'password', 'label': I18N ('Current Password'), 'validators': ['IS_NOT_EMPTY'], 'value': parameters ['temporary_password'], '_class': 'p-col w1p100', '_style': 'display: none;'})));
			}
		}
		var tcontent = DIV (widget_password, forms.FormWidget ('change_password', 'new_password', __kwargtrans__ (dict ({'type': 'password', 'label': I18N ('New password'), 'validators': ['IS_NOT_EMPTY', 'IS_EQUALS:#phanterpwa-widget-input-input-change_password-new_password_repeat'], '_class': 'p-col w1p100'}))), forms.FormWidget ('change_password', 'new_password_repeat', __kwargtrans__ (dict ({'type': 'password', 'label': I18N ('Password Repeat'), 'validators': ['IS_NOT_EMPTY', 'IS_EQUALS:#phanterpwa-widget-input-input-change_password-new_password'], '_class': 'p-col w1p100'}))), __kwargtrans__ ({_class: 'phanterpwa-change_password-form-inputs p-row'})).jquery ();
		if (self.auth_user !== null && self.auth_user !== undefined) {
			tcontent.addClass ('has_auth_user');
		}
		var tfooter = DIV (DIV (forms.SubmitButton ('change_password', I18N ('Change password', __kwargtrans__ (dict ({'_pt-br': 'Mudar a senha'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), __kwargtrans__ ({_class: 'phanterpwa-form-buttons-container'})), __kwargtrans__ ({_class: 'p-col w1p100'})).jquery ();
		modal.Modal.__init__ (self, self.element_target, __kwargtrans__ (dict ({'_phanterpwa-form': 'change_password', '_id': 'form-change_password', 'header_height': 50, 'title': I18N ('Change Password'), 'content': tcontent, 'footer': tfooter, 'after_open': self.binds})));
	});},
	get binds () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target = $ (self.target_selector);
		self.element_target.find ('#phanterpwa-widget-form-submit_button-change_password').off ('click.modal_submit_request').on ('click.modal_submit_request', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.submit ();
		}));
	});},
	get clear_errors () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		$ ('#form-{0}'.format (self._form)).find ('.phanterpwa-widget-error').removeClass ('enabled').html ('');
	});},
	get after_submit () {return __get__ (this, function (self, data, ajax_status) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (ajax_status == 'success') {
			var json = data.responseJSON;
			self.close ();
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
			var LeftBar = window.PhanterPWA.Components ['left_bar'];
			if (LeftBar !== null && LeftBar !== undefined) {
				LeftBar.reload ();
			}
		}
		else if (data.status == 400) {
			var json = data.responseJSON;
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
			forms.SignForm ('#form-change_password');
			var errors = dict (json ['errors']);
			if (errors !== undefined) {
				for (var x of errors.py_keys ()) {
					var id_error = '#phanterpwa-widget-change_password-{0} .phanterpwa-widget-error'.format (x);
					var message = SPAN (errors [x]).xml ();
					$ ('#form-{0}'.format (self._form)).find (id_error).html (message).addClass ('enabled');
				}
			}
		}
	});},
	get submit () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.clear_errors ();
		window.PhanterPWA.change_password ($ ('#phanterpwa-widget-input-input-change_password-csrf_token').val (), $ ('#phanterpwa-widget-input-input-change_password-password').val (), $ ('#phanterpwa-widget-input-input-change_password-new_password').val (), $ ('#phanterpwa-widget-input-input-change_password-new_password_repeat').val (), __kwargtrans__ ({callback: self.after_submit}));
	});}
});
export var LeftBarMainButton =  __class__ ('LeftBarMainButton', [left_bar.LeftBarMainButton], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, target_selector) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'target_selector': var target_selector = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		left_bar.LeftBarMainButton.__init__ (self, target_selector);
	});},
	get switch_leftbar () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_target = $ (self.target_selector);
		var el = self.element_target.find ('#phanterpwa-component-left_bar-main_button');
		if (el.hasClass ('enabled') && el.hasClass ('enabled_submenu')) {
			self.close_leftbar ();
		}
		else if (el.hasClass ('enabled_submenu')) {
			LeftBarAuthUserLogin._close_menu ();
			LeftBarAuthUserNoLogin._close_menu ();
			AuthUser._close_menu ();
			self.open_leftbar ();
		}
		else if (el.hasClass ('enabled')) {
			self.close_leftbar ();
		}
		else {
			self.open_leftbar ();
		}
	});},
	get _close () {return function () {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
				}
			}
		}
		else {
		}
		$ ('#phanterpwa-component-left_bar-main_button').removeClass ('enabled').removeClass ('enabled_submenu');
	};},
	get close_leftbar () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		AuthUser._close_menu ();
		self._close ();
		left_bar.LeftBar._close ();
	});},
	get _open () {return function () {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
				}
			}
		}
		else {
		}
		$ ('#phanterpwa-component-left_bar-main_button').addClass ('enabled');
	};},
	get open_leftbar () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self._open ();
		left_bar.LeftBar._open ();
	});}
});
export var LeftBar =  __class__ ('LeftBar', [left_bar.LeftBar], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, target_selector) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'target_selector': var target_selector = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		left_bar.LeftBar.__init__ (self, target_selector, __kwargtrans__ (parameters));
		self.add_button (LeftBarAuthUserLogin ());
		self.add_button (LeftBarAuthUserNoLogin ());
		self.add_button (left_bar.LeftBarButton ('home', I18N ('Home', __kwargtrans__ (dict ({'_pt-br': 'Principal'}))), I (__kwargtrans__ ({_class: 'fas fa-home'})), __kwargtrans__ (dict ({'_phanterpwa-way': 'home', 'position': 'top'}))));
	});}
});
export var LeftBarAuthUserLogin =  __class__ ('LeftBarAuthUserLogin', [left_bar.LeftBarUserMenu], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		left_bar.LeftBarUserMenu.__init__ (self);
		self.position = 'top';
		self.addSubmenu ('profile', I18N ('Profile', __kwargtrans__ (dict ({'_pt-br': 'Perfil'}))), __kwargtrans__ (dict ({'_class': 'command_user', '_phanterpwa-way': 'profile'})));
		self.addSubmenu ('lock', I18N ('Lock', __kwargtrans__ (dict ({'_pt-br': 'Bloquear'}))), __kwargtrans__ (dict ({'_phanterpwa-way': 'lock', '_class': 'command_user'})));
		self.addSubmenu ('logout', I18N ('Logout', __kwargtrans__ (dict ({'_pt-br': 'Sair'}))), __kwargtrans__ ({_class: 'command_user'}));
	});},
	get switch_menu () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var el = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-menu_button-{0}'.format (self.identifier)).parent ();
		if (el.hasClass ('enabled')) {
			self.close_menu ();
		}
		else {
			self.open_menu ();
		}
	});},
	get _open_menu () {return function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-menu_button-auth_user_login').parent ();
		element.addClass ('enabled');
		$ ('#phanterpwa-component-left_bar').addClass ('enabled_submenu');
		$ ('#phanterpwa-component-left_bar-main_button').addClass ('enabled_submenu');
	};},
	get open_menu () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		AuthUser._open_menu ();
		self._open_menu ();
	});},
	get _close_menu () {return function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-menu_button-auth_user_login').parent ();
		element.removeClass ('enabled');
		if ($ ('#phanterpwa-component-left_bar').find ('.phanterpwa-component-left_bar-menu_button-wrapper.enabled').length == 0) {
			$ ('#phanterpwa-component-left_bar').removeClass ('enabled_submenu');
			$ ('#phanterpwa-component-left_bar-main_button').removeClass ('enabled_submenu');
		}
	};},
	get close_menu () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		AuthUser._close_menu ();
		self._close_menu ();
	});},
	get logout () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		window.PhanterPWA.logout ();
		self.start ();
		window.PhanterPWA.logout ();
		var LeftBar = window.PhanterPWA.Components ['left_bar'];
		if (LeftBar !== null && LeftBar !== undefined) {
			LeftBar.reload ();
		}
		window.PhanterPWA.Components ['auth_user'].start ();
	});},
	get start () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-menu_button-{0}'.format (self.identifier));
		element.off ('click.open_leftbar_menu').on ('click.open_leftbar_menu', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.switch_menu (this);
		}));
		var sub_element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-submenu-from-{0} .phanterpwa-component-left_bar-submenu-button'.format (self.identifier));
		sub_element.off ('click.close_leftbar_submenu').on ('click.close_leftbar_submenu', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.close_menu ();
		}));
		self.auth_user = window.PhanterPWA.get_auth_user ();
		var user_name = 'Anonymous';
		var role = I18N ('User');
		var user_image = window.PhanterPWA.get_auth_user_image ();
		if (self.auth_user !== null) {
			var first_name = self.auth_user.first_name;
			var last_name = self.auth_user.last_name;
			var user_name = '{0} {1}'.format (first_name, last_name);
			var role = I18N (self.auth_user.role);
		}
		element.find ('#phanterpwa-component-left_bar-url-imagem-user').attr ('src', user_image);
		element.find ('#phanterpwa-component-left_bar-name-user').text (user_name);
		$ ('#phanterpwa-component-left_bar-submenu-button-logout').off ('click.left_bar_buton_logout').on ('click.left_bar_buton_logout', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.logout ();
		}));
	});}
});
export var LeftBarAuthUserNoLogin =  __class__ ('LeftBarAuthUserNoLogin', [left_bar.LeftBarMenu], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		left_bar.LeftBarMenu.__init__ (self, 'auth_user_no_login', I18N ('Start', __kwargtrans__ (dict ({'_pt-br': 'Início'}))), I (__kwargtrans__ ({_class: 'fas fa-user'})));
		self.attributes = dict (__kwargtrans__ ({_class: '{0} {1}'.format ('phanterpwa-component-left_bar-menu_button-wrapper-auth_user', 'phanterpwa-component-left_bar-menu_button-wrapper')}));
		self.addSubmenu ('login', I18N ('Login', __kwargtrans__ (dict ({'_pt-br': 'Logar-se'}))), __kwargtrans__ ({_class: 'command_user'}));
		self.addSubmenu ('register', I18N ('Create an account', __kwargtrans__ (dict ({'_pt-br': 'Criar Conta'}))), __kwargtrans__ ({_class: 'command_user'}));
		self.addSubmenu ('request_password', I18N ('Recover password', __kwargtrans__ (dict ({'_pt-br': 'Esqueci a Senha'}))), __kwargtrans__ ({_class: 'command_user'}));
		self.position = 'top';
		self.autorized_roles = ['anonymous'];
	});},
	get switch_menu () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var el = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-menu_button-auth_user_no_login').parent ();
		if (el.hasClass ('enabled')) {
			self.close_menu ();
		}
		else {
			self.open_menu ();
		}
	});},
	get _open_menu () {return function () {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
				}
			}
		}
		else {
		}
		var element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-menu_button-auth_user_no_login').parent ();
		element.addClass ('enabled');
		$ ('#phanterpwa-component-left_bar').addClass ('enabled_submenu');
		$ ('#phanterpwa-component-left_bar-main_button').addClass ('enabled_submenu');
	};},
	get open_menu () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		AuthUser._open_menu ();
		self._open_menu ();
	});},
	get _close_menu () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-menu_button-auth_user_no_login').parent ();
		element.removeClass ('enabled');
		if ($ ('#phanterpwa-component-left_bar').find ('.phanterpwa-component-left_bar-menu_button-wrapper.enabled').length == 0) {
			$ ('#phanterpwa-component-left_bar').removeClass ('enabled_submenu');
			$ ('#phanterpwa-component-left_bar-main_button').removeClass ('enabled_submenu');
		}
	});},
	get close_menu () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		AuthUser._close_menu ();
		self._close_menu ();
	});},
	get close_all () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		AuthUser._close_menu ();
		LeftBarAuthUserLogin._close_menu ();
		LeftBarAuthUserNoLogin._close_menu ();
		LeftBarMainButton._close ();
		left_bar.LeftBar._close ();
	});},
	get modal_login () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close_all ();
		self.Modal = ModalLogin ('#modal-container', __kwargtrans__ ({social_logins: window.PhanterPWA.social_login_list ()}));
		self.Modal.open ();
		forms.SignForm ('#form-login', __kwargtrans__ ({has_captcha: true}));
		forms.ValidateForm ('#form-login');
	});},
	get modal_register () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close_all ();
		self.Modal = ModalRegister ('#modal-container');
		self.Modal.open ();
		forms.SignForm ('#form-register', __kwargtrans__ ({has_captcha: true}));
		forms.ValidateForm ('#form-register');
	});},
	get modal_request_password () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.close_all ();
		self.Modal = ModalRequestPassword ('#modal-container');
		self.Modal.open ();
		forms.SignForm ('#form-request_password', __kwargtrans__ ({has_captcha: true}));
		forms.ValidateForm ('#form-request_password');
	});},
	get start () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-menu_button-{0}'.format (self.identifier));
		element.off ('click.open_leftbar_menu').on ('click.open_leftbar_menu', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.switch_menu ();
		}));
		var sub_element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-submenu-from-{0} .phanterpwa-component-left_bar-submenu-button'.format (self.identifier));
		sub_element.off ('click.close_leftbar_submenu').on ('click.close_leftbar_submenu', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.close_menu ();
		}));
		$ ('#phanterpwa-component-left_bar-submenu-button-login').off ('click.left_bar_login_button').on ('click.left_bar_login_button', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.modal_login ();
		}));
		$ ('#phanterpwa-component-left_bar-submenu-button-register').off ('click.left_bar_register_button').on ('click.left_bar_register_button', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.modal_register ();
		}));
		$ ('#phanterpwa-component-left_bar-submenu-button-request_password').off ('click.left_bar_request_btn').on ('click.left_bar_request_btn', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.modal_request_password ();
		}));
	});}
});
export var Profile =  __class__ ('Profile', [gatehandler.Handler], {
	__module__: __name__,
	get initialize () {return __get__ (this, decorators.check_authorization ((function __lambda__ () {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
				}
			}
		}
		else {
		}
		return window.PhanterPWA.logged ();
	})) (function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.auth_user = window.PhanterPWA.get_last_auth_user ();
		var first_name = '';
		var last_name = '';
		var email = '';
		if (self.auth_user !== null && self.auth_user !== undefined) {
			var first_name = self.auth_user.first_name;
			var last_name = self.auth_user.last_name;
			var email = self.auth_user.email;
		}
		var xml_content = CONCATENATE (DIV (DIV (DIV (DIV (I18N ('Profile', __kwargtrans__ (dict ({'_pt-br': 'Perfil'}))), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (XSECTION (LABEL (I18N ('Personal Information', __kwargtrans__ (dict ({'_pt-br': 'Informações Pessoais'})))), FORM (DIV (DIV (DIV (DIV (preloaders.android, __kwargtrans__ ({_style: 'text-align:center;'})), __kwargtrans__ ({_id: 'profile-image-user-container', _class: 'p-row'})), __kwargtrans__ ({_class: 'p-col w1p100 l4'})), DIV (DIV (DIV (STRONG (I18N ('First Name')), SPAN (first_name), DIV (I (__kwargtrans__ ({_class: 'fas fa-pen'})), __kwargtrans__ ({_class: 'e-tagger-button e-link open-model-edit-personal-information'})), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ ({_class: 'p-row'})), DIV (DIV (DIV (STRONG (I18N ('Last Name')), SPAN (last_name), DIV (I (__kwargtrans__ ({_class: 'fas fa-pen'})), __kwargtrans__ ({_class: 'e-tagger-button e-link open-model-edit-personal-information'})), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ ({_class: 'p-row'})), DIV (DIV (DIV (STRONG (I18N ('E-Mail')), SPAN (email), DIV (I (__kwargtrans__ ({_class: 'fas fa-pen'})), __kwargtrans__ ({_class: 'e-tagger-button e-link open-model-edit-personal-information'})), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ ({_class: 'p-row'})), __kwargtrans__ ({_class: 'e-padding_20'})), DIV (DIV (DIV (forms.FormWidget ('profile', 'first_name', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('First Name'), 'value': first_name, 'validators': ['IS_NOT_EMPTY'], '_class': 'p-col w1p100 w3p50'}))), forms.FormWidget ('profile', 'last_name', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('Last Name'), 'value': last_name, 'validators': ['IS_NOT_EMPTY'], '_class': 'p-col w1p100 w3p50'}))), forms.FormWidget ('profile', 'email', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('E-Mail'), 'value': email, 'validators': ['IS_EMAIL'], '_class': 'p-col w1p100'}))), __kwargtrans__ ({_class: 'p-row profile_inputs_container'})), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ ({_class: 'e-padding_20 e-hidden'})), __kwargtrans__ (dict ({'_phanterpwa-form': 'profile', '_id': 'form-profile', '_class': 'p-row', '_autocomplete': 'off'})))), __kwargtrans__ ({_class: 'e-margin_bottom_20 phanterpwa-card-container e-padding_20 card'})), __kwargtrans__ ({_class: 'phanterpwa-container container'})));
		xml_content.html_to ('#main-container');
		self.reload ();
	}));},
	get after_submit () {return __get__ (this, function (self, data, ajax_status) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (ajax_status == 'success') {
			var json = data.responseJSON;
			var message = json.i18n.message;
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': message})));
			if (data.status == 200) {
				$ ('.phanterpwa-gallery-upload-input-file').val ('');
				var auth_user = json.auth_user;
				window.PhanterPWA.update_auth_user (auth_user);
				self.reload ();
			}
		}
		else {
			forms.SignForm ('#form-profile');
			var json = data.responseJSON;
			var message = json.i18n.message;
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': message})));
		}
	});},
	get submit () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var formdata = new FormData ($ ('#form-profile') [0]);
		window.PhanterPWA.ApiServer.PUT (__kwargtrans__ (dict ({'url_args': ['api', 'auth', 'change'], 'form_data': formdata, 'onComplete': self.after_submit})));
	});},
	get open_modal_change_password () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		window.PhanterPWA.Components ['auth_user'].modal_change_password ();
	});},
	get reload () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		forms.SignForm ('#form-profile');
		self.auth_user = window.PhanterPWA.get_last_auth_user ();
		var first_name = '';
		var last_name = '';
		var email = '';
		var user_image = window.PhanterPWA.get_last_auth_user_image ();
		if (self.auth_user !== null && self.auth_user !== undefined) {
			var first_name = self.auth_user.first_name;
			var last_name = self.auth_user.last_name;
			var email = self.auth_user.email;
		}
		self.GalleryInput = gallery.GalleryInput ('#profile-image-user-container', __kwargtrans__ (dict ({'cutter': true, 'current_image': user_image, 'afterCut': (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.submit ();
		})})));
		if (!($ ('#phanterpwa-component-left_bar-url-imagem-user').lenght == 0)) {
			$ ('#phanterpwa-component-left_bar-url-imagem-user').attr ('src', user_image);
		}
		$ ('#url_image_user').attr ('src', user_image);
		$ ('#phanterpwa-component-left_bar-url-imagem-user').attr ('src', user_image);
		$ ('#phanterpwa-widget-input-profile-first_name').val (first_name);
		$ ('#phanterpwa-widget-input-profile-last_name').val (last_name);
		$ ('#phanterpwa-widget-input-profile-email').val (email).trigger ('keyup');
		$ ('.open-model-edit-personal-information').off ('click.open-model-edit-personal-information').on ('click.open-model-edit-personal-information', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.modal_personal_information ();
		}));
	});},
	get modal_personal_information () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.Modal = ModalPersonalInformation ('#modal-container');
		self.Modal.open ();
	});}
});
export var Lock =  __class__ ('Lock', [gatehandler.Handler], {
	__module__: __name__,
	get initialize () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var request = self.request;
		var last_way = request ['last_way'];
		if (last_way !== null && last_way !== undefined && last_way !== 'lock') {
			sessionStorage.setItem ('way_before_lock', last_way);
		}
		else {
			sessionStorage.setItem ('way_before_lock', window.PhanterPWA.default_way);
		}
		self.last_auth_user = window.PhanterPWA.get_last_auth_user ();
		self.last_auth_user_image = window.PhanterPWA.get_last_auth_user_image ();
		if (self.last_auth_user !== null) {
			window.PhanterPWA.ApiServer.GET (__kwargtrans__ (dict ({'url_args': ['api', 'auth', 'lock'], 'onComplete': self.after_confirm_lock})));
		}
		else {
			self.on_other_user_click ();
		}
	});},
	get on_other_user_click () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		$ ('body').removeClass ('phanterpwa-lock');
		localStorage.removeItem ('last_auth_user');
		localStorage.removeItem ('current_way');
		localStorage.removeItem ('way_before_lock');
		window.PhanterPWA.Components ['auth_user'].logout ();
	});},
	get after_submit () {return __get__ (this, function (self, data, ajax_status) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (ajax_status == 'success') {
			var json = data.responseJSON;
			var authorization = json.authorization;
			var auth_user = json.auth_user;
			var client_token = json.client_token;
			var url_token = json.url_token;
			if (authorization !== undefined && auth_user !== undefined && client_token !== undefined) {
				localStorage.setItem ('phanterpwa-client-token', client_token);
				localStorage.setItem ('phanterpwa-url-token', url_token);
				if (auth_user ['remember_me'] === true) {
					localStorage.setItem ('phanterpwa-authorization', authorization);
					localStorage.setItem ('auth_user', JSON.stringify (auth_user));
					sessionStorage.removeItem ('phanterpwa-authorization');
					sessionStorage.removeItem ('auth_user');
				}
				else {
					sessionStorage.setItem ('phanterpwa-authorization', authorization);
					sessionStorage.setItem ('auth_user', JSON.stringify (auth_user));
					localStorage.removeItem ('phanterpwa-authorization');
					localStorage.removeItem ('auth_user');
				}
				localStorage.setItem ('last_auth_user', JSON.stringify (auth_user));
			}
			var way_before_lock = sessionStorage.getItem ('way_before_lock');
			if (way_before_lock !== null && way_before_lock !== undefined) {
				window.PhanterPWA.open_way (way_before_lock);
			}
			else {
				window.PhanterPWA.open_default_way ();
			}
			self.AuthUser = window.PhanterPWA.Components ['auth_user'];
			if (self.AuthUser !== null && self.AuthUser !== undefined) {
				self.AuthUser.start ();
				self.AuthUser.AlertActivationAccount.check_activation ();
			}
			var LeftBar = window.PhanterPWA.Components ['left_bar'];
			if (LeftBar !== null && LeftBar !== undefined) {
				LeftBar.reload ();
			}
			$ ('body').removeClass ('phanterpwa-lock');
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
		}
		else if (data.status == 400) {
			var json = data.responseJSON;
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
			forms.SignLockForm ();
			var errors = dict (json ['errors']);
			if (errors !== undefined) {
				for (var x of errors.py_keys ()) {
					var id_error = '#phanterpwa-widget-login-{0} .phanterpwa-widget-error'.format ('lock');
					var message = SPAN (errors [x]).xml ();
					$ (id_error).html (message).addClass ('enabled');
				}
			}
		}
	});},
	get submit () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		$ ('#user_locked .phanterpwa-materialize-input-error').removeClass ('enabled').text ('');
		var formdata = new FormData ();
		formdata.append ('csrf_token', $ ('#form-lock #phanterpwa-widget-input-input-lock-csrf_token').val ());
		var login_password = '{0}:{1}'.format (window.btoa ($ ('#form-lock #phanterpwa-widget-input-input-lock-email').val ()), window.btoa ($ ('#form-lock #phanterpwa-widget-input-input-lock-password').val ()));
		formdata.append ('edata', login_password);
		var remember_me = false;
		if ($ ('#form-lock #phanterpwa-widget-checkbox-input-lock-remember_me').prop ('checked')) {
			var remember_me = true;
		}
		formdata.append ($ ('#form-lock #phanterpwa-widget-checkbox-input-lock-remember_me').attr ('name'), remember_me);
		window.PhanterPWA.ApiServer.POST (__kwargtrans__ (dict ({'url_args': ['api', 'auth'], 'form_data': formdata, 'onComplete': self.after_submit})));
	});},
	get binds () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		forms.SignLockForm ();
		$ ('#phanterpwa-widget-form-form_button-other').off ('click.other_user_unlock').on ('click.other_user_unlock', self.on_other_user_click);
		$ ('#phanterpwa-widget-form-submit_button-lock').off ('click.login_user_unlock').on ('click.login_user_unlock', self.submit);
	});},
	get after_confirm_lock () {return __get__ (this, function (self, data, ajax_status) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (ajax_status == 'success') {
			var html = CONCATENATE (DIV (DIV (DIV (DIV (I18N ('Locked', __kwargtrans__ (dict ({'_pt-br': 'Bloqueado'}))), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (DIV (DIV (DIV (FORM (DIV (DIV (DIV (DIV (IMG (__kwargtrans__ ({_id: 'form-lock-image-user-url'})), __kwargtrans__ ({_class: 'form-image-user-img'})), __kwargtrans__ ({_class: 'form-image-user-img-container'})), DIV (DIV (__kwargtrans__ ({_id: 'form-lock-profile-user-name', _class: 'form-profile-user-name'})), DIV (__kwargtrans__ ({_id: 'form-lock-profile-user-role', _class: 'form-profile-user-role'})), __kwargtrans__ ({_class: 'form-profile-user-info'})), __kwargtrans__ ({_class: 'form-profile-container'})), __kwargtrans__ ({_id: 'form-lock-image-user-container', _class: 'form-image-user-container'})), forms.FormWidget ('lock', 'email', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('E-mail'), 'validators': ['IS_NOT_EMPTY', 'IS_EMAIL'], '_class': 'e-display_hidden'}))), DIV (forms.FormWidget ('lock', 'password', __kwargtrans__ (dict ({'label': I18N ('Password', __kwargtrans__ (dict ({'_pt-br': 'Senha'}))), 'type': 'password', 'validators': ['IS_NOT_EMPTY']}))), __kwargtrans__ ({_class: 'p-col w1p100'})), DIV (forms.FormWidget ('lock', 'remember_me', __kwargtrans__ (dict ({'label': I18N ('Remember-me', __kwargtrans__ (dict ({'_pt-br': 'Lembre-me'}))), 'type': 'boolean'}))), __kwargtrans__ ({_class: 'input-field p-col w1p100'})), DIV (DIV (forms.SubmitButton ('lock', I18N ('Unlock', __kwargtrans__ (dict ({'_pt-br': 'Desbloquear'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), forms.FormButton ('other', I18N ('Use other account', __kwargtrans__ (dict ({'_pt-br': 'Usar outra conta'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), __kwargtrans__ ({_class: 'phanterpwa-form-buttons-container'})), __kwargtrans__ ({_class: 'input-field p-col w1p100'})), __kwargtrans__ (dict ({'_phanterpwa-form': 'lock', '_id': 'form-lock', '_class': 'p-row', '_autocomplete': 'off'}))), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ ({_class: 'p-row'})), __kwargtrans__ ({_class: 'lock-container'})), __kwargtrans__ ({_class: 'card'})), __kwargtrans__ ({_class: 'container'})));
			sessionStorage.removeItem ('phanterpwa-authorization');
			sessionStorage.removeItem ('auth_user');
			localStorage.removeItem ('phanterpwa-authorization');
			localStorage.removeItem ('auth_user');
			$ ('body').addClass ('phanterpwa-lock');
			html.html_to ('#main-container');
			$ ('#form-lock #phanterpwa-widget-input-input-lock-email').val (self.last_auth_user.email);
			if (self.last_auth_user.remember_me) {
				PhanterPWA.Request.widgets ['lock-remember_me'].set_value (true);
			}
			$ ('#form-lock-profile-user-name').text ('{0} {1}'.format (self.last_auth_user ['first_name'], self.last_auth_user ['last_name']));
			$ ('#form-lock-profile-user-role').text (self.last_auth_user ['role']);
			$ ('#form-lock-image-user-url').attr ('src', self.last_auth_user_image);
			self.binds ();
		}
		else {
			self.on_other_user_click ();
		}
		var json = data.responseJSON;
		window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
	});}
});
export var TwoFactor =  __class__ ('TwoFactor', [gatehandler.Handler], {
	__module__: __name__,
	get initialize () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self._authorization_url_two_factor = self._request.get_arg (0);
		var AuthUserCmp = window.PhanterPWA.Components ['auth_user'];
		self.AuthUser = null;
		if (AuthUserCmp !== null && AuthUserCmp !== undefined && !(isinstance (AuthUserCmp, AuthUser))) {
			console.error ('Need AuthUser instance on window.PhanterPWA.Components');
		}
		else {
			self.AuthUser = AuthUserCmp;
		}
		var last_way = self._request ['last_way'];
		if (last_way !== null && last_way !== undefined && !(last_way.startswith ('two_factor'))) {
			self.way_before_two_factor = last_way;
		}
		else {
			self.way_before_two_factor = window.PhanterPWA.default_way;
		}
		self.start ();
	});},
	get after_submit () {return __get__ (this, function (self, data, ajax_status) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (ajax_status == 'success') {
			var json = data.responseJSON;
			self.AuthUser.start ();
			self.AuthUser.AlertActivationAccount.check_activation ();
			window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
			var LeftBar = window.PhanterPWA.Components ['left_bar'];
			if (LeftBar !== null && LeftBar !== undefined) {
				LeftBar.reload ();
			}
			window.PhanterPWA.open_way (self.way_before_two_factor);
		}
	});},
	get submit () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		window.PhanterPWA.two_factor (self._authorization_url_two_factor, $ ('#phanterpwa-widget-input-input-confirmation-code-code').val (), __kwargtrans__ ({callback: self.after_submit}));
	});},
	get binds () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		forms.ValidateForm ('#form-confirmation-code');
		$ ('#phanterpwa-widget-form-submit_button-confirmation-code').off ('click.confirmation-code_button_save').on ('click.confirmation-code_button_save', self.submit);
	});},
	get reload () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.start ();
	});},
	get start () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var xml_content = CONCATENATE (DIV (DIV (DIV (DIV (I18N ('Two Factor Authentication', __kwargtrans__ (dict ({'_pt-br': 'Autenticação de duas etapas'}))), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (FORM (H2 (I18N ('Login Confirmation Code', __kwargtrans__ (dict ({'_pt-br': 'Código de confirmação do login'})))), P (I18N ('The two-factor confirmation code has ', 'been sent to your email, add it below and confirm.', __kwargtrans__ (dict ({'_pt-br': 'Um código de confirmação foi enviado ao seu email, digite-o abaixo e confirme'})))), DIV (DIV (forms.FormWidget ('confirmation-code', 'code', __kwargtrans__ (dict ({'type': 'string', 'label': I18N ('Confirmation code', __kwargtrans__ (dict ({'_pt-br': 'Código de Confirmação'}))), 'validators': ['IS_NOT_EMPTY', 'IS_ACTIVATION_CODE'], '_class': 'p-col w1p100'}))), __kwargtrans__ ({_class: 'p-row profile_inputs_container'})), DIV (forms.SubmitButton ('confirmation-code', I18N ('Confirm', __kwargtrans__ (dict ({'_pt-br': 'Confirmar'}))), __kwargtrans__ ({_class: 'btn-autoresize wave_on_click waves-phanterpwa'})), __kwargtrans__ ({_class: 'phanterpwa-form-buttons-container'})), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ (dict ({'_phanterpwa-form': 'confirmation-code', '_id': 'form-confirmation-code', '_class': 'p-row', '_autocomplete': 'off'}))), __kwargtrans__ ({_class: 'e-margin_bottom_20 phanterpwa-card-container e-padding_20 card'})), __kwargtrans__ ({_class: 'phanterpwa-container container'})));
		xml_content.html_to ('#main-container');
		self.binds ();
	});}
});

//# sourceMappingURL=phanterpwa.frontend.components.auth_user.map