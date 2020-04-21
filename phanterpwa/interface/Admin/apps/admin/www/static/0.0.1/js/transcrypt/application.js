// Transcrypt'ed from Python, 2020-03-29 20:00:20
var config = {};
var gatekeeper = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as __module_gatekeeper__ from './gatekeeper.js';
__nest__ (gatekeeper, '', __module_gatekeeper__);
import * as __module_config__ from './config.js';
__nest__ (config, '', __module_config__);
import * as left_bar from './phanterpwa.apptools.components.left_bar.js';
import * as auth_user from './phanterpwa.apptools.components.auth_user.js';
import * as helpers from './phanterpwa.apptools.helpers.js';
import * as application from './phanterpwa.apptools.application.js';
var __name__ = '__main__';
export var I = helpers.XmlConstructor.tagger ('i');
export var I18N = helpers.I18N;
export var MyApp = application.PhanterPWA (config.CONFIG, gatekeeper.gates);
MyApp.add_component (left_bar.LeftBarMainButton ('#layout-main_button-container'));
MyApp.add_component (left_bar.LeftBar ('#layout-left_bar-container'));
MyApp.open_current_way ();

//# sourceMappingURL=application.map