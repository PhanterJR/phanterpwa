"""
Title: helpers

Author: PhanterJR<junior.conex@gmail.com>

License: MIT

Coding: utf-8

In this module are gathered all the TAGs currently used for the creation of HTML5 pages.
TAG objects inherited the functionality of their parent class, the XmlConstructor

You can import all with.

    >>> from phanterpwa.helpers import *

Or just what you want.

    >>> from phanterpwa.helpers import (HTML, HEAD, BODY, DIV, SPAN)
    >>> HTML(HEAD(), BODY(DIV(SPAN())))
    <!DOCTYPE html><head><head><body><div><span></span></div></boby></html>

The complete list can be obtained with.

    >>> from phanterpwa.helpers import ALL_TAGS
    >>> print(ALL_TAGS)
    ['CONCATENATE', 'XML', 'XCOMMENT', 'AREA', 'BASE', 'COL', 'EMBED', 'HR', 'IMG', 'INPUT', 'LINK', 'META', 'PARAM', 'SOURCE', 'TRACK', 'WBR', 'BR', 'A', 'ABBR', 'ADDRESS', 'ARTICLE', 'ASIDE', 'AUDIO', 'B', 'BDI', 'BDO', 'BLOCKQUOTE', 'BODY', 'BUTTON', 'CANVAS', 'CAPTION', 'CITE', 'CODE', 'COLGROUP', 'DATA', 'DATALIST', 'DD', 'DEL', 'DETAILS', 'DFN', 'DIALOG', 'DIV', 'DL', 'DT', 'EM', 'FIELDSET', 'FIGCAPTION', 'FIGURE', 'FOOTER', 'FORM', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'HEAD', 'HEADER', 'HTML', 'I', 'IFRAME', 'INS', 'KBD', 'LABEL', 'LEGEND', 'LI', 'MAIN', 'MAP', 'MARK', 'METER', 'NAV', 'NOSCRIPT', 'OBJECT', 'OL', 'OPTGROUP', 'OPTION', 'OUTPUT', 'P', 'PICTURE', 'PRE', 'PROGRESS', 'Q', 'RP', 'RT', 'RUBY', 'S', 'SAMP', 'SCRIPT', 'SECTION', 'SELECT', 'SMALL', 'SPAN', 'STRONG', 'STYLE', 'SUB', 'SUMMARY', 'SUP', 'SVG', 'TABLE', 'TBODY', 'TD', 'TEMPLATE', 'TEXTAREA', 'TFOOT', 'TH', 'THEAD', 'TIME', 'TITLE', 'TR', 'U', 'UL', 'VAR', 'VIDEO']

There is also a separate list by categories: NORMAL_TAGS, VOID_TAGS,
and SPECIAL_TAGS.
"""

from .xmlconstructor import XmlConstructor
from .third_parties.xss import XssCleaner


SPECIAL_TAGS = [
    'CONCATENATE',
    'XML',
    'XCOMMENT'
]
VOID_TAGS = [
    'AREA',
    'BASE',
    'COL',
    'EMBED',
    'HR',
    'IMG',
    'INPUT',
    'LINK',
    'META',
    'PARAM',
    'SOURCE',
    'TRACK',
    'WBR',
    'BR'
]
NORMAL_TAGS = [
    'A',
    'ABBR',
    'ADDRESS',
    'ARTICLE',
    'ASIDE',
    'AUDIO',
    'B',
    'BDI',
    'BDO',
    'BLOCKQUOTE',
    'BODY',
    'BUTTON',
    'CANVAS',
    'CAPTION',
    'CITE',
    'CODE',
    'COLGROUP',
    'DATA',
    'DATALIST',
    'DD',
    'DEL',
    'DETAILS',
    'DFN',
    'DIALOG',
    'DIV',
    'DL',
    'DT',
    'EM',
    'FIELDSET',
    'FIGCAPTION',
    'FIGURE',
    'FOOTER',
    'FORM',
    'H1',
    'H2',
    'H3',
    'H4',
    'H5',
    'H6',
    'HEAD',
    'HEADER',
    'HTML',
    'I',
    'IFRAME',
    'INS',
    'KBD',
    'LABEL',
    'LEGEND',
    'LI',
    'MAIN',
    'MAP',
    'MARK',
    'METER',
    'NAV',
    'NOSCRIPT',
    'OBJECT',
    'OL',
    'OPTGROUP',
    'OPTION',
    'OUTPUT',
    'P',
    'PICTURE',
    'PRE',
    'PROGRESS',
    'Q',
    'RP',
    'RT',
    'RUBY',
    'S',
    'SAMP',
    'SCRIPT',
    'SECTION',
    'SELECT',
    'SMALL',
    'SPAN',
    'STRONG',
    'STYLE',
    'SUB',
    'SUMMARY',
    'SUP',
    'SVG',
    'TABLE',
    'TBODY',
    'TD',
    'TEMPLATE',
    'TEXTAREA',
    'TFOOT',
    'TH',
    'THEAD',
    'TIME',
    'TITLE',
    'TR',
    'U',
    'UL',
    'VAR',
    'VIDEO',
]
ALL_TAGS = __all__ = SPECIAL_TAGS + VOID_TAGS + NORMAL_TAGS


