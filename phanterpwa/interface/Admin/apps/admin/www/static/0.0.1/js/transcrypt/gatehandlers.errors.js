// Transcrypt'ed from Python, 2020-03-29 19:45:19
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as preloaders from './phanterpwa.apptools.preloaders.js';
import * as forms from './phanterpwa.apptools.forms.js';
import * as helpers from './phanterpwa.apptools.helpers.js';
import * as handler from './phanterpwa.apptools.handler.js';
var __name__ = 'gatehandlers.errors';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var FORM = helpers.XmlConstructor.tagger ('form');
export var SPAN = helpers.XmlConstructor.tagger ('span');
export var IMG = helpers.XmlConstructor.tagger ('img', true);
export var I = helpers.XmlConstructor.tagger ('I');
export var I18N = helpers.I18N;
export var CONCATENATE = helpers.CONCATENATE;
export var H3 = helpers.XmlConstructor.tagger ('h3');
export var html_base = CONCATENATE (DIV (DIV (DIV (DIV (I18N ('Ops!!!', __kwargtrans__ (dict ({'_pt-br': 'Ops!!!'}))), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'phanterpwa-container container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (DIV (DIV (DIV (IMG (__kwargtrans__ ({_class: 'image-warnings'})), __kwargtrans__ ({_class: 'image-warnings-container'})), DIV (__kwargtrans__ ({_id: 'content-warning'})), __kwargtrans__ ({_class: 'content-warnings'})), __kwargtrans__ ({_class: 'warnings-container phanterpwa-card-container card'})), __kwargtrans__ ({_class: 'new-container'})), __kwargtrans__ ({_class: 'phanterpwa-container container'})));
export var Error_404 =  __class__ ('Error_404', [handler.ErrorHandler], {
	__module__: __name__,
	get start () {return __get__ (this, function (self) {
		var html = html_base.jquery ();
		html.find ('.image-warnings').attr ('src', '/static/{0}/images/warning.png'.format (window.PhanterPWA.VERSION));
		html.find ('#content-warning').html ('ERROR 404');
		$ ('#main-container').html (html);
	});}
});
export var Error_401 =  __class__ ('Error_401', [handler.ErrorHandler], {
	__module__: __name__,
	get start () {return __get__ (this, function (self) {
		var html = CONCATENATE (DIV (DIV (DIV (DIV (I18N ('Authentication required', __kwargtrans__ (dict ({'_pt-br': 'Necessário Autenticar-se'}))), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'phanterpwa-container container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (DIV (DIV (DIV (IMG (__kwargtrans__ ({_class: 'image-warnings', _src: '/static/{0}/images/warning.png'.format (window.PhanterPWA.VERSION)}))), __kwargtrans__ ({_class: 'image-warnings-container'})), DIV (I18N ('You need authentication to access this feature.', __kwargtrans__ (dict ({'_pt-br': 'Você precisa autenticar-se para tentar acessar este recurso.'}))), __kwargtrans__ ({_id: 'content-warning', _class: 'content-warnings'})), DIV (DIV (I18N ('Login'), __kwargtrans__ ({_id: 'alternative_login_button', _class: 'btn wave_on_click link'})), __kwargtrans__ ({_class: 'button-container'})), __kwargtrans__ ({_class: 'warnings-container card phanterpwa-card-container'})), __kwargtrans__ ({_class: 'new-container'})), __kwargtrans__ ({_class: 'phanterpwa-container container'})));
		html.html_to ('#main-container');
		$ ('#alternative_login_button').off ('click.alternative_login_button').on ('click.alternative_login_button', (function __lambda__ () {
			return window.PhanterPWA.Components ['auth_user'].modal_login ();
		}));
	});}
});
export var Error_403 =  __class__ ('Error_403', [handler.ErrorHandler], {
	__module__: __name__,
	get start () {return __get__ (this, function (self) {
		var html = html_base.jquery ();
		html.find ('.image-warnings').attr ('src', '/static/{0}/images/warning.png'.format (window.PhanterPWA.VERSION));
		html.find ('#content-warning').html ('ERROR 403');
		$ ('#main-container').html (html);
	});}
});

//# sourceMappingURL=gatehandlers.errors.map