from pydal import Field
from pydal.validators import (
    IS_NOT_EMPTY,
    IS_EMAIL,
    IS_IN_DB,
    IS_NOT_IN_DB
)
from datetime import datetime


class CASTables():
    def __init__(self, projectConfig, DALDatabase):
        self.DALDatabase = DALDatabase
        self.DALDatabase.define_table('auth_cas',
            Field('email', 'string', notnull=True, unique=True),
            Field('password_hash', 'string', notnull=True, requires=IS_NOT_EMPTY())
        )
        self.DALDatabase.auth_cas.email.requires = [
            IS_EMAIL(),
            IS_NOT_IN_DB(self.DALDatabase, self.DALDatabase.auth_cas.email, error_message="Email already in database.")
        ]
        self.DALDatabase.define_table('cas_activity',
            Field('auth_cas', 'reference auth_cas', requires=IS_IN_DB(self.DALDatabase, self.DALDatabase.auth_cas)),
            Field('request', 'text'),
            Field('activity', 'string'),
            Field('date_activity', 'datetime', default=datetime.now())
        )
        self.DALDatabase.define_table('apps_authorization',
            Field('app_name', 'string'),
            Field('auth_cas', 'reference auth_cas', requires=IS_IN_DB(self.DALDatabase, self.DALDatabase.auth_cas)),
            Field('origin', 'string'),
            Field('authorization', 'text', requires=IS_NOT_EMPTY())
        )
        self.DALDatabase.apps_authorization.app_name.requires = [
            IS_NOT_EMPTY(),
            IS_NOT_IN_DB(self.DALDatabase, self.DALDatabase.apps_authorization.app_name, error_message="Email already in database.")
        ]
