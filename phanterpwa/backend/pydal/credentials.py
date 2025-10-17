from pydal import Field
from pydal.validators import (
    IS_IN_DB,
    IS_EMPTY_OR,
    IS_DATETIME
)
from datetime import datetime


class CredentialsTables():
    def __init__(self, projectConfig, DALDatabase, i18nTranslator=None, logger_api=None):
        self.DALDatabase = DALDatabase
        self.logger_api = logger_api
        self.DALDatabase.define_table('client',
            Field('token', 'text', index=True),
            Field('auth_user', 'reference auth_user', requires=IS_EMPTY_OR(
                IS_IN_DB(self.DALDatabase, self.DALDatabase.auth_user))),
            Field('date_created', 'datetime', index=True, default=datetime.now(), requires=IS_EMPTY_OR(IS_DATETIME())),
            Field('last_resign', 'datetime', default=datetime.now()),
            Field('remember_me', 'boolean', default=False),
            Field('locked', 'boolean', default=False),
        )

        self.DALDatabase.define_table('captcha',
            Field('token', 'text', index=True),
            Field('form_identify', 'string'),
            Field('user_agent', 'string'),
            Field('ip', 'string'),
            Field('date_created', 'datetime', index=True, default=datetime.now(), requires=IS_DATETIME()),
            Field('client', 'reference client', requires=IS_EMPTY_OR(
                IS_IN_DB(self.DALDatabase, self.DALDatabase.client)))
        )

        self.DALDatabase.define_table('google_captcha',
            Field('token', 'text', index=True),
            Field('form_identify', 'string'),
            Field('user_agent', 'string'),
            Field('ip', 'string'),
            Field('date_created', 'datetime', index=True, default=datetime.now(), requires=IS_DATETIME()),
            Field('client', 'reference client', requires=IS_EMPTY_OR(
                IS_IN_DB(self.DALDatabase, self.DALDatabase.client)))
        )

        self.DALDatabase.define_table('csrf',
            Field('token', 'text', index=True),
            Field('form_identify', 'string'),
            Field('user_agent', 'string'),
            Field('ip', 'string'),
            Field('date_created', 'datetime', index=True, default=datetime.now(), requires=IS_DATETIME()),
            Field('client', 'reference client', requires=IS_EMPTY_OR(
                IS_IN_DB(self.DALDatabase, self.DALDatabase.client)))
        )
