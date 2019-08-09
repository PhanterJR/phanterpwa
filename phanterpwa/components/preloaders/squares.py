import os
from ...helpers import DIV

html = DIV(
    DIV(
        DIV(
            DIV(
                DIV(_class="phanterpwa_squares phanterpwa_squares_one"),
                DIV(_class="phanterpwa_squares phanterpwa_squares_two"),
                DIV(_class="phanterpwa_squares phanterpwa_squares_three"),
                _class="phanterpwa_squares_container"),
            _class='preloader-wrapper enabled'
        ),
        _class="phanterpwa-preloader-wrapper"),
    _class="phanterpwa-components-preloaders-squares"
)

html.sass_file(
    os.path.join(os.path.dirname(__file__), "squares.sass")
)
html.sass_vars = {
    "CONTAINERWIDTH": "200px",
    "CONTAINERHEIGHT": "200px",
    "COLOR1": "red",
    "COLOR2": "orange",
    "COLOR3": "yellow",
    "BORDERSIZE": "10px",
    "BORDERRADIUS": "10%",
}
