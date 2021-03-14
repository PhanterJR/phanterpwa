import os
import glob
import json
import sys
import tkinter as tk
import psutil
import appdirs
import tempfile
from tkinter import (
    ttk,
    filedialog,
    END,
    VERTICAL,
    LEFT,
    RIGHT,
    Scrollbar,
    Y,
    DISABLED,
    FALSE,
    TRUE
)
from phanterpwa.tools import (
    config,
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


Trans = Translator(os.path.join(CURRENT_DIR, "langs"), "grafics", debug=True)
T = Trans.T



class ProjectsFolderTk():
    def __init__(self):

        self._projectdata_dir = os.path.join(appdirs.user_data_dir(), "phanterpwa")
        self._projectdata_dir_gui = os.path.join(self._projectdata_dir, "gui")
        if not os.path.isdir(self._projectdata_dir):
            os.makedirs(self._projectdata_dir, exist_ok=True)
        if not os.path.isdir(self._projectdata_dir_gui):
            os.makedirs(self._projectdata_dir_gui, exist_ok=True)
        self._projects_path = None
        self.ProjectsPWA = None
        self.ProjectPWA = None
        self.ConfigAPI = None
        self.ConfigAPP = None
        self.CONFIG = config(self._projectdata_dir_gui)
        app_folder_data = ""
        if "projects_folder" in self.CONFIG:
            if os.path.isdir(self.CONFIG["projects_folder"]):
                self.projects_folder = self.CONFIG["projects_folder"]
                app_folder_data = self.projects_folder
        else:
            self.projects_folder = os.getcwd()
        self.start()

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

        self.tkInstance.deiconify()
        self.tkInstance.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.tkInstance.attributes('-topmost', True)
        self.tkInstance.update()
        self.tkInstance.attributes('-topmost', False)
        self.tkInstance.mainloop()

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
        print(self.CONFIG)
        if self.app_folder_input.get():
            self.CONFIG = config(self._projectdata_dir_gui, {"projects_folder": os.path.normpath(self.projects_folder)})
            self.tkInstance.destroy()
        #     if not self.ProjectsPWA:
        #         tkInstance = tk.Toplevel(self.tkInstance)
        #         self.ProjectsPWA = ProjectsPWA(tkInstance, self)
        #     else:
        #         self.ProjectsPWA.tkInstance.destroy()
        #         tkInstance = tk.Toplevel(self.tkInstance)
        #         self.ProjectsPWA = ProjectsPWA(tkInstance, self)
        pass

    def start(self):
        self.tkInstance = tk.Tk()
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

    def onClosing(self):
        print("Closing")
        self.tkInstance.destroy()


def start():

    ProjectsFolderTk()



if __name__ == '__main__':
    start()
