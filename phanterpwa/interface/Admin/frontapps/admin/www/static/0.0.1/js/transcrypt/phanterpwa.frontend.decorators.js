// Transcrypt'ed from Python, 2021-03-12 02:59:54
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'phanterpwa.frontend.decorators';
export var requires_authentication = function (users_id, users_email, roles_id, roles_name) {
	if (typeof users_id == 'undefined' || (users_id != null && users_id.hasOwnProperty ("__kwargtrans__"))) {;
		var users_id = null;
	};
	if (typeof users_email == 'undefined' || (users_email != null && users_email.hasOwnProperty ("__kwargtrans__"))) {;
		var users_email = null;
	};
	if (typeof roles_id == 'undefined' || (roles_id != null && roles_id.hasOwnProperty ("__kwargtrans__"))) {;
		var roles_id = null;
	};
	if (typeof roles_name == 'undefined' || (roles_name != null && roles_name.hasOwnProperty ("__kwargtrans__"))) {;
		var roles_name = null;
	};
	if (arguments.length) {
		var __ilastarg0__ = arguments.length - 1;
		if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
			var __allkwargs0__ = arguments [__ilastarg0__--];
			for (var __attrib0__ in __allkwargs0__) {
				switch (__attrib0__) {
					case 'users_id': var users_id = __allkwargs0__ [__attrib0__]; break;
					case 'users_email': var users_email = __allkwargs0__ [__attrib0__]; break;
					case 'roles_id': var roles_id = __allkwargs0__ [__attrib0__]; break;
					case 'roles_name': var roles_name = __allkwargs0__ [__attrib0__]; break;
				}
			}
		}
	}
	else {
	}
	var decorator = function (f) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'f': var f = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var requires_authentication_decorator = function (self) {
			var kargs = dict ();
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'self': var self = __allkwargs0__ [__attrib0__]; break;
							default: kargs [__attrib0__] = __allkwargs0__ [__attrib0__];
						}
					}
					delete kargs.__kwargtrans__;
				}
				var args = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
			}
			else {
				var args = tuple ();
			}
			self.status = 200;
			if (any ([users_id !== null, users_email !== null, roles_id !== null, roles_name !== null])) {
				if (isinstance (users_id, tuple ([list, tuple]))) {
					if (__in__ (self.current_user.id, users_id)) {
						return f (self, ...args, __kwargtrans__ (kargs));
					}
				}
				if (isinstance (users_id, int)) {
					if (self.current_user.id == users_id) {
						return f (self, ...args, __kwargtrans__ (kargs));
					}
				}
				if (isinstance (users_email, tuple ([list, tuple]))) {
					if (__in__ (self.current_user.email, users_email)) {
						return f (self, ...args, __kwargtrans__ (kargs));
					}
				}
				if (isinstance (users_email, str)) {
					if (users_email == self.current_user.email) {
						return f (self, ...args, __kwargtrans__ (kargs));
					}
				}
				if (isinstance (self.current_user.roles, list)) {
					if (isinstance (roles_id, int)) {
						for (var x of self.current_user.roles_id) {
							if (x == roles_id) {
								return f (self, ...args, __kwargtrans__ (kargs));
							}
						}
					}
					if (isinstance (roles_name, str)) {
						for (var x of self.current_user.roles) {
							if (x == roles_name) {
								return f (self, ...args, __kwargtrans__ (kargs));
							}
						}
					}
					if (isinstance (roles_id, tuple ([list, tuple]))) {
						for (var x of self.current_user.roles_id) {
							if (__in__ (x, roles_id)) {
								return f (self, ...args, __kwargtrans__ (kargs));
							}
						}
					}
					if (isinstance (roles_name, tuple ([list, tuple]))) {
						for (var x of self.current_user.roles) {
							if (__in__ (x, roles_name)) {
								return f (self, ...args, __kwargtrans__ (kargs));
							}
						}
					}
				}
				self.status = 403;
				return self._error (403);
			}
			else if (self.current_user === null || self.current_user === undefined) {
				self.status = 403;
				return self._error (403);
			}
			else {
				return f (self, ...args, __kwargtrans__ (kargs));
			}
		};
		return requires_authentication_decorator;
	};
	return decorator;
};
export var requires_no_authentication = function () {
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
	var decorator = function (f) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'f': var f = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var requires_no_authentication_decorator = function (self) {
			var kargs = dict ();
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'self': var self = __allkwargs0__ [__attrib0__]; break;
							default: kargs [__attrib0__] = __allkwargs0__ [__attrib0__];
						}
					}
					delete kargs.__kwargtrans__;
				}
				var args = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
			}
			else {
				var args = tuple ();
			}
			self.status = 200;
			if (self.phanterpwa_current_user === null || self.phanterpwa_current_user === undefined) {
				return f (self, ...args, __kwargtrans__ (kargs));
			}
			else {
				self.status = 403;
				return self._error (403);
			}
		};
		return requires_no_authentication_decorator;
	};
	return decorator;
};
export var check_authorization = function (authorization_test, on_error) {
	if (typeof authorization_test == 'undefined' || (authorization_test != null && authorization_test.hasOwnProperty ("__kwargtrans__"))) {;
		var authorization_test = false;
	};
	if (typeof on_error == 'undefined' || (on_error != null && on_error.hasOwnProperty ("__kwargtrans__"))) {;
		var on_error = null;
	};
	if (arguments.length) {
		var __ilastarg0__ = arguments.length - 1;
		if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
			var __allkwargs0__ = arguments [__ilastarg0__--];
			for (var __attrib0__ in __allkwargs0__) {
				switch (__attrib0__) {
					case 'authorization_test': var authorization_test = __allkwargs0__ [__attrib0__]; break;
					case 'on_error': var on_error = __allkwargs0__ [__attrib0__]; break;
				}
			}
		}
	}
	else {
	}
	var decorator = function (f) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'f': var f = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var check_authorization_decorator = function (responseObj) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'responseObj': var responseObj = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			var test = false;
			if (callable (authorization_test)) {
				var test = authorization_test ();
			}
			if (test === true) {
				window.PhanterPWA.Response = responseObj;
				return f (responseObj);
			}
			else {
				var code = 401;
				if (window.PhanterPWA.logged ()) {
					var code = 403;
				}
				if (callable (on_error)) {
					on_error (code, self);
				}
				else {
					window.PhanterPWA.open_code_way (code, responseObj._request, responseObj);
				}
			}
		};
		return check_authorization_decorator;
	};
	return decorator;
};

//# sourceMappingURL=phanterpwa.frontend.decorators.map