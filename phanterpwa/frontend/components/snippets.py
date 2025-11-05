import phanterpwa.frontend.helpers as helpers
import phanterpwa.frontend.preloaders as preloaders
from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = js_undefined = setTimeout = window = this = console =\
    localStorage = 0
__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")
SPAN = helpers.XmlConstructor.tagger("span")
I = helpers.XmlConstructor.tagger("i")
H2 = helpers.XmlConstructor.tagger("h2")
LABEL = helpers.XmlConstructor.tagger("label", False)

__pragma__('kwargs')


class Centralizer(helpers.XmlConstructor):
    def __init__(self, identifier, *content, **attributes):
        attributes["_id"] = "phanterpwa-snippet-{0}".format(identifier)
        if "_class" in attributes:
            attributes["_class"] = "{0}{1}".format(attributes["_class"], " phanterpwa-snippet-centralizer")
        else:
            attributes["_class"] = "phanterpwa-snippet-centralizer"
        self._default_height = attributes.get("default_height", 20)
        if "_style" not in attributes:
            attributes["_style"] = "height:{0}px; min-height: {0}px;".format(self._default_height)

        self._centralizer_html = DIV(
            DIV(
                DIV(
                    DIV(
                        *content,
                        _class="phanterpwa-centralizer-center"
                    ),
                    _class="phanterpwa-centralizer-horizontal"

                ),
                _class="phanterpwa-centralizer-vertical"
            ),
            _class="phanterpwa-centralizer-wrapper"
        )

        helpers.XmlConstructor.__init__(self, 'div', False, self._centralizer_html, **attributes)

    def append(self, value):
        self._centralizer_html.append(value)

    def insert(self, pos, value):
        self._centralizer_html.insert(pos, value)


class PromoOption(helpers.XmlConstructor):
    def __init__(self, identifier, icon, title, description=None, **attributes):
        attributes["_id"] = "phanterpwa-snippet-{0}".format(identifier)
        if "_class" in attributes:
            attributes["_class"] = "{0}{1}".format(attributes["_class"], " phanterpwa-snippet-promooption link p-col w1p100")
        else:
            attributes["_class"] = "phanterpwa-snippet-promooption link p-col w1p100"
        html = DIV(
            DIV(
                icon,
                H2(title, _class="promo-title"),
                _class="promo-icon_and_title"
            ),
            **{"_class": "promo-container"}
        )
        if isinstance(description, helpers.XmlConstructor):
            html.append(DIV(description, _class='promo-content'))
        elif not (description is None or description == ""):
            html.append(DIV(description, _class='promo-content'))
        tag = "div"
        if "_href" in attributes:
            tag = "a"
        helpers.XmlConstructor.__init__(self, tag, False, html, **attributes)


class ICombine(helpers.XmlConstructor):
    def __init__(self, identifier, icon1, icon2,  **attributes):
        attributes["_id"] = "phanterpwa-snippet-{0}".format(identifier)
        if "_class" in attributes:
            attributes["_class"] = "{0}{1}".format(attributes["_class"], " phanterpwa-snippet-icombine")
        else:
            attributes["_class"] = "phanterpwa-snippet-icombine"
        if (isinstance(icon1, I) and isinstance(icon2, I)):
            html = DIV(
                SPAN(icon1, _class="icombine-container-first"),
                SPAN(icon2, _class="icombine-container-last"),
                **{"_class": "icombine-container"}
            )
        else:
            html = DIV(
                "",
                **{"_class": "icombine-container"}
            )
            if window.PhanterPWA.DEBUG:
                console.erro("The icon1 and icon2 must be I instance")
        tag = "div"
        if "_href" in attributes:
            tag = "a"
        helpers.XmlConstructor.__init__(self, tag, False, html, **attributes)


class TogglePanel(helpers.XmlConstructor):
    def __init__(self, *args, **attributes):
        _id = attributes.get('_id', None)
        if _id is None:
            self._namespace = "toggle_panel_{}".format(window.PhanterPWA.get_id())
        else:
            self._namespace = "{}_{}".format(str(_id), window.PhanterPWA.get_id())
        _class = attributes.get("_class")
        _class_wrapper = "phanterpwa-snippet-toggle_panel-wrapper"
        if _class is None:
            attributes['_class'] = "phanterpwa-snippet-toggle_panel"
        else:
            attributes['_class'] = "{0} phanterpwa-snippet-toggle_panel".format(_class)
        toggle_show = attributes.get("toggle_show", True)
        toggle_text_show = attributes.get("toggle_text_show")
        if toggle_text_show is None:
            toggle_text_show = "SHOW"
        toggle_text_hidden = attributes.get("toggle_text_hidden")
        if toggle_text_hidden is None:
            toggle_text_hidden = "HIDDEN"
        toggle_text = toggle_text_hidden
        if not toggle_show:
            _class_wrapper = "{0}_{1}".format(_class_wrapper, "snippet-toggle_panel-hidden")
            toggle_text = toggle_text_hidden
        wrapper_html = DIV(
            DIV(*args, _class="phanterpwa-snippet-toggle_panel-content"),
            DIV(
                DIV(_class="phanterpwa-snippet-toggle_panel-separador"),
                DIV(toggle_text, _class="phanterpwa-snippet-toggle_panel-text"),
                DIV(I(_class="fas fa-chevron-circle-up"), _class="phanterpwa-snippet-toggle_panel-icon"),
                _class="phanterpwa-snippet-toggle_panel-toggle_button link",
                **{"_data-target": self._namespace}
            ),
            _id=self._namespace,
            _class=_class_wrapper
        )
        helpers.XmlConstructor.__init__(self, "div", False, wrapper_html, **attributes)


