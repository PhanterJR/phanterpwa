import os
import sys
import shutil
import logging
import psutil
import subprocess
from phanterpwa.config import ProjectConfig

from phanterpwa.tools import (
    list_installed_applications,
    config,
    compiler,
    interpolate,
    package_project_app
)
from phanterpwa.i18n import Translator
from phanterpwa import __version__ as PHANTERPWA_VERSION
ENV_PYTHON = os.path.normpath(sys.executable)
ENV_PATH = os.path.normpath(os.path.dirname(ENV_PYTHON))
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")
PY_VERSION = "{0}.{1}.{2}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])
CURRENT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__)))
Trans = Translator(os.path.join(CURRENT_DIR, "langs"), debug=True)
CONFIG = config(CURRENT_DIR)
if "language" in CONFIG:
    Trans.direct_translation = CONFIG["language"]
T = Trans.T
_About = ""
with open(os.path.join(CURRENT_DIR, "..", "samples", "about_cli"), 'r', encoding='utf-8') as f:
    _About = f.read()
_About = interpolate(_About, {"VERSION": PHANTERPWA_VERSION})
PID = os.getpid()
with open("phanterpwa.pid", "w") as f:
    f.write(str(PID))

if os.path.exists("phanterpwa.pid"):
    with open("phanterpwa.pid", "r") as f:
        pid = f.read().strip()
        if pid:
            for p in psutil.process_iter():
                if int(p.pid) != int(pid):
                    cmd_line = None
                    try:
                        cmd_line = p.cmdline()
                    except Exception:
                        pass
                    if cmd_line:
                        basename = os.path.basename
                        if ENV_PYTHON == cmd_line[0]:
                            if __file__ == cmd_line[-1]:
                                p.terminate()
                                print("close server. PID: ", pid)
                            elif os.path.join(os.path.dirname(__file__), "graphic.py") == cmd_line[-1]:
                                p.terminate()
                                print("close server. PID: ", pid)
        else:
            print("Previous server not found")


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


def CLEAR_CONSOLE():
    os.system('cls' if os.name == 'nt' else 'clear')


def start_server(projectPath):
    target = os.path.normpath(os.path.join(CURRENT_DIR, "..", "server.py"))
    command = " ".join([ENV_PYTHON, target])
    subprocess.run(command, cwd=projectPath, shell=True)


def title(title="", size=79, char="="):
    title = str(title)
    r = size - (len(title) + 2)
    r = r // 2
    if title:
        return "{0} {1} {0}".format(char * r, title)
    else:
        return char * size


def app_menu(configApp):
    is_run = True
    projectPath = configApp['PATH']['project']
    if not os.path.exists(os.path.join(projectPath, 'logs')):
        os.makedirs(os.path.join(projectPath, 'logs'), exist_ok=True)
    formatter = logging.Formatter(
        '%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    formatter_out_app = logging.Formatter(
        '%(asctime)s - %(name)s.app -  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh = logging.FileHandler(os.path.join(projectPath, 'logs', 'app.log'))
    fh.setFormatter(formatter)
    logger = logging.getLogger(os.path.basename(projectPath))
    logger.setLevel(logging.ERROR)
    logger.addHandler(fh)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.ERROR)
    sh.setFormatter(formatter_out_app)
    logger.addHandler(sh)
    CLEAR_CONSOLE()
    alert_app = Alerts()
    while True:
        print(title(configApp['PROJECT']['name']))
        print("".join(["[0] - ", T("Config"), " "]))
        print("".join(["[1] - ", T("Compile"), " "]))
        print("".join(["[2] - ", T("Delete"), " "]))
        print("".join(["[3] - ", T("Package"), " "]))
        print("".join(["[4] - ", T("Start Server"), " "]))
        print(title(char="-"))
        print("".join(["[E] - ", T("Exit"), " "]))
        print(title(char="-"))
        if alert_app:
            print(alert_app.alert)
            alert_app.alert = ""
        c = input("".join([T("What do you want to do?"), " "]))
        if c == "E" or c == "e":
            alert_app.alert = ""
            break
        elif c == "0":
            print(title("Open '{0}'".format(
                os.path.normpath(os.path.join(configApp['PATH']['project'], "config.json")))))
            with open(os.path.join(configApp['PATH']['project'], 'config.json'), 'r', encoding='utf-8') as f:
                print(f.read())
            print(title(char="-"))
            print(T("".join(["Use an editor like vim to edit the configuration file,\n",
                "it is located at"])), "'{0}'".format(
                    os.path.normpath(os.path.join(configApp['PATH']['project'], "config.json"))))
            input(T("Press <enter> key to continue."))
            CLEAR_CONSOLE()
        elif c == "1":
            try:
                compiler(projectPath)
            except Exception:
                logger.error("Compilation error", exc_info=True)
                alert_app.alert = T("Compilation Error, check the log file to learn more.")
                CLEAR_CONSOLE()
            else:
                input("".join([T("Sucess"), "! ", T("Press <enter> key to continue.")]))
                CLEAR_CONSOLE()

        elif c == "2":
            if os.path.exists(projectPath):
                try:
                    shutil.rmtree(projectPath)
                except Exception:
                    logger.error("Deleting application path error", exc_info=True)
                    alert_app.alert = T("Deleting application path error, check the log file to learn more.")
                    CLEAR_CONSOLE()
        elif c == "3":
            print(
                T("Packing on"),
                os.path.normpath(os.path.join(os.path.dirname(projectPath),
                    "{0}.ppwa".format(os.path.basename(projectPath))))
            )
            try:
                package_project_app(projectPath, os.path.dirname(projectPath))
            except Exception:
                logger.error("Packing error", exc_info=True)
                alert_app.alert = T("Packing error, check the log file to learn more.")
                CLEAR_CONSOLE()
            else:
                input("".join([T("Sucess"), "! ", T("Press <enter> key to continue.")]))
                CLEAR_CONSOLE()
        elif c == "4":
            print(T("API Server running in http://{0}:{1}".format(
                configApp['API_SERVER']['host'], configApp['API_SERVER']['port'])))
            print(T("APP Server running in http://{0}:{1}".format(
                configApp['APP_SERVER']['host'], configApp['APP_SERVER']['port'])))
            try:
                print("Press CTRL+C to stop server!")
                config(CURRENT_DIR, {'last_application': configApp['PATH']['project']})
                start_server(projectPath)
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
                CLEAR_CONSOLE()
                input("".join([T("Server Stoped"), "!. ", T("Press <enter> key to continue.")]))
                CLEAR_CONSOLE()
            except Exception:
                logger.error("Server error", exc_info=True)
                alert_app.alert = T("Server error, check the log file to learn more.")
                CLEAR_CONSOLE()
    return is_run


