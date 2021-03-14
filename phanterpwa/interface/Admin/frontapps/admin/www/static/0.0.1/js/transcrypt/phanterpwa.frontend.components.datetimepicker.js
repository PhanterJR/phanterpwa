// Transcrypt'ed from Python, 2021-03-10 09:46:27
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as validations from './phanterpwa.frontend.validations.js';
import * as helpers from './phanterpwa.frontend.helpers.js';
var __name__ = 'phanterpwa.frontend.components.datetimepicker';
export var INPUT = helpers.XmlConstructor.tagger ('input', true);
export var I = helpers.XmlConstructor.tagger ('i');
export var DIV = helpers.XmlConstructor.tagger ('div');
export var FORM = helpers.XmlConstructor.tagger ('form');
export var SPAN = helpers.XmlConstructor.tagger ('span');
export var XML = helpers.XML;
export var HR = helpers.XmlConstructor.tagger ('hr', true);
export var I18N = helpers.I18N;
export var Datepickers =  __class__ ('Datepickers', [object], {
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
		self._days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
		self._ordinaries = ['st', 'nd', 'rd', 'th'];
		self._months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
		self._times = ['hours', 'minutes', 'seconds'];
		self.ordinaries = list (self._ordinaries);
		self.namespace = new Date ().getTime ();
		self.target_selector = target_selector;
		self.days = list (self._days);
		self.months = list (self._months);
		self.times = list (self._times);
		self.date_type = 'datetime';
		self.debug = window.PhanterPWA.DEBUG;
		if (__in__ ('debug', parameters)) {
			self.debug = parameters ['debug'];
		}
		if (__in__ ('date_type', parameters)) {
			self._date_type (parameters ['date_type']);
		}
		self.now = new Date ();
		self.selected_date = new Date (self.now.getFullYear (), self.now.getMonth (), self.now.getDate ());
		self.current_date = new Date (self.now.getFullYear (), self.now.getMonth (), 1);
		if ($ (self.target_selector).length > 0) {
			if ($ (self.target_selector) [0].hasAttribute ('phanterpwa-datetimepicker-iso')) {
				var phanterpwa_datetimepicker_iso = $ (self.target_selector).attr ('phanterpwa-datetimepicker-iso');
				console.log (phanterpwa_datetimepicker_iso);
				self.selected_date = new Date (phanterpwa_datetimepicker_iso);
				console.log (self.selected_date);
				self.current_date = new Date (self._apply_format ('yyyy-MM-01 HH:ss:mm'));
			}
		}
		self.format = 'yyyy-MM-dd';
		if (self.date_type == 'datetime') {
			self.format = 'yyyy-MM-dd HH:ss:mm';
		}
		if (__in__ ('format', parameters)) {
			self.format = self._map_escape_str (parameters ['format']);
		}
		self.format_in = 'yyyy-MM-dd HH:ss:mm';
		if (__in__ ('current_date', parameters)) {
			if (__in__ ('format', parameters)) {
				self._read_formated (parameters ['current_date']);
			}
			else {
				self._selected_date (parameters ['current_date']);
			}
		}
		self.onChoice = null;
		if (__in__ ('onChoice', parameters)) {
			self.onChoice = parameters ['onChoice'];
		}
		if (__in__ ('id_input_target', parameters)) {
			self.id_input_target = parameters ['id_input_target'];
			if ($ (self.id_input_target).length > 0) {
				if (validations.check_datetime ($ (self.id_input_target).val (), self.format, self.date_type)) {
					self._read_formated ($ (self.id_input_target).val ());
					var iso_format = self._apply_format ('yyyy-MM-dd HH:ss:mm');
					$ (self.target_selector).attr ('phanterpwa-datetimepicker-iso', iso_format);
				}
			}
		}
	});},
	get _onChoice () {return __get__ (this, function (self) {
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
		if (callable (self.onChoice)) {
			var iso_format = self._apply_format ('yyyy-MM-dd HH:ss:mm');
			$ (self.target_selector).attr ('phanterpwa-datetimepicker-iso', iso_format);
			var data = {'iso': iso_format, 'formated': self._apply_format (self.format)};
			self.onChoice (data);
		}
		else {
			var iso_format = self._apply_format ('yyyy-MM-dd HH:ss:mm');
			$ (self.target_selector).attr ('phanterpwa-datetimepicker-iso', iso_format);
			if ($ (self.id_input_target).length > 0) {
				$ (self.id_input_target).val (self._apply_format (self.format)).focus ();
			}
			if (self.debug) {
				console.info (self._apply_format (self.format));
			}
		}
	});},
	get _sanitize_i18ns () {return __get__ (this, function (self, value) {
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
		var reserved_letters = dict ({'d': '&#100;', 'M': '&#77;', 't': '&#116;', 'o': '&#111;', 'y': '&#121;', 'H': '&#72;', 'm': '&#109;', 's': '&#115;'});
		for (var x of reserved_letters.py_keys ()) {
			if (__in__ (x, value)) {
				var value = value.py_replace (x, reserved_letters [x]);
			}
		}
		return value;
	});},
	get _map_escape_str () {return __get__ (this, function (self, value) {
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
		var reserved_letters = dict ({'\\d': '&#100;', '\\M': '&#77;', '\\t': '&#116;', '\\o': '&#111;', '\\y': '&#121;', '\\H': '&#72;', '\\m': '&#109;', '\\s': '&#115;'});
		for (var x of reserved_letters.py_keys ()) {
			if (__in__ (x, value)) {
				var value = value.py_replace (x, reserved_letters [x]);
			}
		}
		return value;
	});},
	get _unsanitize_str () {return __get__ (this, function (self, value) {
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
		var htmls_codes = dict ({'&#100;': 'd', '&#77;': 'M', '&#116;': 't', '&#111;': 'o', '&#121;': 'y', '&#72;': 'H', '&#109;': 'm', '&#115;': 's'});
		for (var x of htmls_codes.py_keys ()) {
			if (__in__ (x, value)) {
				var value = value.py_replace (x, htmls_codes [x]);
			}
		}
		return value;
	});},
	get _read_formated () {return __get__ (this, function (self, value) {
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
		var filted_format = self.format;
		var filted_value = self._sanitize_i18ns (self._map_escape_str (value));
		if (__in__ ('dddd', filted_format)) {
			var p = '|'.join ((function () {
				var __accu0__ = [];
				for (var x of self.days) {
					__accu0__.append (self._sanitize_i18ns (x));
				}
				return __accu0__;
			}) ());
			var r = '{0}'.format (p);
			var r = new RegExp (r);
			console.error (r);
			var filted_value = filted_value.replace (r, '');
			var filted_format = filted_format.py_replace ('dddd', '');
		}
		if (__in__ ('ddd', filted_format)) {
			var p = '|'.join ((function () {
				var __accu0__ = [];
				for (var x of self.days) {
					__accu0__.append (self._sanitize_i18ns (x.__getslice__ (0, 3, 1)));
				}
				return __accu0__;
			}) ());
			var r = '{0}'.format (p);
			var r = new RegExp (r);
			var filted_value = filted_value.replace (r, '');
			var filted_format = filted_format.py_replace ('ddd', '');
		}
		if (__in__ ('MMMM', filted_format)) {
			var p = '|'.join ((function () {
				var __accu0__ = [];
				for (var x of self.months) {
					__accu0__.append (self._sanitize_i18ns (x));
				}
				return __accu0__;
			}) ());
			var r = '{0}'.format (p);
			var r = new RegExp (r);
			var filted_value = filted_value.replace (r, '');
			var filted_format = filted_format.py_replace ('MMMM', '');
		}
		if (__in__ ('MMM', filted_format)) {
			var p = '|'.join ((function () {
				var __accu0__ = [];
				for (var x of self.months) {
					__accu0__.append (self._sanitize_i18ns (x.__getslice__ (0, 3, 1)));
				}
				return __accu0__;
			}) ());
			var r = '{0}'.format (p);
			var r = new RegExp (r);
			var filted_value = filted_value.replace (r, '');
			var filted_format = filted_format.py_replace ('MMM', '');
		}
		if (__in__ ('do', filted_format) || __in__ ('Mo', filted_format)) {
			var o = (function () {
				var __accu0__ = [];
				for (var x of self.ordinaries) {
					__accu0__.append (self._sanitize_i18ns (x));
				}
				return __accu0__;
			}) ();
			var r = (((((('1' + o [0]) + '|2') + o [1]) + '|3') + o [2]) + '|[0-9]{1,2}') + o [3];
			var r = new RegExp (r);
			var filted_value = filted_value.replace (r, '');
			var filted_format = filted_format.py_replace ('do', '').py_replace ('Mo', '');
		}
		if (__in__ ('tt', filted_format)) {
			var r = self._sanitize_i18ns ('/PM|AM/');
			var r = new RegExp (r);
			var filted_value = filted_value.replace (r, '');
			var filted_format = filted_format.py_replace ('tt', '');
		}
		var day = null;
		var month = null;
		var year = null;
		var hour = '00';
		var minute = '00';
		var second = '00';
		if (__in__ ('dd', filted_format)) {
			var ini = filted_format.indexOf ('dd');
			var day = filted_value.__getslice__ (ini, ini + 2, 1);
		}
		else {
			var __except0__ = ValueError ("The format must be 'dd' in your pattern");
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (__in__ ('MM', filted_format)) {
			var ini = filted_format.indexOf ('MM');
			var month = filted_value.__getslice__ (ini, ini + 2, 1);
		}
		else {
			var __except0__ = ValueError ("The format must be 'MM' in your pattern");
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (__in__ ('yyyy', filted_format)) {
			var ini = filted_format.indexOf ('yyyy');
			var year = filted_value.__getslice__ (ini, ini + 4, 1);
		}
		else {
			var __except0__ = ValueError ("The format must be 'yyyy' in your pattern");
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (__in__ ('HH', filted_format)) {
			var ini = filted_format.indexOf ('HH');
			var hour = filted_value.__getslice__ (ini, ini + 2, 1);
		}
		else if (self.date_type == 'datetime') {
			var __except0__ = ValueError ("The datetime format must be 'HH' in your pattern");
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (__in__ ('mm', filted_format)) {
			var ini = filted_format.indexOf ('mm');
			var minute = filted_value.__getslice__ (ini, ini + 2, 1);
		}
		else if (self.date_type == 'datetime') {
			var __except0__ = ValueError ("The datetime format must be 'mm' in your pattern");
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (__in__ ('ss', filted_format)) {
			var ini = filted_format.indexOf ('ss');
			var second = filted_value.__getslice__ (ini, ini + 2, 1);
		}
		else if (self.date_type == 'datetime') {
			var __except0__ = ValueError ("The datetime format must be 'ss' in your pattern");
			__except0__.__cause__ = null;
			throw __except0__;
		}
		self.selected_date = new Date ('{0}-{1}-{2} {3}:{4}:{5}'.format (year, month, day, hour, minute, second));
		self.current_date = new Date ('{0}-{1}-01 {2}:{3}:{4}'.format (year, month, hour, minute, second));
	});},
	get _apply_format () {return __get__ (this, function (self, value) {
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
		var smonth = self.selected_date.getMonth ();
		var sday = self.selected_date.getDate ();
		var sweek = self.selected_date.getDay ();
		var syear = self.selected_date.getFullYear ();
		var shour = self.selected_date.getHours ();
		var sminute = self.selected_date.getMinutes ();
		var ssecond = self.selected_date.getSeconds ();
		if (__in__ ('dddd', value)) {
			var value = value.py_replace ('dddd', self._sanitize_i18ns (self.days [sweek]));
		}
		if (__in__ ('ddd', value)) {
			var value = value.py_replace ('ddd', self._sanitize_i18ns (self.days [sweek].__getslice__ (0, 3, 1)));
		}
		if (__in__ ('dd', value)) {
			var value = value.py_replace ('dd', self._zfill (sday, 2));
		}
		if (__in__ ('do', value)) {
			if (sday == 1) {
				var ordi = self.ordinaries [0];
			}
			else if (sday == 2) {
				var ordi = self.ordinaries [1];
			}
			else if (sday == 3) {
				var ordi = self.ordinaries [2];
			}
			else {
				var ordi = self.ordinaries [3];
			}
			var nordi = '{0}{1}'.format (sday, self._sanitize_i18ns (ordi));
			var value = value.py_replace ('do', nordi);
		}
		if (__in__ ('MMMM', value)) {
			var value = value.py_replace ('MMMM', self._sanitize_i18ns (self.months [smonth]));
		}
		if (__in__ ('MMM', value)) {
			var value = value.py_replace ('MMM', self._sanitize_i18ns (self.months [smonth].__getslice__ (0, 3, 1)));
		}
		if (__in__ ('MM', value)) {
			console.log (smonth);
			var value = value.py_replace ('MM', self._zfill (smonth + 1, 2));
		}
		if (__in__ ('Mo', value)) {
			if (smonth + 1 == 1) {
				var ordi = self.ordinaries [0];
			}
			else if (smonth + 1 == 2) {
				var ordi = self.ordinaries [1];
			}
			else if (smonth + 1 == 3) {
				var ordi = self.ordinaries [2];
			}
			else {
				var ordi = self.ordinaries [3];
			}
			var nordi = '{0}{1}'.format (smonth + 1, self._sanitize_i18ns (ordi));
			var value = value.py_replace ('Mo', nordi);
		}
		if (__in__ ('yyyy', value)) {
			var value = value.py_replace ('yyyy', syear);
		}
		if (__in__ ('HH', value)) {
			var value = value.py_replace ('HH', self._zfill (shour, 2));
		}
		if (__in__ ('mm', value)) {
			var value = value.py_replace ('mm', self._zfill (sminute, 2));
		}
		if (__in__ ('ss', value)) {
			var value = value.py_replace ('ss', self._zfill (ssecond, 2));
		}
		var AM_PM = 'PM';
		if (shour < 12) {
			var AM_PM = 'AM';
		}
		if (__in__ ('tt', value)) {
			var value = value.py_replace ('tt', AM_PM);
		}
		return self._unsanitize_str (value);
	});},
	get _zfill () {return __get__ (this, function (self, number, size) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'number': var number = __allkwargs0__ [__attrib0__]; break;
						case 'size': var size = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		console.log (number);
		var number = int (number);
		var number = str (number);
		var s = number;
		for (var x = 0; x < size - len (number); x++) {
			var s = '0' + s;
		}
		return s;
	});},
	get _date_type () {return __get__ (this, function (self, value) {
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
		if (value != 'datetime' && value != 'date') {
			var __except0__ = ValueError ("The date_type must be 'datetime' or 'date'. Given '{0}'".format (value));
			__except0__.__cause__ = null;
			throw __except0__;
		}
		self.date_type = value;
	});},
	get _selected_date () {return __get__ (this, function (self, value) {
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
		if (self.date_type == 'date') {
			var REGEX_BODY = /^([0-9]{4}-[0-9]{2}-[0-9]{2})/
			if (REGEX_BODY.test (value)) {
				self.selected_date = new Date ('{0} 00:00:00'.format (value.__getslice__ (0, 10, 1)));
				self.current_date = new Date ('{0}01 00:00:00'.format (value.__getslice__ (0, 8, 1)));
			}
			else {
				var __except0__ = ValueError ("The current_date must be 'yyyy-mm-dd'. Example: 2019-01-01");
				__except0__.__cause__ = null;
				throw __except0__;
			}
		}
		else if (self.date_type == 'datetime') {
			var REGEX_BODY = /^([0-9]{4}-[0-9]{2}-[0-9]{2}.{1}[0-9]{2}:[0-9]{2}:[0-9]{2})/
			if (REGEX_BODY.test (value)) {
				self.selected_date = new Date ('{0} {1}'.format (value.__getslice__ (0, 10, 1), value.__getslice__ (11, 19, 1)));
				self.current_date = new Date ('{0}01 {1}'.format (value.__getslice__ (0, 8, 1), value.__getslice__ (11, 19, 1)));
			}
			else {
				var __except0__ = ValueError ("The current_date must be 'yyyy-mm-dd'. Example: 2019-01-01");
				__except0__.__cause__ = null;
				throw __except0__;
			}
		}
		else {
			var __except0__ = ValueError ("The date_type must be 'datetime' or 'date'. Given '{0}'".format (value));
			__except0__.__cause__ = null;
			throw __except0__;
		}
	});},
	get previus_year () {return __get__ (this, function (self) {
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
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var cmonth = self.current_date.getMonth ();
		var cday = self.current_date.getDate ();
		var cyear = self.current_date.getFullYear ();
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear - 1, self._zfill (cmonth + 1, 2), self._zfill (cday, 2), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get next_year () {return __get__ (this, function (self) {
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
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var cmonth = self.current_date.getMonth ();
		var cday = self.current_date.getDate ();
		var cyear = self.current_date.getFullYear ();
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear + 1, self._zfill (cmonth + 1, 2), self._zfill (cday, 2), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get previus_month () {return __get__ (this, function (self) {
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
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var cmonth = self.current_date.getMonth ();
		var cyear = self.current_date.getFullYear ();
		var calc_month = cmonth - 1;
		if (calc_month < 0) {
			var calc_month = 11;
		}
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (calc_month + 1, 2), self._zfill (1, 2), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get next_month () {return __get__ (this, function (self) {
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
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var cmonth = self.current_date.getMonth ();
		var cyear = self.current_date.getFullYear ();
		var calc_month = cmonth + 1;
		if (calc_month > 11) {
			var calc_month = 0;
		}
		var sdate = self.selected_date.toJSON ();
		var snew_date = '{0} {1}:{2}:{3}'.format (sdate.__getslice__ (0, 10, 1), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
		self.selected_date = new Date (snew_date);
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (calc_month + 1, 2), self._zfill (1, 2), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get previus_hour () {return __get__ (this, function (self) {
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
		var cyear = self.current_date.getFullYear ();
		var cmonth = self.current_date.getMonth ();
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var calc_hour = chour - 1;
		if (calc_hour < 0) {
			var calc_hour = 23;
		}
		var sdate = self.selected_date.toJSON ();
		var snew_date = '{0} {1}:{2}:{3}'.format (sdate.__getslice__ (0, 10, 1), self._zfill (calc_hour, 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
		self.selected_date = new Date (snew_date);
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (cmonth + 1, 2), self._zfill (1, 2), self._zfill (calc_hour, 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get next_hour () {return __get__ (this, function (self) {
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
		var cyear = self.current_date.getFullYear ();
		var cmonth = self.current_date.getMonth ();
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var calc_hour = chour + 1;
		if (calc_hour > 23) {
			var calc_hour = 0;
		}
		var sdate = self.selected_date.toJSON ();
		var snew_date = '{0} {1}:{2}:{3}'.format (sdate.__getslice__ (0, 10, 1), self._zfill (calc_hour, 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
		self.selected_date = new Date (snew_date);
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (cmonth + 1, 2), self._zfill (1, 2), self._zfill (calc_hour, 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get previus_minute () {return __get__ (this, function (self) {
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
		var cyear = self.current_date.getFullYear ();
		var cmonth = self.current_date.getMonth ();
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var calc_minute = cminute - 1;
		if (calc_minute < 0) {
			var calc_minute = 59;
		}
		var sdate = self.selected_date.toJSON ();
		var snew_date = '{0} {1}:{2}:{3}'.format (sdate.__getslice__ (0, 10, 1), self._zfill (chour, 2), self._zfill (calc_minute, 2), self._zfill (csecond, 2));
		self.selected_date = new Date (snew_date);
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (cmonth + 1, 2), self._zfill (1, 2), self._zfill (chour, 2), self._zfill (calc_minute, 2), self._zfill (csecond, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get next_minute () {return __get__ (this, function (self) {
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
		var cyear = self.current_date.getFullYear ();
		var cmonth = self.current_date.getMonth ();
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var calc_minute = cminute + 1;
		if (calc_minute > 59) {
			var calc_minute = 0;
		}
		var sdate = self.selected_date.toJSON ();
		var snew_date = '{0} {1}:{2}:{3}'.format (sdate.__getslice__ (0, 10, 1), self._zfill (chour, 2), self._zfill (calc_minute, 2), self._zfill (csecond, 2));
		self.selected_date = new Date (snew_date);
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (cmonth + 1, 2), self._zfill (1, 2), self._zfill (chour, 2), self._zfill (calc_minute, 2), self._zfill (csecond, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get previus_second () {return __get__ (this, function (self) {
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
		var cyear = self.current_date.getFullYear ();
		var cmonth = self.current_date.getMonth ();
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var calc_second = csecond - 1;
		if (calc_second < 0) {
			var calc_second = 59;
		}
		var sdate = self.selected_date.toJSON ();
		var snew_date = '{0} {1}:{2}:{3}'.format (sdate.__getslice__ (0, 10, 1), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (calc_second, 2));
		self.selected_date = new Date (snew_date);
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (cmonth + 1, 2), self._zfill (1, 2), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (calc_second, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get next_second () {return __get__ (this, function (self) {
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
		var cyear = self.current_date.getFullYear ();
		var cmonth = self.current_date.getMonth ();
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var calc_second = csecond + 1;
		if (calc_second > 59) {
			var calc_second = 0;
		}
		var sdate = self.selected_date.toJSON ();
		var snew_date = '{0} {1}:{2}:{3}'.format (sdate.__getslice__ (0, 10, 1), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (calc_second, 2));
		self.selected_date = new Date (snew_date);
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (cmonth + 1, 2), self._zfill (1, 2), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (calc_second, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get set_year () {return __get__ (this, function (self, value) {
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
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var REGEX_BODY = /^([0-9]{4})/
		if (REGEX_BODY.test (value)) {
			var cmonth = self.current_date.getMonth ();
			var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (value, self._zfill (cmonth + 1, 2), self._zfill (1, 2), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
			self.current_date = new Date (new_date);
			self.start ();
		}
	});},
	get set_month () {return __get__ (this, function (self, value) {
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
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var cyear = self.current_date.getFullYear ();
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (int (value) + 1, 2), self._zfill (1, 2), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get set_hour () {return __get__ (this, function (self, value) {
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
		var cyear = self.current_date.getFullYear ();
		var cmonth = self.current_date.getMonth ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var sdate = self.selected_date.toJSON ();
		var snew_date = '{0} {1}:{2}:{3}'.format (sdate.__getslice__ (0, 10, 1), self._zfill (int (value), 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
		self.selected_date = new Date (snew_date);
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (cmonth + 1, 2), self._zfill (1, 2), self._zfill (int (value), 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get set_minute () {return __get__ (this, function (self, value) {
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
		var cyear = self.current_date.getFullYear ();
		var cmonth = self.current_date.getMonth ();
		var chour = self.current_date.getHours ();
		var csecond = self.current_date.getSeconds ();
		var sdate = self.selected_date.toJSON ();
		var snew_date = '{0} {1}:{2}:{3}'.format (sdate.__getslice__ (0, 10, 1), self._zfill (chour, 2), self._zfill (value, 2), self._zfill (csecond, 2));
		self.selected_date = new Date (snew_date);
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (cmonth + 1, 2), self._zfill (1, 2), self._zfill (chour, 2), self._zfill (value, 2), self._zfill (csecond, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get set_second () {return __get__ (this, function (self, value) {
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
		var cyear = self.current_date.getFullYear ();
		var cmonth = self.current_date.getMonth ();
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var sdate = self.selected_date.toJSON ();
		var snew_date = '{0} {1}:{2}:{3}'.format (sdate.__getslice__ (0, 10, 1), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (value, 2));
		self.selected_date = new Date (snew_date);
		var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (cmonth + 1, 2), self._zfill (1, 2), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (value, 2));
		self.current_date = new Date (new_date);
		self.start ();
	});},
	get set_selected () {return __get__ (this, function (self, jsonDate) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'jsonDate': var jsonDate = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var new_date = new Date (jsonDate);
		self.selected_date = new_date;
		self._onChoice ();
		self.close ();
	});},
	get show_months () {return __get__ (this, function (self) {
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
		var container = DIV (__kwargtrans__ ({_class: 'phanterpwa_datetimepicker_monthlist_container'}));
		var _month = function (el) {
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
			var m = $ (el).attr ('phanterpwa_datetimepicker_month');
			self.set_month (m);
		};
		var cmonth = self.current_date.getMonth ();
		var row_container = DIV (__kwargtrans__ ({_class: 'phanterpwa_datetimepicker_row'}));
		for (var x = 0; x < 12; x++) {
			var add_class = '';
			if (cmonth == x) {
				var add_class = ' selected';
			}
			row_container.append (DIV (I18N (self.months [x]), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_monthlist_month phanterpwa_datetimepicker_button{0}'.format (add_class), _phanterpwa_datetimepicker_month: x})));
		}
		container.append (row_container);
		container.html_to ('#phanterpwa_datetimepicker_calendar_{0}'.format (self.namespace));
		$ ('#phanterpwa_datetimepicker_calendar_{0} .phanterpwa_datetimepicker_monthlist_month'.format (self.namespace)).on ('click', (function __lambda__ () {
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
			return _month (this);
		}));
	});},
	get show_years () {return __get__ (this, function (self, inicial_year) {
		if (typeof inicial_year == 'undefined' || (inicial_year != null && inicial_year.hasOwnProperty ("__kwargtrans__"))) {;
			var inicial_year = null;
		};
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'inicial_year': var inicial_year = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var container = DIV (__kwargtrans__ ({_class: 'phanterpwa_datetimepicker_yearlist_container'}));
		var _year = function (el) {
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
			var m = $ (el).attr ('phanterpwa_datetimepicker_year');
			self.set_year (m);
		};
		var row_container = DIV (__kwargtrans__ ({_class: 'phanterpwa_datetimepicker_row'}));
		var cyear = self.current_date.getFullYear ();
		if (inicial_year === null) {
			var inicial_year = cyear - 17;
		}
		var final_year = inicial_year + 35;
		for (var x = inicial_year; x < final_year; x++) {
			var add_class = '';
			if (cyear == x) {
				var add_class = ' selected';
			}
			row_container.append (DIV (x, __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_yearlist_year phanterpwa_datetimepicker_button{0}'.format (add_class), _phanterpwa_datetimepicker_year: x})));
		}
		container.append (row_container);
		container.html_to ('#phanterpwa_datetimepicker_month_and_calendar_{0}'.format (self.namespace));
		$ ('#phanterpwa_datetimepicker_month_and_calendar_{0} .phanterpwa_datetimepicker_yearlist_year'.format (self.namespace)).on ('click', (function __lambda__ () {
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
			return _year (this);
		}));
		$ ('#phanterpwa_datetimepicker_prev_year_{0}'.format (self.namespace)).html (DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-double-left'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button'})).xml ()).off ('click.phanterpwa_datetimepicker_prev_year').on ('click.phanterpwa_datetimepicker_prev_year', (function __lambda__ () {
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
			return self.show_years (inicial_year - 35);
		}));
		$ ('#phanterpwa_datetimepicker_next_year_{0}'.format (self.namespace)).html (DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-double-right'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button'})).xml ()).off ('click.phanterpwa_datetimepicker_next_year').on ('click.phanterpwa_datetimepicker_next_year', (function __lambda__ () {
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
			return self.show_years (inicial_year + 35);
		}));
	});},
	get show_hours () {return __get__ (this, function (self) {
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
		var container = DIV (__kwargtrans__ ({_class: 'phanterpwa_datetimepicker_hourlist_container'}));
		var _hour = function (el) {
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
			var m = $ (el).attr ('phanterpwa_datetimepicker_hour');
			self.set_hour (m);
		};
		var chour = self.current_date.getHours ();
		var row_container = DIV (__kwargtrans__ ({_class: 'phanterpwa_datetimepicker_row'}));
		for (var x = 0; x < 24; x++) {
			var add_class = '';
			if (chour == x) {
				var add_class = ' selected';
			}
			row_container.append (DIV (self._zfill (x, 2), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_hourlist_hour phanterpwa_datetimepicker_button{0}'.format (add_class), _phanterpwa_datetimepicker_hour: x})));
		}
		container.append (row_container);
		$ ('#phanterpwa_datetimepicker_calendar_month_years_{0}'.format (self.namespace)).html ('').append (container.xml ());
		$ ('#phanterpwa_datetimepicker_calendar_month_years_{0} .phanterpwa_datetimepicker_hourlist_hour'.format (self.namespace)).on ('click', (function __lambda__ () {
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
			return _hour (this);
		}));
	});},
	get show_minutes () {return __get__ (this, function (self) {
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
		var container = DIV (__kwargtrans__ ({_class: 'phanterpwa_datetimepicker_minutelist_container'}));
		var _minute = function (el) {
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
			var m = $ (el).attr ('phanterpwa_datetimepicker_minute');
			self.set_minute (m);
		};
		var cminute = self.current_date.getMinutes ();
		var row_container = DIV (__kwargtrans__ ({_class: 'phanterpwa_datetimepicker_row'}));
		for (var x = 0; x < 60; x++) {
			var add_class = '';
			if (cminute == x) {
				var add_class = ' selected';
			}
			row_container.append (DIV (self._zfill (x, 2), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_minutelist_minute phanterpwa_datetimepicker_button{0}'.format (add_class), _phanterpwa_datetimepicker_minute: x})));
		}
		container.append (row_container);
		container.html_to ('#phanterpwa_datetimepicker_calendar_month_years_{0}'.format (self.namespace));
		$ ('#phanterpwa_datetimepicker_calendar_month_years_{0} .phanterpwa_datetimepicker_minutelist_minute'.format (self.namespace)).on ('click', (function __lambda__ () {
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
			return _minute (this);
		}));
	});},
	get show_seconds () {return __get__ (this, function (self) {
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
		var container = DIV (__kwargtrans__ ({_class: 'phanterpwa_datetimepicker_secondlist_container'}));
		var _second = function (el) {
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
			var m = $ (el).attr ('phanterpwa_datetimepicker_second');
			self.set_second (m);
		};
		var csecond = self.current_date.getSeconds ();
		var row_container = DIV (__kwargtrans__ ({_class: 'phanterpwa_datetimepicker_row'}));
		for (var x = 0; x < 60; x++) {
			var add_class = '';
			if (csecond == x) {
				var add_class = ' selected';
			}
			row_container.append (DIV (self._zfill (x, 2), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_secondlist_second phanterpwa_datetimepicker_button{0}'.format (add_class), _phanterpwa_datetimepicker_second: x})));
		}
		container.append (row_container);
		container.html_to ('#phanterpwa_datetimepicker_calendar_month_years_{0}'.format (self.namespace));
		$ ('#phanterpwa_datetimepicker_calendar_month_years_{0} .phanterpwa_datetimepicker_secondlist_second'.format (self.namespace)).on ('click', (function __lambda__ () {
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
			return _second (this);
		}));
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
		$ (self.target_selector).find ('.phanterpwa-fixed-fulldisplay').removeClass ('enabled');
		var delete_datepicker = function () {
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
			if (!($ (self.target_selector).find ('.phanterpwa-fixed-fulldisplay').hasClass ('enabled'))) {
				$ (self.target_selector).find ('.phanterpwa-fixed-fulldisplay').remove ();
			}
		};
		setTimeout (delete_datepicker, 500);
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
		var cont = 0;
		var cmonth = self.current_date.getMonth ();
		var cday = self.current_date.getDate ();
		var cweek = self.current_date.getDay ();
		var cyear = self.current_date.getFullYear ();
		var chour = self.current_date.getHours ();
		var cminute = self.current_date.getMinutes ();
		var csecond = self.current_date.getSeconds ();
		var smonth = self.selected_date.getMonth ();
		var sday = self.selected_date.getDate ();
		var sweek = self.selected_date.getDay ();
		var syear = self.selected_date.getFullYear ();
		var shour = self.selected_date.getHours ();
		var sminute = self.selected_date.getMinutes ();
		var ssecond = self.selected_date.getSeconds ();
		var nmonth = self.now.getMonth ();
		var nday = self.now.getDate ();
		var nyear = self.now.getFullYear ();
		var AM_PM = 'PM';
		if (shour < 12) {
			var AM_PM = 'AM';
		}
		var container = DIV (__kwargtrans__ ({_id: 'phanterpwa_datetimepicker_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_wrapper'}));
		var container_calendar_month_years = DIV (DIV (DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-left'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_previusnext', _id: 'phanterpwa_datetimepicker_prev_year_{0}'.format (self.namespace)})), DIV (DIV (cyear, __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button', _id: 'phanterpwa_datetimepicker_year_{0}'.format (self.namespace)})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_year'})), DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-right'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_previusnext', _id: 'phanterpwa_datetimepicker_next_year_{0}'.format (self.namespace)})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_row'})), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_calendar_month_years_{0}'.format (self.namespace)}));
		var hour_container = DIV (DIV (HR (), DIV (DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-left'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button'})), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_prev_hour_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_previusnext'})), DIV (DIV (self._zfill (chour, 2), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button', _id: 'phanterpwa_datetimepicker_hour_{0}'.format (self.namespace)})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_hour'})), DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-right'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button'})), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_next_hour_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_previusnext'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_time_col'})), DIV (DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-left'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button'})), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_prev_minute_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_previusnext'})), DIV (DIV (self._zfill (cminute, 2), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button', _id: 'phanterpwa_datetimepicker_minute_{0}'.format (self.namespace)})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_minute'})), DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-right'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button'})), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_next_minute_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_previusnext'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_time_col'})), DIV (DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-left'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button'})), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_prev_second_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_previusnext'})), DIV (DIV (self._zfill (csecond, 2), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button', _id: 'phanterpwa_datetimepicker_second_{0}'.format (self.namespace)})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_second'})), DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-right'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button'})), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_next_second_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_previusnext'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_time_col'})), DIV (self.times [0], __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_time_col label'})), DIV (self.times [1], __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_time_col label'})), DIV (self.times [2], __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_time_col label'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_row'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_time_container'}));
		var calendar_and_month = DIV (DIV (DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-left'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button'})), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_prev_month_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_previusnext'})), DIV (DIV (I18N (self.months [cmonth]), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button', _id: 'phanterpwa_datetimepicker_month_{0}'.format (self.namespace)})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_month'})), DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-angle-right'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_button'})), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_next_month_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_previusnext'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_row'})), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_month_and_calendar_{0}'.format (self.namespace)}));
		var container_calendar = DIV (DIV (DIV (DIV (I18N (self.days [0].__getslice__ (0, 3, 1)), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_unit'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Sunday'})), DIV (DIV (I18N (self.days [1].__getslice__ (0, 3, 1)), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_unit'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Monday'})), DIV (DIV (I18N (self.days [2].__getslice__ (0, 3, 1)), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_unit'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Tuesday'})), DIV (DIV (I18N (self.days [3].__getslice__ (0, 3, 1)), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_unit'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Wednesday'})), DIV (DIV (I18N (self.days [4].__getslice__ (0, 3, 1)), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_unit'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Thursday'})), DIV (DIV (I18N (self.days [5].__getslice__ (0, 3, 1)), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_unit'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Friday'})), DIV (DIV (I18N (self.days [6].__getslice__ (0, 3, 1)), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_unit'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Saturday'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_row'})), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_calendar_{0}'.format (self.namespace)}));
		var row_days = DIV (__kwargtrans__ ({_class: 'phanterpwa_datetimepicker_row'}));
		for (var y = 0; y < cweek; y++) {
			row_days.append (DIV (__kwargtrans__ ({_class: 'phanterpwa_datetimepicker_day_empty phanterpwa_datetimepicker_{0}'.format (self.days [y])})));
		}
		var inicial_day = 1;
		for (var x = 0; x < 40; x++) {
			if (inicial_day < 32) {
				cont++;
				var new_date = '{0}-{1}-{2} {3}:{4}:{5}'.format (cyear, self._zfill (cmonth + 1, 2), self._zfill (inicial_day, 2), self._zfill (chour, 2), self._zfill (cminute, 2), self._zfill (csecond, 2));
				var d = new Date (new_date);
				if (d.getMonth () == cmonth && d.toJSON () !== null) {
					var add_class = '';
					if (d.getMonth () == nmonth && d.getFullYear () == nyear && d.getDate () == nday) {
						add_class += ' phanterpwa_datetimepicker_its_now';
					}
					if (self.selected_date !== null) {
						if (d.getMonth () == smonth && d.getFullYear () == syear && d.getDate () == sday) {
							add_class += ' phanterpwa_datetimepicker_selected';
						}
					}
					row_days.append (DIV (DIV (d.getDate (), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_unit_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_unit', _phanterpwa_datetimepicker_date: new_date})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_day phanterpwa_datetimepicker_{0}{1}'.format (self._days [d.getDay ()], add_class)})));
				}
			}
			inicial_day++;
		}
		container_calendar.append (row_days);
		calendar_and_month.append (container_calendar);
		container_calendar_month_years.append (calendar_and_month);
		container.append (container_calendar_month_years);
		container.append (hour_container);
		var summary = DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-times'})), __kwargtrans__ ({_class: 'phanterpwa-models-close'})), DIV (DIV (SPAN (self._zfill (sday, 2)), ', ', I18N (self.months [smonth]), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_summary_day_and_month_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_summary_day_and_month'})), DIV (I18N (self.days [sweek]), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_summary_week_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_summary_week'})), DIV (syear, __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_summary_year_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_summary_year'})), DIV ('{0}:{1}:{2} {3}'.format (self._zfill (shour, 2), self._zfill (sminute, 2), self._zfill (ssecond, 2), AM_PM), __kwargtrans__ ({_id: 'phanterpwa_datetimepicker_summary_hour_{0}'.format (self.namespace), _class: 'phanterpwa_datetimepicker_summary_hour'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_row'})), DIV (DIV (DIV (__kwargtrans__ ({_id: 'phanterpwa_datetimepicker_summary_current_data_{0}'.format (self.namespace)})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_row'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_summary_current_data'})), __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_summary_container'}));
		var c_dt = '';
		if (self.date_type == 'date') {
			var c_dt = ' phanterpwa_datetimepicker_is_not_datetime';
		}
		var datetimepicker_container = DIV (summary, container, __kwargtrans__ ({_class: 'phanterpwa_datetimepicker_container{0}'.format (c_dt)}));
		var centralizer = DIV (DIV (DIV (DIV (DIV (datetimepicker_container, __kwargtrans__ ({_id: 'phanterpwa-centralizer-center-{0}'.format (self.namespace), _class: 'phanterpwa-centralizer-center'})), __kwargtrans__ ({_class: 'phanterpwa-centralizer-horizontal'})), __kwargtrans__ ({_class: 'phanterpwa-centralizer-vertical'})), __kwargtrans__ ({_class: 'phanterpwa-centralizer-wrapper'})), __kwargtrans__ ({_class: 'phanterpwa-fixed-fulldisplay'}));
		var _selecting = function (el) {
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
			var v = $ (el).attr ('phanterpwa_datetimepicker_date');
			self.set_selected (v);
		};
		var open_panel = function (el) {
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
				return $ (self.target_selector).find ('.phanterpwa-fixed-fulldisplay').addClass ('enabled');
			}), 100);
		};
		if ($ (self.target_selector).has ('.phanterpwa-fixed-fulldisplay').length == 1) {
			datetimepicker_container.html_to ('#phanterpwa-centralizer-center-{0}'.format (self.namespace));
			$ (self.target_selector).find ('.phanterpwa-fixed-fulldisplay').addClass ('enabled');
		}
		else {
			centralizer.append_to (self.target_selector);
			open_panel ();
		}
		$ ('#phanterpwa_datetimepicker_prev_year_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_prev_year').on ('click.phanterpwa_datetimepicker_prev_year', (function __lambda__ () {
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
			return self.previus_year ();
		}));
		$ ('#phanterpwa_datetimepicker_next_year_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_next_year').on ('click.phanterpwa_datetimepicker_next_year', (function __lambda__ () {
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
			return self.next_year ();
		}));
		$ ('#phanterpwa_datetimepicker_prev_month_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_prev_month').on ('click.phanterpwa_datetimepicker_prev_month', (function __lambda__ () {
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
			return self.previus_month ();
		}));
		$ ('#phanterpwa_datetimepicker_next_month_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_next_month').on ('click.phanterpwa_datetimepicker_next_month', (function __lambda__ () {
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
			return self.next_month ();
		}));
		$ ('#phanterpwa_datetimepicker_prev_hour_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_prev_hour').on ('click.phanterpwa_datetimepicker_prev_hour', (function __lambda__ () {
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
			return self.previus_hour ();
		}));
		$ ('#phanterpwa_datetimepicker_next_hour_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_next_hour').on ('click.phanterpwa_datetimepicker_next_hour', (function __lambda__ () {
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
			return self.next_hour ();
		}));
		$ ('#phanterpwa_datetimepicker_prev_minute_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_prev_minute').on ('click.phanterpwa_datetimepicker_prev_minute', (function __lambda__ () {
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
			return self.previus_minute ();
		}));
		$ ('#phanterpwa_datetimepicker_next_minute_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_next_minute').on ('click.phanterpwa_datetimepicker_next_minute', (function __lambda__ () {
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
			return self.next_minute ();
		}));
		$ ('#phanterpwa_datetimepicker_prev_second_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_prev_second').on ('click.phanterpwa_datetimepicker_prev_second', (function __lambda__ () {
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
			return self.previus_second ();
		}));
		$ ('#phanterpwa_datetimepicker_next_second_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_next_second').on ('click.phanterpwa_datetimepicker_next_second', (function __lambda__ () {
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
			return self.next_second ();
		}));
		$ ('#phanterpwa_datetimepicker_month_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_month').on ('click.phanterpwa_datetimepicker_month', (function __lambda__ () {
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
			return self.show_months ();
		}));
		$ ('#phanterpwa_datetimepicker_year_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_year').on ('click.phanterpwa_datetimepicker_year', (function __lambda__ () {
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
			return self.show_years ();
		}));
		$ ('#phanterpwa_datetimepicker_hour_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_hour').on ('click.phanterpwa_datetimepicker_hour', (function __lambda__ () {
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
			return self.show_hours ();
		}));
		$ ('#phanterpwa_datetimepicker_minute_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_minute').on ('click.phanterpwa_datetimepicker_minute', (function __lambda__ () {
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
			return self.show_minutes ();
		}));
		$ ('#phanterpwa_datetimepicker_second_{0}'.format (self.namespace)).off ('click.phanterpwa_datetimepicker_second').on ('click.phanterpwa_datetimepicker_second', (function __lambda__ () {
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
			return self.show_seconds ();
		}));
		$ ('#phanterpwa_datetimepicker_calendar_{0} {1} .phanterpwa_datetimepicker_unit'.format (self.namespace, '.phanterpwa_datetimepicker_day')).off ('click.selecting_datepicker').on ('click.selecting_datepicker', (function __lambda__ () {
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
			return _selecting (this);
		}));
		$ ('.phanterpwa_datetimepicker_summary_container .phanterpwa-models-close').off ('click.deleting_datepicker').on ('click.deleting_datepicker', (function __lambda__ () {
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
			return self.close ();
		}));
	});}
});

//# sourceMappingURL=phanterpwa.frontend.components.datetimepicker.map