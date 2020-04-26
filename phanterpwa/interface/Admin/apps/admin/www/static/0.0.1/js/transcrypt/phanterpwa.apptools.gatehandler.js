// Transcrypt'ed from Python, 2020-04-25 02:44:25
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as helpers from './phanterpwa.apptools.helpers.js';
var __name__ = 'phanterpwa.apptools.gatehandler';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var IMG = helpers.XmlConstructor.tagger ('img', true);
export var I18N = helpers.I18N;
export var CONCATENATE = helpers.CONCATENATE;
export var Handler =  __class__ ('Handler', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, request) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'request': var request = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		self._request = request;
		self.debug = window.PhanterPWA.DEBUG;
		self.config = window.PhanterPWA.CONFIG;
		self._authorized_roles = parameters.py_get ('authorized_roles', 'all');
		self._authorized_users = parameters.py_get ('authorized_users', 'all');
		self._back = window.PhanterPWA.get_current_way ();
		self._status = 401;
		self._on_error = parameters.py_get ('on_error', null);
		self.auth_user = window.PhanterPWA.get_auth_user ();
		self._has_authorization = self.check_has_authorization ();
		if (self._has_authorization === true) {
			self.request = request;
			window.PhanterPWA.Response = self;
			self.initialize ();
			self.widgets_initialize ();
		}
		else if (callable (self._on_error)) {
			self._on_error (self._has_authorization, self);
		}
		else {
			self._on_credentials_fail ();
		}
	});},
	get stringify () {return __get__ (this, function (self) {
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
		var seen = [];
		var f = function (k, v) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'k': var k = __allkwargs0__ [__attrib0__]; break;
							case 'v': var v = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			if (v !== null && typeof v == 'object'
			) {
				var test = seen.indexOf(v) >= 0
				if (k.startswith ('_')) {
					return ;
				}
				else if (test) {
					return ;
				}
				seen.append (v);
			}
			return v;
		};
		return JSON.stringify (self, (function __lambda__ (k, v) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'k': var k = __allkwargs0__ [__attrib0__]; break;
							case 'v': var v = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return f (k, v);
		}));
	});},
	get _check_authorized_users () {return __get__ (this, function (self) {
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
		if (self._authorized_users == 'all') {
			return true;
		}
		else if (self._authorized_users == 'login') {
			if (self.auth_user !== null) {
				return true;
			}
		}
		else if (self._authorized_users == 'nologin') {
			if (self.auth_user === null) {
				return true;
			}
		}
		else if (isinstance (self._authorized_users, list)) {
			if (self.auth_user !== null && __in__ (int (self.auth_user.id), self._authorized_users)) {
				return true;
			}
		}
		return false;
	});},
	get _check_authorized_roles () {return __get__ (this, function (self) {
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
		if (self._authorized_roles == 'all') {
			return true;
		}
		else if (isinstance (self._authorized_roles, str) && self.auth_user !== null) {
			if (__in__ (self._authorized_roles, self.auth_user.roles)) {
				return true;
			}
		}
		else if (isinstance (self._authorized_roles, list)) {
			if (self.auth_user !== null && len (set (self.auth_user.roles).intersection (set (self.autorized_roles))) > 0) {
				return true;
			}
		}
		return false;
	});},
	get check_has_authorization () {return __get__ (this, function (self) {
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
		if (self._check_authorized_users () && self._check_authorized_roles ()) {
			return true;
		}
		else if (self.auth_user !== null) {
			if (self._authorized_users == 'nologin') {
				return 400;
			}
			else {
				return 403;
			}
		}
		return 401;
	});},
	get on_click_back_button () {return __get__ (this, function (self) {
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
		window.PhanterPWA.open_way (self._back);
	});},
	get _on_credentials_fail () {return __get__ (this, function (self) {
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
		window.PhanterPWA.open_code_way (self._has_authorization, self._request, self);
	});},
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
		if (window.PhanterPWA.DEBUG) {
			console.info ('method not used: Handler.initialize');
		}
	});},
	get widgets_initialize () {return __get__ (this, function (self) {
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
		for (var x of self.request.widgets.py_keys ()) {
			self.request.widgets [x].start ();
		}
	});}
});
export var ErrorHandler =  __class__ ('ErrorHandler', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, request, response) {
		if (typeof response == 'undefined' || (response != null && response.hasOwnProperty ("__kwargtrans__"))) {;
			var response = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'request': var request = __allkwargs0__ [__attrib0__]; break;
						case 'response': var response = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self._request = request;
		self.debug = window.PhanterPWA.DEBUG;
		self.requires_login = false;
		self.autorized_roles = ['all'];
		self.autorized_ids = ['all'];
		self.way_on_back = window.PhanterPWA.get_current_way ();
		self.initialize ();
		self._credentials = true;
		if (self._credentials === true) {
			window.PhanterPWA.Response = response;
			self.start ();
		}
		else {
			self.on_credentials_fail ();
		}
	});},
	get on_click_back_button () {return __get__ (this, function (self) {
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
		window.PhanterPWA.open_way (self.way_on_back);
	});},
	get on_credentials_fail () {return __get__ (this, function (self) {
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
		if (self.debug) {
			console.info ('method not used: ErrorHandler.on_credentials_fail()');
		}
	});},
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
		if (self.debug) {
			console.info ('method not used: ErrorHandler.initialize()');
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
		if (self.debug) {
			console.info ('method not used: ErrorHandler.start()');
		}
	});}
});
export var html_base = CONCATENATE (DIV (DIV (DIV (DIV (I18N ('Ops!!!', __kwargtrans__ (dict ({'_pt-br': 'Ops!!!'}))), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'phanterpwa-container container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (DIV (DIV (DIV (DIV (IMG (__kwargtrans__ ({_class: 'image-warnings'})), __kwargtrans__ ({_class: 'image-warnings-container'})), DIV (__kwargtrans__ ({_id: 'content-warning'})), __kwargtrans__ ({_class: 'content-warnings'})), __kwargtrans__ ({_class: 'warnings-container phanterpwa-card-container'})), __kwargtrans__ ({_class: 'card'})), __kwargtrans__ ({_class: 'new-container'})), __kwargtrans__ ({_class: 'phanterpwa-container container'})));
export var Error_404 =  __class__ ('Error_404', [ErrorHandler], {
	__module__: __name__,
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
		var html = html_base.jquery ();
		html.find ('.image-warnings').attr ('src', '/static/{0}/images/warning.png'.format (window.PhanterPWA.VERSION));
		html.find ('#content-warning').html ('ERROR 404 - Not Found');
		$ ('#main-container').html (html);
	});}
});
export var Error_401 =  __class__ ('Error_401', [ErrorHandler], {
	__module__: __name__,
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
		var html = html_base.jquery ();
		html.find ('.image-warnings').attr ('src', '/static/{0}/images/warning.png'.format (window.PhanterPWA.VERSION));
		html.find ('#content-warning').html ('ERROR 401 - Unauthorized');
		$ ('#main-container').html (html);
	});}
});
export var Error_403 =  __class__ ('Error_403', [ErrorHandler], {
	__module__: __name__,
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
		var html = html_base.jquery ();
		html.find ('.image-warnings').attr ('src', '/static/{0}/images/warning.png'.format (window.PhanterPWA.VERSION));
		html.find ('#content-warning').html ('ERROR 403 - Forbidden');
		$ ('#main-container').html (html);
	});}
});
export var Error_502 =  __class__ ('Error_502', [ErrorHandler], {
	__module__: __name__,
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
		var html = html_base.jquery ();
		html.find ('.image-warnings').attr ('src', '/static/{0}/images/warning.png'.format (window.PhanterPWA.VERSION));
		html.find ('#content-warning').html ('ERROR 502 - Bad Gateway');
		$ ('#main-container').html (html);
	});}
});
export var Error_500 =  __class__ ('Error_500', [ErrorHandler], {
	__module__: __name__,
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
		var html = html_base.jquery ();
		html.find ('.image-warnings').attr ('src', '/static/{0}/images/warning.png'.format (window.PhanterPWA.VERSION));
		html.find ('#content-warning').html ('ERROR 500 - Internal Error');
		$ ('#main-container').html (html);
	});}
});

//# sourceMappingURL=phanterpwa.apptools.gatehandler.map