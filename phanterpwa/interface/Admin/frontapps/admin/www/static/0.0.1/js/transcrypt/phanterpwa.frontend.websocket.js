// Transcrypt'ed from Python, 2021-03-15 14:32:36
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as helpers from './phanterpwa.frontend.helpers.js';
var __name__ = 'phanterpwa.frontend.websocket';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var H2 = helpers.XmlConstructor.tagger ('h2');
export var XML = helpers.XML;
export var TEXTAREA = helpers.XmlConstructor.tagger ('textarea');
export var WebSocketPhanterPWA =  __class__ ('WebSocketPhanterPWA', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, websocket_address) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'websocket_address': var websocket_address = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		self._opened = false;
		self.websocket_address = websocket_address;
		self.comulative_time = 300;
		self.last_ws = null;
		self.manual_connection = false;
		self.manual_close = false;
		self.onClose = null;
		self.onError = null;
		self.onMessage = null;
		self.onOpen = null;
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
			return self.start ();
		}), self.comulative_time);
	});},
	get send () {return __get__ (this, function (self, message) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'message': var message = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (self._opened) {
			self._authorization = window.PhanterPWA.get_authorization ();
			if (self._authorization !== null) {
				var msg = JSON.stringify ({'phanterpwa-authorization': self._authorization, 'message': message});
				self._ws.send (str ('{0}'.format (msg)));
				if (window.PhanterPWA.DEBUG) {
					if (message === 'command_online') {
						console.info ("__ Server, I'm online?");
					}
					else if (message === 'command_offline') {
						console.info ("__ Server, I'm stay offline. Bye.");
					}
				}
			}
			else if (!__in__ (message, ['command_online', 'command_offline'])) {
				var msg = JSON.stringify (message);
				self._ws.send (msg);
			}
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
		self.manual_close = true;
		self._ws.close ();
	});},
	get _onClose () {return __get__ (this, function (self, evt) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'evt': var evt = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self._opened = false;
		if (window.PhanterPWA.DEBUG) {
			console.info ('Closing websocket');
		}
		if (!(self.manual_close)) {
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
				return self.start ();
			}), self.comulative_time);
		}
		else {
			self.manual_close = false;
		}
		if (callable (self.onClose)) {
			self.onClose (evt);
		}
	});},
	get _onError () {return __get__ (this, function (self, evt) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'evt': var evt = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (window.PhanterPWA.DEBUG) {
			console.info ('Error on websocket', evt);
		}
		if (self.comulative_time > 9000 && !(self.manual_connection)) {
			window.PhanterPWA.flash ('Lost server connection!');
			self.manual_connection = true;
		}
		else {
			self.comulative_time = self.comulative_time + 1000;
		}
		if (callable (self.onError)) {
			self.onError (evt);
		}
	});},
	get _onMessage () {return __get__ (this, function (self, evt) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'evt': var evt = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (window.PhanterPWA.DEBUG) {
			console.info (evt.data);
		}
		if (callable (self.onMessage)) {
			self.onMessage (evt);
		}
	});},
	get _onOpen () {return __get__ (this, function (self, evt) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'evt': var evt = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.comulative_time = 0;
		self._opened = true;
		if (window.PhanterPWA.DEBUG) {
			console.info ('Opening websocket');
		}
		self.send ('command_online');
		if (callable (self.onOpen)) {
			self.onOpen (evt);
		}
	});},
	get _binds () {return __get__ (this, function (self) {
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
		self._ws.onopen = (function __lambda__ (evt) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'evt': var evt = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._onOpen (evt);
		});
		self._ws.onmessage = (function __lambda__ (evt) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'evt': var evt = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._onMessage (evt);
		});
		self._ws.onerror = (function __lambda__ (evt) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'evt': var evt = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._onError (evt);
		});
		self._ws.onclose = (function __lambda__ (evt) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'evt': var evt = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._onClose (evt);
		});
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
		if (!(self.manual_connection)) {
			self._ws = new WebSocket (self.websocket_address);
			self._authorization = window.PhanterPWA.get_authorization ();
			self._config = window.PhanterPWA.CONFIG;
			self._binds ();
		}
		else {
			var r = confirm ("It's try connect again?");
			if (r) {
				self.manual_connection = false;
				self.comulative_time = 0;
				self._ws = new WebSocket (self.websocket_address);
				self._authorization = window.PhanterPWA.get_authorization ();
				self._config = window.PhanterPWA.CONFIG;
				self._binds ();
			}
		}
	});}
});

//# sourceMappingURL=phanterpwa.frontend.websocket.map