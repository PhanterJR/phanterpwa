// Transcrypt'ed from Python, 2020-04-20 22:01:20
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as helpers from './phanterpwa.frontend.helpers.js';
var __name__ = 'phanterpwa.frontend.progressbar';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var ProgressBar =  __class__ ('ProgressBar', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, id_container) {
		self.element = $ (id_container);
		self.start ();
	});},
	get addEventProgressBar () {return __get__ (this, function (self, event_name) {
		var events = self.element.attr ('events');
		if (events === undefined) {
			self.element.attr ('events', JSON.stringify ([event_name]));
		}
		else {
			var events = set (JSON.parse (events));
			events.add (event_name);
			var events = list (events);
			self.element.attr ('events', JSON.stringify (events));
		}
	});},
	get removeEventProgressBar () {return __get__ (this, function (self, event_name) {
		var events = self.element.attr ('events');
		if (events !== undefined) {
			var events = set (JSON.parse (events));
			events.remove (event_name);
			var events = JSON.stringify (list (events));
			if (events != '[]') {
				self.element.attr ('events', events);
			}
			else {
				self.element.removeAttr ('events');
				self.element.find ('.phanterpwa-main_progressbar-wrapper').removeClass ('enabled');
			}
		}
	});},
	get forceStop () {return __get__ (this, function (self) {
		self.element.removeAttr ('events');
		self.element.find ('.phanterpwa-main_progressbar-wrapper').removeClass ('enabled');
	});},
	get check_progressbar () {return __get__ (this, function (self) {
		var events = self.element.attr ('events');
		if (events !== undefined) {
			self.element.find ('.phanterpwa-main_progressbar-wrapper').addClass ('enabled');
		}
		else {
			self.element.find ('.phanterpwa-main_progressbar-wrapper').removeClass ('enabled');
		}
	});},
	get start () {return __get__ (this, function (self) {
		self.element.html (self.xml ());
		window.setInterval (self.check_progressbar, 30);
	});},
	get xml () {return __get__ (this, function (self) {
		return DIV (DIV (DIV (__kwargtrans__ ({_class: 'phanterpwa-main_progressbar-movement'})), __kwargtrans__ ({_class: 'phanterpwa-main_progressbar'})), __kwargtrans__ ({_class: 'phanterpwa-main_progressbar-wrapper enabled'})).jquery ();
	});}
});

//# sourceMappingURL=phanterpwa.frontend.progressbar.map