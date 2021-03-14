// Transcrypt'ed from Python, 2021-03-10 09:46:34
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as left_bar from './phanterpwa.frontend.components.left_bar.js';
import * as widgets from './phanterpwa.frontend.components.widgets.js';
import * as helpers from './phanterpwa.frontend.helpers.js';
import * as gatehandler from './phanterpwa.frontend.gatehandler.js';
var __name__ = 'gatehandlers.developer';
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
		var html = CONCATENATE (DIV (DIV (DIV (DIV ('DEVELOPMENT', __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'p-container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (DIV (DIV (widgets.Preloaders ('preload_android'), __kwargtrans__ ({_style: 'width:100%; text-align: center; padding-top: 100px; padding-bottom: 100px;'})), __kwargtrans__ ({_id: 'projects_container'})), __kwargtrans__ ({_class: 'card p-row e-padding_10'})), __kwargtrans__ ({_class: 'phanterpwa-container p-container'})));
		html.html_to ('#main-container');
		var BackButton = left_bar.LeftBarButton ('back_localizar_aluno', 'Voltar', I (__kwargtrans__ ({_class: 'fas fa-arrow-circle-left'})), __kwargtrans__ (dict ({'_phanterpwa-way': 'home', 'position': 'top', 'ways': ['developer']})));
		var TestButton = left_bar.LeftBarButton ('test_phanterpwa', 'Test PhanterPWA', I (__kwargtrans__ ({_class: 'fas fa-tasks'})), __kwargtrans__ (dict ({'_phanterpwa-way': 'test_phanterpwa', 'position': 'top', 'ways': ['developer']})));
		var CheckRequeriments = left_bar.LeftBarButton ('check_requeriments', 'Check Requeriments', I (__kwargtrans__ ({_class: 'fab fa-connectdevelop'})), __kwargtrans__ (dict ({'_phanterpwa-way': 'check_requeriments', 'position': 'top', 'ways': ['developer']})));
		var NewProjectsFolder = left_bar.LeftBarButton ('change_projects_folder', 'Change Project Folder', I (__kwargtrans__ ({_class: 'fas fa-folder-open'})), __kwargtrans__ (dict ({'position': 'top', 'ways': ['developer']})));
		window.PhanterPWA.Components ['left_bar'].add_button (BackButton);
		window.PhanterPWA.Components ['left_bar'].add_button (TestButton);
		window.PhanterPWA.Components ['left_bar'].add_button (CheckRequeriments);
		window.PhanterPWA.Components ['left_bar'].add_button (NewProjectsFolder);
		if (self.projects_data === null || self.projects_data === undefined) {
			window.PhanterPWA.GET (__kwargtrans__ (dict ({'url_args': ['api', 'projects'], 'onComplete': self._after_get_applications})));
		}
		else {
			self._xml_projects_list (self.projects_data);
		}
		self._binds ();
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
	get _bind_btn_run_stop () {return __get__ (this, function (self, el) {
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
		$ (el).find ('.btn_run_stop_project').off ('click.run_stop_project').on ('click.run_stop_project', (function __lambda__ () {
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
			return self._run_stop_project (this);
		}));
	});},
	get _run_stop_project () {return __get__ (this, function (self, el) {
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
		var el = $ (el);
		var project_path = el.attr ('data-path');
		var cmd = el.text ().lower ();
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
		window.PhanterPWA.WS.send (dict ({'authorization': admin_authorization, 'command': cmd, 'project_path': project_path}));
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
		console.log (str_json);
		if (str_json.command == 'change_project_folder') {
			if (str_json.status == 200) {
				window.PhanterPWA.open_way ('developer');
			}
		}
		else if (str_json.command == 'check_all') {
			if (str_json.status == 200) {
				$ ('.phanterpwa-widget-table-data').find ('span.project_status_content').text ('stopped').removeClass ('stopped');
				for (var r of str_json.project_running) {
					$ ('.phanterpwa-widget-table-data').find ("span.project_status_content['data-path'={0}]".format (r)).text ('running').addClass ('running');
				}
			}
		}
		else if (str_json.command == 'run' || str_json.command == 'stop') {
			if (str_json.status == 200) {
				window.PhanterPWA.GET (__kwargtrans__ (dict ({'url_args': ['api', 'projects'], 'onComplete': self._after_get_applications})));
			}
		}
	});},
	get _run_project () {return __get__ (this, function (self, project_path) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'project_path': var project_path = __allkwargs0__ [__attrib0__]; break;
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
		window.PhanterPWA.WS.send (dict ({'authorization': self.admin_authorization, 'command': 'run', 'project_path': project_path}));
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
		var table = XTABLE ('projects-table', XTRH ('projects-table-head', ...['Project Name', 'Diretory', 'Status', 'Port'], DIV (I (__kwargtrans__ ({_class: 'fas fa-plus'})), __kwargtrans__ (dict ({'_phanterpwa-way': 'project/novo', '_class': 'icon_button wave_on_click'})))));
		for (var x of json.projects_list) {
			var btn_lbl = 'run';
			if (x [2] == 'running') {
				var btn_lbl = 'stop';
			}
			table.append (XTRD ('projects-table-data-{0}'.format (x [0]), x [0], x [1], SPAN (x [2].capitalize (), __kwargtrans__ (dict ({'_class': 'project_status_content {0}'.format (x [2]), '_id': 'project_status_{0}'.format (x [0]), '_data-path': x [1]}))), x [3], widgets.MenuBox ('drop_project_{0}'.format (x [0]), DIV (I (__kwargtrans__ ({_class: 'fas fa-ellipsis-v'})), __kwargtrans__ ({_class: 'icon_button wave_on_click'})), __kwargtrans__ ({custom_menu: UL (LI (btn_lbl.capitalize (), __kwargtrans__ (dict ({'_id': 'btn_run_stop_project_{0}'.format (x [0]), '_class': 'btn_run_stop_project', '_data-path': x [1]}))), LI ('View', __kwargtrans__ (dict ({'_class': 'botao_editar_role', '_phanterpwa-way': 'project/{0}/view'.format (x [0])}))), LI ('Delete', __kwargtrans__ (dict ({'_class': 'botao_editar_role', '_phanterpwa-way': 'project/{0}/delete'.format (x [0])}))), __kwargtrans__ (dict ({'data-menubox': 'drop_project_{0}'.format (x [0]), '_class': 'dropdown-content'}))), onOpen: self._bind_btn_run_stop}))));
		}
		var html = DIV (XSECTION (LABEL ('Enviroment'), DIV (DIV (DIV (DIV (STRONG ('PYTHON EXECUTABLE'), SPAN (json.enviroment.python_executable), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ ({_class: 'p-row'})), DIV (DIV (DIV (STRONG ('PYTHON PATH'), SPAN (json.enviroment.python_path), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ ({_class: 'p-row'})), DIV (DIV (DIV (STRONG ('PYTHON VERSION'), SPAN (json.enviroment.python_version), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100 w3p50'})), DIV (DIV (STRONG ('PHANTERPWA VERSION'), SPAN (json.enviroment.phanterpwa_version), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100 w3p50'})), __kwargtrans__ ({_class: 'p-row'})), DIV (DIV (DIV (STRONG ('PROJECTS FOLDER'), SPAN (json.enviroment.projects_folder), __kwargtrans__ ({_class: 'e-tagger-wrapper'})), __kwargtrans__ ({_class: 'p-col w1p100'})), __kwargtrans__ ({_class: 'p-row'})), __kwargtrans__ ({_class: 'e-padding_20'}))), table);
		html.html_to ('#projects_container');
		self._binds ();
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
	});}
});

//# sourceMappingURL=gatehandlers.developer.map