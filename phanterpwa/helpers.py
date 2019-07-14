# -*- coding: utf-8 -*-
from .xmlconstructor import XmlConstructor
from .xss import XssCleaner


class CONCATENATE(XmlConstructor):
    def __init__(self, *content):
        XmlConstructor.__init__(self, "", False, False, *content)
        self.alternative_tag = "concatenate"


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
        XmlConstructor.__init__(self, "", False, False, content)
        XssCleaner.__init__(self)
        self.alternative_tag = "xml"
        self.sanitize = sanitize
        self.permitted_tags = permitted_tags
        self.allowed_attributes = allowed_attributes
        self.strip_disallowed = False
        self._escape_string = False

    def xml(self):
        xml = ""
        if self.content:
            xml = self.xml_content
        if self.sanitize:
            xml = "".join([self.before_xml, xml, self.after_xml])
            return self.strip(xml)
        xml = "".join([self.before_xml, xml, self.after_xml])
        return xml


class SCRIPTMINIFY(XmlConstructor):
    def __init__(self, content, **attributes):
        list_string_content = content.split("\n")
        new_content = ""
        for x in list_string_content:
            new_content = " ".join([new_content, x.strip()])
            new_content = new_content.strip()
        XmlConstructor.__init__(self, "script", False, False, new_content, **attributes)


# html5 by default
class HTML(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "html", False, False, *content, **attributes)
        self.before_xml = "<!DOCTYPE html>"


