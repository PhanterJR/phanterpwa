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

discs = DIV(
    DIV(
        DIV(

            DIV(_class="phanterpwa_discs_one phanterpwa_discs"),
            DIV(_class="phanterpwa_discs_two phanterpwa_discs"),
            DIV(_class="phanterpwa_discs_three phanterpwa_discs"),
            DIV(_class="phanterpwa_discs_four phanterpwa_discs"),
            DIV(_class="phanterpwa_discs_five phanterpwa_discs"),

            _class="phanterpwa_discs_container"
        ),
        _class="preloader-wrapper enabled"
    ),
    _class="phanterpwa-components-preloaders-discs"
)

explosion = DIV(
    DIV(_class="left"),
    DIV(
        DIV(
            DIV(_class="phanterpwa_explosion_one phanterpwa_explosion"),
            DIV(_class="phanterpwa_explosion_two phanterpwa_explosion"),
            DIV(_class="phanterpwa_explosion_three phanterpwa_explosion"),
            DIV(_class="phanterpwa_explosion_four phanterpwa_explosion"),
            DIV(_class="phanterpwa_explosion_five phanterpwa_explosion"),
            DIV(_class="phanterpwa_explosion_six phanterpwa_explosion"),
            DIV(_class="phanterpwa_explosion_seven phanterpwa_explosion"),
            DIV(_class="phanterpwa_explosion_eight phanterpwa_explosion"),
            DIV(_class="phanterpwa_explosion_big phanterpwa_explosion"),
            _class="phanterpwa_explosion_container"
        ),
        _class="preloader-wrapper enabled"
    ),
    DIV(_class="right"),
    _class="phanterpwa-components-preloaders-explosion"
)

indefined_text = DIV(
    DIV(
        DIV(
            DIV(_class="indefined_text"),
            _class="preloader-wrapper enabled"
        ),
        _class="phanterpwa-preloader-wrapper"
    ),
    _class="phanterpwa-components-preloaders-indefined_text"
)

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


square = DIV(
    DIV(
        DIV(
            DIV(
                _class="phanterpwa_square"
            ),
            _class="phanterpwa_square_container"
        ),
        _class="preloader-wrapper enabled"
    ),
    _class="phanterpwa-components-preloaders-square"
)

squares = DIV(
    DIV(_class="left"),
    DIV(
        DIV(

            DIV(_class="phanterpwa_squares_one phanterpwa_squares"),
            DIV(_class="phanterpwa_squares_two phanterpwa_squares"),
            DIV(_class="phanterpwa_squares_three phanterpwa_squares"),

            _class="phanterpwa_squares_container"
        ),
        _class="preloader-wrapper enabled"
    ),
    DIV(_class="right"),
    _class="phanterpwa-components-preloaders-squares"
)
