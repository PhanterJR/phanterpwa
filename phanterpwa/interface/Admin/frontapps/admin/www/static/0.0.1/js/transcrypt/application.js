// Transcrypt'ed from Python, 2021-03-15 14:32:34
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as home from './gatehandlers.home.js';
import * as errors from './gatehandlers.errors.js';
import * as examples from './gatehandlers.examples.js';
import * as fontawesome from './gatehandlers.fontawesome.js';
import * as developer from './gatehandlers.developer.js';
import * as project from './gatehandlers.project.js';
import * as testsp from './gatehandlers.testsp.js';
import * as reqs from './gatehandlers.reqs.js';
import * as config from './auto.config.js';
import * as left_bar from './phanterpwa.frontend.components.left_bar.js';
import * as auth_user from './phanterpwa.frontend.components.auth_user.js';
import * as helpers from './phanterpwa.frontend.helpers.js';
import * as application from './phanterpwa.frontend.application.js';
var __name__ = '__main__';
export var gates = dict ({'home': home.Index, 'examples': examples.Index, 'fontawesome': fontawesome.Index, 'developer': developer.Index, 'project': project.Index, 'test_phanterpwa': testsp.Index, 'check_requeriments': reqs.Index, 'examples': examples.Index, 401: errors.Error_401, 403: errors.Error_403, 404: errors.Error_404});
export var MyApp = application.PhanterPWA (config.CONFIG, gates);
MyApp.add_component (left_bar.LeftBarMainButton ('#layout-main_button-container'));
MyApp.add_component (left_bar.LeftBar ('#layout-left_bar-container'));
MyApp.open_current_way ();

//# sourceMappingURL=application.map