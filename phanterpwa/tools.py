# -*- coding: utf-8 -*-
import re
import os
import json
import shutil
import tempfile
from passlib.hash import pbkdf2_sha512
from glob import glob
from pathlib import PurePath
from pydal.objects import (Set, Table, Field)
from urllib.parse import quote
from unicodedata import normalize
from phanterpwa.samples import project_config_sample


def file_name(name, encoding="utf-8"):
    return quote(name, encoding=encoding)


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
    p = []
    while len(p) < 8:
        number = random.randint(0, len(matrix) - 1)
        char = matrix[number]
        if char not in p:
            p.append(char)
    f = "".join(p)
    return f


def generate_activation_code(size=6):
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
        raise RuntimeError("The '{0}' is not valid config file! Not exists or not is file.".format(config_file))
    return {}


def list_installed_projects(path_project):
    g = glob(os.path.join(path_project, "*"))
    apps = {}
    for y in [x for x in g if os.path.isdir(x)]:
        cfg = os.path.join(y, "config.json")
        try:
            check_valid_project_config(cfg)
        except Exception:
            print("Not a valid project folder:", y)
        else:
            print(y, "pass")
            n = os.path.basename(y)
            j = ""
            with open(cfg, 'r', encoding='utf-8') as f:
                j = json.load(f)
            if j:
                j['PROJECT']['path'] = y
                with open(cfg, 'w', encoding='utf-8') as fw:
                    json.dump(j, fw, ensure_ascii=False, indent=2)
                apps[n] = j
    if not apps:
        print("Don't find installed projects on {0}".format(path_project))
    return apps


def list_installed_apps(path_project):
    apps = {}
    cfg = os.path.join(path_project, "config.json")
    try:
        check_valid_project_config(cfg)
    except Exception:
        print("Not a valid project folder:", path_project)
    else:
        print(path_project, "pass")
        j = ""
        with open(cfg, 'r', encoding='utf-8') as f:
            j = json.load(f)
        if j and j["APPS"]:
            change = False
            for p in glob(os.path.join(j['PROJECT']['path'], "apps", "*")):
                app_name = os.path.split(p)[-1]
                if all([os.path.isdir(p),
                        os.path.isdir(os.path.join(p, "sources", "styles")),
                        os.path.isdir(os.path.join(p, "sources", "templates")),
                        os.path.isdir(os.path.join(p, "sources", "transcrypts")),
                        os.path.isdir(os.path.join(p, "statics"))]):
                    if not j["APPS"].get(app_name, None):
                        change = True
                        j["APPS"][app_name] = {
                            "build_folder": os.path.join(p, "www"),
                            "timeout_to_resign": 600,
                            "host": "0.0.0.0",
                            "port": j["API"]["port"] + 1,
                            "transcrypt_main_file": "application",
                            "styles_main_file": "application",
                            "views_main_file": "application"
                        }
                    apps[app_name] = j["APPS"][app_name]
            if change:
                with open(cfg, 'w', encoding='utf-8') as fw:
                    json.dump(j, fw, ensure_ascii=False, indent=2)
    if not apps:
        print("Don't find installed apps on {0}".format(os.path.join(path_project, "apps")))
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


# def create_transcrypt_config(project_path, keys=["PROJECT", "CONFIGJS"]):
#     appConfig = config(project_path)
#     appConfig['PROJECT']['compilation'] += 1
#     with open(os.path.join(project_path, "config.json"), "w", encoding="utf-8") as f:
#         json.dump(appConfig, f, ensure_ascii=True, indent=2)
#     apps_list = appConfig.get("APPS")
#     apps_list_basedir = os.path.join(appConfig['PROJECT']['path'], "apps")
#     if apps_list and apps_list_basedir:
#         for x in apps_list:
#             CONFIG = {'PROJECT': {}, 'CONFIGJS': {}}

