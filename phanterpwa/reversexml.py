# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from html.entities import name2codepoint
from .xmlconstructor import XmlConstructor
from .helpers import CONCATENATE


class _Tag(XmlConstructor):
    def __init__(self, tag, void, void_close, is_closed):
        XmlConstructor.__init__(self, tag, void, void_close)
        self._is_closed = False

    @property
    def is_closed(self):
        return self._is_closed

    @is_closed.setter
    def is_closed(self, v):
        if self.void is True:
            self._is_closed = True
        else:
            if isinstance(v, bool):
                self._is_closed = v
            else:
                raise TypeError("is_closed must be bool, given: %s" % type(v))


class HtmlToXmlConstructor(CONCATENATE, HTMLParser):
    def __init__(self, strhtml):
        self.void_tags = ["br", "area", "base", "col", "embed", "hr", "img",
            "input", "link", "meta", "param", "source", "track", "wbr"]
        self.strhtml = strhtml
        self.opened_el = []
        CONCATENATE.__init__(self, "")
        HTMLParser.__init__(self)
        self.content = []
        self.feed(strhtml)

    def handle_starttag(self, tag, attrs):
        attr_tag = {}
        for attr in attrs:
            attr_tag["_%s" % attr[0]] = True if attr[1] is None else attr[1]
        el = _Tag(tag, True if tag in self.void_tags else False, False, False)
        el.attributes = attr_tag
        if self.opened_el:
            last_el = self.opened_el[-1]
            if not last_el.is_closed:
                content = list(last_el.content)
                content.append(el)
                last_el.content = content
        else:
            self.append(el)
        if tag not in self.void_tags:
            self.opened_el.append(el)

    def handle_endtag(self, tag):
        last_el = self.opened_el[-1]
        if not last_el.is_closed:
            last_el.is_closed = True
            self.opened_el.pop(-1)

    def handle_data(self, data):
        if self.opened_el:
            last_el = self.opened_el[-1]
            if not last_el.is_closed:
                content = list(last_el.content)
                content.append(data)
                last_el.content = content
        else:
            self.append(data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)
