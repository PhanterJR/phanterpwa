// Transcrypt'ed from Python, 2021-03-15 14:32:35
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as validations from './phanterpwa.frontend.validations.js';
import * as websocket from './phanterpwa.frontend.websocket.js';
import * as modal from './phanterpwa.frontend.components.modal.js';
import * as gatehandler from './phanterpwa.frontend.gatehandler.js';
import * as events from './phanterpwa.frontend.components.events.js';
import * as widgets from './phanterpwa.frontend.components.widgets.js';
import * as helpers from './phanterpwa.frontend.helpers.js';
import * as i18n from './phanterpwa.frontend.i18n.js';
import * as progressbar from './phanterpwa.frontend.progressbar.js';
import * as server from './phanterpwa.frontend.server.js';
var __name__ = 'phanterpwa.frontend.application';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var H2 = helpers.XmlConstructor.tagger ('h2');
export var XML = helpers.XML;
export var TEXTAREA = helpers.XmlConstructor.tagger ('textarea');
export var I = helpers.XmlConstructor.tagger ('i');
export var PhanterPWA =  __class__ ('PhanterPWA', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, config, gates) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'config': var config = __allkwargs0__ [__attrib0__]; break;
						case 'gates': var gates = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		self.get_inicial_config_uri ();
		self.initialize ();
		self._thewidgets = dict ();
		if (config === undefined || config === null) {
			var __except0__ = ValueError ('The config is required');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (gates === undefined || gates === null) {
			var __except0__ = ValueError ('The gates is required');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		self.CONFIG = config;
		self.NAME = config.PROJECT.py_name;
		self.TITLE = config.PROJECT.title;
		self.VERSION = config.PROJECT.version;
		self.COMPILATION = config.PROJECT.compilation;
		self.AUTHOR = config.PROJECT.author;
		self.DEBUG = config.PROJECT.debug;
		self.Gates = dict (gates);
		self.ProgressBar = progressbar.ProgressBar ('#main-progress-bar-container');
		self.Request = WayRequest ();
		self.Components = dict ({});
		self.Events = dict ({});
		self.Cache = dict ({});
		self.Response = null;
		self.default_way = parameters.py_get ('default_way', 'home');
		self._after_open_way = parameters.py_get ('after_open_way', null);
		self.counter = 0;
		self.states = dict ();
		self._social_login_icons = dict ({'google': I (__kwargtrans__ ({_class: 'fab fa-google'})), 'facebook': I (__kwargtrans__ ({_class: 'fab fa-facebook'})), 'twitter': I (__kwargtrans__ ({_class: 'fab fa-twitter'}))});
		window.PhanterPWA = self;
		window.onpopstate = self._onPopState;
		self._onPopState ();
		if (self.DEBUG) {
			console.info ('starting {0} application (version: {1}, compilation: {2})'.format (self.CONFIG.PROJECT.title, self.CONFIG.PROJECT.version, self.CONFIG.PROJECT.compilation));
		}
		self.add_event (events.Waves ());
		self.add_event (events.WayHiperlinks ());
		self.ApiServer = server.ApiServer ();
		self.ApiServer.getClientToken ();
		self.I18N = i18n.I18NServer ();
		self.WS = websocket.WebSocketPhanterPWA (self.CONFIG ['APP'] ['websocket_address']);
		if (self.DEBUG) {
			self.add_component (Developer_Toolbar ());
		}
		self.Valider = validations.Valid;
	});},
	get check_event_namespace () {return function (el, event_name, namespace) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'el': var el = __allkwargs0__ [__attrib0__]; break;
						case 'event_name': var event_name = __allkwargs0__ [__attrib0__]; break;
						case 'namespace': var namespace = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var element = $ (el);
		if (element.length > 0) {
			if (element.length == 1) {
				var obj_events = $._data (element [0], 'events');
				if (obj_events !== undefined) {
					var event_list = obj_events [event_name];
					if (isinstance (event_list, list)) {
						for (var x of event_list) {
							var ns = x.namespace;
							if (ns !== undefined && ns == namespace) {
								return true;
							}
						}
					}
				}
			}
			else {
				console.error ('check_event_namespace must be used in jquery selectors with', 'an element like when using the id selector');
			}
		}
		return false;
	};},
	get ibind () {return function (el, event_name, namespace, callback) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'el': var el = __allkwargs0__ [__attrib0__]; break;
						case 'event_name': var event_name = __allkwargs0__ [__attrib0__]; break;
						case 'namespace': var namespace = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (!(window.PhanterPWA.check_event_namespace (el, event_name, namespace)) && callable (callback)) {
			var ns = '{0}.{1}'.format (event_name, namespace);
			$ (el).off (ns).on (ns, (function __lambda__ (event) {
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
				return callback (this, event);
			}));
		}
	};},
	get get_inicial_config_uri () {return __get__ (this, function (self) {
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
		var initial_config = new URL (window.location.href);
		var params = initial_config.searchParams;
		var authorization = params.get ('authorization');
		var client_token = params.get ('client_token');
		var url_token = params.get ('url_token');
		var auth_user = params.get ('auth_user');
		var redirect = params.get ('redirect');
		var way = params.get ('way');
		if (auth_user !== null && auth_user !== undefined) {
			var auth_user = JSON.parse (auth_user);
		}
		if (authorization !== null && url_token !== null && auth_user !== null && client_token !== null) {
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
		if (redirect !== null && redirect !== undefined) {
			window.location = redirect;
		}
		if (way !== null && way !== undefined) {
			self.open_way (way);
		}
	});},
	get _after_ajax_complete () {return __get__ (this, function (self, event, xhr, option) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						case 'xhr': var xhr = __allkwargs0__ [__attrib0__]; break;
						case 'option': var option = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (option !== undefined) {
			var p_url = self.parse_url (option.url);
			self.reload_components (__kwargtrans__ ({ajax: p_url}));
			self.reload_events (__kwargtrans__ ({ajax: p_url}));
		}
	});},
	get get_id () {return __get__ (this, function (self, salt) {
		if (typeof salt == 'undefined' || (salt != null && salt.hasOwnProperty ("__kwargtrans__"))) {;
			var salt = 'phanterpwa';
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'salt': var salt = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.counter++;
		var timestamp = new Date ().getTime ();
		if (salt === null || salt === undefined) {
			console.error ('The salt of method get_id is invalid! given:', salt);
			var salt = 'phanterpwa';
		}
		return '{0}-{1}-{2}'.format (salt, self.counter, timestamp);
	});},
	get social_login_list () {return __get__ (this, function (self) {
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
		var social_logins = window.PhanterPWA ['CONFIG'] ['SOCIAL_LOGINS'];
		if (social_logins !== null && social_logins !== undefined) {
			var list_login = social_logins.py_keys ();
			var l = [];
			for (var x of list_login) {
				if (__in__ (x, self._social_login_icons)) {
					l.append ([x, self._social_login_icons [x]]);
				}
				else {
					l.append ([x, I (__kwargtrans__ ({_class: 'fas fa-at'}))]);
				}
			}
			return l;
		}
	});},
	get get_app_name () {return function (self) {
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
		return window.PhanterPWA.CONFIG ['APP'] ['name'];
	};},
	get get_api_address () {return function (self) {
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
		return window.PhanterPWA.CONFIG ['APP'] ['http_address'];
	};},
	get flash () {return function (msg) {
		if (typeof msg == 'undefined' || (msg != null && msg.hasOwnProperty ("__kwargtrans__"))) {;
			var msg = null;
		};
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'msg': var msg = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		var timeout = parameters.py_get ('timeout', 3000);
		var timestamp = new Date ().getTime ();
		var msg_id = 'phanterpwa-flash-wrapper-{0}'.format (timestamp);
		var target = $ ('#phanterpwa-flash-container');
		if (target.length == 0) {
			$ ('body').prepend (DIV (__kwargtrans__ ({_id: 'phanterpwa-flash-container'})).jquery ());
		}
		var remove_msg = function () {
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
			$ ('#{0}'.format (msg_id)).removeClass ('enabled').slideUp (500);
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
				return $ ('#{0}'.format (msg_id)).remove ();
			}), 2000);
		};
		if (__in__ ('html', parameters)) {
			var msg = parameters.py_get ('html', null);
			if (msg !== null) {
				var html = DIV (XML (msg), __kwargtrans__ ({_id: msg_id, _class: 'phanterpwa-flash-wrapper enabled', _style: 'opacity: 0; margin-top:-20px'}));
				html.append_to ('#phanterpwa-flash-container');
				$ ('#{0}'.format (msg_id)).addClass ('enabled').animate (dict ({'opacity': 1, 'margin-top': '0px'}));
				setTimeout (remove_msg, timeout);
			}
		}
		else if (msg !== null && msg !== undefined) {
			var html = DIV (msg, __kwargtrans__ ({_id: msg_id, _class: 'phanterpwa-flash-wrapper', _style: 'opacity: 0; margin-top:-20px'}));
			html.append_to ('#phanterpwa-flash-container').find ('#{0}'.format (msg_id)).addClass ('enabled').animate (dict ({'opacity': 1, 'margin-top': '0px'}));
			setTimeout (remove_msg, timeout);
		}
	};},
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
		self.reload_components (__kwargtrans__ (context));
		self.reload_events (__kwargtrans__ (context));
	});},
	get reload_components () {return __get__ (this, function (self) {
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
		for (var c of self.Components.py_keys ()) {
			if (callable (self.Components [c].reload)) {
				if (self.Components [c].actived === false) {
					if (self.DEBUG) {
						console.info ('Reload Components {0}'.format (c));
					}
					self.Components [c].actived = true;
					self.Components [c].reload (__kwargtrans__ (context));
				}
			}
		}
	});},
	get reload_component () {return __get__ (this, function (self, component) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'component': var component = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var comp = self.Components [component];
		if (comp !== undefined) {
			if (self.DEBUG) {
				console.info ('Reload Component: {0}'.format (component));
			}
			comp.reload ();
		}
	});},
	get reload_events () {return __get__ (this, function (self) {
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
		for (var c of self.Events.py_keys ()) {
			if (callable (self.Events [c].reload)) {
				self.Events [c].reload (__kwargtrans__ (context));
			}
		}
		var target = context.py_get ('selector', null);
		var ajax = context.py_get ('ajax', null);
		if (target !== null) {
			self.I18N.DOMTranslate (target);
		}
		else if (ajax !== null && len (ajax [1]) > 0 && ajax [1] [0] == 'signcaptchaforms') {
			self.I18N.DOMTranslate ('.phanterpwa-widget-captcha-container');
		}
	});},
	get async_function () {return __get__ (this, function (self, callback, delay) {
		if (typeof delay == 'undefined' || (delay != null && delay.hasOwnProperty ("__kwargtrans__"))) {;
			var delay = 0;
		};
		var context = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
						case 'delay': var delay = __allkwargs0__ [__attrib0__]; break;
						default: context [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete context.__kwargtrans__;
			}
		}
		else {
		}
		var f = function () {
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
			if (self.DEBUG) {
				console.info ('Async Callback', callback);
			}
			callback ();
			self.reload_components (__kwargtrans__ (context));
			self.reload_events (__kwargtrans__ (context));
		};
		if (callable (callback)) {
			setTimeout (f, delay);
		}
	});},
	get save_state () {return __get__ (this, function (self, key_state) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'key_state': var key_state = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var body_html = $ ('body').html ();
		self.states [key_state] = body_html;
	});},
	get load_state () {return __get__ (this, function (self, key_state, callback) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'key_state': var key_state = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var page = self.states.py_get (key_state, null);
		var body = null;
		if (page !== null) {
			var body = $ ('body').html (page);
			self.reload_components ();
		}
		else {
			console.error ('The key_state do not exist');
		}
		if (callable (callback)) {
			callback (body);
		}
	});},
	get add_component () {return __get__ (this, function (self, component) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'component': var component = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (isinstance (component, Component)) {
			self.Components [component.identifier] = component;
			component.start ();
		}
		else if (isinstance (component, list)) {
			for (var x of component) {
				self.add_component (x);
			}
		}
		else {
			console.error ('The component must be Component instance');
		}
	});},
	get add_event () {return __get__ (this, function (self, event) {
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
		if (isinstance (event, events.Event)) {
			self.Events [event.identifier] = event;
			event.start ();
		}
		else if (isinstance (event, list)) {
			for (var x of event) {
				self.add_event (x);
			}
		}
		else {
			console.error ('The event must be Event instance');
		}
	});},
	get remove_last_auth_user () {return __get__ (this, function (self) {
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
		localStorage.removeItem ('last_auth_user');
	});},
	get _after_submit_login () {return __get__ (this, function (self, data, ajax_status, callback) {
		if (typeof callback == 'undefined' || (callback != null && callback.hasOwnProperty ("__kwargtrans__"))) {;
			var callback = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var json = data.responseJSON;
		if (ajax_status == 'success') {
			if (data.status == 200) {
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
					self.WS.send ('command_online');
					localStorage.setItem ('last_auth_user', JSON.stringify (auth_user));
				}
				window.PhanterPWA.open_current_way ();
			}
			else if (data.status == 206) {
				var client_token = json.client_token;
				if (client_token !== undefined) {
					localStorage.setItem ('phanterpwa-client-token', client_token);
					sessionStorage.removeItem ('phanterpwa-authorization');
					sessionStorage.removeItem ('auth_user');
					localStorage.removeItem ('phanterpwa-authorization');
					localStorage.removeItem ('auth_user');
				}
			}
		}
		if (self.DEBUG) {
			console.info (data.status, json.i18n.message);
		}
		if (callable (callback)) {
			callback (data, ajax_status);
		}
	});},
	get login () {return __get__ (this, function (self, csrf_token, username, password, remember_me) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'csrf_token': var csrf_token = __allkwargs0__ [__attrib0__]; break;
						case 'username': var username = __allkwargs0__ [__attrib0__]; break;
						case 'password': var password = __allkwargs0__ [__attrib0__]; break;
						case 'remember_me': var remember_me = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		if (remember_me === null || remember_me === undefined) {
			var remember_me = false;
		}
		var callback = parameters.py_get ('callback', null);
		var formdata = new FormData ();
		formdata.append ('csrf_token', csrf_token);
		var login_password = '{0}:{1}'.format (window.btoa (username), window.btoa (password));
		formdata.append ('edata', login_password);
		formdata.append ('remember_me', remember_me);
		window.PhanterPWA.ApiServer.POST (__kwargtrans__ (dict ({'url_args': ['api', 'auth'], 'form_data': formdata, 'onComplete': (function __lambda__ (data, ajax_status) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'data': var data = __allkwargs0__ [__attrib0__]; break;
							case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._after_submit_login (data, ajax_status, callback);
		})})));
	});},
	get _after_submit_two_factor () {return __get__ (this, function (self, data, ajax_status, callback) {
		if (typeof callback == 'undefined' || (callback != null && callback.hasOwnProperty ("__kwargtrans__"))) {;
			var callback = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var json = data.responseJSON;
		if (ajax_status == 'success') {
			if (data.status == 200) {
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
					self.WS.send ('command_online');
					localStorage.setItem ('last_auth_user', JSON.stringify (auth_user));
				}
				window.PhanterPWA.open_current_way ();
			}
		}
		if (self.DEBUG) {
			console.info (data.status, json.i18n.message);
		}
		if (callable (callback)) {
			callback (data, ajax_status);
		}
	});},
	get two_factor () {return __get__ (this, function (self, url_authorization, code) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'url_authorization': var url_authorization = __allkwargs0__ [__attrib0__]; break;
						case 'code': var code = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		var callback = parameters.py_get ('callback', null);
		var formdata = new FormData ();
		formdata.append ('code', code);
		window.PhanterPWA.ApiServer.PUT (__kwargtrans__ (dict ({'url_args': ['api', 'auth', 'two-factor', url_authorization], 'form_data': formdata, 'onComplete': (function __lambda__ (data, ajax_status) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'data': var data = __allkwargs0__ [__attrib0__]; break;
							case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._after_submit_two_factor (data, ajax_status, callback);
		})})));
	});},
	get social_login () {return __get__ (this, function (self, social_name, callback) {
		if (typeof callback == 'undefined' || (callback != null && callback.hasOwnProperty ("__kwargtrans__"))) {;
			var callback = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'social_name': var social_name = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		window.PhanterPWA.ApiServer.GET (__kwargtrans__ (dict ({'url_args': ['api', 'oauth', 'prompt', social_name], 'onComplete': (function __lambda__ (data, ajax_status) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'data': var data = __allkwargs0__ [__attrib0__]; break;
							case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._after_get_social_login (data, ajax_status, callback);
		})})));
	});},
	get _after_get_social_login () {return __get__ (this, function (self, data, ajax_status, callback) {
		if (typeof callback == 'undefined' || (callback != null && callback.hasOwnProperty ("__kwargtrans__"))) {;
			var callback = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var json = data.responseJSON;
		if (ajax_status == 'success') {
			window.location = json.redirect;
		}
		if (callable (callback)) {
			callback (data, ajax_status);
		}
	});},
	get _after_submit_register () {return __get__ (this, function (self, data, ajax_status, callback) {
		if (typeof callback == 'undefined' || (callback != null && callback.hasOwnProperty ("__kwargtrans__"))) {;
			var callback = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var json = data.responseJSON;
		if (ajax_status == 'success') {
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
				self.WS.send ('command_online');
				localStorage.setItem ('last_auth_user', JSON.stringify (auth_user));
			}
		}
		else {
			console.info (data.status);
		}
		if (self.DEBUG) {
			console.info (json.i18n.message);
		}
		if (callback !== null) {
			callback (data, ajax_status);
		}
	});},
	get register () {return __get__ (this, function (self, csrf_token, first_name, last_name, email, password, password_repeat) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'csrf_token': var csrf_token = __allkwargs0__ [__attrib0__]; break;
						case 'first_name': var first_name = __allkwargs0__ [__attrib0__]; break;
						case 'last_name': var last_name = __allkwargs0__ [__attrib0__]; break;
						case 'email': var email = __allkwargs0__ [__attrib0__]; break;
						case 'password': var password = __allkwargs0__ [__attrib0__]; break;
						case 'password_repeat': var password_repeat = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		var callback = null;
		if (__in__ ('callback', parameters)) {
			var callback = parameters ['callback'];
		}
		var formdata = new FormData ();
		formdata.append ('csrf_token', csrf_token);
		formdata.append ('first_name', first_name);
		formdata.append ('last_name', last_name);
		formdata.append ('email', email);
		var passwords = '{0}:{1}'.format (window.btoa (password), window.btoa (password_repeat));
		formdata.append ('edata', passwords);
		window.PhanterPWA.ApiServer.POST (__kwargtrans__ (dict ({'url_args': ['api', 'auth', 'create'], 'form_data': formdata, 'onComplete': (function __lambda__ (data, ajax_status) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'data': var data = __allkwargs0__ [__attrib0__]; break;
							case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._after_submit_register (data, ajax_status, callback);
		})})));
	});},
	get _after_submit_request_password () {return __get__ (this, function (self, data, ajax_status, callback) {
		if (typeof callback == 'undefined' || (callback != null && callback.hasOwnProperty ("__kwargtrans__"))) {;
			var callback = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var json = data.responseJSON;
		if (self.DEBUG) {
			console.info (data.status, json.i18n.message);
		}
		if (callback !== null) {
			callback (data, ajax_status);
		}
	});},
	get request_password () {return __get__ (this, function (self, csrf_token, email) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'csrf_token': var csrf_token = __allkwargs0__ [__attrib0__]; break;
						case 'email': var email = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		var last_auth_user = self.get_last_auth_user ();
		if (last_auth_user !== null) {
			if (email != last_auth_user.email) {
				self.remove_last_auth_user ();
			}
		}
		var callback = null;
		if (__in__ ('callback', parameters)) {
			var callback = parameters ['callback'];
		}
		var formdata = new FormData ();
		formdata.append ('csrf_token', csrf_token);
		formdata.append ('email', email);
		window.PhanterPWA.ApiServer.POST (__kwargtrans__ (dict ({'url_args': ['api', 'auth', 'request-password'], 'form_data': formdata, 'onComplete': (function __lambda__ (data, ajax_status) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'data': var data = __allkwargs0__ [__attrib0__]; break;
							case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._after_submit_request_password (data, ajax_status, callback);
		})})));
	});},
	get _after_submit_activation_account () {return __get__ (this, function (self, data, ajax_status, callback) {
		if (typeof callback == 'undefined' || (callback != null && callback.hasOwnProperty ("__kwargtrans__"))) {;
			var callback = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var json = data.responseJSON;
		if (ajax_status == 'success') {
			var auth_user = json.auth_user;
			sessionStorage.setItem ('auth_user', JSON.stringify (auth_user));
			localStorage.setItem ('last_auth_user', JSON.stringify (auth_user));
			self.update_current_way ();
		}
		if (self.DEBUG) {
			console.info (data.status, json.i18n.message);
		}
		if (callback !== null) {
			callback (data, ajax_status);
		}
	});},
	get activation_account () {return __get__ (this, function (self, csrf_token, activation_code) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'csrf_token': var csrf_token = __allkwargs0__ [__attrib0__]; break;
						case 'activation_code': var activation_code = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		var callback = null;
		if (__in__ ('callback', parameters)) {
			var callback = parameters ['callback'];
		}
		var formdata = new FormData ();
		formdata.append ('csrf_token', csrf_token);
		formdata.append ('activation_code', activation_code);
		window.PhanterPWA.ApiServer.POST (__kwargtrans__ (dict ({'url_args': ['api', 'auth', 'active-account'], 'form_data': formdata, 'onComplete': (function __lambda__ (data, ajax_status) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'data': var data = __allkwargs0__ [__attrib0__]; break;
							case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._after_submit_activation_account (data, ajax_status, callback);
		})})));
	});},
	get _after_submit_change_password () {return __get__ (this, function (self, data, ajax_status, callback) {
		if (typeof callback == 'undefined' || (callback != null && callback.hasOwnProperty ("__kwargtrans__"))) {;
			var callback = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var json = data.responseJSON;
		if (self.DEBUG) {
			console.info (data.status, json.i18n.message);
		}
		if (callback !== null) {
			callback (data, ajax_status);
		}
	});},
	get change_password () {return __get__ (this, function (self, csrf_token, password, new_password, new_password_repeat) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'csrf_token': var csrf_token = __allkwargs0__ [__attrib0__]; break;
						case 'password': var password = __allkwargs0__ [__attrib0__]; break;
						case 'new_password': var new_password = __allkwargs0__ [__attrib0__]; break;
						case 'new_password_repeat': var new_password_repeat = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		var callback = null;
		if (__in__ ('callback', parameters)) {
			var callback = parameters ['callback'];
		}
		var formdata = new FormData ();
		formdata.append ('csrf_token', csrf_token);
		formdata.append ('edata', '{0}:{1}:{2}'.format (window.btoa (password), window.btoa (new_password), window.btoa (new_password_repeat)));
		window.PhanterPWA.ApiServer.POST (__kwargtrans__ (dict ({'url_args': ['api', 'auth', 'change-password'], 'form_data': formdata, 'onComplete': (function __lambda__ (data, ajax_status) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'data': var data = __allkwargs0__ [__attrib0__]; break;
							case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._after_submit_change_password (data, ajax_status, callback);
		})})));
	});},
	get logout () {return __get__ (this, function (self) {
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
		}
		else {
		}
		var callback = null;
		if (__in__ ('callback', parameters)) {
			var callback = parameters ['callback'];
		}
		self.WS.send ('command_offline');
		sessionStorage.removeItem ('phanterpwa-authorization');
		sessionStorage.removeItem ('auth_user');
		localStorage.removeItem ('phanterpwa-authorization');
		localStorage.removeItem ('auth_user');
		self.open_default_way ();
		if (callback !== null) {
			callback ();
		}
	});},
	get _after_get_csrf_token () {return __get__ (this, function (self, data, ajax_status, callback) {
		if (typeof callback == 'undefined' || (callback != null && callback.hasOwnProperty ("__kwargtrans__"))) {;
			var callback = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
						case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var json = data.responseJSON;
		if (self.DEBUG) {
			console.info (data.status, json.i18n.message);
		}
		if (callback !== null) {
			callback (data, ajax_status);
		}
	});},
	get get_csrf_token () {return __get__ (this, function (self, table_name) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'table_name': var table_name = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		var callback = null;
		var headers = null;
		if (__in__ ('callback', parameters)) {
			var callback = parameters ['callback'];
		}
		if (__in__ ('headers', parameters)) {
			var headers = parameters ['headers'];
		}
		window.PhanterPWA.ApiServer.GET (__kwargtrans__ (dict ({'url_args': ['api', 'signforms', table_name], 'onComplete': (function __lambda__ (data, ajax_status) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'data': var data = __allkwargs0__ [__attrib0__]; break;
							case 'ajax_status': var ajax_status = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._after_get_csrf_token (data, ajax_status, callback);
		}), 'headers': headers})));
	});},
	get xml_to_dom_element () {return function (xml, target, callback) {
		if (typeof callback == 'undefined' || (callback != null && callback.hasOwnProperty ("__kwargtrans__"))) {;
			var callback = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'xml': var xml = __allkwargs0__ [__attrib0__]; break;
						case 'target': var target = __allkwargs0__ [__attrib0__]; break;
						case 'callback': var callback = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var target = $ (target);
		if (target.length == 0) {
			console.error ("The target element don't exists!");
		}
		if (isinstance (xml, helpers.XmlConstructor)) {
			target.html (xml.jquery ());
		}
		else {
			target.html (xml);
		}
		if (callable (callback)) {
			callback (target);
		}
		window.PhanterPWA.I18N.DOMTranslate (target);
	};},
	get get_current_way () {return function () {
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
		var current_way = sessionStorage.getItem ('current_way');
		if (current_way === null || current_way === undefined || current_way === 'lock') {
			var current_way = 'home';
		}
		return current_way;
	};},
	get open_code_way () {return function (code, request, response) {
		if (typeof code == 'undefined' || (code != null && code.hasOwnProperty ("__kwargtrans__"))) {;
			var code = 500;
		};
		if (typeof request == 'undefined' || (request != null && request.hasOwnProperty ("__kwargtrans__"))) {;
			var request = null;
		};
		if (typeof response == 'undefined' || (response != null && response.hasOwnProperty ("__kwargtrans__"))) {;
			var response = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'code': var code = __allkwargs0__ [__attrib0__]; break;
						case 'request': var request = __allkwargs0__ [__attrib0__]; break;
						case 'response': var response = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (str (code).isdigit ()) {
			var code = int (code);
		}
		if (!__in__ (code, window.PhanterPWA.Gates)) {
			var auth_user = window.PhanterPWA.Components.auth_user;
			if (window.PhanterPWA.DEBUG) {
				console.info (code, request, response);
			}
			if (code == 401) {
				if (auth_user !== null && auth_user !== undefined) {
					auth_user.start ();
				}
				gatehandler.Error_401 (request, response);
			}
			else if (code == 403) {
				if (auth_user !== null && auth_user !== undefined) {
					auth_user.start ();
				}
				gatehandler.Error_403 (request, response);
			}
			else if (code == 404) {
				gatehandler.Error_404 (request, response);
			}
			else {
				gatehandler.Error_502 (request, response);
			}
		}
		else if (isinstance (request, WayRequest)) {
			if (window.PhanterPWA.DEBUG) {
				console.info (code, request, response);
			}
			window.PhanterPWA.Gates [code] (request, response);
		}
		else {
			if (window.PhanterPWA.DEBUG) {
				console.error ('The request must be WayRequest instance.');
			}
			gatehandler.Error_500 (request, response);
		}
	};},
	get get_client_token () {return function () {
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
		var client_token = localStorage.getItem ('phanterpwa-client-token');
		if (client_token !== null && client_token !== undefined) {
			return client_token;
		}
		else {
			return null;
		}
	};},
	get get_url_token () {return function () {
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
		var url_token = localStorage.getItem ('phanterpwa-url-token');
		if (url_token !== null && url_token !== undefined) {
			return url_token;
		}
		else {
			return null;
		}
	};},
	get get_authorization () {return function () {
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
		var authorization = sessionStorage.getItem ('phanterpwa-authorization');
		if (authorization === null || authorization === undefined) {
			var authorization = localStorage.getItem ('phanterpwa-authorization');
		}
		else {
			localStorage.removeItem ('phanterpwa-authorization');
		}
		if (authorization !== null && authorization !== undefined) {
			return authorization;
		}
		else {
			localStorage.removeItem ('auth_user');
			sessionStorage.removeItem ('auth_user');
			return null;
		}
	};},
	get get_auth_user () {return function () {
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
		var auth_user = sessionStorage.getItem ('auth_user');
		if (auth_user === null || auth_user === undefined) {
			var auth_user = localStorage.getItem ('auth_user');
		}
		else {
			localStorage.removeItem ('auth_user');
		}
		if (auth_user !== null && auth_user !== undefined) {
			return JSON.parse (auth_user);
		}
		else {
			window.PhanterPWA.WS.send ('command_offline');
			localStorage.removeItem ('phanterpwa-authorization');
			sessionStorage.removeItem ('phanterpwa-authorization');
			return null;
		}
	};},
	get logged () {return function () {
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
		if (window.PhanterPWA.get_auth_user () === null) {
			return false;
		}
		else {
			return true;
		}
	};},
	get auth_user_has_id () {return function (ids) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'ids': var ids = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (window.PhanterPWA.logged ()) {
			var auth_user = window.PhanterPWA.get_auth_user ();
			if (isinstance (ids, int)) {
				if (int (auth_user.id) == ids) {
					return true;
				}
			}
			else if (isinstance (ids, str) && ids.isdigit () && str (auth_user.id) == ids) {
				return true;
			}
			else if (isinstance (ids, list)) {
				for (var x of ids) {
					if (window.PhanterPWA.auth_user_has_id (x)) {
						return true;
					}
				}
			}
		}
		return false;
	};},
	get auth_user_has_role () {return function (roles) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'roles': var roles = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (window.PhanterPWA.logged ()) {
			var auth_user = window.PhanterPWA.get_auth_user ();
			if (isinstance (roles, str) && __in__ (roles, auth_user.roles)) {
				return true;
			}
			else if (isinstance (roles, list) && len (set (auth_user.roles).intersection (set (roles))) > 0) {
				return true;
			}
		}
		return false;
	};},
	get update_auth_user () {return function (auth_user) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'auth_user': var auth_user = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (auth_user !== null && auth_user !== undefined) {
			if (auth_user ['remember_me'] === true) {
				localStorage.setItem ('auth_user', JSON.stringify (auth_user));
				sessionStorage.removeItem ('auth_user');
			}
			else {
				sessionStorage.setItem ('auth_user', JSON.stringify (auth_user));
				localStorage.removeItem ('auth_user');
			}
			localStorage.setItem ('last_auth_user', JSON.stringify (auth_user));
		}
	};},
	get get_auth_user_image () {return function () {
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
		var image_user = '/static/{0}/images/user.png'.format (window.PhanterPWA.CONFIG.PROJECT.version);
		var auth_user = window.PhanterPWA.get_auth_user ();
		if (auth_user !== null && auth_user ['image'] !== null) {
			var url_token = localStorage.getItem ('phanterpwa-url-token');
			var server = window.PhanterPWA.CONFIG ['APP'] ['http_address'];
			var image_user = '{0}/api/auth/image/{1}?sign={2}'.format (server, auth_user ['image'], url_token);
		}
		return image_user;
	};},
	get get_last_auth_user_image () {return function () {
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
		var image_user = '/static/{0}/images/user.png'.format (window.PhanterPWA.CONFIG.PROJECT.version);
		var auth_user = window.PhanterPWA.get_last_auth_user ();
		if (auth_user !== null && auth_user ['image'] !== null) {
			var url_token = localStorage.getItem ('phanterpwa-url-token');
			var server = window.PhanterPWA.CONFIG ['APP'] ['http_address'];
			var image_user = '{0}/api/auth/image/{1}?sign={2}'.format (server, auth_user ['image'], url_token);
		}
		return image_user;
	};},
	get get_last_auth_user () {return function () {
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
		var last_auth_user = localStorage.getItem ('last_auth_user');
		if (last_auth_user !== null && last_auth_user !== undefined) {
			return JSON.parse (last_auth_user);
		}
		else {
			return null;
		}
	};},
	get open_way () {return __get__ (this, function (self, way) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'way': var way = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (way == self.get_current_way ()) {
			self.open_current_way ();
		}
		else {
			window.location = '#_phanterpwa:/{0}'.format (way);
		}
	});},
	get _onPopState () {return __get__ (this, function (self) {
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
		var way = self._get_way_from_url_hash ();
		self.Request = WayRequest ();
		self.Request.open_way (way);
		if (self._after_open_way !== null && self._after_open_way !== undefined) {
			self._after_open_way (self.Request);
		}
	});},
	get open_current_way () {return __get__ (this, function (self) {
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
		var way = self._get_way_from_url_hash ();
		self.Request = WayRequest ();
		self.Request.open_way (way);
	});},
	get update_current_way () {return __get__ (this, function (self) {
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
		window.location.reload ();
	});},
	get open_default_way () {return __get__ (this, function (self) {
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
		self.open_way (self.default_way);
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
		if (self.DEBUG) {
			console.info ('initializing...');
		}
	});},
	get parse_url () {return __get__ (this, function (self, url) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'url': var url = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var l = new URL (url);
		var t_args = l.pathname.py_split ('/').__getslice__ (1, null, 1);
		var gate = t_args [0];
		var c_args = t_args.__getslice__ (1, null, 1);
		var n_args = list ();
		for (var c of c_args) {
			if (c !== '') {
				n_args.append (c);
			}
		}
		var params = dict ();
		if (l.search !== '') {
			var add_in_p = function (k, v) {
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
				params [k] = v;
			};
			var t_params = l.searchParams;
			t_params.forEach ((function __lambda__ (v, k) {
				if (arguments.length) {
					var __ilastarg0__ = arguments.length - 1;
					if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
						var __allkwargs0__ = arguments [__ilastarg0__--];
						for (var __attrib0__ in __allkwargs0__) {
							switch (__attrib0__) {
								case 'v': var v = __allkwargs0__ [__attrib0__]; break;
								case 'k': var k = __allkwargs0__ [__attrib0__]; break;
							}
						}
					}
				}
				else {
				}
				return add_in_p (k, v);
			}));
		}
		return [gate, n_args, params, url];
	});},
	get parse_way () {return __get__ (this, function (self, way) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'way': var way = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var gate = way;
		var origin = window.location.origin;
		var url = '{0}/{1}'.format (origin, way);
		var tway = self.parse_url (url);
		tway [3] = '{0}/#_phanterpwa:/{1}'.format (origin, way);
		return tway;
	});},
	get _get_way_from_url_hash () {return __get__ (this, function (self) {
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
		var url_hash = window.location.hash;
		var way = self.default_way;
		if (url_hash !== undefined && url_hash !== null && url_hash != '') {
			if (url_hash.startswith ('#_phanterpwa:/')) {
				var way = url_hash.__getslice__ (14, null, 1);
			}
		}
		return way;
	});},
	get _set_way_to_url_hash () {return __get__ (this, function (self, way) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'way': var way = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var current = self._get_way_from_url_hash ();
		if (way != current) {
			window.history.pushState ('', self.TITLE, '#_phanterpwa:/{0}'.format (way));
		}
	});},
	get onPopState () {return __get__ (this, function (self) {
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
		self.open_way (self._get_way_from_url_hash ());
	});},
	get GET () {return __get__ (this, function (self) {
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
		}
		else {
		}
		self.ApiServer.GET (__kwargtrans__ (parameters));
	});},
	get DELETE () {return __get__ (this, function (self) {
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
		}
		else {
		}
		self.ApiServer.DEL (__kwargtrans__ (parameters));
	});},
	get POST () {return __get__ (this, function (self) {
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
		}
		else {
		}
		self.ApiServer.POST (__kwargtrans__ (parameters));
	});},
	get PUT () {return __get__ (this, function (self) {
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
		}
		else {
		}
		self.ApiServer.PUT (__kwargtrans__ (parameters));
	});},
	get LOAD () {return __get__ (this, function (self) {
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
		}
		else {
		}
		Loads (__kwargtrans__ (parameters));
	});}
});
export var Loads =  __class__ ('Loads', [object], {
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
		}
		else {
		}
		self.url_args = parameters.py_get ('args', null);
		self.url_vars = parameters.py_get ('vars', dict ({}));
		self.onComplete = parameters.py_get ('onComplete', null);
		var pro_args = self._process_args ();
		var location = new URL (window.location);
		var origin = location.origin;
		var url = '{0}/{1}'.format (origin, pro_args);
		$.get (url, self._after_load);
	});},
	get _after_load () {return __get__ (this, function (self, data, ajax_status) {
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
		var context = self._process_vars ();
		for (var x of context.py_keys ()) {
			var k = ''.join (['{{', x, '}}']);
			var ls = data.py_split (k);
			var ns = str (context [x]).join (ls);
			var data = ns;
		}
		if (callable (self.onComplete)) {
			self.onComplete (data);
			window.PhanterPWA.reload ();
		}
	});},
	get _process_args () {return __get__ (this, function (self) {
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
		var s_args = '';
		if (isinstance (self.url_args, list)) {
			var s_args = '/'.join (self.url_args);
		}
		else {
			console.error ('LOAD url_args must be list(array).');
		}
		if (s_args != '') {
			var s_args = '{0}'.format (s_args);
		}
		return s_args;
	});},
	get _process_vars () {return __get__ (this, function (self) {
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
		try {
			var _vars = dict (self.url_vars);
		}
		catch (__except0__) {
			if (isinstance (__except0__, Exception)) {
				var e = __except0__;
				console.error ('LOAD url_vars must be dict object');
			}
			else {
				throw __except0__;
			}
		}
		if (isinstance (_vars, dict)) {
			return _vars;
		}
		else {
			return dict ({});
		}
	});}
});
export var Component =  __class__ ('Component', [helpers.XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, identifier) {
		var attributes = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'identifier': var identifier = __allkwargs0__ [__attrib0__]; break;
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
		self.actived = false;
		self.identifier = identifier;
		self._identifier = window.PhanterPWA.get_id (identifier);
		attributes ['_phanterpwa-component'] = self._identifier;
		attributes ['_id'] = identifier;
		if (len (content) == 0) {
			var content = [DIV ('xml content component', __kwargtrans__ ({_style: 'color: red;'}))];
		}
		helpers.XmlConstructor.__init__ (self, 'phanterpwa-component', false, ...content, __kwargtrans__ (attributes));
		window.PhanterPWA.add_component (self);
	});},
	get _onload () {return __get__ (this, function (self) {
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
		if (window.PhanterPWA.DEBUG) {
			console.info ('The Component {0} reload with context {1}'.format (self.identifier, context));
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
export var Developer_Toolbar =  __class__ ('Developer_Toolbar', [Component], {
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
		Component.__init__ (self, 'developer_toolbar');
	});},
	get _switch_panel_objects () {return __get__ (this, function (self) {
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
		var t = $ ('#p-developer_toolbar');
		if (t.hasClass ('enabled')) {
			t.removeClass ('enabled');
		}
		else {
			t.addClass ('enabled');
		}
	});},
	get _get_beautify () {return __get__ (this, function (self) {
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
				if (test) {
					return ;
				}
				seen.append (v);
			}
			return v;
		};
		var response = JSON.stringify (window.PhanterPWA.Response, (function __lambda__ (k, v) {
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
		var n = JSON.parse (response);
		if (n !== null && n !== undefined) {
			var request = JSON.stringify (n._request, null, 4);
			delete n._request;
			var response = JSON.stringify (n, null, 4);
		}
		else {
			var response = null;
			var request = null;
		}
		return [response, request];
	});},
	get _open_modal () {return __get__ (this, function (self) {
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
		var rr = self._get_beautify ();
		var request = TEXTAREA (rr [1]);
		var response = TEXTAREA (rr [0]);
		var content_ = DIV (DIV (H2 ('Request'), request, __kwargtrans__ ({_class: 'phanterpwa-developer_toolbar phanterpwa-developer_toolbar-request'})), DIV (H2 ('Response'), response, __kwargtrans__ ({_class: 'phanterpwa-developer_toolbar phanterpwa-developer_toolbar-response'})), __kwargtrans__ ({_class: 'phanterpwa-developer_toolbar-objects'}));
		self.m_modal = modal.Modal ('#p-developer_toolbar', __kwargtrans__ (dict ({'title': 'Developer Toolbar', 'content': content_})));
		self.m_modal.open ();
	});},
	get check_duplicates_ids () {return __get__ (this, function (self) {
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
		var check = function (el) {
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
			var ids = $ ("[id='{0}']".format (el.id));
			if (ids.length > 1 && ids [0] == el) {
				console.warn ('Developer_Toolbar: Multiple IDs #{0}'.format (el.id));
			}
		};
		$ ('[id]').each ((function __lambda__ () {
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
			return check (this);
		}));
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
		var t = $ ('#p-developer_toolbar');
		t.find ('.button_developer').off ('click.developer_toolbar_button').on ('click.developer_toolbar_button', self._open_modal);
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
			return self._window_size ();
		}));
		self.check_duplicates_ids ();
		self._window_size ();
	});},
	get _window_size () {return __get__ (this, function (self) {
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
		var w = $ (window).width ();
		var h = $ (window).height ();
		$ ('#p-developer_toolbar').find ('.current-size').html ('{0}x{1} - '.format (w, h));
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
		if ($ ('#p-developer_toolbar').length == 0) {
			var xml = DIV (__kwargtrans__ ({_id: 'p-developer_toolbar'}));
			xml.append_to ('body');
		}
		self._binds ();
	});}
});
export var WayRequest =  __class__ ('WayRequest', [object], {
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
		self.timestamp = new Date ().getTime ();
		self.application_info = null;
		self.auth_user = null;
		self.gate = 'home';
		self.way = 'home';
		self.params = null;
		self.args = null;
		self.last_way = 'home';
		self._element = null;
		self.widgets = dict ({});
		self.error = null;
	});},
	get _body_flag () {return function () {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
				}
			}
			var new_flag = tuple ([].slice.apply (arguments).slice (0, __ilastarg0__ + 1));
		}
		else {
			var new_flag = tuple ();
		}
		var body = $ ('body');
		var lclass = body.attr ('class');
		var r = new RegExp ('/\\s+/');
		if (lclass !== undefined) {
			var lclass = lclass.py_split (r);
			for (var x of lclass) {
				if (x.startswith ('phanterpwa-flag-')) {
					body.removeClass (x);
				}
			}
		}
		for (var f of new_flag) {
			if (f.startswith ('phanterpwa-flag-')) {
				var f = f.py_replace ('/', '_');
				body.addClass (f);
			}
			else {
				var f = f.py_replace ('/', '_');
				body.addClass ('phanterpwa-flag-{0}'.format (f));
			}
		}
	};},
	get add_widget () {return __get__ (this, function (self, widget) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'widget': var widget = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (isinstance (widget, widgets.Widget)) {
			self.widgets [widget.identifier] = widget;
			if (callable (widget.initialize)) {
				widget.initialize ();
			}
		}
	});},
	get _process_way () {return __get__ (this, function (self, way) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'way': var way = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.application_info = '{0} (version: {1}, compilation: {2})'.format (window.PhanterPWA.CONFIG.PROJECT.title, window.PhanterPWA.CONFIG.PROJECT.version, window.PhanterPWA.CONFIG.PROJECT.compilation);
		self.auth_user = window.PhanterPWA.get_auth_user ();
		self.gate = way;
		self.way = way;
		if (__in__ ('?', self.way) || __in__ ('/', self.way)) {
			var l = '{0}/{1}'.format (window.PhanterPWA.CONFIG.APP.http_address, self.way);
			var l = new URL (l);
			var t_args = l.pathname.py_split ('/').__getslice__ (1, null, 1);
			self.gate = t_args [0];
			var c_args = t_args.__getslice__ (1, null, 1);
			var n_args = list ();
			for (var c of c_args) {
				if (c !== '') {
					n_args.append (c);
				}
			}
			if (len (n_args) > 0) {
				self.args = n_args;
			}
			if (l.search !== '') {
				var p = dict ();
				var add_in_p = function (k, v) {
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
					p [k] = v;
				};
				var t_params = l.searchParams;
				t_params.forEach ((function __lambda__ (v, k) {
					if (arguments.length) {
						var __ilastarg0__ = arguments.length - 1;
						if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
							var __allkwargs0__ = arguments [__ilastarg0__--];
							for (var __attrib0__ in __allkwargs0__) {
								switch (__attrib0__) {
									case 'v': var v = __allkwargs0__ [__attrib0__]; break;
									case 'k': var k = __allkwargs0__ [__attrib0__]; break;
								}
							}
						}
					}
					else {
					}
					return add_in_p (k, v);
				}));
				self.params = p;
			}
		}
	});},
	get get_arg () {return __get__ (this, function (self, arg) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'arg': var arg = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (arg !== null && arg !== undefined) {
			if (len (self.args) >= int (arg) + 1) {
				return self.args [arg];
			}
			else {
				return null;
			}
		}
		else {
			return null;
		}
	});},
	get get_param () {return __get__ (this, function (self, k) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'k': var k = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		return self.params.py_get (k, null);
	});},
	get _open_way () {return __get__ (this, function (self, way) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'way': var way = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self._process_way (way);
		self._body_flag (self.gate, way);
		var last_way = window.PhanterPWA.get_current_way ();
		self.last_way = last_way;
		if (__in__ (self.gate, window.PhanterPWA.Gates)) {
			if (window.PhanterPWA.DEBUG) {
				sessionStorage.setItem ('current_way', self.way);
				window.PhanterPWA.Gates [self.gate] (self);
			}
			else {
				try {
					window.PhanterPWA.Gates [self.gate] (self);
					try {
						sessionStorage.setItem ('current_way', self.way);
					}
					catch (__except0__) {
					}
				}
				catch (__except0__) {
					if (isinstance (__except0__, Exception)) {
						console.error ("Error on try open '{0}'".format (way));
						window.PhanterPWA.Gates [404] (self);
					}
					else {
						throw __except0__;
					}
				}
			}
		}
		else {
			self.error = 404;
			window.PhanterPWA.Gates [404] (self);
		}
		if (self.DEBUG) {
			if (self._element !== null) {
				console.info ('Using the element ', self._element, "to try way '{0}'. ".format (self.way), 'request: ', self);
			}
			else {
				console.info ("Try programatically way to '{0}'. ".format (self.way), 'request: ', self);
			}
		}
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
			return window.PhanterPWA.ProgressBar.removeEventProgressBar ('OPEN_WAY_{0}'.format (self.timestamp));
		}), 300);
	});},
	get open_way () {return __get__ (this, function (self, way) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'way': var way = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.timestamp = new Date ().getTime ();
		window.PhanterPWA.ProgressBar.addEventProgressBar ('OPEN_WAY_{0}'.format (self.timestamp));
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
			return self._open_way (way);
		}), 30);
	});}
});

//# sourceMappingURL=phanterpwa.frontend.application.map