# -*- coding: utf-8 -*-
# author: PhanterJR<junior.conex@gmail.com>
# license: MIT
import os
import sys
import psutil
import subprocess
import argparse
import logging
from phanterpwa.tools import config
from phanterpwa.interface.graphic import start
from phanterpwa.interface.cli import start as start_cli
CURRENT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__)))
CWD = os.path.join(CURRENT_DIR, "interface")
CONFIG = config(CWD)
ENV_PYTHON = os.path.normpath(sys.executable)
parser = argparse.ArgumentParser()


def start_server(projectPath):
    target = os.path.normpath(os.path.join(CURRENT_DIR, "server.py"))
    command = " ".join([ENV_PYTHON, target])
    subprocess.run(command, cwd=projectPath, shell=True)


def CLEAR_CONSOLE():
    os.system('cls' if os.name == 'nt' else 'clear')


if not len(sys.argv) > 1:
    def main():
        start()
else:
    parser.add_argument('--cli', '-c', nargs='?', const=True,
                        help='CLI interface')

    parser.add_argument('--run_last_app', '-r', nargs='?', const=True,
                        help='Run server of last running application')

    def main():
        args = parser.parse_args()
        if args.cli:
            start_cli()
        elif args.run_last_app:
            if 'last_application' in CONFIG:
                configApp = config(CONFIG['last_application'])
                projectPath = CONFIG['last_application']
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
                print("API Server running in http://{0}:{1}".format(
                    configApp['API_SERVER']['host'], configApp['API_SERVER']['port']))
                print("APP Server running in http://{0}:{1}".format(
                    configApp['APP_SERVER']['host'], configApp['APP_SERVER']['port']))
                try:
                    print("Press CTRL+C to stop server!")
                    config(CWD, {'last_application': configApp['PATH']['project']})
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
                except Exception:
                    logger.error("Server error", exc_info=True)
                    input("Server error, check the log file to learn more. Press <enter> key to exit.")
                    CLEAR_CONSOLE()
        else:
            print("Try --cli or -c arguments")
        return True
if __name__ == "__main__":
    sys.exit(main())
