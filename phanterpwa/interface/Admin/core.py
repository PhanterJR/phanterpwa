import os
import sys
import logging
from phanterpwa.configer import ProjectConfig
from phanterpwa.i18n import Translator
_current_dir = os.path.dirname(__file__)
projectConfig = ProjectConfig(os.path.join(_current_dir, "config.json"))
_debug = projectConfig['PROJECT']['debug']
_project_name = projectConfig['PROJECT']['name']
for app in projectConfig["FRONTEND"].keys():
    Translator_apps = Translator(os.path.join(_current_dir, "frontend", app, "languages"), identifier="{0}-{1}".format(
        _project_name, app), debug=_debug)
    Translator_apps.add_language("pt-BR")
Translator_email = Translator(os.path.join(_current_dir, "api", "languages", "email"), identifier="{0}-email".format(
    _project_name), debug=_debug)
Translator_email.add_language("pt-BR")
Translator_captcha = Translator(os.path.join(_current_dir, "api", "languages", "captcha"), identifier="{0}-captcha".format(
    _project_name), debug=_debug)
Translator_captcha.add_language("pt-BR")
Translator_api = Translator(os.path.join(_current_dir, "api", "languages"), identifier="{0}-api".format(
    _project_name), debug=_debug)
Translator_api.add_language("pt-BR")
formatter = logging.Formatter(
    '%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

formatter_out_app = logging.Formatter(
    '%(asctime)s - %(name)s.app -  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
fh_app = logging.FileHandler(os.path.join(_current_dir, 'logs', 'app.log'))
fh_app.setLevel(logging.ERROR)
fh_app.setFormatter(formatter)
fh_app_warnings = logging.FileHandler(os.path.join(_current_dir, 'logs', 'app.log'))
fh_app_warnings.setLevel(logging.WARNING)
fh_app_warnings.setFormatter(formatter)

sh_app_info = logging.StreamHandler(sys.stdout)
sh_app_info.setLevel(logging.INFO)
sh_app_info.setFormatter(formatter_out_app)

logger_app = logging.getLogger("{0}".format(os.path.basename(_current_dir)))
logger_app.addHandler(fh_app)
logger_app.addHandler(fh_app_warnings)
logger_app.addHandler(sh_app_info)


formatter_out_api = logging.Formatter(
    '%(asctime)s - %(name)s -  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
fh_api = logging.FileHandler(os.path.join(_current_dir, 'logs', 'api.log'))
fh_api.setLevel(logging.ERROR)
fh_api.setFormatter(formatter)
fh_api_warnings = logging.FileHandler(os.path.join(_current_dir, 'logs', 'api.log'))
fh_api_warnings.setLevel(logging.WARNING)
fh_api_warnings.setFormatter(formatter)

sh_api_info = logging.StreamHandler(sys.stdout)
sh_api_info.setLevel(logging.INFO)
sh_api_info.setFormatter(formatter_out_api)

logger_api = logging.getLogger("{0}.api".format(os.path.basename(_current_dir)))
logger_api.addHandler(fh_api)
logger_api.addHandler(fh_api_warnings)
logger_api.addHandler(sh_api_info)