#             CONFIG['PROJECT'] = appConfig['PROJECT']
#             CONFIG['CONFIGJS']['api_server_address'] = appConfig['API']['remote_address']
#             CONFIG['CONFIGJS']['api_websocket_address'] = appConfig['API']['websocket_address']
#             CONFIG['CONFIGJS']['timeout_to_resign'] = apps_list[x]['timeout_to_resign']
#             ini = "\n".join([
#                 "# Created automatically.",
#                 "#",
#                 "# In development it may be necessary to add static data",
#                 "# to the client side application after compiling, use",
#                 "# the CONFIGJS section of the application's config.json",
#                 "# file for this.",
#                 "#",
#                 "from org.transcrypt.stubs.browser import __pragma__\n\n",
#                 "__pragma__('skip')\n",
#                 "# it is ignored on transcrypt\n",
#                 "window = 0\n",
#                 "__pragma__('noskip')\n\n"
#                 "__pragma__('jsiter')\n",
#             ])
#             end = "\n\n__pragma__('nojsiter')\n"

#             with open(os.path.join(
#                     apps_list_basedir, x, "sources", "transcrypts", "config.py"), 'w', encoding="utf-8") as f:
#                 content = "".join([ini, "CONFIG = {0}".format(json.dumps(CONFIG, ensure_ascii=True, indent=4)), end])
#                 content = content.replace('true', 'True').replace('false', 'False').replace('null', 'None')
#                 f.write(content)


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


# def delete_compiled_app_folder(project_path):
#     appConfig = config(project_path)
#     if appConfig.get('APPS'):
#         for x in appConfig.get('APPS'):
#             target = appConfig.get('APPS')[x]['build_folder']
#             if target:
#                 if os.path.exists(target) and os.path.isdir(target):
#                     shutil.rmtree(target)


# def copy_statics(project_path):
#     print("copying statics...")
#     appConfig = config(project_path)
#     version = appConfig['PROJECT']['version']
#     apps_list = appConfig.get("APPS")
#     apps_list_basedir = os.path.join(appConfig['PROJECT']['path'], "apps")
#     if apps_list and apps_list_basedir:
#         for x in apps_list:
#             compile_folder_static = os.path.join(apps_list[x]["build_folder"], "static")
#             if os.path.exists(compile_folder_static) and os.path.isdir(compile_folder_static):
#                 shutil.rmtree(compile_folder_static)
#             if os.path.exists(os.path.join(apps_list_basedir, x, "statics")):
#                 shutil.copytree(
#                     os.path.join(apps_list_basedir, x, "statics"),
#                     os.path.join(compile_folder_static, version)
#                 )
#                 print("copied on", os.path.join(compile_folder_static, version))


# def copy_languages(project_path):
#     print("copying languages...")
#     appConfig = config(project_path)
#     version = appConfig['PROJECT']['version']
#     debug = appConfig['PROJECT']['debug']
#     apps_list = appConfig.get("APPS")
#     apps_list_basedir = os.path.join(appConfig['PROJECT']['path'], "apps")
#     if apps_list and apps_list_basedir:
#         for x in apps_list:
#             source_apps = os.path.join(
#                 apps_list_basedir,
#                 "languages"
#             )
#             folder_lang_apps_list = os.path.join(
#                 apps_list[x]['build_folder'],
#                 "static",
#                 version,
#                 "languages"
#             )
#             os.makedirs(
#                 os.path.join(
#                     folder_lang_apps_list), exist_ok=True)
#             if not os.path.exists(folder_lang_apps_list):
#                 os.makedirs(
#                     os.path.join(folder_lang_apps_list), exist_ok=True
#                 )
#             langs = glob(os.path.join(source_apps, "*.json"))
#             for y in langs:
#                 with open(y, "r", encoding='utf-8') as f:
#                     c = json.load(f)
#                     lang_file = os.path.join(folder_lang_apps_list, os.path.basename(y))
#                     with open(lang_file, "w", encoding='utf-8') as o:
#                         if debug:
#                             json.dump(c, o, ensure_ascii=False, indent=2)
#                         else:
#                             json.dump(c, o, ensure_ascii=False)


