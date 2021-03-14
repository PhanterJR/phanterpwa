// Transcrypt'ed from Python, 2021-03-10 09:46:18
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as snippets from './phanterpwa.frontend.components.snippets.js';
import * as left_bar from './phanterpwa.frontend.components.left_bar.js';
import * as helpers from './phanterpwa.frontend.helpers.js';
import * as gatehandler from './phanterpwa.frontend.gatehandler.js';
var __name__ = 'gatehandlers.home';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var I = helpers.XmlConstructor.tagger ('i');
export var H1 = helpers.XmlConstructor.tagger ('h1');
export var H2 = helpers.XmlConstructor.tagger ('h2');
export var H3 = helpers.XmlConstructor.tagger ('h3');
export var A = helpers.XmlConstructor.tagger ('a');
export var I18N = helpers.I18N;
export var Index =  __class__ ('Index', [gatehandler.Handler], {
	__module__: __name__,
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
		var html = DIV (snippets.Centralizer ('phanterpwa-logo-wrapper', DIV (__kwargtrans__ ({_class: 'phanterpwa-background-logo'})), H1 ('PhanterPWA', __kwargtrans__ ({_class: 'phanterpwa-the_title'})), H3 (I18N ('Full-Stack Progressive Web Applications framework written and programmable with Python.'), __kwargtrans__ ({_class: 'phanterpwa-the_subtitle'}))));
		html.html_to ('#main-container');
		window.PhanterPWA.LOAD (__kwargtrans__ (dict ({'args': ['loads', 'phanterpwa_logo.html'], 'onComplete': self._after_load})));
		var AdminButton = left_bar.LeftBarButton ('phanterpwa-developer-button', 'Development', I (__kwargtrans__ ({_class: 'fas fa-users-cog'})), __kwargtrans__ (dict ({'_phanterpwa-way': 'developer', 'position': 'top', 'ways': ['home']})));
		var teste = left_bar.LeftBarButton ('phanterpwa-components-button', 'Components', I (__kwargtrans__ ({_class: 'fas fa-code'})), __kwargtrans__ (dict ({'_phanterpwa-way': 'examples', 'position': 'top', 'ways': ['home']})));
		window.PhanterPWA.Components ['left_bar'].add_button (AdminButton);
		window.PhanterPWA.Components ['left_bar'].add_button (teste);
	});},
	get _after_load () {return __get__ (this, function (self, data) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'data': var data = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var xml = $ ('#phanterpwa-snippet-phanterpwa-logo-wrapper');
		xml.find ('.phanterpwa-background-logo').html (data);
		xml.height ($ (window).height () - 60).css ('width', '100%');
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
			return xml.height ($ (window).height () - 60).css ('width', '100%');
		}));
	});}
});

//# sourceMappingURL=gatehandlers.home.map