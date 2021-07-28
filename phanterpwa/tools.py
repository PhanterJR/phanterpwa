"""
Title: XmlConstructor

Author: PhanterJR<junior.conex@gmail.com>

License: MIT

Coding: utf-8

Tools that can be used in PhanterPWA.
"""

import re
import sys
import os
import json
import time
import shutil
from datetime import datetime, date
from pathlib import PurePath
from subprocess import Popen, PIPE, call
from unicodedata import normalize
from phanterpwa import __install_requeriments__ as requeriments
from tornado import escape


def check_requeriments() -> "generator - each step returns (str, bool)":
    """Each generator step returns a tuple with the name of the checked requirement and a boolean, True for Passed and
        False for Failed
    """
    for x in requeriments:
        if ">" in x or "<" in x or "=" in x:
            x = x.split(">")[0]
            x = x.split("=")[0]
            x = x.split("<")[0]
        checked = call(["pip", "show", x])
        yield (x, not bool(checked))


def search_google_chrome():
    if sys.platform == "win32":
        winvars = [
            '%PROGRAMFILES(X86)%\\Google',
            '%PROGRAMW6432%\\Google',
            '%PROGRAMFILES%\\Google',
            '%LOCALAPPDATA%\\Google',
        ]
        new_winvars = []
        for x in winvars:
            p = Popen('echo "{0}"'.format(x), stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            ret, error = p.communicate()
            if ret.strip():
                if x not in new_winvars:
                    new_winvars.append(x)
        print(new_winvars)
        for x in new_winvars:
            p = Popen('where /r "{0}" "chrome.exe"'.format(x), stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            print(p.args)
            ret, error = p.communicate()
            if ret.strip():
                return ret.strip()

    elif sys.platform.startswith('linux'):
        names = [
            'google-chrome',
            'google-chrome-stable'
            'chromium-browser',
            'chromium',
        ]
        for x in names:
            p = Popen('which {0}'.format(x), stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            ret, error = p.communicate()
            if ret.strip():
                return ret.strip()
    else:
        return None


def interpolate(xstring, context: dict, delimiters: (list, tuple)=["{{", "}}"], ignore_non_strings: bool=False):
    """Interpolates by replacing strings in certain delimiters

    :param xstring: String that will be interpolated
    :param context: Dictionary containing the strings that will be replaced, the keys will be tracked in the string and
        the values will be replaced by the match found.
    :param delimiters: Is the pair of strings that delimit each variable contained in xstring
    :param ignore_non_strings: By default, all xstring will be converted to str, if set to True, different string
        values or XmlConstructor will not be changed.

    Example:
        >>> from phanterpwa.tools import interpolate
        >>> r = interpolate(
        ...     "long string: Ford {{model1}}, Chevrolet {{model2}}.",
        ...     {"model1": "Focus", "model2": "Celta"}
        ... )
        >>> print(r)
        long string: Ford Focus, Chevrolet Celta.
    """

    if not (isinstance(delimiters, (list, tuple)) and len(delimiters) == 2):
        raise ValueError("The delimiters must be list or tuple type and need two values.")
    if ignore_non_strings:
        from phanterpwa.xmlconstructor import XmlConstructor
        if not isinstance(xstring, (str, XmlConstructor)):
            return xstring
    xstring = str(xstring)
    if isinstance(context, dict):
        for x in context:
            k = "".join([delimiters[0], x, delimiters[1]])
            ls = xstring.split(k)
            ns = str(context[x]).join(ls)
            xstring = ns
        return xstring
    else:
        raise ValueError("The context from _format method must be dict. Given: {0}".format(type(context)))


def sass_change_vars(string_sass: str, context: dict={}) -> str:
    """This function is used to change the values of variables in a sass file

    :param string_sass: String with the sass code
    :param context: The dictionary keys in context represent the variables that will be searched for in the sass code
        with their respective new values.

    Example:
        >>> from phanterpwa.tools import sass_change_vars
        >>> sass_str = '''
        ... $BG: red
        ... $FG: green
        ... .my_class
        ...     background-color: $BG
        ...     color: $FG
        ... '''
        >>> print(sass_change_vars(sass_str, {"BG": blue, "FG": "black"}))
        $BG: blue
        $FG: black
        .my_class
            background-color: $BG
            color: $FG
    """

    ns = ""
    if all([isinstance(context, dict), isinstance(string_sass, str), context, string_sass]):
        lines = string_sass.split('\n')
        for x in lines:
            find = False
            for y in context:
                v = "".join(["$", y, ":"])
                if v in x:
                    ini = x.index(v)
                    ns = "".join([ns, x[:ini], v, " ", context[y], "\n"])
                    find = True
                    break
            if not find:
                ns = "".join([ns, x, "\n"])
        return ns[:-1]

    elif not isinstance(context, dict):
        raise ValueError("The context must be dict type. Given: {0}".format(type(context)))

    elif not isinstance(string_sass, str):
        raise ValueError("The string_sass must be str type. Given: {0}".format(type(string_sass)))

    elif not string_sass:
        raise ValueError("The string_sass is invalid. Given: {0}".format(string_sass))

    return ""


def sass_map_vars(string_sass):
    """Returns a dictionary with all the variables found with their respective values.

    :param string_sass: String with the sass code

    Example:
        >>> from phanterpwa.tools import sass_map_vars
        >>> sass_str = '''
        ... $BG: red
        ... $FG: green
        ... .my_class
        ...     background-color: $BG
        ...     color: $FG
        ... '''
        >>> sass_map_vars(sass_str)
        {'BG': 'red', 'FG': 'green'}
    """

    v = re.compile(r"^[\t ]*?(\$[A-Za-z_][A-Za-z0-9_\-]*\:{1}[ ]?[\w!#$%,\ .\-\(\)]+)\/*.*$", re.MULTILINE)
    r = v.findall(string_sass)
    d = {}
    for x in r:
        k, v = x.split(":")
        d[k.strip()[1:]] = v.strip()
    return d


def temporary_password(
        size: int = 8, chars: str = "abcdefghijlmnopqrstuvxzwykABCDEFGHIJLMNOPQRSTUVXZWYK0123456789") -> str:
    """Create a random sequence of characters.

    :param size: generated string size.
    :param chars: Characters that will be used to make the new string.

    Example:
        >>> from phanterpwa.tools import temporary_password
        >>> temporary_password()
        'j2LGe97s'
        >>> temporary_password(5)
        'OkPw7'
        >>> temporary_password(10, 'aeiou')
        'eioueauaiu'
    """

    if not (isinstance(size, int) and size > 0):
        raise ValueError("The size must be integer type and greater than 0")

    if not (isinstance(chars, str) and len(chars) > 2):
        raise ValueError("The chars must be string type and be at least 3 characters")

    import random
    len_chars = len(chars)
    matrix = chars
    p = []
    while len(p) < size:
        number = random.randint(0, len(matrix) - 1)
        char = matrix[number]
        if size <= len_chars:
            if char not in p:
                p.append(char)
        else:
            if p:
                if p[-1] != char:
                    p.append(char)
            else:
                p.append(char)
    f = "".join(p)
    return f


def app_name_from_relative_child(project_path, child_path):
    """Returns the application's folder name via a child folder

    :param project_path: Project path
    :child_path: Child folder of the project folder
    """
    apps_list_basedir = os.path.join(project_path, "frontapps")
    p = PurePath(child_path)
    r = p.relative_to(os.path.join(apps_list_basedir))
    return r.parts[0]


def generate_activation_code(size: int = 6) -> str:
    """Create a numeric code of predefined size with one character validator.

    :param size: generated string number size.

    Example:
        >>> from phanterpwa.tools import generate_activation_code
        >>> generate_activation_code()
        '425938-E'
        >>> generate_activation_code()
        '762093-A'
        >>> generate_activation_code(4)
        '3624-G'
    """

    if not (isinstance(size, int) and size > 0):
        raise ValueError("The size must be an integer and greater than 0")

    import random
    matrix = '0123456789'
    ver = "ABCDEFGHI"
    p = []
    su = 0
    while len(p) < size:
        number = random.randint(0, len(matrix) - 1)
        char = matrix[number]
        if char not in p:
            p.append(char)
            su += int(char)
            if su >= 9:
                su = su - 9
    f = "".join(p)
    return "-".join([f, ver[su]])


def check_activation_code(code: str, size: int = 6) -> (str, None):
    """Checks whether the string in the code parameter is a valid activation code

    :param size: Activation code size ignoring the check digit

    Example:
        >>> from phanterpwa.tools import (generate_activation_code, check_activation_code)
        >>> generate_activation_code()
        '425938-E'
        >>> check_activation_code('425938-E')
        '425938-E'
        >>> check_activation_code('INVALID_CODE')
        >>> print(check_activation_code('INVALID_CODE'))
        None
        >>> generate_activation_code(4)
        '3624-G'
        >>> check_activation_code('3624-G')
        >>> print(check_activation_code('3624-G'))
        None
        >>> check_activation_code('3624-G', 4)
        '3624-G'
    """

    if not (isinstance(size, int) and size > 0):
        raise ValueError("The size must be an integer and greater than 0")

    if not (isinstance(code, str) and len(code) > 2):
        raise ValueError("The chars must be an integer and be at least 3 characters")

    code = code.strip()
    if (len(code) == size + 2) and "-" in code:
        cod, dig = code.split("-")
        ver = "ABCDEFGHI"
        su = 0
        for char in cod:
            su += int(char)
            if su >= 9:
                su = su - 9
        if ver[su] == dig:
            return code


def config(cfg_file, dict_cfg=None, rewrite=False):
    """With this function it is possible to manipulate configuration files in json format, by default the file name is
    config.json

    :param cfg_file: path to the configuration file
    :param dict_cfg: dictionary with the values you want to add or change.
    :param rewrite: With this option the current file will be overwritten with the new settings added in the dict_cfg
        parameter

    Example:
        >>> from phanterpwa.tools import config
        >>> config("config.json", {"new_key": None})
        {'new_key': None}
        >>> with open("config.json") as f:
        ...     print(f.read())
        ...
        {
            "new_key": null
        }
        >>> config("config.json", {"new_key": False, "other_key": True})
        {'new_key': False, 'other_key': True}
        >>> with open("config.json") as f:
        ...     print(f.read())
        ...
        {
            "new_key": null,
            "other_key": true
        }
        >>> config("config.json", {"more_one_key": "Is it cumulative?"})
        {'new_key': False, 'other_key': True, 'more_one_key': "Is it cumulative?"}
        >>> with open("config.json") as f:
        ...     print(f.read())
        ...
        {
            "new_key": null,
            "other_key": true,
            "more_one_key": "Is it cumulative?"
        }
        >>> config("config.json", {"rewrite": "yes"}, True)
        {'rewrite': 'yes'}
        >>> with open("config.json") as f:
        ...     print(f.read())
        ...
        {
            "rewrite": "yes"
        }

    """
    if dict_cfg is None:
        dict_cfg = dict()

    if not isinstance(dict_cfg, dict):
        ValueError("The dict_cfg must be sict type. Given: {0}".format(type(dict_cfg)))

    if isinstance(cfg_file, str):
        if len(cfg_file) > 5:
            if cfg_file[-5:] != ".json":
                if os.path.exists(cfg_file) and os.path.isdir(cfg_file):
                    cfg_file = os.path.join(cfg_file, "config.json")
                else:
                    cfg_file = "".join([cfg_file, ".json"])
        else:
            if os.path.exists(cfg_file) and os.path.isdir(cfg_file):
                cfg_file = os.path.join(cfg_file, "config.json")
            else:
                cfg_file = "".join(cfg_file, ".json")
    else:
        raise ValueError("The arg 'cfg_file' must be strig. Given: {0}".format(type(cfg_file)))
    if os.path.exists(cfg_file) and not rewrite:
        cfg = None
        with open(cfg_file, 'r', encoding="utf-8") as f:
            cfg = json.load(f)
        if cfg and isinstance(cfg, dict):
            for x in dict_cfg:
                cfg[x] = dict_cfg[x]
        else:
            cfg = dict_cfg
    else:
        basedir = os.path.dirname(cfg_file)
        cfg = dict_cfg
        if basedir:
            os.makedirs(basedir, exist_ok=True)
    ncfg = dict(cfg)
    with open(cfg_file, "w", encoding="utf-8") as f:
        json.dump(ncfg, f, ensure_ascii=True, indent=2)
    return ncfg


def split_seconds(seconds: int) -> dict:
    """This function converts seconds into a dictionary by splitting seconds without year, month, day, hour, minute
    and second when possible.

    :param seconds: seconds that will be converted

    Example:
        >>> from phanterpwa.tools import split_seconds
        >>> split_seconds(123456789)
        {'year': 3, 'month': 11, 'day': 3, 'hour': 21, 'minute': 33, 'second': 9}
        >>> split_seconds(121)
        {'minute': 2, 'second': 1}
        >>> split_seconds(3659)
        {'hour': 1, 'second': 59}
    """

    if not isinstance(seconds, int):
        raise ValueError("The seconds must be an integer. Given: {0}".format(seconds))

    def s(seconds, d={}):
        d = dict(**d)
        if seconds >= 31536000:
            if seconds % 31536000:
                r = seconds % 31536000
                d['year'] = seconds // 31536000
                return s(r, d)
            else:
                d['year'] = seconds // 31536000
                return d
        else:
            if seconds >= 2592000:
                if seconds % 2592000:
                    r = seconds % 2592000
                    d['month'] = seconds // 2592000
                    return s(r, d)
                else:
                    d['month'] = seconds // 2592000
                    return d
            else:
                if seconds >= 86400:
                    if seconds % 86400:
                        r = seconds % 86400
                        d['day'] = seconds // 86400
                        return s(r, d)
                    else:
                        d['day'] = seconds // 86400
                        return d
                else:
                    if seconds >= 3600:
                        if seconds % 3600:
                            r = seconds % 3600
                            d['hour'] = seconds // 3600
                            return s(r, d)
                        else:
                            d['hour'] = seconds // 3600
                            return d
                    else:
                        if seconds >= 60:
                            if seconds % 60:
                                r = seconds % 60
                                d['minute'] = seconds // 60
                                return s(r, d)
                            else:
                                d['minute'] = seconds // 60
                                return d
                        else:
                            d['second'] = seconds
                            return d
    return s(seconds)


def join_seconds(splitted_seconds: dict) -> int:
    """Different from split_seconds, this function transforms a dictionary with the year, month, day, hour, minute and
    second keys with their respective values in seconds.
    
    :param splitted_seconds: dictionary with the year, month, day, hour, minute or
        second keys.

    Example:
        >>> from phanterpwa.tools import join_seconds
        >>> join_seconds({'year': 1, 'hour': 1, 'second': 1})
        31539601
        >>> join_seconds({'year': 1, 'second': 3601})
        31539601
        >>> join_seconds({'year': 1, 'minute': 60, 'second': 1})
        31539601
    """

    if isinstance(splitted_seconds, dict):
        total = 0
        if "year" in splitted_seconds:
            total += splitted_seconds["year"] * 60 * 60 * 24 * 365
        if "month" in splitted_seconds:
            total += splitted_seconds["month"] * 60 * 60 * 24 * 30
        if "day" in splitted_seconds:
            total += splitted_seconds['day'] * 60 * 60 * 24
        if "hour" in splitted_seconds:
            total += splitted_seconds['hour'] * 60 * 60
        if "minute" in splitted_seconds:
            total += splitted_seconds['minute'] * 60
        if "second" in splitted_seconds:
            total += splitted_seconds['second']
        return total
    else:
        raise ValueError("The splitted_seconds must be dict type. Given: {0}".format(type(splitted_seconds)))


def humanize_seconds(seconds: int, translator_instance: ("phanterpwa.i18n.Translator", None)=None) -> str:
    """Humanizes seconds by dividing between year, month, day, hour, minute and second when possible.

    :param seconds: seconds that will be humanized
    :param translator_instance: With this option it is possible to add an i18n instance to translate the return.

    Example:
        >>> from phanterpwa.tools import humanize_seconds
        >>> humanize_seconds(123456789)
        '3 years, 11 months, 3 days, 21 hours, 33 minutes and 9 seconds'
        >>> humanize_seconds(121)
        '2 minutes and 1 second'
        {'minute': 2, 'second': 1}
        >>> humanize_seconds(3659)
        '1 hour and 59 seconds'

        Using phanterpwa.i18n.Translator example

        >>> from phanterpwa.i18n import Translator
        >>> my_translator = Translator("test_path", "humanize_seconds")
        >>> my_translator.translate("pt-BR", "year", "ano")
        {"pt-BR": {"year": "ano"}}
        >>> my_translator.translate("pt-BR", "years", "anos")
        {"pt-BR": {"years": "anos"}}
        >>> my_translator.translate("pt-BR", "month", "mês")
        {"pt-BR": {"month": "mês"}}
        >>> my_translator.translate("pt-BR", "months", "meses")
        {"pt-BR": {"months": "meses"}}
        >>> my_translator.translate("pt-BR", "day", "dia")
        {"pt-BR": {"day": "dia"}}
        >>> my_translator.translate("pt-BR", "days", "dias")
        {"pt-BR": {"days": "dias"}}
        >>> my_translator.translate("pt-BR", "hour", "hora")
        {"pt-BR": {"hour": "hora"}}
        >>> my_translator.translate("pt-BR", "hours", "horas")
        {"pt-BR": {"hours": "horas"}}
        >>> my_translator.translate("pt-BR", "minute", "minuto")
        {"pt-BR": {"minute": "minuto"}}
        >>> my_translator.translate("pt-BR", "minutes", "minutos")
        {"pt-BR": {"minutes": "minutos"}}
        >>> my_translator.translate("pt-BR", "second", "segundo")
        {"pt-BR": {"second": "segundo"}}
        >>> my_translator.translate("pt-BR", "seconds", "segundos")
        {"pt-BR": {"seconds": "segundos"}}
        >>> my_translator.direct_translation = "pt-BR"
        >>> humanize_seconds(123456789, my_translator)
        '3 anos, 11 meses, 3 dias, 21 horas, 33 minutos and 9 segundo'
        >>> my_translator.direct_translation = "en-US"
        >>> humanize_seconds(123456789, my_translator)
        '3 years, 11 months, 3 days, 21 hours, 33 minutes and 9 seconds'
        >>> humanize_seconds(3659, my_translator)
        '1 hour and 59 seconds'
        >>> my_translator.direct_translation = "pt-BR"
        >>> humanize_seconds(3659, my_translator)
        '1 hora and 59 segundos'
        >>> my_translator.translate("pt-BR", "and ", "e ")
        >>> humanize_seconds(3659, my_translator)
        '1 hora e 59 segundos'
    """

    if translator_instance:
        from phanterpwa.i18n import Translator
        if not isinstance(translator_instance, Translator):
            raise ValueError("The translator_instance must be instance of phanterpwa.i18n.Translator or None")
    if not isinstance(seconds, int):
        raise ValueError("The seconds must be an integer. Given: {0}".format(seconds))

    result = split_seconds(seconds)
    s = ""
    ts_list = []
    if "year" in result:
        kunit = unit = "year"
        if result[kunit] > 1:
            unit = "".join([unit, "s"])
        if translator_instance:
            unit = translator_instance.T(unit)
        ts = "".join([str(result[kunit]), " ", unit, " "])
        ts_list.append(ts)
    if "month" in result:
        kunit = unit = "month"
        if result[kunit] > 1:
            unit = "".join([unit, "s"])
        if translator_instance:
            unit = translator_instance.T(unit)
        ts = "".join([str(result[kunit]), " ", unit, " "])
        ts_list.append(ts)
    if "day" in result:
        kunit = unit = "day"
        if result[kunit] > 1:
            unit = "".join([unit, "s"])
        if translator_instance:
            unit = translator_instance.T(unit)
        ts = "".join([str(result[kunit]), " ", unit, " "])
        ts_list.append(ts)
    if "hour" in result:
        kunit = unit = "hour"
        if result[kunit] > 1:
            unit = "".join([unit, "s"])
        if translator_instance:
            unit = translator_instance.T(unit)
        ts = "".join([str(result[kunit]), " ", unit, " "])
        ts_list.append(ts)
    if "minute" in result:
        kunit = unit = "minute"
        if result[kunit] > 1:
            unit = "".join([unit, "s"])
        if translator_instance:
            unit = translator_instance.T(unit)
        ts = "".join([str(result[kunit]), " ", unit, " "])
        ts_list.append(ts)
    if "second" in result:
        kunit = unit = "second"
        if result[kunit] > 1:
            unit = "".join([unit, "s"])
        if translator_instance:
            unit = translator_instance.T(unit)
        ts = "".join([str(result[kunit]), " ", unit, " "])
        ts_list.append(ts)
    if len(ts_list) > 1:
        cont = 0
        for x in ts_list[:-1]:
            if cont:
                s = ", ".join([s.strip(), x])
            else:
                s = "".join([s, x])
            cont += 1
        else:
            if translator_instance:
                s = translator_instance.T("and ").join([s, ts_list[-1].strip()])
            else:
                s = "and ".join([s, ts_list[-1].strip()])
    else:
        if ts_list:
            s = ts_list[0].strip()

    return s


def text_normalize(text: str, upper: bool = True):
    """"Remove the graphic accents of Latin languages"

    :param text: string that will be normalized
    :param upper: This parameter with the value True (default) the output will be capitalized

    Example:
        >>> from phanterpwa.tools import text_normalize
        >>> text_normalize("Maçã")
        'MACA'
        >>> text_normalize("Maçã", False)
        'Maca'

    """

    if upper:
        return normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').upper()
    else:
        return normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')


def string_escape(value):
    r"""Escapes the <,>, ", 'and & characters of a string, when adding an interactable object such as a list,
    a dictionary, tuples and a set it cycles through the values in search of strings recursively, remembering
    that objects of the type tuple and set will be converted to lists.

    :param value: string, dict, list, tuple or set.

    Example:
        >>> from phanterpwa.tools import string_escape
        >>> string_escape("<div>the content<\div>")
        '&lt;div&gt;the content&lt;\div&gt;'
        >>> result = string_escape({
            "one": "<div style='test'>one</div>",
            "two": ["<div>two</div>"],
            "three": ("<div>three</div>", ),
            "four": {"<div>four</div>"},
            "five": {
                "five_one": ["<br>", ("<input>", "<hr>"), {"<a href='link'></a>"}]
            }
        })
        >>> result["one"]
        '&lt;div style=&#39;test&#39;&gt;one&lt;/div&gt;'
        >>> result["two"]
        '["&lt;div&gt;two&lt;/div&gt;"]'
        >>> result["three"]
        '["&lt;div&gt;three&lt;/div&gt;"]'
        >>> result["four"]
        '['&lt;div&gt;four&lt;/div&gt;']'
        >>> result["five"]["five_one"]
        '["&lt;br&gt;", ["&lt;input&gt;", "&lt;hr&gt;"], ["&lt;a href=&#39;link&#39;&gt;&lt;/a&gt;"]]'

    """
    if isinstance(value, str):
        return escape.xhtml_escape(value)
    elif isinstance(value, (list, tuple, set)):
        new_list = []
        for x in value:
            new_list.append(string_escape(x))
        return new_list
    elif isinstance(value, dict):
        new_dict = {}
        for x in value.keys():
            new_dict[x] = string_escape(value[x])
        return new_dict
    elif isinstance(value, datetime):
        return value.isoformat(" ", "seconds")
    elif isinstance(value, date):
        return value.isoformat()
    else:
        return value


def one_space(value):
    """"Removes empty spaces, tabs and new lines from a string and adds a space between words when necessary.

    Example:
        >>> from phanterpwa.tools import one_space
        >>> one_space("   My    long \r\n text. \tTabulation,      spaces,     spaces.         ")
        'My long text. Tabulation, spaces, spaces.'


    """
    result = ""
    if isinstance(value, str):
        value = value.strip()
        value = value.replace("\n", " ").replace("\t", " ").replace("\r", " ")
        spl = value.split(" ")
        result = " ".join([x for x in spl if x])
    return result


def user_agent_parse(user_agent):
    if not isinstance(user_agent, str):
        return "Unknown (Unknown)"
    keys =[
        "Edg",
        "CrOS",
        "Linux",
        "Edge",
        "Chromium",
        "OpenBSD",
        "Waterfox",
        "Lumia",
        "Trident",
        "Nexus",
        "Opera",
        "Android",
        "PaleMoon",
        "BingPreview",
        "Fedora",
        "Ubuntu",
        "Mac OS X",
        "Firefox",
        "iPhone",
        "IEMobile",
        "Tablet",
        "Safari",
        "Instagram",
        "iPad",
        "MSIE",
        "X11",
        "SeaMonkey",
        "Iceweasel",
        "SAMSUNG",
        "Win64",
        "Windows",
        "Puffin",
        "Maxthon",
        "Chrome",
        "MacX11",
        "PhantomJS",
        "Mobile",
        "OPR",
        "PlayStation",
        "WOW64",
        "UCBrowser",
        "FB",
        "iPhone OS",
        "YaBrowser",
        "Redmi",
        "Konqueror",
        "Macintosh"
    ]
    tagx = set(keys)


    for_print = list()
    for y in tagx:
        if y.upper() in user_agent.upper():
            if y == "Trident" or y == "MSIE":
                if "MSIE" not in for_print:
                    for_print.append("MSIE")
            elif y == "WOW64" or y == "Win64" or y == "Windows":
                if "Windows" not in for_print:
                    for_print.append("Windows")
            else:
                for_print.append(y.strip())
    if for_print:
        change = False
        if "Windows" in for_print:
            for_print.pop(for_print.index("Windows"))
            for_print.append("(Windows)")
        if "iPhone OS" in for_print:
            if "iPhone OS" in for_print:
                for_print.pop(for_print.index("iPhone OS"))
            if "Mac OS X" in for_print:
                for_print.pop(for_print.index("Mac OS X"))
            if "Macintosh" in for_print:
                for_print.pop(for_print.index("Macintosh"))
            if "Safari" in for_print and "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            for_print.append("(iOS)")
        if "Mobile" in for_print:
            if "iPad" in for_print:
                for_print.pop(for_print.index("Mobile"))
                for_print.pop(for_print.index("iPad"))
                if "iPhone" in for_print:
                    for_print.pop(for_print.index("iPhone"))
                for_print.insert(0, "iPad")
            if "iPhone" in for_print:
                for_print.pop(for_print.index("Mobile"))
                for_print.pop(for_print.index("iPhone"))
                for_print.insert(0, "iPhone")
            if "Android" in for_print:
                for_print.pop(for_print.index("Mobile"))
                for_print.pop(for_print.index("Android"))
                if "Safari" in for_print:
                    for_print.pop(for_print.index("Safari"))
                if "Linux" in for_print:
                    for_print.pop(for_print.index("Linux"))
                for_print.append("(Android)")
        if "Android" in for_print:
            for_print.pop(for_print.index("Android"))
            if "Chrome" in for_print and "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Linux" in for_print:
                for_print.pop(for_print.index("Linux"))
            for_print.append("(Android)")           
        if "Edg" in for_print or "Edge" in for_print:
            if "Edg" in for_print:
                for_print.pop(for_print.index("Edg"))
            if "Edge" in for_print:
                for_print.pop(for_print.index("Edge"))
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            for_print.insert(0, "Edge")         
        if "X11" in for_print and "Linux" in for_print:
            for_print.pop(for_print.index("X11"))
            for_print.pop(for_print.index("Linux"))
            for_print.append("(Linux)")
        if "X11" in for_print and "CrOS" in for_print:
            for_print.pop(for_print.index("X11"))
            for_print.pop(for_print.index("CrOS"))
            for_print.append("(ChromeOS)")
        if "X11" in for_print and "OpenBSD" in for_print:
            for_print.pop(for_print.index("X11"))
            for_print.pop(for_print.index("OpenBSD"))
            for_print.append("(OpenBSD)")

        if "Chromium" in for_print:
            change=True
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Chromium" in for_print:
                for_print.pop(for_print.index("Chromium"))
            for_print.insert(0, "Chromium")

        if "Macintosh" in for_print or "Mac OS X" in for_print:
            if "Mac OS X" in for_print:
                for_print.pop(for_print.index("Mac OS X"))
            if "Macintosh" in for_print:
                for_print.pop(for_print.index("Macintosh"))
            if "Safari" in for_print and "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            for_print.append("(Mac OS X)")
        if "Safari" in for_print and "Chrome" in for_print:
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
        if "OPR" in for_print or "Opera" in for_print:
            if "OPR" in for_print:
                for_print.pop(for_print.index("OPR"))
            if "Opera" in for_print:
                for_print.pop(for_print.index("Opera"))
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            for_print.insert(0, "Opera")
        if "Nexus" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "PhantomJS" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "Maxthon" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "Puffin" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "SeaMonkey" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "SAMSUNG" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "BingPreview" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "PaleMoon" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "Iceweasel" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "PhantomJS" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "UCBrowser" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "YaBrowser" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "Instagram" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "Waterfox" in for_print:
            if "Chrome" in for_print:
                for_print.pop(for_print.index("Chrome"))
            if "Safari" in for_print:
                for_print.pop(for_print.index("Safari"))
            if "Firefox" in for_print:
                for_print.pop(for_print.index("Firefox"))
        if "Lumia" in for_print:

            for_print.pop(for_print.index("Lumia"))
            if "Mobile" in for_print:
                for_print.pop(for_print.index("Mobile"))
            if "IEMobile" in for_print and "MSIE" in for_print:
                for_print.pop(for_print.index("IEMobile"))
            for_print.insert(0, "Lumia")
        if "Redmi" in for_print:
            for_print.pop(for_print.index("Redmi"))
            for_print.insert(0, "Redmi")
        if "Tablet" in for_print:
            if "Tablet" in for_print:
                for_print.pop(for_print.index("Tablet"))
            for_print.insert(0, "Tablet")
        if "Linux" in for_print:
            for_print.pop(for_print.index("Linux"))
            for_print.append("(Linux)")
        if "FB" in for_print:
            for_print[for_print.index("FB")] = "Facebook"
        return " ".join([z for z in for_print])
    else:
        return "Unknown (Unknown)"


def checkbox_bool(value):
    if str(value).upper() in ["TRUE", "ON"]:
        return True
    else:
        return False


def normalize_names(name, not_captilize=[]):
    return " ".join([
        x if x in not_captilize or len(x) < 3 else x.capitalize() for x in name.lower().strip().split(" ") if x])


class WatchingFiles():
    def __init__(self, path_monitoring, path_destiny, ignore_paths=["__pycache__"]):
        self.path_monitoring = path_monitoring
        self.path_destiny = path_destiny
        self.ignore_paths = ignore_paths
        self._dirs = dict()
        self._files = dict()
        self._create_mtime_list()

    @property
    def path_monitoring(self):
        return self._path_monitoring

    @path_monitoring.setter
    def path_monitoring(self, value):
        if os.path.isdir(value):
            self._path_monitoring = value
        else:
            raise IOError("The path \"{0}\" not exists!".format(value))

    def _create_mtime_list(self):
        print("Checking files modified at source\n")
        self._dirs = dict()
        self._files = dict()
        destiny_dirs = []
        destiny_files = []

        for x in os.walk(self.path_monitoring):
            p = PurePath(x[0])
            if not set(p.parts).intersection(set(self.ignore_paths)):
                df = os.path.normpath(os.path.join(self.path_destiny, p.relative_to(self.path_monitoring)))
                self._dirs[x[0]] = [os.path.getmtime(x[0]), df]
                for y in x[2]:
                    f = os.path.normpath(os.path.join(x[0], y))
                    d = os.path.normpath(os.path.join(self.path_destiny, p.relative_to(self.path_monitoring), y))
                    self._files[
                        f
                    ] = [os.path.getmtime(f), d]
                    if os.path.isfile(d):
                        if os.path.getmtime(f) != os.path.getmtime(d):
                            print("Was Modify: {0}\nCoping {0} to {1}".format(f, d))
                            shutil.copy2(f, d)

        if os.path.isdir(self.path_destiny):
            for x in os.walk(self.path_destiny):
                p = PurePath(x[0])
                if not set(p.parts).intersection(set(self.ignore_paths)):
                    df = os.path.normpath(os.path.normpath(x[0]))
                    destiny_dirs.append(df)
                    for y in x[2]:
                        d = os.path.normpath(os.path.join(x[0], y))
                        destiny_files.append(d)
        diff_dir = set(destiny_dirs).difference(set([self._dirs[x][1] for x in self._dirs.keys()]))
        diff_fil = set(destiny_files).difference(set([self._files[x][1] for x in self._files.keys()]))
        if diff_dir:
            for tt in diff_dir:
                if os.path.isdir(tt):
                    print("Deleting {0}".format(tt))
                    try:
                        shutil.rmtree(tt)
                    except OSError as e:
                        print("Error: %s - %s." % (e.filename, e.strerror))
                        pass
                    while os.path.exists(tt):
                        pass
        if diff_fil:
            for ff in diff_fil:
                if os.path.isfile(ff):
                    print("Deleting {0}".format(ff))
                    try:
                        os.unlink(ff)
                    except OSError as e:
                        print("Error: %s - %s." % (e.filename, e.strerror))
                        pass
                    while os.path.exists(ff):
                        pass

    def monitoring(self):
        print("Starting WatchingFiles...")
        while True:
            dirs_delete = dict(self._dirs)
            files_delete = dict(self._files)
            for x in os.walk(self.path_monitoring):
                p = PurePath(x[0])
                if not set(p.parts).intersection(set(self.ignore_paths)):
                    df = os.path.normpath(os.path.join(self.path_destiny, p.relative_to(self.path_monitoring)))
                    self._dirs[x[0]] = [os.path.getmtime(x[0]), df]
                    if x[0] in dirs_delete:
                        del dirs_delete[x[0]]
                    if not os.path.isdir(df):
                        os.makedirs(df, exist_ok=True)
                        print("Creating Destiny Dirs: {0}".format(df))
                    for y in x[2]:
                        f = os.path.normpath(os.path.join(x[0], y))
                        d = os.path.normpath(os.path.join(self.path_destiny, p.relative_to(self.path_monitoring), y))
                        if f in files_delete:
                            del files_delete[f]
                        if f not in self._files:
                            self._files[
                                f
                            ] = [os.path.getmtime(f), d]
                            print("New File: {0}\nCoping {0} to {1}".format(f, d))
                            shutil.copy2(f, d)
                        else:
                            if self._files[f][0] != os.path.getmtime(f):
                                self._files[
                                    f
                                ] = [os.path.getmtime(f), d]
                                print("Was Modify: {0}\nCoping {0} to {1}".format(f, d))
                                shutil.copy2(f, d)
                            elif not os.path.isfile(d):
                                shutil.copy2(f, d)
                                print("Not Found: {1}\nCoping {0} to {1}".format(f, d))
            if dirs_delete:
                print("Deleting dirs:", dirs_delete)

                for dd in tuple(dirs_delete.keys()):
                    target = dirs_delete[dd][1]
                    print(target)
                    if os.path.isdir(target):
                        try:
                            shutil.rmtree(target)
                        except OSError as e:
                            print("Error: %s - %s." % (e.filename, e.strerror))
                            pass
                        while os.path.exists(target):
                            pass
                        del dirs_delete[dd]
                        del self._dirs[dd]
                    else:
                        del dirs_delete[dd]
                        del self._dirs[dd]

            if files_delete:
                print("Deleting files:", files_delete)

                for ff in tuple(files_delete.keys()):
                    target = files_delete[ff][1]
                    print(target)
                    if os.path.isfile(target):
                        try:
                            os.unlink(target)
                        except OSError as e:
                            print("Error: %s - %s." % (e.filename, e.strerror))
                            pass
                        while os.path.exists(target):
                            pass
                        del files_delete[ff]
                        del self._files[ff]
                    else:
                        del files_delete[ff]
                        del self._files[ff]
            time.sleep(1)

