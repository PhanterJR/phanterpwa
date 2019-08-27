project_config_sample = {
    "CONFIG_INDENTIFY": "project_config",
    "ENVIRONMENT": {
        "path": "",
        "python": ""
    },
    "PROJECT": {
        "name": "PhanterPWA",
        "title": "PhanterPWA",
        "version": "0.0.1",
        "author": "PhanterJR<phanterjr@conexaodidata.com.br>",
        "debug": True,
        "packaged": True
    },
    "API": {
        "secret_key": "your_default_key",
        "url_secret_key": "your_default_key2",
        "default_time_user_token_expire": 7200,
        "default_time_csrf_token_expire": 4200,
        "default_time_temporary_password_expire": 4200,
        "timeout_to_resend_temporary_password_mail": 3900,
        "default_time_client_token_expire": 63072000,
        "default_time_activation_code_expire": 3600,
        "wait_time_to_try_activate_again": 3900,
        "timeout_to_resend_activation_email": 300,
        "max_login_attempts": 5,
        "max_activation_attempts": 5
    },
    "APP": {
        "compiled_app_folder": "{{PROJECT_FOLDER}}\\app\\www",
        "address_in_development": "http://127.0.0.1:8882"
    },
    "PATH": {
        "project": "{{PROJECT_FOLDER}}",
        "api": "{{PROJECT_FOLDER}}\\api",
        "app": "{{PROJECT_FOLDER}}\\app"
    },
    "EMAIL": {
        "server": "mail.yourservermail.com",
        "username": "username@yourservermail.com",
        "password": "password",
        "port": 465,
        "use_tls": False,
        "use_ssl": True
    },
    "TRANSCRYPT": {
        "main_files": [
            "{{PROJECT_FOLDER}}\\app\\scripts\\application\\application.py",
            "{{PROJECT_FOLDER}}\\app\\scripts\\websocket\\websocket.py"
        ]
    },
    "API_SERVER": {
        "host": "127.0.0.1",
        "port": 8881
    },
    "APP_SERVER": {
        "host": "127.0.0.1",
        "port": 8882
    },
    "CONFIGJS": {
        "api_server_address": "http://127.0.0.1:8881",
        "api_websocket_address": "ws://127.0.0.1:8881/websocket"
    },
    "CONTENT_EMAILS": {
        "copyright": "Conexão Didata © 2011-{{now}}",
        "link_to_your_site": "https://phanterpwa.conexaodidata.com.br"
    }
}
