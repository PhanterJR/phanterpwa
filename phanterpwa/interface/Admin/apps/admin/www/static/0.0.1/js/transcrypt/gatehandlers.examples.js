// Transcrypt'ed from Python, 2020-04-24 07:41:54
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as menus from './gatehandlers.ext_examples.menus.js';
import * as selects from './gatehandlers.ext_examples.selects.js';
import * as inputs from './gatehandlers.ext_examples.inputs.js';
import * as left_bar from './phanterpwa.apptools.components.left_bar.js';
import * as codemirror from './plugins.codemirror.js';
import * as helpers from './phanterpwa.apptools.helpers.js';
import * as widgets from './phanterpwa.apptools.components.widgets.js';
import * as gatehandler from './phanterpwa.apptools.gatehandler.js';
var __name__ = 'gatehandlers.examples';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var LABEL = helpers.XmlConstructor.tagger ('label');
export var I = helpers.XmlConstructor.tagger ('i');
export var H2 = helpers.XmlConstructor.tagger ('h2');
export var FORM = helpers.XmlConstructor.tagger ('form');
export var SPAN = helpers.XmlConstructor.tagger ('span');
export var IMG = helpers.XmlConstructor.tagger ('img', true);
export var HR = helpers.XmlConstructor.tagger ('hr', true);
export var UL = helpers.XmlConstructor.tagger ('ul');
export var STRONG = helpers.XmlConstructor.tagger ('strong');
export var LI = helpers.XmlConstructor.tagger ('li');
export var INPUT = helpers.XmlConstructor.tagger ('input', true);
export var BR = helpers.XmlConstructor.tagger ('br', true);
export var P = helpers.XmlConstructor.tagger ('p');
export var A = helpers.XmlConstructor.tagger ('a');
export var I18N = helpers.I18N;
export var CONCATENATE = helpers.CONCATENATE;
export var XML = helpers.XML;
export var XSECTION = helpers.XSECTION;
export var Index =  __class__ ('Index', [gatehandler.Handler], {
	__module__: __name__,
	get initialize () {return __get__ (this, function (self) {
		if (self.request.get_arg (0) == 'inputs') {
			self.inputs = inputs.Inputs (self);
		}
		else if (self.request.get_arg (0) == 'selects') {
			self.selects = selects.Selects (self);
		}
		else if (self.request.get_arg (0) == 'menus') {
			self.menus = menus.MenuBox (self);
		}
		else if (self.request.get_arg (0) == 'others') {
			self.others = Others (self);
		}
		else {
			var html = CONCATENATE (DIV (DIV (DIV (DIV ('COMPONENTES', __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'p-container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (DIV (DIV (DIV (I (__kwargtrans__ (dict ({'_class': 'fas fa-edit promo-icon'}))), H2 ('Inputs', __kwargtrans__ ({_class: 'promo-title'})), __kwargtrans__ (dict ({'_class': 'link', '_phanterpwa-way': 'examples/inputs'}))), __kwargtrans__ (dict ({'_class': 'promo-container'}))), __kwargtrans__ ({_class: 'p-col w1p100 w3p50 w4p25'})), DIV (DIV (DIV (I (__kwargtrans__ (dict ({'_class': 'far fa-caret-square-down promo-icon'}))), H2 ('Selects', __kwargtrans__ ({_class: 'promo-title'})), __kwargtrans__ (dict ({'_class': 'link', '_phanterpwa-way': 'examples/selects'}))), __kwargtrans__ (dict ({'_class': 'promo-container'}))), __kwargtrans__ ({_class: 'p-col w1p100 w3p50 w4p25'})), DIV (DIV (DIV (I (__kwargtrans__ (dict ({'_class': 'fas fa-ellipsis-v  promo-icon'}))), H2 ('Menus', __kwargtrans__ ({_class: 'promo-title'})), __kwargtrans__ (dict ({'_class': 'link', '_phanterpwa-way': 'examples/menus'}))), __kwargtrans__ (dict ({'_class': 'promo-container'}))), __kwargtrans__ ({_class: 'p-col w1p100 w3p50 w4p25'})), DIV (DIV (DIV (I (__kwargtrans__ (dict ({'_class': 'fas fa-file-signature  promo-icon'}))), H2 ('Others', __kwargtrans__ ({_class: 'promo-title'})), __kwargtrans__ (dict ({'_class': 'link', '_phanterpwa-way': 'examples/others'}))), __kwargtrans__ (dict ({'_class': 'promo-container'}))), __kwargtrans__ ({_class: 'p-col w1p100 w3p50 w4p25'})), DIV (DIV (DIV (I (__kwargtrans__ (dict ({'_class': 'fas fa-flag promo-icon'}))), H2 ('Font Awesome', __kwargtrans__ ({_class: 'promo-title'})), __kwargtrans__ (dict ({'_class': 'link', '_phanterpwa-way': 'fontawesome'}))), __kwargtrans__ (dict ({'_class': 'promo-container'}))), __kwargtrans__ ({_class: 'p-col w1p100 w3p50 w4p25'})), __kwargtrans__ ({_class: 'p-row card e-padding_20'})), __kwargtrans__ ({_class: 'phanterpwa-container p-container'})));
			html.html_to ('#main-container');
		}
		var BackButton1 = left_bar.LeftBarButton ('back_home', 'Voltar', I (__kwargtrans__ ({_class: 'fas fa-arrow-circle-left'})), __kwargtrans__ (dict ({'_phanterpwa-way': 'home', 'position': 'top', 'ways': [(function __lambda__ (r) {
			return (r == 'examples' ? true : false);
		})]})));
		var BackButton2 = left_bar.LeftBarButton ('back_examples', 'Voltar', I (__kwargtrans__ ({_class: 'fas fa-arrow-circle-left'})), __kwargtrans__ (dict ({'_phanterpwa-way': 'examples', 'position': 'top', 'ways': [(function __lambda__ (r) {
			return (r.startswith ('examples/') ? true : false);
		})]})));
		window.PhanterPWA.Components ['left_bar'].add_button (BackButton1);
		window.PhanterPWA.Components ['left_bar'].add_button (BackButton2);
	});}
});
export var Others =  __class__ ('Others', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, gatehandler) {
		self.gatehandler = gatehandler;
		var html = CONCATENATE (DIV (DIV (DIV (DIV ('COMPONENTES', __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), DIV ('TEXTAREA', __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'p-container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (DIV (H2 (I18N ('Textboxs')), HR (), XSECTION (LABEL ('Type: Password'), DIV (widgets.Textarea ('textare1', __kwargtrans__ ({label: 'Label Widget'})), __kwargtrans__ ({_class: 'component_materialize'}))), XSECTION (LABEL ('Type: Password'), DIV (widgets.Textarea ('textare2', __kwargtrans__ ({label: 'Label Widget', wear: 'shadows'})), __kwargtrans__ ({_class: 'component_shadows'}))), XSECTION (LABEL ('Type: Password'), DIV (widgets.Textarea ('textare3', __kwargtrans__ ({label: 'Label Widget', wear: 'elegant'})), __kwargtrans__ ({_class: 'component_shadows'}))), H2 (I18N ('Dropdown')), HR (), XSECTION (LABEL ('Value: True'), DIV (DIV (DIV (widgets.MenuBox ('drop1', __kwargtrans__ ({xml_menu: UL (LI (SPAN ('Editar', __kwargtrans__ ({_class: 'botao_editar_socio'}))), LI (SPAN ('Visualizar', __kwargtrans__ ({_class: 'botao_visualizar_socio'}))), __kwargtrans__ ({_class: 'dropdown-content'}))})), __kwargtrans__ ({_class: 'p-col w1p10'})), DIV (' ', __kwargtrans__ ({_class: 'p-col w1p80'})), DIV (widgets.MenuBox ('drop2', __kwargtrans__ ({xml_menu: UL (LI (SPAN ('Editar', __kwargtrans__ ({_class: 'botao_editar_socio'}))), LI (SPAN ('Visualizar', __kwargtrans__ ({_class: 'botao_visualizar_socio'}))), __kwargtrans__ ({_class: 'dropdown-content'}))})), __kwargtrans__ ({_class: 'p-col w1p10'})), __kwargtrans__ ({_class: 'p-row'})), __kwargtrans__ ({_class: 'component_materialize'}))), H2 (I18N ('Checkbox')), HR (), XSECTION (LABEL ('Value: True'), DIV (widgets.CheckBox ('check1', __kwargtrans__ ({value: true, label: 'Label Widget'})), __kwargtrans__ ({_class: 'component_materialize'}))), XSECTION (LABEL ('Value: False'), DIV (widgets.CheckBox ('check2', __kwargtrans__ ({value: false, label: 'Label Widget'})), __kwargtrans__ ({_class: 'component_materialize'}))), XSECTION (LABEL ('Value: False'), DIV (widgets.CheckBox ('check3', __kwargtrans__ ({value: false, label: 'Label Widget', wear: 'elegant'})), __kwargtrans__ ({_class: 'component_materialize'}))), H2 (I18N ('Radiobox')), HR (), XSECTION (LABEL ('Value: True'), DIV (widgets.RadioBox ('radio1', __kwargtrans__ ({value: true, label: 'Label Widget'})), __kwargtrans__ ({_class: 'component_materialize'}))), XSECTION (LABEL ('Value: False'), DIV (widgets.RadioBox ('radio2', __kwargtrans__ ({value: false, label: 'Label Widget'})), __kwargtrans__ ({_class: 'component_materialize'}))), XSECTION (LABEL ('Value: False'), DIV (widgets.RadioBox ('radio4', __kwargtrans__ ({value: false, label: 'Label Widget', py_name: 'my_radio'})), widgets.RadioBox ('radio5', __kwargtrans__ ({value: false, label: 'Label Widget', py_name: 'my_radio'})), widgets.RadioBox ('radio6', __kwargtrans__ ({value: false, label: 'Label Widget', py_name: 'my_radio'})), widgets.RadioBox ('radio7', __kwargtrans__ ({value: false, label: 'Label Widget', py_name: 'my_radio'})), __kwargtrans__ ({_class: 'component_materialize'}))), H2 (I18N ('ListString')), HR (), XSECTION (LABEL ('Value: ["Value01", "Value02", "Value03"]'), DIV (widgets.ListString ('liststring1', __kwargtrans__ ({value: ['Value01', 'Value02', 'Value03'], label: 'Label Widget'})), __kwargtrans__ ({_class: 'component_materialize'}))), XSECTION (LABEL ('data_set: ["Value04", "Value05"] and editable: False'), DIV (widgets.ListString ('liststring2', __kwargtrans__ ({value: ['Value01', 'Value02', 'Value03'], label: 'Label Widget', data_set: ['Value04', 'Value05'], editable: false})), __kwargtrans__ ({_class: 'component_materialize'}))), __kwargtrans__ ({_class: 'card e-padding_20'})), __kwargtrans__ ({_class: 'new-container'})), __kwargtrans__ ({_class: 'phanterpwa-container p-container'})));
		$ ('#main-container').html (html.jquery ());
	});}
});

//# sourceMappingURL=gatehandlers.examples.map