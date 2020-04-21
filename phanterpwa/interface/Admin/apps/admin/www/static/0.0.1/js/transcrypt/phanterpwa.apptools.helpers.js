// Transcrypt'ed from Python, 2020-04-20 12:49:17
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'phanterpwa.apptools.helpers';
export var XmlConstructor =  __class__ ('XmlConstructor', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, tag, singleton) {
		var attributes = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'tag': var tag = __allkwargs0__ [__attrib0__]; break;
						case 'singleton': var singleton = __allkwargs0__ [__attrib0__]; break;
						default: attributes [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete attributes.__kwargtrans__;
			}
			var content = tuple ([].slice.apply (arguments).slice (3, __ilastarg0__ + 1));
		}
		else {
			var content = tuple ();
		}
		self.tag = tag;
		self.singleton = singleton;
		self.content = content;
		self.attributes = attributes;
		self.__jquery_object = '';
	});},
	get _get_tag () {return __get__ (this, function (self) {
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
		return self._tag;
	});},
	get _set_tag () {return __get__ (this, function (self, tag) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'tag': var tag = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self._tag = tag;
	});},
	get _get_singleton () {return __get__ (this, function (self) {
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
		return self._singleton;
	});},
	get append () {return __get__ (this, function (self, value) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'value': var value = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.content.append (value);
	});},
	get insert () {return __get__ (this, function (self, pos, value) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'pos': var pos = __allkwargs0__ [__attrib0__]; break;
						case 'value': var value = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.content.insert (pos, value);
	});},
	get _set_singleton () {return __get__ (this, function (self, singleton) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'singleton': var singleton = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (isinstance (singleton, bool)) {
			self._singleton = singleton;
		}
		else {
			var __except0__ = py_TypeError ('The singleton must be bool, given: {0}'.format (str (singleton)));
			__except0__.__cause__ = null;
			throw __except0__;
		}
	});},
	get xml () {return __get__ (this, function (self) {
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
		if (self.singleton === true) {
			self.__jquery_object = $ ('<{0}>'.format (self.tag));
		}
		else {
			self.__jquery_object = $ ('<{0}></{0}>'.format (str (self.tag)));
			for (var c of self.content) {
				if (isinstance (c, str)) {
					self.__jquery_object.append ($ ('<div/>').text (c).html ());
				}
				else if (isinstance (c, XmlConstructor)) {
					self.__jquery_object.append (c.jquery ());
				}
				else {
					self.__jquery_object.append (c);
				}
			}
		}
		for (var t of self.attributes.py_keys ()) {
			if (t.startswith ('_')) {
				if (self.attributes [t] !== null && self.attributes [t] !== undefined) {
					self.__jquery_object.attr (t.__getslice__ (1, null, 1), self.attributes [t]);
				}
			}
		}
		return self.__jquery_object [0].outerHTML;
	});},
	get __str__ () {return __get__ (this, function (self) {
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
		return self.xml ();
	});},
	get jquery () {return __get__ (this, function (self) {
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
		self.xml ();
		return self.__jquery_object;
	});},
	get html_to () {return __get__ (this, function (self, py_selector) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'py_selector': var py_selector = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.xml ();
		var el = $ (py_selector).html (self.__jquery_object);
		if (window.PhanterPWA !== undefined) {
			window.PhanterPWA.reload_events (__kwargtrans__ ({py_selector: self.__jquery_object}));
		}
		return el;
	});},
	get text_to () {return __get__ (this, function (self, py_selector) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'py_selector': var py_selector = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.xml ();
		return $ (py_selector).text (self.__jquery_object);
	});},
	get append_to () {return __get__ (this, function (self, py_selector) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'py_selector': var py_selector = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.xml ();
		var el = $ (py_selector).append (self.__jquery_object);
		if (window.PhanterPWA !== undefined) {
			window.PhanterPWA.reload_events (__kwargtrans__ ({py_selector: self.__jquery_object}));
		}
		return el;
	});},
	get insert_to () {return __get__ (this, function (self, py_selector, position) {
		if (typeof position == 'undefined' || (position != null && position.hasOwnProperty ("__kwargtrans__"))) {;
			var position = 0;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'py_selector': var py_selector = __allkwargs0__ [__attrib0__]; break;
						case 'position': var position = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.xml ();
		var target = $ (py_selector);
		var last_index = target.children ().size ();
		if (position < 0) {
			var position = max (0, (last_index + 1) + position);
		}
		target.append (self.__jquery_object);
		if (position < last_index) {
			target.children ().eq (position).before (target.children ().last ());
		}
		var el = target;
		if (window.PhanterPWA !== undefined) {
			window.PhanterPWA.reload_events (__kwargtrans__ ({py_selector: self.__jquery_object}));
		}
		return el;
	});},
	get tagger () {return function (tag, singleton) {
		if (typeof singleton == 'undefined' || (singleton != null && singleton.hasOwnProperty ("__kwargtrans__"))) {;
			var singleton = false;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'tag': var tag = __allkwargs0__ [__attrib0__]; break;
						case 'singleton': var singleton = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		return (function __lambda__ () {
			var attributes = dict ();
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							default: attributes [__attrib0__] = __allkwargs0__ [__attrib0__];
						}
					}
					delete attributes.__kwargtrans__;
				}
				var content = tuple ([].slice.apply (arguments).slice (0, __ilastarg0__ + 1));
			}
			else {
				var content = tuple ();
			}
			return XmlConstructor (tag, singleton, ...content, __kwargtrans__ (attributes));
		});
	};}
});
Object.defineProperty (XmlConstructor, 'singleton', property.call (XmlConstructor, XmlConstructor._get_singleton, XmlConstructor._set_singleton));
Object.defineProperty (XmlConstructor, 'tag', property.call (XmlConstructor, XmlConstructor._get_tag, XmlConstructor._set_tag));;
export var I18N =  __class__ ('I18N', [XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		var attributes = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						default: attributes [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete attributes.__kwargtrans__;
			}
			var content = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
		}
		else {
			var content = tuple ();
		}
		for (var x of content) {
			if (!(isinstance (x, str))) {
				var __except0__ = ValueError ('The I18N content must be string type');
				__except0__.__cause__ = null;
				throw __except0__;
			}
		}
		var str_content = ''.join (content);
		attributes ['_phanterpwa-i18n'] = str_content;
		var sanitize = attributes.py_get ('sanitize', true);
		if (sanitize === false) {
			attributes ['_phanterpwa-i18n-sanitize'] = false;
		}
		XmlConstructor.__init__ (self, 'span', false, str_content, __kwargtrans__ (attributes));
	});}
});
export var XSECTION =  __class__ ('XSECTION', [XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
			var content = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
		}
		else {
			var content = tuple ();
		}
		var DIV = XmlConstructor.tagger ('div');
		if (__in__ ('_class', parameters)) {
			parameters ['_class'] = '{0}{1}'.format (parameters ['_class'], ' phanterpwa-xsection-container');
		}
		else {
			parameters ['_class'] = 'phanterpwa-xsection-container';
		}
		self.__child_html = DIV (...content, __kwargtrans__ ({_class: 'phanterpwa-xsection'}));
		XmlConstructor.__init__ (self, 'div', false, self.__child_html, __kwargtrans__ (parameters));
	});},
	get append () {return __get__ (this, function (self, value) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'value': var value = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.__child_html.content.append (value);
	});},
	get insert () {return __get__ (this, function (self, pos, value) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'pos': var pos = __allkwargs0__ [__attrib0__]; break;
						case 'value': var value = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.__child_html.content.insert (pos, value);
	});}
});
export var XTABLE =  __class__ ('XTABLE', [XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
			var content = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
		}
		else {
			var content = tuple ();
		}
		var TABLE = XmlConstructor.tagger ('table');
		if (__in__ ('_class', parameters)) {
			parameters ['_class'] = '{0}{1}'.format (parameters ['_class'], ' phanterpwa-xtable-container');
		}
		else {
			parameters ['_class'] = 'phanterpwa-xtable-container';
		}
		self.__child_html = TABLE (...content, __kwargtrans__ ({_class: 'phanterpwa-xtable p-row'}));
		XmlConstructor.__init__ (self, 'div', false, self.__child_html, __kwargtrans__ (parameters));
	});},
	get append () {return __get__ (this, function (self, value) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'value': var value = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.__child_html.content.append (value);
	});},
	get insert () {return __get__ (this, function (self, pos, value) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'pos': var pos = __allkwargs0__ [__attrib0__]; break;
						case 'value': var value = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.__child_html.content.insert (pos, value);
	});}
});
export var XTRH =  __class__ ('XTRH', [XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
			var content = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
		}
		else {
			var content = tuple ();
		}
		var TH = XmlConstructor.tagger ('th');
		if (__in__ ('_class', parameters)) {
			parameters ['_class'] = '{0}{1}'.format (parameters ['_class'], ' phanterpwa-xtable-xtrh');
		}
		else {
			parameters ['_class'] = 'phanterpwa-xtable-xtrh';
		}
		self.__child_html = CONCATENATE ();
		for (var x of content) {
			self.__child_html.append (TH (x, __kwargtrans__ ({_class: 'phanterpwa-xtable-xtrh-th'})));
		}
		XmlConstructor.__init__ (self, 'tr', false, self.__child_html, __kwargtrans__ (parameters));
	});},
	get append () {return __get__ (this, function (self, value) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'value': var value = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var TH = XmlConstructor.tagger ('th');
		self.__child_html.content.append (TH (value, __kwargtrans__ ({_class: 'phanterpwa-xtable-xtrh-th'})));
	});},
	get insert () {return __get__ (this, function (self, pos, value) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'pos': var pos = __allkwargs0__ [__attrib0__]; break;
						case 'value': var value = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var TH = XmlConstructor.tagger ('th');
		self.__child_html.content.insert (pos, TH (value, __kwargtrans__ ({_class: 'phanterpwa-xtable-xtrh-th'})));
	});}
});
export var XTRD =  __class__ ('XTRD', [XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
			var content = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
		}
		else {
			var content = tuple ();
		}
		self.__dropable = parameters.py_get ('drag_and_drop', true);
		if (self.__dropable) {
			parameters ['_draggable'] = 'true';
		}
		var TD = XmlConstructor.tagger ('td');
		if (__in__ ('_class', parameters)) {
			parameters ['_class'] = '{0}{1}'.format (parameters ['_class'], ' phanterpwa-xtable-xtrd');
		}
		else {
			parameters ['_class'] = 'phanterpwa-xtable-xtrd';
		}
		self.__child_html = CONCATENATE ();
		for (var x of content) {
			self.__child_html.append (TD (x, __kwargtrans__ ({_class: 'phanterpwa-xtable-xtrd-td'})));
		}
		XmlConstructor.__init__ (self, 'tr', false, self.__child_html, __kwargtrans__ (parameters));
	});},
	get __ondragstart () {return __get__ (this, function (self, el) {
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
		window.PhanterPWA.drag = $ (el) [0].outerHTML;
	});},
	get __ondrop () {return __get__ (this, function (self, el) {
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
		$ (el).insertAfter (window.PhanterPWA.drag);
	});},
	get append () {return __get__ (this, function (self, value) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'value': var value = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var TD = XmlConstructor.tagger ('td');
		self.__child_html.content.append (TD (value, __kwargtrans__ ({_class: 'phanterpwa-xtable-xtrd-td'})));
	});},
	get insert () {return __get__ (this, function (self, pos, value) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'pos': var pos = __allkwargs0__ [__attrib0__]; break;
						case 'value': var value = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var TD = XmlConstructor.tagger ('td');
		self.__child_html.content.insert (pos, TD (value, __kwargtrans__ ({_class: 'phanterpwa-xtable-xtrd-td'})));
	});}
});
export var XML =  __class__ ('XML', [XmlConstructor], {
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
			var content = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
		}
		else {
			var content = tuple ();
		}
		XmlConstructor.__init__ (self, '', false, ...content);
	});},
	get xml () {return __get__ (this, function (self) {
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
		var html = '';
		for (var c of self.content) {
			if (isinstance (c, str)) {
				html += c;
			}
			else if (isinstance (c, XmlConstructor)) {
				html += c.xml ();
			}
			else {
				html += c;
			}
		}
		self.__jquery_object = html;
		return html;
	});},
	get jquery () {return __get__ (this, function (self) {
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
		var html = self.xml ();
		return html;
	});}
});
export var CONCATENATE =  __class__ ('CONCATENATE', [XmlConstructor], {
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
			var content = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
		}
		else {
			var content = tuple ();
		}
		XmlConstructor.__init__ (self, '', false, ...content);
	});},
	get xml () {return __get__ (this, function (self) {
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
		var html = '';
		for (var c of self.content) {
			if (isinstance (c, str)) {
				html += $ ('<div/>').text (c).html ();
			}
			else if (isinstance (c, XmlConstructor)) {
				html += c.xml ();
			}
			else {
				html += c;
			}
		}
		self.__jquery_object = $ (html);
		return html;
	});},
	get jquery () {return __get__ (this, function (self) {
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
		var html = self.xml ();
		return $ (html);
	});}
});

//# sourceMappingURL=phanterpwa.apptools.helpers.map