import os
from ...helpers import DIV

PRELOADER = DIV(
    DIV(
        DIV(
            DIV(
                DIV(_class="phanterpwa_discs phanterpwa_discs_one"),
                DIV(_class="phanterpwa_discs phanterpwa_discs_two"),
                DIV(_class="phanterpwa_discs phanterpwa_discs_three"),
                DIV(_class="phanterpwa_discs phanterpwa_discs_four"),
                DIV(_class="phanterpwa_discs phanterpwa_discs_five"),
                _class="pwa_discs_container"
            ),
            _class='preloader-wrapper enabled'
        ),
        _class="phanterpwa-preloader-wrapper"),
    _class="phanterpwa-components-preloaders-discs"
)

PRELOADER.sass_file(
    os.path.join(os.path.dirname(__file__), "discs.sass")
)
PRELOADER.sass_vars = {
    'COLOR1TOP': 'red',
    'COLOR1LEFT': 'transparent',
    'COLOR1BOTTOM': '$COLOR1TOP',
    'COLOR1RIGHT': 'transparent',
    'COLOR2TOP': 'orange',
    'COLOR2LEFT': 'transparent',
    'COLOR2BOTTOM': '$COLOR2TOP',
    'COLOR2RIGHT': 'transparent',
    'COLOR3TOP': 'blue',
    'COLOR3LEFT': 'transparent',
    'COLOR3BOTTOM': '$COLOR3TOP',
    'COLOR3RIGHT': 'transparent',
    'COLOR4TOP': 'green',
    'COLOR4LEFT': '$COLOR4TOP',
    'COLOR4BOTTOM': '$COLOR4TOP',
    'COLOR4RIGHT': 'transparent',
    'COLOR5TOP': 'black',
    'COLOR5LEFT': '$COLOR5TOP',
    'COLOR5BOTTOM': 'transparent',
    'COLOR5RIGHT': 'transparent',
    'BORDERRADIUS': '100%',
    'CONTAINERWIDTH': '200px',
    'BORDER': '10px'
}
