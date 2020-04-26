// Transcrypt'ed from Python, 2020-04-24 14:03:52
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as application from './phanterpwa.apptools.application.js';
import * as helpers from './phanterpwa.apptools.helpers.js';
var __name__ = 'phanterpwa.apptools.components.events';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var Event =  __class__ ('Event', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, identifier) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'identifier': var identifier = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.identifier = identifier;
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
		if (window.PhanterPWA.DEBUG) {
			console.info ('The Event {0} reload'.format (self.identifier));
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
		if (window.PhanterPWA.DEBUG) {
			console.info ('The Component {0} starts'.format (self.identifier));
		}
	});}
});
export var WayHiperlinks =  __class__ ('WayHiperlinks', [Event], {
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
		Event.__init__ (self, 'WayHiperlinks');
	});},
	get _open_way () {return __get__ (this, function (self, el) {
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
		var r = application.WayRequest ();
		r.element = el;
		window.PhanterPWA.Request = r;
		r.open_way ($ (el).attr ('phanterpwa-way'));
	});},
	get _bind () {return __get__ (this, function (self, el, forced) {
		if (typeof forced == 'undefined' || (forced != null && forced.hasOwnProperty ("__kwargtrans__"))) {;
			var forced = false;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'el': var el = __allkwargs0__ [__attrib0__]; break;
						case 'forced': var forced = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var el = $ (el);
		if (!(window.PhanterPWA.check_event_namespace (el, 'click', 'phanterpwa-way')) || forced) {
			el.off ('click.phanterpwa-way').on ('click.phanterpwa-way', (function __lambda__ () {
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
				return self._open_way (this);
			}));
			if (window.PhanterPWA.DEBUG) {
				console.info ('Reload Event WayHiperlinks');
			}
		}
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
		self.start (__kwargtrans__ (context));
	});},
	get start () {return __get__ (this, function (self) {
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
		var target_selector = context.py_get ('selector', 'body');
		if ($ ('body').hasClass ('phanterpwa-lock')) {
			$ ('[phanterpwa-way]').off ('click.phanterpwa-way');
		}
		else {
			$ (target_selector).find ('[phanterpwa-way]').each ((function __lambda__ () {
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
				return self._bind (this);
			}));
		}
	});}
});
export var Waves =  __class__ ('Waves', [Event], {
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
		Event.__init__ (self, 'Waves');
	});},
	get _on_click () {return __get__ (this, function (self, el, ev) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'el': var el = __allkwargs0__ [__attrib0__]; break;
						case 'ev': var ev = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var el = $ (el);
		var pY = ev.pageY - el.offset ().top;
		var pX = ev.pageX - el.offset ().left;
		var wave = DIV (__kwargtrans__ ({_class: 'wave'})).jquery ();
		el.append (wave.css ('left', pX).css ('top', pY).animate (dict ({'top': pY - 300, 'left': pX - 300, 'width': 600, 'height': 600, 'opacity': 0}), 1000));
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
			return wave.remove ();
		}), 2000);
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
		self.start (__kwargtrans__ (context));
	});},
	get _bind () {return __get__ (this, function (self, el, forced) {
		if (typeof forced == 'undefined' || (forced != null && forced.hasOwnProperty ("__kwargtrans__"))) {;
			var forced = false;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'el': var el = __allkwargs0__ [__attrib0__]; break;
						case 'forced': var forced = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var el = $ (el);
		if (!(window.PhanterPWA.check_event_namespace (el, 'click', 'phanterpwa-event-wave')) || forced) {
			el.off ('click.phanterpwa-event-wave').on ('click.phanterpwa-event-wave', (function __lambda__ (event) {
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
				return self._on_click (this, event);
			}));
			if (window.PhanterPWA.DEBUG) {
				console.info ('Reload Event Wave');
			}
		}
	});},
	get start () {return __get__ (this, function (self) {
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
		var target_selector = context.py_get ('target', 'body');
		$ (target_selector).find ('.wave_on_click').each ((function __lambda__ () {
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
			return self._bind (this);
		}));
	});}
});
export var WidgetsInput =  __class__ ('WidgetsInput', [Event], {
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
		Event.__init__ (self, 'WidgetsInput');
		self.focus = false;
		self.has_val = null;
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
		for (var x of window.PhanterPWA.Request.widgets.py_keys ()) {
			window.PhanterPWA.Request.widgets [x]._reload ();
		}
	});},
	get _cleck_element () {return __get__ (this, function (self, instance) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'instance': var instance = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if ($ (instance.target_selector).length == 0) {
			return false;
		}
		return true;
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
		for (var x of window.PhanterPWA.Request.widgets.py_keys ()) {
			window.PhanterPWA.Request.widgets [x].start ();
		}
	});}
});

//# sourceMappingURL=phanterpwa.apptools.components.events.map