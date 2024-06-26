from datetime import datetime
from pydal import Field
from pydal.validators import (
    IS_NOT_EMPTY,
    IS_DATETIME,
    IS_IN_DB,
    IS_EMPTY_OR
)


class MessagesTables():
    def __init__(self, DALDatabase):
        self.DALDatabase = DALDatabase
        self.DALDatabase.define_table(
            'internal_messages',
            Field('senders', 'reference auth_user', notnull=True, requires=IS_IN_DB(
                self.DALDatabase, self.DALDatabase.auth_user)),
            Field('subject', 'string', requires=IS_NOT_EMPTY()),
            Field('text_message', 'string', requires=IS_NOT_EMPTY()),
            Field('message_sent', 'boolean', default=False),
            Field('send_on', 'datetime', requires=IS_EMPTY_OR(IS_DATETIME())),
            Field('written_on', 'datetime', default=datetime.now(), requires=IS_EMPTY_OR(IS_DATETIME()))
        )

        self.DALDatabase.define_table(
            'internal_messages_recipients',
            Field('internal_messages', 'reference internal_messages', notnull=True, requires=IS_IN_DB(
                self.DALDatabase, self.DALDatabase.internal_messages)),
            Field('recipients', 'reference auth_user', notnull=True, requires=IS_IN_DB(
                self.DALDatabase, self.DALDatabase.auth_user)),
            Field('message_read', 'boolean', default=False),
        )
