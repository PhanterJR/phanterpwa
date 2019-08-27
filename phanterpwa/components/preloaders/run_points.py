import os
from ...helpers import DIV

PRELOADER = DIV(
    DIV(
        DIV(
            DIV(
                DIV(
                    DIV(_class="phanterpwa_run_points_one"),
                    _class="phanterpwa_run_points phanterpwa_run_points_one_content"),
                DIV(
                    DIV(_class="phanterpwa_run_points_two"),
                    _class="phanterpwa_run_points phanterpwa_run_points_two_content"),
                DIV(
                    DIV(_class="phanterpwa_run_points_three"),
                    _class="phanterpwa_run_points phanterpwa_run_points_three_content"),
                DIV(
                    DIV(_class="phanterpwa_run_points_four"),
                    _class="phanterpwa_run_points phanterpwa_run_points_four_content"),
                DIV(
                    DIV(_class="phanterpwa_run_points_five"),
                    _class="phanterpwa_run_points phanterpwa_run_points_five_content"),
                _class="pwa_run_points_container"
            ),
            _class='preloader-wrapper enabled'
        ),
        _class="phanterpwa-preloader-wrapper"),
    _class="phanterpwa-components-preloaders-run_points"
)

PRELOADER.sass_file(
    os.path.join(os.path.dirname(__file__), "run_points.sass")
)
PRELOADER.sass_vars = {
    'COLOR1': 'red',
    'COLOR2': 'blue',
    'COLOR3': 'yellow',
    'COLOR4': 'pink',
    'COLOR5': 'green',
    'BORDERRADIUS': '100%',
    'CONTAINERWIDTH': '100px'
}
