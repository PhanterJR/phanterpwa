from org.transcrypt.stubs.browser import __pragma__
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
        dformat_in = "yyyy-MM-dd HH:mm:ss"
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
    cdate = __new__(Date("{0}-{1}-{2} {3}:{4}:{5}".format(year, month, day, hour, minute, second)))

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
        return dformat_out
    else:
        console.error("The date/datetime value is invalid")
        return None


def check_datetime(dvalue, dformat="yyyy-MM-dd HH:mm:ss", dtype="datetime"):
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
    cdate = __new__(Date("{0}-{1}-{2} {3}:{4}:{5}".format(year, month, day, hour, minute, second)))

    result = False
    if cdate.toJSON() is not None:
        result = True
    return result


__pragma__('nokwargs')