def interface_translate():
    if Trans.languages:
        alert = Alerts()
        while True:
            CLEAR_CONSOLE()
            print(title(T("Languages")))
            langs = []
            cont = 0
            for v in Trans.languages:
                print("".join(["[", str(cont), "] - ", T(v)]))
                langs.append(v)
                cont += 1
            print(title(char="-"))
            print("".join(["[E] - ", T("Exit"), " "]))
            print(title(char="-"))
            if alert:
                print(alert)
            c = input("".join([T("What do you want to do?"), " "]))
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
                    config(CURRENT_DIR, {'language': v})
                    Trans.direct_translation = v
                    print(T("You choice translate to"), T(v))
                    break
    else:
        print(T("Without languages..."))


def start():
    is_run = True
    CLEAR_CONSOLE()
    interfaceConfig = config(CURRENT_DIR)
    applications_folder = None
    if "applications_folder" in interfaceConfig:
        applications_folder = interfaceConfig["applications_folder"]
    print("\n")
    with open(os.path.join(CURRENT_DIR, "..", "samples", "art_cli"), "r") as f:
        print(f.read())
    print(title(size=67, char="_"))
    print(_About)
    try:
        print(title(T("Press <enter> key to continue (CTRL+C to interrupt)"), size=67, char=" "))
        input("".join([" " * 33]))
        CLEAR_CONSOLE()
        while is_run:
            if not applications_folder:
                print("First you must define a folder where applications will be stored.")
                f = input("".join([T("Please enter the address where your applications will be stored."), "\n-> "]))
                while not os.path.exists(f):
                    f = input("".join([T("The folder does not exist! Please enter the valid address."), "\n-> "]))
                else:
                    interfaceConfig["applications_folder"] = f
                    config(CURRENT_DIR, interfaceConfig)
                    applications_folder = f
            apps = list_installed_applications(applications_folder)
            if apps:
                alert_main = Alerts()
                while True:
                    CLEAR_CONSOLE()
                    print(title("PhanterPWA - Developer", char="|"))
                    print()
                    print(title(T("Enviroment")))
                    print("Path: {0}".format(ENV_PATH))
                    print("Python: {0}".format(ENV_PYTHON))
                    print("Python version: {0}".format(PY_VERSION))
                    print("PhanterPWA version: {0}".format(PHANTERPWA_VERSION))
                    print(title(char="-"))
                    print()
                    print(title(T("Applications")))
                    l_app = []
                    for n, a in enumerate(apps):
                        l_app.append(apps[a])
                        print("[{0}] - {1} - {2}".format(n, a, apps[a]['PATH']['project']))
                    print(title(char="-"))
                    print("[T] - Translate")
                    print("[Q] - Quit")
                    print(title(char="-"))
                    if alert_main:
                        print(alert_main)
                    e = input("".join([T("What do you want to do?"), " "]))
                    print(title())
                    if e == "Q" or e == "q":
                        alert_main.alert = ""
                        CLEAR_CONSOLE()
                        print("\nGoodbye!")
                        break
                    elif e == "T" or e == "t":
                        alert_main.alert = ""
                        interface_translate()
                    else:
                        v = None
                        try:
                            e_int = int(e)
                            v = l_app[e_int]
                        except Exception:
                            alert_main.alert = T("The value is invalid! Try again!")
                        if v:
                            alert_main.alert = ""
                            is_run = app_menu(v)
                            if is_run is False:
                                break
                break
                print("Goodbye!")

    except KeyboardInterrupt:
        CLEAR_CONSOLE()
        print("\nGoodbye!")


if __name__ == '__main__':
    CLEAR_CONSOLE()
    start()
