import os
from phanterpwa.backend.request_handlers import (
    admin,
    auth,
    credentials,
    i18n_server,
    oauth
)
#  Your conttrolers
from .controllers import (
    welcome,
    developer,
)
from phanterpwa.i18n import Translator
from core import (
    projectConfig,
    logger_api
)

from .models import *

_current_dir = os.path.join(os.path.dirname(__file__))
_app_name = os.path.split(_current_dir)[-1]
_debug = projectConfig['PROJECT']['debug']
_project_name = projectConfig['PROJECT']['name']


Translator_captcha = Translator(os.path.join(_current_dir, "languages", "captcha"), identifier="{0}-captcha".format(
    _project_name), debug=_debug)
Translator_captcha.add_language("pt-BR")

Translator_api = Translator(os.path.join(_current_dir, "languages"), identifier="{0}-api".format(
    _project_name), debug=_debug)
Translator_api.add_language("pt-BR")
Translator_email = Translator(os.path.join(_current_dir, "languages", "email"), identifier="{0}-email".format(
    _project_name), debug=_debug)
Translator_email.add_language("pt-BR")

SETTINGS = {
    'debug': _debug
}


HANDLER = [
    (r"/?(api)?/?", welcome.Welcome),
    (r"/api/websocket/?", developer.EchoWebSocket, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/client/?", credentials.SignClient, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/signforms/([0-9a-zA-Z_-]+)/?", credentials.SignForms, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/signcaptchaforms/([0-9a-zA-Z_-]+)/?", credentials.SignCaptchaForms, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        Translator_captcha=Translator_captcha,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/signlockform/?", credentials.SignLockForm, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/resigncredentials/?", credentials.ReSing, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/auth/?", auth.Auth, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        Translator_email=Translator_email,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/auth/two-factor/([0-9a-zA-Z_\-\.]+)/?", auth.TwoFactor, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        Translator_email=Translator_email,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/auth/lock/?", auth.LockUser, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/auth/image/([0-9]+)/?", auth.ImageUser, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/auth/create/?", auth.CreateAccount, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/auth/change/?", auth.ChangeAccount, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        Translator_email=Translator_email,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/auth/change-password/?", auth.ChangePassword, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/auth/request-password/?", auth.RequestAccount, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        Translator_email=Translator_email,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/auth/active-account/?", auth.ActiveAccount, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        Translator_email=Translator_email,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/oauth/prompt/([a-zA-Z_-]+)?/?", oauth.Prompt, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/oauth/redirect/([a-zA-Z_-]+)?/?", oauth.Redirect, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/admin/usermanager/([0-9]+)?/?", admin.UserManager, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/i18n/([0-9a-zA-Z_-]+)/?", i18n_server.I18N, dict(
        app_name=_app_name,
        projectConfig=projectConfig
    )),
    (r"/api/projects/?([0-9a-zA-Z_-]+)?/?", developer.Projects, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/config/?([0-9a-zA-Z_-]+)?/?", developer.Configs, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),
    (r"/api/automation/([0-9a-zA-Z_-]+)/?", developer.Automation, dict(
        app_name=_app_name,
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator_api,
        logger_api=logger_api
    )),

]
