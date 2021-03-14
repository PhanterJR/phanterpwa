// Transcrypt'ed from Python, 2021-03-10 09:46:21
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as helpers from './phanterpwa.frontend.helpers.js';
var __name__ = 'phanterpwa.frontend.components.modal';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var FORM = helpers.XmlConstructor.tagger ('form');
export var I = helpers.XmlConstructor.tagger ('i');
export var CONCATENATE = helpers.CONCATENATE;
export var Modal =  __class__ ('Modal', [object], {
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
		self.target_element = $ (target_selector);
		self.title = '';
		self.content = '';
		self.footer = '';
		self.header_height = 80;
		self.footer_height = 80;
		self._max_content_height = 400;
		self._form = parameters.py_get ('form', null);
		if (__in__ ('title', parameters)) {
			self.title = parameters ['title'];
		}
		if (__in__ ('content', parameters)) {
			self.content = parameters ['content'];
		}
		if (__in__ ('footer', parameters)) {
			self.footer = parameters ['footer'];
		}
		if (__in__ ('header_height', parameters)) {
			self.header_height = parameters ['header_height'];
		}
		if (__in__ ('footer_height', parameters)) {
			self.footer_height = parameters ['footer_height'];
		}
		if (__in__ ('_class', parameters)) {
			parameters ['_class'] = '{0}{1}'.format (parameters ['_class'].strip (), ' phanterpwa-component-modal-wrapper phanterpwa-container');
		}
		else {
			parameters ['_class'] = 'phanterpwa-component-modal-wrapper phanterpwa-container';
		}
		if (__in__ ('after_open', parameters)) {
			self._after_open = parameters ['after_open'];
		}
		self._z_index = parameters.py_get ('z_index', 1006);
		var wrapper_content = CONCATENATE (DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-times'})), __kwargtrans__ ({_class: 'phanterpwa-component-modal-close link'})), DIV (self.title, __kwargtrans__ ({_class: 'phanterpwa-component-modal-title'})), __kwargtrans__ ({_class: 'phanterpwa-component-modal-header-container'})), DIV (self.content, __kwargtrans__ ({_class: 'phanterpwa-component-modal-content-container'})), DIV (self.footer, __kwargtrans__ ({_class: 'phanterpwa-component-modal-footer-container'})));
		if (self._form !== null) {
			if (__in__ (['_class'], parameters)) {
				parameters ['_class'] = '{0}{1}'.format (parameters ['_class'], ' phanterpwa-form');
			}
			else {
				parameters ['_class'] = 'phanterpwa-form';
			}
			parameters ['_id'] = 'form-{0}'.format (self._form);
			parameters ['_phanterpwa-form'] = self._form;
			self.modal_wrapper = FORM (wrapper_content, __kwargtrans__ (parameters));
		}
		else {
			self.modal_wrapper = DIV (wrapper_content, __kwargtrans__ (parameters));
		}
		self.modal_container = DIV (DIV (DIV (DIV (DIV (self.modal_wrapper, __kwargtrans__ ({_class: 'phanterpwa-centralizer-center'})), __kwargtrans__ ({_class: 'phanterpwa-centralizer-horizontal'})), __kwargtrans__ ({_class: 'phanterpwa-centralizer-vertical'})), __kwargtrans__ ({_class: 'phanterpwa-centralizer-wrapper'})), __kwargtrans__ ({_class: 'phanterpwa-component-modal-container phanterpwa-fixed-fulldisplay', _style: 'z-index: {0}'.format (self._z_index)}));
	});},
	get switch_modal () {return __get__ (this, function (self) {
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
		var modal_container = $ (self.target_selector).find ('.phanterpwa-component-modal-container');
		if (modal_container.hasClass ('enabled')) {
			self.close ();
		}
		else {
			self.open ();
		}
	});},
	get close () {return __get__ (this, function (self) {
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
		var modal_container = $ (self.target_selector).find ('.phanterpwa-component-modal-container');
		modal_container.addClass ('closing');
		setTimeout ((function __lambda__ () {
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
			return modal_container.removeClass ('enabled');
		}), 500);
	});},
	get _close_on_click_container () {return __get__ (this, function (self, event, target_element) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						case 'target_element': var target_element = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (event.target === target_element) {
			self.close ();
		}
	});},
	get open () {return __get__ (this, function (self) {
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
		var modal_container = $ (self.target_selector).find ('.phanterpwa-component-modal-container');
		modal_container.addClass ('enabled');
		if (callable (self._after_open)) {
			self._after_open (modal_container);
		}
		var change_position_and_zindex = function (el) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'el': var el = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			var widget_name = $ (el).attr ('phanterpwa-widget');
			var widget = window.PhanterPWA.Request.widgets.py_get (widget_name, null);
			if (widget !== null) {
				if (callable (widget.set_z_index)) {
					widget.set_z_index (self._z_index + 1);
				}
				if (callable (widget.set_recalc_on_scroll)) {
					widget.set_recalc_on_scroll (true);
				}
			}
		};
		modal_container.find ('[phanterpwa-widget]').each ((function __lambda__ () {
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
			return change_position_and_zindex (this);
		}));
	});},
	get _calc_content_height () {return __get__ (this, function (self) {
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
		var h = $ (window).height ();
		self._max_content_height = ((h - self.header_height) - self.footer_height) - 20;
		if (h <= 0) {
			var h = 0;
		}
		self.target_element = $ (self.target_selector);
		self.target_element.find ('.phanterpwa-component-modal-header-container').css ('height', self.header_height);
		self.target_element.find ('.phanterpwa-component-modal-wrapper').css ('padding-bottom', self.footer_height).css ('padding-top', self.header_height);
		self.target_element.find ('.phanterpwa-component-modal-footer-container').css ('height', self.footer_height);
		self.target_element.find ('.phanterpwa-component-modal-content-container').css ('max-height', self._max_content_height);
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
		self.target_element = $ (self.target_selector);
		self.target_element.find ('.phanterpwa-component-modal-container.phanterpwa-fixed-fulldisplay').remove ();
		self.modal_container.append_to (self.target_selector);
		self._calc_content_height ();
		$ (window).resize ((function __lambda__ () {
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
			return self._calc_content_height ();
		}));
		self.target_element.find ('.phanterpwa-centralizer-horizontal').off ('click.phanterpwa-component-modal-container').on ('click.phanterpwa-component-modal-container', (function __lambda__ (e) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'e': var e = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._close_on_click_container (e, this);
		}));
		self.target_element.find ('.phanterpwa-centralizer-center').off ('click.phanterpwa-component-modal-container').on ('click.phanterpwa-component-modal-container', (function __lambda__ (e) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'e': var e = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._close_on_click_container (e, this);
		}));
		self.target_element.find ('.phanterpwa-component-modal-close').off ('click.phanterpwa-component-modal-container').on ('click.phanterpwa-component-modal-container', self.close);
	});}
});

//# sourceMappingURL=phanterpwa.frontend.components.modal.map