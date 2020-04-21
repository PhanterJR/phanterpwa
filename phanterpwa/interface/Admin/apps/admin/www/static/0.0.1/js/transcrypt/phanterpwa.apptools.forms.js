// Transcrypt'ed from Python, 2020-04-15 16:16:57
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as widgets from './phanterpwa.apptools.components.widgets.js';
import * as helpers from './phanterpwa.apptools.helpers.js';
import * as preloaders from './phanterpwa.apptools.preloaders.js';
import * as validations from './phanterpwa.apptools.validations.js';
var __name__ = 'phanterpwa.apptools.forms';
export var I18N = helpers.I18N;
export var FORM = helpers.XmlConstructor.tagger ('form', false);
export var SPAN = helpers.XmlConstructor.tagger ('span', false);
export var DIV = helpers.XmlConstructor.tagger ('div', false);
export var I = helpers.XmlConstructor.tagger ('i', false);
export var INPUT = helpers.XmlConstructor.tagger ('input', true);
export var LABEL = helpers.XmlConstructor.tagger ('label', false);
export var TEXTAREA = helpers.XmlConstructor.tagger ('textarea', false);
export var SELECT = helpers.XmlConstructor.tagger ('select', false);
export var OPTION = helpers.XmlConstructor.tagger ('option', false);
export var XSECTION = helpers.XSECTION;
export var SignForm =  __class__ ('SignForm', [object], {
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
		self.element_target = $ (target_selector);
		self.table_name = self.element_target.attr ('phanterpwa-form');
		self.has_captcha = null;
		self.after_sign = null;
		self.preload = preloaders.android;
		self.element_csrf_token = $ (self.element_target).find ('#phanterpwa-widget-input-{0}-csrf_token'.format (self.table_name));
		if (self.element_csrf_token.length == 0) {
			self.element_target.prepend (CSRFInput (self.table_name).jquery ());
			self.element_csrf_token = $ (self.element_target).find ('#phanterpwa-widget-input-{0}-csrf_token'.format (self.table_name));
		}
		self.element_captcha_container = $ (self.element_target).find ('#phanterpwa-widget-{0}-captcha-container'.format (self.table_name));
		if (__in__ ('has_captcha', parameters)) {
			self.has_captcha = parameters ['has_captcha'];
		}
		if (__in__ ('after_sign', parameters)) {
			self.after_sign = parameters ['after_sign'];
		}
		if (__in__ ('preload', parameters)) {
			self.preload = parameters ['preload'];
		}
		if (self.has_captcha === true) {
			self.signCaptchaForm ();
		}
		else {
			self.signForm ();
		}
	});},
	get after_try_sign () {return __get__ (this, function (self, data, ajax_status) {
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
			var csrf = data.responseJSON.csrf;
			self.element_csrf_token.val (csrf).trigger ('keyup');
		}
		if (self.after_sign !== null && self.after_sign !== undefined) {
			self.after_sign (data, ajax_status);
		}
	});},
	get signForm () {return __get__ (this, function (self) {
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
		self.element_csrf_token.val ('').trigger ('keyup');
		window.PhanterPWA.ApiServer.GET (__kwargtrans__ (dict ({'url_args': ['api', 'signforms', 'phanterpwa-form-{0}'.format (self.table_name)], 'onComplete': self.after_try_sign})));
	});},
	get on_captcha_fail () {return __get__ (this, function (self) {
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
		self.element_captcha_container.html (DIV (DIV (I18N ('Conection Fail!').jquery ().attr ('pt-BR', 'Conexão Falhou!'), __kwargtrans__ ({_id: 'captcha_reload_conection_fail_messagem'})), DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-redo-alt'})), __kwargtrans__ ({_id: 'captcha_reload_conection_icon'})), DIV (I18N ('Try again!').jquery ().attr ('pt-BR', 'Tente Novamente'), __kwargtrans__ ({_id: 'captcha_reload_conection_try_again_messagem'})), __kwargtrans__ ({_class: 'captcha_reload_conection_button link'})), __kwargtrans__ ({_class: 'captcha_reload_conection_container'})).jquery ());
		self.element_captcha_container.find ('.captcha_reload_conection_button').off ('click.captcha_reload_conection_button_{0}'.format (self.table_name)).on ('click.captcha_reload_conection_button_{0}'.format (self.table_name), (function __lambda__ () {
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
			return tuple ([self.element_captcha_container.html (self.preload), self.signCaptchaForm ()]);
		}));
	});},
	get after_get_captcha_html () {return __get__ (this, function (self, data, ajax_status) {
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
			if (data.responseJSON.status == 'OK') {
				var signature = data.responseJSON.signature;
				var html = data.responseJSON.captcha;
				self.add_html_Captcha (html, signature);
			}
		}
		else if (data.status == 0) {
			self.on_captcha_fail ();
		}
	});},
	get add_html_Captcha () {return __get__ (this, function (self, html, signature) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'html': var html = __allkwargs0__ [__attrib0__]; break;
						case 'signature': var signature = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element_captcha_container.html (html);
		self.element_captcha_container.find ('.captcha-option').off ('click.captcha-option-{0}'.format (self.table_name)).on ('click.captcha-option-{0}'.format (self.table_name), (function __lambda__ () {
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
			return self.on_click_captcha_option (this, signature);
		}));
	});},
	get after_post_captcha_option () {return __get__ (this, function (self, data, ajax_status) {
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
			var html = data.responseJSON.captcha;
			var csrf = data.responseJSON.csrf;
			self.element_csrf_token.val (csrf).trigger ('keyup');
			self.element_captcha_container.html (html);
		}
		else {
			if (data.status == 0) {
				self.on_captcha_fail ();
			}
			else {
				var signature = data.responseJSON.signature;
				var html = data.responseJSON.captcha;
				if (signature !== undefined && html !== undefined) {
					self.add_html_Captcha (html, signature);
				}
				else {
					self.signCaptchaForm ();
				}
			}
			self.element_csrf_token.val ('').trigger ('keyup');
		}
	});},
	get on_click_captcha_option () {return __get__ (this, function (self, el, signature) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'el': var el = __allkwargs0__ [__attrib0__]; break;
						case 'signature': var signature = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var user_choice = $ (el).attr ('token_option');
		var signature = signature;
		var id_form = $ (el).attr ('id_captcha');
		var captcha_vars = {'user_choice': user_choice, 'signature': signature, 'id_form': id_form};
		self.element_captcha_container.html (self.preload);
		window.PhanterPWA.ApiServer.POST (__kwargtrans__ (dict ({'url_args': ['api', 'signcaptchaforms', id_form], 'form_data': captcha_vars, 'onComplete': self.after_post_captcha_option})));
	});},
	get signCaptchaForm () {return __get__ (this, function (self) {
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
		if (self.element_target.length == 0) {
			console.error ('The {0} not exist'.format (self.target_selector));
		}
		else {
			self.element_csrf_token = $ (self.element_target).find ('#phanterpwa-widget-input-{0}-csrf_token'.format (self.table_name));
			self.element_csrf_token.val ('').trigger ('keyup');
			window.PhanterPWA.ApiServer.GET (__kwargtrans__ (dict ({'url_args': ['api', 'signcaptchaforms', 'phanterpwa-form-{0}'.format (self.table_name)], 'onComplete': self.after_get_captcha_html})));
		}
	});}
});
export var SignLockForm =  __class__ ('SignLockForm', [object], {
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
		self.element_target = $ ("[phanterpwa-form='lock']");
		self.element_csrf_token = $ ("[phanterpwa-form='lock'] #phanterpwa-widget-input-lock-csrf_token");
		if (self.element_csrf_token.length == 0) {
			self.element_target.prepend (CSRFInput ('lock').jquery ());
			self.element_csrf_token = $ ("[phanterpwa-form='lock'] #phanterpwa-widget-input-lock-csrf_token");
		}
		self.element_csrf_token.val ('').trigger ('keyup');
		window.PhanterPWA.ApiServer.GET (__kwargtrans__ (dict ({'url_args': ['api', 'signlockform'], 'onComplete': self.after_sign})));
	});},
	get after_sign () {return __get__ (this, function (self, data, ajax_status) {
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
			var csrf = data.responseJSON.csrf;
			self.element_csrf_token.val (csrf).trigger ('keyup');
		}
		else {
			window.PhanterPWA.logout ();
		}
	});}
});
export var CaptchaContainer =  __class__ ('CaptchaContainer', [helpers.XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, table_name) {
		var attributes = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'table_name': var table_name = __allkwargs0__ [__attrib0__]; break;
						default: attributes [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete attributes.__kwargtrans__;
			}
			var content = tuple ([].slice.apply (arguments).slice (2, __ilastarg0__ + 1));
		}
		else {
			var content = tuple ();
		}
		self.table_name = table_name;
		attributes ['_id'] = 'phanterpwa-widget-{0}-captcha-container'.format (self.table_name);
		if (__in__ ('_class', attributes)) {
			attributes ['_class'] = '{0}{1}'.format (attributes ['_class'].strip (), ' phanterpwa-widget-captcha-container');
		}
		else {
			attributes ['_class'] = 'phanterpwa-widget-captcha-container';
		}
		helpers.XmlConstructor.__init__ (self, 'div', false, ...content, __kwargtrans__ (attributes));
	});}
});
export var FormButton =  __class__ ('FormButton', [helpers.XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, py_name, label) {
		var attributes = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'py_name': var py_name = __allkwargs0__ [__attrib0__]; break;
						case 'label': var label = __allkwargs0__ [__attrib0__]; break;
						default: attributes [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete attributes.__kwargtrans__;
			}
		}
		else {
		}
		self.label = label;
		var initial_class = 'phanterpwa-widget-form-form_button-container';
		if (!__in__ (['_id'], attributes)) {
			attributes ['_id'] = 'phanterpwa-widget-form-form_button-{0}'.format (py_name);
		}
		self.button_attributes = attributes;
		if (__in__ ('_class', self.button_attributes)) {
			self.button_attributes ['_class'] = ' '.join ([self.button_attributes ['_class'].strip (), 'btn phanterpwa-widget-form-form_button link']);
		}
		else {
			self.button_attributes ['_class'] = 'btn phanterpwa-widget-form-form_button link';
		}
		if (!__in__ ('_title', self.button_attributes)) {
			if (isinstance (self.label, str)) {
				self.button_attributes ['_title'] = self.label;
			}
		}
		helpers.XmlConstructor.__init__ (self, 'div', false, __kwargtrans__ ({_class: initial_class}));
		self._update_content ();
	});},
	get _update_content () {return __get__ (this, function (self) {
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
		var attributes = self.button_attributes;
		self.content = [DIV (DIV (self.label, __kwargtrans__ (attributes)), __kwargtrans__ ({_class: 'button-form'}))];
	});}
});
export var SubmitButton =  __class__ ('SubmitButton', [FormButton], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, form, label) {
		var attributes = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'form': var form = __allkwargs0__ [__attrib0__]; break;
						case 'label': var label = __allkwargs0__ [__attrib0__]; break;
						default: attributes [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete attributes.__kwargtrans__;
			}
		}
		else {
		}
		attributes ['_phanterpwa_widget_submit_button'] = form;
		if (!__in__ (['_id'], attributes)) {
			attributes ['_id'] = 'phanterpwa-widget-form-submit_button-{0}'.format (form);
		}
		FormButton.__init__ (self, null, label, __kwargtrans__ (attributes));
	});}
});
export var CSRFInput =  __class__ ('CSRFInput', [helpers.XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, table_name) {
		var attributes = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'table_name': var table_name = __allkwargs0__ [__attrib0__]; break;
						default: attributes [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete attributes.__kwargtrans__;
			}
		}
		else {
		}
		self.table_name = table_name;
		if (!__in__ (['_id'], attributes)) {
			attributes ['_id'] = 'phanterpwa-widget-container-{0}-csrf_token'.format (self.table_name);
		}
		self.button_attributes = attributes;
		if (__in__ ('_class', self.button_attributes)) {
			self.button_attributes ['_class'] = ' '.join ([self.button_attributes ['_class'].strip (), 'phanterpwa-widget phanterpwa-widget-hidden e-display_hidden']);
		}
		else {
			self.button_attributes ['_class'] = 'phanterpwa-widget phanterpwa-widget-hidden e-display_hidden';
		}
		helpers.XmlConstructor.__init__ (self, 'div', false, DIV (I (__kwargtrans__ ({_class: 'fas fa-check'})), __kwargtrans__ ({_id: 'phanterpwa-widget-check-{0}-csrf_token'.format (self.table_name), _class: 'phanterpwa-widget-check'})), DIV (INPUT (__kwargtrans__ ({_id: 'phanterpwa-widget-input-{0}-csrf_token'.format (self.table_name), _name: 'csrf_token', _phanterpwa_widget_validator: JSON.stringify (['IS_NOT_EMPTY']), _phanterpwa_widget_table_name: self.table_name, _type: 'hidden'})), LABEL ('CSRF Token', __kwargtrans__ ({_for: 'phanterpwa-widget-input-{0}-csrf_token'.format (self.table_name)})), __kwargtrans__ ({_class: 'input-field'})), DIV (__kwargtrans__ ({_class: 'phanterpwa-widget-error'})), __kwargtrans__ (attributes));
	});}
});
export var FormWidget =  __class__ ('FormWidget', [helpers.XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, table_name, input_name) {
		var json_widget = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'table_name': var table_name = __allkwargs0__ [__attrib0__]; break;
						case 'input_name': var input_name = __allkwargs0__ [__attrib0__]; break;
						default: json_widget [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete json_widget.__kwargtrans__;
			}
		}
		else {
		}
		self.table_name = table_name;
		self.input_name = input_name;
		self.json_widget = json_widget;
		self.placeholder = null;
		self.icon_button = null;
		self.validators = json_widget.py_get ('validators', null);
		self._value = json_widget.py_get ('value', null);
		self._editable = json_widget.py_get ('editable', false);
		self._can_empty = json_widget.py_get ('can_empty', false);
		self._mask = json_widget.py_get ('mask', null);
		self.fmt = json_widget.py_get ('format', null);
		self._cutter = json_widget.py_get ('cutter', false);
		self._url = json_widget.py_get ('url', null);
		self._nocache = json_widget.py_get ('no-cache', false);
		if (!__in__ ('_id', json_widget)) {
			json_widget ['_id'] = 'phanterpwa-widget-wrapper-{0}-{1}'.format (self.table_name, self.input_name);
		}
		if (!__in__ ('type', json_widget)) {
			json_widget ['type'] = 'string';
		}
		self._widget_type = json_widget ['type'];
		if (__in__ ('_class', json_widget)) {
			json_widget ['_class'] = '{0}{1}'.format (json_widget ['_class'].strip (), ' phanterpwa-widget-wrapper');
		}
		else {
			json_widget ['_class'] = 'phanterpwa-widget-wrapper-{0}'.format (json_widget ['type']);
		}
		if (__in__ ('phanterpwa', self.json_widget)) {
			var obj_pwa = dict (self.json_widget ['phanterpwa']);
			for (var a of obj_pwa.py_keys ()) {
				if (a.startswith ('_')) {
					self.extra_attr [a] = self.json_widget ['phanterpwa'] [a];
				}
			}
			if (__in__ ('icon_button', self.json_widget ['phanterpwa'])) {
				self.icon_button = DIV (I (__kwargtrans__ ({_class: self.json_widget ['phanterpwa'] ['icon_button']})), __kwargtrans__ ({_id: 'phanterpwa-widget-icon_button-{0}-{1}'.format (self.table_name, self.input_name), _class: 'phanterpwa-widget-icon_button link btn', _table_name: self.table_name, _input_name: self.input_name}));
			}
			if (self.validators !== null) {
				self.validators = JSON.stringify (self.validators);
			}
			if (__in__ ('mask', self.json_widget ['phanterpwa'])) {
				self._mask = self.json_widget ['phanterpwa'] ['mask'];
			}
			if (__in__ ('format', self.json_widget ['phanterpwa'])) {
				self.fmt = self.json_widget ['phanterpwa'] ['format'];
			}
			if (__in__ ('placeholder', self.json_widget ['phanterpwa'])) {
				self.placeholder = self.json_widget ['phanterpwa'] ['placeholder'];
			}
			if (__in__ ('type', self.json_widget ['phanterpwa'])) {
				self._widget_type = self.json_widget ['phanterpwa'] ['type'];
			}
		}
		helpers.XmlConstructor.__init__ (self, 'div', false, __kwargtrans__ (json_widget));
		self._process ();
	});},
	get _process () {return __get__ (this, function (self) {
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
		if (self._widget_type == 'date' || self._widget_type == 'datetime') {
			var dformat = 'yyyy-MM-dd';
			var dvalue = self.json_widget ['value'];
			if (self._widget_type == 'datetime') {
				var dformat = '{0} HH:mm:ss'.format (dformat);
			}
			if (self.fmt !== null && self.fmt !== undefined) {
				var dformat = self.fmt;
				if (isinstance (dvalue, str)) {
					var dvalue = validations.format_iso_date_datetime (dvalue, dformat, self._widget_type);
				}
			}
			var w = widgets.Input ('{0}-{1}'.format (self.table_name, self.input_name), __kwargtrans__ ({label: self.json_widget ['label'], py_name: self.input_name, value: dvalue, format: dformat, kind: self._widget_type, mask: dformat, form: self.table_name, icon: I (__kwargtrans__ ({_class: 'fas fa-calendar-alt'})), validators: self.validators}));
		}
		else if (self._widget_type == 'reference' || self._widget_type == 'select') {
			var w = widgets.Select ('{0}-{1}'.format (self.table_name, self.input_name), __kwargtrans__ ({label: self.json_widget ['label'], py_name: self.input_name, editable: self._editable, can_empty: self._can_empty, value: self._value, data_set: self.json_widget ['data_set'], form: self.table_name, validators: self.validators}));
		}
		else if (self._widget_type == 'list_string') {
			var w = widgets.ListString ('{0}-{1}'.format (self.table_name, self.input_name), __kwargtrans__ ({label: self.json_widget ['label'], py_name: self.input_name, value: self._value, form: self.table_name}));
		}
		else if (self._widget_type == 'text') {
			var w = widgets.Textarea ('{0}-{1}'.format (self.table_name, self.input_name), __kwargtrans__ ({label: self.json_widget ['label'], py_name: self.input_name, editable: self._editable, can_empty: self._can_empty, value: self._value, mask: self._mask, form: self.table_name, validators: self.validators}));
		}
		else if (self._widget_type == 'id') {
			var w = widgets.Inert ('{0}-{1}'.format (self.table_name, self.input_name), __kwargtrans__ ({label: self.json_widget ['label'], py_name: self.input_name, value: self._value, form: self.table_name}));
		}
		else if (self._widget_type == 'boolean') {
			var w = widgets.CheckBox ('{0}-{1}'.format (self.table_name, self.input_name), __kwargtrans__ ({label: self.json_widget ['label'], py_name: self.input_name, value: self._value === true, form: self.table_name}));
		}
		else if (self._widget_type == 'password') {
			var w = widgets.Input ('{0}-{1}'.format (self.table_name, self.input_name), __kwargtrans__ ({label: self.json_widget ['label'], py_name: self.input_name, value: self._value, form: self.table_name, validators: self.validators, kind: 'password'}));
		}
		else if (self._widget_type == 'hidden') {
			var w = widgets.Input ('{0}-{1}'.format (self.table_name, self.input_name), __kwargtrans__ ({label: self.json_widget ['label'], py_name: self.input_name, value: self._value, editable: self._editable, can_empty: self._can_empty, mask: self._mask, form: self.table_name, kind: 'hidden', validators: self.validators}));
		}
		else if (self._widget_type == 'image') {
			var w = widgets.Image ('{0}-{1}'.format (self.table_name, self.input_name), __kwargtrans__ ({label: self.json_widget ['label'], py_name: self.input_name, value: self._url, form: self.table_name, cutter: self._cutter, nocache: self._nocache}));
		}
		else {
			var w = widgets.Input ('{0}-{1}'.format (self.table_name, self.input_name), __kwargtrans__ ({label: self.json_widget ['label'], py_name: self.input_name, value: self._value, editable: self._editable, can_empty: self._can_empty, mask: self._mask, form: self.table_name, validators: self.validators}));
		}
		self.append (w);
	});}
});
export var Form =  __class__ ('Form', [helpers.XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, json_form) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'json_form': var json_form = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		var fields = null;
		var submit_button = null;
		self.show_id = false;
		self.has_captcha = null;
		self.preload = preloaders.android;
		self.after_sign = null;
		self.element = null;
		self.table_name = json_form.table;
		if (__in__ ('fields', parameters)) {
			var fields = parameters ['fields'];
		}
		if (__in__ ('show_id', parameters)) {
			self.show_id = parameters ['show_id'];
		}
		if (__in__ ('submit_button', parameters)) {
			var submit_button = parameters ['submit_button'];
		}
		if (__in__ ('has_captcha', parameters)) {
			self.has_captcha = parameters ['has_captcha'];
		}
		if (__in__ ('preload', parameters)) {
			self.preload = parameters ['preload'];
		}
		if (__in__ ('after_sign', parameters)) {
			self.after_sign = parameters;
		}
		if (__in__ ('_class', parameters)) {
			parameters ['_class'] = '{0}{1}'.format (parameters ['_class'].strip (), ' phanterpwa-form');
		}
		else {
			parameters ['_class'] = 'phanterpwa-form';
		}
		if (!__in__ ('_id', parameters)) {
			parameters ['_id'] = 'form-{0}'.format (self.table_name);
		}
		parameters ['_phanterpwa-form'] = self.table_name;
		self.json_widgets = json_form ['widgets'];
		self.widgets = dict ();
		self.fields = fields;
		self.table_name = json_form ['table'];
		helpers.XmlConstructor.__init__ (self, 'form', false, CSRFInput (self.table_name), __kwargtrans__ (parameters));
		self._captcha_container = CaptchaContainer (self.table_name, self.preload);
		if (submit_button !== null && submit_button !== undefined) {
			self._buttons_container = DIV (submit_button, __kwargtrans__ ({_class: 'buttons-form-container'}));
		}
		else {
			self._buttons_container = DIV (SubmitButton (self.table_name, I18N ('Submit')), __kwargtrans__ ({_class: 'buttons-form-container'}));
		}
		self._process ();
	});},
	get extra_button () {return __get__ (this, function (self, _id, label) {
		var attributes = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case '_id': var _id = __allkwargs0__ [__attrib0__]; break;
						case 'label': var label = __allkwargs0__ [__attrib0__]; break;
						default: attributes [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete attributes.__kwargtrans__;
			}
		}
		else {
		}
		self._buttons_container.append (FormButton (_id, label, __kwargtrans__ (attributes)));
		self.widget = dict ();
		self.content = list ();
		self._process ();
	});},
	get _process_widget () {return __get__ (this, function (self, wjson) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'wjson': var wjson = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (wjson [0] == 'widget') {
			return FormWidget (self.table_name, wjson [1] [0], __kwargtrans__ (dict (wjson [1] [1])));
		}
		else if (wjson [0] == 'section') {
			var content = [LABEL (wjson [1] [0])];
			for (var x of wjson [1] [1]) {
				content.append (self._process_widget (x));
			}
			return XSECTION (...content);
		}
		else if (wjson [0] == 'group') {
			var content = [];
			for (var x of wjson [1] [1]) {
				content.append (self._process_widget (x));
			}
			return DIV (...content, __kwargtrans__ ({_id: wjson [1] [0], _class: 'phanterpwa-widget-form-group'}));
		}
	});},
	get _process () {return __get__ (this, function (self) {
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
		for (var x of self.json_widgets) {
			var w = self._process_widget (x);
			self.widgets [x] = w;
			if (self.fields !== null && self.fields !== undefined) {
				if (__in__ (x, self.fields)) {
					self.append (w);
				}
			}
			else if (x == 'id') {
				if (self.show_id) {
					self.append (w);
				}
			}
			else {
				self.append (w);
			}
		}
		if (self.has_captcha === true) {
			self.append (self._captcha_container);
		}
		self.append (self._buttons_container);
	});},
	get signForm () {return __get__ (this, function (self) {
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
		self.Signer = SignForm (self.table_name, __kwargtrans__ (dict ({'preload': self.preload, 'has_captcha': self.has_captcha, 'after_sign': self.after_sign})));
	});},
	get target () {return __get__ (this, function (self, element) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'element': var element = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.element = element;
		var el = self.jquery ();
		self.element.html (el);
		self.signForm ();
		return self.element;
	});},
	get custom () {return __get__ (this, function (self, element) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'element': var element = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
			var content = tuple ([].slice.apply (arguments).slice (2, __ilastarg0__ + 1));
		}
		else {
			var content = tuple ();
		}
		self.content = content;
		if (self.has_captcha === true) {
			self.append (self._captcha_container);
		}
		self.append (self._buttons_container);
		var el = self.jquery ();
		self.element.html (el);
		self.signForm ();
		return self.element;
	});},
	get process_api_response () {return function (data) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (data.status == 400) {
			if (data.responseJSON.message !== undefined) {
				window.PhanterPWA.flash (__kwargtrans__ ({html: data.responseJSON.message}));
			}
			if (data.responseJSON.errors !== undefined) {
				var errors = dict (data.responseJSON.errors);
				for (var x of errors.py_keys ()) {
					var target = $ ('#phanterpwa-widget-socios-{0}'.format (x));
					target.find ('.phanterpwa-widget-message_error').text (data.responseJSON.errors [x]);
					target.find ('.phanterpwa-widget-wrapper').addClass ('has_error');
				}
			}
		}
		else if (data.status == 200) {
			if (data.responseJSON.message !== undefined) {
				window.PhanterPWA.flash (__kwargtrans__ ({html: data.responseJSON.message}));
			}
		}
	};}
});
export var ValidateForm =  __class__ ('ValidateForm', [object], {
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
		self.element_target = $ (target_selector);
		self.table_name = self.element_target.attr ('phanterpwa-form');
		self.submit_button = self.element_target.find ('#phanterpwa-widget-form-submit_button-{0}'.format (self.table_name));
		if (self.submit_button.length == 0) {
			self.submit_button = null;
		}
		else {
			self.submit_button.attr ('disabled', 'disabled');
		}
		if (__in__ ('submit_button', parameters)) {
			self.submit_button = $ (parameters ['submit_button']);
			if (self.submit_button.length == 0) {
				self.submit_button = null;
			}
			else {
				self.submit_button.attr ('disabled', 'disabled');
			}
		}
		self.formtests = list ();
		self.formpass = false;
		self.reload ();
	});},
	get _init_validate () {return __get__ (this, function (self, el) {
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
		var validate_test_pass = list ();
		var validate_test = list ($ (el).data ('validators'));
		var input_name = $ (el).attr ('name');
		var table_name = $ (el).data ('form');
		var value_for_validate = self.element_target.find ("input[name='{0}']".format (input_name)).val ();
		var is_empty_or = false;
		if (__in__ ('IS_EMPTY_OR', validate_test)) {
			if (value_for_validate === undefined || value_for_validate === null || value_for_validate == '') {
				validate_test_pass.append (true);
				var is_empty_or = true;
			}
			validate_test.py_pop ('IS_EMPTY_OR');
		}
		if (!(is_empty_or)) {
			for (var x of validate_test) {
				if (x !== null && x !== undefined) {
					validate_test_pass.append (self._validates (x, value_for_validate, el));
				}
			}
		}
		if (all (validate_test_pass)) {
			self.formtests.append (true);
			$ ('#phanterpwa-widget-{0}-{1}'.format (table_name, input_name)).find ('.phanterpwa-widget-wrapper').removeClass ('no_pass');
		}
		else {
			$ ('#phanterpwa-widget-{0}-{1}'.format (table_name, input_name)).find ('.phanterpwa-widget-wrapper').addClass ('no_pass').removeClass ('has_error');
			self.formtests.append (false);
		}
		if (all (self.formtests)) {
			self.formpass = true;
			if (self.submit_button !== null && self.submit_button !== undefined) {
				if (self.formpass) {
					self.submit_button.removeAttr ('disabled');
				}
				else {
					self.submit_button.attr ('disabled', 'disabled');
				}
			}
		}
		else if (self.submit_button !== null && self.submit_button !== undefined) {
			self.submit_button.attr ('disabled', 'disabled');
		}
	});},
	get _validates () {return __get__ (this, function (self, validate_name, value_for_validate, el) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'validate_name': var validate_name = __allkwargs0__ [__attrib0__]; break;
						case 'value_for_validate': var value_for_validate = __allkwargs0__ [__attrib0__]; break;
						case 'el': var el = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var validate_test_pass = list ();
		if (validate_name == 'PROGRAMMATICALLY') {
			if ($ (el) [0].hasAttribute ('phanterpwa-validate-programmatically')) {
				validate_test_pass.append (true);
			}
			else {
				validate_test_pass.append (false);
			}
		}
		if (validate_name.startswith ('IS_IN_SET:')) {
			var res = false;
			var list_options = JSON.parse (validate_name.__getslice__ (10, null, 1));
			if (list_options !== null || list_options !== undefined) {
				var list_options = JSON.parse (list_options);
				if (list_options.indexOf (value_for_validate) > -(1)) {
					var res = true;
				}
			}
			validate_test_pass.append (res);
		}
		if (validate_name == 'IS_NOT_EMPTY') {
			if (value_for_validate === undefined || value_for_validate === null || value_for_validate == '') {
				validate_test_pass.append (false);
			}
			else {
				validate_test_pass.append (true);
			}
		}
		if (validate_name == 'IS_ACTIVATION_CODE') {
			var is_activation_code = false;
			var res = validations.check_activation_code (value_for_validate);
			if (res !== null) {
				var is_activation_code = true;
			}
			validate_test_pass.append (is_activation_code);
		}
		if (validate_name.startswith ('IS_DATE')) {
			if (validate_name.startswith ('IS_DATE:')) {
				var dformat = validate_name.__getslice__ (8, null, 1);
				var res = validations.check_datetime (value_for_validate, dformat, 'date');
				validate_test_pass.append (res);
			}
			else if (validate_name.startswith ('IS_DATETIME:')) {
				var dformat = validate_name.__getslice__ (12, null, 1);
				var res = validations.check_datetime (value_for_validate, dformat, 'datetime');
				validate_test_pass.append (res);
			}
			else if (validate_name == 'IS_DATETIME') {
				var dformat = validate_name.__getslice__ (12, null, 1);
				var res = validations.check_datetime (value_for_validate);
				validate_test_pass.append (res);
			}
			else {
				var dformat = validate_name.__getslice__ (12, null, 1);
				var res = validations.check_datetime (value_for_validate, 'yyyy-MM-dd', 'date');
				validate_test_pass.append (res);
			}
		}
		if (validate_name.startswith ('IS_EQUALS') && __in__ (':', validate_name)) {
			var comp = $ (validate_name.__getslice__ (10, null, 1)).val ();
			if (comp === value_for_validate) {
				validate_test_pass.append (true);
			}
			else {
				validate_test_pass.append (false);
			}
		}
		if (validate_name.startswith ('MATCH:')) {
			var regex = new RegExp (validate_name.__getslice__ (6, null, 1));
			if (value_for_validate.match (regex) !== null) {
				validate_test_pass.append (true);
			}
			else {
				validate_test_pass.append (false);
			}
		}
		if (validate_name == 'IS_EMAIL') {
			if (__in__ ('@', value_for_validate)) {
				var REGEX_BODY = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([_a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
				if (REGEX_BODY.test (value_for_validate)) {
					validate_test_pass.append (true);
				}
				else {
					validate_test_pass.append (false);
				}
			}
			else {
				validate_test_pass.append (false);
			}
		}
		if (all (validate_test_pass)) {
			return true;
		}
		else {
			return false;
		}
	});},
	get _on_input_change () {return __get__ (this, function (self) {
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
		self.formtests = list ();
		var inputs_for_validate = self.element_target.find ('[data-validators]');
		inputs_for_validate.each ((function __lambda__ () {
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
			return self._init_validate (this);
		}));
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
		return self.element_target;
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
		if (self.element_target.length == 0) {
			console.error ('The {0} not exist'.format (self.target_selector));
		}
		self.element_target.off ('change.phanterpwaformvalidator, keyup.phanterpwaformvalidator').on ('change.phanterpwaformvalidator, keyup.phanterpwaformvalidator', (function __lambda__ () {
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
			return self._on_input_change ();
		}));
		self._on_input_change ();
		return self.element_target;
	});}
});

//# sourceMappingURL=phanterpwa.apptools.forms.map