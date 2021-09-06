import os
import shutil
from pydal import Field
from pydal.validators import (
    IS_NOT_EMPTY,
    IS_EMAIL,
    IS_DATETIME,
    IS_IN_DB,
    IS_EMPTY_OR,
    IS_NOT_IN_DB
)
from datetime import datetime


class AuthTables():
    def __init__(self, projectConfig, DALDatabase, i18nTranslator=None, logger_api=None):
        self.DALDatabase = DALDatabase
        default_language = projectConfig["PROJECT"].get("default_language", "en-US")
        self.logger_api = logger_api
        self.DALDatabase.define_table(
            'auth_user',
            Field('first_name', 'string', notnull=True, requires=IS_NOT_EMPTY(), phanterpwa={
                'group': 'group1',
                '_class': 'p-col w1p100 w4p70 e-float_right'
            }),
            Field('last_name', 'string', notnull=True, requires=IS_NOT_EMPTY(), phanterpwa={
                'group': 'group1',
                '_class': 'p-col w1p100 w4p70 e-float_right'
            }),
            Field('email', 'string', notnull=True, unique=True, phanterpwa={
                'group': 'group1',
                '_class': 'p-col w1p100 w4p70 e-float_right'
            }),
            Field('email_activated', 'boolean', default=False),
            Field('fone_number', 'string', phanterpwa={
                'out_of_form': True
            }),
            Field('fone_number_activated', 'boolean', default=False),
            Field('password_hash', 'string', notnull=True, requires=IS_NOT_EMPTY(), phanterpwa={
                'out_of_form': True
            }),
            Field('login_attempts', 'integer', default=0),
            Field('datetime_next_attempt_to_login', 'datetime', requires=IS_EMPTY_OR(IS_DATETIME()), phanterpwa={
                'validators': ['IS_EMPTY_OR', 'IS_DATETIME:yyyy-MM-dd HH:mm:ss'],
                # '_class': 'p-col w1p100 w4p40',
                # 'section': 'Identidade'

            }),
            Field('temporary_password', 'text', phanterpwa={
                'out_of_form': True
            }),  # it's used in the debug
            Field('temporary_password_hash', 'text', phanterpwa={
                'out_of_form': True
            }),

            # datetime_next_attempt_to_login
            Field('temporary_password_expire', 'datetime', requires=IS_EMPTY_OR(IS_DATETIME()), phanterpwa={
                'validators': ['IS_EMPTY_OR', 'IS_DATETIME:yyyy-MM-dd HH:mm:ss']
            }),
            Field('timeout_to_resend_temporary_password_mail', 'datetime', requires=IS_EMPTY_OR(IS_DATETIME()), phanterpwa={
                'validators': ['IS_EMPTY_OR', 'IS_DATETIME:yyyy-MM-dd HH:mm:ss']
            }),
            Field('activation_code_by_mobile', 'string', default=0),
            Field('activation_code', 'string', default=0),
            Field('activation_attempts', 'integer', default=0),
            Field('timeout_to_resend_activation_email', 'datetime', requires=IS_EMPTY_OR(IS_DATETIME()), phanterpwa={
                'validators': ['IS_EMPTY_OR', 'IS_DATETIME:yyyy-MM-dd HH:mm:ss']
            }),

            # wait_time_to_try_activate_again
            Field('datetime_next_attempt_to_activate', 'datetime', requires=IS_EMPTY_OR(IS_DATETIME()), phanterpwa={
                'validators': ['IS_EMPTY_OR', 'IS_DATETIME:yyyy-MM-dd HH:mm:ss']
            }),
            Field('permit_mult_login', 'boolean', default=True),
            Field('activated', 'boolean', default=False, notnull=True),
            Field('websocket_opened', 'boolean', default=False, notnull=True, phanterpwa={
                'out_of_form': True
            }),
            Field('locale', 'string', default=default_language),
            Field('two_factor_login', 'boolean', default=False)
        )

        def delete_upload_folder(s):
            upload_folder = os.path.join(projectConfig["PROJECT"]["path"], "backapps", "api", "uploads")
            target = os.path.join(upload_folder, "user_{0}".format(s.select().first().id))
            if os.path.exists(target) and os.path.isdir(target):
                try:
                    shutil.rmtree(target)
                except Exception:
                    if self.logger_api:
                        self.logger_api.error("Problem on delete folder: \"{0}\"".format(target), exc_info=True)
            else:
                if self.logger_api:
                    self.logger_api.warning("Ther folder \"{0}\" not exists".format(target))

        self.DALDatabase.auth_user._before_delete.append(lambda s: delete_upload_folder(s))

        self.DALDatabase.auth_user.email.requires = [
            IS_EMAIL(),
            IS_NOT_IN_DB(self.DALDatabase, self.DALDatabase.auth_user.email, error_message="Email already in database.")
        ]
        self.DALDatabase.auth_user.fone_number.requires = [
            IS_EMPTY_OR(IS_NOT_IN_DB(self.DALDatabase, self.DALDatabase.auth_user.fone_number, error_message="Mobile number already in database."))
        ]
        self.DALDatabase.define_table('auth_group',
            Field('role', 'string'),
            Field('grade', 'integer', default=0),
            Field('description', 'text'))

        self.DALDatabase.define_table('auth_membership',
            Field('auth_user', 'reference auth_user', requires=IS_IN_DB(
                self.DALDatabase, self.DALDatabase.auth_user)),
            Field('auth_group', 'reference auth_group', requires=IS_IN_DB(
                self.DALDatabase, self.DALDatabase.auth_group)))

        self.DALDatabase.define_table('auth_activity',
            Field('auth_user', 'reference auth_user', requires=IS_IN_DB(self.DALDatabase, self.DALDatabase.auth_user)),
            Field('request', 'text'),
            Field('activity', 'string'),
            Field('date_activity', 'datetime', default=datetime.now()))

        self.DALDatabase.define_table('email_user_list',
            Field('auth_user', 'reference auth_user', requires=IS_IN_DB(self.DALDatabase, self.DALDatabase.auth_user)),
            Field('email', 'string', notnull=True),
            Field('datetime_changed', 'datetime', default=datetime.now())
        )

        self.DALDatabase.define_table('social_auth',
            Field('social_name', 'string'),
            Field('request_state', 'text'),
            Field('client_token', 'text'),
            Field('datetime_created', 'datetime', default=datetime.now()),
            Field('origin', 'text'),
            Field('used', 'boolean', default=False),
            Field('user_credentials', 'text')
        )

        self.DALDatabase.define_table('two_factor_login',
            Field('auth_user', 'reference auth_user', requires=IS_IN_DB(self.DALDatabase, self.DALDatabase.auth_user)),
            Field('two_factor_url', 'text'),
            Field('two_factor_code'),
            Field('datetime_changed', 'datetime', default=datetime.now())
        )

        self.DALDatabase.email_user_list.email.requires = [
            IS_EMAIL()
        ]

        if self.DALDatabase(self.DALDatabase.auth_group).isempty():
            self.DALDatabase._adapter.reconnect()
            self.DALDatabase.auth_group.insert(
                role="root", grade=100, description="Administrator of application (Developer)")
            self.DALDatabase.auth_group.insert(role="administrator", grade=10, description="Super user of site")
            self.DALDatabase.auth_group.insert(role="user", grade=1, description="Default user")
            self.DALDatabase.commit()

        if self.DALDatabase(self.DALDatabase.auth_membership).isempty():
            self.DALDatabase._adapter.reconnect()
            if self.DALDatabase.auth_user[1]:
                id_role = self.DALDatabase(self.DALDatabase.auth_group.role == 'root').select().first()
                if id_role:
                    self.DALDatabase.auth_membership.insert(auth_user=1,
                    auth_group=id_role.id)
                    self.DALDatabase.commit()
