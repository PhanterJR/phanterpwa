from org.transcrypt.stubs.browser import __pragma__
from phanterpwa.frontend.fmasks import stringFilter
__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = RegExp = \
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')

validators_list = {
    "IS_NOT_EMPTY",
    "IS_DATE",
    "IS_EQUALS",
    "IS_ACTIVATION_CODE",
    "IS_EMAIL",
}

__pragma__('kwargs')


def zfill(number, size):
    number = int(number)
    number = str(number)
    s = number
    for x in range(size - len(number)):
        s = "0" + s
    return s


def check_activation_code(code, size=6):
    if isinstance(code, str):
        code = code.strip()
        xsize = size + 2
        if (len(code) == xsize) and "-" in code:
            cod, dig = code.split("-")
            ver = "ABCDEFGHI"
            su = 0
            for char in cod:
                su += int(char)
                if su >= 9:
                    su = su - 9
            if ver[su] == dig:
                return code
    return None


def format_iso_date_datetime(dvalue, dformat_out, dtype='datetime'):
    dformat_in = "yyyy-MM-dd"
    if dtype == "datetime":
        dformat_in = "yyyy-MM-ddTHH:mm:ss"
    if dvalue is "":
        return None
    elif len(str(dvalue)) != len(dformat_in):
        console.error("The date/datetime value is invalid")
        return None
    day = None
    month = None
    year = None
    hour = "00"
    minute = "00"
    second = "00"

    ini = dformat_in.indexOf("dd")
    day = dvalue[ini:ini + 2]
    ini = dformat_in.indexOf("MM")
    month = dvalue[ini:ini + 2]
    ini = dformat_in.indexOf("yyyy")
    year = dvalue[ini:ini + 4]
    if dtype == "datetime":
        ini = dformat_in.indexOf("HH")
        hour = dvalue[ini:ini + 2]
        ini = dformat_in.indexOf("mm")
        minute = dvalue[ini:ini + 2]
        ini = dformat_in.indexOf("ss")
        second = dvalue[ini:ini + 2]
    cdate = __new__(Date("{0}-{1}-{2}T{3}:{4}:{5}".format(year, month, day, hour, minute, second)))

    result = False
    if cdate.toJSON() is not None:
        result = True
    if result:
        dformat_out = dformat_out.replace("dd", zfill(day, 2))
        dformat_out = dformat_out.replace("MM", zfill(month, 2))
        dformat_out = dformat_out.replace("yyyy", zfill(year, 4))
        if dtype == "datetime":
            dformat_out = dformat_out.replace("HH", zfill(hour, 2))
            dformat_out = dformat_out.replace("mm", zfill(minute, 2))
            dformat_out = dformat_out.replace("ss", zfill(second, 2))
            dformat_out = dformat_out.replace("T", " ")
        return dformat_out
    else:
        console.error("The date/datetime value is invalid")
        return None


def check_datetime(dvalue, dformat="yyyy-MM-ddTHH:mm:ss", dtype="datetime"):
    if any(["yyyy" not in dformat,
            "MM" not in dformat,
            "dd" not in dformat]):
        return False
    if dtype == "datetime":
        if any(["HH" not in dformat,
                "mm" not in dformat,
                "ss" not in dformat]):
            return False
    if len(str(dvalue)) != len(dformat):
        return False

    day = None
    month = None
    year = None
    hour = "00"
    minute = "00"
    second = "00"

    ini = dformat.indexOf("dd")
    day = dvalue[ini:ini + 2]
    ini = dformat.indexOf("MM")
    month = dvalue[ini:ini + 2]
    ini = dformat.indexOf("yyyy")
    year = dvalue[ini:ini + 4]
    if dtype == "datetime":
        ini = dformat.indexOf("HH")
        hour = dvalue[ini:ini + 2]
        ini = dformat.indexOf("mm")
        minute = dvalue[ini:ini + 2]
        ini = dformat.indexOf("ss")
        second = dvalue[ini:ini + 2]
    cdate = __new__(Date("{0}-{1}-{2}T{3}:{4}:{5}".format(year, month, day, hour, minute, second)))

    result = False
    if cdate.toJSON() is not None:
        result = True
    return result


