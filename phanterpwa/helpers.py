# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from html.entities import name2codepoint
from .xmlconstructor import XmlConstructor
from .xss import XssCleaner


class CONCATENATE(XmlConstructor):
    def __init__(self, *content):
        XmlConstructor.__init__(self, "", False, *content)


class XML(XmlConstructor, XssCleaner):
    def __init__(self,
            content,
            sanitize=False,
            permitted_tags=[
                'a',
                'b',
                'blockquote',
                'br/',
                'i',
                'li',
                'ol',
                'ul',
                'p',
                'cite',
                'code',
                'pre',
                'img/',
            ],
            allowed_attributes={
                'a': ['href', 'title'],
                'img': ['src', 'alt'],
                'blockquote': ['type']
            }):
        XmlConstructor.__init__(self, "", False, content)
        XssCleaner.__init__(self)
        self.sanitize = sanitize
        self.permitted_tags = permitted_tags
        self.allowed_attributes = allowed_attributes
        self.strip_disallowed = False
        self._escape_string = False

    @property
    def xml_content(self):
        temp_xml_content = ""
        for x in self._content:
            if isinstance(x, XmlConstructor):
                temp_xml_content = "".join([temp_xml_content, x.xml()])
            else:
                temp_xml_content = "".join([temp_xml_content, x])
        self._xml_content = temp_xml_content
        return self._xml_content

    def xml(self):
        xml = ""
        if self.content:
            xml = self.xml_content
        if self.sanitize:
            return self.strip(xml)
        return xml


class SCRIPTMINIFY(XmlConstructor):
    def __init__(self, content, **attributes):
        list_string_content = content.split("\n")
        new_content = ""
        for x in list_string_content:
            new_content = " ".join([new_content, x.strip()])
            new_content = new_content.strip()
        XmlConstructor.__init__(self, "script", False, new_content, **attributes)


class VARIABLE(XmlConstructor):
    def __init__(self, variable_name):
        self._variable_name = variable_name
        XmlConstructor.__init__(self, "", False)

    @property
    def id(self):
        return self._variable_name

    @property
    def xml_content_for_humans(self):
        temp_xml_content = ""
        for x in self._content:
            if isinstance(x, XmlConstructor):
                x._ident_level = self._ident_level
                temp_xml_content = "".join([temp_xml_content, x.humanize()])
            else:
                space = "".join(["\n", " " * ((self._ident_level) * self._ident_size)])
                temp_xml_content = "".join([temp_xml_content, space, str(x)])

        self._xml_content_for_humans = temp_xml_content
        return self._xml_content_for_humans

    def humanize(self):
        human = ""
        space = " " * (self._ident_level * self._ident_size)
        if self.content and not self.singleton:
            human = "".join([self.tag_begin, self.xml_content_for_humans, space, self.tag_end])
        elif self.singleton:
            human = "".join([self.tag_begin])
        else:
            human = "".join([self.tag_begin, space, self.tag_end])
        return space + human

# void tags

class AREA(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "area", True, *content, **attributes)


class BASE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "base", True, *content, **attributes)


class COL(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "col", True, *content, **attributes)


class EMBED(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "embed", True, *content, **attributes)


class HR(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "hr", True, *content, **attributes)


class IMG(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "img", True, *content, **attributes)


class INPUT(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "input", True, *content, **attributes)


class LINK(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "link", True, *content, **attributes)


class META(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "meta", True, *content, **attributes)


class PARAM(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "param", True, *content, **attributes)


class SOURCE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "source", True, *content, **attributes)


class TRACK(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "track", True, *content, **attributes)


class WBR(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "wbr", True, *content, **attributes)


# normal tags


class BR(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "br", False, *content, **attributes)


class A(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "a", False, *content, **attributes)


class ABBR(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "abbr", False, *content, **attributes)


class ADDRESS(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "address", False, *content, **attributes)


class ARTICLE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "article", False, *content, **attributes)


class ASIDE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "aside", False, *content, **attributes)


class AUDIO(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "audio", False, *content, **attributes)


class B(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "b", False, *content, **attributes)


class BDI(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "bdi", False, *content, **attributes)


class BDO(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "bdo", False, *content, **attributes)


class BLOCKQUOTE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "blockquote", False, *content, **attributes)


class BODY(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "body", False, *content, **attributes)


class BUTTON(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "button", False, *content, **attributes)


class CANVAS(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "canvas", False, *content, **attributes)


class CAPTION(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "caption", False, *content, **attributes)


class CITE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "cite", False, *content, **attributes)


class CODE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "code", False, *content, **attributes)


class COLGROUP(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "colgroup", False, *content, **attributes)


class DATA(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "data", False, *content, **attributes)


class DATALIST(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "datalist", False, *content, **attributes)


class DD(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "dd", False, *content, **attributes)


