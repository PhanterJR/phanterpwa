import os
import glob
import importlib
import shutil
import psutil
import time
import sass
import subprocess
import json
from phanterpwa.builds import BuildViews
from core.config import CONFIG
current_folder = os.path.dirname(__file__)


transcrypt_main_file = CONFIG['TRANSCRYPT']['main_file']
project_version = CONFIG['PROJECT']['version']
debug = CONFIG['PROJECT']['debug']
path_www = os.path.join(current_folder, "..", "app", "www")
path_app = os.path.join(current_folder, "..", "app")
python_env = CONFIG['ENVIRONMENT']['python']
app_server_port = CONFIG['APP_SERVER']['port']
app_server_host = CONFIG['APP_SERVER']['host']

if not os.path.exists(python_env):
    raise "The python configured in 'config.ini' " +\
        "for your environment was not found in %s" % python_env

if os.name == 'nt':
    if not os.path.exists("run_app.bat"):
        with open("run_app.bat", "w") as f:
            t = 'mode con: cols=120 lines=50\ncall "%s" "%s"\npause' % (
                python_env,
                os.path.join(current_folder, "run_app.py")
            )
            f.write(t)


def kill_server(forced=False):
    if not forced:
        if os.path.exists("server_app.pid"):
            with open("server_app.pid", "r") as f:
                pid = f.read().strip()
                if pid:
                    for p in psutil.process_iter():
                        if int(p.pid) == int(pid):
                            cmd_line = None
                            try:
                                cmd_line = p.cmd_line()
                            except Exception as e:
                                print(e)
                            if cmd_line:
                                basename = os.path.basename
                                if "python" in basename(cmd_line[0]) and\
                                        "run_app.py" in basename(cmd_line[-1]):
                                    p.terminate()
                                    print("close server. PID: ", pid)
                                    break
                    for c in range(3):
                        print('wait: pass %s second(s)' % (c + 1))
                        time.sleep(1)
                else:
                    print("Previous server not found")
    else:
        for p in psutil.process_iter():
            cmd_line = None
            try:
                cmd_line = p.cmd_line()
            except Exception as e:
                print(e)
            if cmd_line:
                if cmd_line[0] == python_env and cmd_line[-1] == __file__:
                    p.terminate()
                    print("FORCED: close server. PID: ", p.pid)
                    break
        for c in range(3):
            print('wait: pass %s second(s)' % (c + 1))
            time.sleep(1)


kill_server()

monitored_style = {}
monitored_html = {}
if not os.path.exists(os.path.join(path_app, "scripts", transcrypt_main_file)):
    with open(os.path.join(path_app, "scripts", transcrypt_main_file), "w") as f:
        f.write("print(\"Hello World!\")\n")

transcrypt_main_file_path = os.path.join(path_app, "scripts", transcrypt_main_file)

try:
    shutil.rmtree(path_www)
except Exception as e:
    print('Error while deleting directory: %s' % e)


def create_transcrypt_config():
    conf = {}
    permitted_keys = ["PROJECT", "CONFIGJS"]
    conf["PROJECT"] = CONFIG["PROJECT"]
    conf["CONFIGJS"] = CONFIG["CONFIGJS"]
    ini = "\n".join([
        "# created automatically in '%s'" % __file__,
        "# open config.json and get configs from '%s' section(s)" % permitted_keys,
        "\nfrom org.transcrypt.stubs.browser import __pragma__",
        "__pragma__('jsiter')",
        "\n"
    ])
    end = "\n__pragma__('nojsiter')\n"
    with open(os.path.join(path_app, "scripts", "config.py"), 'w', encoding="utf-8") as f:
        content = "".join([ini, "CONFIG = %s" % json.dumps(conf, ensure_ascii=True, indent=2), end])
        content = content.replace('true', 'True').replace('false', 'False').replace('null', 'None')
        f.write(content)


def renew_statics():
    if os.path.exists(os.path.join(path_www, "static")):
        try:
            shutil.rmtree(os.path.join(path_www, "static"))
        except Exception as e:
            print('Error while deleting directory: %s' % e)
    shutil.copytree(
        os.path.join(path_app, "statics"),
        os.path.join(path_www, "static", str(project_version))
    )


def compile_languages():
    if not os.path.exists(os.path.join(path_www, "static", str(project_version), "languages")):
        os.makedirs(
            os.path.join(path_www, "static", str(project_version), "languages"), exist_ok=True
        )
    langs = glob.glob(os.path.join(path_app, "languages", "*.json"))
    for x in langs:
        with open(x, "r", encoding='utf-8') as f:
            c = json.load(f)
            lang_file = os.path.join(path_www, "static", str(project_version), "languages", os.path.basename(x))
            with open(lang_file, "w", encoding='utf-8') as o:
                if debug:
                    json.dump(c, o, ensure_ascii=False, indent=2)
                else:
                    json.dump(c, o, ensure_ascii=False)


