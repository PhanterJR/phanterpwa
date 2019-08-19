import os
from ...helpers import DIV

PRELOADER = DIV(
    DIV(
        DIV(
            DIV(
                DIV(_class="phanterpwa_explosion phanterpwa_explosion_one"),
                DIV(_class="phanterpwa_explosion phanterpwa_explosion_two"),
                DIV(_class="phanterpwa_explosion phanterpwa_explosion_three"),
                DIV(_class="phanterpwa_explosion phanterpwa_explosion_four"),
                DIV(_class="phanterpwa_explosion phanterpwa_explosion_five"),
                DIV(_class="phanterpwa_explosion phanterpwa_explosion_six"),
                DIV(_class="phanterpwa_explosion phanterpwa_explosion_seven"),
                DIV(_class="phanterpwa_explosion phanterpwa_explosion_eight"),
                DIV(_class="phanterpwa_explosion phanterpwa_explosion_big"),
                _class="phanterpwa_explosion_container"
            ),
            _class='preloader-wrapper enabled'
        ),
        _class="phanterpwa-preloader-wrapper"),
    _class="phanterpwa-components-preloaders-explosion"
)

PRELOADER.sass_file(
    os.path.join(os.path.dirname(__file__), "explosion.sass")
)
