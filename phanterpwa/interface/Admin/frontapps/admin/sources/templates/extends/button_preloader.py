from core import projectConfig as CONFIG
from phanterpwa.components.preloaders import run_points
from phanterpwa.helpers import DIV

PRELOADER = run_points.PRELOADER
if CONFIG['PROJECT']["debug"]:
    import os
    from phanterpwa.tools import app_name_from_relative_child
    app_folder_name = app_name_from_relative_child(CONFIG['PROJECT']['path'], __file__)
    PRELOADER._target_sass = os.path.join(
        CONFIG["PROJECT"]["path"], "frontapps", app_folder_name, "sources", "styles", "extends", "run_points.sass")
PRELOADER.sass_vars = {
    'COLOR1': 'red',
    'COLOR2': 'blue',
    'COLOR3': 'yellow',
    'COLOR4': 'pink',
    'COLOR5': 'green',
    'BORDERRADIUS': '100%',
    'CONTAINERWIDTH': '100px'
}
html = DIV(PRELOADER, _class="container_preloader_button_auth_user")
