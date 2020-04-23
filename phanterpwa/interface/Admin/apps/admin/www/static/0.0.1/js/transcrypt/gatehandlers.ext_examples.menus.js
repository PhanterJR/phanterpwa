// Transcrypt'ed from Python, 2020-04-22 07:38:32
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as codemirror from './plugins.codemirror.js';
import * as helpers from './phanterpwa.apptools.helpers.js';
import * as widgets from './phanterpwa.apptools.components.widgets.js';
var __name__ = 'gatehandlers.ext_examples.menus';
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
export var codemirrorsidebyside = '\n# your code\n\nyour_menus = DIV(\n    DIV(\n        widgets.MenuBox(\n            "sideleft",\n            xml_menu=UL(\n                LI(SPAN("Editar", _class="botao_editar_socio")),\n                LI(SPAN("Visualizar", _class="botao_visualizar_socio")),\n                _class=\'dropdown-content\'\n            )\n        ),\n        _class="p-col w1p10"\n    ),\n    DIV(\n        " ",\n        _class="p-col w1p80"\n    ),\n    DIV(\n        widgets.MenuBox(\n            "sideright",\n            xml_menu=UL(\n                LI(SPAN("Editar", _class="botao_editar_socio")),\n                LI(SPAN("Visualizar", _class="botao_visualizar_socio")),\n                _class=\'dropdown-content\'\n            )\n        ),\n        _class="p-col w1p10"\n    ),\n    _class="p-row"\n)\n\n# your code\n';
export var MenuBox =  __class__ ('MenuBox', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, gatehandler) {
		self.gatehandler = gatehandler;
		var html = CONCATENATE (DIV (DIV (DIV (DIV ('COMPONENTES', __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), DIV ('MENUS', __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'p-container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (DIV (H2 (I18N ('MenuBox')), HR (), XSECTION (LABEL (I18N ('Example'), ' 01'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorsidebyside', __kwargtrans__ (dict ({'value': codemirrorsidebyside, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (DIV (DIV (widgets.MenuBox ('sideleft', __kwargtrans__ ({xml_menu: UL (LI (SPAN ('Editar', __kwargtrans__ ({_class: 'botao_editar_socio'}))), LI (SPAN ('Visualizar', __kwargtrans__ ({_class: 'botao_visualizar_socio'}))), __kwargtrans__ ({_class: 'dropdown-content'}))})), __kwargtrans__ ({_class: 'p-col w1p10'})), DIV (' ', __kwargtrans__ ({_class: 'p-col w1p80'})), DIV (widgets.MenuBox ('sideright', __kwargtrans__ ({xml_menu: UL (LI (SPAN ('Editar', __kwargtrans__ ({_class: 'botao_editar_socio'}))), LI (SPAN ('Visualizar', __kwargtrans__ ({_class: 'botao_visualizar_socio'}))), __kwargtrans__ ({_class: 'dropdown-content'}))})), __kwargtrans__ ({_class: 'p-col w1p10'})), __kwargtrans__ ({_class: 'p-row'})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), XSECTION (LABEL (I18N ('Example'), ' 01 (wear="android")'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorsidebyside', __kwargtrans__ (dict ({'value': codemirrorsidebyside, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (DIV (DIV (widgets.MenuBox ('sideleft', __kwargtrans__ ({xml_menu: UL (LI (SPAN ('Editar', __kwargtrans__ ({_class: 'botao_editar_socio'}))), LI (SPAN ('Visualizar', __kwargtrans__ ({_class: 'botao_visualizar_socio'}))), __kwargtrans__ ({_class: 'dropdown-content'}))})), __kwargtrans__ ({_class: 'p-col w1p10'})), DIV (' ', __kwargtrans__ ({_class: 'p-col w1p80'})), DIV (widgets.MenuBox ('sideright', __kwargtrans__ ({xml_menu: UL (LI (SPAN ('Editar', __kwargtrans__ ({_class: 'botao_editar_socio'}))), LI (SPAN ('Visualizar', __kwargtrans__ ({_class: 'botao_visualizar_socio'}))), __kwargtrans__ ({_class: 'dropdown-content'}))})), __kwargtrans__ ({_class: 'p-col w1p10'})), __kwargtrans__ ({_class: 'p-row'})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), __kwargtrans__ ({_class: 'card e-padding_20'})), __kwargtrans__ ({_class: 'new-container'})), __kwargtrans__ ({_class: 'phanterpwa-container p-container'})));
		html.html_to ('#main-container');
	});}
});

//# sourceMappingURL=gatehandlers.ext_examples.menus.map