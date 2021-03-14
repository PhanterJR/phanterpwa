import os
import glob
from pydal import DAL
from core import (projectConfig, logger_api)
from phanterpwa.backend.pydal.auth import AuthTables
from phanterpwa.backend.pydal.credentials import CredentialsTables
from phanterpwa.backend.pydal.gallery import GalleryTables
database_path = os.path.join(os.path.dirname(__file__), '..', 'databases')
files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))

db = DAL(
    'sqlite://storage.sqlite',
    pool_size=10,
    folder=database_path,
    # migrate_enabled=True,
    check_reserved=['all']
)

authdb = AuthTables(projectConfig, db, logger_api=logger_api)
credentialsdb = CredentialsTables(projectConfig, db, logger_api=logger_api)
phantergallerydb = GalleryTables(db)

__all__ = ['authdb', 'credentialsdb', 'phantergallerydb']
_all = [os.path.basename(x)[0:-3] for x in files if os.path.basename(x) != "__init__.py" and x[-3:] == ".py"]
_all.sort()
for y in _all:
    __all__.append(y)
__all__.append("db")