# def compile_style(main_file, target_css, app_version, debug=False):
#     sass_files_subfolders = glob(os.path.join(os.path.dirname(main_file), "**", "*.sass"))
#     with open(main_file, 'r', encoding="utf-8") as f:
#         txt = f.read()
#         txt = "/* SASS Source Code (MAIN FILE): {0} */\n\n{1}".format(main_file, txt)
#         for x in sass_files_subfolders:
#             with open(x, 'r', encoding="utf-8") as s:
#                 c = "/* SASS Source Code: {0} */\n\n".format(x)
#                 temp_c = s.readlines()
#                 for t in temp_c:
#                     if t[0:13] == "$app-version:":
#                         t = "$app-version: {0}\n".format(app_version)
#                     c = "".join([c, t])
#                 txt = "\n".join([txt, c])
#         print("compiling Sass to Css: {0}".format(target_css))
#         if debug:
#             new_css = sass.compile(string=txt, indented=True, output_style="expanded")
#             new_css = new_css.replace("/* start change programmatically */\n", "")
#             new_css = new_css.replace("/*app-version*/\n", "")
#             new_css = new_css.replace("/* end change programmatically */", "")
#         else:
#             new_css = sass.compile(string=txt, indented=True, output_style="compressed")
#         with open(target_css, "w") as o:
#             o.write(new_css)


# def compile_styles(project_path):
#     appConfig = config(project_path)
#     version = appConfig['PROJECT']['version']
#     debug = appConfig['PROJECT']['debug']
#     apps_list = appConfig.get("APPS")
#     apps_list_basedir = os.path.join(appConfig['PROJECT']['path'], "apps")
#     if apps_list and apps_list_basedir:
#         for x in apps_list:
#             folder_css_apps_list = os.path.join(
#                 apps_list[x]['build_folder'],
#                 "static",
#                 version,
#                 "css"
#             )
#             os.makedirs(
#                 os.path.join(
#                     folder_css_apps_list), exist_ok=True)
#             target_css_apps_list = os.path.join(
#                 folder_css_apps_list,
#                 "{0}.css".format(apps_list[x]['styles_main_file'])
#             )
#             styles_main_file = os.path.join(
#                 apps_list_basedir, x, "sources", "styles", "{0}.sass".format(apps_list[x]['styles_main_file'])
#             )
#             compile_style(styles_main_file, target_css_apps_list, version, debug)


# def compile_views(project_path):
#     appConfig = config(project_path)
#     sys.path.append(project_path)
#     os.chdir(project_path)
#     debug = appConfig['PROJECT']['debug']
#     apps_list = appConfig.get("APPS")
#     apps_list_basedir = os.path.join(appConfig['PROJECT']['path'], "apps")
#     try:
#         os.makedirs(os.path.join(project_path, "temp"), exist_ok=True)
#     except OSError as e:
#         raise e("Problem on create folder '{0}'.".format(os.path.join(project_path, "temp")))
#     reg_update = config(os.path.join(project_path, "temp", "python_templates_mtime.json"))
#     new_reg_update = {}

