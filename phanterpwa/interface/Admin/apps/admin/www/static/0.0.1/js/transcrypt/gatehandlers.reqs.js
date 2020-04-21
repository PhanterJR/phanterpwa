// Transcrypt'ed from Python, 2020-04-10 03:52:37
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as left_bar from './phanterpwa.apptools.components.left_bar.js';
import * as widgets from './phanterpwa.apptools.components.widgets.js';
import * as helpers from './phanterpwa.apptools.helpers.js';
import * as gatehandler from './phanterpwa.apptools.gatehandler.js';
var __name__ = 'gatehandlers.reqs';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var I = helpers.XmlConstructor.tagger ('i');
export var H1 = helpers.XmlConstructor.tagger ('h1');
export var H2 = helpers.XmlConstructor.tagger ('h2');
export var H3 = helpers.XmlConstructor.tagger ('h3');
export var STRONG = helpers.XmlConstructor.tagger ('strong');
export var SPAN = helpers.XmlConstructor.tagger ('span');
export var A = helpers.XmlConstructor.tagger ('a');
export var UL = helpers.XmlConstructor.tagger ('ul');
export var LI = helpers.XmlConstructor.tagger ('li');
export var LABEL = helpers.XmlConstructor.tagger ('label');
export var XSECTION = helpers.XSECTION;
export var I18N = helpers.I18N;
export var CONCATENATE = helpers.CONCATENATE;
export var XTABLE = widgets.Table;
export var XML = helpers.XML;
export var XTRD = widgets.TableData;
export var XTRH = widgets.TableHead;
export var XFOOTER = widgets.TableFooterPagination;
export var Index =  __class__ ('Index', [gatehandler.Handler], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, request) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'request': var request = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		gatehandler.Handler.__init__ (self, request);
		self.admin_authorization = localStorage.getItem ('admin_authorization');
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
		var html = CONCATENATE (DIV (DIV (DIV (DIV ('TEST REQUERIMENTS', __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'p-container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (DIV (DIV (widgets.Preloaders ('preload_android'), __kwargtrans__ ({_style: 'width:100%; text-align: center; padding-top: 100px; padding-bottom: 100px;'})), __kwargtrans__ ({_id: 'requeriments_container'})), __kwargtrans__ ({_class: 'card p-row e-padding_10'})), __kwargtrans__ ({_class: 'phanterpwa-container p-container'})));
		html.html_to ('#main-container');
		var BackButton = left_bar.LeftBarButton ('back_developer', 'Voltar', I (__kwargtrans__ ({_class: 'fas fa-arrow-circle-left'})), __kwargtrans__ (dict ({'_phanterpwa-way': 'developer', 'position': 'top', 'ways': [(function __lambda__ () {
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
			return window.PhanterPWA.get_current_way ().startswith ('check_requeriments');
		})]})));
		window.PhanterPWA.Components ['left_bar'].add_button (BackButton);
		window.PhanterPWA.GET (__kwargtrans__ (dict ({'url_args': ['api', 'automation', 'requeriment_list'], 'onComplete': self._after_get_requeriment_list})));
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
		$ ('#phanterpwa-component-left_bar-menu_button-change_projects_folder').off ('click.change_projects_folder').on ('click.change_projects_folder', self.change_projects_folder);
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
	get _bind_open_api () {return __get__ (this, function (self, app_name, url) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'app_name': var app_name = __allkwargs0__ [__attrib0__]; break;
						case 'url': var url = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		$ ('#phanterpwa-component-left_bar-menu_button-view_api').off ('click.open_href_play').on ('click.open_href_play', (function __lambda__ () {
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
			return window.open (url, '_blank');
		}));
	});},
	get _xml_requeriment_list () {return __get__ (this, function (self, json) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'json': var json = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var table = XTABLE ('requeriments-table', XTRH ('requeriments-table-head', ...['Requeriment', 'status']));
		for (var x of json.requeriment_list) {
			if (__in__ ('>', x) || __in__ ('<', x) || __in__ ('=', x)) {
				var x = x.py_split ('>') [0];
				var x = x.py_split ('=') [0];
				var x = x.py_split ('<') [0];
			}
			table.append (XTRD ('requeriments-table-data-{0}'.format (x), x.capitalize (), DIV (SPAN ('Cheking...', __kwargtrans__ ({_style: 'color: orange;'})), __kwargtrans__ (dict ({'_data-test': x, '_class': 'requeriments_phanterpwa_status'})))));
		}
		table.html_to ('#requeriments_container');
		window.PhanterPWA.WS.onMessage = (function __lambda__ (ev) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'ev': var ev = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self._onwsmessage (ev);
		});
		window.PhanterPWA.WS.send (dict ({'authorization': self.admin_authorization, 'command': 'requeriments_phanterpwa'}));
	});},
	get _onwsmessage () {return __get__ (this, function (self, ev) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'ev': var ev = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var json = JSON.parse (ev.data);
		if (json.command == 'requeriments_phanterpwa') {
			if (json.status == 206) {
				$ (".requeriments_phanterpwa_status[data-test='{0}']".format (json.check)).html ((json.result ? "<span style='color: green'>PASS</span>" : "<span style='color: red'>FAIL</span>"));
			}
			else if (json.status == 200) {
				window.PhanterPWA.flash ('Test finished!');
			}
		}
	});},
	get _after_get_requeriment_list () {return __get__ (this, function (self, data, ajax_status) {
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
		if (ajax_status == 'success') {
			var json = data.responseJSON;
			if (data.status == 200) {
				window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
				self._xml_requeriment_list (json);
			}
			self._binds ();
		}
		else {
			window.PhanterPWA.flash ('Problem on server: {0}'.format (str (data.status)));
		}
	});}
});

//# sourceMappingURL=gatehandlers.reqs.map