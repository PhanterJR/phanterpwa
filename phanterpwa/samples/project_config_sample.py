project_config_sample = {
    "CONFIG_INDENTIFY": "project_config",
    "ENVIRONMENT": {
        "path": "",
        "python": ""
    },
    "PROJECT": {
        "name": "PhanterPWA",
        "title": "PhanterPWA",
        "description": "PhanterPWA Project",
        "version": "0.0.1",
        "compilation": 0,
        "author": "PhanterJR<phanterjr@conexaodidata.com.br>",
        "debug": True,
        "packaged": True,
        "minify": False,
        "baseport": 10000,
        "basehost": "127.0.0.1",
        "path": ""
    },
    "FRONTEND": {
        "sample_app": {
            "title": "PhanterPWA Frontend",
            "description": "Frontend Application PhanterPWA",
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
            "default_time_user_token_expire": 7200,
            "default_time_two_factor_code_expire": 3600
        }
    },
    "BACKEND": {
        "sample_app": {
            "title": "PhanterPWA Backend",
            "description": "Backend Application PhanterPWA",
            "build_folder": "",
            "transcrypt_main_file": "application",
            "styles_main_file": "application",
            "views_main_file": "index"
        }
    }
}
