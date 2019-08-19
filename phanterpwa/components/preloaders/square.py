import os
from ...helpers import DIV

PRELOADER = DIV(
    DIV(
        DIV(
            DIV(
                DIV(_class="phanterpwa_square"),
                _class="phanterpwa_square_container"
            ),
            _class='preloader-wrapper enabled'
        ),
        _class="phanterpwa-preloader-wrapper"),
    _class="phanterpwa-components-preloaders-square"
)

PRELOADER.sass_file(
    os.path.join(os.path.dirname(__file__), "square.sass")
)
PRELOADER.sass_vars = {
    "CONTAINERWIDTH": "200px",
    "CONTAINERHEIGHT": "200px",
    "COLOR": "orange",
    "BORDERSIZE": "10px",
    "BORDERRADIUS": "10%",
}
