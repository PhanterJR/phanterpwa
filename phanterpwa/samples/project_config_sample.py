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
        "compilation": 0,
        "author": "PhanterJR<phanterjr@conexaodidata.com.br>",
        "debug": True,
        "packaged": True,
        "path": ""
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
        "wait_time_to_try_activate_again": 3900,
        "timeout_to_resend_activation_email": 300,
        "timeout_to_resign": 600,
        "timeout_to_next_login_attempt": 4200,
        "max_login_attempts": 5,
        "max_activation_attempts": 5,
        "remote_address_on_development": "http://127.0.0.1:8881",
        "websocket_address_on_development": "ws://127.0.0.1:8881/api/websocket",
        "remote_address_on_production": "https://your_domain.com",
        "websocket_address_on_production": "wss://your_domain.com/api/websocket",
        "host": "0.0.0.0",
        "port": 8881
    },
    "APPS": {
        "app_01": {
          "title": "PhanterPWAClient",
          "build_folder": "",
          "timeout_to_resign": 600,
          "host": "127.0.0.1",
          "port": 8882,
          "transcrypt_main_file": "application",
          "styles_main_file": "application",
          "views_main_file": "index"
        },
    },
    "EMAIL": {
        "server": "mail.yourservermail.com",
        "username": "username@yourservermail.com",
        "default_sender": "contato@conexaodidata.com.br",
        "password": "{{password}}",
        "port": 465,
        "use_tls": False,
        "use_ssl": True
    },
    "CONTENT_EMAILS": {
        "copyright": "Conexão Didata © 2011-{{now}}",
        "link_to_your_site": "https://phanterpwa.conexaodidata.com.br"
    }
}
