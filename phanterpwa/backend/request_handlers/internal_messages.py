from pydal import Field
from pydal.validators import (
    IS_NOT_EMPTY,
    IS_DATETIME,
    IS_IN_DB,
    IS_EMPTY_OR
)


class Messages():
    def __init__(self, DALDatabase):
        self.DALDatabase = DALDatabase
        self.DALDatabase.define_table(
            'internal_messages',
            Field('senders', 'reference auth_user', notnull=True, requires=IS_IN_DB(
                self.DALDatabase, self.DALDatabase.auth_user)),
            Field('text_message', 'string', notnull=True, requires=IS_NOT_EMPTY()),
            Field('message_read', 'boolean', default=False),
            Field('subject', 'string', notnull=True, requires=IS_NOT_EMPTY()),
            Field('send_on', 'datetime', requires=IS_EMPTY_OR(IS_DATETIME()))
        )

        self.DALDatabase.define_table(
            'internal_messages_recipients',
            Field('internal_messages', 'reference internal_messages', notnull=True, requires=IS_IN_DB(
                self.DALDatabase, self.DALDatabase.internal_messages)),
            Field('recipients', 'reference auth_user', notnull=True, requires=IS_IN_DB(
                self.DALDatabase, self.DALDatabase.auth_user)),
            Field('message_read', 'boolean', default=False),
        )



