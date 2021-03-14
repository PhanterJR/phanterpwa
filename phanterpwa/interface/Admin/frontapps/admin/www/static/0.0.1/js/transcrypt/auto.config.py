# Created automatically.
#
# In development it may be necessary to add static data
# to the client side application after compiling, use
# the CONFIGJS section of the application's app.ini
# file for this.
#

CONFIG = {
    "PROJECT": {
        "name": "Admin",
        "title": "PhanterPWA",
        "version": "0.0.1",
        "compilation": 29,
        "debug": True,
        "author": "PhanterJR<phanterjr@conexaodidata.com.br>"
    },
    "APP": {
        "build_folder": "C:\\Virtualenv\\py37\\phanterpwaenv\\Lib\\site-packages\\phanterpwa\\interface\\Admin\\frontapps\\admin\\www",
        "title": "Admin",
        "transcrypt_main_file": "application",
        "styles_main_file": "application",
        "timeout_to_resign": 600,
        "http_address": "http://127.0.0.1:10000",
        "websocket_address": "ws://127.0.0.1:10000/api/websocket",
        "name": "admin"
    },
    "I18N": {}
}
