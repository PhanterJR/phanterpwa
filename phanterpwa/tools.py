# -*- coding: utf-8 -*-
import re
import os
import sys
import json
import shutil
import importlib
import subprocess
import tempfile
import sass
from passlib.hash import pbkdf2_sha512
from glob import glob
from pathlib import PurePath
from phanterpwa.samples.project_config_sample import project_config_sample
from pydal import Field


def interpolate(xstring, context, delimiters=["{{", "}}"], ignore_non_strings=False):
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


def sass_change_vars(string_sass, variables={}):
    ns = ""
    if all([isinstance(variables, dict), isinstance(string_sass, str), variables, string_sass]):
        lines = string_sass.split('\n')
        for x in lines:
            find = False
            for y in variables:
                v = "".join(["$", y, ":"])
                if v in x:
                    ini = x.index(v)
                    ns = "".join([ns, x[:ini], v, " ", variables[y], "\n"])
                    find = True
                    break
            if not find:
                ns = "".join([ns, x, "\n"])

        return ns[:-1]


def sass_map_vars(string_sass):
    v = re.compile(r"^[\t ]*?(\$[A-Za-z_][A-Za-z0-9_\-]*\:{1}[ ]?[\w!#$%,\ .\-\(\)]+)\/*.*$", re.MULTILINE)
    r = v.findall(string_sass)
    d = {}
    for x in r:
        k, v = x.split(":")
        d[k.strip()[1:]] = v.strip()
    return d


def temporary_password():
    import random
    matrix = 'abcdefghijlmnopqrstuvxzwykABCDEFGHIJLMNOPQRSTUVXZWYK0123456789'
    password = []
    while len(password) < 8:
        number = random.randint(0, len(matrix) - 1)
        char = matrix[number]
        if char not in password:
            password.append(char)
    final_password = "".join(password)
    return final_password


def activation_code(size=6):
    import random
    matrix = '0123456789'
    ver = "ABCDEFGHI"
    password = []
    su = 0
    while len(password) < size:
        number = random.randint(0, len(matrix) - 1)
        char = matrix[number]
        if char not in password:
            password.append(char)
            su += int(char)
            if su >= 9:
                su = su - 9
    final_password = "".join(password)
    return "-".join([final_password, ver[su]])


def check_activation_code(code, size=6):
    if isinstance(code, str):
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


def check_valid_project_config(config_file) -> dict:
    if os.path.exists(config_file) and os.path.isfile(config_file):
        try:
            with open(config_file, 'r', encoding="utf-8") as f:
                cfg = json.load(f)
        except json.JSONDecodeError as e:
            raise e("Error on json decode the '{0}' config file. Error: {1}".format(config_file, e))
        else:
            for x in project_config_sample:
                if x not in cfg:
                    raise KeyError("The config file not is valid, not found the '{0}' key, it's required".format(x))
                    for y in project_config_sample[x]:
                        if y not in cfg[x]:
                            raise KeyError("".join(["The config file not is valid,",
                                " not found the '{0}' subkey of key '{1}' , it's required".format(y, x)]))
            else:
                return config_file
    else:
        print("The '{0}' is not valid config file! Not exists or not is file.".format(config_file))
    return {}


def list_installed_applications(path_applications):
    g = glob(os.path.join(path_applications, "*"))
    apps = {}
    for y in [x for x in g if os.path.isdir(x)]:
        cfg = os.path.join(y, "config.json")
        if check_valid_project_config(cfg):
            n = os.path.basename(y)
            j = ""
            with open(cfg, 'r', encoding='utf-8') as f:
                j = json.load(f)
            if j:
                if "PATH" in j:
                    if isinstance(j['PATH'], dict):
                        if 'project' in j['PATH']:
                            if j['PATH']['project'] != y:
                                j['PATH']['project'] = y
                        if 'api' in j['PATH']:
                            if j['PATH']['api'] != os.path.join(y, "api"):
                                j['PATH']['api'] = os.path.join(y, "api")
                        if 'app' in j['PATH']:
                            if j['PATH']['app'] != os.path.join(y, "app"):
                                j['PATH']['app'] = os.path.join(y, "app")
                        with open(cfg, 'w', encoding='utf-8') as fw:
                            json.dump(j, fw, ensure_ascii=False, indent=2)
                    apps[n] = j
    if not apps:
        print("Don't find installed apps on {0}".format(path_applications))
    return apps


