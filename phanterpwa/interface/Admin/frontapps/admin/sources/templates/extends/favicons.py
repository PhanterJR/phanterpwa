from core import projectConfig as CONFIG
from phanterpwa.helpers import (
    CONCATENATE,
    LINK
)
app_version = CONFIG['PROJECT']['version']
html = CONCATENATE(
    LINK(
        _rel="apple-touch-icon",
        _sizes="180x180",
        _href="/static/%s/favicons/apple-touch-icon.png" %
        (app_version)
    ),
    LINK(
        _rel="icon",
        _type="image/png",
        _sizes="32x32",
        _href="/static/%s/favicons/favicon-32x32.png" %
        (app_version)
    ),
    LINK(
        _rel="icon",
        _type="image/png",
        _sizes="16x16",
        _href="/static/%s/favicons/favicon-16x16.png" %
        (app_version)
    ),
    LINK(
        _rel="manifest",
        _href="/static/%s/favicons/manifest.json" %
        (app_version)
    ),
    LINK(
        _rel="mask-icon",
        _href="/static/%s/favicons/safari-pinned-tab.svg" %
        (app_version),
        _color="#5bbad5"
    )
)
