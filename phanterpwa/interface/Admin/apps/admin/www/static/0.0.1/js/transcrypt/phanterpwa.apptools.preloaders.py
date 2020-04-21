from phanterpwa.apptools import helpers

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
