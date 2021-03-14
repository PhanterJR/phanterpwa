// Transcrypt'ed from Python, 2021-03-10 09:46:29
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'phanterpwa.frontend.fmasks';
export var Mask =  __class__ ('Mask', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, target_selector, mask_function, reverse, apply_on_init) {
		if (typeof reverse == 'undefined' || (reverse != null && reverse.hasOwnProperty ("__kwargtrans__"))) {;
			var reverse = false;
		};
		if (typeof apply_on_init == 'undefined' || (apply_on_init != null && apply_on_init.hasOwnProperty ("__kwargtrans__"))) {;
			var apply_on_init = false;
		};
		self.target_selector = target_selector;
		self.element_target = $ (target_selector);
		self.mask_function = mask_function;
		self.reverse = reverse;
		self.apply_on_init = apply_on_init;
		self.start ();
	});},
	get stringFilter () {return function (value, you_want_array) {
		if (typeof you_want_array == 'undefined' || (you_want_array != null && you_want_array.hasOwnProperty ("__kwargtrans__"))) {;
			var you_want_array = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
		};
		var value = str (value);
		var new_value = '';
		for (var x of value) {
			if (__in__ (x, you_want_array)) {
				new_value += x;
			}
		}
		return new_value;
	};},
	get onKeyPress () {return __get__ (this, function (self, event, el) {
		var code = event.keyCode || event.which;
		var element = $ (el);
		var pos = element [0].selectionStart;
		var end = element [0].selectionEnd;
		if (pos == end) {
			var current_value = element.val ();
			var v = String.fromCharCode (code);
			var text0 = current_value.__getslice__ (0, pos, 1) + v;
			var text1 = current_value.__getslice__ (pos, null, 1);
			var numbers = (function () {
				var __accu0__ = [];
				for (var x = 0; x < 10; x++) {
					__accu0__.append (str (x));
				}
				return __accu0__;
			}) ();
			if (__in__ (v, numbers)) {
				print (current_value [pos]);
				if (__in__ (current_value [pos], numbers) || current_value [pos] == '_') {
					var pos = pos + 1;
				}
				else {
					var pos = pos + 2;
				}
			}
		}
		else {
			var current_value = element.val ();
			var v = String.fromCharCode (code);
			var text0 = current_value.__getslice__ (0, pos, 1) + v;
			var text1 = current_value.__getslice__ (end, null, 1);
			var numbers = (function () {
				var __accu0__ = [];
				for (var x = 0; x < 10; x++) {
					__accu0__.append (str (x));
				}
				return __accu0__;
			}) ();
			if (__in__ (v, numbers)) {
				var pos = pos + 1;
			}
		}
		var new_value = '{0}{1}'.format (text0, text1);
		var pure_value = self.stringFilter (new_value);
		var new_value = self.mask_function (pure_value) [0];
		if (pure_value !== '') {
			element.val (new_value);
		}
		else {
			element.val ('');
		}
		if (pos > self.mask_function (pure_value) [1]) {
			element [0].selectionStart = self.mask_function (pure_value) [1];
			element [0].selectionEnd = self.mask_function (pure_value) [1];
		}
		else {
			element [0].selectionStart = pos;
			element [0].selectionEnd = pos;
		}
		event.preventDefault ();
	});},
	get onNonPrintingKeysIn () {return __get__ (this, function (self, event, el) {
		var noprintkeys = [8, 46];
		var code = event.keyCode || event.which;
		var element = $ (el);
		if (__in__ (code, noprintkeys)) {
			if (code == 8) {
				var current_value = element.val ();
				if (self.stringFilter (current_value) !== '') {
					var pos = element [0].selectionStart;
					var end = element [0].selectionEnd;
					var text0 = current_value.__getslice__ (0, pos - 1, 1);
					var numbers = (function () {
						var __accu0__ = [];
						for (var x = 0; x < 10; x++) {
							__accu0__.append (str (x));
						}
						return __accu0__;
					}) ();
					if (pos == end) {
						if (__in__ (current_value [pos - 1], numbers)) {
							var text0 = current_value.__getslice__ (0, pos - 1, 1);
						}
						else if (current_value [pos - 1] !== '') {
							var text0 = current_value.__getslice__ (0, pos - 2, 1);
							var pos = pos - 1;
						}
						var text1 = current_value.__getslice__ (pos, null, 1);
						var new_value = '{0}{1}'.format (text0, text1);
						element [0].selectionStart = pos - 1;
						element [0].selectionEnd = pos - 1;
					}
					else {
						var text0 = current_value.__getslice__ (0, pos, 1);
						var text1 = current_value.__getslice__ (end, null, 1);
						var new_value = '{0}{1}'.format (text0, text1);
						element [0].selectionStart = pos;
						element [0].selectionEnd = pos;
					}
					var pure_value = self.stringFilter (new_value);
					var new_value = self.mask_function (pure_value) [0];
					if (pure_value !== '') {
						element.val (new_value);
					}
					else {
						element.val ('');
					}
					element [0].selectionStart = pos - 1;
					element [0].selectionEnd = pos - 1;
				}
				else {
					element.val ('');
				}
			}
			else if (code == 46) {
				var current_value = element.val ();
				if (self.stringFilter (current_value) !== '') {
					var pos = element [0].selectionStart;
					var end = element [0].selectionEnd;
					if (pos == end) {
						var text0 = current_value.__getslice__ (0, pos, 1);
						var numbers = (function () {
							var __accu0__ = [];
							for (var x = 0; x < 10; x++) {
								__accu0__.append (str (x));
							}
							return __accu0__;
						}) ();
						if (__in__ (current_value [pos], numbers)) {
							var text1 = current_value.__getslice__ (pos + 1, null, 1);
						}
						else if (current_value [pos] !== '') {
							var text1 = current_value.__getslice__ (pos + 2, null, 1);
						}
						var new_value = '{0}{1}'.format (text0, text1);
						element [0].selectionStart = pos;
						element [0].selectionEnd = pos;
					}
					else {
						var text0 = current_value.__getslice__ (0, pos, 1);
						var text1 = current_value.__getslice__ (end, null, 1);
						var new_value = '{0}{1}'.format (text0, text1);
						element [0].selectionStart = pos;
						element [0].selectionEnd = pos;
					}
					var pure_value = self.stringFilter (new_value);
					var new_value = self.mask_function (pure_value) [0];
					if (pure_value !== '') {
						element.val (new_value);
					}
					else {
						element.val ('');
					}
					element [0].selectionStart = pos;
					element [0].selectionEnd = pos;
				}
				else {
					element.val ('');
				}
			}
			event.preventDefault ();
		}
	});},
	get onNonPrintingKeys () {return __get__ (this, function (self, event, el) {
		event.preventDefault ();
		var element = $ (el);
		var code = event.keyCode || event.which;
		var noprintkeys = [8, 46, 9];
		if (__in__ (code, noprintkeys)) {
			var value = element.val ();
			element.val (value + '_');
			if (self.reverse) {
				if (self.stringFilter (value) != '') {
					var value = str (int (self.stringFilter (value)));
				}
			}
			var new_value = '';
			var pure_value = self.stringFilter (value);
			if (pure_value == '') {
				element.val ('');
			}
			else {
				var new_value = self.mask_function (pure_value) [0];
				element.attr ('phanterpwa-mask-justnumbers', self.stringFilter (new_value));
				var selection_pos = self.mask_function (pure_value) [1];
				element.val (new_value);
				if (self.reverse) {
					element [0].selectionStart = -(len (new_value));
					element [0].selectionEnd = -(len (new_value));
				}
				else {
					element [0].selectionStart = selection_pos;
					element [0].selectionEnd = selection_pos;
				}
				if (code != 9) {
					event.preventDefault ();
				}
			}
		}
		else {
			var pure_value = self.stringFilter (element.val ());
			if (pure_value == '') {
				element.val ('');
			}
		}
	});},
	get start () {return __get__ (this, function (self) {
		var element = $ (self.target_selector);
		var value = element.val ();
		var pure_value = self.stringFilter (value);
		var new_value = self.mask_function (pure_value) [0];
		var selection_pos = self.mask_function (pure_value) [1];
		if (self.apply_on_init) {
			element.val (new_value);
			if (reverse) {
				element [0].selectionStart = -(len (new_value));
				element [0].selectionEnd = -(len (new_value));
			}
			else {
				element [0].selectionStart = selection_pos;
				element [0].selectionEnd = selection_pos;
			}
		}
		element.off ('keypress.phanterpwaMask, focusout.phanterpwaMask').on ('keypress.phanterpwaMask, focusout.phanterpwaMask', (function __lambda__ (event) {
			return self.onKeyPress (event, this);
		}));
		element.off ('keydown.phanterpwaMask, focusout.phanterpwaMask').on ('keydown.phanterpwaMask, focusout.phanterpwaMask', (function __lambda__ (event) {
			return self.onNonPrintingKeysIn (event, this);
		}));
	});}
});
export var date_and_datetime_to_maks = function (value) {
	var date_format = ['d', 'M', 'o', 't', 'y', 'H', 'm', 's'];
	var string_mask = '';
	if (isinstance (value, str)) {
		for (var x of value) {
			if (__in__ (x, date_format)) {
				var y = '#';
			}
			else {
				var y = x;
			}
			string_mask += y;
		}
	}
	return string_mask;
};
export var isNotEmpty = function (value) {
	if (value !== null && value !== '' && value !== undefined) {
		return true;
	}
	else {
		return false;
	}
};
export var stringFilter = function (value, you_want_array) {
	if (typeof you_want_array == 'undefined' || (you_want_array != null && you_want_array.hasOwnProperty ("__kwargtrans__"))) {;
		var you_want_array = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
	};
	var value = str (value);
	var new_value = '';
	for (var x of value) {
		if (__in__ (x, you_want_array)) {
			new_value += x;
		}
	}
	return new_value;
};
export var hasCaracter = function (value, caracter) {
	if (typeof caracter == 'undefined' || (caracter != null && caracter.hasOwnProperty ("__kwargtrans__"))) {;
		var caracter = '.';
	};
	var value = str (value);
	var has_caractere = false;
	if (__in__ (caracter, value)) {
		var has_caractere = true;
	}
	return has_caractere;
};
export var justSearchedCaracter = function (value, caractere) {
	if (typeof caractere == 'undefined' || (caractere != null && caractere.hasOwnProperty ("__kwargtrans__"))) {;
		var caractere = '.';
	};
	var has_caractere = false;
	var value = str (value);
	var new_value = '';
	for (var x of value) {
		if (x == caractere) {
			if (!(has_caractere)) {
				new_value += x;
				var has_caractere = true;
			}
		}
		else {
			new_value += x;
		}
	}
	return new_value;
};
export var stringForceToFloatstring = function (value, force_dot, localeBR) {
	if (typeof force_dot == 'undefined' || (force_dot != null && force_dot.hasOwnProperty ("__kwargtrans__"))) {;
		var force_dot = false;
	};
	if (typeof localeBR == 'undefined' || (localeBR != null && localeBR.hasOwnProperty ("__kwargtrans__"))) {;
		var localeBR = true;
	};
	if (isNotEmpty (value)) {
		var value = str (value);
		if (localeBR) {
			var value = value.py_replace (',', '.');
		}
		var value = stringFilter (value, ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']);
		var value = justSearchedCaracter (value);
		if (value != '') {
			if (value == '.') {
				if (force_dot) {
					var value = '0.';
				}
				else {
					var value = '';
				}
			}
			else if (!(force_dot)) {
				var value = str (float (value));
			}
		}
		return value;
	}
	else {
		return '';
	}
};
export var stringToFloatstringLimitDecimals = function (value, casas_decimais, localeBR) {
	if (typeof casas_decimais == 'undefined' || (casas_decimais != null && casas_decimais.hasOwnProperty ("__kwargtrans__"))) {;
		var casas_decimais = 2;
	};
	if (typeof localeBR == 'undefined' || (localeBR != null && localeBR.hasOwnProperty ("__kwargtrans__"))) {;
		var localeBR = true;
	};
	var value = str (value);
	if (isNotEmpty (value)) {
		if (localeBR) {
			var value = value.py_replace (',', '.');
		}
		var value = stringFilter (value, ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']);
		var value = justSearchedCaracter (value);
		if (value != '') {
			var value = str (float (value));
			var p_inteiro = value.py_split ('.') [0];
			var p_decimal = value.py_split ('.') [1];
			if (!(isNotEmpty (p_decimal))) {
				var p_decimal = '0';
			}
			if (len (p_decimal) < casas_decimais) {
				var np_decimal = '';
				for (var x = 0; x < casas_decimais - len (p_decimal); x++) {
					np_decimal += '0';
				}
				var p_decimal = p_decimal + np_decimal;
			}
			else {
				var np_decimal = '';
				for (var i = 0; i < casas_decimais; i++) {
					np_decimal += p_decimal [i];
				}
				var p_decimal = np_decimal;
			}
			var r = '{0}.{1}'.format (p_inteiro, p_decimal);
			return r;
		}
		return value;
	}
	else {
		return '';
	}
};
export var floatToCurrency = function (value, casas_decimais, separador_decimal, separador_milhar, currency) {
	if (typeof casas_decimais == 'undefined' || (casas_decimais != null && casas_decimais.hasOwnProperty ("__kwargtrans__"))) {;
		var casas_decimais = 2;
	};
	if (typeof separador_decimal == 'undefined' || (separador_decimal != null && separador_decimal.hasOwnProperty ("__kwargtrans__"))) {;
		var separador_decimal = ',';
	};
	if (typeof separador_milhar == 'undefined' || (separador_milhar != null && separador_milhar.hasOwnProperty ("__kwargtrans__"))) {;
		var separador_milhar = '.';
	};
	if (typeof currency == 'undefined' || (currency != null && currency.hasOwnProperty ("__kwargtrans__"))) {;
		var currency = '';
	};
	var casas_decimais = casas_decimais;
	var separador_decimal = separador_decimal;
	var separador_milhar = separador_milhar;
	var value = str (value);
	var p_m_inteiro = '0';
	var p_m_decimal = '';
	for (var i = 0; i < casas_decimais; i++) {
		p_m_decimal += '0';
	}
	if (hasCaracter (value, '.')) {
		var p_inteiro = value.py_split ('.') [0];
		var p_decimal = value.py_split ('.') [1];
		if (isNotEmpty (p_inteiro)) {
			var p_inteiro = p_inteiro.py_split ('').reverse ().join ('');
			var str_inteiro = '';
			var tamanho_inteiro = len (p_inteiro);
			var adicionar_separador = false;
			if (tamanho_inteiro > 3) {
				for (var i = 0; i < tamanho_inteiro; i++) {
					if (__mod__ (i + 1, 3) == 0) {
						str_inteiro += p_inteiro [i];
						var adicionar_separador = true;
					}
					else if (adicionar_separador) {
						var adicionar_separador = false;
						str_inteiro += separador_milhar + p_inteiro [i];
					}
					else {
						str_inteiro += p_inteiro [i];
					}
				}
			}
			else {
				for (var i = 0; i < tamanho_inteiro; i++) {
					str_inteiro += p_inteiro [i];
				}
			}
			var p_m_inteiro = str_inteiro.py_split ('').reverse ().join ('');
		}
		if (isNotEmpty (p_decimal)) {
			var str_cd = '';
			if (p_decimal.length > casas_decimais) {
				for (var i = 0; i < casas_decimais; i++) {
					str_cd += p_decimal [i];
				}
			}
			else {
				for (var i = 0; i < len (p_decimal); i++) {
					str_cd += p_decimal [i];
				}
				var diferenca = casas_decimais - len (p_decimal);
				var tracos = '';
				for (var i = 0; i < diferenca; i++) {
					tracos += '0';
				}
				str_cd += tracos;
			}
			var p_m_decimal = str_cd;
		}
	}
	else if (value != '') {
		var t_m_inteiro = int (value);
		if (isNotEmpty (t_m_inteiro)) {
			var p_m_inteiro = str (t_m_inteiro);
		}
	}
	if (isNotEmpty (currency)) {
		var r = '{0} {1}{2}{3}'.format (currency, p_m_inteiro, separador_decimal, p_m_decimal);
	}
	else {
		var r = '{1}{2}{3}'.format (p_m_inteiro, separador_decimal, p_m_decimal);
	}
	return r;
};
export var baseCustom = function (value, custom_mask, cursorPosition) {
	if (typeof cursorPosition == 'undefined' || (cursorPosition != null && cursorPosition.hasOwnProperty ("__kwargtrans__"))) {;
		var cursorPosition = 0;
	};
	var value = str (value);
	var size = len (value);
	var char_plus = 0;
	var pos_num = 0;
	var new_value = '';
	for (var i = 0; i < len (custom_mask); i++) {
		if (custom_mask [i] == '#') {
			if (pos_num < size) {
				new_value += value [pos_num];
				pos_num++;
			}
			else {
				new_value += '_';
				pos_num++;
			}
		}
		else {
			if (i < size + char_plus) {
				char_plus++;
			}
			new_value += custom_mask [i];
		}
	}
	var cursorPosition = int (size) + char_plus;
	return [new_value, cursorPosition];
};
export var maskFone = function (valor) {
	var valor = str (valor);
	var size = len (valor);
	if (size == 10) {
		var custom_mask = '(##) ####-####';
	}
	else if (size == 11) {
		var custom_mask = '(##) # ####-####';
	}
	else if (size > 11) {
		var custom_mask = '(##) #####-#########';
	}
	else {
		var custom_mask = '(##) # ####-####';
	}
	return baseCustom (valor, custom_mask);
};
export var maskCNPJ = function (valor) {
	var custom_mask = '##.###.###/####-##';
	return baseCustom (valor, custom_mask);
};
export var maskCPF = function (valor) {
	var custom_mask = '###.###.###-##';
	return baseCustom (valor, custom_mask);
};
export var maskDate = function (valor) {
	var custom_mask = '##/##/####';
	return baseCustom (valor, custom_mask);
};
export var maskDatetime = function (valor) {
	var custom_mask = '##/##/#### ##:##:##';
	return baseCustom (valor, custom_mask);
};
export var maskCEP = function (valor) {
	var custom_mask = '##.###-###';
	return baseCustom (valor, custom_mask);
};
export var applyMask = function (jq_select, maskfunction, reverse, apply_on_init) {
	if (typeof reverse == 'undefined' || (reverse != null && reverse.hasOwnProperty ("__kwargtrans__"))) {;
		var reverse = false;
	};
	if (typeof apply_on_init == 'undefined' || (apply_on_init != null && apply_on_init.hasOwnProperty ("__kwargtrans__"))) {;
		var apply_on_init = false;
	};
	var onKeyPress = function (event, el) {
		var element = $ (el);
		var code = event.keyCode || event.which;
		var noprintkeys = [8, 46, 9];
		if (!__in__ (code, noprintkeys)) {
			var value = element.val ();
			if (reverse) {
				if (stringFilter (value) != '') {
					var value = str (int (stringFilter (value)));
				}
			}
			var new_value = '';
			var value = value + String.fromCharCode (code);
			var pure_value = stringFilter (value);
			if (pure_value == '') {
				element.val ('');
			}
			else {
				var new_value = maskfunction (pure_value) [0];
				element.attr ('phanterpwa-mask-justnumbers', stringFilter (new_value));
				var selection_pos = maskfunction (pure_value) [1];
				element.val (new_value);
				if (reverse) {
					element [0].selectionStart = -(len (new_value));
					element [0].selectionEnd = -(len (new_value));
				}
				else {
					element [0].selectionStart = selection_pos;
					element [0].selectionEnd = selection_pos;
				}
				if (code != 9) {
					event.preventDefault ();
				}
			}
		}
	};
	var onNonPrintingKeys = function (event, el) {
		var element = $ (el);
		var code = event.keyCode || event.which;
		var noprintkeys = [8, 46, 9];
		if (__in__ (code, noprintkeys)) {
			var value = element.val ();
			if (reverse) {
				if (stringFilter (value) != '') {
					var value = str (int (stringFilter (value)));
				}
			}
			var new_value = '';
			var pure_value = stringFilter (value);
			if (pure_value == '') {
				element.val ('');
			}
			else {
				var new_value = maskfunction (pure_value) [0];
				element.attr ('phanterpwa-mask-justnumbers', stringFilter (new_value));
				var selection_pos = maskfunction (pure_value) [1];
				element.val (new_value);
				if (reverse) {
					element [0].selectionStart = -(len (new_value));
					element [0].selectionEnd = -(len (new_value));
				}
				else {
					element [0].selectionStart = selection_pos;
					element [0].selectionEnd = selection_pos;
				}
				if (code != 9) {
					event.preventDefault ();
				}
			}
		}
	};
	var onEachElement = function (el) {
		var element = $ (el);
		var value = element.val ();
		var pure_value = stringFilter (value);
		var new_value = maskfunction (pure_value) [0];
		var selection_pos = maskfunction (pure_value) [1];
		if (apply_on_init) {
			element.val (new_value);
			if (reverse) {
				element [0].selectionStart = -(len (new_value));
				element [0].selectionEnd = -(len (new_value));
			}
			else {
				element [0].selectionStart = selection_pos;
				element [0].selectionEnd = selection_pos;
			}
		}
		element.off ('keypress.phanterpwaMask, focusout.phanterpwaMask').on ('keypress.phanterpwaMask, focusout.phanterpwaMask', (function __lambda__ (event) {
			return onKeyPress (event, this);
		}));
		element.off ('keyup.phanterpwaMask, focusout.phanterpwaMask').on ('keyup.phanterpwaMask, focusout.phanterpwaMask', (function __lambda__ (event) {
			return onNonPrintingKeys (event, this);
		}));
	};
	$ (jq_select).each ((function __lambda__ () {
		return onEachElement (this);
	}));
	return $ (jq_select);
};
export var phanterCurrency = function (jq_select, v_currency, casas_decimais, separador_decimal, separador_milhar) {
	if (typeof v_currency == 'undefined' || (v_currency != null && v_currency.hasOwnProperty ("__kwargtrans__"))) {;
		var v_currency = 'R$';
	};
	if (typeof casas_decimais == 'undefined' || (casas_decimais != null && casas_decimais.hasOwnProperty ("__kwargtrans__"))) {;
		var casas_decimais = 2;
	};
	if (typeof separador_decimal == 'undefined' || (separador_decimal != null && separador_decimal.hasOwnProperty ("__kwargtrans__"))) {;
		var separador_decimal = ',';
	};
	if (typeof separador_milhar == 'undefined' || (separador_milhar != null && separador_milhar.hasOwnProperty ("__kwargtrans__"))) {;
		var separador_milhar = '.';
	};
	return phanterDecimals (__kwargtrans__ ({jq_select: jq_select, v_currency: v_currency, casas_decimais: casas_decimais, separador_decimal: separador_decimal, separador_milhar: separador_milhar}));
};
export var phanterDecimals = function (jq_select, v_currency, casas_decimais, separador_decimal, separador_milhar) {
	if (typeof v_currency == 'undefined' || (v_currency != null && v_currency.hasOwnProperty ("__kwargtrans__"))) {;
		var v_currency = '';
	};
	if (typeof casas_decimais == 'undefined' || (casas_decimais != null && casas_decimais.hasOwnProperty ("__kwargtrans__"))) {;
		var casas_decimais = 2;
	};
	if (typeof separador_decimal == 'undefined' || (separador_decimal != null && separador_decimal.hasOwnProperty ("__kwargtrans__"))) {;
		var separador_decimal = ',';
	};
	if (typeof separador_milhar == 'undefined' || (separador_milhar != null && separador_milhar.hasOwnProperty ("__kwargtrans__"))) {;
		var separador_milhar = '.';
	};
	var l_currency = v_currency;
	var onKeyPress = function (event, el) {
		var element = $ (el);
		var code = event.keyCode || event.which;
		var value = element.attr ('phantermaskTemp');
		var key_value = String.fromCharCode (code);
		if (code == 8) {
			if (hasCaracter (value, '.')) {
				var value = stringToFloatstringLimitDecimals (value, casas_decimais);
			}
			var value = stringFilter (value);
			var value = value.__getslice__ (0, -(1), 1);
		}
		else if (code == 46 && event.key == 'Delete') {
			var value = stringFilter (value);
			var value = value.__getslice__ (1, null, 1);
		}
		else {
			var contat_value = '{0}{1}'.format (value, key_value);
			if ((key_value == separador_decimal || event.key == separador_decimal) && !(hasCaracter (value, '.'))) {
				var value = stringForceToFloatstring (contat_value, true);
			}
			else if (hasCaracter (value, '.')) {
				var value = stringForceToFloatstring (contat_value, true);
			}
			else {
				var value = stringForceToFloatstring (contat_value);
			}
		}
		element.attr ('phantermaskTemp', value);
		if (!(hasCaracter (value, '.'))) {
			if (len (value) >= casas_decimais) {
				var p_inteiro = value.__getslice__ (0, -(1) * casas_decimais, 1);
				if (!(isNotEmpty (p_inteiro))) {
					var p_inteiro = '0';
				}
				var p_decimal = value.__getslice__ (-(1) * casas_decimais, null, 1);
				var value = '{0}.{1}'.format (p_inteiro, p_decimal);
			}
			else {
				var diferenca = casas_decimais - len (value);
				var add_decs = '';
				for (var i = 0; i < diferenca; i++) {
					add_decs += '0';
				}
				var p_inteiro = '0';
				var value = '{0}.{1}{2}'.format (p_inteiro, add_decs, value);
			}
		}
		var value = stringToFloatstringLimitDecimals (value, casas_decimais);
		var new_value = '';
		if (value == '') {
			var qu_decs = '';
			for (var i = 0; i < casas_decimais; i++) {
				qu_decs += '0';
			}
			var new_value = '0{0}{1}'.format (separador_decimal, qu_decs);
			if (element.prop ('TagName') == 'INPUT') {
				element.val (floatToCurrency (stringToFloatstringLimitDecimals (new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency));
			}
			else {
				element.text (floatToCurrency (stringToFloatstringLimitDecimals (new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency));
			}
			element.attr ('phantermaskValue', stringToFloatstringLimitDecimals (new_value, casas_decimais));
		}
		else {
			var new_value = value.py_replace ('.', separador_decimal);
			if (element.prop ('TagName') == 'INPUT') {
				element.val (floatToCurrency (stringToFloatstringLimitDecimals (new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency));
			}
			else {
				element.text (floatToCurrency (stringToFloatstringLimitDecimals (new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency));
			}
			element.attr ('phantermaskValue', stringToFloatstringLimitDecimals (new_value, casas_decimais));
		}
		element [0].selectionStart = -(len (new_value));
		element [0].selectionEnd = -(len (new_value));
		if (code != 9) {
			event.preventDefault ();
		}
	};
	var onPaste = function (el) {
		setTimeout ((function __lambda__ () {
			return $ (el).trigger ('focusout');
		}), 100);
	};
	var onFocusOut = function (event, el) {
		var element = $ (el);
		var value = element.attr ('phantermaskValue');
		var value = stringToFloatstringLimitDecimals (value, casas_decimais);
		var new_value = '';
		if (value == '') {
			var qu_decs = '';
			for (var i = 0; i < casas_decimais; i++) {
				qu_decs += '0';
			}
			var new_value = '0{0}{1}'.format (separador_decimal, qu_decs);
			if (element.prop ('TagName') == 'INPUT') {
				element.val (floatToCurrency (stringToFloatstringLimitDecimals (new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency));
			}
			else {
				element.text (floatToCurrency (stringToFloatstringLimitDecimals (new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency));
			}
			element.attr ('phantermaskValue', stringToFloatstringLimitDecimals (value, casas_decimais));
		}
		else {
			var new_value = value.py_replace ('.', separador_decimal);
			if (element.prop ('TagName') == 'INPUT') {
				element.val (floatToCurrency (stringToFloatstringLimitDecimals (new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency));
			}
			else {
				element.text (floatToCurrency (stringToFloatstringLimitDecimals (new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency));
			}
			element.attr ('phantermaskValue', stringToFloatstringLimitDecimals (value, casas_decimais));
		}
		element [0].selectionStart = -(len (new_value));
		element [0].selectionEnd = -(len (new_value));
	};
	var onEachElement = function (el) {
		var l_currency = '';
		if (v_currency != '') {
			var l_currency = v_currency;
		}
		var element = $ (el);
		if (element.prop ('TagName') == 'INPUT') {
			var defaults = element.val ();
		}
		else {
			var defaults = element.text ();
		}
		var value = stringForceToFloatstring (defaults);
		element.attr ('phantermaskTemp', value);
		var value = stringToFloatstringLimitDecimals (value, casas_decimais);
		var new_value = '';
		if (value == '') {
			var qu_decs = '';
			for (var i = 0; i < casas_decimais; i++) {
				qu_decs += '0';
			}
			var new_value = ('0' + separador_decimal) + qu_decs;
			if (element.prop ('TagName') == 'INPUT') {
				element.val (floatToCurrency (stringToFloatstringLimitDecimals (new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency));
			}
			else {
				element.text (floatToCurrency (stringToFloatstringLimitDecimals (new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency));
			}
			element.attr ('phantermaskValue', stringToFloatstringLimitDecimals (value, casas_decimais));
		}
		else {
			var new_value = value.py_replace ('.', separador_decimal);
			if (element.prop ('TagName') == 'INPUT') {
				element.val (floatToCurrency (stringToFloatstringLimitDecimals (new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency));
			}
			else {
				element.text (floatToCurrency (stringToFloatstringLimitDecimals (new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency));
			}
			element.attr ('phantermaskValue', stringToFloatstringLimitDecimals (value, casas_decimais));
		}
		element [0].selectionStart = -(len (new_value));
		element [0].selectionEnd = -(len (new_value));
		element.off ('keypress.phanterpwaMask').on ('keypress.phanterpwaMask', (function __lambda__ (event) {
			return onKeyPress (event, this);
		})).off ('paste.phanterpwaMask, focusin.phanterpwaMask').on ('paste.phanterpwaMask, focusin.phanterpwaMask', (function __lambda__ () {
			return onFocusOut (this);
		})).off ('focusout.phanterpwaMask').on ('focusout.phanterpwaMask', (function __lambda__ (event) {
			return onFocusOut (event, this);
		}));
	};
	jq_select.each ((function __lambda__ () {
		return onEachElement (this);
	}));
	return $ (jq_select);
};
export var phanterpwaMask = function (mask, parameters, el) {
	var custom_mask = '';
	var casas_decimais = 2;
	var separador_decimal = ',';
	var separador_milhar = '.';
	var currency = 'R$';
	var reverse = false;
	var value = '';
	var apply_on_init = false;
	var date_format = '%d/%m/%Y';
	var datetime_format = '%d/%m/%Y %H:%M:%S';
	if (isNotEmpty (parameters)) {
		if (__in__ ('mask', parameters)) {
			var custom_mask = parameters ['mask'];
		}
		if (__in__ ('casas_decimais', parameters)) {
			var casas_decimais = int (parameters ['casas_decimais']);
		}
		if (__in__ ('separador_decimal', parameters)) {
			var separador_decimal = str (parameters ['separador_decimal']);
		}
		if (__in__ ('separador_milhar', parameters)) {
			var separador_milhar = str (parameters ['separador_milhar']);
		}
		if (__in__ ('currency', parameters)) {
			var currency = str (parameters ['currency']);
		}
		if (__in__ ('value', parameters)) {
			$ (el).val (parameters ['value']);
		}
		if (__in__ ('date_format', parameters)) {
			var date_format = parameters ['date_format'];
		}
		if (__in__ ('datetime_format', parameters)) {
			var datetime_format = parameters ['datetime_format'];
		}
		if (__in__ ('apply_on_init', parameters)) {
			var apply_on_init = parameters ['apply_on_init'];
		}
	}
	$ (el).removeClass ('masked_input');
	if (mask == 'fone') {
		$ (el).addClass ('masked_input');
		applyMask (el, maskFone, reverse, apply_on_init);
	}
	else if (mask == 'cnpj') {
		$ (el).addClass ('masked_input');
		applyMask (el, maskCNPJ, reverse, apply_on_init);
	}
	else if (mask == 'cpf') {
		$ (el).addClass ('masked_input');
		applyMask (el, maskCPF, reverse, apply_on_init);
	}
	else if (mask == 'date') {
		$ (el).off ('click.phanterpwaMaskdata focusin.phanterpwaMaskdata').on ('click.phanterpwaMaskdata focusin.phanterpwaMaskdata', console.info ('future'));
		applyMask (el, maskDate, reverse, apply_on_init);
	}
	else if (mask == 'datetime') {
		$ (el).off ('click.phanterpwaMaskdatahora focusin.phanterpwaMaskdatahora').on ('click.phanterpwaMaskdatahora focusin.phanterpwaMaskdatahora', console.info ('future'));
		applyMask (el, maskDatetime, reverse, apply_on_init);
	}
	else if (mask == 'cep') {
		$ (el).addClass ('masked_input');
		applyMask (el, maskCEP, reverse, apply_on_init);
	}
	else if (mask == 'real') {
		$ (el).addClass ('masked_input');
		phanterCurrency (el, __kwargtrans__ ({v_currency: currency, casas_decimais: casas_decimais, separador_decimal: separador_decimal, separador_milhar: separador_milhar}));
	}
	else if (mask == 'decimal') {
		$ (el).addClass ('masked_input');
		phanterDecimals (el, __kwargtrans__ ({v_currency: '', casas_decimais: casas_decimais, separador_decimal: separador_decimal, separador_milhar: separador_milhar}));
	}
	else if (mask == 'off') {
		$ (el).removeClass ('masked_input').off ('keypress.phanterpwaMask focusout.phanterpwaMask focusin.phanterpwaMask');
	}
	else if (mask == 'custom') {
		$ (el).addClass ('masked_input');
		applyMask (el, (function __lambda__ (v) {
			return baseCustom (v, parameters ['mask']);
		}), reverse, apply_on_init);
	}
	return $ (el);
};

//# sourceMappingURL=phanterpwa.frontend.fmasks.map