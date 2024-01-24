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
        self.__jquery_object = ""

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
            self.__jquery_object = jQuery("<{0}>".format(self.tag))
        else:
            self.__jquery_object = jQuery("<{0}></{0}>".format(str(self.tag)))
            for c in self.content:
                if isinstance(c, str):
                    self.__jquery_object.append(jQuery("<div/>").text(c).html())
                elif isinstance(c, XmlConstructor):
                    self.__jquery_object.append(c.jquery())
                else:
                    self.__jquery_object.append(c)
        for t in self.attributes.keys():
            if t.startswith("_"):
                if self.attributes[t] is not None and self.attributes[t] is not js_undefined:
                    self.__jquery_object.attr(t[1:], self.attributes[t])

        return self.__jquery_object[0].outerHTML

    def __str__(self):
        return self.xml()

    def jquery(self):
        self.xml()
        return self.__jquery_object

    def html_to(self, selector):
        self.xml()
        el = jQuery(selector).html(self.__jquery_object)
        if window.PhanterPWA is not js_undefined:
            window.PhanterPWA.reload_events(selector=self.__jquery_object)
            window.PhanterPWA.I18N.DOMTranslate(self.__jquery_object)
        return el

    def text_to(self, selector):
        self.xml()
        return jQuery(selector).text(self.__jquery_object)

    def append_to(self, selector):
        self.xml()
        el = jQuery(selector).append(self.__jquery_object)
        if window.PhanterPWA is not js_undefined:
            window.PhanterPWA.reload_events(selector=self.__jquery_object)
            window.PhanterPWA.I18N.DOMTranslate(self.__jquery_object)
        return el

    def insert_to(self, selector, position=0):
        self.xml()
        target = jQuery(selector)
        last_index = target.children().length
        if position < 0:
            position = max(0, last_index + 1 + position)
        target.append(self.__jquery_object)
        if position < last_index:
            target.children().eq(position).before(target.children().last())
        el = target
        if window.PhanterPWA is not js_undefined:
            window.PhanterPWA.reload_events(selector=self.__jquery_object)
            window.PhanterPWA.I18N.DOMTranslate(self.__jquery_object)
        return el

    @staticmethod
    def tagger(tag, singleton=False):
        return lambda *content, **attributes: XmlConstructor(tag, singleton, *content, **attributes)


class I18N(XmlConstructor):
    def __init__(self, *content, **attributes):
        for x in content:
            if not isinstance(x, str):
                raise ValueError("The I18N content must be string type")

        str_content = "".join(content)
        attributes["_phanterpwa-i18n"] = str_content
        sanitize = attributes.get("sanitize", True)
        if sanitize is False:
            attributes["_phanterpwa-i18n-sanitize"] = False
        XmlConstructor.__init__(self, 'span', False, str_content, **attributes)


class XSECTION(XmlConstructor):
    def __init__(self, *content, **parameters):
        DIV = XmlConstructor.tagger("div")
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-xsection-container")
        else:
            parameters["_class"] = "phanterpwa-xsection-container"
        self.__child_html = DIV(
            *content,
            _class="phanterpwa-xsection"
        )
        XmlConstructor.__init__(self, 'div', False, self.__child_html, **parameters)

    def append(self, value):
        self.__child_html.content.append(value)

    def insert(self, pos, value):
        self.__child_html.content.insert(pos, value)


class XTABLE(XmlConstructor):
    def __init__(self, *content, **parameters):
        TABLE = XmlConstructor.tagger("table")
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-xtable-container")
        else:
            parameters["_class"] = "phanterpwa-xtable-container"
        self.__child_html = TABLE(
            *content,
            _class="phanterpwa-xtable p-row"
        )
        XmlConstructor.__init__(self, 'div', False, self.__child_html, **parameters)

    def append(self, value):
        self.__child_html.content.append(value)

    def insert(self, pos, value):
        self.__child_html.content.insert(pos, value)


class XTRH(XmlConstructor):
    def __init__(self, *content, **parameters):
        TH = XmlConstructor.tagger("th")
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-xtable-xtrh")
        else:
            parameters["_class"] = "phanterpwa-xtable-xtrh"
        self.__child_html = CONCATENATE()
        for x in content:
            self.__child_html.append(TH(x, _class="phanterpwa-xtable-xtrh-th"))
        XmlConstructor.__init__(self, 'tr', False, self.__child_html, **parameters)

    def append(self, value):
        TH = XmlConstructor.tagger("th")
        self.__child_html.content.append(TH(value, _class="phanterpwa-xtable-xtrh-th"))

    def insert(self, pos, value):
        TH = XmlConstructor.tagger("th")
        self.__child_html.content.insert(pos, TH(value, _class="phanterpwa-xtable-xtrh-th"))


class XTRD(XmlConstructor):
    def __init__(self, *content, **parameters):
        self.__dropable = parameters.get("drag_and_drop", True)
        if self.__dropable:
            parameters["_draggable"] = "true"
        self._drop_if = parameters.get("drop_if", None)
        TD = XmlConstructor.tagger("td")
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-xtable-xtrd")
        else:
            parameters["_class"] = "phanterpwa-xtable-xtrd"
        self.__child_html = CONCATENATE()
        for x in content:
            self.__child_html.append(TD(x, _class="phanterpwa-xtable-xtrd-td"))
        XmlConstructor.__init__(self, 'tr', False, self.__child_html, **parameters)

    def __ondragstart(self, el):
        window.PhanterPWA.drag = jQuery(el)[0].outerHTML

    def __ondrop(self, el):
        if callable(self._drop_if):
            if self._drop_if(el):
                jQuery(el).insertAfter(window.PhanterPWA.drag)
        else:
            jQuery(el).insertAfter(window.PhanterPWA.drag)

    def append(self, value):
        TD = XmlConstructor.tagger("td")
        self.__child_html.content.append(TD(value, _class="phanterpwa-xtable-xtrd-td"))

    def insert(self, pos, value):
        TD = XmlConstructor.tagger("td")
        self.__child_html.content.insert(pos, TD(value, _class="phanterpwa-xtable-xtrd-td"))


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
        self.__jquery_object = html
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
        self.__jquery_object = jQuery(html)
        return html

    def jquery(self):
        html = self.xml()
        return jQuery(html)


class XTAGGER(XmlConstructor):
    def __init__(self, field_name, *content, **parameters):
        DIV = XmlConstructor.tagger("div")
        STRONG = XmlConstructor.tagger("strong")
        SPAN = XmlConstructor.tagger("span")
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-tagger-container")
        else:
            parameters["_class"] = "phanterpwa-tagger-container"
        self.__child_html = DIV(
            STRONG(field_name),
            SPAN(*content),
            _class="phanterpwa-tagger e-tagger-wrapper"
        )
        XmlConstructor.__init__(self, 'div', False, self.__child_html, **parameters)

    def append(self, value):
        self.__child_html.content.append(value)

    def insert(self, pos, value):
        self.__child_html.content.insert(pos, value)



__pragma__('nokwargs')