#     def _compile_html(file, base="", target=None, is_apps=False, check_mtime=False, app_name="", ignore=["__init__.py"]):
#         if os.path.isfile(file) and os.path.basename(file) not in ignore and file[-3:] == ".py":
#             i_mod = "%s" % (os.path.basename(file)[0:-3])
#             if base:
#                 i_mod = "%s.%s" % (base, i_mod)
#             i = importlib.import_module(i_mod)
#             importlib.reload(i)
#             name = "".join([*i_mod.split(".")[-1], ".html"])
#             f_parts = i_mod.split(".")[3:-1]
#             files_www = os.path.join(target, *f_parts)
#             bkp_folder = os.path.join(project_path, "temp", app_name, *f_parts)
#             if is_apps:
#                 bkp_folder = os.path.join(project_path, "temp", app_name, *f_parts[1:])
#                 files_www = os.path.join(target, *f_parts[1:])
#             if not os.path.exists(os.path.join(files_www)):
#                 try:
#                     os.makedirs(os.path.join(files_www), exist_ok=True)
#                 except OSError as e:
#                     raise e("Problem on create folder '{0}'.".format(os.path.join(files_www)))
#             skip_file = False
#             try:
#                 os.makedirs(os.path.join(bkp_folder), exist_ok=True)
#             except OSError as e:
#                 raise e("Problem on create folder '{0}'.".format(os.path.join(bkp_folder)))
#             bkp_file = os.path.join(bkp_folder, name)
#             if check_mtime:
#                 current_tm = os.path.getmtime(file)
#                 new_reg_update[file] = current_tm
#                 if file in reg_update:
#                     if reg_update[file] == current_tm and os.path.exists(bkp_file) and debug:
#                         skip_file = True
#             if skip_file and debug:
#                 print("compiling: skip '{0}'".format(
#                         file,
#                         bkp_file,
#                         os.path.join(files_www, name)
#                     )
#                 )


#             else:
#                 print("compiling: (Convert Python ---> Html: {0})".format(file))
#                 with open(
#                     os.path.join(files_www, name),
#                     "wt",
#                     encoding="utf-8"
#                 ) as f:
#                     if debug:
#                         f.write(i.html.humanize())
#                     else:
#                         f.write(i.html.xml())


#     def _compile_htmls(source, base="", target=None, is_apps=False, check_mtime=False, app_name=""):
#         # htmls to www
#         list_all = glob(os.path.join(source, "*"))
#         for x in list_all:
#             if os.path.isdir(x) and not os.path.basename(x) == "__pycache__":
#                 if base:
#                     new_base = "%s.%s" % (base, os.path.basename(x))
#                     _compile_htmls(x, new_base, target=target, is_apps=is_apps, check_mtime=check_mtime, app_name=app_name)
#             elif os.path.isfile(x):
#                 _compile_html(x, base=base, target=target, is_apps=is_apps, check_mtime=check_mtime, app_name=app_name)

#     if apps_list and apps_list_basedir:
#         for x in apps_list:
#             target_apps = apps_list[x]['build_folder']
#             _compile_htmls(
#                 os.path.join(apps_list_basedir, x, "sources", "templates"),
#                 "apps.{0}.sources.templates".format(x),
#                 target=target_apps,
#                 is_apps=True,
#                 check_mtime=True,
#                 app_name=x
#             )
#         config(os.path.join(project_path, "temp", "python_templates_mtime.json"), new_reg_update)


# def compile_scripts(project_path, ignore=["__init__.py"]):
#     appConfig = config(project_path)
#     version = appConfig['PROJECT']['version']
#     python_env = appConfig['ENVIRONMENT']['python']
#     debug = appConfig['PROJECT']['debug']

#     apps_list = appConfig.get("APPS")
#     apps_list_basedir = os.path.join(appConfig['PROJECT']['path'], "apps")
#     if apps_list and apps_list_basedir:
#         for x in apps_list:
#             folder_script_apps_list = os.path.join(
#                 apps_list[x]['build_folder'],
#                 "static",
#                 version,
#                 "js",
#                 "transcrypt"
#             )
#             os.makedirs(
#                 os.path.join(
#                     folder_script_apps_list), exist_ok=True)
#             source = os.path.join(apps_list_basedir, x, "sources", "transcrypts", "__target__")
#             tar_apps = os.path.join(
#                 apps_list_basedir, x, "sources", "transcrypts", "{0}.py".format(apps_list[x]['transcrypt_main_file']))
#             print("compiling Python to Javascript: %s" % tar_apps)
#             if debug:
#                 subprocess.run("%s -m transcrypt %s -n -m" % (python_env, tar_apps), shell=True)
#             else:
#                 subprocess.run("%s -m transcrypt %s -m" % (python_env, tar_apps), shell=True)
#             list_all = glob(os.path.join(source, "*"))

