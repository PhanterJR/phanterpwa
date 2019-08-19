import os
from ...helpers import DIV

PRELOADER = DIV(
    DIV(
        DIV(
            DIV(
                DIV(
                    DIV(
                        DIV(
                            _class='phanterpwa_circle'
                        ),
                        _class='phanterpwa_circle_clipper left'
                    ),
                    DIV(
                        DIV(
                            _class='phanterpwa_circle'
                        ),
                        _class='phanterpwa_gap-patch'
                    ),
                    DIV(
                        DIV(
                            _class='phanterpwa_circle'
                        ),
                        _class='phanterpwa_circle_clipper right'
                    ),
                    _class='spinner-layer spinner-one'
                ),
                DIV(
                    DIV(
                        DIV(
                            _class='phanterpwa_circle'
                        ),
                        _class='phanterpwa_circle_clipper left'
                    ),
                    DIV(
                        DIV(
                            _class='phanterpwa_circle'
                        ),
                        _class='phanterpwa_gap-patch'
                    ),
                    DIV(
                        DIV(
                            _class='phanterpwa_circle'
                        ),
                        _class='phanterpwa_circle_clipper right'
                    ),
                    _class='spinner-layer spinner-two'
                ),
                DIV(
                    DIV(
                        DIV(
                            _class='phanterpwa_circle'
                        ),
                        _class='phanterpwa_circle_clipper left'
                    ),
                    DIV(
                        DIV(
                            _class='phanterpwa_circle'
                        ),
                        _class='phanterpwa_gap-patch'
                    ),
                    DIV(
                        DIV(
                            _class='phanterpwa_circle'
                        ),
                        _class='phanterpwa_circle_clipper right'
                    ),
                    _class='spinner-layer spinner-three'
                ),
                DIV(
                    DIV(
                        DIV(
                            _class='phanterpwa_circle'
                        ),
                        _class='phanterpwa_circle_clipper left'
                    ),
                    DIV(
                        DIV(
                            _class='phanterpwa_circle'
                        ),
                        _class='phanterpwa_gap-patch'
                    ),
                    DIV(
                        DIV(
                            _class='phanterpwa_circle'
                        ),
                        _class='phanterpwa_circle_clipper right'
                    ),
                    _class='spinner-layer spinner-four'
                ),
                _class='phanterpwa_android'
            ),
            _class='preloader-wrapper enabled'
        ),
        _class="preload-wrapper"),
    _class="phanterpwa-components-preloaders-android"
)

PRELOADER.sass_file(
    os.path.join(os.path.dirname(__file__), "android.sass")
)
PRELOADER.sass_vars = {
    'STROKEWIDTH': '10px',
    'CONTAINERWIDTH': '200px',
    'COLOR1': 'blue',
    'COLOR2': 'red',
    'COLOR3': '#f4b400',
    'COLOR4': 'green',
}
