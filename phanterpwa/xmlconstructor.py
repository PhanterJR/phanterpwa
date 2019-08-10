# -*- coding: utf-8 -*-
from .tools import interpolate, sass_change_vars, sass_map_vars
from .xss import xssescape
from .i18n import Translator
from xml.sax import saxutils
import json
from copy import copy
import os
import re

XML_SAMPLE = '''class XML(XmlConstructor, XssCleaner):
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
        self.alternative_tag = "xml"
        self.sanitize = sanitize
        self.permitted_tags = permitted_tags
        self.allowed_attributes = allowed_attributes
        self.strip_disallowed = False
        self.escape_string = False

    def xml(self) -> str:
        if self.minify:
            xml = self._minified(
                close_void=self.close_void,
                i18nInstance=self.i18nInstance,
                dictionary=self.dictionary,
                do_not_translate=self.do_not_translate,
                tag_translation=self.tag_translation
            )
            if self._formatter:
                xml = self._interpolate(xml, self._formatter, self.delimiters)
        else:
            xml = self.humanize()
        if self.sanitize:
            return self.strip(xml)
        return xml'''

HTML_SAMPLE = '''class HTML(XmlConstructor):
    def __init__(self, *content, **attributes):
        XmlConstructor.__init__(self, "html", False, *content, **attributes)
        self.before_xml = "<!DOCTYPE html>"'''

XCOMMENT_SAMPLE = '''class XCOMMENT(XmlConstructor):
    def __init__(self, *content):
        XmlConstructor.__init__(self, "", False, *content)
        self.alternative_tag = "xcomment"
        self.escape_string = False
        self.before_xml = "<!--"
        self.after_xml = "-->"

    def _humanized(self, indent_size=2, close_void=False, translate=False):
        return "".join(["\\n", " " * (indent_size * (self._indent_level)), self.xml()])'''


class FrozenContent(tuple):
    def __setitem__(self, i, v):
        raise SyntaxError("".join([
            "To modify or add the content do directly in the instance,",
            " example: my_instance[0] = \"new_value\""
        ]))


class FrozenAttributes(dict):
    def __setitem__(self, i, v):
        raise SyntaxError("".join([
            "To modify or add an attribute do directly in the instance,",
            " example: my_instance[\"_ my_attribute\"] = \"new_value\""
        ]))