class CONCATENATE(XmlConstructor):
    """With CONCATENATE it is possible to concatenate several objects to create the html.

    Example:
        >>> from phanterpwa.helpers import DIV, CONCATENATE
        >>> my_instance = CONCATENATE(
        ...     DIV("This is a div"),
        ...     "this is a string",
        ...     DIV("this is other div")
        ... )
        >>> print(my_instance)
        <div>This is a div</div>this is a string<div>this is other div</div>
    """

    def __init__(self, *content):
        XmlConstructor.__init__(self, "", False, *content)
        self.alternative_tag = "concatenate"


class XML(XmlConstructor, XssCleaner):
    """With XML it is possible to apply an optional sanitization, it is disabled by default, so that every string will
    be treated as html.

    Example:
        >>> from phanterpwa.helpers import SPAN, DIV, XML
        >>> instanceDIV = DIV("<span>escaped</span>")
        >>> print(instanceDIV)
        <div>&lt;span&gt;escaped&lt;/span&gt;</div>
        >>> instanceDIV_with_XML = DIV(XML("<span>not escaped</span>"))
        >>> print(instanceDIV_with_XML)
        <div><span>not escaped</span></div>
        >>> instanceSPAN = SPAN("<evil>I will destroy you.</evil>")
        >>> print(instanceSPAN)
        <span>&lt;evil&gt;I will destroy you.&lt;/evil&gt;</span>
        >>> print(DIV("<other_evil>", XML("<evil>I will destroy you.</evil>"), "</other_evil>"))
        <div>&lt;other_evil&gt;<evil>I will destroy you.</evil>&lt;/other_evil&gt;</div>
    """

    def __init__(self,
            *content,
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
        self.alternative_tag = "xml"
        self.sanitize = sanitize
        self.permitted_tags = permitted_tags
        self.allowed_attributes = allowed_attributes
        self.strip_disallowed = False
        self.escape_string = False

    def xml(self) -> str:
        """With this method a string is converted to html with an optional sanitization (predefined tags, predefined
        attributes, escape or not strings), by default sanitization is disabled (False).
        """
        if self.minify:
            xml = self._minified(
                close_void=self.close_void,
                i18nInstance=self.i18nInstance,
                dictionary=self.dictionary,
                do_not_translate=self.do_not_translate,
                tag_translation=self.tag_translation
            )
            if self._formatter:
                xml = self.interpolate(xml, self._formatter, self.delimiters)
        else:
            xml = self.humanize()
        if self.sanitize:
            return self.strip(xml)
        return xml


class XCOMMENT(XmlConstructor):
    """With XCOMMENT it is possible to create html comments.

        Example:
            >>> from phanterpwa.helpers import XCOMMENT
            >>> print(XCOMMENT("thit is a comment"))
            <!--this is a comment-->

    """

    def __init__(self, *content):
        XmlConstructor.__init__(self, "", False, *content)
        self.alternative_tag = "xcomment"
        self.escape_string = False
        self.before_xml = "<!--"
        self.after_xml = "-->"

    def _humanized(self, indent_size=2, close_void=False, translate=False):
        return "".join(["\n", " " * (indent_size * (self._indent_level)), self.xml()])


# html5 by default
class HTML(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "html", False, *content, **attributes)
        self.before_xml = "<!DOCTYPE html>"


# void tags
AREA = XmlConstructor.tagger("area", True)
BASE = XmlConstructor.tagger("base", True)
COL = XmlConstructor.tagger("col", True)
EMBED = XmlConstructor.tagger("embed", True)
HR = XmlConstructor.tagger("hr", True)
IMG = XmlConstructor.tagger("img", True)
INPUT = XmlConstructor.tagger("input", True)
LINK = XmlConstructor.tagger("link", True)
META = XmlConstructor.tagger("meta", True)
PARAM = XmlConstructor.tagger("param", True)
SOURCE = XmlConstructor.tagger("source", True)
TRACK = XmlConstructor.tagger("track", True)
WBR = XmlConstructor.tagger("wbr", True)
BR = XmlConstructor.tagger("br", True)
# normal tags
A = XmlConstructor.tagger("a")
ABBR = XmlConstructor.tagger("abbr")
ADDRESS = XmlConstructor.tagger("address")
ARTICLE = XmlConstructor.tagger("article")
ASIDE = XmlConstructor.tagger("aside")
AUDIO = XmlConstructor.tagger("audio")
B = XmlConstructor.tagger("b")
BDI = XmlConstructor.tagger("bdi")
BDO = XmlConstructor.tagger("bdo")
BLOCKQUOTE = XmlConstructor.tagger("blockquote")
BODY = XmlConstructor.tagger("body")
BUTTON = XmlConstructor.tagger("button")
CANVAS = XmlConstructor.tagger("canvas")
CAPTION = XmlConstructor.tagger("caption")
CITE = XmlConstructor.tagger("cite")
CODE = XmlConstructor.tagger("code")
COLGROUP = XmlConstructor.tagger("colgroup")
DATA = XmlConstructor.tagger("data")
DATALIST = XmlConstructor.tagger("datalist")
DD = XmlConstructor.tagger("dd")
DEL = XmlConstructor.tagger("del")
DETAILS = XmlConstructor.tagger("details")
DFN = XmlConstructor.tagger("dfn")
DIALOG = XmlConstructor.tagger("dialog")
DIV = XmlConstructor.tagger("div")
DL = XmlConstructor.tagger("dl")
DT = XmlConstructor.tagger("dt")
EM = XmlConstructor.tagger("em")
FIELDSET = XmlConstructor.tagger("fieldset")
FIGCAPTION = XmlConstructor.tagger("figcaption")
FIGURE = XmlConstructor.tagger("figure")
FOOTER = XmlConstructor.tagger("footer")
FORM = XmlConstructor.tagger("form")
H1 = XmlConstructor.tagger("h1")
H2 = XmlConstructor.tagger("h2")
H3 = XmlConstructor.tagger("h3")
H4 = XmlConstructor.tagger("h4")
H5 = XmlConstructor.tagger("h5")
H6 = XmlConstructor.tagger("h6")
HEAD = XmlConstructor.tagger("head", never_translate=True)
HEADER = XmlConstructor.tagger("header")
I = XmlConstructor.tagger("i")
IFRAME = XmlConstructor.tagger("iframe")
INS = XmlConstructor.tagger("ins")
KBD = XmlConstructor.tagger("kbd")
LABEL = XmlConstructor.tagger("label")
LEGEND = XmlConstructor.tagger("legend")
LI = XmlConstructor.tagger("li")
MAIN = XmlConstructor.tagger("main")
MAP = XmlConstructor.tagger("map")
MARK = XmlConstructor.tagger("mark")
METER = XmlConstructor.tagger("meter")
NAV = XmlConstructor.tagger("nav")
NOSCRIPT = XmlConstructor.tagger("noscript")
OBJECT = XmlConstructor.tagger("object")
OL = XmlConstructor.tagger("ol")
OPTGROUP = XmlConstructor.tagger("optgroup")
OPTION = XmlConstructor.tagger("option")
OUTPUT = XmlConstructor.tagger("output")
P = XmlConstructor.tagger("p")
PICTURE = XmlConstructor.tagger("picture")
PRE = XmlConstructor.tagger("pre")
PROGRESS = XmlConstructor.tagger("progress")
Q = XmlConstructor.tagger("q")
RP = XmlConstructor.tagger("rp")
RT = XmlConstructor.tagger("rt")
RUBY = XmlConstructor.tagger("ruby")
S = XmlConstructor.tagger("s")
SAMP = XmlConstructor.tagger("samp")
SCRIPT = XmlConstructor.tagger("script", escape_string=False, never_translate=True)
SECTION = XmlConstructor.tagger("section")
SELECT = XmlConstructor.tagger("select")
SMALL = XmlConstructor.tagger("small")
SPAN = XmlConstructor.tagger("span")
STRONG = XmlConstructor.tagger("strong")
STYLE = XmlConstructor.tagger("style", escape_string=False, never_translate=True)
SUB = XmlConstructor.tagger("sub")
SUMMARY = XmlConstructor.tagger("summary")
SUP = XmlConstructor.tagger("sup")
SVG = XmlConstructor.tagger("svg")
TABLE = XmlConstructor.tagger("table")
TBODY = XmlConstructor.tagger("tbody")
TD = XmlConstructor.tagger("td")
TEMPLATE = XmlConstructor.tagger("template")
TEXTAREA = XmlConstructor.tagger("textarea")
TFOOT = XmlConstructor.tagger("tfoot")
TH = XmlConstructor.tagger("th")
THEAD = XmlConstructor.tagger("thead")
TIME = XmlConstructor.tagger("time")
TITLE = XmlConstructor.tagger("title")
TR = XmlConstructor.tagger("tr")
U = XmlConstructor.tagger("u")
UL = XmlConstructor.tagger("ul")
VAR = XmlConstructor.tagger("var")
VIDEO = XmlConstructor.tagger("video")
