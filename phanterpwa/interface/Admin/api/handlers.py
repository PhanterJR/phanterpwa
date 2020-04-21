import os
from phanterpwa.apitools.request_hadlers import (
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
from core import (
    projectConfig,
    Translator_api as Translator,
    Translator_email,
    Translator_captcha,
    logger_api
)
from .models import *
_current_dir = os.path.join(os.path.dirname(__file__))
_debug = projectConfig['PROJECT']['debug']


SETTINGS = {
    'debug': _debug
}


HANDLER = [
    (r"/?(api)?/?", welcome.Welcome, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/websocket/?", developer.EchoWebSocket, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/client/?", credentials.SignClient, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/signforms/([0-9a-zA-Z_-]+)/?", credentials.SignForms, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/signcaptchaforms/([0-9a-zA-Z_-]+)/?", credentials.SignCaptchaForms, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        Translator_captcha=Translator_captcha, i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/signlockform/?", credentials.SignLockForm, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/resigncredentials/?", credentials.ReSing, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/auth/?", auth.Auth, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        Translator_email=Translator_email,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/auth/two-factor/([0-9a-zA-Z_\-\.]+)/?", auth.TwoFactor, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        Translator_email=Translator_email,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/auth/lock/?", auth.LockUser, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/auth/image/([0-9]+)/?", auth.ImageUser, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/auth/create/?", auth.CreateAccount, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/auth/change/?", auth.ChangeAccount, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        Translator_email=Translator_email,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/auth/change-password/?", auth.ChangePassword, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/auth/request-password/?", auth.RequestAccount, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        Translator_email=Translator_email,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/auth/active-account/?", auth.ActiveAccount, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        Translator_email=Translator_email,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/oauth/prompt/([a-zA-Z_-]+)?/?", oauth.Prompt, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/oauth/redirect/([a-zA-Z_-]+)?/?", oauth.Redirect, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/admin/usermanager/([0-9]+)?/?", admin.UserManager, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/i18n/([0-9a-zA-Z_-]+)/?", i18n_server.I18N, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/projects/?([0-9a-zA-Z_-]+)?/?", developer.Projects, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/config/?([0-9a-zA-Z_-]+)?/?", developer.Configs, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),
    (r"/api/automation/([0-9a-zA-Z_-]+)/?", developer.Automation, dict(
        projectConfig=projectConfig,
        DALDatabase=db,
        i18nTranslator=Translator,
        logger_api=logger_api
    )),

]
