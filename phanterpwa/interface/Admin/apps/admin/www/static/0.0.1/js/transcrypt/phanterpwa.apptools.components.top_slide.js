// Transcrypt'ed from Python, 2020-03-29 19:45:27
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as helpers from './phanterpwa.frontend.helpers.js';
var __name__ = 'phanterpwa.frontend.components.top_slide';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var I = helpers.XmlConstructor.tagger ('i');
export var TopSlide =  __class__ ('TopSlide', [helpers.XmlConstructor], {
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
			var content = tuple ([].slice.apply (arguments).slice (2, __ilastarg0__ + 1));
		}
		else {
			var content = tuple ();
		}
		self.target_selector = target_selector;
		self.element_target = $ (self.target_selector);
		self._after_open = null;
		if (__in__ ('after_open', parameters)) {
			self._after_open = parameters ['after_open'];
		}
		if (!__in__ ('_id', parameters)) {
			parameters ['_id'] = 'phanterpwa-component-topslide-wrapper';
		}
		if (__in__ ('_class', parameters)) {
			parameters ['_class'] = '{0}{1}'.format (parameters ['_class'].strip (), ' phanterpwa-component-topslide-wrapper');
		}
		else {
			parameters ['_class'] = 'phanterpwa-component-topslide-wrapper';
		}
		content.insert (0, DIV (I (__kwargtrans__ ({_class: 'fas fa-times'})), __kwargtrans__ ({_class: 'phanterpwa-component-topslide-close link'})));
		helpers.XmlConstructor.__init__ (self, 'div', false, ...content, __kwargtrans__ (parameters));
	});},
	get py_switch () {return __get__ (this, function (self) {
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
		if (self.element_target.find ('#phanterpwa-component-topslide-wrapper').hasClass ('enabled')) {
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
		self.element_target = $ (self.target_selector);
		self.element_target.find ('#phanterpwa-component-topslide-wrapper').slideUp ();
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
		self.element_target = $ (self.target_selector);
		self.start ();
		self.element_target.find ('#phanterpwa-component-topslide-wrapper').slideDown ();
		if (self._after_open !== null && self._after_open !== undefined) {
			self._after_open (self.element_target.find ('#phanterpwa-component-topslide-wrapper'));
		}
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
		if (self.element_target !== null && self.element_target !== undefined) {
			self.element_target.find ('#phanterpwa-component-topslide-wrapper').remove ();
			self.append_to (self.element_target);
			self.element_target.find ('.phanterpwa-component-topslide-close').off ('click.phanterpwa_component_topslide_close').on ('click.phanterpwa_component_topslide_close', self.close);
		}
	});}
});

//# sourceMappingURL=phanterpwa.frontend.components.top_slide.map