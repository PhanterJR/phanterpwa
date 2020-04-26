import phanterpwa.apptools.helpers as helpers
from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = js_undefined = setTimeout = window = this = console =\
    localStorage = 0
__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")
I = helpers.XmlConstructor.tagger("i")


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


__pragma__('nokwargs')