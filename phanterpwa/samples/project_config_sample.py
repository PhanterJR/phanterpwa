project_config_sample = {
    "CONFIG_INDENTIFY": "project_config",
    "ENVIRONMENT": {
        "path": "",
        "python": ""
    },
    "PROJECT": {
        "name": "Scaffold_PhanterPWA_MPI",
        "title": "PhanterPWA",
        "version": "0.0.1",
        "author": "PhanterJR<phanterjr@conexaodidata.com.br>",
        "debug": True,
        "packaged": True
    },
    "API": {
        "secret_key": "your_default_key",
        "default_time_token_expires": 7200,
        "default_time_csrf_token_expires": 4200,
        "default_time_temporary_password_expires": 4200,
        "default_time_next_attempt_to_login": 3900,
        "default_time_client_token_expires": 63072000
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
        "use_tls": True,
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
    }
}
