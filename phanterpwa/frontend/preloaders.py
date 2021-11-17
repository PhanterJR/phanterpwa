from phanterpwa.frontend import helpers

DIV = helpers.XmlConstructor.tagger("div", False)

android = DIV(
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
).jquery()


run_points = DIV(
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