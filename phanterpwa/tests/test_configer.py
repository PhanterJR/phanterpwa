import os
import sys
import json
import unittest
import configparser
from phanterpwa.configer import ProjectConfig
from phanterpwa.tools import interpolate

CURRENT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__)))
ENV_PYTHON = os.path.normpath(sys.executable)

sample_cfg = """{
  "CONFIG_INDENTIFY": "project_config",
  "ENVIRONMENT": {
    "python": "{{pyenv}}",
    "path": "{{pypath}}"
  },
  "PROJECT": {
    "name": "project01",
    "title": "PhanterPWA",
    "version": "0.0.1",
    "compilation": 0,
    "author": "PhanterJR<phanterjr@conexaodidata.com.br>",
    "debug": true,
    "packaged": true,
    "minify": false,
    "baseport": 10000,
    "basehost": "127.0.0.1",
    "path": "{{projectpath}}"
  },
  "FRONTEND": {
    "app01": {
      "build_folder": "{{app01}}",
      "title": "app01",
      "transcrypt_main_file": "application",
      "styles_main_file": "application",
      "views_main_file": "index",
      "timeout_to_resign": 600,
      "host": "127.0.0.1",
      "port": 10001
    },
    "app02": {
      "build_folder": "{{app02}}",
      "title": "app02",
      "transcrypt_main_file": "application",
      "styles_main_file": "application",
      "views_main_file": "index",
      "timeout_to_resign": 600,
      "host": "127.0.0.1",
      "port": 10002
    }
  },
  "BACKEND": {
    "api": {
      "title": "PhanterPWA Backend",
      "default_time_user_token_expire": 7200,
      "default_time_user_token_expire_remember_me": 2592000,
      "default_time_csrf_token_expire": 4200,
      "default_time_temporary_password_expire": 4200,
      "timeout_to_resend_temporary_password_mail": 3900,
      "default_time_client_token_expire": 63072000,
      "default_time_activation_code_expire": 3600,
      "default_time_two_factor_code_expire": 3600,
      "wait_time_to_try_activate_again": 3900,
      "timeout_to_resend_activation_email": 300,
      "timeout_to_resign": 600,
      "timeout_to_next_login_attempt": 4200,
      "max_login_attempts": 5,
      "max_activation_attempts": 5,
      "host": "127.0.0.1",
      "port": 10000,
      "secret_key": "{{secret_key}}",
      "url_secret_key": "{{url_secret_key}}"
    }
  }
}"""

sample_cfg2 = """{
    "CONFIG_INDENTIFY": "project_config",
    "ENVIRONMENT": {
        "python": "{{pyenv}}",
        "path": "{{pypath}}"
    },
    "PROJECT": {
        "name": "project_without_confgjson_and_with_ini",
        "title": "CHANGED",
        "version": "0.0.1",
        "compilation": 0,
        "author": "PhanterJR<phanterjr@conexaodidata.com.br>",
        "debug": true,
        "packaged": true,
        "path": "{{projectpath}}"
    },
    "API": {
        "secret_key": "{{secret_key}}",
        "url_secret_key": "{{url_secret_key}}",
        "default_time_user_token_expire": 7200,
        "default_time_user_token_expire_remember_me": 2592000,
        "default_time_csrf_token_expire": 4200,
        "default_time_temporary_password_expire": 4200,
        "timeout_to_resend_temporary_password_mail": 3900,
        "default_time_client_token_expire": 63072000,
        "default_time_activation_code_expire": 3600,
        "default_time_two_factor_code_expire": 3600,
        "wait_time_to_try_activate_again": 3900,
        "timeout_to_resend_activation_email": 300,
        "timeout_to_resign": 600,
        "timeout_to_next_login_attempt": 4200,
        "max_login_attempts": 5,
        "max_activation_attempts": 5,
        "remote_address_debug": "http://127.0.0.1:8881",
        "websocket_address_debug": "ws://127.0.0.1:8881/api/websocket",
        "remote_address": "https://your_domain.com",
        "websocket_address": "wss://your_domain.com/api/websocket",
        "host": "127.0.0.1",
        "port": 8881
    },
    "FRONTEND": {
        "app01": {
            "build_folder": "{{app01}}",
            "title": "app01",
            "timeout_to_resign": 600,
            "transcrypt_main_file": "application",
            "styles_main_file": "application",
            "views_main_file": "index",
            "host": "127.0.0.1",
            "port": 8882
        },
        "app02": {
            "build_folder": "{{app02}}",
            "title": "app02",
            "timeout_to_resign": 600,
            "transcrypt_main_file": "application",
            "styles_main_file": "application",
            "views_main_file": "index",
            "host": "127.0.0.1",
            "port": 8883
        }
    },
    "EMAIL": {
        "server": "mail.yourservermail.com",
        "username": "username@yourservermail.com",
        "default_sender": "contato@conexaodidata.com.br",
        "password": "{{password}}",
        "port": 465,
        "use_tls": false,
        "use_ssl": true
    },
    "CONTENT_EMAILS": {
        "copyright": "Conex\u00e3o Didata \u00a9 2011-{{now}}",
        "link_to_your_site": "https://phanterpwa.conexaodidata.com.br"
    }
}"""

