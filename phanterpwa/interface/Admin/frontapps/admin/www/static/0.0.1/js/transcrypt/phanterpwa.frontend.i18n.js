// Transcrypt'ed from Python, 2021-03-10 09:46:30
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'phanterpwa.frontend.i18n';
export var I18NServer =  __class__ ('I18NServer', [object], {
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
		self.storage = self.load_storage ();
		self.userLang = self.get_user_lang ();
		self.get_translations_on_server ();
	});},
	get load_storage () {return function (self) {
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
		var result = dict (__kwargtrans__ ({default_lang: null}));
		var t = localStorage.getItem ('phanterpwa_i18n');
		if (t !== null && t !== undefined) {
			try {
				var t = JSON.parse (t);
				var result = t;
			}
			catch (__except0__) {
				if (isinstance (__except0__, Exception)) {
					localStorage.removeItem ('phanterpwa_i18n');
					console.error ('the phanterpwa_i18n is corrupted');
				}
				else {
					throw __except0__;
				}
			}
		}
		else {
			localStorage.setItem ('phanterpwa_i18n', JSON.stringify (window.PhanterPWA.CONFIG ['I18N']));
			var result = window.PhanterPWA.CONFIG ['I18N'];
		}
		return result;
	};},
	get save_storage () {return __get__ (this, function (self) {
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
		localStorage.setItem ('phanterpwa_i18n', JSON.stringify (self.storage));
	});},
	get set_default_user_lang () {return __get__ (this, function (self, lang) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'lang': var lang = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.storage ['default_lang'] = lang;
		self.save_storage ();
	});},
	get get_user_lang () {return function () {
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
		var userLang = navigator.language || navigator.userLanguage;
		var storage = I18NServer.load_storage () ['default_lang'];
		if (__in__ ('default_lang', storage)) {
			var userLang = storage ['default_lang'];
		}
		return userLang;
	};},
	get after_get_translations () {return __get__ (this, function (self, data, ajax_status) {
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
			var default_lang = self.storage ['default_lang'];
			self.storage = json;
			if (default_lang === null || default_lang === undefined) {
				self.storage ['default_lang'] = default_lang;
			}
			self.save_storage (self);
		}
	});},
	get get_translations_on_server () {return __get__ (this, function (self, new_word) {
		if (typeof new_word == 'undefined' || (new_word != null && new_word.hasOwnProperty ("__kwargtrans__"))) {;
			var new_word = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'new_word': var new_word = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (window.PhanterPWA !== undefined) {
			if (window.PhanterPWA.DEBUG) {
				window.PhanterPWA.ApiServer.GET (__kwargtrans__ (dict ({'url_args': ['api', 'i18n', window.PhanterPWA.get_app_name ()], 'url_vars': dict ({'lang': self.userLang, 'new_word': new_word}), 'onComplete': self.after_get_translations})));
			}
		}
	});},
	get translate () {return __get__ (this, function (self, wordkey) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'wordkey': var wordkey = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (__in__ (self.userLang, self.storage)) {
			if (__in__ (wordkey, self.storage [self.userLang])) {
				return self.storage [self.userLang] [wordkey];
			}
		}
		self.get_translations_on_server (wordkey);
		return wordkey;
	});},
	get DOMTranslate () {return __get__ (this, function (self, target) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'target': var target = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.target = $ (target);
		var eachElement = function (el) {
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
			var t_elem = $ (el);
			var sanitize = t_elem.attr ('phanterpwa-i18n-sanitize');
			var word = t_elem.attr ('phanterpwa-i18n');
			if (word !== null && word !== undefined) {
				if (t_elem [0].hasAttribute (self.userLang)) {
					if (sanitize !== null && sanitize !== undefined && str (sanitize).upper () == 'FALSE') {
						t_elem.html (t_elem.attr (self.userLang));
					}
					else {
						t_elem.text (t_elem.attr (self.userLang));
					}
				}
				else {
					var translate = self.translate (word);
					t_elem.attr (self.userLang, translate);
					if (sanitize !== null && sanitize !== undefined && str (sanitize).upper () == 'FALSE') {
						t_elem.html (translate);
					}
					else {
						t_elem.text (translate);
					}
				}
			}
		};
		if (self.target [0] !== undefined) {
			self.target.find ('span[phanterpwa-i18n]').each ((function __lambda__ () {
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
				return eachElement (this);
			}));
		}
		return self.target;
	});}
});

//# sourceMappingURL=phanterpwa.frontend.i18n.map