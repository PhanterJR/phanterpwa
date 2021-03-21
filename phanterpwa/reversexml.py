"""
Title: XmlConstructor

Author: PhanterJR<junior.conex@gmail.com>

License: MIT

Coding: utf-8

Html to XmlConstructor
"""

from html.parser import HTMLParser
from .xmlconstructor import XmlConstructor
from .helpers import CONCATENATE, XCOMMENT


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
                raise TypeError("is_closed must be bool, given: {0}".format(type(v)))


class HtmlToXmlConstructor(CONCATENATE, HTMLParser):
    """The XmlConstructor writes html, this object already does the opposite, with it it is possible with html to
    write XmlConstructor.

    At instantiation we have the following parameters

    :param strhtml: String with html code.
    :param filter_empty_content: Filters empty elements when True (False)
    :param filter_comments: Filter comments elements when True (True)
    """

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
        """Manipulate the initial tag and its attributes, see html.parse.HTMLParser for more details.
        """
        attr_tag = {}
        for attr in attrs:
            attr_tag["_%s" % attr[0]] = True if attr[1] is None else attr[1]
        el = _Tag(tag, True if tag in self.void_tags else False, False)
        el.attributes = attr_tag
        if all([tag == "html",
            self.HTMLdoctypedeclaration,
            self.HTMLdoctypedeclaration != "<!DOCTYPE html>"]):
            el.before_xml = self.HTMLdoctypedeclaration
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
        """Manipulate the end tag, see html.parse.HTMLParser for more details.
        """
        if tag not in self.void_tags:
            last_el = self.opened_el[-1]
            if not last_el.is_closed:
                last_el.is_closed = True
                self.opened_el.pop(-1)

    def handle_data(self, data):
        """Manipulate the data, see html.parse.HTMLParser for more details.
        """
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
        """Manipulate the comments, see html.parse.HTMLParser for more details.
        """
        if self.opened_el:
            last_el = self.opened_el[-1]
            if not last_el.is_closed:
                content = list(last_el.content)
                content.append(XCOMMENT(data))
                last_el.content = content
        else:
            self.append(XCOMMENT(data))

    def handle_decl(self, data):
        """Manipulate the declarations, see html.parse.HTMLParser for more details.
        """
        self.HTMLdoctypedeclaration = "<!{0}>".format(data.strip())

    def xmlconstructor_code(self, add_imports: bool=False, phanterpwa_helpers: bool=False, instance_name: str="html",
            translate: bool=False) -> str:
        """Returns the generated source code, does the same as the source_code method with the difference of omit
        the CONCATENATE root tag when necessary.

        see the documentation for the source_code method of phanterpwa.xmlconstructor.XmlConstructor for more details.

        :param add_imports: add necessary imports in code This arguments
            will take effect if add_imports is true.
        :param phanterpwa_helpers: user phanter.helpers import.
        :param instance_name: The generated code is assigned to a variable
            with the name assigned here.
        :param translate: If True, the generated source_code strings will
            be translated.

        Example:
            >>> from phanterpwa.reversexml import HtmlToXmlConstructor
            >>> html_to_xmlconstructor_instance = HtmlToXmlConstructor("<html><head><meta charset=\"UTF-8\"></head><body><nav class=\"navbar\"><buttom>start</buttom></nav><main id=\"my_content\"><div class=\"row\"><div>my content</div></div></main></body></html>")
            >>> print(html_to_xmlconstructor_instance.xmlconstructor_code())
            HTML(
                HEAD(
                    META(
                        _charset='UTF-8'
                    )
                ),
                BODY(
                    NAV(
                        BUTTOM(
                            'start'
                        ),
                        _class='navbar'
                    ),
                    MAIN(
                        DIV(
                            DIV(
                                'my content'
                            ),
                            _class='row'
                        ),
                        _id='my_content'
                    )
                )
            )
            >>> html_to_xmlconstructor_instance = HtmlToXmlConstructor("<div data-dict=\"i am in dict\" class=\"my_class\">content1</div><div class=\"my_class\">content2</div>")
            >>> print(html_to_xmlconstructor_instance.xmlconstructor_code())
            CONCATENATE(
                DIV(
                    'content1',
                    **{
                        '_data-dict': 'i am in dict',
                        '_class': 'my_class'
                    }
                ),
                DIV(
                    'content2',
                    _class='my_class'
                )
            )
        """
        if len(self) == 1:
            child = self[0]
            child._indent_level = 0
            child._parent = None
            return child.source_code(add_imports, phanterpwa_helpers, instance_name, translate)
        else:
            return self.source_code(add_imports, phanterpwa_helpers, instance_name, translate)


def force_minify_string_content(target: XmlConstructor) -> XmlConstructor:
    """Forces the minification of the string content by removing multiple empty spaces, line breaks, tabs replacing
    with a single space.

    :param target: XmlConstructor (or HtmlToXmlConstructor) instance

    Example:
        >>> from phanterpwa.reversexml import (HtmlToXmlConstructor, force_minify_string_content)
        >>> sample = '''
        ... <html>
        ...     <head>
        ...         <meta charset="utf-8">
        ...     </head>
        ...     <body>
        ...         Forces      the       minification
        ...         of the     string content       by
        ...         removing       multiple     empty
        ...         spaces,      line       breaks,
        ...         tabs      replacing     with a
        ...         single    space.
        ...     </body>
        ... </html>
        ... '''
        >>> html_to_xmlconstructor_instance = HtmlToXmlConstructor(sample)
        >>> print(html_to_xmlconstructor_instance.xml())
        <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                Forces      the       minification
                of the     string content       by
                removing       multiple     empty
                spaces,      line       breaks,
                tabs      replacing     with a
                single    space.
            </body>
        </html>
        >>> force_minify_string_content(html_to_xmlconstructor_instance)
        >>> print(html_to_xmlconstructor_instance.xml())
        <html><head><meta charset="utf-8"></head><body> Forces the minification of the string content by removing multiple empty spaces, line breaks, tabs replacing with a single space. </body></html>
        >>> print(html_to_xmlconstructor_instance.xmlconstructor_code())
        HTML(
            HEAD(
                META(
                    _charset='utf-8'
                )
            ),
            BODY(
                ' Forces the minification of the string content by removing multiple empty spaces, line breaks, tabs replacing with a single space. '
            )
        )
    """
    if isinstance(target, XmlConstructor):
        def f(r):
            new_content = []
            skippers = [" ", "\n", "\t", "\r"]
            for x in r:
                if isinstance(x, XmlConstructor):
                    f(x)
                    new_content.append(x)
                elif isinstance(x, str):
                    set_str = set(x)
                    if set_str.union(set(skippers)) == set(skippers):
                        pass
                    else:
                        if x:
                            i_std = ""
                            f_str = ""
                            if x[0] in skippers:
                                i_std = " "
                            if x[-1] in skippers:
                                f_str = " "
                            n_v = " ".join([z.strip() for z in x.split(" ") if z not in skippers and z])
                            new_content.append("".join([i_std, n_v, f_str]))
                else:
                    new_content.append(x)
            r.content = new_content
        f(target)
        return target
    else:
        raise ValueError("The target must be XmlConstructor instance.")