# void tags
AREA = XmlConstructor.tagger("area", True, False)
BASE = XmlConstructor.tagger("base", True, False)
COL = XmlConstructor.tagger("col", True, False)
EMBED = XmlConstructor.tagger("embed", True, False)
HR = XmlConstructor.tagger("hr", True, False)
IMG = XmlConstructor.tagger("img", True, False)
INPUT = XmlConstructor.tagger("input", True, False)
LINK = XmlConstructor.tagger("link", True, False)
META = XmlConstructor.tagger("meta", True, False)
PARAM = XmlConstructor.tagger("param", True, False)
SOURCE = XmlConstructor.tagger("source", True, False)
TRACK = XmlConstructor.tagger("track", True, False)
WBR = XmlConstructor.tagger("wbr", True, False)
BR = XmlConstructor.tagger("br", True, False)
# normal tags
A = XmlConstructor.tagger("a", False, False)
ABBR = XmlConstructor.tagger("abbr", False, False)
ADDRESS = XmlConstructor.tagger("address", False, False)
ARTICLE = XmlConstructor.tagger("article", False, False)
ASIDE = XmlConstructor.tagger("aside", False, False)
AUDIO = XmlConstructor.tagger("audio", False, False)
B = XmlConstructor.tagger("b", False, False)
BDI = XmlConstructor.tagger("bdi", False, False)
BDO = XmlConstructor.tagger("bdo", False, False)
BLOCKQUOTE = XmlConstructor.tagger("blockquote", False, False)
BODY = XmlConstructor.tagger("body", False, False)
BUTTON = XmlConstructor.tagger("button", False, False)
CANVAS = XmlConstructor.tagger("canvas", False, False)
CAPTION = XmlConstructor.tagger("caption", False, False)
CITE = XmlConstructor.tagger("cite", False, False)
CODE = XmlConstructor.tagger("code", False, False)
COLGROUP = XmlConstructor.tagger("colgroup", False, False)
DATA = XmlConstructor.tagger("data", False, False)
DATALIST = XmlConstructor.tagger("datalist", False, False)
DD = XmlConstructor.tagger("dd", False, False)
DEL = XmlConstructor.tagger("del", False, False)
DETAILS = XmlConstructor.tagger("details", False, False)
DFN = XmlConstructor.tagger("dfn", False, False)
DIALOG = XmlConstructor.tagger("dialog", False, False)
DIV = XmlConstructor.tagger("div", False, False)
DL = XmlConstructor.tagger("dl", False, False)
DT = XmlConstructor.tagger("dt", False, False)
EM = XmlConstructor.tagger("em", False, False)
FIELDSET = XmlConstructor.tagger("fieldset", False, False)
FIGCAPTION = XmlConstructor.tagger("figcaption", False, False)
FIGURE = XmlConstructor.tagger("figure", False, False)
FOOTER = XmlConstructor.tagger("footer", False, False)
FORM = XmlConstructor.tagger("form", False, False)
H1 = XmlConstructor.tagger("h1", False, False)
H2 = XmlConstructor.tagger("h2", False, False)
H3 = XmlConstructor.tagger("h3", False, False)
H4 = XmlConstructor.tagger("h4", False, False)
H5 = XmlConstructor.tagger("h5", False, False)
H6 = XmlConstructor.tagger("h6", False, False)
HEAD = XmlConstructor.tagger("head", False, False)
HEADER = XmlConstructor.tagger("header", False, False)
I = XmlConstructor.tagger("i", False, False)
IFRAME = XmlConstructor.tagger("iframe", False, False)
INS = XmlConstructor.tagger("ins", False, False)
KBD = XmlConstructor.tagger("kbd", False, False)
LABEL = XmlConstructor.tagger("label", False, False)
LEGEND = XmlConstructor.tagger("legend", False, False)
LI = XmlConstructor.tagger("li", False, False)
MAIN = XmlConstructor.tagger("main", False, False)
MAP = XmlConstructor.tagger("map", False, False)
MARK = XmlConstructor.tagger("mark", False, False)
METER = XmlConstructor.tagger("meter", False, False)
NAV = XmlConstructor.tagger("nav", False, False)
NOSCRIPT = XmlConstructor.tagger("noscript", False, False)
OBJECT = XmlConstructor.tagger("object", False, False)
OL = XmlConstructor.tagger("ol", False, False)
OPTGROUP = XmlConstructor.tagger("optgroup", False, False)
OPTION = XmlConstructor.tagger("option", False, False)
OUTPUT = XmlConstructor.tagger("output", False, False)
P = XmlConstructor.tagger("p", False, False)
PICTURE = XmlConstructor.tagger("picture", False, False)
PRE = XmlConstructor.tagger("pre", False, False)
PROGRESS = XmlConstructor.tagger("progress", False, False)
Q = XmlConstructor.tagger("q", False, False)
RP = XmlConstructor.tagger("rp", False, False)
RT = XmlConstructor.tagger("rt", False, False)
RUBY = XmlConstructor.tagger("ruby", False, False)
S = XmlConstructor.tagger("s", False, False)
SAMP = XmlConstructor.tagger("samp", False, False)
SCRIPT = XmlConstructor.tagger("script", False, False)
SECTION = XmlConstructor.tagger("section", False, False)
SELECT = XmlConstructor.tagger("select", False, False)
SMALL = XmlConstructor.tagger("small", False, False)
SPAN = XmlConstructor.tagger("span", False, False)
STRONG = XmlConstructor.tagger("strong", False, False)
STYLE = XmlConstructor.tagger("style", False, False)
SUB = XmlConstructor.tagger("sub", False, False)
SUMMARY = XmlConstructor.tagger("summary", False, False)
SUP = XmlConstructor.tagger("sup", False, False)
SVG = XmlConstructor.tagger("svg", False, False)
TABLE = XmlConstructor.tagger("table", False, False)
TBODY = XmlConstructor.tagger("tbody", False, False)
TD = XmlConstructor.tagger("td", False, False)
TEMPLATE = XmlConstructor.tagger("template", False, False)
TEXTAREA = XmlConstructor.tagger("textarea", False, False)
TFOOT = XmlConstructor.tagger("tfoot", False, False)
TH = XmlConstructor.tagger("th", False, False)
THEAD = XmlConstructor.tagger("thead", False, False)
TIME = XmlConstructor.tagger("time", False, False)
TITLE = XmlConstructor.tagger("title", False, False)
TR = XmlConstructor.tagger("tr", False, False)
U = XmlConstructor.tagger("u", False, False)
UL = XmlConstructor.tagger("ul", False, False)
VAR = XmlConstructor.tagger("var", False, False)
VIDEO = XmlConstructor.tagger("video", False, False)