api_sample = """[API]
default_time_user_token_expire = 7200
default_time_user_token_expire_remember_me = 2592000
default_time_csrf_token_expire = 4200
default_time_temporary_password_expire = 4200
timeout_to_resend_temporary_password_mail = 3900
default_time_client_token_expire = 63072000
default_time_activation_code_expire = 3600
default_time_two_factor_code_expire = 3600
wait_time_to_try_activate_again = 3900
timeout_to_resend_activation_email = 300
timeout_to_resign = 600
timeout_to_next_login_attempt = 4200
max_login_attempts = 5
max_activation_attempts = 5
remote_address_debug = http://127.0.0.1:8881
websocket_address_debug = ws://127.0.0.1:8881/api/websocket
remote_address = https://your_domain.com
websocket_address = wss://your_domain.com/api/websocket
host = 127.0.0.1
port = 8881

"""
project_sample = """[PROJECT]
title = CHANGED
version = 0.0.1
author = PhanterJR<phanterjr@conexaodidata.com.br>
debug = True
packaged = True

[EMAIL]
server = mail.yourservermail.com
username = username@yourservermail.com
default_sender = contato@conexaodidata.com.br
port = 465
use_tls = False
use_ssl = True

[CONTENT_EMAILS]
copyright = Conexão Didata © 2011-{{now}}
link_to_your_site = https://phanterpwa.conexaodidata.com.br

"""
project_sample2 = """[PROJECT]
title = PhanterPWA
version = 0.0.1
author = PhanterJR<phanterjr@conexaodidata.com.br>
debug = True
packaged = True

[EMAIL]
server = mail.yourservermail.com
username = username@yourservermail.com
default_sender = contato@conexaodidata.com.br
port = 465
use_tls = False
use_ssl = True

[CONTENT_EMAILS]
copyright = Conexão Didata © 2011-{{now}}
link_to_your_site = https://phanterpwa.conexaodidata.com.br

"""