class Panel(helpers.XmlConstructor):
    def __init__(self, *args, **attributes):
        _id = attributes.get('_id', None)
        if _id is None:
            self._namespace = "panel_{}".format(window.PhanterPWA.get_id())
        else:
            self._namespace = "{}_{}".format(str(_id), window.PhanterPWA.get_id())
        _class = attributes.get("_class")
        _class_wrapper = "phanterpwa-snippet-panel-wrapper"
        _loading = attributes.get("loading", True)
        _icons_button = attributes.get("icons_button", [])
        _label = attributes.get("label", "")
        _header = attributes.get("header", "")
        _footer = attributes.get("footer", "")
        html = []
        if _class is None:
            attributes['_class'] = "phanterpwa-snippet-panel"
        else:
            attributes['_class'] = "{0} phanterpwa-snippet-panel".format(_class)
        if _loading:
            _class_wrapper = "{0} {1}".format(_class_wrapper, "snippets-panel-loading")
        has_icons_button = False
        if isinstance(_icons_button, list):
            if len(_icons_button) > 0:
                has_icons_button = True
                _class_wrapper = "{0} {1}".format(_class_wrapper, "snippets-panel-has_icon_buttons")
        if not(_label is js_undefined or _label is None or _label is ""):
            _label = DIV(
                DIV(LABEL(_label, _for="#{}".format(self._namespace)), _class="phanterpwa-snippet-panel-label-content"),
                DIV(preloaders.indefined_text, _class="phanterpwa-snippet-panel-label-preloader"),
                _class="phanterpwa-snippet-panel-label"
            )
            if has_icons_button:
                _label.append(
                    DIV(
                        I(_class="fas fa-bars"),
                        _id="{}_{}".format(self._namespace, "menu_button"),
                        _class="icon_button phanterpwa-snippet-panel-menu_button",
                        **{"_data-target": self._namespace}
                    )
                )
            _class_wrapper = "{0} {1}".format(_class_wrapper, "snippets-panel-has_label")
            html.append(_label)
        elif has_icons_button:
            _label = DIV(
                DIV(
                    I(_class="fas fa-bars"),
                    _id="{}_{}".format(self._namespace, "menu_button"),
                    _class="icon_button phanterpwa-snippet-panel-menu_button",
                    **{"_data-target": self._namespace}
                ),
                _class="phanterpwa-snippet-panel-label"
            )
        html_content = DIV(_class="phanterpwa-snippet-panel-content")
        if not(_header is js_undefined or _header is None or _header is ""):
            html_content.append(
                DIV(
                    DIV(_header, _class="phanterpwa-snippet-panel-container-header-content"),
                    DIV(preloaders.discs, _class="phanterpwa-snippet-panel-container-header-preloader"),

                    _class="phanterpwa-snippet-panel-container-header"
                )
            )
        html_content.append(DIV(*args, _class="phanterpwa-snippet-panel-container-content"))
        html_content.append(DIV(preloaders.android, _class="phanterpwa-snippet-panel-container-preloader"))

        if has_icons_button:
            xml_icons = DIV(_class="phanterpwa-snippet-panel-icon_buttons-container")
            for x in _icons_button:
                xml_icons.append(DIV(DIV(x, _class="phanterpwa-snippet-panel-icon_button"), DIV(preloaders.indefined_text, _class="phanterpwa-snippet-panel-icon_buttons-preloader", _style="width:40px;")))
            html_content.append(xml_icons)
        html.append(html_content)
        if not(_footer is js_undefined or _footer is None or _footer is ""):
            html.append(
                DIV(
                    DIV(_footer, _class="phanterpwa-snippet-panel-container-footer-content"),
                    DIV(preloaders.discs, _class="phanterpwa-snippet-panel-container-footer-preloader"),
                    _class="phanterpwa-snippet-panel-container-footer"
                )
            )
        wrapper_html = DIV(
            *html,
            _id=self._namespace,
            _class=_class_wrapper
        )
        helpers.XmlConstructor.__init__(self, "div", False, wrapper_html, **attributes)


__pragma__('nokwargs')
