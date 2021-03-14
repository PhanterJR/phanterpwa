import os
import glob
import json
import sys
import tkinter as tk
import webbrowser
import time
import shutil
import logging
import psutil
import subprocess
from tkinter import (
    ttk,
    filedialog,
    END,
    HORIZONTAL,
    VERTICAL,
    LEFT,
    RIGHT,
    Scrollbar,
    Y,
    DISABLED,
    FALSE,
    TRUE,
    Menu,
    messagebox,
    IntVar
)
import re
from zipfile import ZipFile
from phanterpwa import (
    __version__ as PHANTERPWA_VERSION
)
from phanterpwa.compiler import (
    Compiler
)
from phanterpwa.tools import (
    config,
    humanize_seconds,
    split_seconds,
    join_seconds,
    interpolate
)
from phanterpwa.interface.cli import package_project_app
from phanterpwa.samples import project_config_sample
from phanterpwa.i18n import Translator
ENV_PYTHON = os.path.normpath(sys.executable)
ENV_PATH = os.path.normpath(os.path.dirname(ENV_PYTHON))
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")
PY_VERSION = "{0}.{1}.{2}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])

CURRENT_DIR = os.path.dirname(__file__)
Tra = Translator(CURRENT_DIR, "langs")
T = Tra.T
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
                            elif os.path.join(os.path.dirname(__file__), "cli.py") == cmd_line[-1]:
                                p.terminate()
                                print("close server. PID: ", pid)
        else:
            print("Previous server not found")


print("PhanterPWA PID: {0}".format(PID))
Trans = Translator(os.path.join(CURRENT_DIR, "langs"), "grafics", debug=True)


_About = ""
with open(os.path.join(CURRENT_DIR, "..", "samples", "about_graphic"), 'r', encoding='utf-8') as f:
    _About = f.read()


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
        if j and j["FRONTEND"]:
            change = False
            for p in glob(os.path.join(j['PROJECT']['path'], "frontapps", "*")):
                app_name = os.path.split(p)[-1]
                if all([os.path.isdir(p),
                        os.path.isdir(os.path.join(p, "sources", "styles")),
                        os.path.isdir(os.path.join(p, "sources", "templates")),
                        os.path.isdir(os.path.join(p, "sources", "transcrypts")),
                        os.path.isdir(os.path.join(p, "statics"))]):
                    if not j["FRONTEND"].get(app_name, None):
                        change = True
                        j["FRONTEND"][app_name] = {
                            "build_folder": os.path.join(p, "www"),
                            "timeout_to_resign": 600,
                            "host": "0.0.0.0",
                            "port": j["API"]["port"] + 1,
                            "transcrypt_main_file": "application",
                            "styles_main_file": "application",
                            "views_main_file": "application"
                        }
                    apps[app_name] = j["FRONTEND"][app_name]
            if change:
                with open(cfg, 'w', encoding='utf-8') as fw:
                    json.dump(j, fw, ensure_ascii=False, indent=2)
    if not apps:
        print("Don't find installed apps on {0}".format(os.path.join(path_project, "frontapps")))
    return apps


