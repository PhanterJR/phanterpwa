from core import projectConfig as CONFIG
from phanterpwa.helpers import (
    SCRIPT,
    CONCATENATE,
    XML
)
from phanterpwa.tools import (
    interpolate,
    app_name_from_relative_child
)
app_version = CONFIG['PROJECT']['version']
app_folder_name = app_name_from_relative_child(CONFIG['PROJECT']['path'], __file__)
transcrypt_main_file = CONFIG["FRONTEND"][app_folder_name]['transcrypt_main_file']
html = CONCATENATE(
    SCRIPT(
        _src="/static/{0}/js/jquery.min.js".format(app_version)
    ),
    SCRIPT(
        _src="/static/{0}/lib/codemirror.js".format(app_version)
    ),
    SCRIPT(
        _src="/static/{0}/mode/python/python.js".format(app_version)
    ),
    SCRIPT(
        _src="/static/{0}/js/hammer.min.js".format(app_version)
    ),
    SCRIPT(
        _src="/static/{0}/js/touch-emulator.js".format(app_version)
    ),
    SCRIPT(
        _src="/static/{0}/js/jquery.hammer.js".format(app_version)
    ),
    XML(
        interpolate(
            "<script type=\"module\">import * as {{MODULE}} from '/static/{{VERSION}}/js/transcrypt/{{FILE}}'</script>",
            context={'MODULE': transcrypt_main_file, 'VERSION': app_version, 'FILE': "{0}.js".format(transcrypt_main_file)}
        )
    ),

)
