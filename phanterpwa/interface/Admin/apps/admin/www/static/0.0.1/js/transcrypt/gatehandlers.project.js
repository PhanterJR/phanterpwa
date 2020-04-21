// Transcrypt'ed from Python, 2020-04-10 03:52:37
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as left_bar from './phanterpwa.apptools.components.left_bar.js';
import * as widgets from './phanterpwa.apptools.components.widgets.js';
import * as forms from './phanterpwa.apptools.forms.js';
import * as helpers from './phanterpwa.apptools.helpers.js';
import * as gatehandler from './phanterpwa.apptools.gatehandler.js';
var __name__ = 'gatehandlers.project';
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
export var FORM = helpers.XmlConstructor.tagger ('form');
export var LABEL = helpers.XmlConstructor.tagger ('label');
export var HR = helpers.XmlConstructor.tagger ('hr', true);
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
		self.projects_data = localStorage.getItem ('admin_projects_data');
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
		var html = CONCATENATE (DIV (DIV (DIV (DIV ('PROJECT', __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), DIV (self.request.get_arg (0), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'p-container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (DIV (DIV (widgets.Preloaders ('preload_android'), __kwargtrans__ ({_style: 'width:100%; text-align: center; padding-top: 100px; padding-bottom: 100px;'})), __kwargtrans__ ({_id: 'applications_container'})), __kwargtrans__ ({_class: 'card p-row e-padding_10'})), __kwargtrans__ ({_class: 'phanterpwa-container p-container'})));
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
			return window.PhanterPWA.get_current_way ().startswith ('project');
		})]})));
		window.PhanterPWA.Components ['left_bar'].add_button (BackButton);
		if (self.request.get_arg (1) == 'view') {
			var ConfigProject = left_bar.LeftBarButton ('config_project', 'Configurar Projeto e Api', I (__kwargtrans__ ({_class: 'fas fa-tools'})), __kwargtrans__ (dict ({'_phanterpwa-way': 'project/{0}/config'.format (self.request.get_arg (0)), 'position': 'top', 'ways': [(function __lambda__ () {
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
				return window.PhanterPWA.get_current_way ().startswith ('project');
			})]})));
			window.PhanterPWA.Components ['left_bar'].add_button (ConfigProject);
			window.PhanterPWA.GET (__kwargtrans__ (dict ({'url_args': ['api', 'projects', self.request.get_arg (0)], 'onComplete': self._after_get_applications})));
		}
		else if (self.request.get_arg (1) == 'config') {
			window.PhanterPWA.GET (__kwargtrans__ (dict ({'url_args': ['api', 'config', self.request.get_arg (0)], 'onComplete': self._after_get_config})));
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
	get change_projects_folder () {return __get__ (this, function (self) {
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
		var admin_authorization = localStorage.getItem ('admin_authorization');
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
			return self._after_get_projects_folder (ev);
		});
		window.PhanterPWA.WS.send (dict ({'authorization': admin_authorization, 'command': 'change_project_folder'}));
	});},
	get _after_get_projects_folder () {return __get__ (this, function (self, evt) {
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
		var str_json = JSON.parse (evt.data);
		if (str_json.status == 200) {
			window.PhanterPWA.open_way ('developer');
		}
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
	get _xml_projects_list () {return __get__ (this, function (self, json) {
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
		var table = XTABLE ('applications-table', XTRH ('applications-table-head', ...['Application Name', 'Build Folder'], DIV (I (__kwargtrans__ ({_class: 'fas fa-plus'})), __kwargtrans__ (dict ({'_phanterpwa-way': 'application/new', '_class': 'icon_button wave_on_click'})))));
		var apps_dict = dict (json.config.APPS);
		for (var x of apps_dict.py_keys ()) {
			table.append (XTRD ('applications-table-data-{0}'.format (x), x, apps_dict [x] ['build_folder'], widgets.MenuBox ('drop_2_{0}'.format (x), __kwargtrans__ ({xml_menu: UL (LI ('Compile', __kwargtrans__ (dict ({'_id': 'btn_compile_app_project_{0}'.format (x), '_class': 'btn_compile_app_project', '_data-path': json.config ['PROJECT'] ['path'], '_data-app': x}))), LI ('View', __kwargtrans__ (dict ({'_class': 'botao_editar_role', '_phanterpwa-way': 'application/{0}/view'.format (x)}))), LI ('Delete', __kwargtrans__ (dict ({'_class': 'botao_editar_role', '_phanterpwa-way': 'application/{0}/delete'.format (x)}))), __kwargtrans__ (dict ({'data-menubox': 'drop_2_{0}'.format (x), '_class': 'dropdown-content'})))}))));
		}
		if (json.config.PROJECT.debug) {
			var url = json.config.API.remote_address_on_development;
		}
		else {
			var url = json.config.API.remote_address_on_production;
		}
		var ShowApi = left_bar.LeftBarButton ('view_api', 'Open Api', I (__kwargtrans__ ({_class: 'fas fa-globe'})), __kwargtrans__ (dict ({'position': 'top', 'ways': [(function __lambda__ () {
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
			return (json.running === true && window.PhanterPWA.get_current_way ().startswith ('project/{0}'.format (self.request.get_arg (0))) ? true : false);
		})], 'onStart': (function __lambda__ () {
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
			return self._bind_open_api (self.request.get_arg (0), url);
		})})));
		window.PhanterPWA.Components ['left_bar'].add_button (ShowApi);
		var html = DIV (XSECTION (LABEL ('Summary'), DIV (DIV (DIV (DIV (STRONG ('PROJECT PATH'), SPAN (json.config ['PROJECT'] ['path']), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ ({_class: 'p-row'})), DIV (DIV (DIV (STRONG ('IDENTIFIER NAME'), SPAN (json.config ['PROJECT'] ['name']), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ ({_class: 'p-row'})), DIV (DIV (DIV (STRONG ('TITLE'), SPAN (json.config ['PROJECT'] ['title']), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ ({_class: 'p-row'})), DIV (DIV (DIV (STRONG ('AUTHOR'), SPAN (json.config ['PROJECT'] ['author']), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ ({_class: 'p-row'})), DIV (DIV (DIV (STRONG ('VERSION'), SPAN (json.config ['PROJECT'] ['version']), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100 w3p50'})), DIV (DIV (STRONG ('COMPILATION'), SPAN (json.config ['PROJECT'] ['compilation']), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100 w3p50'})), __kwargtrans__ ({_class: 'p-row'})), DIV (DIV (DIV (STRONG ('DEBUG'), SPAN (json.config ['PROJECT'] ['debug']), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100 w3p50'})), DIV (DIV (STRONG ('STATUS'), SPAN ((json.running ? 'Running' : 'Stopped'), __kwargtrans__ ({_style: 'color: {0};'.format ((json.running ? 'green' : 'red'))})), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100 w3p50'})), __kwargtrans__ ({_class: 'p-row'})), __kwargtrans__ ({_class: 'e-padding_20'}))), table);
		html.html_to ('#applications_container');
	});},
	get _xml_config_project () {return __get__ (this, function (self, json) {
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
		var project_config = dict (json.project_config ['PROJECT']);
		var email_config = dict (json.project_config ['EMAIL']);
		var email_contents_config = dict (json.project_config ['CONTENT_EMAILS']);
		var api_config = dict (json.api_config ['API']);
		var project_default = ['title', 'version', 'author', 'debug', 'packaged'];
		var email_secret_default = ['password'];
		var email_default = ['server', 'username', 'default_sender', 'port', 'use_tls', 'use_ssl'];
		var content_email_default = ['copyright', 'link_to_your_site'];
		var html = FORM (H2 ('PROJECT'), HR (), __kwargtrans__ (dict ({'_phanterpwa-form': 'config_project'})));
		for (var x of project_config.py_keys ()) {
			if (x == 'debug' || x == 'packaged') {
				html.append (widgets.CheckBox ('project_{0}'.format (x), __kwargtrans__ (dict ({'value': project_config [x], 'name': x, 'label': x.py_replace ('_', ' ').capitalize (), 'form': 'config_project'}))));
			}
			else {
				html.append (widgets.Input ('project_{0}'.format (x), __kwargtrans__ (dict ({'value': project_config [x], 'name': x, 'label': x.py_replace ('_', ' ').capitalize (), 'form': 'config_project'}))));
			}
		}
		html.append (CONCATENATE (H2 ('EMAIL'), HR ()));
		for (var x of email_config.py_keys ()) {
			if (x == 'use_tls' || x == 'use_ssl') {
				html.append (widgets.CheckBox ('emai_{0}'.format (x), __kwargtrans__ (dict ({'value': email_config [x], 'name': x, 'label': x.py_replace ('_', ' ').capitalize (), 'form': 'config_project'}))));
			}
			else {
				html.append (widgets.Input ('emai_{0}'.format (x), __kwargtrans__ (dict ({'value': email_config [x], 'name': x, 'label': x.py_replace ('_', ' ').capitalize (), 'form': 'config_project'}))));
			}
		}
		html.append (CONCATENATE (H2 ('CONTENT EMAILS'), HR ()));
		for (var x of email_contents_config.py_keys ()) {
			html.append (widgets.Input ('content_emails_{0}'.format (x), __kwargtrans__ (dict ({'value': email_contents_config [x], 'name': x, 'label': x.py_replace ('_', ' ').capitalize (), 'form': 'config_project'}))));
		}
		html.append (CONCATENATE (H2 ('API'), HR ()));
		for (var x of api_config.py_keys ()) {
			if (x == 'secret_key' || x == 'url_secret_key') {
				html.append (widgets.Input ('api_{0}'.format (x), __kwargtrans__ (dict ({'value': api_config [x], 'name': x, 'label': x.py_replace ('_', ' ').capitalize (), 'form': 'config_project', 'icon': I (__kwargtrans__ ({_class: 'fab fa-sistrix'})), 'icon_on_click': (function __lambda__ () {
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
					return window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': I18N ('Fui Clicado!')})));
				})}))));
			}
			else {
				html.append (widgets.Input ('api_{0}'.format (x), __kwargtrans__ (dict ({'value': api_config [x], 'name': x, 'label': x.py_replace ('_', ' ').capitalize (), 'form': 'config_project'}))));
			}
		}
		html.append (forms.SubmitButton ('config_project', 'Save Config'));
		html.html_to ('#applications_container');
	});},
	get _after_get_applications () {return __get__ (this, function (self, data, ajax_status) {
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
				localStorage.setItem ('admin_projects_data', JSON.stringify (json));
				self.admin_projects_data = json;
				window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
				self._xml_projects_list (json);
			}
			else if (data.status == 202) {
				window.PhanterPWA.flash (__kwargtrans__ (dict ({'html': json.i18n.message})));
			}
			localStorage.setItem ('admin_authorization', json.authorization);
			self.admin_authorization = json.authorization;
			self._binds ();
		}
		else {
			window.PhanterPWA.flash ('Problem on server: {0}'.format (str (data.status)));
		}
	});},
	get _after_get_config () {return __get__ (this, function (self, data, ajax_status) {
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
				self._xml_config_project (json);
			}
		}
		else {
			window.PhanterPWA.flash ('Problem on server: {0}'.format (str (data.status)));
		}
	});}
});

//# sourceMappingURL=gatehandlers.project.map