class Root():
    def __init__(self, tkinterInstance):
        self.ProjectsPWA = None
        self.ProjectPWA = None
        self.ConfigAPI = None
        self.ConfigAPP = None
        self.CONFIG = config(CURRENT_DIR)
        if "projects_folder" in self.CONFIG:
            if os.path.exists(self.CONFIG["projects_folder"]):
                self.projects_folder = self.CONFIG["projects_folder"]
        else:
            self.projects_folder = os.getcwd()
        self.tkInstance = tkinterInstance
        self.tkInstance.withdraw()
        self.maxheight = 400
        self.ApplicationsTornado = {}
        scrollbar = Scrollbar(self.tkInstance, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self.frame_canvas = tk.Canvas(
            self.tkInstance,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.frame_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.frame_canvas.yview)
        self.frame_canvas.pack(side=LEFT, fill=Y, expand=TRUE)

        self.tkInstance.title(T("Project Folder - PhanterPWA"))
        self.tkInstance.iconbitmap(os.path.join(CURRENT_DIR, "grafics", "icon.ico"))

        frame = tk.Frame(self.frame_canvas)

        row = 0
        aLabel = ttk.Label(frame, text=T("Where will your projects be saved?"), font='default 14 bold')
        aLabel.grid(column=0, row=row, columnspan=3, padx=(10, 0), pady=(20, 5))

        row += 1
        app_folder_label = ttk.Label(frame, text=T("Path"))
        app_folder_label.grid(column=0, row=row, padx=(20, 0), pady=(5, 20))
        app_folder_data = ""
        self.app_folder_input = ttk.Entry(frame, width=60)
        self.app_folder_input.insert(0, app_folder_data)
        self.app_folder_input.grid(column=1, row=row, padx=(0, 0), pady=(5, 20))
        button = ttk.Button(frame, text=T("Change"), command=lambda: self.setEntryFolder(self.app_folder_input))
        button.grid(column=2, row=row, padx=(0, 20), pady=(5, 20), sticky="w")

        row += 1
        self.buttonOK = ttk.Button(frame, text=T("OK"), command=self.open_window_projects, state=DISABLED)
        self.buttonOK.grid(column=0, row=row, columnspan=3, padx=10, pady=(5, 30))

        self.frame_canvas.create_window((0, 0), window=frame, anchor='nw')
        self.frame_canvas.bind('<Configure>', self.onConfigure)
        self.tkInstance.resizable(0, 0)
        self.tkInstance.maxsize(width=0, height=self.maxheight)
        self.tkInstance.resizable(0, 0)
        if "projects_folder" in self.CONFIG:
            if os.path.exists(self.CONFIG["projects_folder"]):
                self.projects_folder = self.CONFIG["projects_folder"]
                self.buttonOK.config(state="normal")
                self.app_folder_input.delete(0, END)
                self.app_folder_input.insert(0, os.path.normpath(self.projects_folder))
                self.open_window_projects()
        else:
            self.tkInstance.deiconify()
        self.tkInstance.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.tkInstance.attributes('-topmost', True)
        self.tkInstance.update()
        self.tkInstance.attributes('-topmost', False)

    def setEntryFolder(self, entry_instance):
        if self.projects_folder:
            folder = filedialog.askdirectory(initialdir=self.projects_folder)
        else:
            folder = filedialog.askdirectory()
        if folder:
            self.projects_folder = folder
            self.buttonOK.config(state="normal")
            entry_instance.delete(0, END)
            entry_instance.insert(0, os.path.normpath(folder))

    def onConfigure(self, event):
        height = self.frame_canvas.bbox('all')[3]
        width = self.frame_canvas.bbox('all')[2]
        self.frame_canvas.configure(
            height=height,
            width=width,
            scrollregion=self.frame_canvas.bbox('all')
        )

    def open_window_projects(self):
        # if self.app_folder_input.get():
        #     self.CONFIG = config(CURRENT_DIR, {"projects_folder": os.path.normpath(self.projects_folder)})
        #     self.tkInstance.withdraw()
        #     if not self.ProjectsPWA:
        #         tkInstance = tk.Toplevel(self.tkInstance)
        #         self.ProjectsPWA = ProjectsPWA(tkInstance, self)
        #     else:
        #         self.ProjectsPWA.tkInstance.destroy()
        #         tkInstance = tk.Toplevel(self.tkInstance)
        #         self.ProjectsPWA = ProjectsPWA(tkInstance, self)
        pass

    def open_window_project(self, project_path):
        self.tkInstance.withdraw()
        if not self.ProjectPWA:
            tkInstance = tk.Toplevel(self.tkInstance)
            self.ProjectPWA = ProjectPWA(tkInstance, self, project_path)
        else:
            self.ProjectPWA.tkInstance.destroy()
            tkInstance = tk.Toplevel(self.tkInstance)
            self.ProjectPWA = ProjectPWA(tkInstance, self, project_path)

    def open_window_config_api(self, project_path):
        self.tkInstance.withdraw()
        if self.ConfigAPI:
            self.ConfigAPI.tkInstance.destroy()
        tkInstance = tk.Toplevel(self.tkInstance)
        self.ConfigAPI = ConfigAPI(tkInstance, self, project_path)

    def open_window_config_app(self, project_path, APP):
        self.tkInstance.withdraw()
        if self.ConfigAPP:
            self.ConfigAPP.tkInstance.destroy()
        tkInstance = tk.Toplevel(self.tkInstance)
        self.ConfigAPP = ConfigAPP(tkInstance, self, project_path, APP)

    def close_window_projects(self):
        self.ProjectsPWA.tkInstance.withdraw()

    def onClosing(self):
        for server_running in self.ApplicationsTornado:
            try:
                self.ApplicationsTornado[server_running].stop()
                self.ApplicationsTornado[server_running].tkInstance.destroy()
            except Exception:
                print("Try Close")
        self.tkInstance.destroy()


class ProjectsPWA():
    def __init__(self, tkInstance, Root=None):
        self.CONFIG = config(CURRENT_DIR)
        self.Root = Root
        self.tkInstance = tkInstance
        self.tkInstance.withdraw()
        self.maxheight = 400

        scrollbar = Scrollbar(tkInstance, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self.frame_canvas = tk.Canvas(
            tkInstance,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )

        menubar = Menu(tkInstance)
        menubar.add_command(label=T("Change Projects Folder"), command=self.change_projects_folder)
        menubar.add_command(label=T("Add Application"), command=self.setPPwaFile)
        if Trans.languages:
            langMenu = Menu(tkInstance, tearoff=False)
            menubar.add_cascade(label=T("Translate"), menu=langMenu)
            for v in Trans.languages:
                langMenu.add_command(labe=T(v), command=lambda v=v: self.setLang(str(v)))
        menubar.add_command(label=T("About"), command=self.about)

        tkInstance.config(menu=menubar)

        tkInstance.protocol('WM_DELETE_WINDOW', lambda: self.close())
        self.frame_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.frame_canvas.yview)
        self.frame_canvas.pack(side=LEFT, fill=Y, expand=TRUE)

        tkInstance.title("PhanterPWA")
        tkInstance.iconbitmap(os.path.join(CURRENT_DIR, "grafics", "icon.ico"))

        frame = tk.Frame(self.frame_canvas)

        row = 0
        aLabel = ttk.Label(frame, text=T("PhanterPWA Developer"), font='default 14 bold')
        aLabel.grid(column=0, row=row, columnspan=6, padx=10, pady=(10, 5))

        row += 1
        label_enviroment = ttk.Label(frame, text=T("Enviroment"), font='default 10 bold')
        label_enviroment.grid(column=0, row=row, columnspan=6, padx=0, pady=(10, 0), sticky="w")

        row += 1
        hr_enviroment = ttk.Separator(frame, orient=HORIZONTAL)
        hr_enviroment.grid(column=0, row=row, columnspan=6, sticky='ew')

        row += 1
        enviroment_path_label = ttk.Label(frame, text=T("Path"))
        enviroment_path_label.grid(column=0, row=row, padx=(20, 5), pady=(5, 5), sticky="e")
        enviroment_path_data = os.path.dirname(ENV_PYTHON)
        self.input_enviroment_path = ttk.Entry(frame, width=100)
        self.input_enviroment_path.insert(0, enviroment_path_data)
        self.input_enviroment_path.config(state="readonly")
        self.input_enviroment_path.grid(column=1, row=row, columnspan=5, padx=(0, 10), pady=(5, 5))

        row += 1
        enviroment_python_label = ttk.Label(frame, text=T("Python"))
        enviroment_python_label.grid(column=0, row=row, padx=(20, 5), pady=(5, 5), sticky="e")
        enviroment_python_data = ENV_PYTHON
        self.input_enviroment_python = ttk.Entry(frame, width=100)
        self.input_enviroment_python.insert(0, enviroment_python_data)
        self.input_enviroment_python.config(state="readonly")
        self.input_enviroment_python.grid(column=1, row=row, columnspan=5, padx=(0, 10), pady=(5, 5))

        row += 1
        enviroment_pythonv_label = ttk.Label(frame, text=T("Python Version"))
        enviroment_pythonv_label.grid(column=0, row=row, padx=(20, 5), pady=(5, 5), sticky="e")
        enviroment_pythonv_data = PY_VERSION
        self.input_enviroment_py_version = ttk.Entry(frame, width=100)
        self.input_enviroment_py_version.insert(0, enviroment_pythonv_data)
        self.input_enviroment_py_version.config(state="readonly")
        self.input_enviroment_py_version.grid(column=1, row=row, columnspan=5, padx=(0, 10), pady=(5, 5))

        row += 1
        enviroment_phanterpwav_label = ttk.Label(frame, text=T("PhanterPWA Version"))
        enviroment_phanterpwav_label.grid(column=0, row=row, padx=(20, 5), pady=(5, 5), sticky="e")
        enviroment_phanterpwav_data = PHANTERPWA_VERSION
        self.input_enviroment_ppwa_version = ttk.Entry(frame, width=100)
        self.input_enviroment_ppwa_version.insert(0, enviroment_phanterpwav_data)
        self.input_enviroment_ppwa_version.config(state="readonly")
        self.input_enviroment_ppwa_version.grid(column=1, row=row, columnspan=5, padx=(0, 10), pady=(5, 5))

        row += 1
        enviroment_phanterpwav_label = ttk.Label(frame, text=T("Projects Folder"))
        enviroment_phanterpwav_label.grid(column=0, row=row, padx=(20, 5), pady=(5, 5), sticky="e")
        enviroment_phanterpwav_data = self.CONFIG["projects_folder"]
        self.input_enviroment_projects_folder = ttk.Entry(frame, width=100)
        self.input_enviroment_projects_folder.insert(0, enviroment_phanterpwav_data)
        self.input_enviroment_projects_folder.config(state="readonly")
        self.input_enviroment_projects_folder.grid(column=1, row=row, columnspan=5, padx=(0, 10), pady=(5, 5))

        row += 1
        label_project = ttk.Label(frame, text=T("Installed projects"), font='default 10 bold')
        label_project.grid(column=0, row=row, columnspan=6, padx=0, pady=(40, 0), sticky="w")

        row += 1
        hr_project = ttk.Separator(frame, orient=HORIZONTAL)
        hr_project.grid(column=0, row=row, columnspan=6, sticky='ew')

        self.buttons_dict = {}
        if "projects_folder" in self.CONFIG:
            if os.path.exists(self.CONFIG["projects_folder"]):
                apps = list_installed_projects(self.CONFIG["projects_folder"])
                if apps:
                    row += 1
                    for i in apps:
                        cfg_app = config(os.path.join(self.CONFIG["projects_folder"], i, "config.json"))
                        cfg_app['ENVIRONMENT']['path'] = ENV_PATH
                        cfg_app['ENVIRONMENT']['python'] = ENV_PYTHON
                        project_path = os.path.join(self.CONFIG["projects_folder"], i)
                        if not os.path.exists(os.path.join(project_path, 'logs')):
                            os.makedirs(os.path.join(project_path, 'logs'), exist_ok=True)
                        formatter = logging.Formatter(
                            '%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                        )
                        formatter_out_app = logging.Formatter(
                            '%(asctime)s - %(name)s.app -  %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                        )
                        formatter_out_api = logging.Formatter(
                            '%(asctime)s - %(name)s.api -  %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                        )
                        fh_app = logging.FileHandler(os.path.join(project_path, 'logs', 'app.log'))
                        fh_api = logging.FileHandler(os.path.join(project_path, 'logs', 'api.log'))
                        fh_app.setFormatter(formatter)
                        fh_api.setFormatter(formatter)
                        logger_app = logging.getLogger("{0}.app".format(i))
                        logger_api = logging.getLogger("{0}.api".format(i))
                        logger_app.setLevel(logging.ERROR)
                        logger_api.setLevel(logging.ERROR)
                        logger_app.addHandler(fh_app)
                        logger_api.addHandler(fh_api)
                        sh_app = logging.StreamHandler(sys.stdout)
                        sh_app.setLevel(logging.ERROR)
                        sh_app.setFormatter(formatter_out_app)
                        logger_app.addHandler(sh_app)
                        sh_api = logging.StreamHandler(sys.stdout)
                        sh_api.setLevel(logging.ERROR)
                        sh_api.setFormatter(formatter_out_api)
                        logger_api.addHandler(sh_api)
                        config(os.path.join(project_path, "config.json"), cfg_app)
                        row += 1
                        label_project = ttk.Label(frame, text=cfg_app['PROJECT']['name'], font='default 8 bold')
                        label_project.grid(column=0, row=row, columnspan=5, padx=(20, 10), pady=(5, 0), sticky="w")

                        row += 1
                        hr_project = ttk.Separator(frame, orient=HORIZONTAL)
                        hr_project.grid(column=0, row=row, columnspan=6, padx=(20, 10), sticky='ew')
                        row += 1
                        I_name = ttk.Entry(frame)
                        I_name.insert(0, cfg_app['PROJECT']['title'])
                        I_name.config(state="readonly")
                        I_name.grid(column=0, row=row, padx=(30, 5), pady=(2, 2), sticky='ew')
                        t_name = ttk.Entry(frame, width=90)
                        t_name.insert(0, cfg_app['PROJECT']['path'])
                        t_name.config(state="readonly")
                        t_name.grid(column=1, row=row, columnspan=4, padx=(0, 0), pady=(2, 2), sticky='ew')
                        b0_name = ttk.Button(
                            frame, text=T("View"), command=lambda x=project_path: self.open_window_project(x))
                        b0_name.grid(column=5, row=row, padx=(5, 20), pady=(2, 2), sticky='e')
                        self.buttons_dict[project_path] = [b0_name]
                        row += 1
                        config(os.path.join(self.CONFIG["projects_folder"], i, "config.json"), cfg_app)
                    else:
                        row += 1
                        hr_project = ttk.Separator(frame, orient=HORIZONTAL)
                        hr_project.grid(column=0, row=row, columnspan=6, padx=(20, 10), pady=(20, 0), sticky='ew')
                        row += 1
                        ac = ttk.Button(frame, text="Add new project", command=self.setPPwaFile)
                        ac.grid(column=0, columnspan=6, row=row, padx=(30, 20), pady=(2, 30), sticky="ew")
                else:
                    row += 1
                    ac = ttk.Button(frame, text="Add your first project", command=self.setPPwaFile)
                    ac.grid(column=0, columnspan=6, row=row, padx=20, pady=(20, 30), sticky="ew")
            else:
                row += 1
                ac = ttk.Button(frame, text="Add your first project", command=self.setPPwaFile)
                ac.grid(column=0, columnspan=6, row=row, padx=0, pady=(5, 5), sticky="ew")

        self.frame_canvas.create_window((0, 0), window=frame, anchor='nw')
        self.frame_canvas.bind('<Configure>', self.onConfigure)

        self.openGeometry()
        if "ProjectsPWA_state" in self.CONFIG:
            if self.CONFIG["ProjectsPWA_state"] == "zoomed":
                self.tkInstance.state("zoomed")
            else:
                self.tkInstance.deiconify()
        else:
            self.tkInstance.deiconify()
        self.tkInstance.attributes('-topmost', True)
        self.tkInstance.update()
        self.tkInstance.attributes('-topmost', False)

    def setLang(self, lang):
        config(CURRENT_DIR, {"language": lang})
        Trans.direct_translation = lang
        messagebox.showinfo(
            T("Translation to {0}".format(lang)),
            T("The Application will be translated.")
        )

    def about(self):
        messagebox.showinfo(
            T("About"),
            interpolate(T(_About), context={"VERSION": PHANTERPWA_VERSION})
        )

    def setPPwaFile(self):
        file = filedialog.askopenfile(filetypes=[('PhanterPWA', '.ppwa')])
        if file:
            project_name = os.path.basename(str(file.name))[:-5]
            if project_name.isidentifier():
                with ZipFile(file.name, "r") as zipf:
                    folder = self.CONFIG["projects_folder"]
                    desti = os.path.join(folder, project_name)
                    title_sucess = T("Application Problem")
                    message_sucess = T("The config file of application is not valid!")
                    if os.path.exists(desti):
                        choice = messagebox.askquestion(
                            T("Are you sure?"),
                            T("".join(["The project folder existis, Do you want rewrite?"])),
                            icon='warning'
                        )
                        if choice == "yes":
                            zipf.extractall(path=desti)
                            if check_valid_project_config(os.path.join(desti, "config.json")):
                                cfg = config(os.path.join(desti, "config.json"))
                                cfg["PROJECT"]["packaged"] = False
                                config(desti, cfg)
                                title_sucess = T("Sucess"),
                                message_sucess = T("Application installed successfully!")
                            messagebox.showinfo(
                                title_sucess,
                                message_sucess
                            )
                    else:
                        zipf.extractall(path=desti)
                        if check_valid_project_config(os.path.join(desti, "config.json")):
                            cfg = config(os.path.join(desti, "config.json"))
                            cfg["PROJECT"]["packaged"] = False
                            config(desti, cfg)
                            title_sucess = T("Sucess"),
                            message_sucess = T("Application installed successfully!")
                        messagebox.showinfo(
                            title_sucess,
                            message_sucess
                        )
                self.tkInstance.destroy()
                self.Root.open_window_projects()

    def close(self):
        if self.Root:
            self.saveSize()
            for server_running in self.Root.ApplicationsTornado:
                try:
                    self.Root.ApplicationsTornado[server_running].stop()
                    self.Root.ApplicationsTornado[server_running].tkInstance.destroy()
                except Exception:
                    print("Try Close")
            self.Root.onClosing()

    def change_projects_folder(self):
        if self.Root:
            self.saveSize()
            self.tkInstance.destroy()
            self.Root.tkInstance.deiconify()

    def onConfigure(self, event):
        height = self.frame_canvas.bbox('all')[3]
        width = self.frame_canvas.bbox('all')[2]
        self.frame_canvas.configure(
            height=height,
            width=width,
            scrollregion=self.frame_canvas.bbox('all')
        )

    def open_window_project(self, project_path):
        self.Root.open_window_project(project_path)
        self.tkInstance.destroy()

    def openGeometry(self, event=None):
        if "ProjectsPWA" in self.CONFIG:
            self.tkInstance.geometry(self.CONFIG["ProjectsPWA"])

    def saveSize(self, event=None):
        self.CONFIG = config(
            CURRENT_DIR, {
                "ProjectsPWA": self.tkInstance.geometry(),
                "ProjectsPWA_state": self.tkInstance.state()
            }
        )

    def update(self):
        self.tkInstance.destroy()
        self.Root.open_window_projects()


class ProjectPWA():
    def __init__(self, tkInstance, Root, project_path):
        self.CONFIG = Root.CONFIG
        self.Root = Root
        self.tkInstance = tkInstance
        self.tkInstance.withdraw()
        self.maxheight = 400
        self.AppCONFIG = config(project_path)
        self.project_path_name = os.path.basename(project_path)
        self.project_path = project_path

        scrollbar = Scrollbar(tkInstance, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self.frame_canvas = tk.Canvas(
            tkInstance,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        style_orange = ttk.Style()
        style_orange.configure('Wf.TButton', font=('default', 10, 'bold'), foreground='orange')
        style_green = ttk.Style()
        style_green.configure('Wg.TButton', font=('default', 10, 'bold'), foreground='green')
        style_default = ttk.Style()
        style_default.configure('Wd.TButton', font=('default', 10))
        tkInstance.protocol('WM_DELETE_WINDOW', lambda: self.close())
        self.frame_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.frame_canvas.yview)
        self.frame_canvas.pack(side=LEFT, fill=Y, expand=TRUE)

        tkInstance.title("{0} - PhanterPWA".format(self.AppCONFIG['PROJECT']['title']))
        tkInstance.iconbitmap(os.path.join(CURRENT_DIR, "grafics", "icon.ico"))

        frame = tk.Frame(self.frame_canvas)

        row = 0
        aLabel = ttk.Label(frame, text=self.AppCONFIG['PROJECT']['title'], font='default 14 bold')
        aLabel.grid(column=0, row=row, columnspan=6, padx=10, pady=(10, 5))
        row += 1
        label_project = ttk.Label(frame, text=T("PROJECT"), font='default 10 bold')
        label_project.grid(column=0, row=row, columnspan=6, padx=0, pady=(10, 0), sticky="w")

        row += 1
        hr_project = ttk.Separator(frame, orient=HORIZONTAL)
        hr_project.grid(column=0, row=row, columnspan=6, sticky='ew')

        row += 1
        project_name_label = ttk.Label(frame, text=T("Identifier Name:"))
        project_name_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        project_name = self.AppCONFIG['PROJECT']['name']
        self.project_name_input = ttk.Entry(frame, width=90)
        self.project_name_input.insert(0, project_name)
        self.project_name_input.grid(column=1, row=row, columnspan=4, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Name"))
        button.grid(column=5, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        project_title_label = ttk.Label(frame, text=T("Title:"))
        project_title_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        project_title = self.AppCONFIG['PROJECT']['title']
        self.project_title_input = ttk.Entry(frame, width=90)
        self.project_title_input.insert(0, project_title)
        self.project_title_input.grid(column=1, row=row, columnspan=4, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Title"))
        button.grid(column=5, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        project_version_label = ttk.Label(frame, text=T("Version:"))
        project_version_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        project_version = self.AppCONFIG['PROJECT']['version']
        self.project_version_input = ttk.Entry(frame, width=90)
        self.project_version_input.insert(0, project_version)
        self.project_version_input.grid(column=1, row=row, columnspan=4, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Version"))
        button.grid(column=5, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        project_author_label = ttk.Label(frame, text=T("Author:"))
        project_author_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        project_author = self.AppCONFIG['PROJECT']['author']
        self.project_author_input = ttk.Entry(frame, width=90)
        self.project_author_input.insert(0, project_author)
        self.project_author_input.grid(column=1, row=row, columnspan=4, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Author"))
        button.grid(column=5, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        project_path_label = ttk.Label(frame, text=T("Path:"))
        project_path_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        project_path_data = self.AppCONFIG['PROJECT']['path']
        self.project_path_input = ttk.Entry(frame, width=100)
        self.project_path_input.insert(0, project_path_data)
        self.project_path_input.config(state="readonly")
        self.project_path_input.grid(column=1, row=row, columnspan=5, padx=(5, 10), pady=(5, 5), sticky="we")

        row += 1
        self.var_debug = IntVar()
        if self.AppCONFIG['PROJECT']['debug'] is True or self.AppCONFIG['PROJECT']['debug'] == "true":
            self.var_debug.set(1)
            is_debug = ttk.Checkbutton(frame, text=T("Debug (Set off on production)"), variable=self.var_debug, command=self.setDebug)
        else:
            self.var_debug.set(0)
            is_debug = ttk.Checkbutton(frame, text=T("Debug (Set off on production)"), variable=self.var_debug, command=self.setDebug)
        is_debug.grid(column=0, row=row, columnspan=6, padx=(10, 5), pady=(5, 5))
        row += 1
        label_project = ttk.Label(frame, text=T("ACTIONS"), font='default 10 bold')
        label_project.grid(column=0, row=row, columnspan=6, padx=0, pady=(10, 0), sticky="w")

        row += 1
        hr_project = ttk.Separator(frame, orient=HORIZONTAL)
        hr_project.grid(column=0, row=row, columnspan=6, sticky='ew')
        row += 1
        b1_name = ttk.Button(
            frame, text=T("Compile"), command=lambda z=project_path: self.compileApp(z)
        )
        b1_name.grid(column=0, row=row, padx=(2, 2), pady=(20, 2), sticky='ew')
        b2_name = ttk.Button(
            frame, text=T("Delete"), command=lambda z=project_path: self.deleteApp(z)
        )
        b2_name.grid(column=1, row=row, padx=(2, 2), pady=(20, 2), sticky='ew')
        b3_name = ttk.Button(
            frame, text=T("Package"), command=lambda z=project_path: self.packageApp(z)
        )
        b3_name.grid(column=2, row=row, padx=(2, 2), pady=(20, 2), sticky='ew')
        if os.path.basename(project_path) in self.Root.ApplicationsTornado:
            b4_name = ttk.Button(
                frame, text=T("Running..."), command=lambda z=project_path: self.runApp(z)
            )
            b4_name.grid(column=3, row=row, columnspan=2, padx=(2, 2), pady=(20, 2), sticky='ew')
            b4_name.configure(style='Wg.TButton')
        else:
            b4_name = ttk.Button(
                frame, text=T("Stoped"), command=lambda z=project_path: self.runApp(z)
            )
            b4_name.grid(column=3, row=row, columnspan=3, padx=(2, 2), pady=(20, 2), sticky='ew')
        b4_name.update()

        row += 1
        label_enviroment = ttk.Label(frame, text=T("API"), font='default 10 bold')
        label_enviroment.grid(column=0, row=row, columnspan=6, padx=0, pady=(40, 0), sticky="w")

        row += 1
        hr_enviroment = ttk.Separator(frame, orient=HORIZONTAL)
        hr_enviroment.grid(column=0, row=row, columnspan=6, sticky='ew')

        row += 1
        api_path_label = ttk.Label(frame, text=T("Path:"))
        api_path_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        api_path_data = os.path.join(project_path_data, "api")
        api_path_input = ttk.Entry(frame, width=90)
        api_path_input.insert(0, api_path_data)
        api_path_input.config(state="readonly")
        api_path_input.grid(column=1, row=row, columnspan=4, padx=(5, 10), pady=(5, 5))
        b0_name = ttk.Button(frame, text="Config", command=lambda x=project_path: self.open_window_config_api(x))
        b0_name.grid(column=5, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        label_project = ttk.Label(frame, text=T("INSTALLED APPS"), font='default 10 bold')
        label_project.grid(column=0, row=row, columnspan=6, padx=0, pady=(40, 0), sticky="w")

        row += 1
        hr_project = ttk.Separator(frame, orient=HORIZONTAL)
        hr_project.grid(column=0, row=row, columnspan=6, sticky='ew')

        self.buttons_dict = {}
        self.projects_entries = {}

        if "projects_folder" in self.CONFIG:
            if os.path.exists(self.CONFIG["projects_folder"]):
                apps = list_installed_apps(self.project_path)
                if apps:
                    row += 1
                    for i in apps:
                        row += 1
                        label_project = ttk.Label(frame, text=i, font='default 8 bold')
                        label_project.grid(column=0, row=row, columnspan=5, padx=(20, 10), pady=(5, 0), sticky="w")

                        row += 1
                        hr_project = ttk.Separator(frame, orient=HORIZONTAL)
                        hr_project.grid(column=0, row=row, columnspan=6, padx=(20, 10), sticky='ew')
                        row += 1
                        I_name = ttk.Label(frame, text=T("Path:"), font='default 8')

                        I_name.grid(column=0, row=row, padx=(30, 5), pady=(2, 2), sticky='e')
                        t_name = ttk.Entry(frame)
                        t_name.insert(0, os.path.join(project_path_data, "frontapps", i))
                        t_name.config(state="readonly")
                        t_name.grid(column=1, row=row, columnspan=4, padx=(0, 0), pady=(2, 2), sticky='ew')
                        bapp_name = ttk.Button(
                            frame, text="Config", command=lambda x=project_path: self.open_window_config_app(project_path, i))
                        bapp_name.grid(column=5, row=row, padx=10, pady=(5, 5), sticky="w")
                    else:
                        row += 1
                        hr_project = ttk.Separator(frame, orient=HORIZONTAL)
                        hr_project.grid(column=0, row=row, columnspan=6, padx=(20, 10), pady=(20, 0), sticky='ew')
                        row += 1
                        ac = ttk.Button(frame, text="Add new application", command=lambda: self.add_new_app())
                        ac.grid(column=0, columnspan=6, row=row, padx=(30, 20), pady=(2, 30), sticky="ew")
                else:
                    row += 1
                    ac = ttk.Button(frame, text="Add your first application", command=lambda: self.add_new_app())
                    ac.grid(column=0, columnspan=6, row=row, padx=20, pady=(20, 30), sticky="ew")
            else:
                row += 1
                ac = ttk.Button(frame, text="Add your first application", command=lambda: self.add_new_app())
                ac.grid(column=0, columnspan=6, row=row, padx=0, pady=(5, 5), sticky="ew")
        row += 1
        label_email = ttk.Label(frame, text=T("EMAIL"), font='default 10 bold')
        label_email.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 0), sticky="w")

        row += 1
        hr_email = ttk.Separator(frame, orient=HORIZONTAL)
        hr_email.grid(column=0, row=row, columnspan=4, sticky='ew')

        row += 1
        email_server_label = ttk.Label(frame, text=T("Server:"))
        email_server_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        email_server = self.AppCONFIG['EMAIL']['server']
        self.email_server_input = ttk.Entry(frame, width=70)
        self.email_server_input.insert(0, email_server)
        self.email_server_input.grid(column=1, row=row, columnspan=4, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Email_server"))
        button.grid(column=5, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        email_username_label = ttk.Label(frame, text=T("Username:"))
        email_username_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        email_username = self.AppCONFIG['EMAIL']['username']
        self.email_username_input = ttk.Entry(frame, width=70)
        self.email_username_input.insert(0, email_username)
        self.email_username_input.grid(column=1, row=row, columnspan=4, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Email_username"))
        button.grid(column=5, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        email_password_label = ttk.Label(frame, text=T("Password:"))
        email_password_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        email_password = self.AppCONFIG['EMAIL']['password']
        self.email_password_input = ttk.Entry(frame, width=70)
        self.email_password_input.insert(0, email_password)
        self.email_password_input.grid(column=1, row=row, columnspan=4, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Email_password"))
        button.grid(column=5, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        email_port_label = ttk.Label(frame, text=T("Port:"))
        email_port_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        email_port = self.AppCONFIG['EMAIL']['port']
        self.email_port_input = ttk.Entry(frame, width=70)
        self.email_port_input.insert(0, email_port)
        self.email_port_input.grid(column=1, row=row, columnspan=4, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Email_port"))
        button.grid(column=5, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        self.var_tls = IntVar()
        if self.AppCONFIG['EMAIL']['use_tls'] is True or self.AppCONFIG['EMAIL']['use_tls'] == "true":
            self.var_tls.set(1)
        else:
            self.var_tls.set(0)
        is_debug = ttk.Checkbutton(
            frame,
            text=T("Email uses TLS"),
            variable=self.var_tls,
            command=lambda: self.setEmail("TLS")
        )
        is_debug.grid(column=0, row=row, columnspan=2, padx=(10, 5), pady=(5, 5))

        self.var_ssl = IntVar()
        if self.AppCONFIG['EMAIL']['use_ssl'] is True or self.AppCONFIG['EMAIL']['use_ssl'] == "true":
            self.var_ssl.set(1)
        else:
            self.var_ssl.set(0)
        is_debug = ttk.Checkbutton(
            frame,
            text=T("Email uses SSL"),
            variable=self.var_ssl,
            command=lambda: self.setEmail("SSL")
        )
        is_debug.grid(column=1, row=row, columnspan=2, padx=(10, 5), pady=(5, 5))

        self.frame_canvas.create_window((0, 0), window=frame, anchor='nw')
        self.frame_canvas.bind('<Configure>', self.onConfigure)

        self.openGeometry()
        if "ProjectPWA_state" in self.CONFIG:
            if self.CONFIG["ProjectPWA_state"] == "zoomed":
                self.tkInstance.state("zoomed")
            else:
                self.tkInstance.deiconify()
        else:
            self.tkInstance.deiconify()
        self.tkInstance.attributes('-topmost', True)
        self.tkInstance.update()
        self.tkInstance.attributes('-topmost', False)

    def validAndSave(self, entry):
        if entry == "Name":
            v = self.project_name_input.get()
            if v.isidentifier():
                self.AppCONFIG['PROJECT']['name'] = v
                self.updateAppCONFIG()
            else:
                self.project_name_input.delete(0, END)
                self.project_name_input.insert(0, self.AppCONFIG['PROJECT']['name'])
                messagebox.showinfo(
                    T("Invalid name identifier!"),
                    T(
                        "".join(["The given name \"",
                        v,
                        "\" cannot be used as an identifier, cannot have spaces or special characters."])
                    )
                )
        elif entry == "Title":
            v = self.project_title_input.get()
            self.AppCONFIG['PROJECT']['title'] = v
            self.updateAppCONFIG()
        elif entry == "Version":
            v = self.project_version_input.get()
            r = re.compile(r"^([0-9]*\.[0-9]*.[0-9]*)$")
            if r.match(v):
                self.AppCONFIG['PROJECT']['version'] = v
                self.updateAppCONFIG()
            else:
                self.project_name_input.delete(0, END)
                self.project_name_input.insert(0, self.AppCONFIG['PROJECT']['version'])
                messagebox.showinfo(
                    T("Invalid version identifier!"),
                    T(
                        "".join(["The given version \"",
                        v,
                        "\" cannot be used. ",
                        "The version should follow the A.B.C standard, ",
                        "where A is the major version (Incompatible with",
                        " previous versions), B the minor version (Insertion",
                        " of new functionality without breaking compatibility)",
                        " and C a for bug fixes."])
                    )
                )
        elif entry == "Author":
            v = self.project_author_input.get()
            self.AppCONFIG['PROJECT']['author'] = v
            self.updateAppCONFIG()
        elif entry == "Email_server":
            v = self.email_server_input.get()
            self.AppCONFIG['EMAIL']['server'] = v
            self.updateAppCONFIG()
        elif entry == "Email_username":
            v = self.email_username_input.get()
            self.AppCONFIG['EMAIL']['username'] = v
            self.updateAppCONFIG()
        elif entry == "Email_password":
            v = self.email_password_input.get()
            self.AppCONFIG['EMAIL']['password'] = v
            self.updateAppCONFIG()
        elif entry == "Email_port":
            v = self.email_port_input.get()
            self.AppCONFIG['EMAIL']['port'] = v
            self.updateAppCONFIG()

    def compileApp(self, projectPath):
        choice = messagebox.askquestion(
            T("Are you sure?"),
            T("".join(["Do you really want to compile the app?"])),
            icon='warning'
        )
        if choice == "yes":
            name_dir = os.path.basename(projectPath)
            button_0 = self.buttons_dict[projectPath][0]
            button_2 = self.buttons_dict[projectPath][2]
            button_3 = self.buttons_dict[projectPath][3]
            button_0.configure(state=DISABLED)
            button_2.configure(state=DISABLED)
            button_3.configure(state=DISABLED)
            button_0.update()
            button_2.update()
            button_3.update()

            button_1 = self.buttons_dict[projectPath][1]
            button_4 = self.buttons_dict[projectPath][4]
            if name_dir in self.Root.ApplicationsTornado:
                button_4.configure(state="normal")
                button_4.configure(text=T("Stoping..."))
                button_4.update()
                button_4.configure(state=DISABLED)
                button_1.configure(text=T("Waiting..."))
                button_1.update()
                button_1.configure(state=DISABLED)
                button_4.update()
                time.sleep(1)
                self.Root.ApplicationsTornado[name_dir].stop()
                self.Root.ApplicationsTornado[name_dir].tkInstance.destroy()
                time.sleep(1)
                del self.Root.ApplicationsTornado[name_dir]
                button_1.configure(state="normal")
                button_4.configure(state="normal")
                button_1.configure(text=T("Compiling..."))
                button_4.configure(text=T("Waiting..."))
                button_1.configure(state=DISABLED)
                button_4.configure(state=DISABLED)
                button_1.update()
                button_4.update()
                time.sleep(1)
                try:
                    Compiler(projectPath).compile()
                except Exception as e:
                    logger_app = logging.getLogger(name_dir)
                    logger_app.error("Problem in compilation", exc_info=True)
                    messagebox.showinfo(
                        T("Problem in compilation"),
                        "".join([
                            T("".join(["There was a problem while compiling the application,",
                                " check the log to learn more. \nError:"])),
                            " \n\n", str(e)

                        ])
                    )
                else:
                    messagebox.showinfo(
                        T("Sucess"),
                        T("Application compiled successfully!")
                    )
                finally:
                    button_4.configure(state="normal")
                    button_4.configure(text=T("Stoped"))
                    button_4.configure(style='Wf.TButton')
                    button_4.update()
                    button_1.configure(state="normal")
                    button_1.configure(text=T("Compile"))
                    button_1.update()
            else:
                button_4.configure(state=DISABLED)
                button_4.update()
                button_1.configure(text=T("Compiling..."))
                button_1.update()
                button_1.configure(state=DISABLED)
                time.sleep(1)
                try:
                    Compiler(projectPath).compile()
                except Exception as e:
                    logger_app = logging.getLogger(name_dir)
                    logger_app.error("Problem in compilation", exc_info=True)
                    messagebox.showinfo(
                        T("Problem in compilation"),
                        "".join([
                            T(
                                "".join(["There was a problem while compiling the application,",
                                " check the log to learn more. Error:"])
                            ),
                            " ",
                            str(e)

                        ])
                    )
                else:
                    messagebox.showinfo(
                        T("Sucess"),
                        T("Application compiled successfully!")
                    )
                finally:
                    button_1.configure(state="normal")
                    button_1.configure(text=T("Compile"))
                    button_1.update()
                    button_4.configure(state="normal")
                    button_4.configure(text=T("Stoped"))
                    button_4.configure(style='Wf.TButton')
                    button_4.update()
            button_0.configure(state="normal")
            button_2.configure(state="normal")
            button_3.configure(state="normal")
            button_0.update()
            button_2.update()
            button_3.update()

    def deleteApp(self, projectPath):
        choice = messagebox.askquestion(
            T("Are you sure?"),
            T("".join(["Do you really want to delete the app?"])),
            icon='warning'
        )
        if choice == "yes":
            name_dir = os.path.basename(projectPath)
            button_0 = self.buttons_dict[projectPath][0]
            button_1 = self.buttons_dict[projectPath][1]
            button_3 = self.buttons_dict[projectPath][3]
            button_0.configure(state=DISABLED)
            button_1.configure(state=DISABLED)
            button_3.configure(state=DISABLED)
            button_0.update()
            button_1.update()
            button_3.update()

            button_2 = self.buttons_dict[projectPath][2]
            button_4 = self.buttons_dict[projectPath][4]
            if name_dir in self.Root.ApplicationsTornado:
                button_4.configure(state="normal")
                button_4.configure(text=T("Stoping..."))
                button_4.update()
                button_4.configure(state=DISABLED)
                button_2.configure(text=T("Waiting..."))
                button_2.update()
                button_2.configure(state=DISABLED)
                button_4.update()
                time.sleep(1)
                self.Root.ApplicationsTornado[name_dir].stop()
                self.Root.ApplicationsTornado[name_dir].tkInstance.destroy()
                time.sleep(1)
                del self.Root.ApplicationsTornado[name_dir]
                button_2.configure(state="normal")
                button_4.configure(state="normal")
                button_2.configure(text=T("Deleting..."))
                button_4.configure(text=T("Waiting..."))
                button_2.configure(state=DISABLED)
                button_4.configure(state=DISABLED)
                button_2.update()
                button_4.update()
                time.sleep(1)
                try:
                    if os.path.exists(projectPath):
                        shutil.rmtree(projectPath)
                    else:
                        raise IOError("The folder '{0}' not exists".format(projectPath))
                except Exception as e:
                    logger_app = logging.getLogger(name_dir)
                    logger_app.error("Problem on deletation", exc_info=True)
                    messagebox.showinfo(
                        T("Problem on deletation"),
                        "".join([
                            T("".join(["There was a problem while deleting the application,",
                                " check the log to learn more. \nError:"])),
                            " \n\n", str(e)

                        ])
                    )
                else:
                    messagebox.showinfo(
                        T("Sucess"),
                        T("Application deleted successfully!")
                    )
                finally:
                    button_4.configure(state="normal")
                    button_4.configure(text=T("Stoped"))
                    button_4.configure(style='Wf.TButton')
                    button_4.update()
                    button_2.configure(state="normal")
                    button_2.configure(text=T("Delete"))
                    button_2.update()
            else:
                try:
                    if os.path.exists(projectPath):
                        shutil.rmtree(projectPath)
                    else:
                        raise IOError("The folder '{0}' not exists".format(projectPath))
                except Exception as e:
                    logger_app = logging.getLogger(name_dir)
                    logger_app.error("Problem on deletation", exc_info=True)
                    messagebox.showinfo(
                        T("Problem on deletation"),
                        "".join([
                            T("".join(["There was a problem while deleting the application,",
                                " check the log to learn more. \nError:"])),
                            " \n\n", str(e)

                        ])
                    )
                else:
                    messagebox.showinfo(
                        T("Sucess"),
                        T("Application deleted successfully!")
                    )
                finally:
                    button_4.configure(state="normal")
                    button_4.configure(text=T("Stoped"))
                    button_4.configure(style='Wf.TButton')
                    button_4.update()
                    button_2.configure(state="normal")
                    button_2.configure(text=T("Delete"))
                    button_2.update()
            button_0.configure(state="normal")
            button_1.configure(state="normal")
            button_3.configure(state="normal")
            button_0.update()
            button_1.update()
            button_3.update()
            self.update()

    def packageApp(self, projectPath):
        choice = messagebox.askquestion(
            T("Are you sure?"),
            T("".join(["Do you really want to pack the app?"])),
            icon='warning'
        )
        target = None
        if choice:
            appConfig = config(projectPath)
            target = filedialog.askdirectory(initialdir=os.path.dirname(appConfig['PROJECT']['path']))
        if target:
            name_dir = os.path.basename(projectPath)
            button_0 = self.buttons_dict[projectPath][0]
            button_1 = self.buttons_dict[projectPath][1]
            button_2 = self.buttons_dict[projectPath][2]
            button_0.configure(state=DISABLED)
            button_1.configure(state=DISABLED)
            button_2.configure(state=DISABLED)
            button_0.update()
            button_1.update()
            button_2.update()

            button_3 = self.buttons_dict[projectPath][3]
            button_4 = self.buttons_dict[projectPath][4]
            if name_dir in self.Root.ApplicationsTornado:
                button_4.configure(state="normal")
                button_4.configure(text=T("Stoping..."))
                button_4.update()
                button_4.configure(state=DISABLED)
                button_3.configure(text=T("Waiting..."))
                button_3.update()
                button_3.configure(state=DISABLED)
                button_4.update()
                time.sleep(1)
                self.Root.ApplicationsTornado[name_dir].stop()
                self.Root.ApplicationsTornado[name_dir].tkInstance.destroy()
                time.sleep(1)
                del self.Root.ApplicationsTornado[name_dir]
                button_3.configure(state="normal")
                button_4.configure(state="normal")
                button_3.configure(text=T("Packing..."))
                button_4.configure(text=T("Waiting..."))
                button_3.configure(state=DISABLED)
                button_4.configure(state=DISABLED)
                button_3.update()
                button_4.update()
                time.sleep(1)
                try:
                    package_project_app(projectPath, target)
                except Exception as e:
                    logger_app = logging.getLogger(name_dir)
                    logger_app.error("Problem on packing", exc_info=True)
                    messagebox.showinfo(
                        T("Problem on packing"),
                        "".join([
                            T("".join(["There was a problem while packing the application,",
                                " check the log to learn more. \nError:"])),
                            " \n\n", str(e)

                        ])
                    )
                else:
                    messagebox.showinfo(
                        T("Sucess"),
                        T("Application packaged successfully!")
                    )
                finally:
                    button_4.configure(state="normal")
                    button_4.configure(text=T("Stoped"))
                    button_4.configure(style='Wf.TButton')
                    button_4.update()
                    button_3.configure(state="normal")
                    button_3.configure(text=T("Package"))
                    button_3.update()
            else:
                button_4.configure(state=DISABLED)
                button_4.update()
                button_3.configure(text=T("Packing..."))
                button_3.update()
                button_3.configure(state=DISABLED)
                time.sleep(1)
                try:
                    package_project_app(projectPath, target)
                except Exception as e:
                    logger_app = logging.getLogger(name_dir)
                    logger_app.error("Problem on packing", exc_info=True)
                    messagebox.showinfo(
                        T("Problem in packing"),
                        "".join([
                            T(
                                "".join(["There was a problem while packing the application,",
                                " check the log to learn more. Error:"])
                            ),
                            " ",
                            str(e)

                        ])
                    )
                else:
                    messagebox.showinfo(
                        T("Sucess"),
                        T("Application packaged successfully!")
                    )
                finally:
                    button_3.configure(state="normal")
                    button_3.configure(text=T("Package"))
                    button_3.update()
                    button_4.configure(state="normal")
                    button_4.update()
            button_0.configure(state="normal")
            button_1.configure(state="normal")
            button_2.configure(state="normal")
            button_0.update()
            button_1.update()
            button_2.update()

    def runApp(self, projectPath):
        name_dir = os.path.basename(projectPath)
        button_0 = self.buttons_dict[projectPath][0]
        button_1 = self.buttons_dict[projectPath][1]
        button_2 = self.buttons_dict[projectPath][2]
        button_3 = self.buttons_dict[projectPath][3]
        button_0.configure(state=DISABLED)
        button_1.configure(state=DISABLED)
        button_2.configure(state=DISABLED)
        button_3.configure(state=DISABLED)
        button_0.update()
        button_1.update()
        button_2.update()
        button_3.update()

        button_4 = self.buttons_dict[projectPath][4]

        if name_dir in self.Root.ApplicationsTornado:
            button_4.configure(text=T("Stoping..."))
            button_4.update()
            button_4.configure(state=DISABLED)
            button_4.update()
            time.sleep(1)
            print(self.Root.ApplicationsTornado[name_dir])
            self.Root.ApplicationsTornado[name_dir].stop()
            time.sleep(1)
            self.Root.ApplicationsTornado[name_dir].tkInstance.destroy()
            time.sleep(1)
            del self.Root.ApplicationsTornado[name_dir]
            button_4.configure(state="normal")
            button_4.configure(text=T("Stoped"))
            button_4.configure(style='Wf.TButton')
            button_0.configure(state="normal")
            button_1.configure(state="normal")
            button_2.configure(state="normal")
            button_3.configure(state="normal")
            button_0.update()
            button_1.update()
            button_2.update()
            button_3.update()
        else:
            button_4.configure(text=T("Starting..."))
            button_4.update()
            button_4.configure(state=DISABLED)
            button_4.update()
            time.sleep(1)
            self.current_app = tk.Toplevel(self.tkInstance)
            self.app = RunAPP(self.current_app, projectPath)
            self.Root.ApplicationsTornado[name_dir] = self.app
            time.sleep(2)
            button_4.configure(state="normal")
            button_4.configure(text=T("Running..."))
            button_4.configure(style='Wg.TButton')

    def add_new_app(self):
        pass

    def close(self):
        self.saveSize()
        self.Root.open_window_projects()
        self.tkInstance.destroy()

    def onConfigure(self, event):
        height = self.frame_canvas.bbox('all')[3]
        width = self.frame_canvas.bbox('all')[2]
        self.frame_canvas.configure(
            height=height,
            width=width,
            scrollregion=self.frame_canvas.bbox('all')
        )

    def open_window_config_api(self, project_path):
        self.saveSize()
        self.Root.open_window_config_api(project_path)
        self.tkInstance.destroy()

    def open_window_config_app(self, project_path, APP):
        self.saveSize()
        self.Root.open_window_config_app(project_path, APP)
        self.tkInstance.destroy()

    def openGeometry(self, event=None):
        if "ProjectPWA" in self.CONFIG:
            self.tkInstance.geometry(self.CONFIG["ProjectPWA"])

    def saveSize(self, event=None):
        self.CONFIG = config(
            CURRENT_DIR, {
                "ProjectPWA": self.tkInstance.geometry(),
                "ProjectPWA_state": self.tkInstance.state()
            }
        )

    def update(self):
        self.Root.open_window_project(self.project_path)

    def setDebug(self):
        v = self.var_debug.get()
        if v:
            self.AppCONFIG['PROJECT']['debug'] = True
        else:
            self.AppCONFIG['PROJECT']['debug'] = False
        self.updateAppCONFIG()

    def updateAppCONFIG(self):
        self.AppCONFIG = config(os.path.join(self.AppCONFIG["PROJECT"]["path"], "config.json"), self.AppCONFIG)


class ConfigAPI():
    def __init__(self, tkInstance, Root, project_path):
        self.CONFIG = config(CURRENT_DIR)
        self.AppCONFIG = config(project_path)
        self.project_path_name = os.path.basename(project_path)
        self.project_path = project_path
        self.Root = Root
        self.tkInstance = tkInstance
        self.tkInstance.withdraw()
        self.maxheight = 400
        scrollbar = Scrollbar(tkInstance, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self.frame_canvas = tk.Canvas(
            tkInstance,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.frame_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.frame_canvas.yview)
        self.frame_canvas.pack(side=LEFT, fill=Y, expand=TRUE)
        tkInstance.protocol('WM_DELETE_WINDOW', lambda: self.close())
        tkInstance.title("API - {0} - PhanterPWA".format(self.AppCONFIG['PROJECT']['title']))
        tkInstance.iconbitmap(os.path.join(CURRENT_DIR, "grafics", "icon.ico"))
        style_orange = ttk.Style()
        style_orange.configure('Wf.TButton', font=('default', 10, 'bold'), foreground='orange')
        style_green = ttk.Style()
        style_green.configure('Wg.TButton', font=('default', 10, 'bold'), foreground='green')
        frame = tk.Frame(self.frame_canvas)

        row = 0
        aLabel = ttk.Label(frame, text=T("API Configuration"), font='default 14 bold')
        aLabel.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 5))

        row += 1
        API_key_label = ttk.Label(frame, text=T("Secret Key"))
        API_key_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        API_key = self.AppCONFIG['API']['secret_key']
        self.API_key_input = ttk.Entry(frame, width=70)
        self.API_key_input.insert(0, API_key)
        self.API_key_input.config(state="readonly")
        self.API_key_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5), sticky="we")
        button = ttk.Button(frame, text=T("Generate"), command=lambda: self.generateSecret("secret_key"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        API_key_url_label = ttk.Label(frame, text=T("Secret url Key"))
        API_key_url_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        API_key_url = self.AppCONFIG['API']['secret_key']
        self.API_key_url_input = ttk.Entry(frame, width=70)
        self.API_key_url_input.insert(0, API_key_url)
        self.API_key_url_input.config(state="readonly")
        self.API_key_url_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5), sticky="we")
        button_url = ttk.Button(frame, text=T("Generate"), command=lambda: self.generateSecret("url_key"))
        button_url.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")
        time_values = {
            "default_time_user_token_expire": "User token expiration time",
            "default_time_user_token_expire_remember_me": "User token expiration time on \"Remember me\"",
            "default_time_csrf_token_expire": "CSRF expiration time (Form sign)",
            "default_time_temporary_password_expire": "Temporary password expiration time",
            "timeout_to_resend_temporary_password_mail": "\"Interval time\" to resend temporary password email",
            "default_time_client_token_expire": "Client token expiration time",
            "default_time_activation_code_expire": "Activation code expiration time",
            "wait_time_to_try_activate_again": "\"Wait time\" to try activate after all attempts",
            "timeout_to_resend_activation_email": "\"Wait time\" to resend a new activation code email",
            "timeout_to_resign": "\"Interval time\" to request new resign",
            "timeout_to_next_login_attempt": "\"Wait time\" to try login after all attempts",
        }
        for k in time_values:
            row += 1
            k_label = ttk.Label(frame, text=T(time_values[k]))
            k_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
            k_value = self.AppCONFIG['API'][k]
            self.k_input = ttk.Entry(frame, width=70)
            self.k_input.insert(
                0,
                "{0} ({1} seconds)".format(humanize_seconds(k_value, Trans), k_value)
            )
            self.k_input.config(state="readonly")
            self.k_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5), sticky="we")
            button = ttk.Button(
                frame,
                text=T("Change"),
                command=lambda Entry=self.k_input, seconds=k_value, key_api=k:
                    self.getSeconds(
                        Entry,
                        seconds,
                        key_api
                )
            )
            button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")
        row += 1
        api_max_login_attempts = ttk.Label(frame, text=T("Maximum Login Attempts"))
        api_max_login_attempts.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        max_login_attempts = self.AppCONFIG['API']['max_login_attempts']
        self.api_max_login_attempts_input = ttk.Entry(frame, width=50)
        self.api_max_login_attempts_input.insert(0, max_login_attempts)
        self.api_max_login_attempts_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        api_max_login_attempts_help = ttk.Label(frame, text="default: 5")
        api_max_login_attempts_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("max_login_attempts"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        api_max_activation_attempts = ttk.Label(frame, text=T("Maximum Activation Attempts"))
        api_max_activation_attempts.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        max_activation_attempts = self.AppCONFIG['API']['max_activation_attempts']
        self.api_max_activation_attempts_input = ttk.Entry(frame, width=50)
        self.api_max_activation_attempts_input.insert(0, max_activation_attempts)
        self.api_max_activation_attempts_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        api_max_activation_attempts_help = ttk.Label(frame, text="default: 5")
        api_max_activation_attempts_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("max_activation_attempts"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        api_remote_address = ttk.Label(frame, text=T("API Access Address"))
        api_remote_address.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        remote_address = self.AppCONFIG['API']['remote_address']
        self.api_remote_address_input = ttk.Entry(frame, width=50)
        self.api_remote_address_input.insert(0, remote_address)
        self.api_remote_address_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5), sticky="ew")
        api_remote_address_help = ttk.Label(frame, text="Default: http://localhost:8881")
        api_remote_address_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("remote_address"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        label_config_action = ttk.Label(frame, text=T("Tornado Server API Configuration"))
        label_config_action.grid(column=0, row=row, columnspan=3, padx=10, pady=(10, 0), sticky="w")

        row += 1
        hr_config_action = ttk.Separator(frame, orient=HORIZONTAL)
        hr_config_action.grid(column=0, row=row, columnspan=3, sticky='ew')

        row += 1
        api_host_label = ttk.Label(frame, text=T("Api server host"))
        api_host_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        api_host = self.AppCONFIG['API']['host']
        self.api_host_input = ttk.Entry(frame, width=50)
        self.api_host_input.insert(0, api_host)
        self.api_host_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        api_host_help = ttk.Label(frame, text="Default: 127.0.0.1")
        api_host_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("host"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        api_port_label = ttk.Label(frame, text=T("Api server port"))
        api_port_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        api_port = self.AppCONFIG['API']['port']
        self.api_port_input = ttk.Entry(frame, width=50)
        self.api_port_input.insert(0, api_port)
        self.api_port_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5), sticky="ew")
        api_port_help = ttk.Label(frame, text="Default: 8881")
        api_port_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("port"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        api_server_port_label = ttk.Label(frame, text=T("Results"))
        api_server_port_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        api_server_port_label = ttk.Label(
            frame,
            text="http://{0}:{1}/".format(self.api_host_input.get(), self.api_port_input.get()),
            width=50
        )
        api_server_port_label.grid(column=1, row=row, padx=(10, 5), pady=(5, 10))
        self.frame_canvas.create_window((0, 0), window=frame, anchor='nw')

        self.frame_canvas.bind('<Configure>', self.onConfigure)
        self.openGeometry()
        if "ConfigAPI_state" in self.CONFIG:
            if self.CONFIG["ConfigAPI_state"] == "zoomed":
                self.tkInstance.state("zoomed")
            else:
                self.tkInstance.deiconify()
        else:
            self.tkInstance.deiconify()
        self.tkInstance.attributes('-topmost', True)
        self.tkInstance.update()
        self.tkInstance.attributes('-topmost', False)

    def getSeconds(self, Entry, seconds, key_api):
        self.secondsWindow = tk.Toplevel(self.tkInstance)
        self.TimeCombox = TimeCombox(self.secondsWindow, seconds, Entry, self, key_api)

    def validAndSave(self, entry):
        if entry == "max_login_attempts":
            v = self.api_max_login_attempts_input.get()
            self.AppCONFIG['API']['max_login_attempts'] = v
            self.updateAppCONFIG()
        elif entry == "max_activation_attempts":
            v = self.api_max_activation_attempts_input.get()
            self.AppCONFIG['API']['max_activation_attempts'] = v
            self.updateAppCONFIG()
        elif entry == "remote_address":
            v = self.api_remote_address_input.get()
            self.AppCONFIG['API']['remote_address'] = v
            self.updateAppCONFIG()
        elif entry == "host":
            v = self.api_host_input.get()
            self.AppCONFIG['API']['host'] = v
            self.updateAppCONFIG()
        elif entry == "port":
            v = self.api_port_input.get()
            self.AppCONFIG['API']['port'] = v
            self.updateAppCONFIG()

    def updateAppCONFIG(self):
        self.AppCONFIG = config(os.path.join(self.AppCONFIG["PROJECT"]["path"], "config.json"), self.AppCONFIG)

    def generateSecret(self, context):
        if context == "secret_key":
            choice = messagebox.askquestion(
                T("Are you sure?"),
                T("".join(["This change affects all user passwords and access keys,",
                    " for security the current key will be stored in the config.json file."])),
                icon='warning'
            )
            if choice == "yes":
                cfg = config(CURRENT_DIR)
                ns = []
                if "secrets_keys" in cfg:
                    s = set(cfg["secrets_keys"])
                else:
                    s = set()
                a = self.API_key_input.get()
                s.add(a)
                ns = list(s)
                c = os.urandom(12).hex()
                self.AppCONFIG['API']['secret_key'] = str(c)
                self.updateAppCONFIG()
                self.API_key_input.config(state="normal")
                self.API_key_input.delete(0, END)
                self.API_key_input.insert(0, str(c))
                self.API_key_input.config(state="readonly")
                n = config(CURRENT_DIR, {"secrets_keys": ns})
                self.CONFIG = n
        elif context == "url_key":
            choice = messagebox.askquestion(
                T("Are you sure?"),
                T("".join(["This change affects all url access keys,",
                    " for security the current key will be stored in the config.json file."])),
                icon='warning'
            )
            if choice == "yes":
                cfg = config(CURRENT_DIR)
                ns = []
                if "url_keys" in cfg:
                    s = set(cfg["url_keys"])
                else:
                    s = set()
                a = self.API_key_input.get()
                s.add(a)
                ns = list(s)
                c = os.urandom(12).hex()
                self.AppCONFIG['API']["secret_key"] = str(c)
                self.updateAppCONFIG()
                self.API_key_input.config(state="normal")
                self.API_key_input.delete(0, END)
                self.API_key_input.insert(0, str(c))
                self.API_key_input.config(state="readonly")
                n = config(CURRENT_DIR, {"url_keys": ns})
                self.CONFIG = n

    def setEntryFolder(self, value):
        if value == "Enviroment_path":
            current_path = self.AppCONFIG["ENVIRONMENT"]["path"]
            folder = filedialog.askdirectory(initialdir=current_path)
            if folder:
                self.AppCONFIG["ENVIRONMENT"]["path"] = os.path.normpath(folder)
                self.updateAppCONFIG()
                self.enviroment_path_input.config(state="normal")
                self.enviroment_path_input.delete(0, END)
                self.enviroment_path_input.insert(0, os.path.normpath(folder))
                self.enviroment_path_input.config(state="readonly")
        elif value == "Project_path":
            current_path = self.AppCONFIG["PROJECT"]["path"]
            folder = filedialog.askdirectory(initialdir=current_path)
            if folder:
                self.AppCONFIG["PROJECT"]["path"] = os.path.normpath(folder)
                self.updateAppCONFIG()
                self.project_path_input.config(state="normal")
                self.project_path_input.delete(0, END)
                self.project_path_input.insert(0, os.path.normpath(folder))
                self.project_path_input.config(state="readonly")

    def setEntryFile(self, value):
        if value == "Enviroment_python":
            current_path = os.path.dirname(self.AppCONFIG["ENVIRONMENT"]["python"])
            file = filedialog.askopenfile(initialdir=current_path)
            if file:
                self.AppCONFIG["ENVIRONMENT"]["python"] = os.path.normpath(file.name)
                self.updateAppCONFIG()
                self.enviroment_python_input.config(state="normal")
                self.enviroment_python_input.delete(0, END)
                self.enviroment_python_input.insert(0, os.path.normpath(file.name))
                self.enviroment_python_input.config(state="readonly")
        elif value == "Transcrypt_main_file":
            current_path = os.path.dirname(self.AppCONFIG["TRANSCRYPT"]["main_files"])
            file = filedialog.askopenfile(initialdir=current_path)
            if file:
                self.AppCONFIG["TRANSCRYPT"]["main_files"] = os.path.normpath(file.name)
                self.updateAppCONFIG()
                self.transcrypt_main_file_input.config(state="normal")
                self.transcrypt_main_file_input.delete(0, END)
                self.transcrypt_main_file_input.insert(0, os.path.normpath(file.name))
                self.transcrypt_main_file_input.config(state="readonly")

    def close(self):
        self.saveSize()
        self.Root.open_window_project(self.project_path)
        self.tkInstance.destroy()

    def onConfigure(self, event):
        height = self.frame_canvas.bbox('all')[3]
        width = self.frame_canvas.bbox('all')[2]
        self.frame_canvas.configure(
            height=height,
            width=width,
            scrollregion=self.frame_canvas.bbox('all')
        )

    def openGeometry(self, event=None):
        if "ConfigAPI" in self.CONFIG:
            self.tkInstance.geometry(self.CONFIG["ConfigAPI"])

    def saveSize(self, event=None):
        self.CONFIG = config(
            CURRENT_DIR, {
                "ConfigAPI": self.tkInstance.geometry(),
                "ConfigAPI_state": self.tkInstance.state()
            }
        )


class ConfigAPP():
    def __init__(self, tkInstance, Root, project_path, APP):
        self.CONFIG = config(CURRENT_DIR)
        self.AppCONFIG = config(project_path)
        self.project_path_name = os.path.basename(project_path)
        self.project_path = project_path
        self.APP = APP
        self.Root = Root
        self.tkInstance = tkInstance
        self.tkInstance.withdraw()
        self.maxheight = 400
        scrollbar = Scrollbar(tkInstance, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self.frame_canvas = tk.Canvas(
            tkInstance,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.frame_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.frame_canvas.yview)
        self.frame_canvas.pack(side=LEFT, fill=Y, expand=TRUE)
        tkInstance.protocol('WM_DELETE_WINDOW', lambda: self.close())
        tkInstance.title("APP - {0} - PhanterPWA".format(self.AppCONFIG["FRONTEND"][APP]["title"]))
        tkInstance.iconbitmap(os.path.join(CURRENT_DIR, "grafics", "icon.ico"))
        style_orange = ttk.Style()
        style_orange.configure('Wf.TButton', font=('default', 10, 'bold'), foreground='orange')
        style_green = ttk.Style()
        style_green.configure('Wg.TButton', font=('default', 10, 'bold'), foreground='green')
        frame = tk.Frame(self.frame_canvas)

        row = 0
        aLabel = ttk.Label(frame, text=T("APP Configuration"), font='default 14 bold')
        aLabel.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 5))

        row += 1
        APP_title_label = ttk.Label(frame, text=T("Title"))
        APP_title_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        APP_title = self.AppCONFIG["FRONTEND"][APP]["title"]
        self.APP_title_input = ttk.Entry(frame, width=70)
        self.APP_title_input.insert(0, APP_title)
        self.APP_title_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5), sticky="we")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("title"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        APP_compiled_folder_label = ttk.Label(frame, text=T("Target folder on Compile"))
        APP_compiled_folder_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        APP_compiled_folder = self.AppCONFIG["FRONTEND"][APP]['build_folder']
        self.APP_compiled_folder_input = ttk.Entry(frame, width=70)
        self.APP_compiled_folder_input.insert(0, APP_compiled_folder)
        self.APP_compiled_folder_input.config(state="readonly")
        self.APP_compiled_folder_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5), sticky="we")
        button = ttk.Button(frame, text=T("Change"), command=lambda: self.setEntryFolder(APP))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")
        time_values = {
            "timeout_to_resign": "\"Interval time\" to auto request new resign",
        }
        for k in time_values:
            row += 1
            k_label = ttk.Label(frame, text=T(time_values[k]))
            k_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
            k_value = self.AppCONFIG["FRONTEND"][APP][k]
            self.k_input = ttk.Entry(frame, width=70)
            self.k_input.insert(
                0,
                "{0} ({1} seconds)".format(humanize_seconds(k_value, Trans), k_value)
            )
            self.k_input.config(state="readonly")
            self.k_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5), sticky="we")
            button = ttk.Button(
                frame,
                text=T("Change"),
                command=lambda Entry=self.k_input, seconds=k_value, key_api=k:
                    self.getSeconds(
                        Entry,
                        seconds,
                        key_api
                )
            )
            button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")
        row += 1
        api_host_label = ttk.Label(frame, text=T("App developer server host"))
        api_host_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        api_host = self.AppCONFIG['API']['host']
        self.api_host_input = ttk.Entry(frame, width=50)
        self.api_host_input.insert(0, api_host)
        self.api_host_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        api_host_help = ttk.Label(frame, text="Default: 127.0.0.1")
        api_host_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("host"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        api_port_label = ttk.Label(frame, text=T("App developer server port"))
        api_port_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        api_port = self.AppCONFIG['API']['port']
        self.api_port_input = ttk.Entry(frame, width=50)
        self.api_port_input.insert(0, api_port)
        self.api_port_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5), sticky="ew")
        api_port_help = ttk.Label(frame, text="Default: 8882")
        api_port_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("port"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        api_server_port_label = ttk.Label(frame, text=T("Results"))
        api_server_port_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5), sticky="e")
        api_server_port_label = ttk.Label(
            frame,
            text="http://{0}:{1}/".format(self.api_host_input.get(), self.api_port_input.get()),
            width=50
        )
        api_server_port_label.grid(column=1, row=row, padx=(10, 5), pady=(5, 10))

        row += 1

        self.frame_canvas.create_window((0, 0), window=frame, anchor='nw')

        self.frame_canvas.bind('<Configure>', self.onConfigure)
        self.openGeometry()
        if "ConfigAPP_state" in self.CONFIG:
            if self.CONFIG["ConfigAPP_state"] == "zoomed":
                self.tkInstance.state("zoomed")
            else:
                self.tkInstance.deiconify()
        else:
            self.tkInstance.deiconify()
        self.tkInstance.attributes('-topmost', True)
        self.tkInstance.update()
        self.tkInstance.attributes('-topmost', False)

    def getSeconds(self, Entry, seconds, APP, key_app):
        self.secondsWindow = tk.Toplevel(self.tkInstance)
        self.TimeCombox = TimeComboxAPP(self.secondsWindow, seconds, Entry, self, APP, key_app)

    def validAndSave(self, entry):
        if entry == "host":
            v = self.api_host_input.get()
            self.AppCONFIG["FRONTEND"][self.APP]['host'] = v
            self.updateAppCONFIG()
        elif entry == "port":
            v = self.api_port_input.get()
            self.AppCONFIG["FRONTEND"][self.APP]['port'] = v
            self.updateAppCONFIG()

    def updateAppCONFIG(self):
        self.AppCONFIG = config(os.path.join(self.AppCONFIG["PROJECT"]["path"], "config.json"), self.AppCONFIG)

    def generateSecret(self, context):
        if context == "secret_key":
            choice = messagebox.askquestion(
                T("Are you sure?"),
                T("".join(["This change affects all user passwords and access keys,",
                    " for security the current key will be stored in the config.json file."])),
                icon='warning'
            )
            if choice == "yes":
                cfg = config(CURRENT_DIR)
                ns = []
                if "secrets_keys" in cfg:
                    s = set(cfg["secrets_keys"])
                else:
                    s = set()
                a = self.API_key_input.get()
                s.add(a)
                ns = list(s)
                c = os.urandom(12).hex()
                self.AppCONFIG['API']['secret_key'] = str(c)
                self.updateAppCONFIG()
                self.API_key_input.config(state="normal")
                self.API_key_input.delete(0, END)
                self.API_key_input.insert(0, str(c))
                self.API_key_input.config(state="readonly")
                n = config(CURRENT_DIR, {"secrets_keys": ns})
                self.CONFIG = n
        elif context == "url_key":
            choice = messagebox.askquestion(
                T("Are you sure?"),
                T("".join(["This change affects all url access keys,",
                    " for security the current key will be stored in the config.json file."])),
                icon='warning'
            )
            if choice == "yes":
                cfg = config(CURRENT_DIR)
                ns = []
                if "url_keys" in cfg:
                    s = set(cfg["url_keys"])
                else:
                    s = set()
                a = self.API_key_input.get()
                s.add(a)
                ns = list(s)
                c = os.urandom(12).hex()
                self.AppCONFIG['API']["secret_key"] = str(c)
                self.updateAppCONFIG()
                self.API_key_input.config(state="normal")
                self.API_key_input.delete(0, END)
                self.API_key_input.insert(0, str(c))
                self.API_key_input.config(state="readonly")
                n = config(CURRENT_DIR, {"url_keys": ns})
                self.CONFIG = n

    def setEntryFolder(self, APP):

        current_path = self.AppCONFIG["FRONTEND"][APP]["build_folder"]
        folder = filedialog.askdirectory(initialdir=current_path)
        if folder:
            self.AppCONFIG["FRONTEND"][APP]["build_folder"] = os.path.normpath(folder)
            self.updateAppCONFIG()
            self.APP_compiled_folder_input.config(state="normal")
            self.APP_compiled_folder_input.delete(0, END)
            self.APP_compiled_folder_input.insert(0, os.path.normpath(folder))
            self.APP_compiled_folder_input.config(state="readonly")

    def setEntryFile(self, value):
        if value == "Enviroment_python":
            current_path = os.path.dirname(self.AppCONFIG["ENVIRONMENT"]["python"])
            file = filedialog.askopenfile(initialdir=current_path)
            if file:
                self.AppCONFIG["ENVIRONMENT"]["python"] = os.path.normpath(file.name)
                self.updateAppCONFIG()
                self.enviroment_python_input.config(state="normal")
                self.enviroment_python_input.delete(0, END)
                self.enviroment_python_input.insert(0, os.path.normpath(file.name))
                self.enviroment_python_input.config(state="readonly")
        elif value == "Transcrypt_main_file":
            current_path = os.path.dirname(self.AppCONFIG["TRANSCRYPT"]["main_files"])
            file = filedialog.askopenfile(initialdir=current_path)
            if file:
                self.AppCONFIG["TRANSCRYPT"]["main_files"] = os.path.normpath(file.name)
                self.updateAppCONFIG()
                self.transcrypt_main_file_input.config(state="normal")
                self.transcrypt_main_file_input.delete(0, END)
                self.transcrypt_main_file_input.insert(0, os.path.normpath(file.name))
                self.transcrypt_main_file_input.config(state="readonly")

    def close(self):
        self.saveSize()
        self.Root.open_window_project(self.project_path)
        self.tkInstance.destroy()

    def onConfigure(self, event):
        height = self.frame_canvas.bbox('all')[3]
        width = self.frame_canvas.bbox('all')[2]
        self.frame_canvas.configure(
            height=height,
            width=width,
            scrollregion=self.frame_canvas.bbox('all')
        )

    def openGeometry(self, event=None):
        if "ConfigAPP" in self.CONFIG:
            self.tkInstance.geometry(self.CONFIG["ConfigAPP"])

    def saveSize(self, event=None):
        self.CONFIG = config(
            CURRENT_DIR, {
                "ConfigAPP": self.tkInstance.geometry(),
                "ConfigAPP_state": self.tkInstance.state()
            }
        )


# class AppsPWA:
#     def __init__(self, tkInstance, project_path, MainPWA):
#         self.CONFIG = config(CURRENT_DIR)
#         self.AppCONFIG = config(project_path)
#         self.project_path_name = os.path.basename(project_path)
#         self.project_path = project_path
#         self.MainPWA = MainPWA
#         self.Root = MainPWA.Root
#         self.tkInstance = tkInstance
#         self.tkInstance.withdraw()
#         self.maxheight = 400
#         scrollbar = Scrollbar(tkInstance, orient=VERTICAL)
#         scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
#         self.frame_canvas = tk.Canvas(
#             tkInstance,
#             bd=0,
#             highlightthickness=0,
#             yscrollcommand=scrollbar.set
#         )
#         self.frame_canvas.config(yscrollcommand=scrollbar.set)
#         scrollbar.config(command=self.frame_canvas.yview)
#         self.frame_canvas.pack(side=LEFT, fill=Y, expand=TRUE)
#         tkInstance.protocol('WM_DELETE_WINDOW', lambda: self.close())
#         tkInstance.title("{0} - PhanterPWA".format(self.project_path_name))
#         tkInstance.iconbitmap(os.path.join(CURRENT_DIR, "grafics", "icon.ico"))
#         style_orange = ttk.Style()
#         style_orange.configure('Wf.TButton', font=('default', 10, 'bold'), foreground='orange')
#         style_green = ttk.Style()
#         style_green.configure('Wg.TButton', font=('default', 10, 'bold'), foreground='green')
#         frame = tk.Frame(self.frame_canvas)

#         row = 0
#         aLabel = ttk.Label(frame, text=T("Configuration"), font='default 14 bold')
#         aLabel.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 5))
#         row += 1
#         label_enviroment = ttk.Label(frame, text=T("Enviroment"))
#         label_enviroment.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 0), sticky="w")

#         row += 1
#         hr_enviroment = ttk.Separator(frame, orient=HORIZONTAL)
#         hr_enviroment.grid(column=0, row=row, columnspan=4, sticky='ew')

#         row += 1
#         enviroment_path_label = ttk.Label(frame, text=T("Path"))
#         enviroment_path_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
#         enviroment_path_data = self.AppCONFIG['ENVIRONMENT']['path']
#         self.enviroment_path_input = ttk.Entry(frame, width=70)
#         self.enviroment_path_input.insert(0, enviroment_path_data)
#         self.enviroment_path_input.config(state="readonly")
#         self.enviroment_path_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
#         button = ttk.Button(frame, text=T("Change"), command=lambda: self.setEntryFolder("Enviroment_path"))
#         button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

#         row += 1
#         enviroment_python_label = ttk.Label(frame, text=T("Python"))
#         enviroment_python_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
#         enviroment_python_data = self.AppCONFIG['ENVIRONMENT']['python']
#         self.enviroment_python_input = ttk.Entry(frame, width=70)
#         self.enviroment_python_input.insert(0, enviroment_python_data)
#         self.enviroment_python_input.config(state="readonly")
#         self.enviroment_python_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
#         button = ttk.Button(frame, text=T("Change"), command=lambda: self.setEntryFile("Enviroment_python"))
#         button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

#         row += 1
#         label_transcrypt = ttk.Label(frame, text=T("Transcrypt"))
#         label_transcrypt.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 0), sticky="w")

#         row += 1
#         hr_transcrypt = ttk.Separator(frame, orient=HORIZONTAL)
#         hr_transcrypt.grid(column=0, row=row, columnspan=4, sticky='ew')

#         row += 1
#         label_API = ttk.Label(frame, text=T("API"))
#         label_API.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 0), sticky="w")

#         row += 1
#         hr_API = ttk.Separator(frame, orient=HORIZONTAL)
#         hr_API.grid(column=0, row=row, columnspan=4, sticky='ew')

#         row += 1
#         API_key_label = ttk.Label(frame, text=T("Secret Key"))
#         API_key_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
#         API_key = self.AppCONFIG['API']['secret_key']
#         self.API_key_input = ttk.Entry(frame, width=70)
#         self.API_key_input.insert(0, API_key)
#         self.API_key_input.config(state="readonly")
#         self.API_key_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
#         button = ttk.Button(frame, text=T("Generate"), command=self.generateSecret)
#         button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

#         # default_time_user_token_expire
#         row += 1
#         API_key_token_label = ttk.Label(frame, text=T("Token time"))
#         API_key_token_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
#         API_key_token = self.AppCONFIG['API']['default_time_user_token_expire']
#         self.API_key_token_input = ttk.Entry(frame, width=70)
#         self.API_key_token_input.insert(
#             0,
#             "{0} ({1} seconds)".format(humanize_seconds(API_key_token, Trans), API_key_token)
#         )
#         self.API_key_token_input.config(state="readonly")
#         self.API_key_token_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
#         button = ttk.Button(
#             frame,
#             text=T("Change"),
#             command=lambda z='default_time_user_token_expire',
#                 y=API_key_token,
#                 x=self.API_key_token_input: self.getSeconds(
#                     x,
#                     y,
#                     z
#             )
#         )
#         button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

#         # default_time_csrf_token_expire
#         row += 1
#         API_key_csrf_label = ttk.Label(frame, text=T("CSRF token time"))
#         API_key_csrf_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
#         API_key_csrf = self.AppCONFIG['API']['default_time_csrf_token_expire']
#         self.API_key_csrf_input = ttk.Entry(frame, width=70)
#         self.API_key_csrf_input.insert(
#             0,
#             "{0} ({1} seconds)".format(humanize_seconds(API_key_csrf, Trans), API_key_csrf)
#         )
#         self.API_key_csrf_input.config(state="readonly")
#         self.API_key_csrf_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
#         button = ttk.Button(
#             frame,
#             text=T("Change"),
#             command=lambda z='default_time_csrf_token_expire',
#                 y=API_key_csrf,
#                 x=self.API_key_csrf_input: self.getSeconds(
#                     x,
#                     y,
#                     z
#             )
#         )
#         button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

#         row += 1
#         API_key_passsword_label = ttk.Label(frame, text=T("Temporary password time"))
#         API_key_passsword_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
#         API_key_passsword = self.AppCONFIG['API']['default_time_temporary_password_expire']
#         self.API_key_passsword_input = ttk.Entry(frame, width=70)
#         self.API_key_passsword_input.insert(
#             0,
#             "{0} ({1} seconds)".format(humanize_seconds(API_key_passsword, Trans), API_key_passsword)
#         )
#         self.API_key_passsword_input.config(state="readonly")
#         self.API_key_passsword_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
#         button = ttk.Button(
#             frame,
#             text=T("Change"),
#             command=lambda z='default_time_temporary_password_expire',
#                 y=API_key_passsword,
#                 x=self.API_key_passsword_input: self.getSeconds(
#                     x,
#                     y,
#                     z
#             )
#         )
#         button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

#         row += 1
#         API_key_attempt_login_label = ttk.Label(frame, text=T("Attempt to login time"))
#         API_key_attempt_login_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
#         API_key_attempt_login = self.AppCONFIG['API']['default_time_temporary_password_expire']
#         self.API_key_attempt_login_input = ttk.Entry(frame, width=70)
#         self.API_key_attempt_login_input.insert(
#             0,
#             "{0} ({1} seconds)".format(humanize_seconds(API_key_attempt_login, Trans), API_key_attempt_login)
#         )
#         self.API_key_attempt_login_input.config(state="readonly")
#         self.API_key_attempt_login_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
#         button = ttk.Button(
#             frame,
#             text=T("Change"),
#             command=lambda z='default_time_temporary_password_expire',
#                 y=API_key_attempt_login,
#                 x=self.API_key_attempt_login_input: self.getSeconds(
#                     x,
#                     y,
#                     z
#             )
#         )
#         button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")
#         row += 1

#         API_key_client_token_label = ttk.Label(frame, text=T("Client Token time"))
#         API_key_client_token_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
#         API_key_client_token = self.AppCONFIG['API']['default_time_client_token_expire']
#         self.API_key_client_token_input = ttk.Entry(frame, width=70)
#         self.API_key_client_token_input.insert(
#             0,
#             "{0} ({1} seconds)".format(humanize_seconds(API_key_client_token, Trans), API_key_client_token)
#         )
#         self.API_key_client_token_input.config(state="readonly")
#         self.API_key_client_token_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
#         button = ttk.Button(
#             frame,
#             text=T("Change"),
#             command=lambda z='default_time_client_token_expire',
#                 y=API_key_client_token,
#                 x=self.API_key_client_token_input: self.getSeconds(
#                     x,
#                     y,
#                     z
#             )
#         )
#         button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

#         row += 1
#         label_config_action = ttk.Label(frame, text=T("APP"))
#         label_config_action.grid(column=0, row=row, columnspan=3, padx=10, pady=(10, 0), sticky="w")

#         row += 1
#         hr_config_action = ttk.Separator(frame, orient=HORIZONTAL)
#         hr_config_action.grid(column=0, row=row, columnspan=3, sticky='ew')

#         row += 1
#         api_server_address = ttk.Label(frame, text=T("API Access by"))
#         api_server_address.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
#         server_adress = self.AppCONFIG['API']['remote_address']
#         self.api_server_address = ttk.Entry(frame, width=50)
#         self.api_server_address.insert(0, server_adress)
#         self.api_server_address.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
#         api_server_address_help = ttk.Label(frame, text="http://localhost:8881")
#         api_server_address_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
#         button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("API_access_by"))
#         button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

#         row += 1
#         label_config_action = ttk.Label(frame, text=T("Tornado Server"))
#         label_config_action.grid(column=0, row=row, columnspan=3, padx=10, pady=(10, 0), sticky="w")

#         row += 1
#         hr_config_action = ttk.Separator(frame, orient=HORIZONTAL)
#         hr_config_action.grid(column=0, row=row, columnspan=3, sticky='ew')

#         row += 1
#         api_server_host_label = ttk.Label(frame, text=T("Api server host"))
#         api_server_host_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
#         api_server_host = self.AppCONFIG['API']['host']
#         self.api_server_host_input = ttk.Entry(frame, width=50)
#         self.api_server_host_input.insert(0, api_server_host)
#         self.api_server_host_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
#         api_server_host_help = ttk.Label(frame, text="Default(127.0.0.1)")
#         api_server_host_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
#         button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Api_server_host"))
#         button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

#         row += 1
#         api_server_port_label = ttk.Label(frame, text=T("Api server port"))
#         api_server_port_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
#         api_server_port = self.AppCONFIG['API']['port']
#         self.api_server_port_input = ttk.Entry(frame, width=50)
#         self.api_server_port_input.insert(0, api_server_port)
#         self.api_server_port_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
#         api_server_port_help = ttk.Label(frame, text="Default(5000)")
#         api_server_port_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
#         button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Api_server_port"))
#         button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

#         row += 1
#         api_server_port_label = ttk.Label(frame, text=T("Results"))
#         api_server_port_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
#         api_server_port_label = ttk.Label(
#             frame,
#             text="http://{0}:{1}/".format(self.api_server_host_input.get(), self.api_server_port_input.get()),
#             width=50
#         )
#         api_server_port_label.grid(column=1, row=row, padx=(10, 5), pady=(5, 10))

#         row += 1
#         self.var_debug = IntVar()
#         if self.AppCONFIG['PROJECT']['debug'] is True or self.AppCONFIG['PROJECT']['debug'] == "true":
#             self.var_debug.set(1)
#             is_debug = ttk.Checkbutton(frame, text=T("Debug"), variable=self.var_debug, command=self.setDebug)
#         else:
#             self.var_debug.set(0)
#             is_debug = ttk.Checkbutton(frame, text=T("Debug"), variable=self.var_debug, command=self.setDebug)
#         is_debug.grid(column=0, row=row, columnspan=4, padx=(10, 5), pady=(5, 5))

#         row += 1

#         self.button_compile = ttk.Button(frame, text=T("Compile"), command=self.compileApp)
#         self.button_compile.grid(column=0, row=row, columnspan=2, padx=(10, 10), pady=(5, 50))
#         if os.path.basename(self.project_path) in self.Root.ApplicationsTornado:
#             self.button_start = ttk.Button(frame, text=T("Running..."), command=self.runApp)
#             self.button_start.grid(column=2, row=row, columnspan=1, padx=(10, 10), pady=(5, 50))
#             self.button_start.configure(style='Wg.TButton')
#         else:
#             self.button_start = ttk.Button(frame, text=T("Stoped"), command=self.runApp)
#             self.button_start.grid(column=2, row=row, columnspan=1, padx=(10, 10), pady=(5, 50))
#             self.button_start.configure(style='Wf.TButton')
#         self.button_start.update()
#         self.frame_canvas.create_window((0, 0), window=frame, anchor='nw')

#         self.frame_canvas.bind('<Configure>', self.onConfigure)
#         self.openGeometry()
#         if "AppsPWA_state" in self.CONFIG:
#             if self.CONFIG["AppsPWA_state"] == "zoomed":
#                 self.tkInstance.state("zoomed")
#             else:
#                 self.tkInstance.deiconify()
#         else:
#             self.tkInstance.deiconify()
#         self.tkInstance.attributes('-topmost', True)
#         self.tkInstance.update()
#         self.tkInstance.attributes('-topmost', False)

#     def compileApp(self, ):
#         projectPath = self.project_path
#         choice = messagebox.askquestion(
#             T("Are you sure?"),
#             T("".join(["Do you really want to compile the app?"])),
#             icon='warning'
#         )
#         if choice == "yes":
#             name_dir = os.path.basename(projectPath)
#             b1 = self.button_compile
#             b2 = self.button_start
#             if name_dir in self.Root.ApplicationsTornado:
#                 b2.configure(text=T("Stoping..."))
#                 b2.update()
#                 b2.configure(state=DISABLED)
#                 b1.configure(text=T("Waiting..."))
#                 b1.update()
#                 b1.configure(state=DISABLED)
#                 b2.update()
#                 time.sleep(1)
#                 self.Root.ApplicationsTornado[name_dir].stop()
#                 self.Root.ApplicationsTornado[name_dir].tkInstance.destroy()
#                 time.sleep(1)
#                 del self.Root.ApplicationsTornado[name_dir]
#                 b1.configure(state="normal")
#                 b2.configure(state="normal")
#                 b1.configure(text=T("Compiling..."))
#                 b2.configure(text=T("Waiting..."))
#                 b1.configure(state=DISABLED)
#                 b2.configure(state=DISABLED)
#                 b1.update()
#                 b2.update()
#                 time.sleep(1)
#                 try:
#                     Compiler(projectPath).compile()
#                 except Exception as e:
#                     logger_app = logging.getLogger(name_dir)
#                     logger_app.error("Problem on packing", exc_info=True)
#                     messagebox.showinfo(
#                         T("Problem in compilation"),
#                         "".join([
#                             T("".join(["There was a problem while compiling the application,",
#                                 " check the log to learn more. \nError:"])),
#                             " \n\n", str(e)
#                         ])
#                     )
#                 else:
#                     messagebox.showinfo(
#                         T("Sucess"),
#                         T("Application compiled successfully!")
#                     )
#                 finally:
#                     b2.configure(state="normal")
#                     b2.configure(text=T("Stoped"))
#                     b2.configure(style='Wf.TButton')
#                     b2.update()
#                     b1.configure(state="normal")
#                     b1.configure(text=T("Compile"))
#                     b1.update()
#             else:
#                 b2.configure(state=DISABLED)
#                 b2.update()
#                 b1.configure(text=T("Compiling..."))
#                 b1.update()
#                 b1.configure(state=DISABLED)
#                 time.sleep(1)
#                 try:
#                     Compiler(projectPath).compile()
#                 except Exception as e:
#                     logger_app = logging.getLogger(name_dir)
#                     logger_app.error("Problem on packing", exc_info=True)
#                     messagebox.showinfo(
#                         T("Problem in compilation"),
#                         "".join([
#                             T(
#                                 "".join(["There was a problem while compiling the application,",
#                                 " check the log to learn more. Error:"])
#                             ),
#                             " ",
#                             str(e)
#                         ])
#                     )
#                 else:
#                     messagebox.showinfo(
#                         T("Sucess"),
#                         T("Application compiled successfully!")
#                     )
#                 finally:
#                     b1.configure(state="normal")
#                     b1.configure(text=T("Compile"))
#                     b1.update()
#                     b2.configure(state="normal")
#                     b2.update()

#     def getSeconds(self, Entry, seconds, key_api):
#         self.secondsWindow = tk.Toplevel(self.tkInstance)
#         self.TimeCombox = TimeCombox(self.secondsWindow, seconds, Entry, self, key_api)

#     def runApp(self):
#         name_dir = self.project_path_name
#         b = self.button_start

#         if name_dir in self.Root.ApplicationsTornado:
#             b.configure(text=T("Stoping..."))
#             b.update()
#             b.configure(state=DISABLED)
#             b.update()
#             time.sleep(1)
#             self.Root.ApplicationsTornado[name_dir].stop()
#             self.Root.ApplicationsTornado[name_dir].tkInstance.destroy()
#             time.sleep(1)
#             del self.Root.ApplicationsTornado[name_dir]
#             b.configure(state="normal")
#             b.configure(text=T("Run"))
#         else:
#             b.configure(text=T("Starting..."))
#             b.update()
#             b.configure(state=DISABLED)
#             b.update()
#             time.sleep(1)
#             self.current_app = tk.Toplevel(self.tkInstance)
#             self.app = RunAPP(self.current_app, self.project_path)
#             self.Root.ApplicationsTornado[name_dir] = self.app
#             time.sleep(2)
#             b.configure(state="normal")
#             b.configure(text=T("Stop"))

#     def setEmail(self, value):
#         if value == "SSL":
#             v = self.var_ssl.get()
#             if v:
#                 self.AppCONFIG['EMAIL']['use_ssl'] = True
#             else:
#                 self.AppCONFIG['EMAIL']['use_ssl'] = False
#         elif value == "TLS":
#             v = self.var_tls.get()
#             if v:
#                 self.AppCONFIG['EMAIL']['use_tls'] = True
#             else:
#                 self.AppCONFIG['EMAIL']['use_tls'] = False
#         self.updateAppCONFIG()

#     def validAndSave(self, entry):
#         if entry == "Name":
#             v = self.project_name_input.get()
#             if v.isidentifier():
#                 self.AppCONFIG['PROJECT']['name'] = v
#                 self.updateAppCONFIG()
#             else:
#                 self.project_name_input.delete(0, END)
#                 self.project_name_input.insert(0, self.AppCONFIG['PROJECT']['name'])
#                 messagebox.showinfo(
#                     T("Invalid name identifier!"),
#                     T(
#                         "".join(["The given name \"",
#                         v,
#                         "\" cannot be used as an identifier, cannot have spaces or special characters."])
#                     )
#                 )
#         elif entry == "Title":
#             v = self.project_title_input.get()
#             self.AppCONFIG['PROJECT']['title'] = v
#             self.updateAppCONFIG()
#         elif entry == "Version":
#             v = self.project_version_input.get()
#             r = re.compile(r"^([0-9]*\.[0-9]*.[0-9]*)$")
#             if r.match(v):
#                 self.AppCONFIG['PROJECT']['version'] = v
#                 self.updateAppCONFIG()
#             else:
#                 self.project_name_input.delete(0, END)
#                 self.project_name_input.insert(0, self.AppCONFIG['PROJECT']['version'])
#                 messagebox.showinfo(
#                     T("Invalid version identifier!"),
#                     T(
#                         "".join(["The given version \"",
#                         v,
#                         "\" cannot be used. ",
#                         "The version should follow the A.B.C standard, ",
#                         "where A is the major version (Incompatible with",
#                         " previous versions), B the minor version (Insertion",
#                         " of new functionality without breaking compatibility)",
#                         " and C a for bug fixes."])
#                     )
#                 )
#         elif entry == "Author":
#             v = self.project_author_input.get()
#             self.AppCONFIG['PROJECT']['author'] = v
#             self.updateAppCONFIG()
#         elif entry == "Email_server":
#             v = self.email_server_input.get()
#             self.AppCONFIG['EMAIL']['server'] = v
#             self.updateAppCONFIG()
#         elif entry == "Email_username":
#             v = self.email_username_input.get()
#             self.AppCONFIG['EMAIL']['username'] = v
#             self.updateAppCONFIG()
#         elif entry == "Email_password":
#             v = self.email_password_input.get()
#             self.AppCONFIG['EMAIL']['password'] = v
#             self.updateAppCONFIG()
#         elif entry == "Email_port":
#             v = self.email_port_input.get()
#             self.AppCONFIG['EMAIL']['port'] = v
#             self.updateAppCONFIG()
#         elif entry == "API_access_by":
#             v = self.api_server_address.get()
#             self.AppCONFIG['API']['remote_address'] = v
#             self.updateAppCONFIG()
#         elif entry == "Api_server_host":
#             v = self.api_server_host_input.get()
#             self.AppCONFIG['API']['host'] = v
#             self.updateAppCONFIG()
#         elif entry == "Api_server_port":
#             v = self.api_server_port_input.get()
#             self.AppCONFIG['API']['port'] = v
#             self.updateAppCONFIG()
#         elif entry == "App_server_host":
#             v = self.app_server_host_input.get()
#             self.AppCONFIG['APP_SERVER']['host'] = v
#             self.updateAppCONFIG()
#         elif entry == "App_server_port":
#             v = self.app_server_port_input.get()
#             self.AppCONFIG['APP_SERVER']['port'] = v
#             self.updateAppCONFIG()

#     def setDebug(self):
#         v = self.var_debug.get()
#         if v:
#             self.AppCONFIG['PROJECT']['debug'] = True
#         else:
#             self.AppCONFIG['PROJECT']['debug'] = False
#         self.updateAppCONFIG()

#     def updateAppCONFIG(self):
#         self.AppCONFIG = config(os.path.join(self.AppCONFIG["PROJECT"]["path"], "config.json"), self.AppCONFIG)

#     def generateSecret(self):
#         choice = messagebox.askquestion(
#             T("Are you sure?"),
#             T("".join(["This change affects all user passwords and access keys,",
#                 " for security the current key will be stored in the config.json file."])),
#             icon='warning'
#         )
#         if choice == "yes":
#             cfg = config(CURRENT_DIR)
#             ns = []
#             if "secrets_keys" in cfg:
#                 s = set(cfg["secrets_keys"])
#             else:
#                 s = set()
#             a = self.API_key_input.get()
#             s.add(a)
#             ns = list(s)
#             c = os.urandom(12).hex()
#             self.AppCONFIG['API']['secret_key'] = str(c)
#             self.updateAppCONFIG()
#             self.API_key_input.config(state="normal")
#             self.API_key_input.delete(0, END)
#             self.API_key_input.insert(0, str(c))
#             self.API_key_input.config(state="readonly")
#             n = config(CURRENT_DIR, {"secrets_keys": ns})
#             self.CONFIG = n

#     def setEntryFolder(self, value):
#         if value == "Enviroment_path":
#             current_path = self.AppCONFIG["ENVIRONMENT"]["path"]
#             folder = filedialog.askdirectory(initialdir=current_path)
#             if folder:
#                 self.AppCONFIG["ENVIRONMENT"]["path"] = os.path.normpath(folder)
#                 self.updateAppCONFIG()
#                 self.enviroment_path_input.config(state="normal")
#                 self.enviroment_path_input.delete(0, END)
#                 self.enviroment_path_input.insert(0, os.path.normpath(folder))
#                 self.enviroment_path_input.config(state="readonly")
#         elif value == "Project_path":
#             current_path = self.AppCONFIG["PROJECT"]["path"]
#             folder = filedialog.askdirectory(initialdir=current_path)
#             if folder:
#                 self.AppCONFIG["PROJECT"]["path"] = os.path.normpath(folder)
#                 self.AppCONFIG["PATH"]["api"] = os.path.normpath(os.path.join(folder, "api"))
#                 self.AppCONFIG["PATH"]["app"] = os.path.normpath(os.path.join(folder, "app"))
#                 self.updateAppCONFIG()
#                 self.project_path_input.config(state="normal")
#                 self.project_path_input.delete(0, END)
#                 self.project_path_input.insert(0, os.path.normpath(folder))
#                 self.project_path_input.config(state="readonly")

#     def setEntryFile(self, value):
#         if value == "Enviroment_python":
#             current_path = os.path.dirname(self.AppCONFIG["ENVIRONMENT"]["python"])
#             file = filedialog.askopenfile(initialdir=current_path)
#             if file:
#                 self.AppCONFIG["ENVIRONMENT"]["python"] = os.path.normpath(file.name)
#                 self.updateAppCONFIG()
#                 self.enviroment_python_input.config(state="normal")
#                 self.enviroment_python_input.delete(0, END)
#                 self.enviroment_python_input.insert(0, os.path.normpath(file.name))
#                 self.enviroment_python_input.config(state="readonly")
#         elif value == "Transcrypt_main_file":
#             current_path = os.path.dirname(self.AppCONFIG["TRANSCRYPT"]["main_files"])
#             file = filedialog.askopenfile(initialdir=current_path)
#             if file:
#                 self.AppCONFIG["TRANSCRYPT"]["main_files"] = os.path.normpath(file.name)
#                 self.updateAppCONFIG()
#                 self.transcrypt_main_file_input.config(state="normal")
#                 self.transcrypt_main_file_input.delete(0, END)
#                 self.transcrypt_main_file_input.insert(0, os.path.normpath(file.name))
#                 self.transcrypt_main_file_input.config(state="readonly")

#     def close(self):
#         self.saveSize()
#         self.tkInstance.destroy()
#         self.MainPWA.saveSize()
#         self.MainPWA.Root.open_window_projects()
#         self.MainPWA.tkInstance.destroy()

#     def onConfigure(self, event):
#         height = self.frame_canvas.bbox('all')[3]
#         width = self.frame_canvas.bbox('all')[2]
#         self.frame_canvas.configure(
#             height=height,
#             width=width,
#             scrollregion=self.frame_canvas.bbox('all')
#         )

#     def openGeometry(self, event=None):
#         if "AppsPWA" in self.CONFIG:
#             self.tkInstance.geometry(self.CONFIG["AppsPWA"])

#     def saveSize(self, event=None):
#         self.CONFIG = config(
#             CURRENT_DIR, {
#                 "AppsPWA": self.tkInstance.geometry(),
#                 "AppsPWA_state": self.tkInstance.state()
#             }
#         )



class TimeCombox():
    def __init__(self, tkinterInstance, seconds, Entry, AppsPWA, key_api=None):
        self.split_seconds = split_seconds(seconds)
        self.entry_seconds = Entry
        self.initial_value = seconds
        self.tkInstance = tkinterInstance
        self.tkInstance.withdraw()
        self.AppsPWA = AppsPWA
        self.key_api = key_api
        scrollbar = Scrollbar(self.tkInstance, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self.frame_canvas = tk.Canvas(
            self.tkInstance,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.frame_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.frame_canvas.yview)
        self.frame_canvas.pack(side=LEFT, fill=Y, expand=TRUE)

        self.tkInstance.title(T("Application Folder - PhanterPWA"))
        self.tkInstance.iconbitmap(os.path.join(CURRENT_DIR, "grafics", "icon.ico"))

        frame = tk.Frame(self.frame_canvas)

        row = 0
        aLabel = ttk.Label(frame, text=T("Seconds Converter"), font='default 14 bold')
        aLabel.grid(column=0, row=row, columnspan=6, padx=10, pady=(10, 5))

        row += 1
        year_label = ttk.Label(frame, text=T("Year(s)"))
        year_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        year_values = [0, 1, 2, 3, 4]
        self.yearCombox = ttk.Combobox(frame, width=10, values=year_values)
        self.yearCombox.current(year_values.index(self.split_seconds['year'] if 'year' in self.split_seconds else 0))
        self.yearCombox.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        self.yearCombox.bind("<<ComboboxSelected>>", self.comboxChange)


        month_label = ttk.Label(frame, text=T("Month(s)"))
        month_label.grid(column=2, row=row, padx=(10, 5), pady=(5, 5))
        month_values = [f for f in range(0, 12)]
        self.monthCombox = ttk.Combobox(frame, width=10, values=month_values)
        self.monthCombox.current(month_values.index(self.split_seconds['month'] if 'month' in self.split_seconds else 0))
        self.monthCombox.grid(column=3, row=row, padx=(5, 10), pady=(5, 5))
        self.monthCombox.bind("<<ComboboxSelected>>", self.comboxChange)


        day_label = ttk.Label(frame, text=T("Day(s)"))
        day_label.grid(column=4, row=row, padx=(10, 5), pady=(5, 5))
        day_values = [f for f in range(0, 30)]
        self.dayCombox = ttk.Combobox(frame, width=10, values=day_values)
        self.dayCombox.current(day_values.index(self.split_seconds['day'] if 'day' in self.split_seconds else 0))
        self.dayCombox.grid(column=5, row=row, padx=(5, 10), pady=(5, 5))
        self.dayCombox.bind("<<ComboboxSelected>>", self.comboxChange)

        row += 1
        hour_label = ttk.Label(frame, text=T("Hour(s)"))
        hour_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        hour_values = [f for f in range(0, 24)]
        self.hourCombox = ttk.Combobox(frame, width=10, values=hour_values)
        self.hourCombox.current(hour_values.index(self.split_seconds['hour'] if 'hour' in self.split_seconds else 0))
        self.hourCombox.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        self.hourCombox.bind("<<ComboboxSelected>>", self.comboxChange)

        minute_label = ttk.Label(frame, text=T("Minute(s)"))
        minute_label.grid(column=2, row=row, padx=(10, 5), pady=(5, 5))
        minute_values = [f for f in range(0, 60)]
        self.minuteCombox = ttk.Combobox(frame, width=10, values=minute_values)
        self.minuteCombox.current(minute_values.index(self.split_seconds['minute'] if 'minute' in self.split_seconds else 0))
        self.minuteCombox.grid(column=3, row=row, padx=(5, 10), pady=(5, 5))
        self.minuteCombox.bind("<<ComboboxSelected>>", self.comboxChange)


        second_label = ttk.Label(frame, text=T("Second(s)"))
        second_label.grid(column=4, row=row, padx=(10, 5), pady=(5, 5))
        second_values = [f for f in range(0, 60)]
        self.secondCombox = ttk.Combobox(frame, width=10, values=second_values)
        self.secondCombox.current(second_values.index(self.split_seconds['second'] if 'second' in self.split_seconds else 0))
        self.secondCombox.grid(column=5, row=row, padx=(5, 10), pady=(5, 5))
        self.secondCombox.bind("<<ComboboxSelected>>", self.comboxChange)

        row += 1
        self.label_verify = ttk.Label(frame, text=Entry.get())
        self.label_verify.grid(column=0, row=row, columnspan=6, padx=(10, 5), pady=(5, 5))

        row += 1
        self.buttonOK = ttk.Button(frame, text=T("OK"), command=self.confirmChange, state=DISABLED)
        self.buttonOK.grid(column=0, row=row, columnspan=6, padx=10, pady=(5, 5))

        self.frame_canvas.create_window((0, 0), window=frame, anchor='nw')
        self.frame_canvas.bind('<Configure>', self.onConfigure)
        self.tkInstance.resizable(0, 0)
        self.tkInstance.deiconify()

    def comboxChange(self, event):
        s_seconds = {}
        s_seconds['year'] = int(self.yearCombox.get())
        s_seconds['month'] = int(self.monthCombox.get())
        s_seconds['day'] = int(self.dayCombox.get())
        s_seconds['hour'] = int(self.hourCombox.get())
        s_seconds['minute'] = int(self.minuteCombox.get())
        s_seconds['second'] = int(self.secondCombox.get())
        t_seconds = join_seconds(s_seconds)
        self.label_verify.configure(text="{0} ({1} second(s))".format(
            humanize_seconds(t_seconds, Trans),
            t_seconds
        ))
        if self.initial_value != t_seconds:
            self.buttonOK.configure(state="normal")
        else:
            self.buttonOK.configure(state=DISABLED)

    def onConfigure(self, event):
        height = self.frame_canvas.bbox('all')[3]
        width = self.frame_canvas.bbox('all')[2]
        self.frame_canvas.configure(
            height=height,
            width=width,
            scrollregion=self.frame_canvas.bbox('all')
        )

    def confirmChange(self):
        v = self.label_verify.cget("text")
        s_seconds = {}
        s_seconds['year'] = int(self.yearCombox.get())
        s_seconds['month'] = int(self.monthCombox.get())
        s_seconds['day'] = int(self.dayCombox.get())
        s_seconds['hour'] = int(self.hourCombox.get())
        s_seconds['minute'] = int(self.minuteCombox.get())
        s_seconds['second'] = int(self.secondCombox.get())
        t_seconds = join_seconds(s_seconds)
        self.entry_seconds.config(state="normal")
        self.entry_seconds.delete(0, END)
        self.entry_seconds.insert(0, v)
        self.entry_seconds.config(state="readonly")
        if self.key_api:
            self.AppsPWA.AppCONFIG['API'][self.key_api] = t_seconds
            self.AppsPWA.updateAppCONFIG()
        self.tkInstance.destroy()

class TimeComboxAPP():
    def __init__(self, tkinterInstance, seconds, Entry, AppsPWA, APP, key_app=None):
        self.split_seconds = split_seconds(seconds)
        self.entry_seconds = Entry
        self.APP = APP
        self.initial_value = seconds
        self.tkInstance = tkinterInstance
        self.tkInstance.withdraw()
        self.AppsPWA = AppsPWA
        self.key_app = key_app
        scrollbar = Scrollbar(self.tkInstance, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self.frame_canvas = tk.Canvas(
            self.tkInstance,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.frame_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.frame_canvas.yview)
        self.frame_canvas.pack(side=LEFT, fill=Y, expand=TRUE)

        self.tkInstance.title(T("Application Folder - PhanterPWA"))
        self.tkInstance.iconbitmap(os.path.join(CURRENT_DIR, "grafics", "icon.ico"))

        frame = tk.Frame(self.frame_canvas)

        row = 0
        aLabel = ttk.Label(frame, text=T("Seconds Converter"), font='default 14 bold')
        aLabel.grid(column=0, row=row, columnspan=6, padx=10, pady=(10, 5))

        row += 1
        year_label = ttk.Label(frame, text=T("Year(s)"))
        year_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        year_values = [0, 1, 2, 3, 4]
        self.yearCombox = ttk.Combobox(frame, width=10, values=year_values)
        self.yearCombox.current(year_values.index(self.split_seconds['year'] if 'year' in self.split_seconds else 0))
        self.yearCombox.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        self.yearCombox.bind("<<ComboboxSelected>>", self.comboxChange)


        month_label = ttk.Label(frame, text=T("Month(s)"))
        month_label.grid(column=2, row=row, padx=(10, 5), pady=(5, 5))
        month_values = [f for f in range(0, 12)]
        self.monthCombox = ttk.Combobox(frame, width=10, values=month_values)
        self.monthCombox.current(month_values.index(self.split_seconds['month'] if 'month' in self.split_seconds else 0))
        self.monthCombox.grid(column=3, row=row, padx=(5, 10), pady=(5, 5))
        self.monthCombox.bind("<<ComboboxSelected>>", self.comboxChange)


        day_label = ttk.Label(frame, text=T("Day(s)"))
        day_label.grid(column=4, row=row, padx=(10, 5), pady=(5, 5))
        day_values = [f for f in range(0, 30)]
        self.dayCombox = ttk.Combobox(frame, width=10, values=day_values)
        self.dayCombox.current(day_values.index(self.split_seconds['day'] if 'day' in self.split_seconds else 0))
        self.dayCombox.grid(column=5, row=row, padx=(5, 10), pady=(5, 5))
        self.dayCombox.bind("<<ComboboxSelected>>", self.comboxChange)

        row += 1
        hour_label = ttk.Label(frame, text=T("Hour(s)"))
        hour_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        hour_values = [f for f in range(0, 24)]
        self.hourCombox = ttk.Combobox(frame, width=10, values=hour_values)
        self.hourCombox.current(hour_values.index(self.split_seconds['hour'] if 'hour' in self.split_seconds else 0))
        self.hourCombox.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        self.hourCombox.bind("<<ComboboxSelected>>", self.comboxChange)

        minute_label = ttk.Label(frame, text=T("Minute(s)"))
        minute_label.grid(column=2, row=row, padx=(10, 5), pady=(5, 5))
        minute_values = [f for f in range(0, 60)]
        self.minuteCombox = ttk.Combobox(frame, width=10, values=minute_values)
        self.minuteCombox.current(minute_values.index(self.split_seconds['minute'] if 'minute' in self.split_seconds else 0))
        self.minuteCombox.grid(column=3, row=row, padx=(5, 10), pady=(5, 5))
        self.minuteCombox.bind("<<ComboboxSelected>>", self.comboxChange)


        second_label = ttk.Label(frame, text=T("Second(s)"))
        second_label.grid(column=4, row=row, padx=(10, 5), pady=(5, 5))
        second_values = [f for f in range(0, 60)]
        self.secondCombox = ttk.Combobox(frame, width=10, values=second_values)
        self.secondCombox.current(second_values.index(self.split_seconds['second'] if 'second' in self.split_seconds else 0))
        self.secondCombox.grid(column=5, row=row, padx=(5, 10), pady=(5, 5))
        self.secondCombox.bind("<<ComboboxSelected>>", self.comboxChange)

        row += 1
        self.label_verify = ttk.Label(frame, text=Entry.get())
        self.label_verify.grid(column=0, row=row, columnspan=6, padx=(10, 5), pady=(5, 5))

        row += 1
        self.buttonOK = ttk.Button(frame, text=T("OK"), command=self.confirmChange, state=DISABLED)
        self.buttonOK.grid(column=0, row=row, columnspan=6, padx=10, pady=(5, 5))

        self.frame_canvas.create_window((0, 0), window=frame, anchor='nw')
        self.frame_canvas.bind('<Configure>', self.onConfigure)
        self.tkInstance.resizable(0, 0)
        self.tkInstance.deiconify()

    def comboxChange(self, event):
        s_seconds = {}
        s_seconds['year'] = int(self.yearCombox.get())
        s_seconds['month'] = int(self.monthCombox.get())
        s_seconds['day'] = int(self.dayCombox.get())
        s_seconds['hour'] = int(self.hourCombox.get())
        s_seconds['minute'] = int(self.minuteCombox.get())
        s_seconds['second'] = int(self.secondCombox.get())
        t_seconds = join_seconds(s_seconds)
        self.label_verify.configure(text="{0} ({1} second(s))".format(
            humanize_seconds(t_seconds, Trans),
            t_seconds
        ))
        if self.initial_value != t_seconds:
            self.buttonOK.configure(state="normal")
        else:
            self.buttonOK.configure(state=DISABLED)

    def onConfigure(self, event):
        height = self.frame_canvas.bbox('all')[3]
        width = self.frame_canvas.bbox('all')[2]
        self.frame_canvas.configure(
            height=height,
            width=width,
            scrollregion=self.frame_canvas.bbox('all')
        )

    def confirmChange(self):
        v = self.label_verify.cget("text")
        s_seconds = {}
        s_seconds['year'] = int(self.yearCombox.get())
        s_seconds['month'] = int(self.monthCombox.get())
        s_seconds['day'] = int(self.dayCombox.get())
        s_seconds['hour'] = int(self.hourCombox.get())
        s_seconds['minute'] = int(self.minuteCombox.get())
        s_seconds['second'] = int(self.secondCombox.get())
        t_seconds = join_seconds(s_seconds)
        self.entry_seconds.config(state="normal")
        self.entry_seconds.delete(0, END)
        self.entry_seconds.insert(0, v)
        self.entry_seconds.config(state="readonly")
        if self.key_app:
            self.AppsPWA.AppCONFIG["FRONTEND"][self.APP][self.key_app] = t_seconds
            self.AppsPWA.updateAppCONFIG()
        self.tkInstance.destroy()

class RunAPP:
    def __init__(self, tkInstance, projectPath):
        self.tkInstance = tkInstance
        self.tkInstance.withdraw()
        self.projectPath = projectPath
        self.AppCONFIG = config(projectPath)

        self.run()

        webbrowser.open_new("http://127.0.0.1:{0}".format(self.AppCONFIG["APP_SERVER"]["port"]))

    def run(self):
        self.target = os.path.normpath(os.path.join(CURRENT_DIR, "..", "server.py"))
        command = " ".join([ENV_PYTHON, self.target])
        self.subprocess = subprocess.Popen(command, cwd=self.projectPath, shell=True)

    def stop(self):
        for p in psutil.process_iter():
            cmd_line = None
            try:
                cmd_line = p.cmdline()
            except Exception:
                pass
            if cmd_line:
                if ENV_PYTHON == cmd_line[0]:
                    if os.path.normpath(self.target) == cmd_line[-1]:
                        p.terminate()


def start():
    win = tk.Tk()
    Root(win)
    win.mainloop()


if __name__ == '__main__':
    start()