#             for y in list_all:
#                 if os.path.isfile(y):
#                     script_file = os.path.join(
#                         folder_script_apps_list, os.path.basename(y)
#                     )
#                     shutil.copy(
#                         y,
#                         script_file
#                     )

#     print("Finish compiling scripts")


# def generate_script_importing_transcrypt_module(project_path, script_main_file) -> list:
#     appConfig = config(project_path)
#     base = os.path.join(appConfig['PATH']['app'], "sources", "transcrypts")
#     main_files = appConfig['TRANSCRYPT']['main_files']
#     version = appConfig['PROJECT']['version']
#     targets = []
#     if isinstance(main_files, list):
#         t = set()
#         for x in set(main_files):
#             t.add(os.path.normpath(x))
#         targets = list(t)
#     else:
#         targets.append(os.path.normpath(main_files))
#     res = []
#     for x in targets:
#         p = PurePath(script_main_file)
#         p = p.relative_to(base)
#         p.parts
#         rel = "/".join(p.parts)
#         rel = rel.replace("\\", "/")
#         cod = interpolate(
#             "<script type=\"module\">import * as {{MODULE}} from '/static/{{VERSION}}/js/transcrypt/{{FILE}}'</script>",
#             context={'MODULE': os.path.basename(rel)[:-3], 'VERSION': version, 'FILE': "{0}.js".format(rel[:-3])}
#         )
#         res.append(cod)
#     return res


def app_name_from_relative_child(project_path, file_or_folder_in_apps_path):
    apps_list_basedir = os.path.join(project_path, "apps")
    p = PurePath(file_or_folder_in_apps_path)
    r = p.relative_to(os.path.join(apps_list_basedir))
    return r.parts[0]


def package_project_app(project_path, target, reset_config=True):
    appConfig = config(project_path)
    secret_key = appConfig['API']['secret_key']
    password_email = appConfig['EMAIL']['password']
    if reset_config:
        appConfig['ENVIRONMENT']['path'] = ""
        appConfig['ENVIRONMENT']['python'] = ""
        appConfig['PROJECT']['packaged'] = True
        appConfig['API']['secret_key'] = "secret_key"
        appConfig['APP']['compiled_app_folder'] = "{{PROJECT_FOLDER}}\\app\\www"
        appConfig['PATH']['project'] = '{{PROJECT_FOLDER}}'
        appConfig['PATH']['api'] = '{{PROJECT_FOLDER}}\\api'
        appConfig['PATH']['app'] = '{{PROJECT_FOLDER}}\\app'
        appConfig['EMAIL']['password'] = "email_password"
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
        temp_file,
        ignore=shutil.ignore_patterns('*.pyc', '.*', '__target__')
    )
    with open(os.path.join(temp_file, "config.json"), "w", encoding="utf-8") as f:
        json.dump(appConfig, f, ensure_ascii=True, indent=2)
    if os.path.exists(os.path.join(temp_file, "app", "www")):
        shutil.rmtree(os.path.join(temp_file, "app", "www"))
    if os.path.exists(os.path.join(temp_file, "api", "databases")):
        shutil.rmtree(os.path.join(temp_file, "api", "databases"))
    if os.path.exists(os.path.join(temp_file, "api", "languages")):
        shutil.rmtree(os.path.join(temp_file, "api", "languages"))
    if os.path.exists(os.path.join(temp_file, "app", "languages")):
        shutil.rmtree(os.path.join(temp_file, "app", "languages"))
    if os.path.exists(os.path.join(temp_file, "api", "uploads")):
        shutil.rmtree(os.path.join(temp_file, "api", "uploads"))
    if os.path.exists(os.path.join(temp_file, "logs")):
        shutil.rmtree(os.path.join(temp_file, "logs"))
    if os.path.exists(os.path.join(temp_file, "__pycache__")):
        shutil.rmtree(os.path.join(temp_file, "__pycache__"))
    if os.path.exists(os.path.join(temp_file, ".git")):
        shutil.rmtree(os.path.join(temp_file, ".git"))

    pycaches = glob("{0}\\**\\__pycache__".format(temp_file), recursive=True)
    for x in pycaches:
        shutil.rmtree(x)
    pid = glob("{0}\\**\\phanterpwa.pid".format(temp_file), recursive=True)
    for x in pid:
        os.remove(x)
    if os.path.exists("{0}\\**\\.gitattributes".format(temp_file)):
        os.remove("{0}\\**\\.gitattributes".format(temp_file))

    if os.path.exists("{0}\\**\\.gitignore".format(temp_file)):
        os.remove("{0}\\**\\.gitignore".format(temp_file))

    os.makedirs(os.path.join(temp_file, "api", "languages"), exist_ok=True)
    os.makedirs(os.path.join(temp_file, "app", "languages"), exist_ok=True)
    os.makedirs(os.path.join(temp_file, "api", "uploads"), exist_ok=True)
    os.makedirs(os.path.join(temp_file, "api", "databases"), exist_ok=True)
    os.makedirs(os.path.join(temp_file, "app", "www"), exist_ok=True)
    os.makedirs(os.path.join(temp_file, "logs"), exist_ok=True)

    shutil.make_archive(os.path.join(os.path.join(compact_temp), file_name), 'zip', temp_file)
    shutil.copyfile(
        os.path.join(compact_temp, "{0}.zip".format(file_name)),
        os.path.join(target, "{0}.ppwa".format(file_name))
    )
    with open(os.path.join(target, "{0}.secret".format(file_name)), "w", encoding="utf-8") as f:
        f.write(
            "secret_key: {0}\npassword_email: {1}".format(secret_key, password_email)
        )


