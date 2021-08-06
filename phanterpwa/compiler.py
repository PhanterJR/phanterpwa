import os
import sys
import sass
import json
import importlib
import shutil
import subprocess
import phanterpwa
import time
import datetime
import re
import traceback
from pathlib import PurePath
from glob import glob, iglob
from phanterpwa.configer import ProjectConfig
from os.path import (
    normpath,
    join,
    isdir,
    isfile,
    dirname,
    basename,
    exists,
    getmtime
)

ENV_PYTHON = normpath(sys.executable)
PATH_PHANTERPWA = dirname(phanterpwa.__file__)

class Compiler():
    """
        pt-BR: A classe Compilar, baseado na configuração do projeto (project.ini, api.ini e app.ini), axecuta as seguintes ações:
            Se a configuração do projeto estiver em debug: True
            - Converte os templates python pra o formato html
            -
    """

    def __init__(self, projectpath, build_apps_folder=None, reset_compilation=False):
        self.has_error = None
        self.ProjectConfig = ProjectConfig(projectpath)
        self.projectpath = projectpath
        self.config = self.ProjectConfig.config
        self._check_app_list()
        self.build_apps_folder = build_apps_folder
        if reset_compilation:
            self.current_compilation = 0

        else:
            self.current_compilation = self.config['PROJECT'].get("compilation", 0)
            self.current_compilation += 1
        self.config['PROJECT']["compilation"] = self.current_compilation
        self.config['PROJECT']['versioning'] = "{0}.{1}".format(
            self.config["PROJECT"].get("version", "0.0.1"),
            self.current_compilation
        )
        self.debug = self.config['PROJECT']["debug"]
        self.versioning = self.config['PROJECT']['versioning']
        self.tempfolder = join(self.projectpath, "temp")
        if self.debug:
            self.minify = False
            self.full_compilation = False
            self.clear_builder_folder = False
        else:
            self.minify = True
            self.full_compilation = True
            self.clear_builder_folder = True
        self.ProjectConfig.save()
        self._templates_to_update = {}
        self._statics_to_update = {}
        self._styles_changed = {}
        self._phanterpwa_modules_changed = []
        self._has_config_changed = {}
        self._has_style_change = {}
        self._has_template_change = {}
        self._has_static_change = {}
        self._has_script_change = {}
        self._has_phanterpwa_modules_change = {}
        self._create_temp_folder()

    def _check_app_list(self):

        for app in list(self.config['FRONTEND'].keys()):
            if not isdir(join(self.projectpath, "frontapps", app)):
                del self.config['FRONTEND'][app]

    @property
    def app_list(self):
        """
            lista os aplicativos
        """
        self._check_app_list()
        return self.config['FRONTEND'].keys()

    @property
    def build_apps_folder(self):
        return self._build_apps_folder

    @build_apps_folder.setter
    def build_apps_folder(self, value):
        self._build_apps_folder = None
        if value is not None:
            if isdir(value):
                self._build_apps_folder = value
            else:
                raise IOError("The build apps folder don't found! Given: {0}".format(value))

    @property
    def minify(self):
        return self._minify

    @minify.setter
    def minify(self, value):
        if isinstance(value, bool):
            self._minify = value
        else:
            raise ValueError("The minify attribute must be boolean type. Given: {0}".format(type(value)))

    @property
    def projectpath(self):
        return self._projectpath

    @projectpath.setter
    def projectpath(self, value):
        if isdir(join(value)):
            if isfile(join(value, "config.json")):
                self._projectpath = value
            else:
                raise ValueError("the project path don't have the config file (config.json).")
        else:
            raise IOError("The project path is invalid!. Given: {0}".format(value))

    @staticmethod
    def get_files_dir(path, ignore_files=[], ignore_paths=[]):
        r = os.walk(path)
        for x in r:
            if basename(x[0]) not in ignore_paths:
                for y in x[2]:
                    if basename(y) not in ignore_files:
                        yield normpath(join(x[0], y))
        pass

    def templates_files(self, app, include_extends=False):
        if include_extends:
            ig_paths = ["__pycache__"]
        else:
            ig_paths = ["__pycache__", "extends"]
        files = self.get_files_dir(
            self.path_templates_folder(app), ignore_files=["__init__.py"], ignore_paths=ig_paths)
        return (x for x in files if x.endswith(".py"))

    def extends_files(self, app):
        files = self.get_files_dir(
            join(self.path_templates_folder(app), "extends"),
                ignore_files=["__init__.py"], ignore_paths=["__pycache__"])
        return (x for x in files if x.endswith(".py"))

    def static_files(self, app):
        files = self.get_files_dir(
            self.path_statics_folder(app), ignore_files=["__init__.py"], ignore_paths=["__pycache__"])
        return (x for x in files)

    def transcrypt_files(self, app):
        files = self.get_files_dir(
            self.path_transcrypts_folder(app), ignore_files=["__init__.py"],
                ignore_paths=["__pycache__", "__target__"])
        return (x for x in files if x.endswith(".py"))

    def style_files(self, app):
        files = self.get_files_dir(
            self.path_styles_folder(app), ignore_files=["__init__.py"], ignore_paths=["__pycache__"])
        return (normpath(x) for x in files if x.endswith(".sass"))

    def phanterpwa_usual_sass(self, app):
        print("\nProcess PhanterPWA usual sass...")
        main_file = join(PATH_PHANTERPWA, "usual_sass", "phanterpwa.sass")
        if exists(join(dirname(main_file), "_compiler_sass_temp_file.sass")):
            os.unlink(join(dirname(main_file), "_compiler_sass_temp_file.sass"))
        target_dir = join(self.projectpath, "frontapps", app, "statics", "css")
        if not isdir(target_dir):
            try:
                os.makedirs(target_dir, exist_ok=True)
            except OSError as e:
                raise e("Problem on create folder '{0}'.".format(target_dir))
        target_css = join(target_dir, "phanterpwa.css")

        sfiles = self.get_files_dir(
            join(PATH_PHANTERPWA, "usual_sass"), ignore_files=["__init__.py"], ignore_paths=["__pycache__"])
        sass_files = (normpath(x) for x in sfiles if x.endswith(".sass"))

        with open(main_file, 'r', encoding="utf-8") as f:
            txt = f.read()
            txt = re.sub(
                r"/\* start change programmatically[\W\w]*end change programmatically \*[\r\n]?/",
                "",
                txt
            )
            if re.search(r"\$app-version: [\"\'][0-9]{0, 3}\.[0-9]{0, 3}\.[0-9]{0, }\.[0-9]{0, }\"", txt):
                new_text_to_save = re.sub(
                    r"\$app-version: [\"\'][0-9]{0, 3}\.[0-9]{0, 3}\.[0-9]{0, }\.[0-9]{0, }\"",
                    "$app-version: \"{0}\"".format(self.versioning),
                    txt
                )
            else:
                new_text_to_save = "".join([
                    "/* start change programmatically */\n",
                    "$app-version: \"{0}\"\n".format(self.versioning),
                    "/* end change programmatically */",
                    txt
                ])
            txt = new_text_to_save
            txt = "/* SASS Source Code (MAIN FILE): {0} */\n\n{1}".format(main_file, txt)
            has_import = False
            for x in sass_files:
                if x != normpath(main_file):
                    c = "/* SASS Source Code: {0} */\n\n".format(x)
                    p = PurePath(x)
                    p = p.relative_to(dirname(main_file))
                    l = [*p.parts]
                    l[-1] = l[-1][0:-5]
                    patter = "@import '{0}'".format("/".join(l))
                    txt = "".join(["\n", txt, c, patter, "\n\n"])
                    has_import = True
            if has_import:
                print("    Creating imports and adding in temp file",
                    dirname(main_file), "_compiler_sass_temp_file.sass")

            with open(join(dirname(main_file), "_compiler_sass_temp_file.sass"), "w", encoding="utf-8") as f2:
                f2.write(txt)
            print("    Convert sass to css: {0}".format(target_css))
            if self.minify:
                new_css = sass.compile(
                    filename=join(dirname(main_file), "_compiler_sass_temp_file.sass"),
                    output_style="compressed"
                )
            else:
                new_css = sass.compile(
                    filename=join(dirname(main_file), "_compiler_sass_temp_file.sass"),
                    output_style="expanded"
                )
                new_css = re.sub(
                    r"^/\* start change programmatically[\W\w]*end change programmatically \*/$",
                    "",
                    new_css)
            if isfile(join(self.projectpath, "temp", "_compiler_sass_temp_file.sass")):
                os.unlink(join(self.projectpath, "temp", "_compiler_sass_temp_file.sass"))
            shutil.copy(
                join(dirname(main_file), "_compiler_sass_temp_file.sass"),
                join(self.projectpath, "temp", "_compiler_sass_temp_file.sass")
            )
            with open(target_css, "w") as o:
                o.write(new_css)
            os.unlink(join(dirname(main_file), "_compiler_sass_temp_file.sass"))
        with open(main_file, "w", encoding="utf-8") as fw:
            fw.write(new_text_to_save)

    @staticmethod
    def target_by_relative_path(src_path, tgt_path, ext_src=None, ext_tgt=None, ignore_files=[], ignore_paths=[]):

        def _target(file_path, relative_to, tgt_path, ext_src, ext_tgt):
            p = PurePath(file_path)
            p = p.relative_to(relative_to)
            target_file = join(tgt_path, *p.parts)
            if ext_tgt is not None:
                target_file = "".join([target_file[0:-len(ext_src)], ext_tgt])
            return [file_path, target_file]

        if ext_tgt is not None:
            if ext_src is None:
                raise SyntaxError("The ext_src can't be None when ext_tgt is different of None.")
            if not ext_tgt.startswith("."):
                raise ValueError("The ext_tgt must be starts with dot(.) or must be None. Examplo: .py")

        if ext_src is not None:
            if not ext_src.startswith("."):
                raise ValueError("The ext_src must be starts with dot(.) or must be None. Examplo: .py")
            return (
                _target(
                    f,
                    relative_to=src_path,
                    tgt_path=tgt_path, ext_src=ext_src,
                    ext_tgt=ext_tgt
                ) for f in Compiler.get_files_dir(src_path,
                        ignore_files=ignore_files,
                        ignore_paths=ignore_paths) if f.endswith(ext_src)
            )
        else:
            return (
                _target(
                    f,
                    relative_to=src_path,
                    tgt_path=tgt_path, ext_src=ext_src,
                    ext_tgt=ext_tgt
                ) for f in Compiler.get_files_dir(src_path,
                        ignore_files=ignore_files,
                        ignore_paths=ignore_paths)
            )

    def _create_temp_folder(self):
        try:
            os.makedirs(join(self.tempfolder), exist_ok=True)
        except OSError as e:
            raise e("Problem on create folder '{0}'.".format(join(self.tempfolder)))

    def path_build_templates_folder(self, app):
        if self.build_apps_folder:
            return join(self.build_apps_folder, app, "www")
        else:
            return self.config["FRONTEND"][app]["build_folder"]

    def path_build_statics_folder(self, app):
        if self.build_apps_folder:
            return join(self.build_apps_folder, app, "www", "static")
        else:
            return join(self.config["FRONTEND"][app]["build_folder"], "static")

    def path_build_styles_folder(self, app):
        if self.build_apps_folder:
            return join(self.build_apps_folder, app, "www", "static", self.versioning, "css")
        else:
            return join(self.config["FRONTEND"][app]["build_folder"], "static", self.versioning, "css")

    def path_build_transcrypt_folder(self, app):
        if self.build_apps_folder:
            return join(self.build_apps_folder, app, "www", "static", self.versioning, "js", "transcrypt")
        else:
            return join(self.config["FRONTEND"][app]["build_folder"], "static", self.versioning, "js", "transcrypt")

    def path_templates_folder(self, app):
        return join(self.projectpath, "frontapps", app, "sources", "templates")

    def path_styles_folder(self, app):
        return join(self.projectpath, "frontapps", app, "sources", "styles")

    def path_transcrypts_folder(self, app):
        return join(self.projectpath, "frontapps", app, "sources", "transcrypts")

    def path_statics_folder(self, app):
        return join(self.projectpath, "frontapps", app, "statics")

    def path_app_config_file(self, app):
        os.makedirs(join(self.path_transcrypts_folder(app), "auto"), exist_ok=True)
        return join(self.path_transcrypts_folder(app), "auto", "config.py")

    def target_template_file_by_source(self, src, app) -> str:
        relative_to = self.path_templates_folder(app)
        target_path = self.path_build_templates_folder(app)
        p = PurePath(src)
        p = p.relative_to(relative_to)
        target_file = join(target_path, *p.parts)
        target_file = "".join([target_file[0:-3], ".html"])
        return target_file

    def _check_templates_target_exist(self, src, app) -> bool:
        target = self.target_template_file_by_source(src, app)
        return isfile(target)

    def target_static_file_by_source(self, src, app) -> str:
        relative_to = self.path_statics_folder(app)
        target_path = join(self.path_build_statics_folder(app), self.versioning)
        p = PurePath(src)
        p = p.relative_to(relative_to)
        target_file = join(target_path, *p.parts)
        return target_file

    def _check_statics_target_exist(self, src, app) -> bool:
        target = self.target_static_file_by_source(src, app)
        return isfile(target)

    def _check_style_target_exist(self, app):
        target = join(self.path_build_styles_folder(app),
            "{0}.css".format(self.config["FRONTEND"][app]["styles_main_file"]))
        return isfile(target)

    def _check_transcrypt_target_exist(self, app):
        target = join(self.path_build_transcrypt_folder(app),
            "{0}.js".format(self.config["FRONTEND"][app]["transcrypt_main_file"]))
        return isfile(target)

    def create_templates_to_update_generator(self, app):
        if any([self.full_compilation, self._has_config_changed.get(app, False),
                self._check_template_extends_change(app)]):
            self._templates_to_update[app] = self.templates_files(app)
        else:
            self._templates_to_update[app] = []
            t_files = self.templates_files(app)
            if isfile(join(self.tempfolder, "templates_mtime_{0}.json".format(app))):
                with open(join(self.tempfolder,
                        "templates_mtime_{0}.json".format(app)), "r", encoding="utf-8") as f:
                    content = json.load(f)
                    for x in t_files:
                        if x in content:
                            if getmtime(x) != content[x] or not self._check_templates_target_exist(x, app):
                                self._templates_to_update[app].append(x)
                        else:
                            self._templates_to_update[app].append(x)
            else:
                self._templates_to_update[app] = self.templates_files(app)

    def create_statics_to_update_generator(self, app):
        if any([self.full_compilation, self._has_config_changed.get(app, False)]):
            self._statics_to_update[app] = self.static_files(app)
        else:
            self._statics_to_update[app] = []
            t_files = self.static_files(app)
            if isfile(join(self.tempfolder, "statics_mtime_{0}.json".format(app))):
                with open(join(self.tempfolder,
                        "statics_mtime_{0}.json".format(app)), "r", encoding="utf-8") as f:
                    content = json.load(f)
                    for x in t_files:
                        if x in content:
                            if getmtime(x) != content[x] or not self._check_statics_target_exist(x, app):
                                self._statics_to_update[app].append(x)
                        else:
                            self._statics_to_update[app].append(x)
            else:
                self._statics_to_update[app] = self.static_files(app)

    def _check_styles_change(self, app):
        if any([self.full_compilation,
                self._has_config_changed.get(app, False), not self._check_style_target_exist(app)]):
            return True
        t_files = self.style_files(app)
        if isfile(join(self.tempfolder, "styles_mtime_{0}.json".format(app))):
            with open(join(self.tempfolder,
                    "styles_mtime_{0}.json".format(app)), "r", encoding="utf-8") as f:
                content = json.load(f)
                for x in t_files:
                    if x in content:
                        if getmtime(x) != content[x]:
                            return True
                    else:
                        return True
        else:
            return True
        return False

    def _check_script_change(self, app):
        if any([self.full_compilation,
                self._has_config_changed.get(app, False), not self._check_transcrypt_target_exist(app)]):
            return True
        t_files = self.transcrypt_files(app)
        if isfile(join(self.tempfolder, "transcrypts_mtime_{0}.json".format(app))):
            with open(join(self.tempfolder,
                    "transcrypts_mtime_{0}.json".format(app)), "r", encoding="utf-8") as f:
                content = json.load(f)
                for x in t_files:
                    if x in content:
                        if getmtime(x) != content[x]:
                            return True
                    else:
                        return True
                for x in content:
                    if not isfile(x):
                        return True
        else:
            return True
        return False

    # def modules_files_monitor(self):
    #     t = join(dirname(phanterpwa.__file__), "frontapps")
    #     lfi = self.get_files_dir(t, ignore_files=["__init__.py"], ignore_paths=["__pycache__"])
    #     return [x for x in lfi] + [
    #         join(dirname(phanterpwa.__file__), "xmlconstructor.py"),
    #         join(dirname(phanterpwa.__file__), "helpers.py")
    #     ]

    # def _check_phanterpwa_modules(self):
    #     t_files = self.modules_files_monitor()
    #     has_change = False
    #     if isfile(join(self.tempfolder, "phanterpwa_modules_mtime.json")):
    #         with open(join(self.tempfolder,
    #                 "phanterpwa_modules_mtime.json"), "r", encoding="utf-8") as f:
    #             content = json.load(f)
    #             for x in t_files:
    #                 if x in content:
    #                     if getmtime(x) != content[x]:
    #                         has_change = True
    #                 else:
    #                     has_change = True
    #     else:
    #         has_change = True
    #     if has_change:
    #         for app in self.app_list:
    #             if exists(join(self.tempfolder, "transcrypts_mtime_{0}.json".format(app))):
    #                 os.unlink(join(self.tempfolder, "transcrypts_mtime_{0}.json".format(app)))

    #             if exists(join(self.tempfolder, "templates_mtime_{0}.json".format(app))):
    #                 os.unlink(join(self.tempfolder, "templates_mtime_{0}.json".format(app)))

    def _check_template_extends_change(self, app):
        extends_files = self.extends_files(app)
        if isfile(join(self.tempfolder, "extends_mtime_{0}.json".format(app))):
            with open(join(self.tempfolder,
                    "extends_mtime_{0}.json".format(app)), "r", encoding="utf-8") as f:
                content = json.load(f)
                for x in extends_files:
                    if x in content:
                        if getmtime(x) != content[x]:
                            return True
                    else:
                        return True
                return False
        else:
            return True

    def copy_statics(self, app) -> list:
        print("\nProcess statics...")
        self.create_statics_to_update_generator(app)
        if self.full_compilation:
            path_build_statics_folder_versioned = join(self.path_build_statics_folder(app), self.versioning)
            path_statics_folder = self.path_statics_folder(app)
            if exists(path_build_statics_folder_versioned) and isdir(path_build_statics_folder_versioned):
                shutil.rmtree(path_build_statics_folder_versioned)
            if exists(path_statics_folder):
                shutil.copytree(
                    path_statics_folder,
                    path_build_statics_folder_versioned
                )
                print("    Coping on", join(path_build_statics_folder_versioned))
        else:
            paths_on_static_folder = (x for x in glob(join(self.path_build_statics_folder(app), "*")) if isdir(x))
            for pat in paths_on_static_folder:
                if basename(pat) != self.versioning:
                    try:
                        shutil.rmtree(pat)
                    except Exception as e:
                        print(e)
            has_copy = False
            for x in self._statics_to_update[app]:
                rel = self.target_static_file_by_source(x, app)
                print("    Coping statics: {0} ---> {1}".format(x, rel))
                try:
                    os.makedirs(dirname(rel), exist_ok=True)
                except OSError as e:
                    raise e("Problem on create folder '{0}'.".format(dirname(rel)))
                shutil.copy2(x, rel)
                has_copy = True
            if not has_copy:
                pass
                print("    Skiping Static...")

    def delete_compiled_app_folder(self, app):
        appConfig = self.config
        if self.full_compilation:
            target = appConfig.get('FRONTEND')[app]['build_folder']
            if target:
                if exists(target) and isdir(target):
                    print("Deleting builder folder...")
                    try:
                        shutil.rmtree(target)
                    except OSError as e:
                        print("Error: %s - %s." % (e.filename, e.strerror))
                        pass
                    while exists(target):
                        pass
                    print("Deleted ({0})".format(target))

    def copy_languages(self, app):
        print("\nCopying languages...")
        appConfig = self.config
        version = self.versioning
        apps_list_basedir = join(appConfig['PROJECT']['path'], "frontapps")
        source_apps = join(
            apps_list_basedir,
            "languages"
        )
        folder_lang_apps_list = join(
            appConfig["FRONTEND"][app]['build_folder'],
            "static",
            version,
            "languages"
        )
        os.makedirs(
            join(
                folder_lang_apps_list), exist_ok=True)
        if not exists(folder_lang_apps_list):
            os.makedirs(
                join(folder_lang_apps_list), exist_ok=True
            )
        langs = glob(join(source_apps, "*.json"))
        for y in langs:
            with open(y, "r", encoding='utf-8') as f:
                c = json.load(f)
                lang_file = join(folder_lang_apps_list, basename(y))
                with open(lang_file, "w", encoding='utf-8') as o:
                    if self.minify:
                        json.dump(c, o, ensure_ascii=False)
                    else:
                        json.dump(c, o, ensure_ascii=False, indent=2)

    def compile_styles(self, app):
        print("\nProcess styles...")
        appConfig = self.config
        changed = self._check_styles_change(app)
        if changed or self.full_compilation:
            main_file = join(
                self.path_styles_folder(app), "{0}.sass".format(
                    appConfig["FRONTEND"][app]['styles_main_file'])
            )
            if exists(join(dirname(main_file), "_compiler_sass_temp_file.sass")):
                os.unlink(join(dirname(main_file), "_compiler_sass_temp_file.sass"))
            target_css = join(
                self.path_build_styles_folder(app),
                    "{0}.css".format(appConfig["FRONTEND"][app]['styles_main_file'])
            )
            try:
                os.makedirs(dirname(target_css), exist_ok=True)
            except OSError as e:
                raise e("Problem on create folder '{0}'.".format(target_css))

            sass_files = self.style_files(app)

            with open(main_file, 'r', encoding="utf-8") as f:
                txt = f.read()
                txt = re.sub(
                    r"/\* start change programmatically[\W\w]*end change programmatically \*[\r\n]?/",
                    "",
                    txt
                )
                if re.search(r"\$app-version: [\"\'][0-9]{0, 3}\.[0-9]{0, 3}\.[0-9]{0, }\.[0-9]{0, }\"", txt):
                    new_text_to_save = re.sub(
                        r"\$app-version: [\"\'][0-9]{0, 3}\.[0-9]{0, 3}\.[0-9]{0, }\.[0-9]{0, }\"",
                        "$app-version: \"{0}\"".format(self.versioning),
                        txt
                    )
                else:
                    new_text_to_save = "".join([
                        "/* start change programmatically */\n",
                        "$app-version: \"{0}\"\n".format(self.versioning),
                        "/* end change programmatically */",
                        txt
                    ])
                txt = new_text_to_save
                txt = "/* SASS Source Code (MAIN FILE): {0} */\n\n{1}".format(main_file, txt)
                has_import = False
                for x in sass_files:
                    if x != normpath(main_file):
                        c = "/* SASS Source Code: {0} */\n\n".format(x)
                        p = PurePath(x)
                        p = p.relative_to(dirname(main_file))
                        l = [*p.parts]
                        l[-1] = l[-1][0:-5]
                        patter = "@import '{0}'".format("/".join(l))
                        txt = "".join(["\n", txt, c, patter, "\n\n"])
                        has_import = True
                if has_import:
                    print("    Creating imports and adding in temp file",
                        dirname(main_file), "_compiler_sass_temp_file.sass")

                with open(join(dirname(main_file), "_compiler_sass_temp_file.sass"), "w", encoding="utf-8") as f2:
                    f2.write(txt)
                print("    Convert sass to css: {0}".format(target_css))
                if self.minify:
                    new_css = sass.compile(
                        filename=join(dirname(main_file), "_compiler_sass_temp_file.sass"),
                        output_style="compressed"
                    )
                else:
                    new_css = sass.compile(
                        filename=join(dirname(main_file), "_compiler_sass_temp_file.sass"),
                        output_style="expanded"
                    )
                    new_css = re.sub(
                        r"^/\* start change programmatically[\W\w]*end change programmatically \*/$",
                        "",
                        new_css)
                if isfile(join(self.projectpath, "temp", "_compiler_sass_temp_file.sass")):
                    os.unlink(join(self.projectpath, "temp", "_compiler_sass_temp_file.sass"))
                shutil.copy(
                    join(dirname(main_file), "_compiler_sass_temp_file.sass"),
                    join(self.projectpath, "temp", "_compiler_sass_temp_file.sass")
                )
                with open(target_css, "w") as o:
                    o.write(new_css)
                os.unlink(join(dirname(main_file), "_compiler_sass_temp_file.sass"))
            with open(main_file, "w", encoding="utf-8") as fw:
                fw.write(new_text_to_save)
        else:
            print("    Skiping styles...")

    def compile_templates(self, app):
        print("\nProcess Templates...")
        self.create_templates_to_update_generator(app)
        project_path = self.projectpath
        appConfig = self.config
        sys.path.append(project_path)
        os.chdir(project_path)
        base_dir = join(appConfig['PROJECT']['path'], "frontapps", app)

        def _compile_html(file, base="", target=None, is_apps=False, app_name="", ignore=["__init__.py"]):

            if isfile(file) and basename(file) not in ignore and file[-3:] == ".py":
                i_mod = "%s" % (basename(file)[0:-3])
                if base:
                    i_mod = "%s.%s" % (base, i_mod)
                i = importlib.import_module(i_mod)
                importlib.reload(i)
                name = "".join([*i_mod.split(".")[-1], ".html"])
                f_parts = i_mod.split(".")[3:-1]
                files_www = join(target, *f_parts)
                if is_apps:
                    files_www = join(target, *f_parts[1:])
                if not exists(join(files_www)):
                    try:
                        os.makedirs(join(files_www), exist_ok=True)
                    except OSError as e:
                        raise e("Problem on create folder '{0}'.".format(join(files_www)))
                print("    Convert python to html: {0} ---> {1})".format(file, join(files_www, name)))
                with open(
                    join(files_www, name),
                    "wt",
                    encoding="utf-8"
                ) as f:
                    if self.minify:
                        f.write(i.html.xml())
                    else:
                        f.write(i.html.humanize())

        def _compile_htmls(source, base="", target=None, is_apps=False, app_name=""):
            list_all = iglob(join(source, "*"))
            ignore_paths = ["__pycache__", "extends"]
            for x in list_all:
                bname = basename(x)
                if isdir(x) and bname not in ignore_paths:
                    if base:
                        new_base = "{0}.{1}".format(base, basename(x))
                        _compile_htmls(x, new_base, target=target, is_apps=is_apps, app_name=app_name)
                elif isfile(x) and x in self._templates_to_update[app]:
                    _compile_html(x, base=base, target=target, is_apps=is_apps, app_name=app_name)

        target_apps = self.path_build_templates_folder(app)
        self._templates_to_update[app] = [x for x in self._templates_to_update[app]]
        if self._templates_to_update[app]:
            _compile_htmls(
                join(base_dir, "sources", "templates"),
                "frontapps.{0}.sources.templates".format(app),
                target=target_apps,
                is_apps=True,
                app_name=app
            )
        else:
            print("    Skiping templates...")
            self._cont_templates = 0

    def compile_transcrypts(self, app):
        print("\nProcess scrypts...")
        appConfig = self.config
        changed = self._check_script_change(app)
        if not (changed or self.full_compilation):
            print("    Local files no changed...")
        python_env = appConfig['ENVIRONMENT']['python']
        folder_script_apps_list = self.path_build_transcrypt_folder(app)
        os.makedirs(
            join(
                folder_script_apps_list), exist_ok=True)
        source = join(self.path_transcrypts_folder(app), "__target__")
        files_trans = []
        for t in glob(join(self.path_transcrypts_folder(app), "*.py")):
            if not basename(t).startswith("_"):
                files_trans.append(t)
        for main_file in files_trans:
            now = datetime.datetime.now()
            mdtime = time.mktime(now.timetuple())
            os.utime(main_file, (mdtime, mdtime))
            print("    Convert python to javascript: {0}".format(main_file))
            print("    Starting Transcrypt compiler. Wait to complete.")
            if self.minify:
                print("    For minification it's necessary to have java installed, if compilation fail,",
                    " the compilation will try transcrypt on unminify format.")
                try:
                    subprocess.run("{0} -X utf8 -m transcrypt {1}".format(python_env, main_file), shell=True, check=True)
                except Exception as e:
                    print("    Minification Fail!!! It's try unminify mode now, it's fast.",
                        " Check java instalation. Error:", e)
                    subprocess.run("{0} -X utf8 -m transcrypt {1} -n".format(python_env, main_file), shell=True, check=True)
            else:
                subprocess.run("{0} -X utf8 -m transcrypt {1} -n -m".format(python_env, main_file), shell=True, check=True)
            list_all = glob(join(source, "*"))
            print("Coping scripts from __target__ to {0}\n".format(folder_script_apps_list))
            for y in list_all:
                if isfile(y):
                    script_file = join(
                        folder_script_apps_list, basename(y)
                    )
                    shutil.copy(
                        y,
                        script_file
                    )
                    if self.minify and not self.debug:
                        with open(script_file, "r", encoding="utf-8") as f:
                            lines_script = f.readlines()
                        if lines_script:
                            if lines_script[-1].startswith("//# sourceMappingURL"):
                                with open(script_file, "w", encoding="utf-8") as f:
                                    f.write("".join(lines_script[0:-1]))

        print("Finish!!!\n\n\n")

    def transcrypts_config(self, app=None):
        if app:
            self._has_config_changed[app] = self._process_transcrypt_config(app)
        else:
            for app in self.app_list:
                self._has_config_changed[app] = self._process_transcrypt_config(app)

    def _process_transcrypt_config(self, app):
        ignore_keys = [
            "transcrypt_main_file"
            "styles_main_file",
            "views_main_file",
            "host",
            "port"
        ]

        last_app_config = join(self.tempfolder, "project_config_{0}.json".format(app))
        path_app_config_file = self.path_app_config_file(app)
        CONFIG = {
            "PROJECT": {
                "name": self.config["PROJECT"]["name"],
                "title": self.config["PROJECT"]["title"],
                "version": self.config["PROJECT"]["version"],
                "compilation": self.config["PROJECT"]["compilation"],
                "versioning": self.config["PROJECT"]["versioning"],
                "debug": self.config["PROJECT"]["debug"],
                "author": self.config["PROJECT"]["author"],
            },
            "APP": {
            },
            "I18N": {
                "default_lang": self.config["PROJECT"].get("default_language", None)

            }
        }
        for x in self.config['FRONTEND'][app]:
            if x not in ignore_keys:
                CONFIG['APP'][x] = self.config['FRONTEND'][app][x]

        CONFIG['APP']['name'] = app

        ini = "\n".join([
            "# Created automatically.",
            "#",
            "# In development it may be necessary to add static data",
            "# to the client side application after compiling, use",
            "# the CONFIGJS section of the application's app.ini",
            "# file for this.",
            "#\n\n",
        ])
        i18n_files = join(self.projectpath, "frontapps", app, "languages")
        files = glob(join(i18n_files, "*.json"))
        i18n_languages = {"default_lang": self.config["PROJECT"].get("default_language", None)}
        for x in files:
            if basename(x) != "entries.json":
                lang = basename(x)[0:-5]
                with open(x, encoding="utf-8") as f:
                    translates = json.load(f)
                i18n_languages[lang] = translates
        CONFIG['I18N'] = i18n_languages
        end = "\n"
        content = "".join([ini, "CONFIG = {0}".format(json.dumps(CONFIG, ensure_ascii=True, indent=4)), end])
        content = re.sub(r"(:[\t\n\r ]{0,}true[\t\n\r ]{0,})[,}]", ": True,", content)
        content = re.sub(r"(:[\t\n\r ]{0,}false[\t\n\r ]{0,})[,}]", ": False,", content)
        content = re.sub(r"(:[\t\n\r ]{0,}null[\t\n\r ]{0,})[,}]", ": None,", content)
        with open(path_app_config_file, "w", encoding="utf-8") as f:
            f.write(content)
        if not isfile(last_app_config):
            with open(last_app_config, "w", encoding="utf-8") as f:
                new_c = json.dumps(self.config)
                new_c = json.loads(new_c)
                new_c["FRONTEND"] = {app: new_c["FRONTEND"][app]}
                json.dump(new_c, f, ensure_ascii=True, indent=2)
            return True
        else:
            with open(last_app_config, "r", encoding="utf-8") as f:
                v = json.load(f)
                new_v = v
                new_v['PROJECT']['compilation'] = self.config['PROJECT']['compilation']
                new_c = json.dumps(self.config, ensure_ascii=True)
                new_c = json.loads(new_c)
                new_c["FRONTEND"] = {app: new_c["FRONTEND"][app]}
                new_v["FRONTEND"] = {app: new_v["FRONTEND"][app]}

                if new_v == new_c:
                    if exists(join(self.tempfolder, "transcrypts_mtime_{0}.json".format(app))):
                        with open(join(self.tempfolder,
                                "transcrypts_mtime_{0}.json".format(app)), "r", encoding="utf-8") as f:
                            changes_register = json.load(f)
                        if path_app_config_file in changes_register:
                            changes_register[path_app_config_file] = getmtime(path_app_config_file)
                        with open(join(self.tempfolder,
                                "transcrypts_mtime_{0}.json".format(app)), "w", encoding="utf-8") as f:
                            json.dump(changes_register, f, ensure_ascii=True, indent=2)
                    return False
            with open(last_app_config, "w", encoding="utf-8") as f:
                new_c = json.dumps(self.config)
                new_c = json.loads(new_c)
                new_c["FRONTEND"] = {app: new_c["FRONTEND"][app]}
                json.dump(new_c, f, ensure_ascii=True, indent=2)
            return True

    def _save_mtimes(self):
        for app in self.app_list:
            content = {x: getmtime(x) for x in self.style_files(app)}
            with open(join(self.tempfolder,
                    "styles_mtime_{0}.json".format(app)), "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=True, indent=2)

            content = {x: getmtime(x) for x in self.extends_files(app)}
            with open(join(self.tempfolder,
                    "extends_mtime_{0}.json".format(app)), "w", encoding="utf-8") as f:
                if isinstance(content, dict):
                    json.dump(content, f, ensure_ascii=True, indent=2)
                else:
                    raise "The templates_mtime content must be dict type. Given: {0}".format(content)

            content = {x: getmtime(x) for x in self.templates_files(app)}
            with open(join(self.tempfolder,
                    "templates_mtime_{0}.json".format(app)), "w", encoding="utf-8") as f:
                if isinstance(content, dict):
                    json.dump(content, f, ensure_ascii=True, indent=2)
                else:
                    raise "The templates_mtime content must be dict type. Given: {0}".format(content)

            content = content = {x: getmtime(x) for x in self.static_files(app)}
            with open(join(self.tempfolder,
                    "statics_mtime_{0}.json".format(app)), "w", encoding="utf-8") as f:
                if isinstance(content, dict):
                    json.dump(content, f, ensure_ascii=True, indent=2)
                else:
                    raise "The statics_mtime content must be dict type. Given: {0}".format(content)

            content = {x: getmtime(x) for x in self.transcrypt_files(app)}
            with open(join(self.tempfolder,
                    "transcrypts_mtime_{0}.json".format(app)), "w", encoding="utf-8") as f:
                if isinstance(content, dict):
                    json.dump(content, f, ensure_ascii=True, indent=2)
                else:
                    raise "The scripts_mtime content must be dict type. Given: {0}".format(content)

            # content = {x: getmtime(x) for x in self.modules_files_monitor()}
            # with open(join(self.tempfolder,
            #         "phanterpwa_modules_mtime.json"), "w", encoding="utf-8") as f:
            #     json.dump(content, f, ensure_ascii=True, indent=2)

    def compile_by_step(self, app=None, full_compilation=False, minify=False):
        app_list = self.app_list
        if app:
            app_list = [app]
        for app in app_list:
            msg = "Transcrypt config"
            try:
                self.transcrypt_config(app)
                yield [msg, True, "Pass"]
            except Exception as e:
                yield [msg, False, traceback.format_tb(e.__traceback__)]
            current_debug = self.config["PROJECT"]["debug"]
            self.minify = self.config['PROJECT'].get("minify", False)
            # if current_debug:
            #     self.full_compilation = False
            # else:
            #     self.full_compilation = True
            # self._check_phanterpwa_modules()
            if full_compilation is not None:
                self.full_compilation = bool(full_compilation)
            if minify is not None:
                self.minify = bool(minify)
            msg = "Delete compiled app folder"
            try:
                self.delete_compiled_app_folder(app)
                yield [msg, True, "Pass"]
            except Exception as e:
                yield [msg, True, "".join(traceback.format_tb(e.__traceback__))]
            if current_debug or not exists(join(self.projectpath, "frontapps", app, "statics", "css", "phanterpwa.css")):
                msg = "Creating phanterpwa.css"
                try:
                    self.phanterpwa_usual_sass(app)
                    yield [msg, True, "Pass"]
                except Exception as e:
                    yield [msg, True, "".join(traceback.format_tb(e.__traceback__))]

            msg = "Copy statics"
            try:
                self.copy_statics(app)
                yield [msg, True, "Pass"]
            except Exception as e:
                yield [msg, True, "".join(traceback.format_tb(e.__traceback__))]
            msg = "Copy languages"
            try:
                self.copy_languages(app)
                yield [msg, True, "Pass"]
            except Exception as e:
                yield [msg, True, "".join(traceback.format_tb(e.__traceback__))]
            msg = "Compile styles"
            try:
                self.compile_styles(app)
                yield [msg, True, "Pass"]
            except Exception as e:
                yield [msg, True, "".join(traceback.format_tb(e.__traceback__))]
            msg = "Compile templates"
            try:
                self.compile_templates(app)
                yield [msg, True, "Pass"]
            except Exception as e:
                yield [msg, True, "".join(traceback.format_tb(e.__traceback__))]
            msg = "Compile transcrypts"
            try:
                self.compile_transcrypts(app)
                yield [msg, True, "Pass"]
            except Exception as e:
                yield [msg, True, "".join(traceback.format_tb(e.__traceback__))]
        self._save_mtimes()

    def compile(self,
        app=None, full_compilation=None,
        minify=None,
        force_transcrypt_compilation=True,
        ):

        app_list = self.app_list
        if app:
            app_list = [app]
        for app in app_list:
            self.transcrypts_config(app)
            print("\n============ APP COMPILATION: {0} ==============".format(app))
            current_debug = self.config["PROJECT"]["debug"]
            self.minify = self.config["PROJECT"].get("minify", False)
            print("DEBUG:", current_debug, "\t\t MINIFY:", self.minify)
            # if current_debug:
            #     self.full_compilation = False
            # else:
            #     self.full_compilation = True
            # self._check_phanterpwa_modules()
            if full_compilation is not None:
                self.full_compilation = bool(full_compilation)
            if minify is not None:
                self.minify = bool(minify)
            self.delete_compiled_app_folder(app)
            self.phanterpwa_usual_sass(app)
            self.copy_languages(app)
            self.compile_templates(app)
            self.copy_statics(app)
            self.compile_styles(app)
            self.compile_transcrypts(app)
        self._save_mtimes()
