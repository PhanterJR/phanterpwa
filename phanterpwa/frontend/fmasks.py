from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = String = setTimeout =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')


class Mask():
    def __init__(self, target_selector, mask_function, reverse=False, apply_on_init=False):
        self.target_selector = target_selector
        self.element_target = jQuery(target_selector)
        self.mask_function = mask_function
        self.reverse = reverse
        self.apply_on_init = apply_on_init
        self.start()

    @staticmethod
    def stringFilter(
        value,
        you_want_array=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
        value = str(value)
        new_value = ""
        for x in value:
            if x in you_want_array:
                new_value += x
        return new_value

    def onKeyPress(self, event, el):
        event.preventDefault()
        code = event.keyCode or event.which
        element = jQuery(el)
        pos = element[0].selectionStart
        end = element[0].selectionEnd
        if pos == end:
            current_value = element.val()
            v = String.fromCharCode(code)
            text0 = current_value[0: pos] + v
            text1 = current_value[pos:]
            numbers = [str(x) for x in range(10)]
            if v in numbers:
                # print(current_value[pos])
                if current_value[pos] in numbers or current_value[pos] == "_":
                    pos = pos + 1
                else:
                    pos = pos + 2
        else:
            current_value = element.val()
            v = String.fromCharCode(code)
            text0 = current_value[0: pos] + v
            text1 = current_value[end:]
            numbers = [str(x) for x in range(10)]
            if v in numbers:
                pos = pos + 1
        new_value = "{0}{1}".format(text0, text1)
        pure_value = self.stringFilter(new_value)
        new_value = self.mask_function(pure_value)[0]
        if pure_value is not "":
            element.val(new_value)
        else:
            element.val("")

        element[0].selectionStart = self.mask_function(pure_value)[1]
        element[0].selectionEnd = self.mask_function(pure_value)[1]

    def onKeyUp(self, event, el):
        element = jQuery(el)
        new_value = element.val()
        pure_value = self.stringFilter(new_value)
        new_value = self.mask_function(pure_value)[0]
        if pure_value is not "":
            element.val(new_value)
        else:
            element.val("")

        element[0].selectionStart = self.mask_function(pure_value)[1]
        element[0].selectionEnd = self.mask_function(pure_value)[1]
        element.focus()
        element[0].setSelectionRange(self.mask_function(pure_value)[1], self.mask_function(pure_value)[1])


    def onNonPrintingKeysIn(self, event, el):
        noprintkeys = [8, 46]
        code = event.keyCode or event.which
        element = jQuery(el)
        if code in noprintkeys:
            if code == 8:
                current_value = element.val()
                if self.stringFilter(current_value) is not "":
                    pure_value = self.stringFilter(current_value)
                    pure_value = pure_value[0:-1]
                    new_value = self.mask_function(pure_value)[0]
                    if pure_value is not "":
                        element.val(new_value)
                    else:
                        element.val("")
                    element[0].selectionStart = self.mask_function(pure_value)[1]
                    element[0].selectionEnd = self.mask_function(pure_value)[1]
                else:
                    element.val("")
            elif code == 46:
                current_value = element.val()
                if self.stringFilter(current_value) is not "":
                    pos = element[0].selectionStart
                    end = element[0].selectionEnd
                    if pos == end:
                        text0 = current_value[0:pos]
                        numbers = [str(x) for x in range(10)]
                        if current_value[pos] in numbers:
                            text1 = current_value[pos + 1:]
                        elif current_value[pos] is not "":
                            text1 = current_value[pos + 2:]

                        new_value = "{0}{1}".format(text0, text1)
                        element[0].selectionStart = pos
                        element[0].selectionEnd = pos
                    else:
                        text0 = current_value[0: pos]
                        text1 = current_value[end:]
                        new_value = "{0}{1}".format(text0, text1)
                        element[0].selectionStart = pos
                        element[0].selectionEnd = pos
                    pure_value = self.stringFilter(new_value)
                    new_value = self.mask_function(pure_value)[0]
                    if pure_value is not "":
                        element.val(new_value)
                    else:
                        element.val("")
                    element[0].selectionStart = pos
                    element[0].selectionEnd = pos
                else:
                    element.val("")

            event.preventDefault()

    def onNonPrintingKeys(self, event, el):
        event.preventDefault()
        element = jQuery(el)
        code = event.keyCode or event.which
        noprintkeys = [8, 46, 9]
        if code in noprintkeys:
            value = element.val()
            element.val(value + "_")
            if (self.reverse):
                if (self.stringFilter(value) != ""):
                    value = str(int(self.stringFilter(value)))
            new_value = ""

            pure_value = self.stringFilter(value)
            if pure_value == "":
                element.val("")
            else:
                new_value = self.mask_function(pure_value)[0]
                element.attr("phanterpwa-mask-justnumbers", self.stringFilter(new_value))
                selection_pos = self.mask_function(pure_value)[1]
                element.val(new_value)
                if (self.reverse):
                    element[0].selectionStart = -len(new_value)
                    element[0].selectionEnd = -len(new_value)
                else:
                    element[0].selectionStart = selection_pos
                    element[0].selectionEnd = selection_pos
                if(code != 9):
                    event.preventDefault()
        else:
            pure_value = self.stringFilter(element.val())
            if pure_value == "":
                element.val("")

    def onFocusOut(self, event, el):
        element = jQuery(el)
        new_value = element.val()
        pure_value = self.stringFilter(new_value)
        new_value = self.mask_function(pure_value)[0]
        if pure_value is not "":
            element.val(new_value)
        else:
            element.val("")


    def start(self):
        element = jQuery(self.target_selector)
        value = element.val()
        pure_value = self.stringFilter(value)
        new_value = self.mask_function(pure_value)[0]
        selection_pos = self.mask_function(pure_value)[1]

        if(self.apply_on_init):
            element.val(new_value)
            if(self.reverse):
                element[0].selectionStart = -len(new_value)
                element[0].selectionEnd = -len(new_value)
            else:
                element[0].selectionStart = selection_pos
                element[0].selectionEnd = selection_pos

        element.off(
            "keypress.phanterpwaMask"
        ).on(
            "keypress.phanterpwaMask",
            lambda event: self.onKeyPress(event, this)
        )
        element.off(
            "focusout.phanterpwaMask"
        ).on(
            "focusout.phanterpwaMask",
            lambda event: self.onFocusOut(event, this)
        )
        element.off(
            "keyup.phanterpwaMask2,"
        ).on(
            "keyup.phanterpwaMask2,",
            lambda event: self.onKeyUp(event, this)
        )
        element.off(
            "keydown.phanterpwaMask, focusout.phanterpwaMask"
        ).on(
            "keydown.phanterpwaMask, focusout.phanterpwaMask",
            lambda event: self.onNonPrintingKeysIn(event, this)
        )


def date_and_datetime_to_maks(value):
    date_format = ["d", "M", "o", "t", "y", "H", "m", "s"]
    string_mask = ""
    if isinstance(value, str):
        for x in value:
            if x in date_format:
                y = "#"
            else:
                y = x
            string_mask += y
    return string_mask


def isNotEmpty(value):
    if ((value is not None) and (value is not "") and (value is not js_undefined)):
        return True
    else:
        return False


def stringFilter(
    value,
    you_want_array=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
    value = str(value)
    new_value = ""
    for x in value:
        if x in you_want_array:
            new_value += x
    return new_value


def hasCaracter(value, caracter="."):
    value = str(value)
    has_caractere = False
    if caracter in value:
        has_caractere = True
    return has_caractere


def justSearchedCaracter(value, caractere="."):
    has_caractere = False
    value = str(value)
    new_value = ""
    for x in value:
        if x == caractere:
            if not has_caractere:
                new_value += x
                has_caractere = True
        else:
            new_value += x
    return new_value


def stringForceToFloatstring(value, force_dot=False, localeBR=True):
    if isNotEmpty(value):
        value = str(value)
        if localeBR:
            value = value.replace(",", ".")
        value = stringFilter(value, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."])
        value = justSearchedCaracter(value)
        if (value != ""):
            if (value == "."):
                if (force_dot):
                    value = "0."
                else:
                    value = ""
            else:
                if not force_dot:
                    value = str(float(value))
        return value
    else:
        return ""


def stringToFloatstringLimitDecimals(value, casas_decimais=2, localeBR=True):
    value = str(value)
    if isNotEmpty(value):
        if(localeBR):
            value = value.replace(",", ".")
        value = stringFilter(value, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."])
        value = justSearchedCaracter(value)
        if(value != ""):
            value = str(float(value))
            p_inteiro = value.split(".")[0]
            p_decimal = value.split(".")[1]
            if not isNotEmpty(p_decimal):
                p_decimal = "0"
            if len(p_decimal) < casas_decimais:
                np_decimal = ""
                for x in range(casas_decimais - len(p_decimal)):
                    np_decimal += "0"
                p_decimal = p_decimal + np_decimal
            else:
                np_decimal = ""
                for i in range(casas_decimais):
                    np_decimal += p_decimal[i]
                p_decimal = np_decimal
            r = "{0}.{1}".format(p_inteiro, p_decimal)
            return r
        return value
    else:
        return ""


def floatToCurrency(value, casas_decimais=2, separador_decimal=",", separador_milhar=".", currency=""):
    casas_decimais = casas_decimais
    separador_decimal = separador_decimal
    separador_milhar = separador_milhar
    value = str(value)
    p_m_inteiro = "0"
    p_m_decimal = ""
    for i in range(casas_decimais):
        p_m_decimal += "0"

    if hasCaracter(value, "."):
        p_inteiro = value.split(".")[0]
        p_decimal = value.split(".")[1]
        if(isNotEmpty(p_inteiro)):
            p_inteiro = p_inteiro.split("").reverse().join("")
            str_inteiro = ""
            tamanho_inteiro = len(p_inteiro)
            adicionar_separador = False
            if (tamanho_inteiro > 3):
                for i in range(tamanho_inteiro):
                    if (((i + 1) % 3) == 0):
                        str_inteiro += p_inteiro[i]
                        adicionar_separador = True
                    else:
                        if(adicionar_separador):
                            adicionar_separador = False
                            str_inteiro += separador_milhar + p_inteiro[i]
                        else:
                            str_inteiro += p_inteiro[i]
            else:
                for i in range(tamanho_inteiro):
                    str_inteiro += p_inteiro[i]
            p_m_inteiro = str_inteiro.split("").reverse().join("")

        if(isNotEmpty(p_decimal)):
            str_cd = ""
            if (p_decimal.length > casas_decimais):
                for i in range(casas_decimais):
                    str_cd += p_decimal[i]
            else:
                for i in range(len(p_decimal)):
                    str_cd += p_decimal[i]
                diferenca = casas_decimais - len(p_decimal)
                tracos = ""
                for i in range(diferenca):
                    tracos += "0"
                str_cd += tracos
            p_m_decimal = str_cd

    else:
        if value != "":
            t_m_inteiro = int(value)
            if (isNotEmpty(t_m_inteiro)):
                p_m_inteiro = str(t_m_inteiro)
    if(isNotEmpty(currency)):
        r = "{0} {1}{2}{3}".format(currency, p_m_inteiro, separador_decimal, p_m_decimal)
    else:
        r = "{1}{2}{3}".format(p_m_inteiro, separador_decimal, p_m_decimal)
    return r


def baseCustom(value, custom_mask, cursorPosition=0):
    value = str(value)
    size = len(value)
    char_plus = 0
    pos_num = 0
    new_value = ""
    for i in range(len(custom_mask)):
        if (custom_mask[i] == "#"):
            if (pos_num < size):
                new_value += value[pos_num]
                pos_num += 1
            else:
                new_value += "_"
                pos_num += 1
        else:
            if (i < (size + char_plus)):
                char_plus += 1

            new_value += custom_mask[i]
    if new_value.indexOf("_") > 0:
        cursorPosition = new_value.indexOf("_")
    else:
        cursorPosition = int(size) + char_plus
    return [new_value, cursorPosition]


def maskFone(valor):
    valor = str(valor)
    size = len(valor)
    if (size == 10):
        custom_mask = "(##) ####-####"
    elif (size == 11):
        custom_mask = "(##) # ####-####"
    elif (size > 11):
        custom_mask = "(##) #####-#########"
    else:
        custom_mask = "(##) # ####-####"
    return baseCustom(valor, custom_mask)


def maskCNPJ(valor):
    custom_mask = "##.###.###/####-##"
    return baseCustom(valor, custom_mask)


def maskCPF(valor):
    custom_mask = "###.###.###-##"
    return baseCustom(valor, custom_mask)


def maskDate(valor):
    custom_mask = "##/##/####"
    return baseCustom(valor, custom_mask)


def maskDatetime(valor):
    custom_mask = "##/##/#### ##:##:##"
    return baseCustom(valor, custom_mask)


def maskCEP(valor):
    custom_mask = "##.###-###"
    return baseCustom(valor, custom_mask)


def applyMask(jq_select, maskfunction, reverse=False, apply_on_init=False):

    def onKeyPress(event, el):
        element = jQuery(el)
        code = event.keyCode or event.which
        noprintkeys = [8, 46, 9]
        if code not in noprintkeys:
            value = element.val()
            if (reverse):
                if (stringFilter(value) != ""):
                    value = str(int(stringFilter(value)))
            new_value = ""

            value = value + String.fromCharCode(code)
            pure_value = stringFilter(value)
            if pure_value == "":
                element.val("")
            else:
                new_value = maskfunction(pure_value)[0]
                element.attr("phanterpwa-mask-justnumbers", stringFilter(new_value))
                selection_pos = maskfunction(pure_value)[1]
                element.val(new_value)
                if (reverse):
                    element[0].selectionStart = -len(new_value)
                    element[0].selectionEnd = -len(new_value)
                else:
                    element[0].selectionStart = selection_pos
                    element[0].selectionEnd = selection_pos
                if(code != 9):
                    event.preventDefault()

    def onNonPrintingKeys(event, el):
        element = jQuery(el)
        code = event.keyCode or event.which
        noprintkeys = [8, 46, 9]
        if code in noprintkeys:
            value = element.val()
            if (reverse):
                if (stringFilter(value) != ""):
                    value = str(int(stringFilter(value)))
            new_value = ""

            pure_value = stringFilter(value)
            if pure_value == "":
                element.val("")
            else:
                new_value = maskfunction(pure_value)[0]
                element.attr("phanterpwa-mask-justnumbers", stringFilter(new_value))
                selection_pos = maskfunction(pure_value)[1]
                element.val(new_value)
                if (reverse):
                    element[0].selectionStart = -len(new_value)
                    element[0].selectionEnd = -len(new_value)
                else:
                    element[0].selectionStart = selection_pos
                    element[0].selectionEnd = selection_pos
                if(code != 9):
                    event.preventDefault()

    def onEachElement(el):
        element = jQuery(el)
        value = element.val()
        pure_value = stringFilter(value)
        new_value = maskfunction(pure_value)[0]
        selection_pos = maskfunction(pure_value)[1]

        if(apply_on_init):
            element.val(new_value)
            if(reverse):
                element[0].selectionStart = -len(new_value)
                element[0].selectionEnd = -len(new_value)
            else:
                element[0].selectionStart = selection_pos
                element[0].selectionEnd = selection_pos

        element.off(
            "keypress.phanterpwaMask, focusout.phanterpwaMask"
        ).on(
            "keypress.phanterpwaMask, focusout.phanterpwaMask",
            lambda event: onKeyPress(event, this)
        )

        element.off(
            "keyup.phanterpwaMask, focusout.phanterpwaMask"
        ).on(
            "keyup.phanterpwaMask, focusout.phanterpwaMask",
            lambda event: onNonPrintingKeys(event, this)
        )

    jQuery(jq_select).each(lambda: onEachElement(this))
    return jQuery(jq_select)


def phanterCurrency(
    jq_select,
    v_currency="R$",
    casas_decimais=2,
    separador_decimal=",",
    separador_milhar="."):
    return phanterDecimals(
        jq_select=jq_select,
        v_currency=v_currency,
        casas_decimais=casas_decimais,
        separador_decimal=separador_decimal,
        separador_milhar=separador_milhar)


def phanterDecimals(
    jq_select,
    v_currency="",
    casas_decimais=2,
    separador_decimal=",",
    separador_milhar="."):
    l_currency = v_currency

    def onKeyPress(event, el):
        element = jQuery(el)
        code = event.keyCode or event.which
        value = element.attr("phantermaskTemp")
        key_value = String.fromCharCode(code)
        if (code == 8):
            if(hasCaracter(value, ".")):
                value = stringToFloatstringLimitDecimals(value, casas_decimais)
            value = stringFilter(value)
            value = value[0:-1]
        elif((code == 46) and event.key == "Delete"):
            value = stringFilter(value)
            value = value[1:]
        else:
            contat_value = "{0}{1}".format(value, key_value)
            if (((key_value == separador_decimal) or (event.key == separador_decimal)) and not hasCaracter(value, ".")):
                value = stringForceToFloatstring(contat_value, True)
            else:
                if (hasCaracter(value, ".")):
                    value = stringForceToFloatstring(contat_value, True)
                else:
                    value = stringForceToFloatstring(contat_value)
        element.attr("phantermaskTemp", value)
        if not hasCaracter(value, "."):
            if (len(value) >= casas_decimais):
                p_inteiro = value[0: (-1) * casas_decimais]
                if not isNotEmpty(p_inteiro):
                    p_inteiro = "0"
                p_decimal = value[(-1) * casas_decimais:]
                value = "{0}.{1}".format(p_inteiro, p_decimal)
            else:
                diferenca = casas_decimais - len(value)
                add_decs = ""
                for i in range(diferenca):
                    add_decs += "0"
                p_inteiro = "0"
                value = "{0}.{1}{2}".format(p_inteiro, add_decs, value)
        value = stringToFloatstringLimitDecimals(value, casas_decimais)
        new_value = ""
        if (value == ""):
            qu_decs = ""
            for i in range(casas_decimais):
                qu_decs += "0"
            new_value = "0{0}{1}".format(separador_decimal, qu_decs)
            if(element.prop('TagName') == "INPUT"):
                element.val(
                    floatToCurrency(
                        stringToFloatstringLimitDecimals(
                            new_value,
                            casas_decimais
                        ),
                        casas_decimais,
                        separador_decimal,
                        separador_milhar,
                        l_currency)
                )
            else:
                element.text(
                    floatToCurrency(
                        stringToFloatstringLimitDecimals(
                            new_value,
                            casas_decimais
                        ),
                        casas_decimais,
                        separador_decimal,
                        separador_milhar,
                        l_currency)
                )
            element.attr("phantermaskValue", stringToFloatstringLimitDecimals(new_value, casas_decimais))
        else:
            new_value = value.replace(".", separador_decimal)
            if(element.prop('TagName') == "INPUT"):
                element.val(
                    floatToCurrency(
                        stringToFloatstringLimitDecimals(
                            new_value,
                            casas_decimais
                        ),
                        casas_decimais,
                        separador_decimal,
                        separador_milhar,
                        l_currency)
                )
            else:
                element.text(
                    floatToCurrency(
                        stringToFloatstringLimitDecimals(
                            new_value,
                            casas_decimais
                        ),
                        casas_decimais,
                        separador_decimal,
                        separador_milhar,
                        l_currency)
                )
            element.attr("phantermaskValue", stringToFloatstringLimitDecimals(new_value, casas_decimais))
        element[0].selectionStart = -len(new_value)
        element[0].selectionEnd = -len(new_value)
        if (code != 9):
            event.preventDefault()

    def onPaste(el):
        setTimeout(
            lambda: jQuery(el).trigger("focusout"),
            100
        )

    def onFocusOut(event, el):
        element = jQuery(el)
        value = element.attr("phantermaskValue")
        value = stringToFloatstringLimitDecimals(value, casas_decimais)
        new_value = ""
        if (value == ""):
            qu_decs = ""
            for i in range(casas_decimais):
                qu_decs += "0"
            new_value = "0{0}{1}".format(separador_decimal, qu_decs)
            if(element.prop('TagName') == "INPUT"):
                element.val(floatToCurrency(stringToFloatstringLimitDecimals(
                    new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency))
            else:
                element.text(floatToCurrency(stringToFloatstringLimitDecimals(
                    new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency))
            element.attr("phantermaskValue", stringToFloatstringLimitDecimals(value, casas_decimais))
        else:
            new_value = value.replace(".", separador_decimal)
            if(element.prop('TagName') == "INPUT"):
                element.val(floatToCurrency(stringToFloatstringLimitDecimals(
                    new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency))
            else:
                element.text(floatToCurrency(stringToFloatstringLimitDecimals(
                    new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency))
            element.attr("phantermaskValue", stringToFloatstringLimitDecimals(value, casas_decimais))
        element[0].selectionStart = -len(new_value)
        element[0].selectionEnd = -len(new_value)

    def onEachElement(el):
        l_currency = ""
        if(v_currency != ""):
            l_currency = v_currency
        element = jQuery(el)
        if(element.prop('TagName') == "INPUT"):
            defaults = element.val()
        else:
            defaults = element.text()
        value = stringForceToFloatstring(defaults)
        element.attr("phantermaskTemp", value)
        value = stringToFloatstringLimitDecimals(value, casas_decimais)
        new_value = ""
        if (value == ""):
            qu_decs = ""
            for i in range(casas_decimais):
                qu_decs += "0"
            new_value = "0" + separador_decimal + qu_decs
            if(element.prop('TagName') == "INPUT"):
                element.val(floatToCurrency(stringToFloatstringLimitDecimals(
                    new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency))
            else:
                element.text(floatToCurrency(stringToFloatstringLimitDecimals(
                    new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency))
            element.attr("phantermaskValue", stringToFloatstringLimitDecimals(value, casas_decimais))
        else:
            new_value = value.replace(".", separador_decimal)
            if(element.prop('TagName') == "INPUT"):
                element.val(floatToCurrency(stringToFloatstringLimitDecimals(
                    new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency))
            else:
                element.text(floatToCurrency(stringToFloatstringLimitDecimals(
                    new_value, casas_decimais), casas_decimais, separador_decimal, separador_milhar, l_currency))
            element.attr("phantermaskValue", stringToFloatstringLimitDecimals(value, casas_decimais))
        element[0].selectionStart = -len(new_value)
        element[0].selectionEnd = -len(new_value)
        element.off(
            'keypress.phanterpwaMask'
        ).on(
            'keypress.phanterpwaMask',
            lambda event: onKeyPress(event, this)
        ).off(
            "paste.phanterpwaMask, focusin.phanterpwaMask"
        ).on(
            "paste.phanterpwaMask, focusin.phanterpwaMask",
            lambda: onFocusOut(this)
        ).off(
            'focusout.phanterpwaMask'
        ).on(
            'focusout.phanterpwaMask',
            lambda event: onFocusOut(event, this)
        )
    jq_select.each(lambda: onEachElement(this))
    return jQuery(jq_select)


def phanterpwaMask(mask, parameters, el):
    custom_mask = ""
    casas_decimais = 2
    separador_decimal = ","
    separador_milhar = "."
    currency = "R$"
    reverse = False
    value = ""
    apply_on_init = False
    date_format = "%d/%m/%Y"
    datetime_format = "%d/%m/%Y %H:%M:%S"
    if (isNotEmpty(parameters)):
        if ("mask" in parameters):
            custom_mask = parameters['mask']
        if ("casas_decimais" in parameters):
            casas_decimais = int(parameters['casas_decimais'])
        if ("separador_decimal" in parameters):
            separador_decimal = str(parameters['separador_decimal'])
        if ("separador_milhar" in parameters):
            separador_milhar = str(parameters['separador_milhar'])
        if ("currency" in parameters):
            currency = str(parameters['currency'])
        if ("value" in parameters):
            jQuery(el).val(parameters['value'])
        if ("date_format" in parameters):
            date_format = parameters['date_format']
        if ("datetime_format" in parameters):
            datetime_format = parameters['datetime_format']
        if ("apply_on_init" in parameters):
            apply_on_init = parameters['apply_on_init']
    jQuery(el).removeClass("masked_input")
    if (mask == "fone"):
        jQuery(el).addClass("masked_input")
        applyMask(el, maskFone, reverse, apply_on_init)
    elif(mask == "cnpj"):
        jQuery(el).addClass("masked_input")
        applyMask(el, maskCNPJ, reverse, apply_on_init)
    elif(mask == "cpf"):
        jQuery(el).addClass("masked_input")
        applyMask(el, maskCPF, reverse, apply_on_init)
    elif(mask == "date"):
        jQuery(
            el
        ).off(
            'click.phanterpwaMaskdata focusin.phanterpwaMaskdata'
        ).on(
            'click.phanterpwaMaskdata focusin.phanterpwaMaskdata',
            console.info("future")
        )
        applyMask(el, maskDate, reverse, apply_on_init)
    elif(mask == "datetime"):
        jQuery(
            el
        ).off(
            'click.phanterpwaMaskdatahora focusin.phanterpwaMaskdatahora'
        ).on(
            'click.phanterpwaMaskdatahora focusin.phanterpwaMaskdatahora',
            console.info("future")
        )
        applyMask(el, maskDatetime, reverse, apply_on_init)
    elif(mask == "cep"):
        jQuery(el).addClass("masked_input")
        applyMask(el, maskCEP, reverse, apply_on_init)
    elif(mask == "real"):
        jQuery(el).addClass("masked_input")
        phanterCurrency(el,
            v_currency=currency,
            casas_decimais=casas_decimais,
            separador_decimal=separador_decimal,
            separador_milhar=separador_milhar)
    elif(mask == "decimal"):
        jQuery(el).addClass("masked_input")
        phanterDecimals(el,
            v_currency="",
            casas_decimais=casas_decimais,
            separador_decimal=separador_decimal,
            separador_milhar=separador_milhar)
    elif(mask == "off"):
        jQuery(
            el
        ).removeClass(
            "masked_input"
        ).off(
            "keypress.phanterpwaMask focusout.phanterpwaMask focusin.phanterpwaMask"
        )
    elif(mask == "custom"):
        jQuery(el).addClass("masked_input")
        applyMask(el, lambda v: baseCustom(v, parameters['mask']), reverse, apply_on_init)
    return jQuery(el)
