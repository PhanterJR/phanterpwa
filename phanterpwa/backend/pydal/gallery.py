from pydal import Field
from pydal.validators import (
    IS_DATETIME,
    IS_IN_DB,
    IS_EMPTY_OR
)
from datetime import datetime


class GalleryTables():
    def __init__(self, DALDatabase):
        self.DALDatabase = DALDatabase
        self.DALDatabase.define_table('phanterpwagallery',
            Field('folder'),
            Field('filename'),
            Field('alias_name'),
            Field('content_type')
        )

        self.DALDatabase.define_table('auth_user_phanterpwagallery',
            Field('phanterpwagallery', 'reference phanterpwagallery'),
            Field('auth_user', 'reference auth_user', requires=IS_EMPTY_OR(
                IS_IN_DB(self.DALDatabase, self.DALDatabase.auth_user))),
            Field('subfolder'),
            Field('last_update', 'datetime', default=datetime.now(), requires=IS_EMPTY_OR(IS_DATETIME()))
        )
