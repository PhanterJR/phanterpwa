import os
import re
import sys
import glob
import shutil
import psutil
import subprocess
import appdirs
import tempfile
import json
from pathlib import PurePath
from phanterpwa.tools import (
    config,
    interpolate,
    check_requeriments
)
from phanterpwa.configer import ProjectConfig
from phanterpwa.tests.tests import run as test
from phanterpwa.i18n import Translator
from phanterpwa import __version__ as PHANTERPWA_VERSION
from phanterpwa import compiler

ENV_PYTHON = os.path.normpath(sys.executable)
ENV_PATH = os.path.normpath(os.path.dirname(ENV_PYTHON))
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")
PY_VERSION = "{0}.{1}.{2}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])
CURRENT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__)))
Trans = Translator(os.path.join(CURRENT_DIR, "langs"), "cli", debug=True)
Trans.add_language("portuguese")
Trans.add_language("english")

T = Trans.T
_About = ""
with open(os.path.join(CURRENT_DIR, "..", "samples", "about_cli"), 'r', encoding='utf-8') as f:
    _About = f.read()
_About = interpolate(_About, {"VERSION": PHANTERPWA_VERSION})


class Alerts:
    def __init__(self, alert=""):
        self.alert = alert

    @property
    def alert(self):
        return self._alert

    @alert.setter
    def alert(self, value):
        self._alert = value

    def __repr__(self):
        return self.alert

    def __str__(self):
        return self.alert

    def __bool__(self):
        return bool(self.alert)


class Projects():
    def __init__(self, projects_path):
        self.projects_path = projects_path
        self._projects_list = []

    @property
    def projects_list(self):
        self._find_projects_list()
        return self._projects_list

    def _valid_project_name(self, projectname: str) -> bool:
        if isinstance(projectname, str):
            if projectname.isidentifier():
                return True
        return False

    def _find_projects_list(self) -> list:
        self._projects_list = []
        files_and_paths = glob.glob(os.path.join(self.projects_path, "*"))
        for x in files_and_paths:
            if self._is_project(x):
                project_identifier = os.path.basename(x)
                if self._valid_project_name(project_identifier):
                    self._projects_list.append((project_identifier, x))
        return self._projects_list

    def _is_project(self, path: str) -> bool:
        if os.path.isdir(path):
            conf_file = os.path.join(path, 'config.json')
            if os.path.isfile(conf_file):
                conf = config(conf_file)
                is_pro = conf.get("CONFIG_INDENTIFY", False)
                if is_pro == "project_config":
                    return True
        return False


def package_project_app(project_path, target, reset_config=True):
    file_name = os.path.basename(project_path)
    compact_temp = os.path.join(tempfile.gettempdir(), 'phanterpwa')
    temp_file = os.path.join(compact_temp, file_name)
    os.makedirs(compact_temp, exist_ok=True)
    if os.path.exists(temp_file):
        shutil.rmtree(temp_file)
    print(os.path.join(temp_file, "frontapps", '*', 'www'))
    shutil.copytree(
        project_path,
        temp_file,
        ignore=shutil.ignore_patterns(
            '*.pyc',
            '.*',
            '*.sublime-workspace',
            '*.sublime-project',
            '__target__',
            '__pycache__',
            'secret.ini',
        )
    )
    for x in glob.glob(os.path.join(temp_file, "frontapps", '*', 'www')):
        if os.path.isdir(x):
            shutil.rmtree(x)
    if os.path.isdir(os.path.join(temp_file, 'api', 'uploads')):
        shutil.rmtree(os.path.join(temp_file, 'api', 'uploads'))
    if os.path.isdir(os.path.join(temp_file, 'api', 'databases')):
        shutil.rmtree(os.path.join(temp_file, 'api', 'databases'))
    if os.path.isdir(os.path.join(temp_file, 'temp')):
        shutil.rmtree(os.path.join(temp_file, 'temp'))
    if os.path.isdir(os.path.join(temp_file, 'logs')):
        shutil.rmtree(os.path.join(temp_file, 'logs'))
    if os.path.isfile(os.path.join(temp_file, 'config.json')):
        os.remove(os.path.join(temp_file, 'config.json'))
    if os.path.exists("{0}\\**\\.gitattributes".format(temp_file)):
        os.remove("{0}\\**\\.gitattributes".format(temp_file))

    if os.path.exists("{0}\\**\\.gitignore".format(temp_file)):
        os.remove("{0}\\**\\.gitignore".format(temp_file))

    os.makedirs(os.path.join(temp_file, "api", "uploads"), exist_ok=True)
    os.makedirs(os.path.join(temp_file, "api", "databases"), exist_ok=True)
    os.makedirs(os.path.join(temp_file, "logs"), exist_ok=True)

    shutil.make_archive(os.path.join(os.path.join(compact_temp), file_name), 'zip', temp_file)
    shutil.copyfile(
        os.path.join(compact_temp, "{0}.zip".format(file_name)),
        os.path.join(target, "{0}.ppwa".format(file_name))
    )


