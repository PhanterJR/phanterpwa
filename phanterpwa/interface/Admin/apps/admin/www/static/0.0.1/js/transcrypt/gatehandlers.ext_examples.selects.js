// Transcrypt'ed from Python, 2020-04-28 03:38:44
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as codemirror from './plugins.codemirror.js';
import * as helpers from './phanterpwa.apptools.helpers.js';
import * as widgets from './phanterpwa.apptools.components.widgets.js';
var __name__ = 'gatehandlers.ext_examples.selects';
export var DIV = helpers.XmlConstructor.tagger ('div');
export var LABEL = helpers.XmlConstructor.tagger ('label');
export var I = helpers.XmlConstructor.tagger ('i');
export var H2 = helpers.XmlConstructor.tagger ('h2');
export var H3 = helpers.XmlConstructor.tagger ('h3');
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
export var codemirrorselectwearandroidnolabel = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectwearandroidnolabel",\n    placeholder="Placeholder Widget",\n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    }\n),\n\n# your code\n';
export var codemirrorselectwearshadowsnolabel = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectwearshadowsnolabel",\n    placeholder="Placeholder Widget",\n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    },\n    wear="shadows"\n),\n\n# your code\n';
export var codemirrorselectwearelegantnolabel = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectwearelegantnolabel",\n    placeholder="Placeholder Widget",\n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    },\n    wear="elegant"\n),\n\n# your code\n';
export var codemirrorselectwearandroid = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectwearandroid",\n    label="Label Widget",\n    placeholder="Placeholder Widget",\n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    }\n),\n\n# your code\n';
export var codemirrorselectwearshadows = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectwearshadows",\n    label="Label Widget",\n    placeholder="Placeholder Widget",\n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    },\n    wear="shadows"\n),\n\n# your code\n';
export var codemirrorselectwearelegant = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectwearelegant",\n    label="Label Widget",\n    placeholder="Placeholder Widget",\n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    },\n    wear="elegant"\n),\n\n# your code\n';
export var codemirrorselectwearandroidicon = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectwearandroidicon",\n    label="Label Widget",\n    placeholder="Placeholder Widget",\n    icon=I(_class="fab fa-telegram-plane"),\n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    }\n),\n\n# your code\n';
export var codemirrorselectwearshadowsicon = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectwearshadowsicon",\n    label="Label Widget",\n    placeholder="Placeholder Widget",\n    icon=I(_class="fab fa-telegram-plane"), \n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    },\n    wear="shadows"\n),\n\n# your code\n';
export var codemirrorselectweareleganticon = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectweareleganticon",\n    label="Label Widget",\n    placeholder="Placeholder Widget",\n    icon=I(_class="fab fa-telegram-plane"), \n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    },\n    wear="elegant"\n),\n\n# your code\n';
export var codemirrorselectwearandroidiconnolabel = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectwearandroidiconnolabel",\n    placeholder="Placeholder Widget",\n    icon=I(_class="fab fa-telegram-plane"),\n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    }\n),\n\n# your code\n';
export var codemirrorselectwearshadowsiconnolabel = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectwearshadowsiconnolabel",\n    placeholder="Placeholder Widget",\n    icon=I(_class="fab fa-telegram-plane"),\n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    },\n    wear="shadows"\n),\n\n# your code\n';
export var codemirrorselectweareleganticonnolabel = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectweareleganticonnolabel",\n    placeholder="Placeholder Widget",\n    icon=I(_class="fab fa-telegram-plane"),\n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    },\n    wear="elegant"\n),\n\n# your code\n';
export var codemirrorsimpleselect = '\n# your code\n\nyour_instance = widgets.Select(\n    "simpleselect",\n    label="Label Widget",\n    data_set={\n        "banana": "banana",\n        "abacate": "abacate",\n        "doce": "doce"\n    }\n)\n\n# your code\n';
export var codemirrorselectcanempty = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectcanempty",\n    label="Label Widget",\n    can_empty=True,\n    data_set={\n        "banana": "banana",\n        "abacate": "abacate",\n        "doce": "doce"\n    }\n)\n\n# your code\n';
var codemirrorselectcanempty = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectcanempty",\n    label="Label Widget",\n    can_empty=True,\n    data_set={\n        "banana": "banana",\n        "abacate": "abacate",\n        "doce": "doce"\n    }\n)\n\n# your code\n';
export var codemirrorselectcanemptyplaceholder = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectcanemptyplaceholder",\n    label="Label Widget",\n    placeholder="Placeholder Widget",\n    can_empty=True,\n    data_set={\n        "banana": "banana",\n        "abacate": "abacate",\n        "doce": "doce"\n    }\n)\n\n# your code\n';
export var codemirrorselectcanemptyeditableplaceholder = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectcanemptyeditableplaceholder",\n    label="Label Widget",\n    placeholder="Placeholder Widget",\n    editable=True,\n    can_empty=True,\n    data_set={\n        "banana": "banana",\n        "abacate": "abacate",\n        "doce": "doce"\n    }\n)\n\n# your code\n';
export var codemirrorselectcanemptyeditable = '\n# your code\n\nyour_instance = widgets.Select(\n    "selectcanemptyeditable",\n    label="Label Widget",\n    editable=True,\n    can_empty=True,\n    data_set={\n        "banana": "banana",\n        "abacate": "abacate",\n        "doce": "doce"\n    }\n)\n\n# your code\n';
export var multselect1_source = '\n# your code\n\nyour_instance = widgets.MultSelect(\n    "the_multiselect1",\n    label="Label Widget",\n    placeholder="Placeholder Widget",\n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    },\n)\n\n# your code\n\n';
export var multselect2_source = '\n# your code\n\nyour_instance = widgets.MultSelect(\n    "the_multiselect2",\n    label="Label Widget",\n    placeholder="Placeholder Widget",\n    editable=True,\n    data_set={\n        "banana": "Banana",\n        "abacate": "Abacate",\n        "doce": "Doce"\n    },\n)\n\n# your code\n\n';
export var cod_mult_sec_styles = '\nimport phanterpwa.apptools.components.widgets as widgets\nimport phanterpwa.apptools.helpers as helpers\n\nCONCATENATE = helpers.CONCATENATE\nDIV = helpers.XmlConstructor.tagger("div")\nH3 = helpers.XmlConstructor.tagger("h3")\n\nyour_instance = CONTATENATE(\n    H3("Style android"),\n    DIV(\n        widgets.MultSelect(\n            "the_multiselect1stylesnolabelnoplaceholder",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n        ),\n        widgets.MultSelect(\n            "the_multiselect1stylesnolabelnoplaceh",\n            placeholder="Placeholder Widget",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n        ),\n        widgets.MultSelect(\n            "the_multiselect1styles",\n            label="Label Widget",\n            placeholder="Placeholder Widget",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n        ),\n        widgets.MultSelect(\n            "the_multiselect1stylesnolabelicon",\n            placeholder="Placeholder Widget",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n            icon=I(_class="fab fa-telegram-plane")\n        ),\n        widgets.MultSelect(\n            "the_multiselect1stylesicon",\n            label="Label Widget",\n            placeholder="Placeholder Widget",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n            icon=I(_class="fab fa-telegram-plane")\n        ),\n        _class="widget_input_example"\n    ),\n    H3("Style shadows"),\n    DIV(\n        widgets.MultSelect(\n            "the_multiselect1stylesshadowsnolabelnoplaceholder",\n            wear="shadows",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n        ),\n        widgets.MultSelect(\n            "the_multiselect1stylesshadowsnolabelnoplaceh",\n            placeholder="Placeholder Widget",\n            wear="shadows",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n        ),\n        widgets.MultSelect(\n            "the_multiselect1stylesshadows",\n            label="Label Widget",\n            placeholder="Placeholder Widget",\n            wear="shadows",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n        ),\n        widgets.MultSelect(\n            "the_multiselect1stylesshadowsnolabelicon",\n            placeholder="Placeholder Widget",\n            wear="shadows",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n            icon=I(_class="fab fa-telegram-plane")\n        ),\n        widgets.MultSelect(\n            "the_multiselect1stylesshadowsicon",\n            label="Label Widget",\n            placeholder="Placeholder Widget",\n            wear="shadows",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n            icon=I(_class="fab fa-telegram-plane")\n        ),\n        _class="widget_input_example"\n    ),\n    H3("Style elegant"),\n    DIV(\n        widgets.MultSelect(\n            "the_multiselect1elegantnolabelnoplaceholder",\n            wear="elegant",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n        ),\n        widgets.MultSelect(\n            "the_multiselect1elegantnolabelnoplaceh",\n            placeholder="Placeholder Widget",\n            wear="elegant",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n        ),\n        widgets.MultSelect(\n            "the_multiselect1elegant",\n            label="Label Widget",\n            placeholder="Placeholder Widget",\n            wear="elegant",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n        ),\n        widgets.MultSelect(\n            "the_multiselect1elegantnolabelicon",\n            placeholder="Placeholder Widget",\n            wear="elegant",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n            icon=I(_class="fab fa-telegram-plane")\n        ),\n        widgets.MultSelect(\n            "the_multiselect1eleganticon",\n            label="Label Widget",\n            placeholder="Placeholder Widget",\n            wear="elegant",\n            data_set={\n                "banana": "Banana",\n                "abacate": "Abacate",\n                "doce": "Doce"\n            },\n            icon=I(_class="fab fa-telegram-plane")\n        ),\n        _class="widget_input_example"\n    ),\n)\n';
export var Selects =  __class__ ('Selects', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, gatehandler) {
		self.gatehandler = gatehandler;
		var html = CONCATENATE (DIV (DIV (DIV (DIV ('COMPONENTES', __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), DIV ('SELECT', __kwargtrans__ ({_class: 'phanterpwa-breadcrumb'})), __kwargtrans__ ({_class: 'phanterpwa-breadcrumb-wrapper'})), __kwargtrans__ ({_class: 'p-container'})), __kwargtrans__ ({_class: 'title_page_container card'})), DIV (DIV (DIV (H2 (I18N ('Select - Styles (Wear)')), HR (), XSECTION (LABEL (I18N ('Examples'), ' 01 (wear, label, icon)'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectwearandroidnolabel', __kwargtrans__ (dict ({'value': codemirrorselectwearandroidnolabel, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectwearandroidnolabel', __kwargtrans__ ({placeholder: 'Placeholder Widget', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), __kwargtrans__ ({_class: 'widget_input_example'})), BR (), H3 ('Label example'), STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectwearandroid', __kwargtrans__ (dict ({'value': codemirrorselectwearandroid, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectwearandroid', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), __kwargtrans__ ({_class: 'widget_input_example'})), BR (), H3 ('Icon examples'), STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectwearandroidiconnolabel', __kwargtrans__ (dict ({'value': codemirrorselectwearandroidiconnolabel, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectwearandroidiconnolabel', __kwargtrans__ ({placeholder: 'Placeholder Widget', icon: I (__kwargtrans__ ({_class: 'fab fa-telegram-plane'})), data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), __kwargtrans__ ({_class: 'widget_input_example'})), BR (), STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectwearandroidicon', __kwargtrans__ (dict ({'value': codemirrorselectwearandroidicon, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectwearandroidicon', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', icon: I (__kwargtrans__ ({_class: 'fab fa-telegram-plane'})), data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), XSECTION (LABEL (I18N ('Example'), ' 02 (wear="shadows")'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectwearshadowsnolabel', __kwargtrans__ (dict ({'value': codemirrorselectwearshadowsnolabel, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectwearshadowsnolabel', __kwargtrans__ ({placeholder: 'Placeholder Widget', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), wear: 'shadows'})), __kwargtrans__ ({_class: 'widget_input_example'})), BR (), H3 ('Label Example'), STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectwearshadows', __kwargtrans__ (dict ({'value': codemirrorselectwearshadows, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectwearshadows', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), wear: 'shadows'})), __kwargtrans__ ({_class: 'widget_input_example'})), BR (), STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectwearshadowsiconnolabel', __kwargtrans__ (dict ({'value': codemirrorselectwearshadowsiconnolabel, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectwearshadowsiconnolabel', __kwargtrans__ ({placeholder: 'Placeholder Widget', icon: I (__kwargtrans__ ({_class: 'fab fa-telegram-plane'})), data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), wear: 'shadows'})), __kwargtrans__ ({_class: 'widget_input_example'})), BR (), STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectwearshadowsicon', __kwargtrans__ (dict ({'value': codemirrorselectwearshadowsicon, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectwearshadowsicon', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', icon: I (__kwargtrans__ ({_class: 'fab fa-telegram-plane'})), data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), wear: 'shadows'})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), XSECTION (LABEL (I18N ('Example'), ' 03 (wear="elegant")'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectwearelegantnolabel', __kwargtrans__ (dict ({'value': codemirrorselectwearelegantnolabel, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectwearelegantnolabel', __kwargtrans__ ({placeholder: 'Placeholder Widget', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), wear: 'elegant'})), __kwargtrans__ ({_class: 'widget_input_example'})), BR (), STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectwearelegant', __kwargtrans__ (dict ({'value': codemirrorselectwearelegant, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectwearelegant', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), wear: 'elegant'})), __kwargtrans__ ({_class: 'widget_input_example'})), BR (), H3 ('Icon examples'), STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectweareleganticonnolabel', __kwargtrans__ (dict ({'value': codemirrorselectweareleganticonnolabel, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectweareleganticonnolabel', __kwargtrans__ ({placeholder: 'Placeholder Widget', icon: I (__kwargtrans__ ({_class: 'fab fa-telegram-plane'})), data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), wear: 'elegant'})), __kwargtrans__ ({_class: 'widget_input_example'})), H3 ('Icon example'), STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectweareleganticon', __kwargtrans__ (dict ({'value': codemirrorselectweareleganticon, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectweareleganticon', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', icon: I (__kwargtrans__ ({_class: 'fab fa-telegram-plane'})), data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), wear: 'elegant'})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), H2 (I18N ('Select - Parameters')), HR (), XSECTION (LABEL (I18N ('Example'), ' 01'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorsimpleselect', __kwargtrans__ (dict ({'value': codemirrorsimpleselect, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('simpleselect', __kwargtrans__ ({label: 'Label Widget', data_set: dict ({'banana': 'banana', 'abacate': 'abacate', 'doce': 'doce'})})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), XSECTION (LABEL (I18N ('Example'), ' 02 (can_empty="True")'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectcanempty', __kwargtrans__ (dict ({'value': codemirrorselectcanempty, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectcanempty', __kwargtrans__ ({label: 'Label Widget', can_empty: true, data_set: dict ({'banana': 'banana', 'abacate': 'abacate', 'doce': 'doce'})})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), XSECTION (LABEL (I18N ('Example'), ' 03 (can_empty=True, placeholder="Placeholder Widget")'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectcanemptyplaceholder', __kwargtrans__ (dict ({'value': codemirrorselectcanemptyplaceholder, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectcanemptyplaceholder', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', can_empty: true, data_set: dict ({'banana': 'banana', 'abacate': 'abacate', 'doce': 'doce'})})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), XSECTION (LABEL (I18N ('Example'), ' 04 (editable=True, can_empty=True)'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectcanemptyeditable', __kwargtrans__ (dict ({'value': codemirrorselectcanemptyeditable, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectcanemptyeditable', __kwargtrans__ ({label: 'Label Widget', editable: true, can_empty: true, data_set: dict ({'banana': 'banana', 'abacate': 'abacate', 'doce': 'doce'})})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), XSECTION (LABEL (I18N ('Example'), ' 05 (editable=True, can_empty=True, placeholder="Placeholder Widget")'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrorselectcanemptyeditableplaceholder', __kwargtrans__ (dict ({'value': codemirrorselectcanemptyeditableplaceholder, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.Select ('selectcanemptyeditableplaceholder', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', editable: true, can_empty: true, data_set: dict ({'banana': 'banana', 'abacate': 'abacate', 'doce': 'doce'})})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), H2 (I18N ('MultiSelect')), HR (), XSECTION (LABEL (I18N ('Example'), ' 01'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('cod_mult_sec_styles', __kwargtrans__ (dict ({'value': cod_mult_sec_styles, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), H3 ('Style android'), DIV (widgets.MultSelect ('the_multiselect1stylesnolabelnoplaceholder', __kwargtrans__ ({data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), widgets.MultSelect ('the_multiselect1stylesnolabelnoplaceh', __kwargtrans__ ({placeholder: 'Placeholder Widget', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), widgets.MultSelect ('the_multiselect1styles', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), widgets.MultSelect ('the_multiselect1stylesnolabelicon', __kwargtrans__ ({placeholder: 'Placeholder Widget', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), icon: I (__kwargtrans__ ({_class: 'fab fa-telegram-plane'}))})), widgets.MultSelect ('the_multiselect1stylesicon', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), icon: I (__kwargtrans__ ({_class: 'fab fa-telegram-plane'}))})), __kwargtrans__ ({_class: 'widget_input_example'})), H3 ('Style shadows'), DIV (widgets.MultSelect ('the_multiselect1stylesshadowsnolabelnoplaceholder', __kwargtrans__ ({wear: 'shadows', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), widgets.MultSelect ('the_multiselect1stylesshadowsnolabelnoplaceh', __kwargtrans__ ({wear: 'shadows', placeholder: 'Placeholder Widget', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), widgets.MultSelect ('the_multiselect1stylesshadows', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', wear: 'shadows', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), widgets.MultSelect ('the_multiselect1stylesshadowsnolabelicon', __kwargtrans__ ({placeholder: 'Placeholder Widget', wear: 'shadows', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), icon: I (__kwargtrans__ ({_class: 'fab fa-telegram-plane'}))})), widgets.MultSelect ('the_multiselect1stylesshadowsicon', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', wear: 'shadows', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), icon: I (__kwargtrans__ ({_class: 'fab fa-telegram-plane'}))})), __kwargtrans__ ({_class: 'widget_input_example'})), H3 ('Style elegant'), DIV (widgets.MultSelect ('the_multiselect1elegantnolabelnoplaceholder', __kwargtrans__ ({wear: 'elegant', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), widgets.MultSelect ('the_multiselect1elegantnolabelnoplaceh', __kwargtrans__ ({placeholder: 'Placeholder Widget', wear: 'elegant', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), widgets.MultSelect ('the_multiselect1elegant', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', wear: 'elegant', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), widgets.MultSelect ('the_multiselect1elegantnolabelicon', __kwargtrans__ ({placeholder: 'Placeholder Widget', wear: 'elegant', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), icon: I (__kwargtrans__ ({_class: 'fab fa-telegram-plane'}))})), widgets.MultSelect ('the_multiselect1eleganticon', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', wear: 'elegant', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'}), icon: I (__kwargtrans__ ({_class: 'fab fa-telegram-plane'}))})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), XSECTION (LABEL (I18N ('Example'), ' 02'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrormultselect1', __kwargtrans__ (dict ({'value': multselect1_source, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.MultSelect ('the_multiselect1', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), XSECTION (LABEL (I18N ('Example'), ' 03'), DIV (STRONG (I18N ('Code'), ':'), codemirror.CodeMirrorHelper ('codemirrormultselect2', __kwargtrans__ (dict ({'value': multselect2_source, 'mode': 'python', 'lineNumbers': true}))), STRONG (I18N ('Results'), ':'), DIV (widgets.MultSelect ('the_multiselect2', __kwargtrans__ ({label: 'Label Widget', placeholder: 'Placeholder Widget', editable: true, data_set: dict ({'banana': 'Banana', 'abacate': 'Abacate', 'doce': 'Doce'})})), __kwargtrans__ ({_class: 'widget_input_example'})), __kwargtrans__ ({_class: 'e-padding_10'}))), __kwargtrans__ ({_class: 'card e-padding_20'})), __kwargtrans__ ({_class: 'new-container'})), __kwargtrans__ ({_class: 'phanterpwa-container p-container'})));
		html.html_to ('#main-container');
	});}
});

//# sourceMappingURL=gatehandlers.ext_examples.selects.map