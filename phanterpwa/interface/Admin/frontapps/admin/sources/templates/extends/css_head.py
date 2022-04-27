from core import projectConfig as CONFIG
from phanterpwa.helpers import (
    LINK,
    CONCATENATE
)
app_version = CONFIG['PROJECT']['version']
html = CONCATENATE(
    LINK(
        _rel="stylesheet",
        _href="/static/{0}/css/normalize.css".format(app_version)
    ),
    LINK(
        _rel="stylesheet",
        _href="/static/{0}/lib/codemirror.css".format(app_version)
    ),
    LINK(
        _rel="stylesheet",
        _href="/static/{0}/css/all.min.css".format(app_version)
    ),
    LINK(
        _rel="stylesheet",
        _href="/static/{0}/css/phanterpwa.css".format(app_version)
    ),
    LINK(
        _rel="stylesheet",
        _href="/static/{0}/css/application.css".format(app_version)
    ),
)
