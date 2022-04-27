from core import projectConfig as CONFIG
from phanterpwa.helpers import (
    DIV,
    A,
    I,
    HTML,
    HEAD,
    BODY,
    META,
    TITLE,
    NAV,
    UL,
    LI,
    MAIN,
    FOOTER,
    SPAN,
    XML,
    H4,
    LINK
)
from .extends.svg_logo import html as SVG_LOGO
from .extends.javascript_head import html as JAVASCRIPT_HEAD
from .extends.css_head import html as CSS_HEAD
from .extends.favicons import html as FAVICONS
from .extends.captcha_preload import PRELOADER

app_version = CONFIG['PROJECT']['version']
app_name = CONFIG['PROJECT']['name']

html = HTML(
    HEAD(
        TITLE(app_name),
        META(_charset="utf-8"),
        META(
            _name="viewport",
            _content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
        ),
        META(_name="aplication-name", _content="Flask, Nginx, Cordova"),
        META(_name="aplication-version", _content=app_version),
        META(_name="msapplication-tap-highlight", _content="no"),
        # LINK(_rel="manifest", _href="/static/{0}/json/manifest.json".format(app_version)),
        CSS_HEAD,
        JAVASCRIPT_HEAD,
        FAVICONS
    ),
    BODY(
        DIV(_id="layout-top_slide-container"),
        NAV(
            DIV(
                DIV(
                    _id="layout-main_button-container",
                    _class="e-float_left"
                ),
                DIV(
                    DIV(
                        XML(SVG_LOGO),
                        _class="logo-svg"
                    ),
                    _class="p-logo link"
                ),
                _class="nav-wrapper"
            ),
            _class="main-nav"
        ),
        DIV(
            DIV(
                _id="layout-left_bar-container"
            ),
            MAIN(
                DIV(
                    PRELOADER,
                    _style="width:100%; text-align: center; padding-top: 100px;"
                ),
                _id="main-container"
            ),
            _class="main-and-left_bar"
        ),
        DIV(
            _id="modal-container"),
        FOOTER(
            DIV(
                _id="main-progress-bar-container",
                _class="main-progress-bar-container"
            ),
            DIV(
                DIV(_class="row"),
                _class='container'
            ),
            DIV(
                DIV(
                    A(
                        "Conexão Didata © 2011-", SPAN("2020", _id="conexao_year"),
                        _class="copyright",
                        _href="https://www.conexaodidata.com.br",
                        _target="blank"
                    ),
                    A(
                        "PhanterJR",
                        _class="e-float_right",
                        _href="https://phanterjr.conexaodidata.com.br",
                        _target="blank"
                    ),
                    _class="phanterpwa-container"
                ),
                _class="footer-copyright grey darken-3"
            ),
            _class="page-footer main-footer grey darken-4"
        ),
    ),
    _lang="pt-BR"
)
