// Transcrypt'ed from Python, 2021-03-15 14:32:34
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as application from './phanterpwa.frontend.application.js';
import * as helpers from './phanterpwa.frontend.helpers.js';
var __name__ = 'phanterpwa.frontend.components.left_bar';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var I = helpers.XmlConstructor.tagger ('i');
export var IMG = helpers.XmlConstructor.tagger ('img', true);
export var CONCATENATE = helpers.CONCATENATE;
export var I18N = helpers.I18N;
export var LeftBar =  __class__ ('LeftBar', [application.Component], {
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
		if (!__in__ ('_id', parameters)) {
			parameters ['_id'] = 'phanterpwa-component-left_bar';
		}
		if (__in__ ('_class', parameters)) {
			parameters ['_class'] = '{0} {1}'.format (parameters ['_class'], 'phanterpwa-component-left_bar-wrapper');
		}
		else {
			parameters ['_class'] = 'phanterpwa-component-left_bar-wrapper';
		}
		var tcontent = [DIV (__kwargtrans__ ({_id: 'phanterpwa-component-left_bar-top'})), DIV (__kwargtrans__ ({_id: 'phanterpwa-component-left_bar-middle'})), DIV (__kwargtrans__ ({_id: 'phanterpwa-component-left_bar-bottom'}))];
		self.all_buttons = list ();
		self.dict_buttons = dict ();
		self.html = DIV (...tcontent, __kwargtrans__ (parameters));
		application.Component.__init__ (self, 'left_bar', self.html);
		self.html_to (target_selector);
	});},
	get add_button () {return __get__ (this, function (self, button) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'button': var button = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		if (isinstance (button, tuple ([LeftBarMenu, LeftBarButton, LeftBarUserMenu]))) {
			var id_button = button.identifier;
			var has_button = false;
			var cont = 0;
			var position = null;
			for (var b of self.all_buttons) {
				if (b.identifier == id_button) {
					var has_button = true;
					var position = cont;
				}
				cont++;
			}
			if (!(has_button)) {
				self.all_buttons.append (button);
			}
			else {
				self.all_buttons [position] = button;
			}
		}
		self.reload ();
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
		self.element_target = $ (self.target_selector);
		for (var x of self.all_buttons) {
			var id_button = 'phanterpwa-component-left_bar-menu_button-{0}'.format (x.identifier);
			if (all ([self._check_button_requires_login (x), self._check_button_ways (x), self._check_button_roles (x)])) {
				var position = self._get_button_position (x);
				var b = self.element_target.find ('#phanterpwa-component-left_bar-{0}'.format (position)).find ('#{0}'.format (id_button));
				if (b.length > 0) {
					b.parent ().remove ();
				}
				self.element_target.find ('#phanterpwa-component-left_bar-{0}'.format (position)).append (x.jquery ());
				x.start ();
			}
			else {
				self.element_target.find ('#{0}'.format (id_button)).parent ().remove ();
			}
		}
		window.PhanterPWA.reload_events (__kwargtrans__ (dict ({'selector': '#phanterpwa-component-left_bar'})));
	});},
	get _get_button_position () {return __get__ (this, function (self, button) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'button': var button = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var pos = button.position;
		if (pos !== null && pos !== undefined) {
			if (__in__ (pos, ['middle', 'top'])) {
				return pos;
			}
		}
		return 'bottom';
	});},
	get _check_button_requires_login () {return __get__ (this, function (self, button) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'button': var button = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var requires_login = button.requires_login;
		if (requires_login !== null && requires_login !== undefined) {
			if (requires_login === true) {
				var authorization = window.PhanterPWA.get_authorization ();
				if (authorization !== null) {
					return true;
				}
			}
			else {
				return true;
			}
		}
		return false;
	});},
	get _check_button_roles () {return __get__ (this, function (self, button) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'button': var button = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var roles = button.autorized_roles;
		if (roles !== null && roles !== undefined) {
			if (isinstance (roles, list)) {
				if (__in__ ('all', roles)) {
					return true;
				}
				var auth_user = window.PhanterPWA.get_auth_user ();
				if (auth_user !== null) {
					if (isinstance (auth_user.roles, list) && isinstance (roles, list)) {
						if (len (set (auth_user.roles).intersection (set (roles))) > 0) {
							return true;
						}
					}
				}
				else if (__in__ ('anonymous', roles)) {
					return true;
				}
			}
		}
		return false;
	});},
	get _check_button_ways () {return __get__ (this, function (self, button) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'button': var button = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var current_way = window.PhanterPWA.get_current_way ();
		var ways = button.ways;
		if (ways !== null && ways !== undefined) {
			if (isinstance (ways, list)) {
				if (__in__ ('all', ways)) {
					return true;
				}
				else if (__in__ (current_way, ways)) {
					return true;
				}
				else {
					for (var x of ways) {
						if (callable (x)) {
							if (x (current_way) === true) {
								return true;
							}
						}
						else if (x.startswith ('^')) {
							var r = new RegExp (x);
							var result = current_way.match (r);
							if (result !== null) {
								return true;
							}
						}
					}
				}
			}
		}
		return false;
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
		$ ('#phanterpwa-component-left_bar').addClass ('enabled');
	};},
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
		self._open ();
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
		$ ('#phanterpwa-component-left_bar').removeClass ('enabled').removeClass ('enabled_submenu').find ('.phanterpwa-component-left_bar-menu_button-wrapper').removeClass ('enabled');
	};},
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
		self._close ();
	});}
});
export var LeftBarMainButton =  __class__ ('LeftBarMainButton', [application.Component], {
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
		self._icon = I (__kwargtrans__ ({_class: 'fas fa-bars'}));
		if (!__in__ ('_id', parameters)) {
			parameters ['_id'] = 'phanterpwa-component-left_bar-main_button';
		}
		if (__in__ ('_class', parameters)) {
			parameters ['_class'] = '{0} {1}'.format (parameters ['_class'], 'phanterpwa-component-left_bar-main_button-wrapper wave_on_click waves-phanterpwa link');
		}
		else {
			parameters ['_class'] = '{0} {1}'.format ('phanterpwa-component-left_bar-main_button-wrapper', 'wave_on_click waves-phanterpwa link');
		}
		if (__in__ ('icon', parameters)) {
			self._icon = parameters ['icon'];
		}
		var html = DIV (self._icon, __kwargtrans__ (parameters));
		application.Component.__init__ (self, 'left_bar_main_button', html);
		self.html_to (target_selector);
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
		if (el.hasClass ('enabled') || el.hasClass ('enabled_submenu')) {
			self.close_leftbar ();
		}
		else {
			self.open_leftbar ();
		}
	});},
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
		self.element_target = $ (self.target_selector);
		self.element_target.find ('#phanterpwa-component-left_bar-main_button').removeClass ('enabled').removeClass ('enabled_submenu');
		LeftBar._close ();
	});},
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
		self.element_target = $ (self.target_selector);
		self.element_target.find ('#phanterpwa-component-left_bar-main_button').addClass ('enabled');
		LeftBar._open ();
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
		self.element_target = $ (self.target_selector);
		self.element_target.find ('#phanterpwa-component-left_bar-main_button').off ('click.mainbutton_leftbar').on ('click.mainbutton_leftbar', (function __lambda__ () {
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
			return self.switch_leftbar ();
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
		self._binds ();
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
		self._binds ();
	});}
});
export var LeftBarButton =  __class__ ('LeftBarButton', [helpers.XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, identifier, label, icon) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'identifier': var identifier = __allkwargs0__ [__attrib0__]; break;
						case 'label': var label = __allkwargs0__ [__attrib0__]; break;
						case 'icon': var icon = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		self.identifier = identifier;
		self.label = label;
		self.icon = icon;
		self.requires_login = false;
		self.autorized_roles = ['all'];
		self.ways = ['all'];
		self.position = 'bottom';
		self._on_start = parameters.py_get ('onStart', null);
		parameters ['_id'] = 'phanterpwa-component-left_bar-menu_button-{0}'.format (self.identifier);
		if (__in__ ('_class', parameters)) {
			parameters ['_class'] = '{0} {1}'.format (parameters ['_class'], 'phanterpwa-component-left_bar-button link');
		}
		else {
			parameters ['_class'] = 'phanterpwa-component-left_bar phanterpwa-component-left_bar-button link';
		}
		if (__in__ ('requires_login', parameters)) {
			self.requires_login = parameters ['requires_login'];
		}
		if (__in__ ('autorized_roles', parameters)) {
			if (isinstance (parameters ['autorized_roles'], list)) {
				self.autorized_roles = parameters ['autorized_roles'];
			}
			else if (window.PhanterPWA.DEBUG) {
				console.error ("The parameter 'autorized_roles' must be type list");
			}
		}
		if (__in__ ('ways', parameters)) {
			if (isinstance (parameters ['ways'], list)) {
				self.ways = parameters ['ways'];
			}
			else if (window.PhanterPWA.DEBUG) {
				console.error ("The parameter 'ways' must be type list");
			}
		}
		if (__in__ ('position', parameters)) {
			self.position = parameters ['position'];
		}
		var content = [DIV (DIV (self.icon, __kwargtrans__ ({_class: 'phanterpwa-component-left_bar-icon-container'})), DIV (self.label, __kwargtrans__ ({_class: 'phanterpwa-component-left_bar-label'})), __kwargtrans__ (parameters))];
		helpers.XmlConstructor.__init__ (self, 'div', false, ...content, __kwargtrans__ ({_class: 'phanterpwa-component-left_bar-menu_button-wrapper'}));
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
			console.info ('start button {0}'.format (self.identifier));
		}
		if (callable (self._on_start)) {
			self._on_start ();
		}
	});}
});
export var LeftBarSubMenu =  __class__ ('LeftBarSubMenu', [helpers.XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, identifier, label) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'identifier': var identifier = __allkwargs0__ [__attrib0__]; break;
						case 'label': var label = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		self.identifier = identifier;
		self.label = label;
		self.initial_class = 'phanterpwa-component-left_bar-submenu-button link';
		parameters ['_id'] = 'phanterpwa-component-left_bar-submenu-button-{0}'.format (identifier);
		if (__in__ ('_class', parameters)) {
			self.initial_class = ' '.join ([parameters ['_class'].strip (), 'phanterpwa-component-left_bar-submenu-button link']);
		}
		parameters ['_class'] = self.initial_class;
		var content = [DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-right'})), __kwargtrans__ ({_class: 'phanterpwa-component-left_bar-submenu-icon-container'})), DIV (self.label, __kwargtrans__ ({_class: 'phanterpwa-component-left_bar-submenu-label'}))];
		helpers.XmlConstructor.__init__ (self, 'div', false, ...content, __kwargtrans__ (parameters));
	});}
});
export var LeftBarMenu =  __class__ ('LeftBarMenu', [helpers.XmlConstructor], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, identifier, label, icon) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'identifier': var identifier = __allkwargs0__ [__attrib0__]; break;
						case 'label': var label = __allkwargs0__ [__attrib0__]; break;
						case 'icon': var icon = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		self.identifier = identifier;
		self.label = label;
		self.icon = icon;
		self.parameters = parameters;
		self.submenus = [];
		self.componentSubmenu = LeftBarSubMenu;
		self.requires_login = false;
		self.autorized_roles = ['all'];
		self.ways = ['all'];
		self.position = 'bottom';
		parameters ['_id'] = 'phanterpwa-component-left_bar-menu_button-{0}'.format (self.identifier);
		if (__in__ ('_class', parameters)) {
			parameters ['_class'] = '{0} {1}'.format (parameters ['_class'], 'phanterpwa-component-left_bar-menu link');
		}
		else {
			parameters ['_class'] = 'phanterpwa-component-left_bar phanterpwa-component-left_bar-menu link';
		}
		if (__in__ ('requires_login', parameters)) {
			self.requires_login = parameters ['requires_login'];
		}
		if (__in__ ('autorized_roles', parameters)) {
			if (isinstance (parameters ['autorized_roles'], list)) {
				self.autorized_roles = parameters ['autorized_roles'];
			}
			else if (window.PhanterPWA.DEBUG) {
				console.error ("The parameter 'autorized_roles' must be type list");
			}
		}
		if (__in__ ('ways', parameters)) {
			if (isinstance (parameters ['ways'], list)) {
				self.ways = parameters ['ways'];
			}
			else if (window.PhanterPWA.DEBUG) {
				console.error ("The parameter 'ways' must be type list");
			}
		}
		if (__in__ ('position', parameters)) {
			self.position = parameters ['position'];
		}
		helpers.XmlConstructor.__init__ (self, 'div', false, __kwargtrans__ ({_class: 'phanterpwa-component-left_bar-menu_button-wrapper'}));
		self._update_content ();
	});},
	get addSubmenu () {return __get__ (this, function (self, identifier, label) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'identifier': var identifier = __allkwargs0__ [__attrib0__]; break;
						case 'label': var label = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		self.submenus.append (LeftBarSubMenu (identifier, label, __kwargtrans__ (parameters)));
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
		var html_submenus = '';
		if (self.submenus) {
			self.parameters ['_target_submenu'] = 'phanterpwa-component-left_bar-submenu-from-{0}'.format (self.identifier);
			var html_submenus = DIV (...self.submenus, __kwargtrans__ ({_id: self.parameters ['_target_submenu'], _class: 'phanterpwa-component-left_bar-submenu-container'}));
		}
		self.content = [DIV (DIV (self.icon, __kwargtrans__ ({_class: 'phanterpwa-component-left_bar-icon-container'})), DIV (self.label, __kwargtrans__ ({_class: 'phanterpwa-component-left_bar-label'})), __kwargtrans__ (self.parameters)), html_submenus];
	});},
	get switch_menu () {return __get__ (this, function (self, el) {
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
		if ($ (el).parent ().hasClass ('enabled')) {
			self.close_menu ();
		}
		else {
			self.open_menu ();
		}
	});},
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
		var element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-menu_button-{0}'.format (self.identifier)).parent ();
		element.addClass ('enabled');
		$ ('#phanterpwa-component-left_bar').addClass ('enabled_submenu').addClass ('enabled');
		$ ('#phanterpwa-component-left_bar-main_button').addClass ('enabled');
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
		var element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-menu_button-{0}'.format (self.identifier)).parent ();
		element.removeClass ('enabled');
		if ($ ('#phanterpwa-component-left_bar').find ('.phanterpwa-component-left_bar-menu_button-wrapper.enabled').length == 0) {
			$ ('#phanterpwa-component-left_bar').removeClass ('enabled_submenu').removeClass ('enabled');
			$ ('#phanterpwa-component-left_bar-main_button').removeClass ('enabled');
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
		var sub_element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-submenu-from-{0} {1}'.format (self.identifier, '.phanterpwa-component-left_bar-submenu-button'));
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
	});}
});
export var LeftBarUserMenu =  __class__ ('LeftBarUserMenu', [helpers.XmlConstructor], {
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
		self.identifier = 'auth_user_login';
		self.submenus = [];
		self.parameters = parameters;
		self.requires_login = true;
		self.autorized_roles = ['all'];
		self.ways = ['all'];
		self.position = 'bottom';
		parameters ['_id'] = 'phanterpwa-component-left_bar-menu_button-{0}'.format (self.identifier);
		if (__in__ ('_class', parameters)) {
			parameters ['_class'] = '{0} {1}'.format (parameters ['_class'], 'phanterpwa-component-left_bar-menu link');
		}
		else {
			parameters ['_class'] = 'phanterpwa-component-left_bar phanterpwa-component-left_bar-menu link';
		}
		if (__in__ ('requires_login', parameters)) {
			self.requires_login = parameters ['requires_login'];
		}
		if (__in__ ('autorized_roles', parameters)) {
			if (isinstance (parameters ['autorized_roles'], list)) {
				self.autorized_roles = parameters ['autorized_roles'];
			}
			else if (window.PhanterPWA.DEBUG) {
				console.error ("The parameter 'autorized_roles' must be type list");
			}
		}
		if (__in__ ('ways', parameters)) {
			if (isinstance (parameters ['ways'], list)) {
				self.ways = parameters ['ways'];
			}
			else if (window.PhanterPWA.DEBUG) {
				console.error ("The parameter 'ways' must be type list");
			}
		}
		if (__in__ ('position', parameters)) {
			self.position = parameters ['position'];
		}
		self._image = IMG (__kwargtrans__ ({_id: 'phanterpwa-component-left_bar-url-imagem-user', _src: '/static/{0}/images/user.png'.format (window.PhanterPWA.CONFIG.PROJECT.version), _alt: 'user avatar'}));
		helpers.XmlConstructor.__init__ (self, 'div', false, __kwargtrans__ ({_class: '{0} {1}'.format ('phanterpwa-component-left_bar-menu_button-wrapper-auth_user', 'phanterpwa-component-left_bar-menu_button-wrapper')}));
		self._update_content ();
	});},
	get addSubmenu () {return __get__ (this, function (self, identifier, label) {
		var parameters = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'identifier': var identifier = __allkwargs0__ [__attrib0__]; break;
						case 'label': var label = __allkwargs0__ [__attrib0__]; break;
						default: parameters [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete parameters.__kwargtrans__;
			}
		}
		else {
		}
		self.submenus.append (LeftBarSubMenu (identifier, label, __kwargtrans__ (parameters)));
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
		var html_submenus = '';
		self.parameters;
		if (self.submenus) {
			self.parameters ['_target_submenu'] = 'phanterpwa-component-left_bar-submenu-from-{0}'.format (self.identifier);
			var html_submenus = DIV (...self.submenus, __kwargtrans__ ({_id: self.parameters ['_target_submenu'], _class: 'phanterpwa-component-left_bar-submenu-container'}));
		}
		self.content = [DIV (DIV (DIV (self._image, __kwargtrans__ ({_class: 'phanterpwa-component-left_bar-image-user'})), __kwargtrans__ ({_class: 'phanterpwa-component-left_bar-image-user-container'})), DIV (self.name_user, __kwargtrans__ ({_id: 'phanterpwa-component-left_bar-name-user', _class: 'phanterpwa-component-left_bar-label'})), __kwargtrans__ (self.parameters)), html_submenus];
	});},
	get switch_menu () {return __get__ (this, function (self, el) {
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
		if ($ (el).parent ().hasClass ('enabled')) {
			self.close_menu ();
		}
		else {
			self.open_menu ();
		}
	});},
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
		var element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-menu_button-{0}'.format (self.identifier)).parent ();
		element.addClass ('enabled');
		$ ('#phanterpwa-component-left_bar').addClass ('enabled_submenu').addClass ('enabled');
		$ ('#phanterpwa-component-left_bar-main_button').addClass ('enabled');
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
		var element = $ ('#phanterpwa-component-left_bar').find ('#phanterpwa-component-left_bar-menu_button-{0}'.format (self.identifier)).parent ();
		element.removeClass ('enabled');
		if ($ ('#phanterpwa-component-left_bar').find ('.phanterpwa-component-left_bar-menu_button-wrapper.enabled').length == 0) {
			$ ('#phanterpwa-component-left_bar').removeClass ('enabled_submenu').removeClass ('enabled');
			$ ('#phanterpwa-component-left_bar-main_button').removeClass ('enabled');
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
		var user_image = '/static/{0}/images/user.png'.format (window.PhanterPWA.CONFIG.PROJECT.version);
		if (self.auth_user !== null) {
			var first_name = self.auth_user.first_name;
			var last_name = self.auth_user.last_name;
			var user_name = '{0} {1}'.format (first_name, last_name);
			var role = I18N (self.auth_user.role);
			if (self.auth_user.image !== null && self.auth_user.image !== undefined) {
				var user_image = self.auth_user.image;
			}
		}
		element.find ('#phanterpwa-component-left_bar-url-imagem-user').attr ('src', user_image);
		element.find ('#phanterpwa-component-left_bar-name-user').text (user_name);
	});}
});

//# sourceMappingURL=phanterpwa.frontend.components.left_bar.map