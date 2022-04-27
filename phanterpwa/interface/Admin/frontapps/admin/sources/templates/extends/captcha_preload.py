
from core import projectConfig as CONFIG
from phanterpwa.components.preloaders import android

PRELOADER = android.PRELOADER
if CONFIG['PROJECT']["debug"]:
    import os
    from phanterpwa.tools import app_name_from_relative_child
    app_folder_name = app_name_from_relative_child(CONFIG['PROJECT']['path'], __file__)
    PRELOADER._target_sass = os.path.join(
        CONFIG["PROJECT"]["path"], "frontapps", app_folder_name, "sources", "styles", "extends", "capcha_preload.sass")
PRELOADER.sass_vars = {
    'STROKEWIDTH': '10px',
    'CONTAINERWIDTH': '200px',
    'COLOR1': 'blue',
    'COLOR2': 'red',
    'COLOR3': '#f4b400',
    'COLOR4': 'green'
}
html = PRELOADER
