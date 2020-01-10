from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")


__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = \
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')


__pragma__('kwargs')


class XmlConstructor():
    def __init__(self, tag, singleton, *content, **attributes):
        self.tag = tag
        self.singleton = singleton
        self.content = content
        self.attributes = attributes

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        self._tag = tag

    @property
    def singleton(self):
        return self._singleton

    def append(self, value):
        self.content.append(value)

    def insert(self, pos, value):
        self.content.insert(pos, value)

    @singleton.setter
    def singleton(self, singleton):
        if isinstance(singleton, bool):
            self._singleton = singleton
        else:
            raise TypeError("The singleton must be bool, given: {0}".format(str(singleton)))

    def xml(self):
        if (self.singleton is True):
            self.el = jQuery("<{0}>".format(self.tag))
        else:
            self.el = jQuery("<{0}></{0}>".format(str(self.tag)))
            for c in self.content:
                if isinstance(c, str):
                    self.el.append(jQuery("<div/>").text(c).html())
                elif isinstance(c, XmlConstructor):
                    self.el.append(c.jquery())
                else:
                    self.el.append(c)
        for t in self.attributes.keys():
            if t.startswith("_"):
                if self.attributes[t] is not None and self.attributes[t] is not js_undefined:
                    self.el.attr(t[1:], self.attributes[t])

        return self.el[0].outerHTML

    def __str__(self):
        return self.xml()

    def jquery(self):
        self.xml()
        return self.el

    @staticmethod
    def tagger(tag, singleton=False):
        return lambda *content, **attributes: XmlConstructor(tag, singleton, *content, **attributes)


class I18N(XmlConstructor):
    def __init__(self, content, **attributes):
        str_content = "{0}".format(content)
        attributes["_phanterpwa-i18n"] = str_content
        XmlConstructor.__init__(self, 'span', False, str_content, **attributes)


class DOMXmlWriter():
    def __init__(self, **parameters):
        self.escape = False
        self.after_write = None
        self.xml = ""
        self.target = None
        self.parameters = parameters
        if "after_write" in parameters:
            self.after_write = parameters['after_write']

    def html(self, target, xml):
        self.target = jQuery(target)
        if self.target.length == 0:
            console.error("The target element don't exists!")
        else:
            if isinstance(xml, XmlConstructor):
                self.target.html(xml.jquery())
            else:
                self.target.html(xml)
            if "after_write" in self.parameters:
                self.parameters['after_write'](self.target)

    def text(self, target, xml):
        self.target = jQuery(target)
        if self.target.length == 0:
            console.error("The target element don't exists!")
        else:
            if isinstance(xml, XmlConstructor):
                self.target.text(xml.xml())
            else:
                self.target.text(xml)
            if "after_write" in self.parameters:
                self.parameters['after_write'](self.target)

    def append(self, target, xml):
        self.target = jQuery(target)
        if self.target.length == 0:
            console.error("The target element don't exists!")
        else:
            if isinstance(xml, XmlConstructor):
                self.target.append(xml.jquery())
            else:
                self.target.append(xml)
            if "after_write" in self.parameters:
                self.parameters['after_write'](self.target)

    def prepend(self, target, xml):
        self.target = jQuery(target)
        if self.target.length == 0:
            console.error("The target element don't exists!")
        else:
            if isinstance(xml, XmlConstructor):
                self.target.prepend(xml.jquery())
            else:
                self.target.prepend(xml)
            if "after_write" in self.parameters:
                self.parameters['after_write'](self.target)


class XML(XmlConstructor):
    def __init__(self, *content):
        XmlConstructor.__init__(self, '', False, *content)

    def xml(self):
        html = ""
        for c in self.content:
            if isinstance(c, str):
                html += c
            elif isinstance(c, XmlConstructor):
                html += c.xml()
            else:
                html += c
        return html

    def jquery(self):
        html = self.xml()
        return html


class CONCATENATE(XmlConstructor):
    def __init__(self, *content):
        XmlConstructor.__init__(self, '', False, *content)

    def xml(self):
        html = ""
        for c in self.content:
            if isinstance(c, str):
                html += jQuery("<div/>").text(c).html()
            elif isinstance(c, XmlConstructor):
                html += c.xml()
            else:
                html += c
        return html

    def jquery(self):
        html = self.xml()
        return jQuery(html)


__pragma__('nokwargs')
