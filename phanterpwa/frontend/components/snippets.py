import phanterpwa.frontend.helpers as helpers
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


__pragma__('kwargs')


class Centralizer(helpers.XmlConstructor):
    def __init__(self, identifier, *content, **attributes):
        attributes["_id"] = "phanterpwa-snippet-{0}".format(identifier)
        if "_class" in attributes:
            attributes["_class"] = "{0}{1}".format(attributes["_class"], " phanterpwa-snippet-centralizer")
        else:
            attributes["_class"] = "phanterpwa-snippet-centralizer"
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

__pragma__('nokwargs')
