import os
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
from phanterpwa import __version__ as PHANTERPWA_VERSION
from phanterpwa.tools import (
    check_valid_project_config,
    list_installed_applications,
    config,
    humanize_seconds,
    splits_seconds,
    join_seconds,
    interpolate,
    package_project_app,
    compiler
)
from phanterpwa.i18n import Translator
ENV_PYTHON = os.path.normpath(sys.executable)
ENV_PATH = os.path.normpath(os.path.dirname(ENV_PYTHON))
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")
PY_VERSION = "{0}.{1}.{2}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])

CURRENT_DIR = os.path.dirname(__file__)

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
CONFIG = config(CURRENT_DIR)
Trans = Translator(os.path.join(CURRENT_DIR, "langs"), debug=True)
if "language" in CONFIG:
    Trans.direct_translation = CONFIG["language"]
T = Trans.T

_About = ""
with open(os.path.join(CURRENT_DIR, "..", "samples", "about_graphic"), 'r', encoding='utf-8') as f:
    _About = f.read()


class Root:
    def __init__(self, tkinterInstance):
        self.CONFIG = config(CURRENT_DIR)
        if "applications_folder" in self.CONFIG:
            if os.path.exists(self.CONFIG["applications_folder"]):
                self.applications_folder = self.CONFIG["applications_folder"]
        else:
            self.applications_folder = os.getcwd()
        self.master = tkinterInstance
        self.master.withdraw()
        self.maxheight = 400
        self.ApplicationsTornado = {}
        scrollbar = Scrollbar(self.master, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self.frame_canvas = tk.Canvas(
            self.master,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.frame_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.frame_canvas.yview)
        self.frame_canvas.pack(side=LEFT, fill=Y, expand=TRUE)

        self.master.title(T("Application Folder - PhanterPWA"))
        self.master.iconbitmap(os.path.join(CURRENT_DIR, "grafics", "icon.ico"))

        frame = tk.Frame(self.frame_canvas)

        row = 0
        aLabel = ttk.Label(frame, text=T("Where will your apps be saved?"), font='default 14 bold')
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
        self.buttonOK = ttk.Button(frame, text=T("OK"), command=self.openMainPWA, state=DISABLED)
        self.buttonOK.grid(column=0, row=row, columnspan=3, padx=10, pady=(5, 30))

        self.frame_canvas.create_window((0, 0), window=frame, anchor='nw')
        self.frame_canvas.bind('<Configure>', self.onConfigure)
        self.master.resizable(0, 0)
        self.master.maxsize(width=0, height=self.maxheight)
        self.master.resizable(0, 0)
        if "applications_folder" in self.CONFIG:
            if os.path.exists(self.CONFIG["applications_folder"]):
                self.applications_folder = self.CONFIG["applications_folder"]
                self.buttonOK.config(state="normal")
                self.app_folder_input.delete(0, END)
                self.app_folder_input.insert(0, os.path.normpath(self.applications_folder))
                self.openMainPWA()
        else:
            self.master.deiconify()
        self.master.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.master.attributes('-topmost', True)
        self.master.update()
        self.master.attributes('-topmost', False)

    def setEntryFolder(self, entry_instance):
        if self.applications_folder:
            folder = filedialog.askdirectory(initialdir=self.applications_folder)
        else:
            folder = filedialog.askdirectory()
        if folder:
            self.applications_folder = folder
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

    def openMainPWA(self):
        if self.app_folder_input.get():
            self.CONFIG = config(CURRENT_DIR, {"applications_folder": os.path.normpath(self.applications_folder)})
            self.master.withdraw()
            self.newWindow = tk.Toplevel(self.master)
            self.MainPWA = MainPWA(self.newWindow, self)

    def onClosing(self):
        for server_running in self.ApplicationsTornado:
            try:
                self.ApplicationsTornado[server_running].stop()
                self.ApplicationsTornado[server_running].master.destroy()
            except Exception:
                print("Try Close")
        self.master.destroy()


class MainPWA:
    def __init__(self, master, Root=None):
        self.CONFIG = config(CURRENT_DIR)
        self.Root = Root
        self.master = master
        self.master.withdraw()
        self.maxheight = 400

        scrollbar = Scrollbar(master, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self.frame_canvas = tk.Canvas(
            master,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )

        menubar = Menu(master)
        menubar.add_command(label=T("Change Application Folder"), command=self.changeAppFolder)
        menubar.add_command(label=T("Add Application"), command=self.setPPwaFile)
        if Trans.languages:
            langMenu = Menu(master, tearoff=False)
            menubar.add_cascade(label=T("Translate"), menu=langMenu)
            for v in Trans.languages:
                langMenu.add_command(labe=T(v), command=lambda v=v: self.setLang(str(v)))
        menubar.add_command(label=T("About"), command=self.about)

        master.config(menu=menubar)

        master.protocol('WM_DELETE_WINDOW', lambda: self.close())
        self.frame_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.frame_canvas.yview)
        self.frame_canvas.pack(side=LEFT, fill=Y, expand=TRUE)

        master.title("PhanterPWA")
        master.iconbitmap(os.path.join(CURRENT_DIR, "grafics", "icon.ico"))

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
        enviroment_path_input = ttk.Entry(frame, width=80)
        enviroment_path_input.insert(0, enviroment_path_data)
        enviroment_path_input.config(state="readonly")
        enviroment_path_input.grid(column=1, row=row, columnspan=5, padx=(0, 10), pady=(5, 5))

        row += 1
        enviroment_python_label = ttk.Label(frame, text=T("Python"))
        enviroment_python_label.grid(column=0, row=row, padx=(20, 5), pady=(5, 5), sticky="e")
        enviroment_python_data = ENV_PYTHON
        enviroment_python_input = ttk.Entry(frame, width=80)
        enviroment_python_input.insert(0, enviroment_python_data)
        enviroment_python_input.config(state="readonly")
        enviroment_python_input.grid(column=1, row=row, columnspan=5, padx=(0, 10), pady=(5, 5))

        row += 1
        enviroment_pythonv_label = ttk.Label(frame, text=T("Python Version"))
        enviroment_pythonv_label.grid(column=0, row=row, padx=(20, 5), pady=(5, 5), sticky="e")
        enviroment_pythonv_data = PY_VERSION
        enviroment_pythonv_input = ttk.Entry(frame, width=80)
        enviroment_pythonv_input.insert(0, enviroment_pythonv_data)
        enviroment_pythonv_input.config(state="readonly")
        enviroment_pythonv_input.grid(column=1, row=row, columnspan=5, padx=(0, 10), pady=(5, 5))

        row += 1
        enviroment_phanterpwav_label = ttk.Label(frame, text=T("PhanterPWA Version"))
        enviroment_phanterpwav_label.grid(column=0, row=row, padx=(20, 5), pady=(5, 5), sticky="e")
        enviroment_phanterpwav_data = PHANTERPWA_VERSION
        enviroment_phanterpwav_input = ttk.Entry(frame, width=80)
        enviroment_phanterpwav_input.insert(0, enviroment_phanterpwav_data)
        enviroment_phanterpwav_input.config(state="readonly")
        enviroment_phanterpwav_input.grid(column=1, row=row, columnspan=5, padx=(0, 10), pady=(5, 5))

        row += 1
        label_project = ttk.Label(frame, text=T("Installed Applications"), font='default 10 bold')
        label_project.grid(column=0, row=row, columnspan=6, padx=0, pady=(40, 0), sticky="w")

        row += 1
        hr_project = ttk.Separator(frame, orient=HORIZONTAL)
        hr_project.grid(column=0, row=row, columnspan=6, sticky='ew')

        row += 1
        enviroment_phanterpwav_label = ttk.Label(frame, text=T("Application Folder"))
        enviroment_phanterpwav_label.grid(column=0, row=row, padx=(20, 5), pady=(5, 5), sticky="e")
        enviroment_phanterpwav_data = self.CONFIG["applications_folder"]
        enviroment_phanterpwav_input = ttk.Entry(frame, width=80)
        enviroment_phanterpwav_input.insert(0, enviroment_phanterpwav_data)
        enviroment_phanterpwav_input.config(state="readonly")
        enviroment_phanterpwav_input.grid(column=1, row=row, columnspan=5, padx=(0, 10), pady=(5, 5))

        self.buttons_dict = {}
        style_orange = ttk.Style()
        style_orange.configure('Wf.TButton', font=('default', 10, 'bold'), foreground='orange')
        style_green = ttk.Style()
        style_green.configure('Wg.TButton', font=('default', 10, 'bold'), foreground='green')
        style_default = ttk.Style()
        style_default.configure('Wd.TButton', font=('default', 10))
        if "applications_folder" in self.CONFIG:
            if os.path.exists(self.CONFIG["applications_folder"]):
                apps = list_installed_applications(self.CONFIG["applications_folder"])
                if apps:
                    row += 1
                    for i in apps:
                        cfg_app = config(os.path.join(self.CONFIG["applications_folder"], i, "config.json"))
                        cfg_app['ENVIRONMENT']['path'] = ENV_PATH
                        cfg_app['ENVIRONMENT']['python'] = ENV_PYTHON
                        project_path = os.path.join(self.CONFIG["applications_folder"], i)
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
                        t_name = ttk.Entry(frame)
                        t_name.insert(0, cfg_app['PATH']['project'])
                        t_name.config(state="readonly")
                        t_name.grid(column=1, row=row, columnspan=4, padx=(0, 0), pady=(2, 2), sticky='ew')
                        row += 1
                        b0_name = ttk.Button(frame, text="Config", command=lambda x=project_path: self.openAppWin(x, self))
                        b0_name.grid(column=0, row=row, padx=(30, 2), pady=(2, 2), sticky='ew')
                        b1_name = ttk.Button(
                            frame, text=T("Compile"), command=lambda z=project_path: self.compileApp(z)
                        )
                        b1_name.grid(column=1, row=row, padx=(2, 2), pady=(2, 2), sticky='ew')
                        b2_name = ttk.Button(
                            frame, text=T("Delete"), command=lambda z=project_path: self.deleteApp(z)
                        )
                        b2_name.grid(column=2, row=row, padx=(2, 2), pady=(2, 2), sticky='ew')
                        b3_name = ttk.Button(
                            frame, text=T("Package"), command=lambda z=project_path: self.packageApp(z)
                        )
                        b3_name.grid(column=3, row=row, padx=(2, 2), pady=(2, 2), sticky='ew')
                        if os.path.basename(project_path) in self.Root.ApplicationsTornado:
                            b4_name = ttk.Button(
                                frame, text=T("Running..."), command=lambda z=project_path: self.runApp(z)
                            )
                            b4_name.grid(column=4, row=row, padx=(2, 2), pady=(2, 2), sticky='ew')
                            b4_name.configure(style='Wg.TButton')
                        else:
                            b4_name = ttk.Button(
                                frame, text=T("Stoped"), command=lambda z=project_path: self.runApp(z)
                            )
                            b4_name.grid(column=4, row=row, padx=(2, 2), pady=(2, 2), sticky='ew')
                            has_compile = os.listdir(cfg_app['APP']['compiled_app_folder'])
                            if len(has_compile):
                                b4_name.configure(style='Wf.TButton', state='normal')
                            else:
                                b4_name.configure(style='Wd.TButton', state=DISABLED, text=T("Need to compile"))
                        b4_name.update()

                        self.buttons_dict[project_path] = [b0_name, b1_name, b2_name, b3_name, b4_name]
                        row += 1
                        config(os.path.join(self.CONFIG["applications_folder"], i, "config.json"), cfg_app)
                    else:
                        row += 1
                        hr_project = ttk.Separator(frame, orient=HORIZONTAL)
                        hr_project.grid(column=0, row=row, columnspan=6, padx=(20, 10), pady=(20, 0), sticky='ew')
                        row += 1
                        ac = ttk.Button(frame, text="Add new application", command=self.setPPwaFile)
                        ac.grid(column=0, columnspan=6, row=row, padx=(30, 20), pady=(2, 30), sticky="ew")
                else:
                    row += 1
                    ac = ttk.Button(frame, text="Add your first application", command=self.setPPwaFile)
                    ac.grid(column=0, columnspan=6, row=row, padx=20, pady=(20, 30), sticky="ew")
            else:
                row += 1
                ac = ttk.Button(frame, text="Add your first application", command=self.setPPwaFile)
                ac.grid(column=0, columnspan=6, row=row, padx=0, pady=(5, 5), sticky="ew")

        self.frame_canvas.create_window((0, 0), window=frame, anchor='nw')
        self.frame_canvas.bind('<Configure>', self.onConfigure)

        self.openGeometry()
        if "MainPWA_state" in self.CONFIG:
            if self.CONFIG["MainPWA_state"] == "zoomed":
                self.master.state("zoomed")
            else:
                self.master.deiconify()
        else:
            self.master.deiconify()
        self.master.attributes('-topmost', True)
        self.master.update()
        self.master.attributes('-topmost', False)

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
                self.Root.ApplicationsTornado[name_dir].master.destroy()
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
                    compiler(projectPath)
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
                    compiler(projectPath)
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
                self.Root.ApplicationsTornado[name_dir].master.destroy()
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
            target = filedialog.askdirectory(initialdir=os.path.dirname(appConfig['PATH']['project']))
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
                self.Root.ApplicationsTornado[name_dir].master.destroy()
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
            self.Root.ApplicationsTornado[name_dir].master.destroy()
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
            self.current_app = tk.Toplevel(self.master)
            self.app = RunAPP(self.current_app, projectPath)
            self.Root.ApplicationsTornado[name_dir] = self.app
            time.sleep(2)
            button_4.configure(state="normal")
            button_4.configure(text=T("Running..."))
            button_4.configure(style='Wg.TButton')

    def setEntryFolder(self, entry):
        folder = filedialog.askdirectory()
        if folder:
            entry.delete(0, END)
            entry.insert(0, os.path.normpath(folder))

    def setPPwaFile(self):
        file = filedialog.askopenfile(filetypes=[('PhanterPWA', '.ppwa')])
        if file:
            project_name = os.path.basename(str(file.name))[:-5]
            if project_name.isidentifier():
                with ZipFile(file.name, "r") as zipf:
                    folder = self.CONFIG["applications_folder"]
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
                self.master.destroy()
                self.Root.openMainPWA()

    def close(self):
        if self.Root:
            self.saveSize()
            for server_running in self.Root.ApplicationsTornado:
                try:
                    self.Root.ApplicationsTornado[server_running].stop()
                    self.Root.ApplicationsTornado[server_running].master.destroy()
                except Exception:
                    print("Try Close")
            self.Root.onClosing()

    def changeAppFolder(self):
        if self.Root:
            self.saveSize()
            self.master.destroy()
            self.Root.master.deiconify()

    def onConfigure(self, event):
        height = self.frame_canvas.bbox('all')[3]
        width = self.frame_canvas.bbox('all')[2]
        self.frame_canvas.configure(
            height=height,
            width=width,
            scrollregion=self.frame_canvas.bbox('all')
        )

    def openAppWin(self, project_path, parent):
        # self.master.withdraw()
        self.newWindow = tk.Toplevel(self.master)
        self.AppsPWA = AppsPWA(self.newWindow, project_path, parent)

    def openGeometry(self, event=None):
        if "MainPWA" in self.CONFIG:
            self.master.geometry(self.CONFIG["MainPWA"])

    def saveSize(self, event=None):
        self.CONFIG = config(
            CURRENT_DIR, {
                "MainPWA": self.master.geometry(),
                "MainPWA_state": self.master.state()
            }
        )

    def update(self):
        self.master.destroy()
        self.Root.openMainPWA()


class AppsPWA:
    def __init__(self, master, project_path, MainPWA):
        self.CONFIG = config(CURRENT_DIR)
        self.AppCONFIG = config(project_path)
        self.project_path_name = os.path.basename(project_path)
        self.project_path = project_path
        self.MainPWA = MainPWA
        self.Root = MainPWA.Root
        self.master = master
        self.master.withdraw()
        self.maxheight = 400
        scrollbar = Scrollbar(master, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self.frame_canvas = tk.Canvas(
            master,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.frame_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.frame_canvas.yview)
        self.frame_canvas.pack(side=LEFT, fill=Y, expand=TRUE)
        master.protocol('WM_DELETE_WINDOW', lambda: self.close())
        master.title("{0} - PhanterPWA".format(self.project_path_name))
        master.iconbitmap(os.path.join(CURRENT_DIR, "grafics", "icon.ico"))
        style_orange = ttk.Style()
        style_orange.configure('Wf.TButton', font=('default', 10, 'bold'), foreground='orange')
        style_green = ttk.Style()
        style_green.configure('Wg.TButton', font=('default', 10, 'bold'), foreground='green')
        frame = tk.Frame(self.frame_canvas)

        row = 0
        aLabel = ttk.Label(frame, text=T("Configuration"), font='default 14 bold')
        aLabel.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 5))
        row += 1
        label_enviroment = ttk.Label(frame, text=T("Enviroment"))
        label_enviroment.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 0), sticky="w")

        row += 1
        hr_enviroment = ttk.Separator(frame, orient=HORIZONTAL)
        hr_enviroment.grid(column=0, row=row, columnspan=4, sticky='ew')

        row += 1
        enviroment_path_label = ttk.Label(frame, text=T("Path"))
        enviroment_path_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        enviroment_path_data = self.AppCONFIG['ENVIRONMENT']['path']
        self.enviroment_path_input = ttk.Entry(frame, width=70)
        self.enviroment_path_input.insert(0, enviroment_path_data)
        self.enviroment_path_input.config(state="readonly")
        self.enviroment_path_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Change"), command=lambda: self.setEntryFolder("Enviroment_path"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        enviroment_python_label = ttk.Label(frame, text=T("Python"))
        enviroment_python_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        enviroment_python_data = self.AppCONFIG['ENVIRONMENT']['python']
        self.enviroment_python_input = ttk.Entry(frame, width=70)
        self.enviroment_python_input.insert(0, enviroment_python_data)
        self.enviroment_python_input.config(state="readonly")
        self.enviroment_python_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Change"), command=lambda: self.setEntryFile("Enviroment_python"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        label_project = ttk.Label(frame, text=T("Project"))
        label_project.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 0), sticky="w")

        row += 1
        hr_project = ttk.Separator(frame, orient=HORIZONTAL)
        hr_project.grid(column=0, row=row, columnspan=4, sticky='ew')

        row += 1
        project_name_label = ttk.Label(frame, text=T("Identifier Name"))
        project_name_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        project_name = self.AppCONFIG['PROJECT']['name']
        self.project_name_input = ttk.Entry(frame, width=70)
        self.project_name_input.insert(0, project_name)
        self.project_name_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Name"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        project_title_label = ttk.Label(frame, text=T("Title"))
        project_title_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        project_title = self.AppCONFIG['PROJECT']['title']
        self.project_title_input = ttk.Entry(frame, width=70)
        self.project_title_input.insert(0, project_title)
        self.project_title_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Title"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        project_version_label = ttk.Label(frame, text=T("Version"))
        project_version_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        project_version = self.AppCONFIG['PROJECT']['version']
        self.project_version_input = ttk.Entry(frame, width=70)
        self.project_version_input.insert(0, project_version)
        self.project_version_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Version"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        project_author_label = ttk.Label(frame, text=T("Author"))
        project_author_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        project_author = self.AppCONFIG['PROJECT']['author']
        self.project_author_input = ttk.Entry(frame, width=70)
        self.project_author_input.insert(0, project_author)
        self.project_author_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Author"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        project_path_label = ttk.Label(frame, text=T("Path"))
        project_path_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        project_path_data = self.AppCONFIG['PATH']['project']
        self.project_path_input = ttk.Entry(frame, width=70)
        self.project_path_input.insert(0, project_path_data)
        self.project_path_input.config(state="readonly")
        self.project_path_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Change"), command=lambda: self.setEntryFolder("Project_path"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        label_email = ttk.Label(frame, text=T("Email"))
        label_email.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 0), sticky="w")

        row += 1
        hr_email = ttk.Separator(frame, orient=HORIZONTAL)
        hr_email.grid(column=0, row=row, columnspan=4, sticky='ew')

        row += 1
        email_server_label = ttk.Label(frame, text=T("Server"))
        email_server_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        email_server = self.AppCONFIG['EMAIL']['server']
        self.email_server_input = ttk.Entry(frame, width=70)
        self.email_server_input.insert(0, email_server)
        self.email_server_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Email_server"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        email_username_label = ttk.Label(frame, text=T("Username"))
        email_username_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        email_username = self.AppCONFIG['EMAIL']['username']
        self.email_username_input = ttk.Entry(frame, width=70)
        self.email_username_input.insert(0, email_username)
        self.email_username_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Email_username"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        email_password_label = ttk.Label(frame, text=T("Password"))
        email_password_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        email_password = self.AppCONFIG['EMAIL']['password']
        self.email_password_input = ttk.Entry(frame, width=70)
        self.email_password_input.insert(0, email_password)
        self.email_password_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Email_password"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        email_port_label = ttk.Label(frame, text=T("Port"))
        email_port_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        email_port = self.AppCONFIG['EMAIL']['port']
        self.email_port_input = ttk.Entry(frame, width=70)
        self.email_port_input.insert(0, email_port)
        self.email_port_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Email_port"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

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

        row += 1
        label_transcrypt = ttk.Label(frame, text=T("Transcrypt"))
        label_transcrypt.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 0), sticky="w")

        row += 1
        hr_transcrypt = ttk.Separator(frame, orient=HORIZONTAL)
        hr_transcrypt.grid(column=0, row=row, columnspan=4, sticky='ew')

        row += 1
        transcrypt_main_file_data = self.AppCONFIG['TRANSCRYPT']['main_files']
        if isinstance(transcrypt_main_file_data, list):
            for p in transcrypt_main_file_data:
                transcrypt_main_file_label = ttk.Label(frame, text=T("Main file"))
                transcrypt_main_file_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
                transcrypt_main_file_input = ttk.Entry(frame, width=70)
                transcrypt_main_file_input.insert(0, p)
                transcrypt_main_file_input.config(state="readonly")
                transcrypt_main_file_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
                button = ttk.Button(
                    frame, text=T("Delete"), command=lambda p=p: self.delTranscript(p)
                )
                button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")
                row += 1
        else:
            transcrypt_main_file_label = ttk.Label(frame, text=T("Main file"))
            transcrypt_main_file_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
            transcrypt_main_file_input = ttk.Entry(frame, width=70)
            transcrypt_main_file_input.insert(0, p)
            transcrypt_main_file_input.config(state="readonly")
            transcrypt_main_file_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
            button = ttk.Button(
                frame, text=T("Delete"), command=lambda p=transcrypt_main_file_data: self.delTranscript(p)
            )
            button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        button = ttk.Button(
            frame,
            text=T("Add new transcrypt mains file"),
            command=lambda p=transcrypt_main_file_data: self.addTranscript(p)
        )
        button.grid(column=1, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        label_API = ttk.Label(frame, text=T("API"))
        label_API.grid(column=0, row=row, columnspan=4, padx=10, pady=(10, 0), sticky="w")

        row += 1
        hr_API = ttk.Separator(frame, orient=HORIZONTAL)
        hr_API.grid(column=0, row=row, columnspan=4, sticky='ew')

        row += 1
        API_key_label = ttk.Label(frame, text=T("Secret Key"))
        API_key_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        API_key = self.AppCONFIG['API']['secret_key']
        self.API_key_input = ttk.Entry(frame, width=70)
        self.API_key_input.insert(0, API_key)
        self.API_key_input.config(state="readonly")
        self.API_key_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(frame, text=T("Generate"), command=self.generateSecret)
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        API_key_token_label = ttk.Label(frame, text=T("Token time"))
        API_key_token_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        API_key_token = self.AppCONFIG['API']['default_time_token_expires']
        self.API_key_token_input = ttk.Entry(frame, width=70)
        self.API_key_token_input.insert(
            0,
            "{0} ({1} seconds)".format(humanize_seconds(API_key_token, Trans), API_key_token)
        )
        self.API_key_token_input.config(state="readonly")
        self.API_key_token_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(
            frame,
            text=T("Change"),
            command=lambda z='default_time_token_expires',
                y=API_key_token,
                x=self.API_key_token_input: self.getSeconds(
                    x,
                    y,
                    z
            )
        )
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        API_key_csrf_label = ttk.Label(frame, text=T("CSRF token time"))
        API_key_csrf_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        API_key_csrf = self.AppCONFIG['API']['default_time_csrf_token_expires']
        self.API_key_csrf_input = ttk.Entry(frame, width=70)
        self.API_key_csrf_input.insert(
            0,
            "{0} ({1} seconds)".format(humanize_seconds(API_key_csrf, Trans), API_key_csrf)
        )
        self.API_key_csrf_input.config(state="readonly")
        self.API_key_csrf_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(
            frame,
            text=T("Change"),
            command=lambda z='default_time_csrf_token_expires',
                y=API_key_csrf,
                x=self.API_key_csrf_input: self.getSeconds(
                    x,
                    y,
                    z
            )
        )
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        API_key_passsword_label = ttk.Label(frame, text=T("Temporary password time"))
        API_key_passsword_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        API_key_passsword = self.AppCONFIG['API']['default_time_temporary_password_expires']
        self.API_key_passsword_input = ttk.Entry(frame, width=70)
        self.API_key_passsword_input.insert(
            0,
            "{0} ({1} seconds)".format(humanize_seconds(API_key_passsword, Trans), API_key_passsword)
        )
        self.API_key_passsword_input.config(state="readonly")
        self.API_key_passsword_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(
            frame,
            text=T("Change"),
            command=lambda z='default_time_temporary_password_expires',
                y=API_key_passsword,
                x=self.API_key_passsword_input: self.getSeconds(
                    x,
                    y,
                    z
            )
        )
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        API_key_attempt_login_label = ttk.Label(frame, text=T("Attempt to login time"))
        API_key_attempt_login_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        API_key_attempt_login = self.AppCONFIG['API']['default_time_next_attempt_to_login']
        self.API_key_attempt_login_input = ttk.Entry(frame, width=70)
        self.API_key_attempt_login_input.insert(
            0,
            "{0} ({1} seconds)".format(humanize_seconds(API_key_attempt_login, Trans), API_key_attempt_login)
        )
        self.API_key_attempt_login_input.config(state="readonly")
        self.API_key_attempt_login_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(
            frame,
            text=T("Change"),
            command=lambda z='default_time_next_attempt_to_login',
                y=API_key_attempt_login,
                x=self.API_key_attempt_login_input: self.getSeconds(
                    x,
                    y,
                    z
            )
        )
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")
        row += 1

        API_key_client_token_label = ttk.Label(frame, text=T("Client Token time"))
        API_key_client_token_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        API_key_client_token = self.AppCONFIG['API']['default_time_client_token_expires']
        self.API_key_client_token_input = ttk.Entry(frame, width=70)
        self.API_key_client_token_input.insert(
            0,
            "{0} ({1} seconds)".format(humanize_seconds(API_key_client_token, Trans), API_key_client_token)
        )
        self.API_key_client_token_input.config(state="readonly")
        self.API_key_client_token_input.grid(column=1, row=row, columnspan=2, padx=(5, 10), pady=(5, 5))
        button = ttk.Button(
            frame,
            text=T("Change"),
            command=lambda z='default_time_client_token_expires',
                y=API_key_client_token,
                x=self.API_key_client_token_input: self.getSeconds(
                    x,
                    y,
                    z
            )
        )
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        label_config_action = ttk.Label(frame, text=T("APP"))
        label_config_action.grid(column=0, row=row, columnspan=3, padx=10, pady=(10, 0), sticky="w")

        row += 1
        hr_config_action = ttk.Separator(frame, orient=HORIZONTAL)
        hr_config_action.grid(column=0, row=row, columnspan=3, sticky='ew')

        row += 1
        api_server_address = ttk.Label(frame, text=T("API Access by"))
        api_server_address.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        server_adress = self.AppCONFIG['CONFIGJS']['api_server_address']
        self.api_server_address = ttk.Entry(frame, width=50)
        self.api_server_address.insert(0, server_adress)
        self.api_server_address.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        api_server_address_help = ttk.Label(frame, text="http://localhost:5000")
        api_server_address_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("API_access_by"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        label_config_action = ttk.Label(frame, text=T("Tornado Server"))
        label_config_action.grid(column=0, row=row, columnspan=3, padx=10, pady=(10, 0), sticky="w")

        row += 1
        hr_config_action = ttk.Separator(frame, orient=HORIZONTAL)
        hr_config_action.grid(column=0, row=row, columnspan=3, sticky='ew')

        row += 1
        api_server_host_label = ttk.Label(frame, text=T("Api server host"))
        api_server_host_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        api_server_host = self.AppCONFIG['API_SERVER']['host']
        self.api_server_host_input = ttk.Entry(frame, width=50)
        self.api_server_host_input.insert(0, api_server_host)
        self.api_server_host_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        api_server_host_help = ttk.Label(frame, text="Default(127.0.0.1)")
        api_server_host_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Api_server_host"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        api_server_port_label = ttk.Label(frame, text=T("Api server port"))
        api_server_port_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        api_server_port = self.AppCONFIG['API_SERVER']['port']
        self.api_server_port_input = ttk.Entry(frame, width=50)
        self.api_server_port_input.insert(0, api_server_port)
        self.api_server_port_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        api_server_port_help = ttk.Label(frame, text="Default(5000)")
        api_server_port_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("Api_server_port"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        api_server_port_label = ttk.Label(frame, text=T("Results"))
        api_server_port_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        api_server_port_label = ttk.Label(
            frame,
            text="http://{0}:{1}/".format(self.api_server_host_input.get(), self.api_server_port_input.get()),
            width=50
        )
        api_server_port_label.grid(column=1, row=row, padx=(10, 5), pady=(5, 10))

        row += 1
        app_server_host_label = ttk.Label(frame, text=T("App server host"))
        app_server_host_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        app_server_host = self.AppCONFIG['APP_SERVER']['host']
        self.app_server_host_input = ttk.Entry(frame, width=50)
        self.app_server_host_input.insert(0, app_server_host)
        self.app_server_host_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        app_server_host_help = ttk.Label(frame, text="Default(127.0.0.1)")
        app_server_host_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("App_server_host"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        app_server_port_label = ttk.Label(frame, text=T("App server port"))
        app_server_port_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        app_server_port = self.AppCONFIG['APP_SERVER']['port']
        self.app_server_port_input = ttk.Entry(frame, width=50)
        self.app_server_port_input.insert(0, app_server_port)
        self.app_server_port_input.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        app_server_port_help = ttk.Label(frame, text="Default(5500)")
        app_server_port_help.grid(column=2, row=row, padx=(10, 5), pady=(5, 5), sticky="w")
        button = ttk.Button(frame, text=T("Save"), command=lambda: self.validAndSave("App_server_port"))
        button.grid(column=3, row=row, padx=10, pady=(5, 5), sticky="w")

        row += 1
        self.var_debug = IntVar()
        if self.AppCONFIG['PROJECT']['debug'] is True or self.AppCONFIG['PROJECT']['debug'] == "true":
            self.var_debug.set(1)
            is_debug = ttk.Checkbutton(frame, text=T("Debug"), variable=self.var_debug, command=self.setDebug)
        else:
            self.var_debug.set(0)
            is_debug = ttk.Checkbutton(frame, text=T("Debug"), variable=self.var_debug, command=self.setDebug)
        is_debug.grid(column=0, row=row, columnspan=4, padx=(10, 5), pady=(5, 5))

        row += 1

        self.button_compile = ttk.Button(frame, text=T("Compile"), command=self.compileApp)
        self.button_compile.grid(column=0, row=row, columnspan=2, padx=(10, 10), pady=(5, 50))
        if os.path.basename(self.project_path) in self.Root.ApplicationsTornado:
            self.button_start = ttk.Button(frame, text=T("Running..."), command=self.runApp)
            self.button_start.grid(column=2, row=row, columnspan=1, padx=(10, 10), pady=(5, 50))
            self.button_start.configure(style='Wg.TButton')
        else:
            self.button_start = ttk.Button(frame, text=T("Stoped"), command=self.runApp)
            self.button_start.grid(column=2, row=row, columnspan=1, padx=(10, 10), pady=(5, 50))
            self.button_start.configure(style='Wf.TButton')
        self.button_start.update()
        self.frame_canvas.create_window((0, 0), window=frame, anchor='nw')

        self.frame_canvas.bind('<Configure>', self.onConfigure)
        self.openGeometry()
        if "AppsPWA_state" in self.CONFIG:
            if self.CONFIG["AppsPWA_state"] == "zoomed":
                self.master.state("zoomed")
            else:
                self.master.deiconify()
        else:
            self.master.deiconify()
        self.master.attributes('-topmost', True)
        self.master.update()
        self.master.attributes('-topmost', False)

    def compileApp(self, ):
        projectPath = self.project_path
        choice = messagebox.askquestion(
            T("Are you sure?"),
            T("".join(["Do you really want to compile the app?"])),
            icon='warning'
        )
        if choice == "yes":
            name_dir = os.path.basename(projectPath)
            b1 = self.button_compile
            b2 = self.button_start
            if name_dir in self.Root.ApplicationsTornado:
                b2.configure(text=T("Stoping..."))
                b2.update()
                b2.configure(state=DISABLED)
                b1.configure(text=T("Waiting..."))
                b1.update()
                b1.configure(state=DISABLED)
                b2.update()
                time.sleep(1)
                self.Root.ApplicationsTornado[name_dir].stop()
                self.Root.ApplicationsTornado[name_dir].master.destroy()
                time.sleep(1)
                del self.Root.ApplicationsTornado[name_dir]
                b1.configure(state="normal")
                b2.configure(state="normal")
                b1.configure(text=T("Compiling..."))
                b2.configure(text=T("Waiting..."))
                b1.configure(state=DISABLED)
                b2.configure(state=DISABLED)
                b1.update()
                b2.update()
                time.sleep(1)
                try:
                    compiler(projectPath)
                except Exception as e:
                    logger_app = logging.getLogger(name_dir)
                    logger_app.error("Problem on packing", exc_info=True)
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
                    b2.configure(state="normal")
                    b2.configure(text=T("Stoped"))
                    b2.configure(style='Wf.TButton')
                    b2.update()
                    b1.configure(state="normal")
                    b1.configure(text=T("Compile"))
                    b1.update()
            else:
                b2.configure(state=DISABLED)
                b2.update()
                b1.configure(text=T("Compiling..."))
                b1.update()
                b1.configure(state=DISABLED)
                time.sleep(1)
                try:
                    compiler(projectPath)
                except Exception as e:
                    logger_app = logging.getLogger(name_dir)
                    logger_app.error("Problem on packing", exc_info=True)
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
                    b1.configure(state="normal")
                    b1.configure(text=T("Compile"))
                    b1.update()
                    b2.configure(state="normal")
                    b2.update()

    def getSeconds(self, Entry, seconds, key_api):
        self.secondsWindow = tk.Toplevel(self.master)
        self.TimeCombox = TimeCombox(self.secondsWindow, seconds, Entry, self, key_api)

    def runApp(self):
        name_dir = self.project_path_name
        b = self.button_start

        if name_dir in self.Root.ApplicationsTornado:
            b.configure(text=T("Stoping..."))
            b.update()
            b.configure(state=DISABLED)
            b.update()
            time.sleep(1)
            self.Root.ApplicationsTornado[name_dir].stop()
            self.Root.ApplicationsTornado[name_dir].master.destroy()
            time.sleep(1)
            del self.Root.ApplicationsTornado[name_dir]
            b.configure(state="normal")
            b.configure(text=T("Run"))
        else:
            b.configure(text=T("Starting..."))
            b.update()
            b.configure(state=DISABLED)
            b.update()
            time.sleep(1)
            self.current_app = tk.Toplevel(self.master)
            self.app = RunAPP(self.current_app, self.project_path)
            self.Root.ApplicationsTornado[name_dir] = self.app
            time.sleep(2)
            b.configure(state="normal")
            b.configure(text=T("Stop"))

    def setEmail(self, value):
        if value == "SSL":
            v = self.var_ssl.get()
            if v:
                self.AppCONFIG['EMAIL']['use_ssl'] = True
            else:
                self.AppCONFIG['EMAIL']['use_ssl'] = False
        elif value == "TLS":
            v = self.var_tls.get()
            if v:
                self.AppCONFIG['EMAIL']['use_tls'] = True
            else:
                self.AppCONFIG['EMAIL']['use_tls'] = False
        self.updateAppCONFIG()

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
        elif entry == "API_access_by":
            v = self.api_server_address.get()
            self.AppCONFIG['CONFIGJS']['api_server_address'] = v
            self.updateAppCONFIG()
        elif entry == "Api_server_host":
            v = self.api_server_host_input.get()
            self.AppCONFIG['API_SERVER']['host'] = v
            self.updateAppCONFIG()
        elif entry == "Api_server_port":
            v = self.api_server_port_input.get()
            self.AppCONFIG['API_SERVER']['port'] = v
            self.updateAppCONFIG()
        elif entry == "App_server_host":
            v = self.app_server_host_input.get()
            self.AppCONFIG['APP_SERVER']['host'] = v
            self.updateAppCONFIG()
        elif entry == "App_server_port":
            v = self.app_server_port_input.get()
            self.AppCONFIG['APP_SERVER']['port'] = v
            self.updateAppCONFIG()

    def setDebug(self):
        v = self.var_debug.get()
        if v:
            self.AppCONFIG['PROJECT']['debug'] = True
        else:
            self.AppCONFIG['PROJECT']['debug'] = False
        self.updateAppCONFIG()

    def updateAppCONFIG(self):
        self.AppCONFIG = config(os.path.join(self.AppCONFIG["PATH"]["project"], "config.json"), self.AppCONFIG)

    def generateSecret(self):
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
            current_path = self.AppCONFIG["PATH"]["project"]
            folder = filedialog.askdirectory(initialdir=current_path)
            if folder:
                self.AppCONFIG["PATH"]["project"] = os.path.normpath(folder)
                self.AppCONFIG["PATH"]["api"] = os.path.normpath(os.path.join(folder, "api"))
                self.AppCONFIG["PATH"]["app"] = os.path.normpath(os.path.join(folder, "app"))
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
        self.master.destroy()
        self.MainPWA.saveSize()
        self.MainPWA.Root.openMainPWA()
        self.MainPWA.master.destroy()

    def onConfigure(self, event):
        height = self.frame_canvas.bbox('all')[3]
        width = self.frame_canvas.bbox('all')[2]
        self.frame_canvas.configure(
            height=height,
            width=width,
            scrollregion=self.frame_canvas.bbox('all')
        )

    def openGeometry(self, event=None):
        if "AppsPWA" in self.CONFIG:
            self.master.geometry(self.CONFIG["AppsPWA"])

    def saveSize(self, event=None):
        self.CONFIG = config(
            CURRENT_DIR, {
                "AppsPWA": self.master.geometry(),
                "AppsPWA_state": self.master.state()
            }
        )


class TimeCombox:
    def __init__(self, tkinterInstance, seconds, Entry, AppsPWA, key_api=None):
        self.splits_seconds = splits_seconds(seconds)
        self.entry_seconds = Entry
        self.initial_value = seconds
        self.master = tkinterInstance
        self.master.withdraw()
        self.AppsPWA = AppsPWA
        self.key_api = key_api
        scrollbar = Scrollbar(self.master, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self.frame_canvas = tk.Canvas(
            self.master,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.frame_canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.frame_canvas.yview)
        self.frame_canvas.pack(side=LEFT, fill=Y, expand=TRUE)

        self.master.title(T("Application Folder - PhanterPWA"))
        self.master.iconbitmap(os.path.join(CURRENT_DIR, "grafics", "icon.ico"))

        frame = tk.Frame(self.frame_canvas)

        row = 0
        aLabel = ttk.Label(frame, text=T("Seconds Converter"), font='default 14 bold')
        aLabel.grid(column=0, row=row, columnspan=6, padx=10, pady=(10, 5))

        row += 1
        year_label = ttk.Label(frame, text=T("Year(s)"))
        year_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        year_values = [0, 1, 2, 3, 4]
        self.yearCombox = ttk.Combobox(frame, width=10, values=year_values)
        self.yearCombox.current(year_values.index(self.splits_seconds['year'] if 'year' in self.splits_seconds else 0))
        self.yearCombox.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        self.yearCombox.bind("<<ComboboxSelected>>", self.comboxChange)


        month_label = ttk.Label(frame, text=T("Month(s)"))
        month_label.grid(column=2, row=row, padx=(10, 5), pady=(5, 5))
        month_values = [f for f in range(0, 12)]
        self.monthCombox = ttk.Combobox(frame, width=10, values=month_values)
        self.monthCombox.current(month_values.index(self.splits_seconds['month'] if 'month' in self.splits_seconds else 0))
        self.monthCombox.grid(column=3, row=row, padx=(5, 10), pady=(5, 5))
        self.monthCombox.bind("<<ComboboxSelected>>", self.comboxChange)


        day_label = ttk.Label(frame, text=T("Day(s)"))
        day_label.grid(column=4, row=row, padx=(10, 5), pady=(5, 5))
        day_values = [f for f in range(0, 30)]
        self.dayCombox = ttk.Combobox(frame, width=10, values=day_values)
        self.dayCombox.current(day_values.index(self.splits_seconds['day'] if 'day' in self.splits_seconds else 0))
        self.dayCombox.grid(column=5, row=row, padx=(5, 10), pady=(5, 5))
        self.dayCombox.bind("<<ComboboxSelected>>", self.comboxChange)

        row += 1
        hour_label = ttk.Label(frame, text=T("Hour(s)"))
        hour_label.grid(column=0, row=row, padx=(10, 5), pady=(5, 5))
        hour_values = [f for f in range(0, 24)]
        self.hourCombox = ttk.Combobox(frame, width=10, values=hour_values)
        self.hourCombox.current(hour_values.index(self.splits_seconds['hour'] if 'hour' in self.splits_seconds else 0))
        self.hourCombox.grid(column=1, row=row, padx=(5, 10), pady=(5, 5))
        self.hourCombox.bind("<<ComboboxSelected>>", self.comboxChange)

        minute_label = ttk.Label(frame, text=T("Minute(s)"))
        minute_label.grid(column=2, row=row, padx=(10, 5), pady=(5, 5))
        minute_values = [f for f in range(0, 60)]
        self.minuteCombox = ttk.Combobox(frame, width=10, values=minute_values)
        self.minuteCombox.current(minute_values.index(self.splits_seconds['minute'] if 'minute' in self.splits_seconds else 0))
        self.minuteCombox.grid(column=3, row=row, padx=(5, 10), pady=(5, 5))
        self.minuteCombox.bind("<<ComboboxSelected>>", self.comboxChange)


        second_label = ttk.Label(frame, text=T("Second(s)"))
        second_label.grid(column=4, row=row, padx=(10, 5), pady=(5, 5))
        second_values = [f for f in range(0, 60)]
        self.secondCombox = ttk.Combobox(frame, width=10, values=second_values)
        self.secondCombox.current(second_values.index(self.splits_seconds['second'] if 'second' in self.splits_seconds else 0))
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
        self.master.resizable(0, 0)
        self.master.deiconify()

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
        self.master.destroy()


class RunAPP:
    def __init__(self, master, projectPath):
        self.master = master
        self.master.withdraw()
        self.projectPath = projectPath
        self.AppCONFIG = config(projectPath)

        self.run()

        webbrowser.open_new("http://127.0.0.1:{0}".format(self.AppCONFIG["APP_SERVER"]["port"]))

    def run(self):
        self.target = os.path.abspath(os.path.join("..", "server.py"))
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