class XmlConstructor(object):
    r"""
    @author: PhanterJR<junior.conex@gmail.com>
    @license: MIT

    Helper to constroi html tags.
    With this class you can create other predefined tags.
    Example:
        >>> class DIV(XmlConstructor):
                def __init__(self, *content, **attributes):
                    XmlConstructor.__init__(self,
                        "div"
                         False,
                        *content,
                        **attributes)
        >>> print(DIV())
        <div></div>

    Or you can (recommended). Using the tagger method you can create a
    metaclass of class XmlConstructor.

        >>> DIV = XmlConstructor.tagger("div")
        >>> print(DIV())
        <div></div>
        >>> print(DIV("My content", _class="my_atribute_class"))
        <div class="my_atribute_class">My content</div>

    IMPORTANT, Use the xml (or html) method to capture the results you
    can see in the print command

        >>> DIV = XmlConstructor.tagger("div")
        >>> print(DIV("My content", _class="my_atribute_class"))
        <div class="my_atribute_class">My content</div>
        >>> DIV("My content", _class="my_atribute_class").xml()
        '<div class="my_atribute_class">My content</div>'
        >>> instanceDIV = DIV("My content", _class="my_atribute_class")
        >>> instanceDIV.xml()
        '<div class="my_atribute_class">My content</div>'
        >>> print(instanceDIV)
        <div class="my_atribute_class">My content</div>
        >>> new_instance = DIV("line0", "\nline1")
        >>> new_instance.xml()
        '<div>line0\nline1</div>'
        >>> print(new_instance)  # the print command convert "\n" to breaklines
        <div>line0
        line1</div>

    We already have tags ready to use, no need to reinvent the wheel. In
    the package module helpers of the phanterpwa package contains all
    tags used for html5, just import with.

        >>> from phanterpwa.helpers import *

    Or just what you want.

        >>> from phanterpwa.helpers import (HTML, HEAD, BODY, DIV, SPAN)

    The complete list can be obtained with.

        >>> from phanterpwa.helpers import ALL_TAGS
        >>> print (ALL_TAGS)

    There is also a separate list by categories: NORMAL_TAGS, VOID_TAGS,
    and SPECIAL_TAGS.
    """
    __author__ = "PhanterJR<junior.conex@gmail.com>"
    __license__ = "MIT"
    _indent_size = 2
    _all_instances = {}
    _tag_list = []
    _close_void = False
    _minify = True
    _interpolate = interpolate

    def __init__(self, tag: str, void: bool=False, *content, **attributes):
        """
        Constructor of the class

        Args:

            @tag: Name of tag. Example: div, img, br.
            @void: If True, the tag does not has content.
            @content = Content of element. exemple:
                >>> XmlConstructor.tagger("this is", " my content")
            @attributes = Element attributes. Each key of the attribute
            must begin with underline (_) (because of the keyword class
            and id), keys without underline will store on
            yourInstance.kargs

        Examples with void is True.

            >>> instenceBR = XmlConstructor.tagger("br", True)()
            <br>
            >>> print(XmlConstructor.tagger("hr", True)(_class="especial_hr"))
            <hr class="especial_hr">
            >>> print(XmlConstructor.tagger("img", True)(_href="#my_url"))
            <img href="#my_url">

        Same example, with best practices, creating a metaclass with the
        tagger method:

            >>> BR = XmlConstructor.tagger("br", True)
            >>> HR = XmlConstructor.tagger("hr", True)
            >>> IMG = XmlConstructor.tagger("img", True)
            >>> instanceBR = BR()
            >>> print(instanceBR)
            <br>
            >>> instanceBR.close_void = True  # If True, the tag of void elements are closed with "/".
            >>> print(instanceBR)
            <br />
            >>> instanceHR = HR(_class="especial_hr")
            >>> print(instanceHR)  # This close_void uses a classmethod, so a change reflects on all instances
            <hr class="especial_hr" />
            >>> instanceBR.close_void = False
            >>> print(instanceHR)  # The close_void is False
            <hr class="especial_hr">
            >>> print(IMG(_href="#my_url"))
            <img href="#my_url">

        if @void is False, the tag will be close tag:

            >>> print(XmlConstructor.tagger("div")())
            <div></div>
            >>> H1 = XmlConstructor.tagger("h1", False, False)
            >>> print(H1("My title"))
            <h1>My title</h1>
            >>> BUTTON = XmlConstructor.tagger("button", False, False)
            >>> print(BUTTON("my_content", _class="my_class"))
            <button class="my_class">my_content</button>

        BEST PRACTICE: To help in use, use the classmethod tagger, in
        this way you can suppress some parameters.
        Using the tagger method you can create a metaclass of class
        XmlConstructor, see:

            >>> DIV = XmlConstructor.tagger("div")
            >>> IMG = XmlConstructor.tagger("img", True)
            >>> BR = XmlConstructor.tagger("br", True)
            >>> print(DIV())
            <div></div>
            >>> print(DIV("this", "is", "join", " its no. ", "<tag_evil>evil</tag_evil>"))
            <div>thisisjoin its no. &lt;tag_evil&gt;evil&lt;/tag_evil&gt;</div>
            >>> print(IMG(_class="images"))
            <img class="images">
            >>> print(BR())
            <br>
        """

        super(XmlConstructor, self).__init__()
        self.alternative_tag = "empty_tag"
        self.tag = tag
        self.before_xml = ""
        self.after_xml = ""
        self.void = void
        self._parent = None
        self._root_parent = None
        self._was_copied = set()
        self.kargs = {}
        self.escape_string = True
        self.is_reverse = False
        self.attributes = attributes
        self.delimiters = ["{{", "}}"]
        self.content = content
        self.dictionary = None
        self.do_not_translate = []
        self.i18nInstance = None
        self.tag_translation = "span"
        self._add_instance(tag, self)
        self._indent_level = 0
        self._idx = 0
        self._humanized_idx = ""
        self._all_children = {}
        self.src_attr_dict = None
        self._formatter = {}
        self._sass = None
        self._minify_css = None
        self._target_sass = None
        self._target_css = None
        self.never_translate = False

    @property
    def id(self) -> int:
        """
        GET:

            Get element id

        Usage:

            >>> UL = XmlConstructor.tagger("div")
            >>> instanceUL = UL()
            >>> other_instanceUL = UL()
            >>> print(instanceUL.id)
            32344567
            >>> print(other_instanceUL.id)
            234678454
        """

        return id(self)

    @property
    def introspect(self):
        """
        GET:

            This property returns a representation of the instance, with
            the class, id, and tag information.

        Example:

            from phanterpwa.helpers import DIV
            >>> instanceDIV = DIV()
            >>> print(instanceDIV.introspect)
            <class 'phanterpwa.xmlconstructor.XmlConstructor.tagger.<locals>.TAGGER'> {id: 46269904, tag: div}
        """
        str_repr = "{0} {{id: {1}, tag: {2}}}".format(self.__class__, self.id, self.tag)
        return str_repr

    @property
    def all_instances(self):
        """
        GET:

            This property returns a dict with all instances created
            The key is the id and the value is the instance

        Example:

            from phanterpwa.helpers import DIV, SPAN
            >>> instanceDIV = DIV(SPAN() * 3)
            >>> print(instanceDIV.all_instances)
            {2384912: <class 'phanterpwa.xmlconstructor.XmlConstructor.tagger.<locals>.TAGGER'> {id: 2384912, tag: span},
            47221040: <class 'phanterpwa.xmlconstructor.XmlConstructor.tagger.<locals>.TAGGER'> {id: 47221040, tag: span},
            47221136: <class 'phanterpwa.xmlconstructor.XmlConstructor.tagger.<locals>.TAGGER'> {id: 47221136, tag: span},
            2387280: <class 'phanterpwa.xmlconstructor.XmlConstructor.tagger.<locals>.TAGGER'> {id: 2387280, tag: div}
        """
        return self._all_instances

    @property
    def tag_list(self) -> list:
        """
        GET:

            list all tags used in instance creation

        Example:

            >>> DIV = XmlConstructor.tagger("div")
            >>> SPAN = XmlConstructor.tagger("span")
            >>> instanceDIV = DIV(SPAN() * 3)
            >>> print(instanceDIV.tag_list)
            ['span', 'div']
        """

        return self._tag_list

    @property
    def was_copied(self) -> set:
        """
        When we add an instance to an element automatically it will be
        the parent, if we add the same instance to another element, it
        will already have a parent, so an instance must only have one
        parent, so in those cases a copy of the instance is created to
        add a parent different, the list of copies is stored in this
        property.

        GET:

            Returns a set with all instances copied

        Example:

            >>> from phanterpwa.helpers import DIV, SPAN
            >>> sourceInstance = SPAN("Is this the same instance? get id")
            >>> containerDIV = DIV(sourceInstance, sourceInstance, sourceInstance)
            >>> print(containerDIV)
            <div><span>Is this the same instance? get id</span><span>Is this the same instance? get id</span><span>Is this the same instance? get id</span></div>
            >>> sourceInstance.content = "changed!"
            >>> print(containerDIV)
            <div><span>changed!</span><span>Is this the same instance? get id</span><span>Is this the same instance? get id</span></div>

        If you want to access the copies just use this property (was_copied):

            >>> for x in sourceInstance.was_copied:
                    x.content = "changed!"
            >>> print(containerDIV)
            <div><span>changed!</span><span>changed!</span><span>changed!</span></div>

        """
        return self._was_copied

    @property
    def root_parent(self) -> 'XmlConstructor':
        """
        This property returns the main instance (root), in which the other
        instances are introduced.

        GET:

            returns the main instance (root)

        Usage:

            >>> DIV = XmlConstructor.tagger("div")
            >>> SPAN = XmlConstructor.tagger("span")
            >>> child_instance = DIV("I am a child")
            >>> root_parent = DIV(SPAN(child_instance), SPAN())
            >>> print(root_parent)  # the root_parent
            <div><span><div>I am a child</div></span><span></span></div>
            >>> print(child_instance)  # the child_instance
            <div>I am a child</div>
            >>> print(child_instance.parent)  # parent of child_instance
            <span><div>I am a child</div></span>
            >>> print(child_instance.root_parent)  # The root instance called from child instance
            <div><span><div>I am a child</div></span><span></span></div>

        """
        if self.parent is None:
            self._root_parent = self
            return self
        else:
            self._root_parent = self.parent.root_parent
            return self._root_parent

    @property
    def parent(self) -> 'XmlConstructor':
        """
        This property returns the parent of the instance.
        If the instance is main element (root), it returns None

        GET:

            Returns the parent of the instance.

        Usage:

            >>> DIV = XmlConstructor.tagger("div")
            >>> SPAN = XmlConstructor.tagger("span")
            >>> child_instance = DIV("I am a child")
            >>> root_parent = DIV(SPAN(child_instance), SPAN())
            >>> print(root_parent)  # the root_parent
            <div><span><div>I am a child</div></span><span></span></div>
            >>> print(child_instance)  # the child_instance
            <div>I am a child</div>
            >>> print(child_instance.parent)  # parent of child_instance (SPAN)
            <span><div>I am a child</div></span>

        """
        return self._parent

    @property
    def tag_begin(self) -> str:
        """
        GET

            Get begin tag.

        Example:

            >>> DIV = XmlConstructor.tagger('div', False)
            >>> instance_element = DIV()
            >>> print(instance_element)
            <div class="my_class" id="my_id"></div>
            >>> instance_element.attributes = {"_class": "my_class", "_id": "my_id"}
            >>> print(instance_element.tag_begin)
            <div class="my_class" id="my_id">
        """
        self._tag_begin = self._tag_begin_cmp(self.close_void)
        return self._tag_begin

    @property
    def tag_end(self) -> str:
        """
        GET:

            Get end tag.

        Example:

            >>> DIV = XmlConstructor.tagger('div', False)
            >>> instance_element = DIV()
            >>> instance_element.attributes = {"_class": "my_class", "_id": "my_id"}
            >>> print(instance_element.tag_end)
            '</div>'
            >>> HR = XmlConstructor.tagger('hr', True)
            >>> instance_element = HR()
            >>> print(instance_element.tag_end)

            >>>
        """
        if self._tag and not self.void:
            self._tag_end = "</{0}>".format(self.tag)
        else:
            self._tag_end = ""
        return self._tag_end

    @property
    def xml_content(self) -> str:
        """
        With the xml_content property you can view the generated xml of
        the elements that are in the content of the main element.

        GET:

            gets xml generated from content elements

        Usage:

            >>> DIV = XmlConstructor.tagger("div")
            >>> SPAN = XmlConstructor.tagger("span")
            >>> html = DIV(SPAN(DIV()), SPAN())
            >>> print(html)
            <div><span><div></div></span><span></span></div>
            >>> print(html.xml_content) # Only the xml of the elements contained in the root element
            <span><div></div></span><span></span>
        """
        if self.minify:
            self._xml_content = self._minified_content(
                close_void=self.close_void,
                i18nInstance=self.i18nInstance,
                dictionary=self.dictionary,
                do_not_translate=self.do_not_translate,
                tag_translation=self.tag_translation
            )
        else:
            self._xml_content = self._humanized_content(
                indent_size=self.indent_size,
                close_void=self.close_void,
                i18nInstance=self.i18nInstance,
                dictionary=self.dictionary,
                do_not_translate=self.do_not_translate,
                tag_translation=self.tag_translation
            )
        return self._xml_content

    @property
    def xml_attributes(self) -> str:
        """
        With the xml_attributes property you can view the generated
         string of the attribute from element.

        GET:

            gets string generated from element

        Usage:

            >>> DIV = XmlConstructor.tagger("div")
            >>> instanceDIV = DIV(_id="my_id", _class="my_class")
            >>> print(instanceDIV.xml_attributes)
            id="my_id" class="my_class"
        """
        self.attributes = self._attributes
        return self._xml_attributes

    @property
    def xml_humanized_content(self) -> str:
        """
        With the xml_humanized_content property you can view the
        generated string of the content from element indented.

        GET:

            gets string indented of the content from element

        Usage:

            >>> DIV = XmlConstructor.tagger("div")
            >>> SPAN = XmlConstructor.tagger("div")
            >>> instanceDIV = DIV(SPAN("My content"), DIV("Other content"))
            >>> print(instanceDIV.xml_humanized_content)

              <span>
                My content
              </span>
              <div>
                Other content
              </div>
        """
        self._xml_humanized_content = self._humanized_content(
            indent_size=self.indent_size,
            close_void=self.close_void,
            i18nInstance=self.i18nInstance,
            dictionary=self.dictionary,
            do_not_translate=self.do_not_translate,
            tag_translation=self.tag_translation
        )
        return self._xml_humanized_content

    @property
    def all_children(self) -> dict:
        """
        GET:

            Returns a dict with all direct and indirect children, the
            keys are the index and the value is the instance.
            This option only affects the instance to which it is
            applied.

        Example:

            >>> from phanterpwa import (DIV, SPAN, A, BUTTON)
            >>> instanceDIV = DIV(SPAN(A(BUTTON("the direct parent is button"))))
            >>> for x in instanceDIV.all_children:
                    print('index:', x, '- xml:', instanceDIV.all_children[x])
            index: [0] - xml: <span><a><button>the direct parent is button</button></a></span>
            index: [0][0] - xml: <a><button>the direct parent is button</button></a>
            index: [0][0][0] - xml: <button>the direct parent is button</button>
            index: [0][0][0][0] - xml: the direct parent is button
        """
        self._all_children = {}
        idx = 0
        for x in self:
            if isinstance(x, XmlConstructor):
                x._indent_level = self._indent_level + 1
                x._humanized_idx = x._indexescalc("[{0}]".format(x._idx))
                self._all_children[x._humanized_idx] = x
                childs = x.all_children
                for y in childs:
                    self._all_children[y] = childs[y]
            else:
                if self._indent_level != 0:
                    self._all_children[self._indexescalc("[{0}][{1}]".format(self._idx, idx))] = x
                else:
                    self._all_children[self._indexescalc("[{0}]".format(idx))] = x
            idx += 1
        return self._all_children

    @property
    def tag(self) -> str:
        """
        GET:

            Get the tag name of instance

        SET:

            Set the tag of element
            @tag_name: Name of tag

        Example GET:

            >>> DIV = XmlConstructor.tagger('div')
            >>> instanceDIV = DIV()
            >>> print(instanceDIV.tag)
            div

        Example SET:

            >>> DIV = XmlConstructor.tagger('div')
            >>> my_instance = DIV()
            >>> print(my_instance)
            <div></div>
            >>> my_instance.tag = 'button'
            >>> print(my_instance)
            <button></button>

        """
        return self._tag

    @tag.setter
    def tag(self, tag_name: str):
        if isinstance(tag_name, str):
            self._tag = tag_name
            if tag_name:
                self._add_tag(tag_name)
                self.alternative_tag = tag_name
        else:
            raise TypeError("The tag must be string")

    @property
    def void(self) -> bool:
        """
        There are elements without content that does not have an end
        tag, they are the void elements. With this property it is
        possible to set this.
        This property can be set by using the tagger method.

        GET:

            Get the void parameter

        SET:

            Set a void parameter.
            So by setting the void parameter False, automatically the
            close_void parameter will also be set to False.
            @value: True or False to set if element is void or not.

        Example GET:

            >>> my_instance = XmlConstructor.tagger("button")() # The default is False
            >>> print(my_instance.void)
            False

        Example SET (True) using the tagger method:

            >>> my_instance = XmlConstructor.tagger("br", void=True)()
            >>> print(my_instance)
            <br>
            >>> my_instance = XmlConstructor.tagger("hr", True)()
            >>> print(my_instance)
            <hr>

        Example SET (Set False) using the tagger method:

            >>> my_instance = XmlConstructor.tagger("div")()
            >>> print(my_instance)
            <div></div>
            >>> my_instance = XmlConstructor.tagger("h1", False)
            >>> print(my_instance("My title"))
            <h1>My title</h1>

        Example SET change instance:

            >>> my_instance = XmlConstructor.tagger("mypersonal_tag")()
            >>> print(my_instance)
            <mypersonal_tag></mypersonal_tag>
            >>> my_instance.void = True
            >>> print(my_instance)
            <mypersonal_tag>
            >>> my_instance.void = False
            >>> print(my_instance)
            <mypersonal_tag></mypersonal_tag>
        """
        return self._void

    @void.setter
    def void(self, value: bool):
        if isinstance(value, bool):
            self._void = value
        else:
            raise TypeError("The void must be boolean. given: {0}".format(type(value)))

    # classmethod
    @property
    def close_void(self) -> bool:
        """
        In the void elements of html5 closing or not the tag is optional,
        if you are writing a html legacy (xhtml) with this property you
        can configure the closing of the tag.

        GET:

            Get the close_void parameter

        SET:

            Set a close_void parameter
            The change is only effective if the void parameter is also True.
            @value: True or False to set if the void element is closed or not

        Example GET:

            >>> my_instance = XmlConstructor.tagger("meta", void=True)(_charset="utf-8")
            >>> print(my_instance)
            <meta charset="utf-8">
            >>> print(my_instance.close_void)
            False

        Example SET (Set False) using the tagger method:

            >>> my_instance = XmlConstructor.tagger("hr", void=True)  # The default is False
            >>> print(my_instance().close_void)
            False
            >>> print(my_instance())
            <hr>

        Example SET (True) using the tagger method:

            >>> my_instance = XmlConstructor.tagger("div", void=False)()
            >>> print(my_instance.close_void)  # Is False because the void is False
            False
            >>> print(my_instance())
            <div></div>
            >>> my_instance = XmlConstructor.tagger("br", void=True)()
            >>> my_instance.close_void = True
            >>> print(my_instance)
            <br />
            >>> my_instance2 = XmlConstructor.tagger("hr", True, True)()
            >>> my_instance.attributes = {"_class": "has_class"}
            >>> print(my_instance)
            <hr class="has_class" />

        Example SET change instance:

            >>> my_instance = XmlConstructor.tagger("hr")()
            >>> print(my_instance)
            <hr></hr>
            >>> my_instance.close_void = True
            >>> print(my_instance)  # The change is only effective if the void parameter is also True
            <hr></hr>
            >>> my_instance.void = False
            >>> print(my_instance)
            <hr />
            >>> my_instance.close_void = False
            >>> print(my_instance)
            <hr>
        """
        return XmlConstructor.get_close_void()

    # classmethod
    @close_void.setter
    def close_void(self, value: bool):
        XmlConstructor.set_close_void(value)

    # classmethod
    @property
    def minify(self):
        """
        The xml method is called internally when the instance is
        converted to string (__str__) (when we print for example), this
        property changes the xml format generated by the xml method, the
        default is True, when False the generated xml is indented.
        By changing an attribute of the Class the change reflects in all
        instances.

        GET:

            Get the minify parameter. (default is True)

        SET:

            Set the minify parameter. (True or False)

        Example:

        >>> from phanterpwa.helpers import DIV
        >>> instanceDIV = DIV(DIV("content", _id="id_child"), _id="id_parent", _class="my_div")
        >>> otherInstanceDIV = DIV("other_instance", _id="id_other")
        >>> print(otherInstanceDIV.minify)
        True
        >>> print(instanceDIV.minify)
        True
        >>> print(instanceDIV)
        <div id="id_parent" class="my_div"><div id="id_child">content</div></div>
        >>> print(otherInstanceDIV)
        <div id="id_other">other_instance</div>
        >>> instanceDIV.minify = False  # change minify from instanceDIV
        >>> print(otherInstanceDIV.minify)  # reflects in all instances
        False
        >>> print(instanceDIV)
        <div id="id_parent" class="my_div">
          <div id="id_child">
            content
          </div>
        </div>
        >>> print(otherInstanceDIV)
        <div id="id_other">
          other_instance
        </div>
        """
        return XmlConstructor.get_minify()

    # classmethod
    @minify.setter
    def minify(self, value):
        if isinstance(value, bool):
            XmlConstructor.set_minify(value)
        else:
            raise "The minify must be True or False. Given: '{0}'".format(type(value))

    # classmethod
    @property
    def indent_size(self) -> int:
        """
        GET:

            Get current indentation of the class

        SET:

            Set the indentation of the xml method when the minification
            (minify attribute) is False and also the indentation of the
            humanize method.
            This property uses a classmethod, so a change reflects on
            all instances.

            @size: indentation size (2 is default).

        GET usage:

            >>> DIV = XmlConstructor.tagger("div")
            >>> DIV.indent_size
            2

        SET usage:

            >>> DIV = XmlConstructor.tagger("div")
            >>> DIV.indent_size = 4 #  default is 2

        SET example:

            >>> DIV = XmlConstructor.tagger("div")
            >>> instanceDIV = DIV("my content", _id="my_id")
            >>> otherInstance = DIV("my other content", _id="my_other_id")
            >>> print(instanceDIV)
            <div id="my_id">my content</div>
            >>> print(otherInstance)
            <div id="my_other_id">my other content</div>
            >>> instanceDIV.minify = False # minify is classmethod, this reflect all instances
            >>> print(instanceDIV)
            <div id="my_id">
              my content
            </div>
            >>> print(otherInstance)
            <div id="my_other_id">
              my other content
            </div>
            >>> otherInstance.indent_size = 4  # indent_size is classmethod, this reflect all instances
            >>> print(instanceDIV)
            <div id="my_id">
                my content
            </div>
            >>> instanceDIV.minify = True
            >>> print(otherInstance) # the indent_size is effective if the minify parameter is False
            <div id="my_other_id">my other content</div>
        """
        return XmlConstructor.get_indent_size()

    # classmethod
    @indent_size.setter
    def indent_size(self, size: int):
        XmlConstructor.set_indent_size(size)

    @property
    def escape_string(self):
        """
        By default every string escaped to prevent xss attacks, by
        setting this property to False strings will no longer be
        escaped.

        GET:

            Get current setting (default is True)

        SET:

            Set the setting to True or False
            @value: True or False

        Example:

            >>> from phanterpwa import SPAN, DIV
            >>> instanceSPAN = SPAN("<evil>I will destroy you.</evil>")
            >>> print(instanceSPAN)
            <span>&lt;evil&gt;I will destroy you.&lt;/evil&gt;</span>
            >>> instanceSPAN.escape_string=False
            >>> print(instanceSPAN)
            <span><evil>I will destroy you.</evil></span>
            >>> print(DIV("<other_evil>", instanceSPAN, "</other_evil>"))
            <div>&lt;other_evil&gt;<span><evil>I will destroy you.</evil></span>&lt;/other_evil&gt;</div>
        """
        return self._escape_string

    @escape_string.setter
    def escape_string(self, value):
        if isinstance(value, bool):
            self._escape_string = value
        else:
            raise "".join(["The value must be False or True. Given: ", str(type(value))])

    @property
    def alternative_tag(self) -> str:
        """
        the alternative tag is used in the source_code and childern_indexes
        methods on elements that do not have a tag.
        In some cases it is necessary to have containers without a tag,
        but a tag is necessary for the methods mentioned (source_code and children_indexes).

        GET:

            Get alternative tag. By default the tag name is used if no new name is defined.
            If in the metaclass definition the tag is not assigned, the name "empty_tag" is used by default

        SET:

            Set the alternative tag of element
            @tag_name: Name of tag

        Example GET:

            >>> DIV = XmlConstructor.tagger('div')
            >>> instanceDIV = DIV()
            >>> print(instanceDIV.alternative_tag)
            div
            >>> METACLASS_WITHOUT_TAG = XmlConstructor.tagger('')
            >>> instanceEmptyTag = METACLASS_WITHOUT_TAG("content")
            >>> print(instanceEmptyTag.alternative_tag)
            empty_tag
            >>> print(instanceEmptyTag.source_code())
            EMPTY_TAG(
                'content'
            )
            >>> print(instanceEmptyTag.children_indexes())
            [ROOT_PARENT]<empty_tag> {}
                [0]"content"
            }


        Example SET:

            >>> METACLASS_WITHOUT_TAG = XmlConstructor.tagger('')
            >>> instanceEmptyTag = METACLASS_WITHOUT_TAG("content")
            >>> print(instanceEmptyTag.alternative_tag)
            empty_tag
            >>> print(instanceEmptyTag.source_code())
            EMPTY_TAG(
                'content'
            )
            >>> print(instanceEmptyTag.children_indexes())
            [ROOT_PARENT]<empty_tag> {}
                [0]"content"
            }
            >>> instanceEmptyTag.alternative_tag = "new_alternative_name_to_tag"
            >>> print(instanceEmptyTag.source_code())
            NEW_ALTERNATIVE_NAME_TO_TAG(
                'content'
            )
            >>> print(instanceEmptyTag.children_indexes())
            [ROOT_PARENT]<new_alternative_name_to_tag> {}
                [0]"content"
            }
        """
        return self._alternative_tag

    @alternative_tag.setter
    def alternative_tag(self, tag_name: str):
        self._alternative_tag = str(tag_name)

    @property
    def before_xml(self) -> str:
        """
        In some cases it is necessary to add a string before the
        generated xml, such as opening a comment, this is possible with
        this property

        GET:

            Get before_xml

        SET:

            Set a string to be inserted before the generated xml.
            @value: string to be insert

        Examples:

            >>> HTML = XmlConstructor.tagger('html')
            >>> P = XmlConstructor.tagger('p')
            >>> my_comment = P("My comment")
            >>> print(my_comment)
            <p>My comment</p>
            >>> print(my_comment.before_xml) # The default is empty

            >>> my_comment.before_xml = '<!--This is a comment.-->' #  Set a value in before_xml
            >>> my_comment.before_xml
            <!--This is a comment.-->
            >>> print(my_comment)
            <!--This is a comment.--><p>My comment</p>  #  The value to be inserted before xml
            >>> is_html5 = HTML()
            <html></html>
            >>> is_html5.before_xml = "<!DOCTYPE html>"
            >>> print(is_html5)
            <!DOCTYPE html><html></html>

        """
        return self._before_xml

    @before_xml.setter
    def before_xml(self, value: str):
        self._before_xml = str(value)

    @property
    def after_xml(self) -> str:
        """
        In some cases it is necessary to add a string after the
        generated html, such as closing a comment, this is possible with
        this property.

        GET:

            Get after_xml

        SET:

            Set a string to be inserted after the generated xml.
            @value: string to be insert

        Examples:

            >>> HTML = XmlConstructor.tagger('html')
            >>> P = XmlConstructor.tagger('p')
            >>> is_comment = P("This is a comment")
            >>> is_not_comment = P("This is not a comment")
            >>> html = HTML(is_comment, is_not_comment)
            >>> print(html)
            <html><p>This is a comment</p><p>This is not a comment</p></html>
            >>> print(is_comment.after_xml) # The default is empty

            >>> is_comment.before_xml = '<!--'
            >>> is_comment.after_xml = '-->' #  Set a value in after_xml
            >>> print(is_comment.after_xml)
            -->
            >>> print(is_comment)
            <!--<p>This is a comment</p>-->  #  The value to be inserted after xml
            >>> print(html)
            <html><!--<p>This is a comment</p>--><p>This is not a comment</p></html>
        """
        return self._after_xml

    @after_xml.setter
    def after_xml(self, value: str):
        self._after_xml = str(value)

    @property
    def content(self) -> FrozenContent:
        """
        The content property is one of the most important, with it you
        can add new elements in the root element. It is triggered when
        the element is instantiated, so elements can be added at creation
        time. You can also activate it later with the content property,
        the objects must be of type String, Other instances or insterable
        objects of the type List, Tuple and Set (You can also add a dict,
        but it will be treated by the attributes of the parent instance),
        within mentioned interfaces one can place all the objects already
        mentioned (nested).
        You can also add a function that returns any of the types
        mentioned above.

        GET:

            Gets a FrozenConten(tuple) with all elements

        SET:

            Adds new elements to the content. In it, String, Other
            instances (XmlConstructor), List, Tuple and Set are accepted.
            You can also add a dict, but it will be treated by the
            attributes of the parent instance.
            @contents: Elements to be added of type String, Other
                XmlConstructor instances or insterable objects of the
                type List, Tuple and Set (dict in special case).


        Example GET:

            >>> DIV = XmlConstructor.tagger("div")
            >>> Instance = DIV("This", "is", DIV("content")) # Set is triggered when the element is instantiated
            >>> print(Instance)
            <div>Thisis<div>content</div></div>
            >>> print(Instance.content)
            ('This', 'is', <class 'phanterpwa.xmlconstructor.XmlConstructor.tagger.
            <locals>.TAGGER'> {id: 14811344, tag: div})

        Example SET, String:

            >>> instanceDIV = XmlConstructor.tagger("div")()
            >>> instanceDIV.content = "my new content"
            >>> print(instanceDIV)
            <div>my new content</div>

        Example SET, XmlConstructor instance:

            >>> DIV = XmlConstructor.tagger("div")
            >>> STRONG = XmlConstructor.tagger("strong")
            >>> instanceDIV = DIV()
            >>> A = XmlConstructor.tagger("a", False)
            >>> instanceA = A("click ", STRONG("here"), _href="#my_url")
            >>> instanceDIV.content = instanceA
            >>> print(instanceDIV)
            <div><a href="#my_url">click <strong>here</strong></a></div>

        Example SET, using interable (List, Tuple, Set):

            >>> DIV = XmlConstructor.tagger("div")
            >>> SPAN = XmlConstructor.tagger("span")
            >>> HR = XmlConstructor.tagger("hr", True)
            >>> other_element = DIV([SPAN("Hello"), HR(), "World"])
            >>> list_el = [other_element, other_element]
            >>> set_el = set(list_el)
            >>> tuple_el = (list_el, HR(), set_el, "final string")
            >>> new_element = DIV()
            >>> new_element.content = ['my_', 'content', SPAN('span, span, span'), tuple_el]
            >>> print(new_element.humanize())
            <div>
              my_
              content
              <span>
                span, span, span
              </span>
              <div>
                <span>
                  Hello
                </span>
                <hr>
                World
              </div>
              <div>
                <span>
                  Hello
                </span>
                <hr>
                World
              </div>
              <hr>
              <div>
                <span>
                  Hello
                </span>
                <hr>
                World
              </div>
              final string
            </div>

        Example SET, function:

            >>> DIV = XmlConstructor.tagger("div")
            >>> SPAN = XmlConstructor.tagger("span")
            >>> instanceDIV.content = lambda: (SPAN("span * 3") * 3) + DIV("plus")
            >>> print(instanceDIV)
            <div><span>span * 3</span><span>span * 3</span><span>span * 3</span><div>plus</div></div>

        Example SET, special case, using dict:

            >>> DIV = XmlConstructor.tagger("div")
            >>> instanceDIV1 = DIV("content")
            >>> instanceDIV1.content = dict(_id="my_id")
            >>> print(instanceDIV1)
            <div id="my_id"></div>
            >>> instanceDIV1.content = ["new_content", dict(_class="my_class")]
            >>> print(instanceDIV1)
            <div class="my_class">new_content</div>
            >>> BR = XmlConstructor.tagger("br", True)
            >>> instanceDIV1.content = [set(["new_content", "new_content"]), [BR() * 2], {'_class': 'new_class'}]
            >>> instanceDIV1.close_void = True
            <div class="new_class">new_content<br /><br /></div>
        """
        return FrozenContent(self._content)

    @content.setter
    def content(self, contents: (list, tuple, set, str, dict, "function")):
        if isinstance(contents, (list, tuple, set)):
            temp_content = self._content_inter(contents)
            self._content = tuple(temp_content)
        else:
            self.content = (contents, )  # recursive

    @property
    def attributes(self) -> FrozenAttributes:
        """
        This property is also important, with it you can add the
        attributes in the instance of the element like classes, ids,
        styles, etc. It is stored in a dict, the keys must be compatible
        with the attributes of the HTML5 tags and the accepted values
        can be strings, lists of dictionaries. Keys must be started by
        underline (to avoid reserved python words, such as 'class' for
        example), keys that do not start with underline are stored in
        the Kargs attribute.

        GET:

            Returns an instance of FrozenAttributes (dict)

        SET:

            To add attributes it is recommended to use a dict, when a
            string is used a dict is created with the string as key and
            with the value True assigned.
            If the key values are added None or False, the attributes
            are ignored. If True is assigned, it will be an attribute
            with no content. With a function you can add values that
            would normally be ignored or modified.
            @attrs: Attributes to be added in the instance, can be a
            dict or string in special case.

        Example GET:

            >>> instanceDIV = XmlConstructor.tagger('div')
            >>> instanceDIV.attributes = {"_class": "my_class", "_id": "my_id"}
            >>> instanceDIV.attributes
            {"_class": "my_class", "_id": "my_id"}

        Example SET string:

            >>> BUTTON = XmlConstructor.tagger('button')
            >>> instanceBUTTON = BUTTON("Disabled Button")
            >>> instanceBUTTON.attributes = 'disabled'
            >>> print(instanceBUTTON)
            <button disabled>Disabled Button</button>

        Example SET dict:

            Each key of the attribute must begin with underline (_)
            (because of the keyword class and id), keys without underline
            will store in Kargs attribute.

            >>> DIV = XmlConstructor.tagger('div')
            >>> instanceDIV = DIV("My Content", _class="this will be replaced", go_to_kargs="go_to_kargs")
            >>> instanceDIV.attributes = {"_class": "my_class", "_id": "my_id"}
            >>> print(instanceDIV)
            <div class="my_class" id="my_id">My Content</div>

        Example SET dict, value None, False, True and Function:

            >>> DIV = XmlConstructor.tagger("div")
            >>> SPAN = XmlConstructor.tagger("span")
            >>> instanceDIV = DIV(_class="my_class", _underline="_underline", without_underline="without_underline")
            >>> print(instanceDIV)
            <div class="my_class" underline="_underline"></div>
            >>> print(instanceDIV.attributes)
            {'_class': 'my_class', '_underline': '_underline'}
            >>> print(instanceDIV.kargs)
            {'without_underline': 'without_underline'}
            >>> instanceDIV.attributes = {"_teste": lambda: "false"}
            >>> print(instanceDIV)
            <div teste=false></div>
            >>> print(instanceDIV.attributes)
            {'_teste': <function <lambda> at 0x02CD7858>}
            >>> instanceDIV = DIV(_id="my_class", _bye=None, _class=False)
            >>> print(instanceDIV)
            <div id="my_class"></div>
            >>> print(instanceDIV.attributes)
            {'_id': 'my_class'}
        """
        return FrozenAttributes(self._attributes)

    @attributes.setter
    def attributes(self, attrs):
        if isinstance(attrs, str):
            a = self._vk(attrs.strip())
            if not a.startswith("_"):
                a = "".join(["_", a])
            self._attributes = {a: True}
            self._xml_attributes = a
        elif isinstance(attrs, dict):
            fill_attr = {}
            str_attr = ""
            for k in attrs.keys():
                v = attrs[k]
                if k.startswith("_") and not (v is None or v is False):
                    if k in ["_class", "_id", "_style", "_href", "_title", "_alt", "_src"]:
                        fill_attr[k] = v
                        v = saxutils.quoteattr(v)
                        str_attr = " ".join([str_attr, "=".join([k[1:], v])])
                    else:
                        k = self._vk(k)
                        if attrs[k] is True:
                            fill_attr[k] = True
                            str_attr = " ".join([str_attr, k[1:]])
                        elif callable(attrs[k]):
                            fill_attr[k] = attrs[k]
                            str_attr = " ".join([str_attr, "=".join([k[1:], str(attrs[k]())])])
                        else:
                            fill_attr[k] = v
                            v = self._process_attrs_values(v)
                            if isinstance(v, (list, dict)):
                                v = json.dumps(v)
                            v = saxutils.quoteattr(v)
                            str_attr = " ".join([str_attr, "=".join([k[1:], v])])
                else:
                    self.kargs[k] = attrs[k]

            self._attributes = fill_attr
            self._xml_attributes = str_attr.strip()
        else:
            raise TypeError("The attributes must be a dict or string to set HTML attributes without values")

    @property
    def src_attr_dict(self) -> "True, False or None":
        """
        This property affects the souce_code method, You can put 3 values,
        None for automatic, False for disabled, and True for enabled.

        GET:

            Gets the current state of this property. None is default

        SET:

            Sets the value for this property
            @value: Sets here None, True or False
            In html, the elements attribute keys accept the minus
            character (-) in their name, in python no, we can
            define the attributes using arguments when
            instantiating, but this character can not be used, so
            we use a dict to get around the problem.

        Example GET

            >>> DIV = XmlConstructor.tagger("div")
            >>> instanceDIV = DIV()
            >>> instanceDIV.src_attr_dict
            None

        Example SET, None (default).

            >>> from phanterpwa.helpers import (DIV, HR, SPAN)
            >>> instanceDIV = DIV(HR(), SPAN(_class="the valid karg"))
            >>> instanceDIV.attributes = {"_invalid-attr-in-karg": "the_key_is_valis_in_html5"}
            >>> print(instanceDIV.source_code())
            DIV(
                HR(
                ),
                SPAN(
                    _class='the valid karg'
                ),
                **{
                    '_invalid-attr-in-karg': 'the_key_is_valis_in_html5'
                }
            )

        Note that in the DIV element a dictionary was used to add
        the attributes and in the SPAN element an argument.

        Example SET, True

            >>> from phanterpwa.helpers import (DIV, HR, SPAN)
            >>> instanceDIV = DIV(HR(), SPAN(_class="the valid karg"))
            >>> instanceDIV.attributes = {"_invalid-attr-in-karg": "the_key_is_valis_in_html5"}
            >>> print(instanceDIV.source_code())
            DIV(
                HR(
                ),
                SPAN(
                    **{
                        '_class': 'the valid karg'
                    }
                ),
                **{
                    '_invalid-attr-in-karg': 'the_key_is_valis_in_html5'
                }
            )

        Note that in all elements a dictionary was used to add the
        attributes.

        Example SET, False (Not recommended)

            >>> from phanterpwa.helpers import (DIV, HR, SPAN)
            >>> instanceDIV = DIV(HR(), SPAN(_class="the valid karg"))
            >>> instanceDIV.attributes = {"_invalid-attr-in-karg": "the_key_is_valis_in_html5"}
            >>> print(instanceDIV.source_code())
            Traceback (most recent call last):
              ...
            ValueError: The argument name is invalid, given: _invalid-attr-in-karg

        It generates an error because the '_invalid-attr-in-karg' value
        can not be used as argument name in python.
        This option should only be used when you are sure that the keys
        of the html attributes are values that can be used as name
        identifier.
        """
        return self._src_attr_dict

    @src_attr_dict.setter
    def src_attr_dict(self, value: "True, False or None"):
        if isinstance(value, bool) or (value is None):
            self._src_attr_dict = value
        else:
            raise TypeError("The value must be boolean or None. given: {0}".format(str(type(value))))

    @property
    def i18nInstance(self):
        """
        This property makes it possible to add an instance of the
        Translation object of the i18n module located in the phanterpwa
        package, this instance will be used to translate the strings.
        For more details see the documentation for the i18n method and
        the dictionary and tag_translation properties.

        GET:

            Get the current phanterpwa.i18n.Translator instance

        SET:

            Set the instance of object phanterpwa.i18n.Translator
            @value: Instance of phanterpwa.i18n.Translator object

        Example:

            >>> from phanterpwa.helpers import DIV, P
            >>> from phanterpwa.i18n import Translator
            >>> instanceDIV = DIV(P("Monkey"))
            >>> print(instanceDIV.humanize())
            <div>
              <p>
                Monkey
              </p>
            </div>
            >>> i18nMyInstance = Translator("path_of_languages", debug=True)
            >>> i18nMyInstance.translate("pt-BR", "Monkey", "Macaco")
            >>> i18nMyInstance.translate("fr", "Monkey", "Singe")
            >>> i18nMyInstance.translate("es", "Monkey", "Mono")
            >>> instanceDIV.i18nInstance = i18nMyInstance
            >>> print(instanceDIV.humanize())  # The default of tag_translarion is "span"
            <div>
              <p>
                <span phanterpwa_i18n='{"pt-BR": {"Monkey": "Macaco"}, "fr": {"Monkey": "Singe"}, "es": {"Monkey": "Mono"}}'>Monkey</span>
              </p>
            </div>
            >>> instanceDIV.dictionary = 'fr'  # set specific dictionary
            >>> print(instanceDIV.humanize())
            <div>
              <p>
                Singe
              </p>
            </div>
        """
        return self._i18nInstance

    @i18nInstance.setter
    def i18nInstance(self, value):
        if value is None:
            self._i18nInstance = None
        else:
            instancei18n = self._validate_i18nInstance(value)
            self._i18nInstance = instancei18n
            for x in self:
                if isinstance(x, XmlConstructor):
                    x._i18nInstance = instancei18n

    @property
    def tag_translation(self):
        """
        With the i18n method you can perform two ways of translating
        strings, one of them makes more sense to be used on the server
        side and the other on the client side. With this property you
        enable the translation that is best for use on the client side,
        you define which element tag to use, the default is the 'span'.
        This property is effective only if there is a instance of the
        Translation object of the i18n module located in the phanterpwa
        package set on i18nInstance property.
        For more details read the documentation on the i18n method and
        dictionary and i18nInstance properties.

        GET:

            get current tag. (default is "span")

        SET:

            Set a new tag_translation. When you set a new valid tag name
            the dictionary property is automatically changed to None.
            @value: new tag name

        Example:

            >>> from phanterpwa.helpers import DIV, P
            >>> from phanterpwa.i18n import Translator
            >>> i18nMyInstance = Translator("path_of_languages", debug=True)
            >>> i18nMyInstance.translate("pt-BR", "Apple", "Maçã")
            >>> i18nMyInstance.translate("pt-BR", "Orange", "Laranja")
            >>> i18nMyInstance.translate("pt-PT", "Orange", "Laranja")
            >>> i18nMyInstance.translate("pt-PT", "Grape", "Uva")
            >>> instanceDIV = DIV(P("Apple", "Orange", "Grape", "Do not have translate"))
            >>> instanceDIV.i18nInstance = i18nMyInstance
            >>> print(instanceDIV.tag_translation)  # tag_translation is "span" by default
            span
            >>> print(instanceDIV.humanize())
            <div>
              <p>
                <span phanterpwa_i18n='{"pt-BR": {"Apple": "Ma\\u00e7\\u00e3"}}'>Apple</span>
                <span phanterpwa_i18n='{"pt-BR": {"Orange": "Laranja"}, "pt-PT": {"Orange": "Laranja"}}'>Orange</span>
                <span phanterpwa_i18n='{"pt-PT": {"Grape": "Uva"}}'>Grape</span>
                <span>Do not have translate</span>
              </p>
            </div>
            >>> instanceDIV.tag_translation = None
            >>> print(instanceDIV.humanize())
            <div>
              <p>
                Apple
                Orange
                Grape
                Do not have translate
              </p>
            </div>
            >>> instanceDIV.tag_translation = "i18n"
            >>> print(instanceDIV.humanize())
            <div>
              <p>
                <i18n phanterpwa_i18n='{"pt-BR": {"Apple": "Ma\\u00e7\\u00e3"}}'>Apple</i18n>
                <i18n phanterpwa_i18n='{"pt-BR": {"Orange": "Laranja"}, "pt-PT": {"Orange": "Laranja"}}'>Orange</i18n>
                <i18n phanterpwa_i18n='{"pt-PT": {"Grape": "Uva"}}'>Grape</i18n>
                <i18n>Do not have translate</i18n>
              </p>
            </div>

        Note that for entries a span has been created with an attribute
        called phanterpwa-i18n, it has the list of dictionaries followed
        by the original entry and their translation, so on the client
        side just use a jquery plug-in to capture the json in the
        element attribute span and add to your content.
        """
        return self._tag_translation

    @tag_translation.setter
    def tag_translation(self, value):
        if isinstance(value, str):
            self._dictionary = None
            self._tag_translation = value
            for x in self:
                if isinstance(x, XmlConstructor):
                    x._dictionary = None
                    x._tag_translation = value
        elif value is None:
            self._tag_translation = value
            for x in self:
                if isinstance(x, XmlConstructor):
                    x._tag_translation = value
        else:
            raise "".join(["The value must be String. Given: ", str(type(value))])

    @property
    def dictionary(self) -> (str, None):
        """
        With the i18n method you can perform two ways of translating
        strings, one of them makes more sense to be used on the server
        side and the other on the client side. With this property you
        enable the translation that is best for use on the server side.
        The translation is direct. Here you define which dictionary will
        be used for translation.
        This property is effective only if there is a instance of the
        Translation object of the i18n module located in the
        phanterpwa package set in i18nInstance property.
        For more details read the documentation on the i18n method and
        tag_translation and i18nInstance properties.

        GET:

            Set the current dictionary. (default is None)

        SET:

            Set a dictionary. When setting a dictionary the
            tag_translation property automatically changes to None.
            @value: dictionary name

        Example:

            >>> from phanterpwa.helpers import DIV, P
            >>> from phanterpwa.i18n import Translator
            >>> instanceDIV = DIV(P("The book is on the table"))
            >>> print(instanceDIV.humanize())
            <div>
              <p>
                The book is on the table
              </p>
            </div>
            >>> i18nMyInstance = Translator("path_of_languages", debug=True)
            >>> i18nMyInstance.translate("pt-BR", "The book is on the table", "O livro está sobre a mesa")
            >>> i18nMyInstance.translate("fr", "The book is on the table", "Le livre est sur la table")
            >>> i18nMyInstance.translate("es", "The book is on the table", "El libro está sobre la mesa")
            >>> instanceDIV.i18nInstance = i18nMyInstance
            >>> print(instanceDIV.humanize())  # The default of tag_translarion is "span" and dictionary is None
            <div>
              <p>
                <span phanterpwa_i18n='{"es": {"The book is on the table": "El libro est\\u00e1 sobre la mesa"}, "fr": {"The book is on the table": "Le livre est sur la table"}, "pt-BR": {"The book is on the table": "O livro est\\u00e1 sobre a mesa"}}'>The book is on the table</span>
              </p>
            </div>
            >>> instanceDIV.dictionary = 'fr'  # set specific dictionary, tag_translation automatically changes to None
            >>> print(instanceDIV.humanize())
            <div>
              <p>
                Le livre est sur la table
              </p>
            </div>

        """
        return self._dictionary

    @dictionary.setter
    def dictionary(self, value: (str, None)):
        if isinstance(value, str) or value is None:
            self._dictionary = value
            self.tag_translation = None
            for x in self:
                if isinstance(x, XmlConstructor):
                    x._dictionary = value
                    x._tag_translation = None
        else:
            raise TypeError("".join(["The dictionary name must be None or String, given: ", str(type(value))]))

    @property
    def do_not_translate(self) -> list:
        """
        This property stores a list of strings that should be
        ignored in the translation. Read the documentation for the i18n
        method and tag_translate, dictionary, and i18nInstance
        properties for more details.
        This property is effective only if there is an instance of
        phanterpwa.i18n.Translator on i18nInstance and a valid parameter
        in the tag_translation or dictionary property.

        GET:

            Get the current list string. (default is empty list [])

        SET:

            Set the list string that should be ignored.
            @value: list string

        Example:

            >>> from phanterpwa.helpers import DIV, P
            >>> from phanterpwa.i18n import Translator
            >>> instanceDIV = DIV(P("The colors ", " Blue ", "and", " Green ", "are not translated."))
            >>> print(instanceDIV.xml())
            <div><p>The colors  Blue and Green are not translated.</p></div>
            >>> i18nMyInstance = Translator("path_of_languages", debug=True)
            >>> i18nMyInstance.translate("pt-BR", "The colors ", "As cores ")
            >>> i18nMyInstance.translate("pt-BR", " Blue ", " Azul ")
            >>> i18nMyInstance.translate("pt-BR", "and", "e")
            >>> i18nMyInstance.translate("pt-BR", " Green ", "Verde")
            >>> i18nMyInstance.translate("pt-BR", "are not translated.", "não são traduzidas.")
            >>> instanceDIV.i18nInstance = i18nMyInstance
            >>> print(instanceDIV.humanize())
            <div>
              <p>
                <span phanterpwa_i18n='{"pt-BR": {"The colors ": "As cores "}}'>The colors </span>
                <span phanterpwa_i18n='{"pt-BR": {" Blue ": " Azul "}}'> Blue </span>
                <span phanterpwa_i18n='{"pt-BR": {"and": "e"}}'>and</span>
                <span phanterpwa_i18n='{"pt-BR": {" Green ": "Verde"}}'> Green </span>
                <span phanterpwa_i18n='{"pt-BR": {"are not translated.": "n\\u00e3o s\\u00e3o traduzidas."}}'>are not translated.</span>
              </p>
            </div>
            >>> instanceDIV.do_not_translate = [" Blue ", " Green "]
            >>> print(instanceDIV.humanize())
            <div>
              <p>
                <span phanterpwa_i18n='{"pt-BR": {"The colors ": "As cores "}}'>The colors </span>
                 Blue 
                <span phanterpwa_i18n='{"pt-BR": {"and": "e"}}'>and</span>
                 Green 
                <span phanterpwa_i18n='{"pt-BR": {"are not translated.": "n\\u00e3o s\\u00e3o traduzidas."}}'>are not translated.</span>
              </p>
            </div>
            >>> instanceDIV.dictionary = "pt-BR"
            >>> print(instanceDIV.humanize())
            <div>
              <p>
                As cores 
                 Blue 
                e
                 Green 
                não são traduzidas.
              </p>
            </div>
        """
        return self._do_not_translate

    @do_not_translate.setter
    def do_not_translate(self, value: list):
        if isinstance(value, (list, tuple, set)):
            self._do_not_translate = list(value)
        else:
            raise TypeError("".join([
                "do_not_translate must be a list, tuple or set with strings. Given: ",
                str(type(value))
            ]))

    @property
    def never_translate(self):
        return self._never_translate

    @never_translate.setter
    def never_translate(self, value: bool):
        if isinstance(value, bool):
            self._never_translate = value
        else:
            raise ValueError("The never_translate must be boolean. Given: {0}".format(type(value))) 

    @property
    def delimiters(self):
        """
        This property changes the delimiters of the formatter method.

        GET:

            returns the current pair of delimiters.

        SET:

            For a new pair of delimiters two strings are required in a list or
            tuple, the left string will be the left delimiter and vice versa.
            @value: Pair of de delimiters.

        Example:

            >>> from phanterpwa.helpers import DIV
            >>> instanceDIV = DIV("{{Change_this}} or not ", "[[change]]")
            >>> print(instanceDIV)
            <div>{{Change_this}} or not [[change]]</div>
            >>> instanceDIV.formatter(Change_this="Changed", change="hooooo nooooooo!")
            >>> print(instanceDIV)
            <div>Changed or not [[change]]</div>
            >>> print(instanceDIV.delimiters)
            ['{{', '}}']
            >>> instanceDIV.delimiters = ["[[", "]]"]
            >>> print(instanceDIV.delimiters)
            ['[[', ']]']
            >>> print(instanceDIV)
            <div>{{Change_this}} or not hooooo nooooooo!</div>
        """
        return self._delimiters

    @delimiters.setter
    def delimiters(self, value):
        if isinstance(value, (list, tuple)):
            if all([(len(value) == 2), (isinstance(value[0], str)), (isinstance(value[1], str))]):
                self._delimiters = value
            else:
                raise ValueError("The delimiters must be list os tuple with two strings. Given: {0}".format(value))

    @property
    def formatter_list_keys(self):
        """
        GET:

            This property lists all the keys in the generated xml that are within
            the delimiters (see the delimiters property documentation), keys can be
            converted to values with the formatter method (see the formatter
            documentation too)

        Example:

            >>> from phanterpwa.helpers import DIV, SPAN, A
            >>> instanceDIV = DIV(
                    SPAN(
                        "This is value one: {{value-one}}",
                        "{this is ignored}"
                    ),
                    A("{{message_link}}", _href="{{attr_indefined}}"),
                    SPAN("I want repeat: {{repeat}} {{repeat}} {{repeat}}.")
                )
            >>> print(instanceDIV.formatter_list_keys)
            ['value-one', 'message_link', 'attr_indefined', 'repeat']
        """
        e = self.xml()
        r = "".join([re.escape(self.delimiters[0]), r"([_a-zA-Z][\w-]+)", re.escape(self.delimiters[1])])
        c = re.compile(r)
        li = set()
        for x in c.findall(e):
            li.add(x)
        return list(li)

    @property
    def sass_vars(self):
        """
        With this property you can view the variables contained in the sass file
        applied in the sass_file method, you can also change the values of the
        variables, as this change does not change the original file, but if a
        target is detected in the sass_file method the change reflects in its
        content.

        GET:
            You can view the variables contained in the sass file applied in the
            sass_file method.

        SET:
            You can change the values of the variables contained in the sass
            file applied in the sass_file method
            @value: Dictionary with keys referencing variables and values
                changing current value.

        Examples:

            Consider the sass file (my_sass.sass) with the following content:
                '''
                $COLOR: red
                $CONTAINERWIDTH: 60px
                $CONTAINERHEIGHT: 60px
                $BORDERRADIUS: 0
                .example_container
                  *
                    box-sizing: border-box
                  .my_square
                    display: inline-block
                    position: relative
                    width: $CONTAINERWIDTH
                    height: $CONTAINERHEIGHT
                    .other_square
                      width: 100%
                      height: 100%
                      border-radius: $BORDERRADIUS

                '''
            >>> from phanterpwa.helpers import DIV
            >>> instanceDIV = DIV(DIV(DIV(_class="other_square"), _class="my_square"), _class="example_container")
            >>> instanceDIV.sass_file("my_sass.sass")
            >>> print(instanceDIV.sass_vars)
            {'COLOR': 'red', 'CONTAINERWIDTH': '60px', 'CONTAINERHEIGHT': '60px', 'BORDERRADIUS': '0'}

        Let's try modifying the COLOR and BORDERRADIUS variables.
        The original file will not be modified.

            >>> instanceDIV.sass_vars = {"COLOR": "orange", "BORDERRADIUS": "100%"}
            >>> print(instanceDIV.sass_vars)
            {'COLOR': 'orange', 'CONTAINERWIDTH': '60px', 'CONTAINERHEIGHT': '60px', 'BORDERRADIUS': '100%'}
            >>> print(instanceDIV.sass)
            $COLOR: orange
            $CONTAINERWIDTH: 60px
            $CONTAINERHEIGHT: 60px
            $BORDERRADIUS: 100%
            .example_container
              *
                box-sizing: border-box
              .my_square
                display: inline-block
                position: relative
                width: $CONTAINERWIDTH
                height: $CONTAINERHEIGHT
                .other_square
                  width: 100%
                  height: 100%
                  border-radius: $BORDERRADIUS
        """
        if self._sass:
            self._sass_vars = sass_map_vars(self._sass)
            return self._sass_vars
        else:
            raise SyntaxError("A sass file must be defined in the sass method to use this property.")

    @sass_vars.setter
    def sass_vars(self, value):
        if self._sass:
            self._sass = sass_change_vars(self._sass, value)
            self._sass_vars = sass_map_vars(self._sass)
            self.css(self._minify_css, self._target_css)
            if self._target_sass:
                with open(self._target_sass, 'w', encoding='utf-8') as f:
                    f.write(self._sass)
            return self._sass
        else:
            raise SyntaxError("A sass file must be defined in the sass method to use this property.")

    @property
    def sass(self):
        """
        GET:
            With this property you can view the current sass applied to the
            sass_file method.
        """
        if self._sass:
            return self._sass
        else:
            raise SyntaxError("A sass file must be defined in the sass method to use this property.")

    def sass_file(self,
        file_name: "path of sass file",
        variables: dict=None,
        target: "path of target file"=None) -> str:
        """
        With this method it is possible to associate a file sass to the
        instance, so with the method css can be generated a minified or not with
        the associated sass. You can also change the values of the variables in
        the code read from the sass file.
        @file_name: sass file
        @variables: Dictionary with the name of the variables and the new values.
            (Default is None)
        @target: defines a file to which the generated content will be saved.

        Example:

            Consider the sass file (my_sass.sass) with the following content:
                '''
                $COLOR: red
                $CONTAINERWIDTH: 60px
                $CONTAINERHEIGHT: 60px
                $BORDERRADIUS: 0
                .example_container
                  *
                    box-sizing: border-box
                  .my_square
                    display: inline-block
                    position: relative
                    width: $CONTAINERWIDTH
                    height: $CONTAINERHEIGHT
                    .other_square
                      width: 100%
                      height: 100%
                      border-radius: $BORDERRADIUS

                '''
            >>> from phanterpwa.helpers import DIV
            >>> instanceDIV = DIV(DIV(DIV(_class="other_square"), _class="my_square"), _class="example_container")
            >>> print(instanceDIV.sass_file("my_sass.sass"))
            $COLOR: red
            $CONTAINERWIDTH: 60px
            $CONTAINERHEIGHT: 60px
            $BORDERRADIUS: 0
            .example_container
              *
                box-sizing: border-box
              .my_square
                display: inline-block
                position: relative
                width: $CONTAINERWIDTH
                height: $CONTAINERHEIGHT
                .other_square
                  width: 100%
                  height: 100%
                  border-radius: $BORDERRADIUS

        Let's try modifying the COLOR and BORDERRADIUS variables.
        The original file will not be modified.

            >>> print(instanceDIV.sass_file("my_sass.sass", {"COLOR": "orange", "BORDERRADIUS": "100%"}))
            $COLOR: orange
            $CONTAINERWIDTH: 60px
            $CONTAINERHEIGHT: 60px
            $BORDERRADIUS: 100%
            .example_container
              *
                box-sizing: border-box
              .my_square
                display: inline-block
                position: relative
                width: $CONTAINERWIDTH
                height: $CONTAINERHEIGHT
                .other_square
                  width: 100%
                  height: 100%
                  border-radius: $BORDERRADIUS
        """

        if os.path.exists(file_name) and os.path.isfile(file_name):
            name = os.path.basename(file_name)
            ext = name.split(".")[-1]
            if ext == "sass":
                sass = ""
                with open(file_name, 'r', encoding="utf-8") as f:
                    sass = f.read()
                self._sass = sass
                if variables:
                    self.sass_vars = variables
                if sass and self._sass is None:
                    raise Exception("Could not generate valid sass when trying to change variables.")
                else:
                    if target:
                        if target[-5:] != ".sass":
                            target = "".join([target, ".sass"])
                        with open(target, 'w', encoding='utf-8') as f:
                            f.write(self._sass)
                        self._target_sass = target
                    else:
                        self._target_sass = None
                    return self._sass
            else:
                raise IOError("The file don't have '.sass' extension")
        else:
            raise IOError("The file not exist. Given: {0}".format(file_name))

    def css(self, minify=True, target=None):
        """
        After defining a sass file in the sass method, a css can be generated
        with this method.
        @minify: With minify active css will be minified.
        @target: defines a file to which the generated content will be saved.

        Example:
            Consider the sass file (my_sass.sass) with the following content:
                '''
                $COLOR: red
                $CONTAINERWIDTH: 60px
                $CONTAINERHEIGHT: 60px
                $BORDERRADIUS: 0
                .example_container
                  *
                    box-sizing: border-box
                  .my_square
                    display: inline-block
                    position: relative
                    width: $CONTAINERWIDTH
                    height: $CONTAINERHEIGHT
                    .other_square
                      width: 100%
                      height: 100%
                      border-radius: $BORDERRADIUS
                '''
            >>> from phanterpwa.helpers import DIV
            >>> instanceDIV = DIV(DIV(DIV(_class="other_square"), _class="my_square"), _class="example_container")
            >>> instanceDIV.sass_file("my_sass.sass")
            >>> print(instanceDIV.css(minify=False))
            .example_container * {
              box-sizing: border-box;
            }

            .example_container .my_square {
              display: inline-block;
              position: relative;
              width: 60px;
              height: 60px;
            }

            .example_container .my_square .other_square {
              width: 100%;
              height: 100%;
              border-radius: 100%;
            }
        """

        self._minify_css = minify
        try:
            import sass
        except ImportError as e:
            raise e("libsass required")
        if self._sass:
            css = ""
            c = self._sass
            if minify:
                css = sass.compile(string=c, indented=True, output_style="compressed")
            else:
                css = sass.compile(string=c, indented=True, output_style="expanded")
            if target:
                if target[-4:] != ".css":
                    target = "".join([target, ".css"])
                with open(target, 'w', encoding='utf-8') as f:
                    f.write(css)
                self._target_css = target
            else:
                self._target_css = None
            return css
        else:
            raise SyntaxError("A sass file must be defined in the sass method to use this property.")

    def formatter(self, value=None, **kvalue):
        """
        This method uses the format method used in strings, it is applied over
        the xml generated in the xml and humanized methods. The difference with
        the format method is that it accepts as its first argument a dictionary
        or a series of arguments with identifiers (kargs).

            @value: Dictionary with the identifier to be found with their
            respective values.
            @Kvalue: Arguments with their respective identifiers and
            values.

        Example:

            >>> from phanterpwa.helpers import DIV, SPAN, A
            >>> instanceDIV = DIV(
                    SPAN(
                        "This is value one: {{value-one}}",
                        "{this is ignored}"
                    ),
                    A("{{message_link}}", _href="{{attr_indefined}}"),
                    SPAN("I want repeat: {{repeat}} {{repeat}} {{repeat}}.")
                )
            >>> print(instanceDIV.humanize())
            <div>
              <span>
                This is value one&#58; {{value-one}}
                {this is ignored}
              </span>
              <a href="{{attr_indefined}}">
                {{message_link}}
              </a>
              <span>
                I want repeat&#58; {{repeat}} {{repeat}} {{repeat}}.
              </span>
            </div>
            >>> instanceDIV.formatter({
                    "value-one": "1",
                    "repeat": "Ha",
                    "message_link": "click here!",
                    "attr_indefined": "http://localhost",
                    "this is ignored": "is it works?"
                })
            >>> print(instanceDIV.humanize())
            <div>
              <span>
                This is value one&#58; 1
                {this is ignored}
              </span>
              <a href="http://localhost">
                click here!
              </a>
              <span>
                I want repeat&#58; Ha Ha Ha.
              </span>
            </div>

        The value-one name cannot be used as an argument identifier, so a
        dictionary was used to pass the arguments, it is possible to merge,
        see:
            >>> instanceDIV.formatter(
                    {"value-one": "1", "this is ignored": "is it works?"},
                    repeat="Ha",
                    message_link="click here!",
                    attr_indefined="http://localhost"
                )
            >>> print(instanceDIV.humanize())
            <div>
              <span>
                This is value one&#58; 1
                {this is ignored}
              </span>
              <a href="http://localhost">
                click here!
              </a>
              <span>
                I want repeat&#58; Ha Ha Ha.
              </span>
            </div>

        Or you can put it all in one dictionary and unpack with **. Note that in
        the first example the dictionary was passed as the first argument.

            >>> instanceDIV.formatter(**{
                    "value-one": "1",
                    "repeat": "Ha",
                    "message_link": "click here!",
                    "attr_indefined": "http://localhost",
                    "this is ignored": "is it works?"
                })
            >>> print(instanceDIV.humanize())
            <div>
              <span>
                This is value one&#58; 1
                {this is ignored}
              </span>
              <a href="http://localhost">
                click here!
              </a>
              <span>
                I want repeat&#58; Ha Ha Ha.
              </span>
            </div>
        """
        if value:
            if isinstance(value, dict):
                nvalue = value
                if kvalue:
                    for x in kvalue:
                        nvalue[x] = kvalue[x]
                self._formatter = nvalue
                return self._interpolate(self.xml(), nvalue, self.delimiters)
            else:
                raise "".join(["To format the string, only one dict is accepted. given: ", str(type(value))])
        else:
            self._formatter = kvalue
            return self._interpolate(self.xml(), kvalue, self.delimiters)

    def children_indexes(self) -> str:
        """
        With the children_indexes method returns a string with the xml
        structure showing its respective indexes. With indexes you can
        easily access each element.

        Example:

            >>> from phanterpwa.helpers import (HTML, HEAD, META, TITLE, BODY, MAIN, XML, FOOTER)
            >>> instanceHTML = HTML(
                HEAD(
                    META(_charset="utf-8"),
                    TITLE("PhanterPWA")),
                BODY(
                    MAIN(
                        XML("<strong>xml instance not escape</strong>"),
                        "<strong>this will escape<strong>"
                    ),
                    FOOTER("PhanterJR")
                )
            )

        XML (CONCATENATE too) object is omitted in xml generated.

            >>> print(instanceHTML.html(minify=False))
            <html>
              <head>
                <meta charset="utf-8">
                <title>
                  PhanterPWA
                </title>
              </head>
              <body>
                <main>
                  <strong>xml instance not escape</strong>
                  &lt;strong&gt;this will escape&lt;strong&gt;
                </main>
                <footer>
                  PhanterJR
                </footer>
              </body>
            </html>
            >>> print(instanceHTML.children_indexes())
            [ROOT_PARENT]<html> {}
                [0]<head> {}
                    [0][0]<meta> {"_charset": "utf-8"}
                    [0][1]<title> {}
                        [0][1][0]"PhanterPWA"
                [1]<body> {}
                    [1][0]<main> {}
                        [1][0][0]<xml> {}
                            [1][0][0][0]"<strong>xml instance not escape</strong>"
                        [1][0][1]"<strong>this will escape<strong>"
                    [1][1]<footer> {}
                        [1][1][0]"PhanterJR"

        Note that in the html method (xml() and humanize() method too)
        the XML (CONCATENATE too) object is omitted, but in the
        children_indexes method its index is shown.
        """
        s = "".join(["[ROOT_PARENT]<", self.tag if self.tag else self.alternative_tag, "> ",
            json.dumps(self._attributes) if self.tag else "{}"])
        c = self.all_children
        for x in c:
            lvl = 0
            for i in x:
                if i == "[":
                    lvl += 1
            if isinstance(c[x], XmlConstructor):
                s = "".join([s, "\n", " " * (lvl * 4), x,
                    "<", c[x].tag if c[x].tag else c[x].alternative_tag, "> ",
                    json.dumps(c[x]._attributes) if c[x].tag else "{}"]
                )
            else:
                s = "".join([s, "\n", " " * (lvl * 4), x, saxutils.unescape(saxutils.quoteattr(c[x]))])
        return s

    def source_code(self,
        add_imports: bool=False,
        phanterpwa_helpers: bool=False,
        instance_name: str="html",
        translate: bool=False) -> str:
        """
        With this method it is possible to generate static source code
        of the instance, it is useful to reverse engineer when used in
        conjunction with the HtmlToXmlConstructor object located in the
        reversexml module of the phanterpwa package. Another advantage
        is that the generated code is indented to facilitate and read.
        You can also add the necessary imports, using or not the helpers
        module of the phanterpwa package.
        It is important to read the documentation of the src_attr_dict
        property.

        Args:

            @add_imports: add necessary imports in code This arguments
            will take effect if add_imports is true.
            @phanterpwa_helpers: user phanter.helpers import.
            @instance_name: The generated code is assigned to a variable
            with the name assigned here.
            @translate: If True, the generated source_code strings will
            be translated.

        Examples:

            >>> from phanterpwa.helpers import (DIV, HR, SPAN)
            >>> instanceDIV = DIV(XML("<strong>not escape</strong>"), HR(), SPAN("without xml?", _class="the valid karg"))
            >>> instanceDIV.attributes = {"_invalid-attr-in-karg": "the_key_is_valis_in_html5"}
            >>> print(instanceDIV.source_code())
            DIV(
                XML(
                    '<strong>not escape</strong>'
                ),
                HR(
                ),
                SPAN(
                    'without xml?',
                    _class='the valid karg'
                ),
                **{
                    '_invalid-attr-in-karg': 'the_key_is_valis_in_html5'
                }
            )
            >>> print(instanceDIV.source_code(add_imports=True, phanterpwa_helpers=True))
            from phanterpwa.helpers import (
                XML,
                HR,
                SPAN,
                DIV
            )


            html = DIV(
                XML(
                    '<strong>not escape</strong>'
                ),
                HR(
                ),
                SPAN(
                    'without xml?',
                    _class='the valid karg'
                ),
                **{
                    '_invalid-attr-in-karg': 'the_key_is_valis_in_html5'
                }
            )
            >>> instanceDIV.close_void = True
            >>> print(instanceDIV.source_code(add_imports=True, instance_name="MY_INSTANCE"))
            from phanterpwa.xmlconstructor import XmlConstructor
            from phanterpwa.xss import XssCleaner


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
                    self.alternative_tag = "xml"
                    self.sanitize = sanitize
                    self.permitted_tags = permitted_tags
                    self.allowed_attributes = allowed_attributes
                    self.strip_disallowed = False
                    self.escape_string = False

                def xml(self):
                    xml = ""
                    if self.content:
                        xml = self.xml_content
                    if self.sanitize:
                        xml = "".join([self.before_xml, xml, self.after_xml])
                        return self.strip(xml)
                    xml = "".join([self.before_xml, xml, self.after_xml])
                    return xml


            HR = XmlConstructor.tagger('hr', True)
            SPAN = XmlConstructor.tagger('span')
            DIV = XmlConstructor.tagger('div')


            MY_INSTANCE = DIV(
                XML(
                    '<strong>not escape</strong>'
                ),
                HR(
                ),
                SPAN(
                    'without xml?',
                    _class='the valid karg'
                ),
                **{
                    '_invalid-attr-in-karg': 'the_key_is_valis_in_html5'
                }
            )

            MY_INSTANCE.close_void = True
        """
        if not instance_name.isidentifier():
            raise ValueError("The name '{0}' in instance_name can not be used as identifier".format(instance_name))
        src = ""
        space = " " * (self._indent_level * 4)
        if not self.void:
            src = "".join([
                self.tag.upper() if self.tag else self.alternative_tag.upper(), "(",
                self._src_content(translate),
                self._src_attr(space + "    "),
                "\n",
                space,
                ")" if self._indent_level == 0 else "),"
            ])
        else:
            src = "".join([
                self.tag.upper() if self.tag else self.alternative_tag.upper(),
                "(",
                self._src_attr(space + "    "),
                "\n",
                space,
                ")" if self._indent_level == 0 else "),"])
        src = "".join(["\n" if self._indent_level != 0 else "", space, src])
        if add_imports and self._indent_level == 0:
            str_imp = ""
            unics_tag = []
            unics_alt = []
            all_instances = self.all_instances
            if phanterpwa_helpers:
                from phanterpwa.helpers import ALL_TAGS
                extra_imp = ""
                xml_import = ""
                str_class = ""
                for x in all_instances:
                    inst = all_instances[x]
                    if inst.tag:
                        if inst.tag.upper() not in ALL_TAGS:
                            if inst.tag not in unics_tag:
                                if not xml_import:
                                    xml_import = "from phanterpwa.xmlconstructor import XmlConstructor\n"
                                unics_tag.append(inst.tag)
                                if inst.void:
                                    str_imp = "".join([
                                        str_imp,
                                        "\n",
                                        inst.tag.upper(),
                                        " = XmlConstructor.tagger(",
                                        "'", inst.tag, "', ",
                                        str(inst.void),
                                        ")\n"
                                    ])
                                else:
                                    str_imp = "".join([
                                        str_imp,
                                        "\n",
                                        inst.tag.upper(),
                                        " = XmlConstructor.tagger(",
                                        "'", inst.tag,
                                        "')\n"
                                    ])
                        else:
                            if inst.tag not in unics_tag:
                                unics_tag.append(inst.tag)
                                if not extra_imp:
                                    extra_imp = "from phanterpwa.helpers import (\n"
                                extra_imp = "".join([extra_imp, "    ", inst.tag.upper(), ",\n"])
                    elif inst.alternative_tag:
                        if inst.alternative_tag.upper() not in ALL_TAGS:
                            if inst.alternative_tag not in unics_alt:
                                if not xml_import:
                                    xml_import = "from phanterpwa.xmlconstructor import XmlConstructor\n"
                                unics_alt.append(inst.alternative_tag)
                                str_class = "".join([
                                    str_class,
                                    "\n\nclass ", inst.alternative_tag.upper(), "(XmlConstructor):\n",
                                    "    def __init__(self, *content):\n",
                                    "        XmlConstructor.__init__(self, '', ", str(inst.void), ", *content)\n"
                                    "        self.alternative_tag = '", inst.alternative_tag, "'",
                                    "\n"
                                ])
                        else:
                            if inst.alternative_tag not in unics_alt:
                                unics_alt.append(inst.alternative_tag)
                                if not extra_imp:
                                    extra_imp = "from phanterpwa.helpers import (\n"
                                extra_imp = "".join([extra_imp, "    ", inst.alternative_tag.upper(), ",\n"])
                if extra_imp:
                    extra_imp = "".join([extra_imp[:-2], "\n)\n"])
                str_imp = "".join([
                    xml_import,
                    extra_imp,
                    str_class,
                    "\n\n" if str_class else "",
                    str_imp,
                    "\n\n",
                    instance_name, " = "
                ])
            else:
                xml_import = "from phanterpwa.xmlconstructor import XmlConstructor\n"
                str_imp = ""
                str_class = ""
                for x in all_instances:
                    inst = all_instances[x]
                    if inst.tag:
                        if inst.tag not in unics_tag:
                            unics_tag.append(inst.tag)
                            if inst.void:
                                str_imp = "".join([
                                    str_imp,
                                    inst.tag.upper(),
                                    " = XmlConstructor.tagger(",
                                    "'", inst.tag, "', ",
                                    str(inst.void),
                                    ")\n"
                                ])
                            else:
                                if inst.tag == "html":
                                    str_class = "".join([
                                        str_class,
                                        "\n\n",
                                        HTML_SAMPLE,
                                        "\n"
                                    ])
                                else:
                                    str_imp = "".join([
                                        str_imp,
                                        inst.tag.upper(),
                                        " = XmlConstructor.tagger(",
                                        "'", inst.tag,
                                        "')\n"
                                    ])
                    elif inst.alternative_tag:
                        if inst.alternative_tag == "xml":
                            xml_import = "".join([
                                xml_import,
                                "from phanterpwa.xss import XssCleaner\n"
                            ])
                            if not inst.alternative_tag in unics_alt:
                                str_class = "".join([
                                    str_class,
                                    "\n\n",
                                    XML_SAMPLE,
                                    "\n"
                                ])
                            unics_alt.append(inst.alternative_tag)
                        elif inst.alternative_tag == "xcomment":
                            if not inst.alternative_tag in unics_alt:
                                str_class = "".join([
                                    str_class,
                                    "\n\n",
                                    XCOMMENT_SAMPLE,
                                    "\n"
                                ])
                            unics_alt.append(inst.alternative_tag)
                        elif inst.alternative_tag not in unics_alt:

                            unics_alt.append(inst.alternative_tag)
                            str_class = "".join([
                                str_class,
                                "\n\nclass ", inst.alternative_tag.upper(), "(XmlConstructor):\n",
                                "    def __init__(self, *content):\n",
                                "        XmlConstructor.__init__(self, '', ", str(inst.void), ", *content)\n"
                                "        self.alternative_tag = '", inst.alternative_tag, "'",
                                "\n"
                            ])
                str_imp = "".join([
                    xml_import,
                    str_class,
                    "\n\n" if str_class else "",
                    str_imp, "\n\n",
                    instance_name,
                    " = "
                ])
            src = "".join([str_imp, src])
        if self._indent_level == 0 and add_imports:
            src = "".join([src, "\n"])
            if self.close_void:
                src = "".join([src, "\n", instance_name, ".close_void = ", str(self.close_void), "\n"])
            if self.minify is False:
                src = "".join([src, "\n", instance_name, ".indent_size = ", str(self.minify), "\n"])
            if self.indent_size != 2 and self.minify is False:
                src = "".join([src, "\n", instance_name, ".indent_size = ", str(self.indent_size), "\n"])
        return src

    def html(
        self,
        minify: bool=True,
        indent_size: int=2,
        close_void: bool=False,
        translate: bool=False,
        formatter: (None, dict)=None,
        delimiters: list=["{{", "}}"],
        i18nInstance: (None, Translator)=None,
        tag_translation=None,
        dictionary: (None, str)=None,
        do_not_translate: list=[],
        escape_string=True,
        file=None,
        encoding="utf-8") -> str:
        """
        With this method it is possible to generate an xml with
        different formats, with minimized indentation, with closed void
        elements without changing any other instance property. You can
        also write the generated xml to a file.

        Args:

            @minify: If True the generated xml will be minified, if
            False will be indented. (default: True).
            @indent_size: Only has effect with minify False, determines
            the size of the indentation. (default: 2).
            @close_void: The xml of the void elements will be closed.
            (default: False).
            @translate: With the translate True the translation will be
            applied (see more details in the i18n method). (default:
            False).
            @formatter: Adds the Format String Syntax (str.format()) in
            the generated xml. (default: None).
            @i18nInstance: Set phanterpwa.i18n.Translator instance to
            translate, dictionary or tag_translation must be valid
            argument.
            @tag_translation: Set the tag used on translation on client
            side.
            @dictionary: Specifics the dictionary that be used. Need a
            valid parameter on i18nTranslate.
            @do_not_translate: List with the Words that be ignored in
            translation.
            @escape_string: The strings aren't be scaped if
            escape_string is False. True is default.
            @file: Name of the file that will be written to the
            generated xml. (default: None).
            @encoding: It only takes effect if the file argument is
            other than None, here determines the encoding used in the
            xml script in the file.

        example:

            >>> from phanterpwa.helpers import (DIV, BR, HR, SPAN)
            >>> instanceDIV = DIV(DIV(BR(), HR(), SPAN()), _class="my_class", _underline="_underline", without_underline="without_underline")
            >>> # The method html is not affected by these attributes
            >>> instanceDIV.minify = False
            >>> instanceDIV.indent_size = 4
            >>> instanceDIV.close_void = True
            >>> print(instanceDIV.html())  # default: minify=True, indent_size=2, close_void=False
            <div class="my_class" underline="_underline"><div><br><hr><span></span></div></div>
            >>> print(instanceDIV.html(False, 8))  # minify=False, indent_size=8, close_void=False(default)
            <div class="my_class" underline="_underline">
                    <div>
                            <br>
                            <hr>
                            <span>
                            </span>
                    </div>
            </div>
            >>> print(instanceDIV.html(minify=False, close_void=True))  # minify=False, indent_size=4, close_void=False(default)
            <div class="my_class" underline="_underline">
              <div>
                <br />
                <hr />
                <span>
                </span>
              </div>
            </div>

        The method humanize is affected by the indent_size and
        close_void attribute

            >>> print(instanceDIV.humanize())
            <div class="my_class" underline="_underline">
                <div>
                    <br />
                    <hr />
                    <span>
                    </span>
                </div>
            </div>

        The method xml is affected by the minify, indent_size (when
        instance.minify=True) and close_void attribute.

            >>> instanceDIV.minify = True
            >>> print(instanceDIV.xml())
            <div class="my_class" underline="_underline"><div><br /><hr /><span></span></div></div>
            >>> instanceDIV.minify = False
            >>> print(instanceDIV.xml())
            <div class="my_class" underline="_underline">
                <div>
                    <br />
                    <hr />
                    <span>
                    </span>
                </div>
            </div>
        """
        t_escape_str = self.escape_string
        self.escape_string = escape_string
        if minify:
            xml = self._minified(
                close_void,
                i18nInstance,
                dictionary,
                do_not_translate,
                tag_translation
            )
        else:
            xml = self._humanized(
                indent_size,
                close_void,
                i18nInstance,
                dictionary,
                do_not_translate,
                tag_translation
            )
        if formatter is not None:
            if isinstance(formatter, dict):
                xml = self._interpolate(xml, formatter, delimiters)
            else:
                raise "".join(["To format the string, only one dict is accepted. Given: ", str(type(formatter))])
        if file is not None:
            with open(file, "w", encoding=encoding) as f:
                f.write(xml)
        self.escape_string = t_escape_str
        return xml

    def humanize(self) -> str:
        """
        The humanize method returns the xml in indented format for
        easier reading by humans, it is affected by the close_void and
        indent_size attributes of the class.

        Example:

            >>> from phanterpwa.helpers import (DIV, BR, HR, SPAN)
            >>> instanceDIV = DIV(
                    DIV(
                        BR(),
                        HR(),
                        SPAN()
                    ),
                    _class="my_class",
                    _underline="_underline",
                    without_underline="without_underline"
                )
            >>> print(instanceDIV.humanize())
            <div class="my_class" underline="_underline">
              <div>
                <br>
                <hr>
                <span>
                </span>
              </div>
            </div>
            >>> instanceDIV.close_void = True
            >>> print(instanceDIV.humanize())
            <div class="my_class" underline="_underline">
              <div>
                <br />
                <hr />
                <span>
                </span>
              </div>
            </div>
            >>> instanceDIV.indent_size = 4
            >>> print(instanceDIV.humanize())
            <div class="my_class" underline="_underline">
                <div>
                    <br />
                    <hr />
                    <span>
                    </span>
                </div>
            </div>
        """
        xml = self._humanized(
            self.indent_size,
            self.close_void,
            self.i18nInstance,
            self.dictionary,
            self.do_not_translate,
            self.tag_translation
        )
        if self._formatter:
            xml = self._interpolate(xml, self._formatter, self.delimiters)
        return xml

    def xml(self) -> str:
        """
        With this method it is possible to generate a xml of the instance.
        The format of the generated xml depends on the void_close, minify,
        and indent_size (indent size will only take effect if minify for
        False) properties that change class attributes XmlConstructor.

        example:

            >>> from phanterpwa.helpers import (DIV, BR, HR, SPAN)
            >>> instanceDIV = DIV(
                    DIV(
                        BR(),
                        HR(),
                        SPAN()
                    ),
                    _class="my_class", _underline="_underline"
                )
            >>> # The method html is not affected by these attributes
            >>> instanceDIV.indent_size = 4
            >>> instanceDIV.close_void = True
            >>> print(instanceDIV.xml())
            <div class="my_class" underline="_underline"><div><br /><hr /><span></span></div></div>
            >>> instanceDIV.minify = False
            >>> print(instanceDIV.xml())
            <div class="my_class" underline="_underline">
                <div>
                    <br />
                    <hr />
                    <span>
                    </span>
                </div>
            </div>
            >>> instanceDIV.indent_size = 8
            >>> instanceDIV.close_void = False
            >>> print(instanceDIV.xml())
            <div class="my_class" underline="_underline">
                    <div>
                            <br>
                            <hr>
                            <span>
                            </span>
                    </div>
            </div>
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
                xml = self._interpolate(xml, self._formatter, self.delimiters)
        else:
            xml = self.humanize()
        return xml

    def json(self, **kargs) -> str:
        """
        In some cases, it is necessary to pass the generated XML from
        the instance to an argument from some javascript library, such
        as jquery for example, so this method converts xml (multiline)
        to json string (quotted).
        @kargs: to kargs json.dumps.

        Example:

            from phanterpwa.helpers import (DIV, HR, SPAN, SCRIPT)
            >>> instanceDIV = DIV(
                    DIV("multline\nline01\nline02"),
                    SPAN("it's red", _style="color:red;"),
                    HR()
                )
            >>> print(instanceDIV)
            <div><div>multline
            line01
            line02</div><span style="color:red;">it&#x27;s red</span><hr></div>
            >>> print(instanceDIV.json())
            "<div><div>multline\nline01\nline02</div><span style=\"color:red;\">it&#x27;s red</span><hr></div>"
            >>> instanceSCRIPT = SCRIPT('$("#my_id").html({0});'.format(instanceDIV.json()))
            >>> print(instanceSCRIPT)
            <script>$("#my_id").html("<div><div>multline\nline01\nline02</div><span style=\"color:red;\">it&#x27;s red</span><hr></div>");</script>
        """
        return json.dumps(self.xml(), **kargs)

    def search(self, search) -> list:
        """
        With this method you can find instances contained in the main
        instance by giving it some parameters such as: string, dict,
        other instances and integers. Each type will be treated
        differently, as we will see below.
        @search: Search Parameter, must be string, XmlConstructor, dict,
        int, list, set or tuple.
        It will always return a list with the result, if not found it
        will be empty.

        Consider the following instances below:

            >>> from phanterpwa.helpers import (DIV, SPAN, HR, HTML)
            >>> instanceHR = HR(_class="one two")
            >>> id_to_search = instanceHR.id
            >>> print(id_to_search)
            >>> sampleSEARCH = HTML(
                DIV(
                    DIV(
                        "content",
                        _class="two",
                        _style="color:   white;  display   : none;"
                    ),
                    SPAN(
                        "content",
                        HR(
                            _class="one two"
                        )
                    ),
                    instanceHR,
                    DIV(
                        "long_content",
                        SPAN(
                            "long_content"
                        ),
                        _class="one",
                        _style="color:   white"
                    ),
                    _style="display:none;"
                ),
                DIV("multiple")
            )

        Let's find using another instance, this way the method will look
        inside the contents of the main instance for all instances that
        generate the same xml.

            >>> search = SPAN("long_content")
            >>> result = sampleSEARCH.search(search)
            >>> print("located", len(result))
            located 1
            >>> for x in result:
                    print("instance:", x.introspect)
                    print("xml:", x)
            instance: <class 'phanterpwa.xmlconstructor.XmlConstructor.tagger.<locals>.TAGGER'> {id: 47216592, tag: span}
            xml: <span>long_content</span>

        Let's search now using a string, so the method will search
        within content strings that have at least one occurrence
        returning the parent instance that contains the string.

            >>> search = "long_content"
            >>> result = sampleSEARCH.search(search)
            >>> print("located", len(result))
            located 2
            >>> for x in result:
                    print("It has the string 'long_content'?", x)
            It has the string 'long_content'? <div class="one" style="color:   white">long_content<span>long_content</span></div>
            It has the string 'long_content'? <span>long_content</span>
            >>> search = "content"
            >>> result = sampleSEARCH.search(search)
            >>> print("located", len(result))
            located 4
            >>> for x in result:
                    print("It has the string 'content'?", x)
            It has the string 'content'? <div class="one" style="color:   white">long_content<span>long_content</span></div>
            It has the string 'content'? <span>content<hr class="one two"></span>
            It has the string 'content'? <div class="two" style="color:   white;  display   : none;">content</div>
            It has the string 'content'? <span>long_content</span>

        Let's search now using a dict, so the method will look for all
        instances that have the same attributes as searched, the values
        must be the same except for the _class and _style attributes
        where just match a string in their content.

            >>> result = sampleSEARCH.search({'_style':"  display:   none;"})
            >>> print("located", len(result))
            located 2
            >>> for x in result:
                    print("xml:", x)
            xml: <div class="two" style="color:   white;  display   : none;">content</div>
            xml: <div style="display:none;"><div class="two" style="color:   white;  display   : none;">content</div><span>content<hr class="one two"></span><hr class="one two"><div class="one" style="color:   white">long_content<span>long_content</span></div></div>
            >>> result = sampleSEARCH.search({'_style':"  display:   none;", '_class': 'two'})
            >>> print("located", len(result))
            located 1
            >>> for x in result:
                    print("xml:", x)
            xml: <div class="two" style="color:   white;  display   : none;">content</div>
            >>> result = sampleSEARCH.search({'_class': 'two'})
            >>> print("located", len(result))
            located 3
            >>> for x in result:
                    print("xml:", x)
            xml: <hr class="one two">
            xml: <hr class="one two">
            xml: <div class="two" style="color:   white;  display   : none;">content</div>
            >>> result = sampleSEARCH.search({'_class': 'two one'})
            >>> print("located", len(result))
            located 2
            >>> for x in result:
                    print("xml:", x)
            xml: <hr class="one two">
            xml: <hr class="one two">

        When we add an integer the method will look for the id.

            >>> result = sampleSEARCH.search(id_to_search)
            >>> print("located", len(result))
            located 1
            >>> for x in result:
                    print("xml:", x)
            xml: <hr class="one two">

        When we add a list, a set or a tuple, it will do multiple
        searches returning a list with all the instances found.

            >>> result = sampleSEARCH.search([
                id_to_search, SPAN("long_content"), "multiple"
            ])
            >>> print("located", len(result))
            located 3
            >>> for x in result:
                    print("xml:", x)
            xml: <div>multiple</div>
            xml: <span>long_content</span>
            xml: <hr class="one two">
        """
        results = []
        if isinstance(search, XmlConstructor):
            for x in self:
                if isinstance(x, XmlConstructor):
                    if x.xml() == search.xml():
                        results.append(x)
                    resul_rec = x.search(search)
                    for r in resul_rec:
                        results.append(r)
            return results
        elif isinstance(search, dict):
            list_source_attrs = {y[1:] if y.startswith("_") else y: search[y] for y in search}
            for x in self:
                if isinstance(x, XmlConstructor):
                    list_target_attrs = set(y[1:] for y in x.attributes.keys() if y.startswith("_"))
                    if set(list_target_attrs) & set(list_source_attrs) == set(list_source_attrs):
                        pass_all = []
                        for z in list_source_attrs.keys():
                            if z == "class":
                                if set(list_source_attrs[z].split(" ")) &\
                                        set(x.attributes["_{0}".format(z)].split(" ")) ==\
                                        set(list_source_attrs[z].split(" ")):
                                    pass_all.append(True)
                                else:
                                    pass_all.append(False)
                            elif z == "style":
                                if "_style" in x.attributes:
                                    if set(self._styles_css(list_source_attrs[z])) &\
                                            set(self._styles_css(x.attributes["_style"])):
                                        pass_all.append(True)
                                    else:
                                        pass_all.append(False)
                            else:
                                if list_source_attrs[z] == x.attributes["_{0}".format(z)]:
                                    pass_all.append(True)
                                else:
                                    pass_all.append(False)
                        if all(pass_all):
                            results.append(x)
                    resul_rec = x.search(search)
                    for r in resul_rec:
                        results.append(r)
        elif isinstance(search, str):
            results = []
            for x in self:
                if isinstance(x, XmlConstructor):
                    resul_rec = x.search(search)
                    for r in resul_rec:
                        results.append(r)
                else:
                    if search in str(x):
                        results.append(self)
        elif isinstance(search, int):
            results = []
            for x in self:
                if isinstance(x, XmlConstructor):
                    if x.id == search:
                        results.append(x)
                        break
                    else:
                        resul_rec = x.search(search)
                        if resul_rec:
                            results.append(resul_rec[0])
                            break
        elif isinstance(search, list):
            for x in search:
                resul_rec = self.search(x)
                for r in resul_rec:
                    results.append(r)
        else:
            raise TypeError("".join([
                "The search must be string, XmlConstructor, dict,",
                " int, list, set, tuple. Given ",
                str(type(search))
            ]))
        results = set(results)
        return list(results)

    def i18n(self,
        i18nInstance: Translator,
        dictionary: (None, str)=None,
        tag_translation: (None, bool)=None,
        do_not_translate: list=[]):
        """
        With this method it is possible to translate the strings
        contained in the main instance and its children, it uses the
        Translator class of the module i18n of the phanterpwa package,
        it replaces the strings with the corresponding translation.
        You can perform two ways of translating
        strings, one of them makes more sense to be used on the server
        side and the other on the client side.
        One of the ways of translation, it is translated directly using a
        specific dictionary, the xml generated in the xml and humanize methods
        have the strings found in the dictionary translated to use this method
        you must have an instance of the phanterpwa.i18n.Translator object in
        the i18nInstance argument and a valid dictionary specified in the
        dictionary argument.
        In the other way, it creates an element with a tag specified in
        the tag_translation argument and with an attribute called
        "phanterpwa_i18n" in which a dictionary with all dictionaries
        with that specific translation is stored, on the client side
        you can use a Jquery plug-in, example:
            $("#id_parent_element").phanterpwa_i18n();
        This plug-in from phanterpwa.js replace the element content with the
        attribute value of a specific dictionary, which may even be the
        browser language. Remember that nothing prevents the server
        side using this common method on the client side or vice
        versa.

        Args:

            @i18nInstance: phanterpwa.i18n.Translator instance.
            @dictionary: A dictionary disponible on phanterpwa.i18n.Translator.
                When setting a dictionary the tag_translation automatically
                changes to None.
            @tag_translation: New tag_translation name. When you set a new
                valid tag name the dictionary is automatically changed to None.
            @do_not_translate: list of strings that should be ignored in the
                translation

        Example:

            >>> from phanterpwa.helpers import DIV, P
            >>> from phanterpwa.i18n import Translator
            >>> instanceDIV = DIV(
                    "Can I use formatter method? {response}",
                    P("Monkey", ". Don't have translation this and not has translation of ", "Camel", " in Spanish"),
                    P("Do not exist translation"),
                    P("Apple", "Orange", "Grape", "Do not have translate"),
                    P("The book is on the table", " is ignored")
                )
            >>> print(instanceDIV.humanize())
            <div>
              Can I use formatter method? {response}
              <p>
                Monkey
                . Don&#x27;t have translation this and not has translation of 
                Camel
                 in Spanish
              </p>
              <p>
                Do not exist translation
              </p>
              <p>
                Apple
                Orange
                Grape
                Do not have translate
              </p>
              <p>
                The book is on the table
                 is ignored
              </p>
            </div>
            >>> i18nMyInstance = Translator("path_of_languages", debug=True)
            >>> i18nMyInstance.translate("pt-PT", "Orange", "Laranja")
            >>> i18nMyInstance.translate("pt-PT", "Grape", "Uva")
            >>> i18nMyInstance.translate("pt-BR", "Apple", "Maçã")
            >>> i18nMyInstance.translate("pt-BR", "Orange", "Laranja")
            >>> i18nMyInstance.translate("pt-BR", "The book is on the table", "O livro está sobre a mesa")
            >>> i18nMyInstance.translate("pt-BR", "Camel", "Camelo")
            >>> i18nMyInstance.translate("pt-BR", "It is must be ignored", "Isto pode ser ignorado")
            >>> i18nMyInstance.translate("pt-BR", "Can I use formatter method? {response}", "Posso usar o método formatter? {response}")
            >>> i18nMyInstance.translate("fr", "The book is on the table", "Le livre est sur la table")
            >>> i18nMyInstance.translate("fr", "Monkey", "Singe")
            >>> i18nMyInstance.translate("es", "The book is on the table", "El libro está sobre la mesa")
            >>> i18nMyInstance.translate("es", "Monkey", "Mono")
            >>> instanceDIV.i18n(i18nMyInstance, tag_translation="span", do_not_translate=["It is must be ignored", "The book is on the table"])
            >>> print(instanceDIV.humanize())  # The default of tag_translarion is "span"
            <div>
              <span phanterpwa_i18n='{"pt-BR": {"Can I use formatter method? {response}": "Posso usar o m\u00e9todo formatter? {response}"}}'>Can I use formatter method? {response}</span>
              <p>
                <span phanterpwa_i18n='{"es": {"Monkey": "Mono"}, "fr": {"Monkey": "Singe"}, "pt-BR": {"Monkey": "Macaco"}}'>Monkey</span>
                . Don&#x27;t have translation this and not has translation of 
                <span phanterpwa_i18n='{"pt-BR": {"Camel": "Camelo"}}'>Camel</span>
                 in Spanish
              </p>
              <p>
                Do not exist translation
              </p>
              <p>
                <span phanterpwa_i18n='{"pt-BR": {"Apple": "Ma\\u00e7\\u00e3"}}'>Apple</span>
                <span phanterpwa_i18n='{"pt-BR": {"Orange": "Laranja"}, "pt-PT": {"Orange": "Laranja"}}'>Orange</span>
                <span phanterpwa_i18n='{"pt-PT": {"Grape": "Uva"}}'>Grape</span>
                Do not have translate
              </p>
              <p>
                The book is on the table
                 is ignored
              </p>
            </div>
            >>> instanceDIV.i18n(i18nMyInstance, tag_translation="i18n", do_not_translate=["It is must be ignored", "The book is on the table"])
            >>> print(instanceDIV.humanize())  # change tag_translarion to "i18n"
            <div>
              <i18n phanterpwa_i18n='{"pt-BR": {"Can I use formatter method? {response}": "Posso usar o m\\u00e9todo formatter? {response}"}}'>Can I use formatter method? {response}</i18n>
              <p>
                <i18n phanterpwa_i18n='{"es": {"Monkey": "Mono"}, "fr": {"Monkey": "Singe"}, "pt-BR": {"Monkey": "Macaco"}}'>Monkey</i18n>
                . Don&#x27;t have translation this and not has translation of 
                <i18n phanterpwa_i18n='{"pt-BR": {"Camel": "Camelo"}}'>Camel</i18n>
                 in Spanish
              </p>
              <p>
                Do not exist translation
              </p>
              <p>
                <i18n phanterpwa_i18n='{"pt-BR": {"Apple": "Ma\\u00e7\\u00e3"}}'>Apple</i18n>
                <i18n phanterpwa_i18n='{"pt-BR": {"Orange": "Laranja"}, "pt-PT": {"Orange": "Laranja"}}'>Orange</i18n>
                <i18n phanterpwa_i18n='{"pt-PT": {"Grape": "Uva"}}'>Grape</i18n>
                Do not have translate
              </p>
              <p>
                The book is on the table
                 is ignored
              </p>
            </div>
            >>> instanceDIV.i18n(i18nMyInstance, dictionary="es" , do_not_translate=["It is must be ignored"])
            >>> print(instanceDIV.humanize())  # dictionary "es"
            <div>
              Can I use formatter method? {response}
              <p>
                Mono
                . Don&#x27;t have translation this and not has translation of 
                Camel
                 in Spanish
              </p>
              <p>
                Do not exist translation
              </p>
              <p>
                Apple
                Orange
                Grape
                Do not have translate
              </p>
              <p>
                El libro está sobre la mesa
                 is ignored
              </p>
            </div>
            >>> instanceDIV.i18n(i18nMyInstance, dictionary="fr" , do_not_translate=["It is must be ignored"])
            >>> print(instanceDIV.humanize())  # dictionary "fr"
            <div>
              Can I use formatter method? {response}
              <p>
                Singe
                . Don&#x27;t have translation this and not has translation of 
                Camel
                 in Spanish
              </p>
              <p>
                Do not exist translation
              </p>
              <p>
                Apple
                Orange
                Grape
                Do not have translate
              </p>
              <p>
                Le livre est sur la table
                 is ignored
              </p>
            </div>
            >>> instanceDIV.i18n(i18nMyInstance, dictionary="pt-PT" , do_not_translate=["It is must be ignored"])
            >>> print(instanceDIV.humanize())  # dictionary "pt-PT"
            <div>
              Can I use formatter method? {response}
              <p>
                Monkey
                . Don&#x27;t have translation this and not has translation of 
                Camel
                 in Spanish
              </p>
              <p>
                Do not exist translation
              </p>
              <p>
                Apple
                Laranja
                Uva
                Do not have translate
              </p>
              <p>
                The book is on the table
                 is ignored
              </p>
            </div>
            >>> instanceDIV.i18n(i18nMyInstance, dictionary="pt-BR" , do_not_translate=["It is must be ignored"])
            >>> print(instanceDIV.humanize())  # dictionary "pt-BR"
            <div>
              Posso usar o método formatter? {response}
              <p>
                Macaco
                . Don&#x27;t have translation this and not has translation of 
                Camelo
                 in Spanish
              </p>
              <p>
                Do not exist translation
              </p>
              <p>
                Maçã
                Laranja
                Grape
                Do not have translate
              </p>
              <p>
                O livro está sobre a mesa
                 is ignored
              </p>
            </div>
            >>> instanceDIV.formatter(response="SIM (YES)")
            >>> print(instanceDIV.humanize())
            <div>
              Posso usar o método formatter? SIM (YES)
              <p>
                Macaco
                . Don&#x27;t have translation this and not has translation of 
                Camelo
                 in Spanish
              </p>
              <p>
                Do not exist translation
              </p>
              <p>
                Maçã
                Laranja
                Grape
                Do not have translate
              </p>
              <p>
                O livro está sobre a mesa
                 is ignored
              </p>
            </div>
        """
        self.i18nInstance = i18nInstance
        self.dictionary = dictionary
        self.tag_translation = tag_translation
        self.do_not_translate = do_not_translate
        for x in self:
            if isinstance(x, XmlConstructor):
                x.i18n(i18nInstance, dictionary, tag_translation, do_not_translate)

    def append(self, value: "String or XmlConstructor instance"):
        """
        Add a new element in the content of the current element in the
        last position.
        @value: Element to be added

        usage:

            >>> DIV = XmlConstructor.tagger("div")
            >>> my_instance = DIV()
            >>> print(my_instance)
            <div></div>
            >>> my_instance.append("content0")
            >>> print(my_instance)
            <div>content0</div>
            >>> my_instance.append("content1")
            >>> print(my_instance)
            <div>content0content1</div>
        """
        t = list(self._content)
        t.append(value)
        self.content = t

    def insert(self, position, value: "String or XmlConstructor instance"):
        """
        Add a new element in specific position of the content.
        @position: position of the content
        @value: Element to be added

        usage:

            >>> DIV = XmlConstructor.tagger("div")
            >>> my_instance = DIV()
            >>> print(my_instance)
            <div></div>
            >>> my_instance.insert(0, "content0")
            >>> print(my_instance)
            <div>content0</div>
            >>> my_instance.insert(0, "content-1")
            >>> print(my_instance)
            <div>content-1content0</div>
            >>> my_instance.insert(1, "content-1.5")
            >>> print(my_instance)
            <div>content-1content-1.5content0</div>
        """
        t = list(self._content)
        t.insert(position, value)
        self.content = t

    def replace(self, position, value: "String or XmlConstructor instance"):
        """
        Replace a element in specific position in the content.
        @position: position of the element in the content to be replaced
        @value: Element to be added

        usage:

            >>> DIV = XmlConstructor.tagger("div")
            >>> SPAN = XmlConstructor.tagger("span")
            >>> HR = XmlConstructor.tagger("hr", True)
            >>> my_instance = DIV(SPAN(), HR(), DIV())
            >>> print(my_instance)
            <div><span></span><hr><div></div></div>
            >>> my_instance.replace(2, SPAN())
            >>> print(my_instance)
            <div><span></span><hr><span></span></div>
        """
        t = list(self._content)
        t[position] = value
        self._content = t

    @classmethod
    def get_indent_size(cls) -> int:
        """
        See indent_size documetation
        """
        return cls._indent_size

    @classmethod
    def set_indent_size(cls, size: int=2) -> int:
        """
        See indent_size documetation
        """
        if isinstance(size, int):
            cls._indent_size = size
        else:
            raise TypeError("The size must be integer. Given: \"{0}\"".format(str(type(size))))
        return size

    @classmethod
    def get_minify(cls) -> bool:
        """
        See minify documetation
        """
        return cls._minify

    @classmethod
    def set_minify(cls, value: bool) -> bool:
        """
        See minify documetation
        """
        if isinstance(value, bool):
            cls._minify = value
        else:
            raise TypeError("The size must be boolean. Given: \"{0}\"".format(str(type(value))))

    @classmethod
    def set_close_void(cls, value: bool) -> bool:
        """
        See close_void documetation
        """
        if isinstance(value, bool):
            cls._close_void = value
            return value
        else:
            raise TypeError("The close_void must be boolean. Given: \"{0}\"".format(str(type(value))))

    @classmethod
    def get_close_void(cls) -> bool:
        """
        See close_void documetation
        """
        return cls._close_void

    @classmethod
    def tagger(cls, tag: str, void: bool=False, escape_string: bool=True, never_translate: bool=False) -> 'XmlConstructor':
        """
        Using the tagger method you can create a metaclass of class
        XmlConstructor
        """
        cls._add_tag(tag)

        class TAGGER(cls):
            def __init__(self, *content, **attributes):
                cls.__init__(self, tag, void, *content, **attributes)
                self.never_translate = never_translate
                self.escape_string = escape_string
        return TAGGER

    @classmethod
    def _add_instance(cls, tag, instance):
        if instance.id not in cls._all_instances:
            cls._all_instances[instance.id] = instance

    @classmethod
    def _add_tag(cls, tag):
        if tag not in cls._tag_list:
            cls._tag_list.append(tag)

    @staticmethod
    def _styles_css(style: str) -> list:
        list_sty = set()
        sty = style.split(";")
        for x in sty:
            if ":" in x:
                rs = x.split(":")
                if len(rs) == 2:
                    css_sty = rs[0].strip()
                    css_val = rs[1].strip()
                    css_sty_val = "".join([css_sty, ": ", css_val, ";"])
                    list_sty.add(css_sty_val)
        return list(list_sty)

    @staticmethod
    def _interpolate(xstring, contex, delimiters=["{{", "}}"]):
        if isinstance(contex, dict):
            return interpolate(xstring, contex, delimiters)
        else:
            raise ValueError("The contex from _format method must be dict. Given: {0}".format(type(contex)))

    def _process_attrs_values(self, attr_value):
        if isinstance(attr_value, list):
            new_list = []
            for x in attr_value:
                v = self._process_attrs_values(x)  # recursive
                new_list.append(v)
            return new_list
        elif isinstance(attr_value, dict):
            new_dict = {}
            for k in attr_value:
                v = self._process_attrs_values(attr_value[k])  # recursive
                new_dict[k] = v
            return new_dict
        elif isinstance(attr_value, XmlConstructor):
            v = attr_value.xml()
            return v
        else:
            return attr_value

    def _validate_i18nInstance(self, value):
        if isinstance(value, Translator):
            return value
        else:
            raise ValueError("".join([
                "The i18nInsntance argument must be an instance",
                " of the phanterpwa.i18n.Translator object. Given: ",
                str(type(value))
            ]))

    def _tag_begin_cmp(self, close_void: bool=False) -> str:
        str_tag_begin = ""
        if self._tag:
            if self.xml_attributes:
                if all([self.void, close_void]):
                    str_tag_begin = "<{tag} {attr} />".format(tag=self.tag, attr=self.xml_attributes)
                else:
                    str_tag_begin = "<{tag} {attr}>".format(tag=self.tag, attr=self.xml_attributes)
            else:
                if all([self.void, close_void]):
                    str_tag_begin = "<{tag} />".format(tag=self.tag)
                else:
                    str_tag_begin = "<{tag}>".format(tag=self.tag)
        else:
            str_tag_begin = ""
        return str_tag_begin

    def _indexescalc(self, last=""):
        n_last = last
        if self._parent:
            if self._parent._indent_level > 0:
                last = "".join(["[", str(self._parent._idx), "]", last])
                n_last = self._parent._indexescalc(last)
        return n_last

    def _content_unpack(self, content, process_dict=True):
        t_c_unpack = []
        for x in content:
            if isinstance(x, (list, tuple, set)):
                extra_contents = self._content_unpack(x, process_dict)  # recursive
                for e in extra_contents:
                    t_c_unpack.append(e)
            elif callable(x):
                extra_contents = self._content_unpack(x(), process_dict)  # recursive
                for e in extra_contents:
                    t_c_unpack.append(e)
            elif isinstance(x, dict):
                if process_dict:
                    self.attributes = x
            else:
                t_c_unpack.append(x)
        return t_c_unpack

    def _content_inter(self, content, process_dict=True, process_parent=True):
        temp_content = []
        index = 0
        conf = []
        xcontent = self._content_unpack(content, process_dict)
        for x in xcontent:
            if isinstance(x, XmlConstructor):
                if process_parent:
                    if x._parent is None:
                        conf.append(x.id)
                        x._parent = self
                        x._idx = index
                    else:
                        if (x._parent.id != self.id) or (x.id in conf):
                            if x.tag:
                                y = copy(x)
                                y._add_instance(y.tag, y)
                                x._was_copied.add(y)
                                y._was_copied.add(x)
                                x._was_copied |= y._was_copied
                                y._was_copied = x._was_copied
                                x = y
                                x._parent = self
                                x._idx = index
                temp_content.append(x)
            else:
                x = str(x)
                temp_content.append(x)
            index += 1
        return temp_content

    def _vk(self, k):
        i_caracter = {
            " ": "empty space",
            "=": "equals",
            "'": "single quotes",
            '"': "double quotes",
            ">": "greater than",
            "<": "less than",
            "/": "division"}
        if isinstance(k, str):
            k = k.strip()
            for c in i_caracter.keys():
                if c in k:
                    raise ValueError(
                        "Invalid caracter (\"{0}\": {1}) in attribute name: \"{2}\"".format(i_caracter[c], c, k)
                    )
        else:
            raise TypeError("The key of atribute must is String. Given: \"{0}\"".format(str(type(k))))
        return k

    def _check_keys_attr(self, k: str) -> bool:
        if isinstance(k, str):
            o = k.strip()
            if o.isidentifier():
                return True
        return False

    def _varg(self, k):
        if isinstance(k, str):
            o = k.strip()
            if o.isidentifier():
                return o
            else:
                raise ValueError("".join([
                    "The argument name is invalid, given: ", k
                ]))
        else:
            raise TypeError("The key of atribute must is String. Given: \"{0}\"".format(str(type(k))))

    def _add_key_attr(self, k: str, v: (None, True, False, str), invalid_to_kargs=True):
        fill_attr = self._attributes
        if k.startswith("_") and not (v is None or v is False):
            k = self._vk(k)
            if k is True:
                fill_attr[k] = True
            else:
                fill_attr[k] = v
            self.attributes = fill_attr
        else:
            if invalid_to_kargs:
                self.kargs[k] = v
            else:
                raise SyntaxError("The attributes keys must starts with '_'. Given: \"{0}\"".format(str(k)))

    def _humanized_content(self,
        indent_size=2,
        close_void=False,
        i18nInstance=None,
        dictionary=None,
        do_not_translate=[],
        tag_translation=None):
        t_str = ""
        for x in self._content:
            if isinstance(x, XmlConstructor):
                if self.tag == "":
                    x._indent_level = self._indent_level
                else:
                    x._indent_level = self._indent_level + 1
                t_str = "".join([
                    t_str,
                    x._humanized(
                        indent_size,
                        close_void,
                        i18nInstance,
                        dictionary,
                        do_not_translate,
                        tag_translation
                    )
                ])
            else:
                if all([dictionary, i18nInstance, x not in do_not_translate, not self.never_translate]):
                    x = i18nInstance.translator(x, dictionary)
                    if self.escape_string:
                        x = xssescape(x)
                elif all([i18nInstance, x not in do_not_translate, tag_translation, not self.never_translate]):
                    attr_i18n = i18nInstance.phanterpwa_i18n(x)
                    if attr_i18n:
                        x = XmlConstructor.tagger(tag_translation)(x, {'_phanterpwa_i18n': attr_i18n})
                    else:
                        if self.escape_string:
                            x = xssescape(x)
                else:
                    if self.escape_string:
                        x = xssescape(x)
                if self.tag == "":
                    space = "".join(["\n", " " * ((self._indent_level) * (indent_size))])
                else:
                    space = "".join(["\n", " " * ((self._indent_level + 1) * (indent_size))])
                t_str = "".join([t_str, space, str(x)])
        t_str
        return t_str

    def _src_content(self, translate=False):
        t_src_content = ""
        dictionary = self.dictionary
        i18nInstance = self.i18nInstance
        do_not_translate = self.do_not_translate
        tag_translation = self.tag_translation
        for x in self._content:
            if isinstance(x, XmlConstructor):
                x._indent_level = self._indent_level + 1
                t_src_content = "".join([t_src_content, x.source_code(translate=translate)])
            else:
                if all([dictionary, i18nInstance, x not in do_not_translate, translate, not self.never_translate]):
                    x = i18nInstance.translator(x, dictionary)
                elif all([i18nInstance, x not in do_not_translate, translate, tag_translation, not self.never_translate]):
                    attr_i18n = i18nInstance.phanterpwa_i18n(x)
                    if attr_i18n:
                        x = XmlConstructor.tagger(tag_translation)(x, {'_phanterpwa_i18n': attr_i18n})
                        x._indent_level = self._indent_level + 1
                        x = x.source_code()
                    else:
                        if self.escape_string:
                            x = xssescape(x)
                space = "".join(["\n", " " * ((self._indent_level + 1) * (4))])
                t_src_content = "".join([t_src_content, space, x.__repr__(), ","])
        if not self.attributes:
            t_src_content = t_src_content[:-1]
        return t_src_content

    def _minified_content(self,
        close_void=False,
        i18nInstance=None,
        dictionary=None,
        do_not_translate=[],
        tag_translation=None):
        mini_con = ""
        for x in self._content:
            if isinstance(x, XmlConstructor):
                mini_con = "".join([mini_con, x._minified(
                    close_void,
                    i18nInstance,
                    dictionary,
                    do_not_translate,
                    tag_translation
                )])
            else:
                if all([dictionary, i18nInstance, x not in do_not_translate, not self.never_translate]):
                    x = i18nInstance.translator(x, dictionary)
                    if self.escape_string:
                        x = xssescape(x)
                elif all([i18nInstance, x not in do_not_translate, tag_translation, not self.never_translate]):
                    attr_i18n = i18nInstance.phanterpwa_i18n(x)
                    if attr_i18n:
                        x = XmlConstructor.tagger(tag_translation)(x, {'_phanterpwa_i18n': attr_i18n})
                    else:
                        if self.escape_string:
                            x = xssescape(x)
                else:
                    if self.escape_string:
                        x = xssescape(x)
                mini_con = "".join([mini_con, str(x)])
        return mini_con

    def _humanized(self,
        indent_size=2,
        close_void=False,
        i18nInstance=None,
        dictionary=None,
        do_not_translate=[],
        tag_translation=None):
        human = ""
        space = " " * (self._indent_level * indent_size)
        if self.content and not self.void:
            if self.tag == "":
                human = "".join([
                    self._tag_begin_cmp(close_void),
                    self._humanized_content(
                        indent_size=indent_size,
                        close_void=close_void,
                        i18nInstance=i18nInstance,
                        dictionary=dictionary,
                        do_not_translate=do_not_translate,
                        tag_translation=tag_translation
                    ),
                    self.tag_end
                ])
            else:
                human = "".join([
                    self._tag_begin_cmp(close_void),
                    self._humanized_content(
                        indent_size=indent_size,
                        close_void=close_void,
                        i18nInstance=i18nInstance,
                        dictionary=dictionary,
                        do_not_translate=do_not_translate,
                        tag_translation=tag_translation
                    ),
                    "\n",
                    space,
                    self.tag_end
                ])
        elif self.void:
            human = "".join([self._tag_begin_cmp(close_void)])
        else:
            if self.tag == "":
                return ""
            else:
                human = "".join([self._tag_begin_cmp(close_void), "\n", space, self.tag_end])
        if self.tag == "":
            return human
        else:
            return "".join(["\n" if self._indent_level != 0 else "", space, human])

    def _src_attr(self, space):
        s = ""
        if self.attributes:
            if self.root_parent.src_attr_dict is None:
                if all([self._check_keys_attr(z) for z in self.attributes]):
                    s = "\n"
                    c = self.attributes
                    for x in c:
                        if isinstance(c[x], str):
                            str_attr = c[x].__repr__()
                        else:
                            str_attr = c[x]
                        s = "".join([s, space, x, "=", str(str_attr), ",\n"])
                    if s:
                        s = s[:-2]
                else:
                    s = "\n"
                    s = "".join([s, space, "**{\n"])
                    c = self.attributes
                    for x in c:
                        if isinstance(c[x], str):
                            str_attr = c[x].__repr__()
                        else:
                            str_attr = c[x]
                        s = "".join([s, "    ", space, x.__repr__(), ": ", str(str_attr), ",\n"])
                    s = s[:-2]
                    s = "".join([s, "\n", space, "}"])
            elif self.root_parent.src_attr_dict is False:
                s = "\n"
                c = self.attributes
                for x in c:
                    if isinstance(c[x], str):
                        str_attr = c[x].__repr__()
                    else:
                        str_attr = c[x]
                    s = "".join([s, space, self._varg(x), "=", str(str_attr), ",\n"])
                if s:
                    s = s[:-2]
            else:
                s = "\n"
                s = "".join([s, space, "**{\n"])
                c = self.attributes
                for x in c:
                    if isinstance(c[x], str):
                        str_attr = c[x].__repr__()
                    else:
                        str_attr = c[x]
                    s = "".join([s, "    ", space, x.__repr__(), ": ", str(str_attr), ",\n"])
                s = s[:-2]
                s = "".join([s, "\n", space, "}"])
        return s

    def _minified(self,
        close_void=False,
        i18nInstance=None,
        dictionary=None,
        do_not_translate=[],
        tag_translation=None):
        xml = ""
        if self.content and not self.void:
            xml = "".join([
                self._tag_begin_cmp(close_void),
                self._minified_content(
                    close_void=close_void,
                    i18nInstance=i18nInstance,
                    dictionary=dictionary,
                    do_not_translate=do_not_translate,
                    tag_translation=tag_translation
                ),
                self.tag_end
            ])
        elif self.void:
            xml = self._tag_begin_cmp(close_void)
        else:
            xml = "".join([self._tag_begin_cmp(close_void), self.tag_end])
        xml = "".join([self.before_xml, xml, self.after_xml])
        return xml

    def __hash__(self):
        return hash(self.xml())

    def __str__(self):
        return self.xml()

    def __repr__(self):
        return self.introspect

    def __bool__(self):
        return bool(self.content)

    def __add__(self, add):
        el = []
        if isinstance(add, (list, tuple, set, dict, str, XmlConstructor)):
            el = self._content_inter([self, add], False, False)
            return el
        else:
            raise SyntaxError("".join([
                "The XmlConstructor accepts only addition",
                " operations with list, tuple, set, dict and string"
            ]))

    def __radd__(self, radd):
        el = []
        if isinstance(radd, (list, tuple, set, dict, str, XmlConstructor)):
            el = self._content_inter([radd, self], False, False)
            return el
        else:
            raise SyntaxError("".join([
                "The XmlConstructor accepts only addition",
                " operations with list, tuple, set, dict and string"
            ]))
        return [radd, self]

    def __mul__(self, f):
        if isinstance(f, int):
            return [self for x in range(f)]
        else:
            raise TypeError("".join([
                "The XmlConstructor accepts only ",
                "multiplication operations with integers, given: ",
                str(type(f))
            ]))

    def __iter__(self):
        for c in self.content:
            yield c

    def __getitem__(self, i):
        if isinstance(i, str):
            if i in self._attributes:
                return self._attributes[i]
            else:
                raise ValueError("".join(["The given index",
                " was not found in the attributes, given: '", str(i), "'"]))
        else:
            return self.content[i]

    def __setitem__(self, i, v):
        if isinstance(i, str):
            self._add_key_attr(i, v, False)
        else:
            self.replace(i, v)

    def __delitem__(self, i):
        if isinstance(i, str):
            if i in self._attributes:
                del self._attributes[i]
            else:
                raise ValueError("".join(["The given index",
                " was not found in the attributes, given: '", str(i), "'"]))
        else:
            c = list(self.content)
            del c[i]
            self.content = c

    def __getslice__(self, i, j):
        return self.content[i:j]

    def __len__(self):
        return len(self.content)