def config(cfg_file, dict_cfg={}, rewrite=False):
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
    with open(cfg_file, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=True, indent=2)
    if "CONFIG_INDENTIFY" in cfg and cfg["CONFIG_INDENTIFY"] == "project_config":
        if cfg["PROJECT"]["packaged"] is True:
            path_app = os.path.normpath(os.path.join(os.path.dirname(cfg_file)))
            with open(cfg_file, "r", encoding="utf-8") as n:
                string_file = n.read()
                string_file = interpolate(string_file, context={"PROJECT_FOLDER": re.escape(path_app)})
                cfg = json.loads(string_file)
                cfg["PROJECT"]["packaged"] = False
            with open(cfg_file, "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=True, indent=2)
    return cfg


def url_pattern_relative_paths(path_base, file_search="*.html"):
    base = os.path.normpath(path_base)
    p = os.path.join(base, "**", file_search)
    b = []
    pattern = ""
    for x in glob(p, recursive=True):
        f = os.path.relpath(
            os.path.split(os.path.normpath(x))[0],
            start=base
        )
        if all([f != ".", f not in b]):
            b.append(f)

            f = f.replace("\\", "/")

            if pattern:
                pattern = "|".join([pattern, re.escape(f)])
            else:
                pattern = "".join(["(", re.escape(f)])
    if pattern:
        return "".join([pattern, ")"])


def create_transcrypt_config(project_path, keys=["PROJECT", "CONFIGJS"]):
    appConfig = config(project_path)
    target = appConfig['TRANSCRYPT']['main_files']
    targets = []
    if isinstance(target, list):
        t = set()
        for x in set(target):
            t.add(os.path.normpath(os.path.dirname(x)))
        targets = list(t)
    else:
        targets.append(os.path.dirname(target))
    CONFIG = {}
    for x in keys:
        CONFIG[x] = appConfig[x]
    ini = "\n".join([
        "# Created automatically.",
        "#",
        "# In development it may be necessary to add static data",
        "# to the client side application after compiling, use",
        "# the CONFIGJS section of the application's config.json",
        "# file for this.",
        "#",
        "\n\nfrom org.transcrypt.stubs.browser import __pragma__\n\n",
        "__pragma__('jsiter')",
        "\n"
    ])
    end = "\n__pragma__('nojsiter')\n"
    for ta in targets:
        with open(os.path.join(ta, "config.py"), 'w', encoding="utf-8") as f:
            content = "".join([ini, "CONFIG = {0}".format(json.dumps(CONFIG, ensure_ascii=True, indent=2)), end])
            content = content.replace('true', 'True').replace('false', 'False').replace('null', 'None')
            f.write(content)


def splits_seconds(seconds, d={}):
    d = dict(**d)
    if seconds >= 31536000:
        if seconds % 31536000:
            r = seconds % 31536000
            d['year'] = seconds // 31536000
            return splits_seconds(r, d)
        else:
            d['year'] = seconds // 31536000
            return d
    else:
        if seconds >= 2592000:
            if seconds % 2592000:
                r = seconds % 2592000
                d['month'] = seconds // 2592000
                return splits_seconds(r, d)
            else:
                d['month'] = seconds // 2592000
                return d
        else:
            if seconds >= 86400:
                if seconds % 86400:
                    r = seconds % 86400
                    d['day'] = seconds // 86400
                    return splits_seconds(r, d)
                else:
                    d['day'] = seconds // 86400
                    return d
            else:
                if seconds >= 3600:
                    if seconds % 3600:
                        r = seconds % 3600
                        d['hour'] = seconds // 3600
                        return splits_seconds(r, d)
                    else:
                        d['hour'] = seconds // 3600
                        return d
                else:
                    if seconds >= 60:
                        if seconds % 60:
                            r = seconds % 60
                            d['minute'] = seconds // 60
                            return splits_seconds(r, d)
                        else:
                            d['minute'] = seconds // 60
                            return d
                    else:
                        d['second'] = seconds
                        return d


def join_seconds(splits_seconds):
    total = 0
    if "year" in splits_seconds:
        total += splits_seconds["year"] * 60 * 60 * 24 * 365
    if "month" in splits_seconds:
        total += splits_seconds["month"] * 60 * 60 * 24 * 30
    if "day" in splits_seconds:
        total += splits_seconds['day'] * 60 * 60 * 24
    if "hour" in splits_seconds:
        total += splits_seconds['hour'] * 60 * 60
    if "minute" in splits_seconds:
        total += splits_seconds['minute'] * 60
    if "second" in splits_seconds:
        total += splits_seconds['second']
    return total


def humanize_seconds(seconds, translator_instance=None):
    result = splits_seconds(seconds)
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


def delete_compiled_app_folder(project_path):
    appConfig = config(project_path)
    target = appConfig['APP']['compiled_app_folder']
    if os.path.exists(target) and os.path.isdir(target):
        shutil.rmtree(target)


def copy_statics(project_path):
    appConfig = config(project_path)
    target = os.path.join(appConfig['APP']['compiled_app_folder'], "static")
    source = os.path.join(appConfig['PATH']['app'], "statics")
    version = appConfig['PROJECT']['version']
    if os.path.exists(target) and os.path.isdir(target):
        shutil.rmtree(target)
    shutil.copytree(
        source,
        os.path.join(target, version)
    )


def copy_languages(project_path):
    appConfig = config(project_path)
    version = appConfig['PROJECT']['version']
    source = os.path.join(appConfig['PATH']['app'], "languages")
    target = os.path.join(appConfig['APP']['compiled_app_folder'], "static", version, "languages")
    debug = appConfig['PROJECT']['debug']
    if not os.path.exists(target):
        os.makedirs(
            os.path.join(target), exist_ok=True
        )
    langs = glob(os.path.join(source, "*.json"))
    for x in langs:
        with open(x, "r", encoding='utf-8') as f:
            c = json.load(f)
            lang_file = os.path.join(target, os.path.basename(x))
            with open(lang_file, "w", encoding='utf-8') as o:
                if debug:
                    json.dump(c, o, ensure_ascii=False, indent=2)
                else:
                    json.dump(c, o, ensure_ascii=False)


def compile_styles(project_path):
    appConfig = config(project_path)
    version = appConfig['PROJECT']['version']
    source = os.path.join(appConfig['PATH']['app'], "styles")
    target = os.path.join(appConfig['APP']['compiled_app_folder'], "static", version, "css")
    list_sass = glob(os.path.join(source, "*"))
    debug = appConfig['PROJECT']['debug']
    exclude = ["__pycache__", "__init__.py"]
    for s in list_sass:
        os.makedirs(
            os.path.join(
                target), exist_ok=True)
        if os.path.isfile(s) and s[-5:] == ".sass":
            print("compiling Sass to Css: {0}".format(s))
            with open(s, "r") as f:
                filename = os.path.basename(s)[0:-5]
                c = ""
                temp_c = f.readlines()
                for t in temp_c:
                    if t[0:12] == "$app-version":
                        t = "$app-version: {0}\n".format(version)
                    c = "".join([c, t])
                if debug:
                    new_css = "".join([sass.compile(string=c, indented=True, output_style="expanded"), "\n"])
                else:
                    new_css = sass.compile(string=c, indented=True, output_style="compressed")
                with open(
                    os.path.join(
                        target, "{0}.css".format(filename)), "w") as o:
                    o.write(new_css)
        elif os.path.isdir(s) and s not in exclude:
            n_list_sass = glob(os.path.join(s, "*.sass"))
            filename = os.path.split(s)[-1]
            pre_c = ""
            for n in n_list_sass:
                with open(n, "r") as f:
                    c = ""
                    temp_c = f.readlines()
                    for t in temp_c:
                        if t[0:12] == "$app-version":
                            t = "$app-version: {0}\n".format(version)
                        c = "".join([c, t])
                    pre_c = "".join([pre_c, c, "\n"])
            print("compiling Sass to Css: %s" % os.path.join(s, "{0}.css".format(filename)))
            if debug:
                new_css = sass.compile(string=pre_c, indented=True, output_style="expanded")
            else:
                new_css = sass.compile(string=pre_c, indented=True, output_style="compressed")
            with open(
                os.path.join(
                    target, "{0}.css".format(filename)), "w") as o:
                o.write(new_css)


def compile_views(project_path):
    appConfig = config(project_path)
    sys.path.append(project_path)
    os.chdir(project_path)
    debug = appConfig['PROJECT']['debug']
    target = appConfig['APP']['compiled_app_folder']
    source = os.path.join(appConfig['PATH']['app'], "views")

    def _compile_html(file, base="", ignore=["__init__.py"]):
        if os.path.isfile(file) and os.path.basename(file) not in ignore and file[-3:] == ".py":
            print("compiling Python to html: %s" % file)
            i_mod = "%s" % (os.path.basename(file)[0:-3])
            if base:
                i_mod = "%s.%s" % (base, i_mod)
            i = importlib.import_module(i_mod)
            importlib.reload(i)
            name = "".join([*i_mod.split(".")[-1], ".html"])
            files_www = os.path.join(target, *i_mod.split(".")[2:-1])
            if not os.path.exists(os.path.join(files_www)):
                try:
                    os.makedirs(os.path.join(files_www), exist_ok=True)
                except OSError as e:
                    raise e("Problem on create folder '{0}'.".format(os.path.join(files_www)))
            new_folder = os.path.join(files_www)
            with open(
                os.path.join(new_folder, name),
                "wt",
                encoding="utf-8"
            ) as f:
                if debug:
                    f.write(i.html.humanize())
                else:
                    f.write(i.html.xml())

    def _compile_htmls(source, base=""):
        # htmls to www
        list_all = glob(os.path.join(source, "*"))
        for x in list_all:
            if os.path.isdir(x) and not os.path.basename(x) == "__pycache__":
                if base:
                    new_base = "%s.%s" % (base, os.path.basename(x))
                    _compile_htmls(x, new_base)
            elif os.path.isfile(x):
                _compile_html(x, base=base)

    _compile_htmls(source, "app.views")


def compile_scripts(project_path, ignore=["__init__.py"]):
    appConfig = config(project_path)
    main_files = appConfig['TRANSCRYPT']['main_files']
    targets = []
    if isinstance(main_files, list):
        t = set()
        for x in set(main_files):
            t.add(os.path.normpath(x))
        targets = list(t)
    else:
        targets.append(os.path.normpath(main_files))

    version = appConfig['PROJECT']['version']
    python_env = appConfig['ENVIRONMENT']['python']
    debug = appConfig['PROJECT']['debug']
    for ta in targets:
        source = os.path.join(os.path.dirname(ta), "__target__")
        path_name = os.path.basename(os.path.dirname(ta))
        target = os.path.join(
            appConfig['APP']['compiled_app_folder'], "static", version, "js", "transcrypt", path_name
        )
        print("compiling Python to Javascript: %s" % ta)
        if not os.path.exists(target):
            os.makedirs(target, exist_ok=True)
        if debug:
            subprocess.run("%s -m transcrypt %s -n -m" % (python_env, ta), shell=True)
        else:
            subprocess.run("%s -m transcrypt %s -m" % (python_env, ta), shell=True)
        list_all = glob(os.path.join(source, "*"))
        for x in list_all:
            if os.path.isfile(x):
                script_file = os.path.join(
                    target, os.path.basename(x)
                )
                shutil.copy(
                    x,
                    script_file
                )
    print("Finish compiling scripts")


def generate_script_importing_transcrypt_module(project_path: dict) -> list:
    appConfig = config(project_path)
    base = os.path.join(appConfig['PATH']['app'], "scripts")
    main_files = appConfig['TRANSCRYPT']['main_files']
    version = appConfig['PROJECT']['version']
    targets = []
    if isinstance(main_files, list):
        t = set()
        for x in set(main_files):
            t.add(os.path.normpath(x))
        targets = list(t)
    else:
        targets.append(os.path.normpath(main_files))
    res = []
    for x in targets:
        p = PurePath(x)
        p = p.relative_to(base)
        p.parts
        rel = "/".join(p.parts)
        rel = rel.replace("\\", "/")
        cod = interpolate(
            "<script type=\"module\">import * as application from '/static/{{VERSION}}/js/transcrypt/{{FILE}}'</script>",
            context={'VERSION': version, 'FILE': "{0}.js".format(rel[:-3])}
        )
        res.append(cod)
    return res


def package_project_app(project_path, target):
    appConfig = config(project_path)
    appConfig['ENVIRONMENT']['path'] = ""
    appConfig['ENVIRONMENT']['python'] = ""
    appConfig['PROJECT']['packaged'] = True
    appConfig['APP']['compiled_app_folder'] = "{{PROJECT_FOLDER}}\\app\\www"
    appConfig['PATH']['project'] = '{{PROJECT_FOLDER}}'
    appConfig['PATH']['api'] = '{{PROJECT_FOLDER}}\\api'
    appConfig['PATH']['app'] = '{{PROJECT_FOLDER}}\\app'
    appConfig['TRANSCRYPT']['main_files']
    file_name = os.path.basename(project_path)
    temp_main_files = []
    for t in appConfig['TRANSCRYPT']['main_files']:
        p = PurePath(t)
        p = p.relative_to(project_path)
        rel = "\\".join([r'{{PROJECT_FOLDER}}', *p.parts])
        temp_main_files.append(rel)
    appConfig['TRANSCRYPT']['main_files'] = temp_main_files
    compact_temp = os.path.join(tempfile.gettempdir(), 'phanterpwa')
    temp_file = os.path.join(compact_temp, file_name)
    os.makedirs(compact_temp, exist_ok=True)
    if os.path.exists(temp_file):
        shutil.rmtree(temp_file)
    shutil.copytree(
        project_path,
        temp_file
    )
    with open(os.path.join(temp_file, "config.json"), "w", encoding="utf-8") as f:
        json.dump(appConfig, f, ensure_ascii=True, indent=2)
    if os.path.exists(os.path.join(temp_file, "app", "www")):
        shutil.rmtree(os.path.join(temp_file, "app", "www"))
    if os.path.exists(os.path.join(temp_file, "logs")):
        shutil.rmtree(os.path.join(temp_file, "logs"))

    os.makedirs(os.path.join(temp_file, "app", "www"), exist_ok=True)
    os.makedirs(os.path.join(temp_file, "logs"), exist_ok=True)

    shutil.make_archive(os.path.join(os.path.join(compact_temp), file_name), 'zip', temp_file)
    shutil.copyfile(
        os.path.join(compact_temp, "{0}.zip".format(file_name)),
        os.path.join(target, "{0}.ppwa".format(file_name))
    )


def compiler(projectPath):
    delete_compiled_app_folder(projectPath)
    create_transcrypt_config(projectPath)
    copy_statics(projectPath)
    copy_languages(projectPath)
    compile_styles(projectPath)
    compile_views(projectPath)
    compile_scripts(projectPath)


def generate_password_hash(password):
    hash = pbkdf2_sha512.hash(password)
    return hash


def check_password_hash(password, hash):
    return pbkdf2_sha512.verify(hash, password)


class CheckDictOnFieldsDAL(object):

    def __init__(self, dict_args, *fields):
        super(CheckDictOnFieldsDAL, self).__init__()
        self.dict_args = dict_args
        self.fields = fields
        self._errors = {}
        self._verified = {}
        self._ignored = {}

    @property
    def errors(self):
        self.validate()
        return self._errors

    @property
    def dict_args(self):
        return self._dict_args

    @dict_args.setter
    def dict_args(self, dict_args):
        if isinstance(dict_args, dict):
            self._dict_args = dict_args
        else:
            raise TypeError(
                "The dict_args must be flaks.dict_args object. given: %s" % type(dict_args)
            )

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, list_fields):
        for x in list_fields:
            if not isinstance(x, Field):
                raise TypeError(
                    "The fields must be pydal.Field object. given: %s" % type(x)
                )
        self._fields = list_fields

    @property
    def verified(self):
        self.validate()
        return self._verified

    @property
    def ignored(self):
        self.validate()
        return self._ignored

    def validate(self):
        self._errors = {}
        self._verified = {}
        self._ignored = {}
        for f in self.dict_args:
            ig = True
            for F in self.fields:
                if F.name == f:
                    ig = False
                    result = F.validate(self.dict_args[f])
                    if result[1] is not None:
                        self._errors[f] = result[1]
                    else:
                        self._verified[f] = self.dict_args[f]
            if ig:
                self._ignored[f] = self.dict_args[f]

        if self._errors:
            return self._errors

    def validate_and_insert(self, dbtable, commit=True):
        self.validate()
        if not self.errors:
            rep = dbtable.validate_and_insert(**self.verified)
            dbtable._db._adapter.reconnect()
            if rep.errors:
                dbtable._db.rollback()
            elif rep.id and commit:
                dbtable._db.commit()
            return rep

    def validate_and_update(self, dbtable, commit=True):
        self.validate()
        if not self.errors:
            rep = dbtable.validate_and_insert(**self.verified)
            dbtable._db._adapter.reconnect()
            if rep.errors:
                dbtable._db.rollback
            elif rep.id and commit:
                dbtable._db.commit()
            return rep


if __name__ == '__main__':
    package_project_app("D:\\Nova_pasta\\PhanterPWA", "D:\\Nova_pasta")