class Cli():
    def __init__(self):
        self.Projects = None
        self.ProjectConfig = None
        self.projects_list = []
        self.switch = True
        self._message = []
        self._init_appdata_dir()
        self.start()

    @property
    def message(self):
        if self._message:
            l_msg = self._message
            for msg in self._message:
                print(self.title(T(msg), char=" "))
            print(self.title(char="_"))
            self._message = []
            return l_msg

    @message.setter
    def message(self, msg):
        if isinstance(msg, str):
            self._message.append(msg)
        elif isinstance(msg, list):
            self._message = [x for x in msg if isinstance(msg, str)]
        else:
            self._message = []

    def _change_projects_folder(self, path):
        if os.path.isdir(path):
            config(self._projectdata_dir_cli)
            return path

        return None

    def start(self):
        self.switch = True
        self.clear()
        self.projects_list = []
        self.interfaceConfig = config(self._projectdata_dir_cli)
        if "language" in self.interfaceConfig:
            Trans.direct_translation = self.interfaceConfig["language"]
        self._projects_path = None
        if "applications_folder" in self.interfaceConfig:
            self._projects_path = self.interfaceConfig["applications_folder"]
            self.Projects = Projects(self._projects_path)
        print("\n")
        with open(os.path.join(CURRENT_DIR, "..", "samples", "art_cli"), "r") as f:
            print(f.read())
        print(self.title(size=67, char="_"))
        print(_About)
        try:
            print(self.title(T("Press <ENTER> key to continue (CTRL+C to interrupt)"), size=67, char=" "))
            input("".join([" " * 33]))
            self.clear()
            while self.switch:
                if not self.Projects:
                    print("First you must define a folder where applications will be stored.")
                    f = input("".join([T("Please enter the address where your applications will be stored."), "\n-> "]))
                    while not os.path.exists(f):
                        f = input("".join([T("The folder does not exist! Please enter the valid address."), "\n-> "]))
                    else:
                        self.interfaceConfig["applications_folder"] = f
                        config(self._projectdata_dir_cli, self.interfaceConfig)
                        self._projects_path = f
                        self.Projects = Projects(self._projects_path)

                while True:
                    self.clear()
                    print(self.title("PhanterPWA - Developer", char="|"))
                    print()
                    print(self.title(T("Enviroment")))
                    print()
                    print("  {0}: {1}".format(T("Path"), ENV_PATH))
                    print("  Python: {0}".format(ENV_PYTHON))
                    print(
                        "  {0}: {1}".format(T("Python version"), PY_VERSION),
                        "                {0}: {1}".format(T("PhanterPWA version"), PHANTERPWA_VERSION)
                    )
                    print("  {0}: {1}".format(T("Projects Folder"), self._projects_path))
                    print()
                    print(self.title(char="-"))
                    print()
                    print(self.title(T("Menu")))
                    print()
                    print("  [C] -", T("Change project folder"), "               [R] -", "Check requeriments")
                    print("  [L] -", T("Language"))
                    print("  [T] -", T("Tests"))
                    print(self.title("[Q] - {0}".format(T("Quit")), char=" "))
                    print()
                    print(self.title(T("Project List")))
                    print()
                    projects = self.Projects.projects_list
                    self.projects_list = projects
                    if projects:
                        l_app = []
                        for n, a in enumerate(projects):
                            l_app.append(a[0])
                            print("  [{0}] - {1} - {2}".format(n, a[0], a[1]))
                    else:
                        print(T("No installed projects found"))
                    print()
                    print(self.title(char="-"))
                    self.message
                    e = input("".join(["  ", T("What do you want to do?"), " "]))
                    print(self.title())
                    if e.strip() == "Q" or e.strip() == "q":
                        self.clear()
                        print("\nGoodbye!")
                        self.switch = False
                        break
                    elif e == "L" or e == "l":
                        self.interface_translate()
                    elif e == "R" or e == "r":
                        self._check_requeriments()
                    elif e == "T" or e == "t":
                        self._tests()
                        input("".join([T("press <ENTER> to continue."), "\n -> "]))
                    elif e == "c" or e == "C":
                        self.interface_project_folder()
                    else:
                        v = None
                        try:
                            e_int = int(e)
                            v = l_app[e_int]
                        except Exception:
                            self.message = T("The value is invalid! Try again!")
                        if v:
                            self.switch = self.project_menu(
                                self.Projects.projects_list[e_int][0], self.Projects.projects_list[e_int][1]
                            )
                            if self.switch is False:
                                break
                    break
                    print("Goodbye!")

        except KeyboardInterrupt:
            self.clear()
            print("\nGoodbye!")
            self.clear()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        pass

    def _tests(self):
        self.clear()
        print(self.title(T("Tests"), char="="))
        try:
            test()
        except Exception:
            input(T("There was a problem, check the output above. Press <ENTER> to continue."))
        else:
            self.message = T("All tests pass")

    def _check_requeriments(self):
        self.clear()
        print(self.title(T("Check requirements"), char="="))
        res = check_requeriments()
        has_problem = False
        for x in res:
            name = x[0]
            size = len(name)
            if size > 70:
                name = name[0:70]
                size = 70
            if not x[1]:
                has_problem = True
            print("\n{0} {1} {2}\n".format(name, "." * (71 - size), T("Pass") if x[1] else T("Fail")))
        if has_problem:
            print(self.title(T("Resume"), char="-"))
            input(T("There was a problem, check the output above. Press <ENTER> to continue."))
        else:
            self.message = T("All requirements are present!")

    def _init_appdata_dir(self):
        self._projectdata_dir = os.path.join(appdirs.user_data_dir(), "phanterpwa")
        self._projectdata_dir_cli = os.path.join(self._projectdata_dir, "cli")
        self._projectdata_dir_gui = os.path.join(self._projectdata_dir, "gui")
        if not os.path.isdir(self._projectdata_dir):
            self._tests()
            self._check_requeriments()
            os.makedirs(self._projectdata_dir, exist_ok=True)
        if not os.path.isdir(self._projectdata_dir_cli):
            os.makedirs(self._projectdata_dir_cli, exist_ok=True)
        if not os.path.isdir(self._projectdata_dir_gui):
            os.makedirs(self._projectdata_dir_gui, exist_ok=True)

    def start_server(self, projectPath):
        target = os.path.normpath(os.path.join(CURRENT_DIR, "..", "server.py"))
        command = " ".join([ENV_PYTHON, target])
        subprocess.run(command, cwd=projectPath, shell=True)

    def title(self, title="", size=79, char="="):
        title = str(title)
        r = size - (len(title) + 2)
        r = r // 2
        if title:
            return "{0} {1} {0}".format(char * r, title)
        else:
            return char * size

    def interface_project_folder(self):
        exit = False
        while not exit:
            exists_path = False
            while not exists_path:
                self.clear()
                print(self.title(T('Project Folder'), char="|"))
                print()
                print(T("Current Folder:"), config(self._projectdata_dir_cli)['applications_folder'])
                print(self.title("", char="-"))
                self.message
                e = input("".join([T("Enter the folder path and press <ENTER> or 'E' to exit."), "\n -> "]))
                if e == "e" or e == "E":
                    exit = exists_path = True
                elif e == "":
                    self.message = T("The path can't empty.")
                else:
                    try:
                        if os.path.exists(e) and os.path.isdir(e):
                            exists_path = True
                        else:
                            raise IOError("Invalid path!")
                    except Exception:
                        self.message = T("The path does not exist or is not a folder, try again!")
                    else:
                        if e:
                            config(self._projectdata_dir_cli, {"applications_folder": e})
                            self.interfaceConfig["applications_folder"] = e
                            self._projects_path = e
                            self.Projects = Projects(e)
                        exit = True

    def project_menu(self, project_name, project_path):
        is_run = True
        self.ProjectConfig = ProjectConfig(os.path.join(project_path, "config.json"))
        self.ProjectConfig.save()
        while True:
            self.clear()
            print(self.title("PhanterPWA - Project", char="|"))
            print()
            print(self.title(T("Summary")))
            print()
            print("  {0}: {1}".format(T("Path"), project_path))
            print("  {0}: {1}".format(T("Identifier Name"), project_name))
            print("  {0}: {1}".format(T("Title"), self.ProjectConfig['PROJECT']['title']))
            print("  {0}: {1}".format(T("Author"), self.ProjectConfig['PROJECT']['author']))
            print(
                "  {0}: {1}".format(T("Version"), self.ProjectConfig['PROJECT']['version']),
                "                {0}: {1}".format(T("Compilation"), self.ProjectConfig['PROJECT']['compilation'])
            )
            print("  {0}: {1}".format(T("Debug"), self.ProjectConfig['PROJECT']['debug']))
            print()
            print(self.title(T("Actions")))
            print()
            print("  [C] -", T("Project Config"), "                         [A] -", T("Api Config"))
            print("  [O] -", T("Compile"), "                                [P] -", T("Package"))
            print("  [D] -", T("Delete"), "                                 [S] -", T("Start Server"))
            print(self.title("[E] - {0}".format(T("Exit")), char=" "))
            print()
            print(self.title(T("App List")))
            print()
            cont = 0
            app_list = list(self.ProjectConfig["FRONTEND"].keys())
            for a in app_list:
                path_app = os.path.join(project_path, "frontapps", a)
                print("  [{0}] - {1} - {2}".format(cont, a, path_app))
                cont += 1

            print()
            print(self.title(char="-"))

            self.message
            c = input("".join(["  ", T("What do you want to do?"), " "]))
            if c == "E" or c == "e":
                break
            elif c == "C" or c == "c":
                self._menu_config_project(project_path)
            elif c == "A" or c == "a":
                self._menu_config_api(project_path)
            elif c == "O" or c == "o":

                compi = compiler.Compiler(project_path)

                try:
                    compi.compile()
                except Exception:
                    self.message = T("Compilation Error, check the log file to learn more.")
                    self.clear()
                else:
                    input("".join([T("Sucess"), "! ", T("Press <ENTER> key to continue.")]))
                    self.clear()

            elif c == "D" or c == "d":
                confirm = input(T("Press \"Y\" and <ENTER> to continue."))
                if confirm == "y" or confirm == "Y":
                    if os.path.exists(project_path):
                        try:
                            # shutil.rmtree(project_path)
                            self.message = T("Project \"{0}\" deleted!".format(project_name))
                            break
                        except Exception:
                            self.message = T("Deleting application path error, check the log file to learn more.")
                            self.clear()
            elif c == "P" or c == "p":
                print(
                    T("Packing on"),
                    os.path.normpath(os.path.join(os.path.dirname(project_name),
                        "{0}.ppwa".format(os.path.basename(project_name))))
                )
                try:
                    package_project_app(project_path, os.path.dirname(project_path))
                except Exception as e:
                    print(e)
                    input()
                    self.message = T("Packing error, check the log file to learn more.")
                    self.clear()
                else:
                    self.message = "".join([
                        T("Sucess!"), " ", T("The package was created at"), " ",
                        os.path.join(project_path, "{0}.ppwa".format(project_name))
                    ])
                    self.clear()
            elif c == "S" or c == "s":
                try:
                    print("Press CTRL+C to stop server!")
                    self.start_server(project_path)
                except KeyboardInterrupt:
                    target = os.path.abspath(os.path.join("..", "server.py"))
                    for p in psutil.process_iter():
                        cmd_line = None
                        try:
                            cmd_line = p.cmdline()
                        except Exception:
                            pass
                        if cmd_line:
                            if ENV_PYTHON == cmd_line[0]:
                                if os.path.normpath(target) == cmd_line[-1]:
                                    p.terminate()
                    self.clear()
                    input("".join([T("Server Stoped"), "!. ", T("Press <ENTER> key to continue.")]))
                    self.clear()
                except Exception as e:
                    self.message = "".join([T("Server error."), str(e)])
                    self.clear()
            else:
                try:
                    choice = int(c)
                    app_choiced = app_list[choice]
                except Exception:
                    self.message = T("Invalid choice!")
                else:
                    self.app_menu(app_choiced, project_path)
        return is_run

    def app_menu(self, app_name, project_path):
        self.ProjectConfig = ProjectConfig(os.path.join(project_path, "config.json"))
        while True:
            self.clear()
            print(self.title("PhanterPWA - Application", char="|"))
            print()
            print(self.title(T("Summary")))
            print()
            print("  {0}: {1}".format(T("Path"), os.path.join(project_path, "frontapps", app_name)))
            print("  {0}: {1}".format(T("Identifier Name"), app_name))
            print("  {0}: {1}".format(T("Title"), self.ProjectConfig["FRONTEND"][app_name]['title']))
            print()
            print(self.title(T("Actions")))
            print()
            print("  [C] -", T("App Config"))
            print("  [D] -", T("Delete"))
            print(self.title("[E] - {0}".format(T("Exit")), char=" "))
            print()
            c = "E"
            print(self.title(char="-"))
            self.message
            c = input("".join(["  ", T("What do you want to do?"), " "]))
            if c == "E" or c == "e":
                break
            elif c == "C" or c == "c":
                self._menu_config_app(project_path, app_name)
            elif c == "D" or c == "d":
                self.message = T("Not Implemented!")
            else:
                self.message = T("Invalid choice!")

    def _menu_config_project(self, project_path):
        self.ProjectConfig = ProjectConfig(os.path.join(project_path, "config.json"))
        while True:
            self.clear()
            print(self.title(T("Project Config")))
            print()
            print("  File: {0}".format(os.path.join(project_path, "project.ini")))
            cont = 0
            switch = {}
            for x in self.ProjectConfig.project_ini.sections():
                print("  [{0}] - {1}".format(cont, x))
                switch[cont] = x
                cont += 1
            print()
            print(self.title(char="-"))
            print()
            limit = cont
            print("  File: {0}".format(os.path.join(project_path, "secret.ini")))
            try:
                sect = self.ProjectConfig.secret_ini.sections()
            except:
                sect = []
            for x in sect:
                print("  [{0}] - {1}".format(cont, x))
                switch[cont] = x
                cont += 1
            print()
            print(self.title(char="-"))
            print()
            print(self.title("[E] - {0}".format(T("Exit")), char=" "))
            print()
            print(self.title(T("You can use an editor like vim to edit the configuration file"), char=" "))
            print()
            print(self.title(char="-"))
            self.message
            c = input("".join(["  ", T("What do you want to do?"), " "]))
            if c == "E" or c == "e":
                break
            elif c.isdigit() and int(c) in switch:
                app_choiced = switch[int(c)]
                if int(c) < limit:
                    self._menu_config_project_item(project_path, app_choiced)
                else:
                    self._menu_config_secret_item(project_path, app_choiced)

            else:
                self.message = T("Invalid choice!")
            self.clear()

    def _menu_config_api(self, project_path):
        self.ProjectConfig = ProjectConfig(os.path.join(project_path, "config.json"))
        while True:
            self.clear()
            print(self.title(T("Api Config")))
            print()
            print("  File: {0}".format(os.path.join(project_path, "api", "api.ini")))
            cont = 0
            switch = {}
            for x in self.ProjectConfig.api_ini.sections():
                print("  [{0}] - {1}".format(cont, x))
                switch[cont] = x
                cont += 1
            print()
            print(self.title(char="-"))
            print()
            print(self.title("[E] - {0}".format(T("Exit")), char=" "))
            print()
            print(self.title(T("You can use an editor like vim to edit the configuration file"), char=" "))
            print()
            print(self.title(char="-"))
            self.message
            c = input("".join(["  ", T("What do you want to do?"), " "]))
            if c == "E" or c == "e":
                break
            elif c.isdigit() and int(c) in switch:
                app_choiced = switch[int(c)]
                self._menu_config_api_item(project_path, app_choiced)
            else:
                self.message = T("Invalid choice!")
            self.clear()

    def _menu_config_app(self, project_path, app_name):
        self.ProjectConfig = ProjectConfig(os.path.join(project_path, "config.json"))
        while True:
            self.clear()
            print(self.title("".join([T("Application"), " (", app_name, ") ", T("config")])))
            print()
            print("  File: {0}".format(os.path.join(project_path, "frontapps", app_name, "app.ini")))
            cont = 0
            switch = {}
            app_ini = self.ProjectConfig.apps_ini.get(app_name, {})
            if app_ini:
                for x in app_ini.sections():
                    print("  [{0}] - {1}".format(cont, x))
                    switch[cont] = x
                    cont += 1
                print()
                print(self.title(char="-"))
                print()
                print(self.title("[E] - {0}".format(T("Exit")), char=" "))
                print()
                print(self.title(T("You can use an editor like vim to edit the configuration file"), char=" "))
                print()
                print(self.title(char="-"))
                self.message
                c = input("".join(["  ", T("What do you want to do?"), " "]))
                if c == "E" or c == "e":
                    break
                elif c.isdigit() and int(c) in switch:
                    app_choiced = switch[int(c)]
                    self._menu_config_app_item(project_path, app_name, app_choiced)
                else:
                    self.message = T("Invalid choice!")
                self.clear()
            else:
                self.message = T("Config file not found!")
                break

    def _menu_config_api_item(self, project_path, section):
        self.ProjectConfig = ProjectConfig(os.path.join(project_path, "config.json"))
        while True:
            self.clear()
            print(self.title("".join([T("Project Config - Section:"), " ", section])))
            print()
            print("  File: {0}".format(os.path.join(project_path, 'api', "api.ini")))
            cont = 0
            switch = {}
            for x in self.ProjectConfig.api_ini[section]:
                print("  [{0}] - {1}: {2}".format(cont, x, self.ProjectConfig.api_ini[section].get(x)))
                switch[cont] = x
                cont += 1
            print(self.title("[E] - {0}".format(T("Exit")), char=" "))
            print()
            print(self.title(char="-"))
            self.message
            c = input("".join([T("Which field do you want to change?"), " "]))
            if c == "E" or c == "e":
                break
            elif c.isdigit() and int(c) in switch:
                app_choiced = switch[int(c)]
                boolean_fields = []
                is_not_empty = []
                regex_fields = {}
                code_fields = []
                boolean_fields = []
                is_integer = []
                if section == "API":
                    is_integer = [
                        "default_time_user_token_expire",
                        "default_time_user_token_expire_remember_me",
                        "default_time_csrf_token_expire",
                        "default_time_temporary_password_expire",
                        "timeout_to_resend_temporary_password_mail",
                        "default_time_client_token_expire",
                        "default_time_activation_code_expire",
                        "wait_time_to_try_activate_again",
                        "timeout_to_resend_activation_email",
                        "timeout_to_resign",
                        "timeout_to_next_login_attempt",
                        "max_login_attempts",
                        "max_activation_attempts",

                        "port",
                        "default_time_two_factor_code_expire",
                    ]
                    is_not_empty = ["host"]
                elif section == "DEVELOPMENT" or section == "PRODUCTION":
                    is_not_empty = ["remote_address",
                        "websocket_address"]

                if app_choiced in code_fields:
                    msg = T("Please enter \"Y\" to create a new code.")
                    print(msg)
                    new_value = input("".join([app_choiced, ": "]))
                    if new_value == "Y" or new_value == "y":
                        new_value = os.urandom(12).hex()
                        self.ProjectConfig.api_ini[section][app_choiced] = new_value
                    else:
                        self.message = T("Nothing changed!")
                elif app_choiced in is_integer:
                    print(T("Please enter the new value in the field below:"))
                    new_value = input("".join([app_choiced, ": "]))
                    if app_choiced.isdigit():
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.api_ini[section][app_choiced] = new_value
                    else:
                        self.message = T("Nothing changed!")
                elif app_choiced in boolean_fields:
                    msg = T("Please enter 0 for False and 1 for True in the fields below.")
                    print(msg)
                    new_value = input("".join([app_choiced, ": "]))
                    if new_value == "1" or new_value == "true" or new_value == "True":
                        new_value = "True"
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.api_ini[section][app_choiced] = new_value
                    elif new_value == "0" or new_value == "false" or new_value == "False":
                        new_value = "False"
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.api_ini[section][app_choiced] = new_value
                    else:
                        self.message = "".join([T("Error! The \""), app_choiced, T("\" must be \"0\" or \"1\"")])
                elif app_choiced in regex_fields:
                    print(T("Please enter the new value in the field below:"))
                    new_value = input("".join([app_choiced, ": "]))
                    re_res = re.match(regex_fields[app_choiced], new_value)
                    print(re_res)
                    if re_res:
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.api_ini[section][app_choiced] = new_value
                    else:
                        self.message = "".join([
                            T("The "), app_choiced, T(" not match!"), " (regex: \"", regex_fields[app_choiced], "\")"])
                else:
                    print(T("Please enter the new value in the field below:"))
                    new_value = input("".join([app_choiced, ": "]))
                    if app_choiced in is_not_empty:
                        if new_value:
                            self.message = "".join([app_choiced, " ", T("changed!")])
                            self.ProjectConfig.api_ini[section][app_choiced] = new_value
                        else:
                            self.message = "".join([T("The "), app_choiced, T(" value is not Empty!")])
                    else:
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.api_ini[section][app_choiced] = new_value
                with open(os.path.join(project_path, 'api', 'api.ini'), 'w', encoding="utf-8") as configfile:
                    self.ProjectConfig.api_ini.write(configfile)
                self.ProjectConfig.save()
            else:
                self.message = T("Invalid choice!")
            self.clear()

    def _menu_config_app_item(self, project_path, app_name, section):
        self.ProjectConfig = ProjectConfig(os.path.join(project_path, "config.json"))
        while True:
            self.clear()
            print(self.title("".join([T("Application"), " (", app_name, ") ", T("Config - Section:"), " ", section])))
            print()
            print("  File: {0}".format(os.path.join(project_path, "frontapps", app_name, "app.ini")))
            cont = 0
            switch = {}
            app_ini = self.ProjectConfig.apps_ini.get(app_name, {})
            if app_ini:
                for x in app_ini[section]:
                    print("  [{0}] - {1}: {2}".format(cont, x, app_ini[section].get(x)))
                    switch[cont] = x
                    cont += 1
                print(self.title("[E] - {0}".format(T("Exit")), char=" "))
                print()
                print(self.title(char="-"))
                self.message
                c = input("".join([T("Which field do you want to change?"), " "]))
                if c == "E" or c == "e":
                    break
                elif c.isdigit() and int(c) in switch:
                    app_choiced = switch[int(c)]
                    boolean_fields = []
                    is_not_empty = []
                    regex_fields = {}
                    code_fields = []
                    boolean_fields = []
                    is_integer = []
                    if section == "APP":
                        is_integer = [
                            "timeout_to_resign",
                        ]
                        is_not_empty = [
                            "title",
                            "transcrypt_main_file",
                            "styles_main_file",
                            "views_main_file",
                        ]


                    if app_choiced in code_fields:
                        msg = T("Please enter \"Y\" to create a new code.")
                        print(msg)
                        new_value = input("".join([app_choiced, ": "]))
                        if new_value == "Y" or new_value == "y":
                            new_value = os.urandom(12).hex()
                            app_ini[section][app_choiced] = new_value
                        else:
                            self.message = T("Nothing changed!")
                    elif app_choiced in is_integer:
                        print(T("Please enter the new value in the field below:"))
                        new_value = input("".join([app_choiced, ": "]))
                        if app_choiced.isdigit():
                            self.message = "".join([app_choiced, " ", T("changed!")])
                            app_ini[section][app_choiced] = new_value
                        else:
                            self.message = T("Nothing changed!")
                    elif app_choiced in boolean_fields:
                        msg = T("Please enter 0 for False and 1 for True in the fields below.")
                        print(msg)
                        new_value = input("".join([app_choiced, ": "]))
                        if new_value == "1" or new_value == "true" or new_value == "True":
                            new_value = "True"
                            self.message = "".join([app_choiced, " ", T("changed!")])
                            app_ini[section][app_choiced] = new_value
                        elif new_value == "0" or new_value == "false" or new_value == "False":
                            new_value = "False"
                            self.message = "".join([app_choiced, " ", T("changed!")])
                            app_ini[section][app_choiced] = new_value
                        else:
                            self.message = "".join([T("Error! The \""), app_choiced, T("\" must be \"0\" or \"1\"")])
                    elif app_choiced in regex_fields:
                        print(T("Please enter the new value in the field below:"))
                        new_value = input("".join([app_choiced, ": "]))
                        re_res = re.match(regex_fields[app_choiced], new_value)
                        print(re_res)
                        if re_res:
                            self.message = "".join([app_choiced, " ", T("changed!")])
                            app_ini[section][app_choiced] = new_value
                        else:
                            self.message = "".join([
                                T("The "), app_choiced, T(" not match!"), " (regex: \"", regex_fields[app_choiced], "\")"])
                    else:
                        print(T("Please enter the new value in the field below:"))
                        new_value = input("".join([app_choiced, ": "]))
                        if app_choiced in is_not_empty:
                            if new_value:
                                self.message = "".join([app_choiced, " ", T("changed!")])
                                app_ini[section][app_choiced] = new_value
                            else:
                                self.message = "".join([T("The "), app_choiced, T(" value is not Empty!")])
                        else:
                            self.message = "".join([app_choiced, " ", T("changed!")])
                            app_ini[section][app_choiced] = new_value
                    with open(os.path.join(project_path, "frontapps", app_name, "app.ini"), 'w', encoding="utf-8") as configfile:
                        app_ini.write(configfile)
                    self.ProjectConfig.save()
                else:
                    self.message = T("Invalid choice!")
                self.clear()

    def _menu_config_project_item(self, project_path, section):
        self.ProjectConfig = ProjectConfig(os.path.join(project_path, "config.json"))
        while True:
            self.clear()
            print(self.title("".join([T("Project Config - Section:"), " ", section])))
            print()
            print("  File: {0}".format(os.path.join(project_path, "project.ini")))
            cont = 0
            switch = {}
            for x in self.ProjectConfig.project_ini[section]:
                print("  [{0}] - {1}: {2}".format(cont, x, self.ProjectConfig.project_ini[section].get(x)))
                switch[cont] = x
                cont += 1
            print(self.title("[E] - {0}".format(T("Exit")), char=" "))
            print()
            print(self.title(char="-"))
            self.message
            c = input("".join([T("Which field do you want to change?"), " "]))
            if c == "E" or c == "e":
                break
            elif c.isdigit() and int(c) in switch:
                app_choiced = switch[int(c)]
                boolean_fields = []
                is_not_empty = []
                regex_fields = {}
                code_fields = []
                boolean_fields = []
                if section == "PROJECT":
                    boolean_fields = ["debug"]
                    is_not_empty = ["title", "author"]
                    regex_fields = {
                        "version": r"[0-9]{0,}.[0-9]{0,}.[0-9]{0,}"
                    }
                elif section == "EMAIL":
                    boolean_fields = ["use_tls", "use_ssl"]
                    is_integer = ["port"]
                    is_not_empty = ["server",
                        "username",
                        "default_sender"]

                if app_choiced in code_fields:
                    msg = T("Please enter \"Y\" to create a new code.")
                    print(msg)
                    new_value = input("".join([app_choiced, ": "]))
                    if new_value == "Y" or new_value == "y":
                        new_value = os.urandom(12).hex()
                        self.ProjectConfig.project_ini[section][app_choiced] = new_value
                    else:
                        self.message = T("Nothing changed!")
                elif app_choiced in is_integer:
                    print(T("Please enter the new value in the field below:"))
                    new_value = input("".join([app_choiced, ": "]))
                    if app_choiced.isdigit():
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.project_ini[section][app_choiced] = new_value
                    else:
                        self.message = T("Nothing changed!")
                elif app_choiced in boolean_fields:
                    msg = T("Please enter 0 for False and 1 for True in the fields below.")
                    print(msg)
                    new_value = input("".join([app_choiced, ": "]))
                    if new_value == "1" or new_value == "true" or new_value == "True":
                        new_value = "True"
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.project_ini[section][app_choiced] = new_value
                    elif new_value == "0" or new_value == "false" or new_value == "False":
                        new_value = "False"
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.project_ini[section][app_choiced] = new_value
                    else:
                        self.message = "".join([T("Error! The \""), app_choiced, T("\" must be \"0\" or \"1\"")])
                elif app_choiced in regex_fields:
                    print(T("Please enter the new value in the field below:"))
                    new_value = input("".join([app_choiced, ": "]))
                    re_res = re.match(regex_fields[app_choiced], new_value)
                    print(re_res)
                    if re_res:
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.project_ini[section][app_choiced] = new_value
                    else:
                        self.message = "".join([
                            T("The "), app_choiced, T(" not match!"), " (regex: \"", regex_fields[app_choiced], "\")"])
                else:
                    print(T("Please enter the new value in the field below:"))
                    new_value = input("".join([app_choiced, ": "]))
                    if app_choiced in is_not_empty:
                        if new_value:
                            self.message = "".join([app_choiced, " ", T("changed!")])
                            self.ProjectConfig.project_ini[section][app_choiced] = new_value
                        else:
                            self.message = "".join([T("The "), app_choiced, T(" value is not Empty!")])
                    else:
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.project_ini[section][app_choiced] = new_value
                with open(os.path.join(project_path, 'project.ini'), 'w', encoding="utf-8") as configfile:
                    self.ProjectConfig.project_ini.write(configfile)
                self.ProjectConfig.save()
            else:
                self.message = T("Invalid choice!")
            self.clear()

    def _menu_config_secret_item(self, project_path, section):
        self.ProjectConfig = ProjectConfig(os.path.join(project_path, "config.json"))
        while True:
            self.clear()
            print(self.title("".join([T("Secret Config - Section:"), " ", section])))
            print()
            print("  File: {0}".format(os.path.join(project_path, "secret.ini")))
            cont = 0
            switch = {}
            for x in self.ProjectConfig.secret_ini[section]:
                print("  [{0}] - {1}: {2}".format(cont, x, self.ProjectConfig.secret_ini[section].get(x)))
                switch[cont] = x
                cont += 1
            print(self.title("[E] - {0}".format(T("Exit")), char=" "))
            print()
            print(self.title(char="-"))
            self.message
            c = input("".join([T("Which field do you want to change?"), " "]))
            if c == "E" or c == "e":
                break
            elif c.isdigit() and int(c) in switch:
                app_choiced = switch[int(c)]
                boolean_fields = []
                is_not_empty = []
                regex_fields = {}
                code_fields = []
                boolean_fields = []
                is_integer = []
                if section == "API":
                    code_fields = ["secret_key", "url_secret_key"]
                elif section == "EMAIL":
                    is_not_empty = ["password"]

                if app_choiced in code_fields:
                    msg = T("Please enter \"Y\" to create a new code.")
                    print(msg)
                    new_value = input("".join([app_choiced, ": "]))
                    if new_value == "Y" or new_value == "y":
                        new_value = os.urandom(12).hex()
                        self.ProjectConfig.secret_ini[section][app_choiced] = new_value
                    else:
                        self.message = T("Nothing changed!")
                elif app_choiced in is_integer:
                    print(T("Please enter the new value in the field below:"))
                    new_value = input("".join([app_choiced, ": "]))
                    if app_choiced.isdigit():
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.secret_ini[section][app_choiced] = new_value
                    else:
                        self.message = T("Nothing changed!")
                elif app_choiced in boolean_fields:
                    msg = T("Please enter 0 for False and 1 for True in the fields below.")
                    print(msg)
                    new_value = input("".join([app_choiced, ": "]))
                    if new_value == "1" or new_value == "true" or new_value == "True":
                        new_value = "True"
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.secret_ini[section][app_choiced] = new_value
                    elif new_value == "0" or new_value == "false" or new_value == "False":
                        new_value = "False"
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.secret_ini[section][app_choiced] = new_value
                    else:
                        self.message = "".join([T("Error! The \""), app_choiced, T("\" must be \"0\" or \"1\"")])
                elif app_choiced in regex_fields:
                    print(T("Please enter the new value in the field below:"))
                    new_value = input("".join([app_choiced, ": "]))
                    re_res = re.match(regex_fields[app_choiced], new_value)
                    print(re_res)
                    if re_res:
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.secret_ini[section][app_choiced] = new_value
                    else:
                        self.message = "".join([
                            T("The "), app_choiced, T(" not match!"), " (regex: \"", regex_fields[app_choiced], "\")"])
                else:
                    print(T("Please enter the new value in the field below:"))
                    new_value = input("".join([app_choiced, ": "]))
                    if app_choiced in is_not_empty:
                        if new_value:
                            self.message = "".join([app_choiced, " ", T("changed!")])
                            self.ProjectConfig.secret_ini[section][app_choiced] = new_value
                        else:
                            self.message = "".join([T("The "), app_choiced, T(" value is not Empty!")])
                    else:
                        self.message = "".join([app_choiced, " ", T("changed!")])
                        self.ProjectConfig.secret_ini[section][app_choiced] = new_value
                with open(os.path.join(project_path, 'secret.ini'), 'w', encoding="utf-8") as configfile:
                    self.ProjectConfig.secret_ini.write(configfile)
                self.ProjectConfig.save()
            else:
                self.message = T("Invalid choice!")
            self.clear()

    def interface_translate(self):
        if Trans.languages:
            alert = Alerts()
            while True:
                self.clear()
                print(self.title(T("Languages"), char="|"))
                print()
                langs = []
                cont = 0
                for v in Trans.languages:
                    print("".join(["[", str(cont), "] - ", T(v)]))
                    langs.append(v)
                    cont += 1
                print(self.title(char="-"))
                print("".join(["[E] - ", T("Exit"), " "]))
                print(self.title(char="-"))
                if alert:
                    print(alert)
                c = input("".join(["  ", T("What do you want to do?"), " "]))
                if c == "E" or c == "e":
                    break
                else:
                    v = None
                    try:
                        e_int = int(c)
                        v = langs[e_int]
                    except Exception:
                        alert.alert = T("The value is invalid! Try again!")
                    else:
                        alert.alert = ""
                        config(self._projectdata_dir_cli, {'language': v})
                        Trans.direct_translation = v
                        print(T("You choice translate to"), T(v))
                        break
        else:
            print(T("Without languages..."))



if __name__ == '__main__':
    start()
