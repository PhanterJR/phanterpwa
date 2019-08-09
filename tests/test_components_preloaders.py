# -*- coding: utf-8 -*-
import unittest
from phanterpwa.helpers import (
    # DIV,
    # IMG,
    # XML,
    # A,
    # TD,
    # SPAN,
    # CONCATENATE,
    # B,
    HTML,
    HEAD,
    BODY,
    SCRIPT,
    TITLE,
    META,
    STYLE,
    MAIN
)


SAMPLE_HTML = HTML(
    HEAD(
        TITLE(
            'Test Components Preloaders'
        ),
        META(
            _charset='utf-8'
        ),
        META(
            _name='viewport',
            _content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'
        ),
        META(
            _name='msapplication-tap-highlight',
            _content='no'
        ),
        SCRIPT(
            _src='/static/jquery.min.js'
        ),
        STYLE(
            "{{style}}"
        )
    ),
    BODY(
        MAIN(
            "{{content}}",
            _style="text-align: center;"
        ),
    ),
    _lang='pt-BR'
)


class TestHelpers(unittest.TestCase):
    def test1_android(self):
        from phanterpwa.components.preloaders import android
        instanceAndroid = android.html
        SAMPLE_HTML.html(
            formatter={'style': instanceAndroid.css(), 'content': instanceAndroid},
            file="test_components_preloaders_android.html"
        )

    def test2_square(self):
        from phanterpwa.components.preloaders import square
        instancesquare = square.html
        SAMPLE_HTML.html(
            formatter={'style': instancesquare.css(), 'content': instancesquare},
            file="test_components_preloaders_square.html"
        )

    def test3_squares(self):
        from phanterpwa.components.preloaders import squares
        instancesquares = squares.html
        SAMPLE_HTML.html(
            formatter={'style': instancesquares.css(), 'content': instancesquares},
            file="test_components_preloaders_squares.html"
        )

    def test4_explosion(self):
        from phanterpwa.components.preloaders import explosion
        instanceexplosion = explosion.html
        SAMPLE_HTML.html(
            formatter={'style': instanceexplosion.css(), 'content': instanceexplosion},
            file="test_components_preloaders_explosion.html"
        )

    def test5_run_points(self):
        from phanterpwa.components.preloaders import run_points
        instancerun_points = run_points.html
        SAMPLE_HTML.html(
            formatter={'style': instancerun_points.css(), 'content': instancerun_points},
            file="test_components_preloaders_run_points.html"
        )

    def test5_discs(self):
        from phanterpwa.components.preloaders import discs
        instancediscs = discs.html
        SAMPLE_HTML.html(
            formatter={'style': instancediscs.css(), 'content': instancediscs},
            file="test_components_preloaders_discs.html"
        )


if __name__ == '__main__':
    unittest.main()