class Valider():
    def __init__(self, value, validators_list):
        self.validators_list = validators_list
        self.value = value
        self.tests = {}

    def validate(self):
        validate_test_pass = list()
        validate_test = self.validators_list
        value_for_validate = self.value
        is_empty_or = False
        self.tests = {}
        for x in validate_test:
            self.tests[x] = "Ignored"
        if "IS_EMPTY_OR" in validate_test:
            if (value_for_validate is js_undefined) or \
                (value_for_validate is None) or (value_for_validate == ""):
                validate_test_pass.append(True)
                self.tests["IS_EMPTY_OR"] = "Pass"
                is_empty_or = True
            else:
                self.tests["IS_EMPTY_OR"] = "Fail"
            validate_test.pop("IS_EMPTY_OR")
        if not is_empty_or:
            for x in validate_test:
                if x is not None and x is not js_undefined:
                    validate_test_pass.append(self._validates(x))

        if all(validate_test_pass):
            return True

        else:
            return False

    def _validates(self, validate_name):
        value_for_validate = self.value
        validate_test_pass = list()
        is_not_valid = True
        if validate_name.startswith("IS_IN_SET:"):
            is_not_valid = False
            res = False
            list_options = JSON.parse(validate_name[10:])
            if list_options is not None or list_options is not js_undefined:
                list_options = JSON.parse(list_options)
                if list_options.indexOf(value_for_validate) > -1:
                    res = True
            validate_test_pass.append(res)

        if validate_name == "IS_NOT_EMPTY":
            self.tests[validate_name] = "Fail"
            is_not_valid = False
            if (value_for_validate is js_undefined) or \
                (value_for_validate is None) or (value_for_validate == ""):
                validate_test_pass.append(False)
            else:
                validate_test_pass.append(True)
                self.tests[validate_name] = "Pass"

        if validate_name == "IS_ACTIVATION_CODE":
            self.tests[validate_name] = "Fail"
            is_not_valid = False
            is_activation_code = False
            res = check_activation_code(value_for_validate)
            if res is not None:
                is_activation_code = True
            validate_test_pass.append(is_activation_code)

        if validate_name.startswith("IS_DATE"):
            self.tests[validate_name] = "Fail"
            is_not_valid = False
            if validate_name.startswith("IS_DATE:"):
                dformat = validate_name[8:]
                res = check_datetime(value_for_validate, dformat, "date")
                validate_test_pass.append(res)
            elif validate_name.startswith("IS_DATETIME:"):
                dformat = validate_name[12:]
                res = check_datetime(value_for_validate, dformat, "datetime")
                validate_test_pass.append(res)
            elif validate_name == "IS_DATETIME":
                dformat = validate_name[12:]
                res = check_datetime(value_for_validate)
                validate_test_pass.append(res)
            else:
                dformat = validate_name[12:]
                res = check_datetime(value_for_validate, "yyyy-MM-dd", "date")
                validate_test_pass.append(res)

        if validate_name.startswith("IS_EQUALS:"):
            self.tests[validate_name] = "Fail"
            is_not_valid = False
            comp = validate_name[10:]
            if comp.startswith("#"):
                val = jQuery(comp).val()
                if val == value_for_validate:
                    validate_test_pass.append(True)
                    self.tests[validate_name] = "Pass"
                else:
                    validate_test_pass.append(False)
            else:
                if comp == value_for_validate:
                    validate_test_pass.append(True)
                    self.tests[validate_name] = "Pass"
                else:
                    validate_test_pass.append(False)

        if validate_name.startswith("MATCH:"):
            self.tests[validate_name] = "Fail"
            is_not_valid = False
            regex = __new__(RegExp(validate_name[6:]))

            if value_for_validate.match(regex) is not None:
                validate_test_pass.append(True)
                self.tests[validate_name] = "Pass"
            else:
                validate_test_pass.append(False)

        if validate_name.startswith("MASK:"):
            self.tests[validate_name] = "Fail"
            is_not_valid = False
            mask_val = validate_name[5:]
            cont_mask = 0
            for x in str(mask_val):
                if x == "#":
                    cont_mask += 1

            if len(stringFilter(str(value_for_validate))) == cont_mask:
                validate_test_pass.append(True)
                self.tests[validate_name] = "Pass"
            else:
                validate_test_pass.append(False)
        if validate_name == "IS_EMAIL":
            value_for_validate = str(value_for_validate).strip()
            self.tests[validate_name] = "Fail"
            is_not_valid = False
            if "@" in value_for_validate:
                REGEX_BODY = __pragma__(
                    'js',
                    '{}',
                    r'/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([_a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/'
                )
                if REGEX_BODY.test(value_for_validate):
                    validate_test_pass.append(True)
                    self.tests[validate_name] = "Pass"
                else:
                    validate_test_pass.append(False)
            else:
                validate_test_pass.append(False)

        if is_not_valid:
            console.error("The {0} is not valid!".format(validate_name))
            return False

        if all(validate_test_pass):
            return True
        else:
            return False



__pragma__('nokwargs')
