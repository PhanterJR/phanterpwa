# -*- coding: utf-8 -*-
# author: PhanterJR<junior.conex@gmail.com>
# license: MIT
import os
import sys
import psutil
import subprocess
import argparse
import traceback

from phanterpwa.tools import (
    config
)
from phanterpwa.compiler import Compiler
#from phanterpwa.interface.graphic import start
try:
    import tkinter as Tk
    from phanterpwa.interface.admin_tk import start
except:
    def start():
        print("The tkinter fails. Your Python may not be configured for Tk")
from phanterpwa.interface.cli import Cli
CURRENT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__)))
CWD = os.path.join(CURRENT_DIR, "interface")
CONFIG = config(CWD)
ENV_PYTHON = os.path.normpath(sys.executable)
parser = argparse.ArgumentParser(description="".join(['Without arguments the phanterpwa GUI will be executed,\n',
    ' if there is an error try to use the CLI version.']))


def start_server(projectPath):
    target = os.path.normpath(os.path.join(CURRENT_DIR, "server.py"))
    command = " ".join([ENV_PYTHON, target])
    subprocess.run(command, cwd=projectPath, shell=True)


def CLEAR_CONSOLE():
    os.system('cls' if os.name == 'nt' else 'clear')


if not len(sys.argv) > 1:
    def main():
        Cli()
else:
    parser.add_argument('-g', '--gui', action="store_true", default=False,
                        help='Grafical interface')

    parser.add_argument('-r', '--compile_and_server_last_project', action="store_true", default=False,
                        help='Compile and server of last running project')

    parser.add_argument('-s', '--server_last_project', action="store_true", default=False,
                        help='Run server of last running project')

    def main():
        args = parser.parse_args()
        if args.gui:
            start()
        elif args.compile_and_server_last_project or args.server_last_project:
            if 'last_application' in CONFIG:
                configProject = config(CONFIG['last_application'])
                projectPath = CONFIG['last_application']

                if args.compile_and_server_last_project:
                    try:
                        Compiler(projectPath).compile()
                    except Exception as e:
                        traceback.print_tb(e.__traceback__)

                print("API Server running in http://{0}:{1}".format(
                    configProject['API_SERVER']['host'], configProject['API_SERVER']['port']))
                print("APP Server running in http://{0}:{1}".format(
                    configProject['APP_SERVER']['host'], configProject['APP_SERVER']['port']))
                try:
                    print("Press CTRL+C to stop server!")
                    config(CWD, {'last_application': configProject['PATH']['project']})
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
                    input("Server Stoped""! Press <enter> key to exit.")
                    CLEAR_CONSOLE()
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    input("Server error, check the log file to learn more. Press <enter> key to exit.")
                    CLEAR_CONSOLE()
        else:
            print("Try --cli or -c arguments")
        return True
if __name__ == "__main__":
    sys.exit(main())