class TestProjectConfig(unittest.TestCase):
    def test0_documentation_example(self):
        # module doc
        import phanterpwa
        path_dir = os.path.join(os.path.dirname(phanterpwa.__file__), "tests", "test_configer_path", "project01")
        if os.path.isfile(os.path.join(path_dir, "config.json")):
            os.remove(os.path.join(path_dir, "config.json"))
        # if os.path.isfile(os.path.join(path_dir, "backapps", "api", "app.ini")):
        #     os.remove(os.path.join(path_dir, "backapps", "api", "app.ini"))
        if os.path.isfile(os.path.join(path_dir, "project.ini")):
            os.remove(os.path.join(path_dir, "project.ini"))
        cfg = ProjectConfig(path_dir)
        print(cfg._ini_apps_backend)

        self.assertTrue(os.path.isfile(os.path.join(path_dir, "config.json")))
        self.assertTrue(os.path.isfile(os.path.join(path_dir, "backapps", "api", "app.ini")))
        self.assertTrue(os.path.isfile(os.path.join(path_dir, "project.ini")))
        # file
        self.assertEqual(
            cfg.file,
            os.path.join(path_dir, "config.json")
        )
        # config
        string_cfg = json.dumps(cfg.config, ensure_ascii=False, indent=2)
        print(string_cfg)
        s_cfg = interpolate(sample_cfg, {
            "pyenv": ENV_PYTHON.replace("\\", "\\\\"),
            "pypath": os.path.dirname(ENV_PYTHON).replace("\\", "\\\\"),
            "projectpath": path_dir.replace("\\", "\\\\"),
            "app01": os.path.join(path_dir, "frontapps", "app01", "www").replace("\\", "\\\\"),
            "app02": os.path.join(path_dir, "frontapps", "app02", "www").replace("\\", "\\\\")
        })
        self.assertEqual(
            string_cfg,
            s_cfg
        )
        # inis
        self.assertTrue(isinstance(cfg.backend_ini["api"], configparser.ConfigParser))
        self.assertTrue(isinstance(cfg.project_ini, configparser.ConfigParser))
        self.assertTrue(isinstance(cfg.project_secret_ini, configparser.ConfigParser))
        self.assertTrue(isinstance(cfg.frontend_ini["app01"], configparser.ConfigParser))
        self.assertTrue(isinstance(cfg.frontend_ini["app02"], configparser.ConfigParser))
        # save
        self.assertEqual(
            cfg['PROJECT']['title'],
            "PhanterPWA"
        )
        cfg['PROJECT']['title'] = 'PhanterPWA2'
        cfg.save()
        with open(os.path.join(path_dir, "config.json"), encoding="utf-8") as f:
            content = json.load(f)
        content
        self.assertEqual(
            content['PROJECT']['title'],
            "PhanterPWA2"
        )

    # def test1(self):
    #     path_dir = os.path.join(CURRENT_DIR, 'test_configer_path', 'project_without_ini')
    #     if os.path.isfile(os.path.join(path_dir, "project.ini")):
    #         os.remove(os.path.join(path_dir, "project.ini"))
    #     if os.path.isfile(os.path.join(path_dir, "api", "api.ini")):
    #         os.remove(os.path.join(path_dir, "api", "api.ini"))
    #     ProjectConfig(path_dir)
    #     self.assertTrue(os.path.isfile(os.path.join(path_dir, "config.json")))
    #     self.assertTrue(os.path.isfile(os.path.join(path_dir, "api", "api.ini")))
    #     self.assertTrue(os.path.isfile(os.path.join(path_dir, "project.ini")))
    #     with open(os.path.join(path_dir, "api", "api.ini"), "r", encoding="utf-8") as f:
    #         apicontent = f.read()
    #     self.assertEqual(apicontent, api_sample)
    #     with open(os.path.join(path_dir, "project.ini"), "r", encoding="utf-8") as f:
    #         projectcontent = f.read()
    #     self.assertEqual(projectcontent, project_sample2)

    # def test2(self):
    #     path_dir = os.path.join(CURRENT_DIR, 'test_configer_path', 'project_without_confgjson_and_with_ini')
    #     if os.path.isfile(os.path.join(path_dir, "config.json")):
    #         os.remove(os.path.join(path_dir, "config.json"))
    #     with open(os.path.join(path_dir, "project.ini"), 'w', encoding='utf-8') as f:
    #         f.write(project_sample2)

    #     cfg = ProjectConfig(path_dir)
    #     self.assertTrue(os.path.isfile(os.path.join(path_dir, "config.json")))
    #     self.assertTrue(os.path.isfile(os.path.join(path_dir, "api", "api.ini")))
    #     self.assertTrue(os.path.isfile(os.path.join(path_dir, "project.ini")))
    #     self.assertEqual(cfg['PROJECT']['title'], 'PhanterPWA')
    #     self.assertEqual(cfg.project_ini['PROJECT']['title'], 'PhanterPWA')

    #     cfg['PROJECT']['title'] = "CHANGED"
    #     cfg.save()
    #     with open(os.path.join(path_dir, "config.json"), "r", encoding="utf-8") as f:
    #         cfgcontent = json.load(f)
    #         cfgcontent = json.dumps(cfgcontent, ensure_ascii=False, indent=4)
    #     s_cfg = interpolate(sample_cfg2, {
    #         "pyenv": ENV_PYTHON.replace("\\", "\\\\"),
    #         "pypath": os.path.dirname(ENV_PYTHON).replace("\\", "\\\\"),
    #         "projectpath": path_dir.replace("\\", "\\\\"),
    #         "app01": os.path.join(path_dir, "frontapps", "app01", "www").replace("\\", "\\\\"),
    #         "app02": os.path.join(path_dir, "frontapps", "app02", "www").replace("\\", "\\\\")
    #     })
    #     self.assertEqual(cfgcontent, s_cfg)
    #     with open(os.path.join(path_dir, "api", "api.ini"), "r", encoding="utf-8") as f:
    #         apicontent = f.read()
    #     self.assertEqual(apicontent, api_sample)
    #     with open(os.path.join(path_dir, "project.ini"), "r", encoding="utf-8") as f:
    #         projectcontent = f.read()
    #     self.assertEqual(projectcontent, project_sample)


if __name__ == '__main__':
    unittest.main()