# def compiler(projectPath):
#     appConfig = config(projectPath)
#     debug = appConfig['PROJECT']['debug']
#     if not debug:
#         delete_compiled_app_folder(projectPath)
#     create_transcrypt_config(projectPath)
#     copy_statics(projectPath)
#     copy_languages(projectPath)
#     compile_styles(projectPath)
#     compile_views(projectPath)
#     compile_scripts(projectPath)


def generate_password_hash(password):
    hash = pbkdf2_sha512.hash(password)
    return hash


def check_password_hash(hash, password):
    return pbkdf2_sha512.verify(password, hash)


class DictArgsToDALFields(object):

    def __init__(self, dict_args, *fields):
        super(DictArgsToDALFields, self).__init__()
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
                "The dict_args must be dict object. given: %s" % type(dict_args)
            )

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, list_fields):
        n_l = list()
        for x in list_fields:
            if isinstance(x, Field):
                n_l.append(x)
            else:
                if x is not None:
                    raise TypeError(
                        "The fields must be pydal.Field object. given: %s" % type(x)
                    )
        self._fields = n_l

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
        if not self.errors and isinstance(dbtable, Table):
            rep = dbtable.validate_and_insert(**self.verified)
            dbtable._db._adapter.reconnect()
            if rep.errors:
                dbtable._db.rollback()
            elif rep.id and commit:
                dbtable._db.commit()
            return rep
        else:
            if not self.errors:
                raise "The dbtable must be pydal.DAL.Table instance. given: {0}.".format(type(dbtable))

    def validate_and_update(self, dbset, commit=True):
        self.validate()
        if not self.errors and isinstance(dbset, Set):
            rep = dbset.validate_and_update(**self.verified)
            dbset._db._adapter.reconnect()
            if rep.errors:
                dbset._db.rollback
            elif rep.id and commit:
                dbset._db.commit()
            return rep
        else:
            if not self.errors:
                raise "The dbtable must be pydal.Objects.Set instance. given: {0}.".format(type(dbset))


def text_normalize(text, upper=True):
    if upper:
        return normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').upper()
    else:
        return normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')


if __name__ == '__main__':
    package_project_app()