def compile_styles():
    list_sass = glob.glob(os.path.join(path_app, "styles", "*"))
    exclude = ["__pycache__", "__init__.py"]
    for s in list_sass:
        os.makedirs(
            os.path.join(
                path_www, "static", str(project_version), "css"), exist_ok=True)
        if os.path.isfile(s) and s[-5:] == ".sass":
            is_to_compile = False
            if s in monitored_style:
                if os.path.getmtime(s) != monitored_style[s]:
                    is_to_compile = True
                    monitored_style[s] = os.path.getmtime(s)
            else:
                is_to_compile = True
                monitored_style[s] = os.path.getmtime(s)
            if is_to_compile:
                print("compiling Sass to Css: %s" % s)
                with open(s, "r") as f:
                    filename = os.path.basename(s)[0:-5]
                    c = ""
                    temp_c = f.readlines()
                    for t in temp_c:
                        if t[0:12] == "$app-version":
                            t = "$app-version: %s\n" % project_version
                        c = "".join([c, t])
                    if debug:
                        humanized = sass.compile(string=c, indented=True, output_style="expanded") + "\n"
                        with open(
                            os.path.join(
                                path_www, "static", str(project_version), "css", "%s.css" % filename), "w") as o:
                            o.write(humanized)
                    else:
                        compressed = sass.compile(string=c, indented=True, output_style="compressed")
                        with open(
                            os.path.join(
                                path_www, "static", str(project_version), "css", "%s.css" % filename), "w") as o:
                            o.write(compressed)
        elif os.path.isdir(s) and s not in exclude:
            n_list_sass = glob.glob(os.path.join(s, "*.sass"))
            filename = os.path.split(s)[-1]
            is_to_compile = False
            for n in n_list_sass:
                if n in monitored_style:
                    if os.path.getmtime(n) != monitored_style[n]:
                        is_to_compile = True
                        monitored_style[n] = os.path.getmtime(n)
                else:
                    is_to_compile = True
                    monitored_style[n] = os.path.getmtime(n)
            if is_to_compile:
                pre_c = ""
                for n in n_list_sass:
                    with open(n, "r") as f:
                        c = ""
                        temp_c = f.readlines()
                        for t in temp_c:
                            if t[0:12] == "$app-version":
                                t = "$app-version: %s\n" % project_version
                            c = "".join([c, t])
                        pre_c = "".join([pre_c, c, "\n"])
                print("compiling Sass to Css: %s" % os.path.join(s, "%s.css" % filename))
                if debug:
                    joined_humanized = sass.compile(string=pre_c, indented=True, output_style="expanded")
                    with open(
                        os.path.join(
                            path_www, "static", str(project_version), "css", "%s.css" % filename), "w") as o:
                        o.write(joined_humanized)
                else:
                    joined_compressed = sass.compile(string=pre_c, indented=True, output_style="compressed")
                    with open(
                        os.path.join(
                            path_www, "static", str(project_version), "css", "%s.css" % filename), "w") as o:
                        o.write(joined_compressed)


def compile_html(file, base="", ignore=["__init__.py"]):
    if os.path.isfile(file) and os.path.basename(file) not in ignore and file[-3:] == ".py":
        is_to_compile = False
        if file in monitored_html:
            if os.path.getmtime(file) != monitored_html[file]:
                is_to_compile = True
                monitored_html[file] = os.path.getmtime(file)
        else:
            is_to_compile = True
            monitored_html[file] = os.path.getmtime(file)
        if is_to_compile:
            print("compiling Python to html: %s" % file)
            i_mod = "%s" % (os.path.basename(file)[0:-3])
            if base:
                i_mod = "%s.%s" % (base, i_mod)
            i = importlib.import_module(i_mod)
            importlib.reload(i)
            name = "".join([*i_mod.split(".")[-1], ".html"])
            files_www = os.path.join(path_www, *i_mod.split(".")[2:-1])
            print(i_mod)
            if debug:
                builder = BuildViews(name, i.html, files_www, True)
            else:
                builder = BuildViews(name, i.html, files_www)
            builder.build()


def compile_htmls(source, base=""):
    # htmls to www
    list_all = glob.glob(os.path.join(source, "*"))
    for x in list_all:
        if os.path.isdir(x) and not os.path.basename(x) == "__pycache__":
            if base:
                new_base = "%s.%s" % (base, os.path.basename(x))
                compile_htmls(x, new_base)
        elif os.path.isfile(x):
            compile_html(x, base=base)


def compile_script(file, python_env, ignore=["__init__.py"]):
    print("compiling Python to Javascript: %s" % file)
    if os.path.basename(file) not in ignore:
        if not os.path.exists(os.path.join(path_www, "static", str(project_version), "js", "transcrypt")):
            os.makedirs(os.path.join(path_www, "static", str(project_version), "js", "transcrypt"), exist_ok=True)
        if debug:
            subprocess.run("%s -m transcrypt %s -n -m" % (python_env, file))
        else:
            subprocess.run("%s -m transcrypt %s -m" % (python_env, file))
        list_all = glob.glob(os.path.join(path_app, "scripts", "__target__", "*"))
        for x in list_all:
            if os.path.isfile(x):
                script_file = os.path.join(
                    path_www, "static", str(project_version), "js", "transcrypt", os.path.basename(x)
                )
                shutil.copy(
                    x,
                    script_file
                )


create_transcrypt_config()
renew_statics()
compile_languages()
compile_styles()
compile_htmls(os.path.join(path_app, "views"), "app.views")
compile_script(transcrypt_main_file_path, python_env)
