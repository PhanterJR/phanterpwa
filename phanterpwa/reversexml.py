# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from html.entities import name2codepoint
from .xmlconstructor import XmlConstructor
from .helpers import CONCATENATE, XML, XCOMMENT
import json


class _Tag(XmlConstructor):
    def __init__(self, tag, void, is_closed):
        XmlConstructor.__init__(self, tag, void)
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
    def __init__(self, strhtml, filter_empty_content=False, filter_comments=True):
        self.void_tags = ["br", "area", "base", "col", "embed", "hr", "img",
            "input", "link", "meta", "param", "source", "track", "wbr"]
        self.strhtml = strhtml
        self.opened_el = []
        CONCATENATE.__init__(self, "")
        HTMLParser.__init__(self)
        self.content = []
        self.filter_empty_content = filter_empty_content
        self.HTMLdoctypedeclaration = ""
        self.feed(strhtml)

    def handle_starttag(self, tag, attrs):
        attr_tag = {}
        for attr in attrs:
            attr_tag["_%s" % attr[0]] = True if attr[1] is None else attr[1]
        el = _Tag(tag, True if tag in self.void_tags else False, False)
        el.attributes = attr_tag
        if all([tag == "html", self.HTMLdoctypedeclaration, self.HTMLdoctypedeclaration != "<!DOCTYPE html>"]):
            el.before_xml=self.HTMLdoctypedeclaration
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
        if tag not in self.void_tags:
            last_el = self.opened_el[-1]
            if not last_el.is_closed:
                last_el.is_closed = True
                self.opened_el.pop(-1)

    def handle_data(self, data):
        just_data = set([" ", "\n", "\t", "\r"])
        set_data = set(data)
        if self.opened_el:
            last_el = self.opened_el[-1]
            if not last_el.is_closed:
                content = list(last_el.content)
                if (set_data.union(just_data) == just_data):
                    if not self.filter_empty_content:
                        content.append(data)
                else:
                    content.append(data)
                last_el.content = content
        else:
            if set_data.union(just_data) == just_data:
                if not self.filter_empty_content:
                    self.append(data)
            else:
                self.append(data)

    def handle_comment(self, data):
        if self.opened_el:
            last_el = self.opened_el[-1]
            if not last_el.is_closed:
                content = list(last_el.content)
                content.append(XCOMMENT(data))
                last_el.content = content
        else:
            self.append(XCOMMENT(data))


    def handle_decl(self, data):
        self.HTMLdoctypedeclaration = "<!%s>" %data.strip()