class DEL(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "del", False, *content, **attributes)


class DETAILS(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "details", False, *content, **attributes)


class DFN(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "dfn", False, *content, **attributes)


class DIALOG(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "dialog", False, *content, **attributes)


class DIV(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "div", False, *content, **attributes)


class DL(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "dl", False, *content, **attributes)


class DT(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "dt", False, *content, **attributes)


class EM(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "em", False, *content, **attributes)


class FIELDSET(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "fieldset", False, *content, **attributes)


class FIGCAPTION(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "figcaption", False, *content, **attributes)


class FIGURE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "figure", False, *content, **attributes)


class FOOTER(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "footer", False, *content, **attributes)


class FORM(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "form", False, *content, **attributes)


class H1(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "h1", False, *content, **attributes)


class H2(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "h2", False, *content, **attributes)


class H3(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "h3", False, *content, **attributes)


class H4(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "h4", False, *content, **attributes)


class H5(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "h5", False, *content, **attributes)


class H6(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "h6", False, *content, **attributes)


class HEAD(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "head", False, *content, **attributes)


class HEADER(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "header", False, *content, **attributes)


class HTML(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "html", False, *content, **attributes)

    @property
    def tag_begin(self):
        if self._tag:
            if self.xml_attributes:
                self._tag_begin = "<!DOCTYPE html><%s %s>" % (self.tag, self.xml_attributes)
            else:
                self._tag_begin = "<!DOCTYPE html><%s>" % (self.tag)
        else:
            self._tag_begin = ""
        return self._tag_begin


class I(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "i", False, *content, **attributes)


class IFRAME(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "iframe", False, *content, **attributes)


class INS(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "ins", False, *content, **attributes)


class KBD(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "kbd", False, *content, **attributes)


class LABEL(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "label", False, *content, **attributes)


class LEGEND(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "legend", False, *content, **attributes)


class LI(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "li", False, *content, **attributes)


class MAIN(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "main", False, *content, **attributes)


class MAP(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "map", False, *content, **attributes)


class MARK(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "mark", False, *content, **attributes)


class METER(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "meter", False, *content, **attributes)


class NAV(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "nav", False, *content, **attributes)


class NOSCRIPT(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "noscript", False, *content, **attributes)


class OBJECT(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "object", False, *content, **attributes)


class OL(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "ol", False, *content, **attributes)


class OPTGROUP(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "optgroup", False, *content, **attributes)


class OPTION(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "option", False, *content, **attributes)


class OUTPUT(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "output", False, *content, **attributes)


class P(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "p", False, *content, **attributes)


class PICTURE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "picture", False, *content, **attributes)


class PRE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "pre", False, *content, **attributes)


class PROGRESS(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "progress", False, *content, **attributes)


class Q(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "q", False, *content, **attributes)


class RP(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "rp", False, *content, **attributes)


class RT(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "rt", False, *content, **attributes)


class RUBY(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "ruby", False, *content, **attributes)


class S(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "s", False, *content, **attributes)


class SAMP(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "samp", False, *content, **attributes)


class SCRIPT(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "script", False, *content, **attributes)


class SECTION(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "section", False, *content, **attributes)


class SELECT(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "select", False, *content, **attributes)


class SMALL(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "small", False, *content, **attributes)


class SPAN(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "span", False, *content, **attributes)


class STRONG(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "strong", False, *content, **attributes)


class STYLE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "style", False, *content, **attributes)


class SUB(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "sub", False, *content, **attributes)


class SUMMARY(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "summary", False, *content, **attributes)


class SUP(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "sup", False, *content, **attributes)


class SVG(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "svg", False, *content, **attributes)


class TABLE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "table", False, *content, **attributes)


class TBODY(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "tbody", False, *content, **attributes)


class TD(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "td", False, *content, **attributes)


class TEMPLATE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "template", False, *content, **attributes)


class TEXTAREA(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "textarea", False, *content, **attributes)


class TFOOT(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "tfoot", False, *content, **attributes)


class TH(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "th", False, *content, **attributes)


class THEAD(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "thead", False, *content, **attributes)


class TIME(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "time", False, *content, **attributes)


class TITLE(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "title", False, *content, **attributes)


class TR(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "tr", False, *content, **attributes)


class U(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "u", False, *content, **attributes)


class UL(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "ul", False, *content, **attributes)


class VAR(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "var", False, *content, **attributes)


class VIDEO(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "video", False, *content, **attributes)


class _Tag(XmlConstructor):
    def __init__(self, tag, singleton, is_closed):
        XmlConstructor.__init__(self, tag, singleton)
        self._is_closed = False

    @property
    def is_closed(self):
        return self._is_closed

    @is_closed.setter
    def is_closed(self, v):
        if self.singleton is True:
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
        el = _Tag(tag, True if tag in self.void_tags else False, False)
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
