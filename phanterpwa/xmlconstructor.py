# -*- coding: utf-8 -*-
from .xss import xssescape
from .i18n import Translator
from xml.sax import saxutils
import json
from copy import copy


class XmlConstructor(object):
    r"""
    @author: PhanterJR<junior.conex@gmail.com>
    @license: MIT

    Helper to constroi html tags.
    With this class you can create other predefined tags.
    Example:
        >>> class DIV(XmlConstructor):
                def __init__(self, *content, **attributes):
                    XmlConstructor.__init__(self, "div", False, False, *content, **attributes)
        >>> print(DIV())
        <div></div>

    Or you can (recommended). Using the tagger method you can create a metaclass of class XmlConstructor:

        >>> DIV = XmlConstructor.tagger("div")
        >>> print(DIV())
        <div></div>
        >>> print(DIV("My content", _class="my_atribute_class"))
        <div class="my_atribute_class">My content</div>

    IMPORTANT, Use the xml (or html) method to capture the results you can see in the print command:

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
    """
    __author__ = "PhanterJR<junior.conex@gmail.com>"
    __license__ = "MIT"
    _indent_size = 2
    _all_instances = {}
    _tag_list = []

    def __init__(self, tag: str, void: bool=False, close_void: bool=False, *content, **attributes):
        """
        @tag: Name of tag. Example: div, img, br

        @void: If True, the tag does not has content.

        @close_void: If True, the tag of void elements are closed with "/".

        @content = Content of element. exemple: XmlConstructor.tagger("this is", " my content")

        @attributes = Element attributes. Each key of the attribute must begin
            with underline (_) (because of the keyword class and id),
            keys without underline will create a Exeption. Example:
            XmlConstructor.tagger(_class="my_class", _style="display:block")

        Examples with void is True:

            >>> print(XmlConstructor.tagger("br", True, False)())
            <br>
            >>> print(XmlConstructor.tagger("br", True, True)())
            <br />
            >>> print(XmlConstructor.tagger("hr", True, False)(_class="especial_hr"))
            <hr class="especial_hr">
            >>> print(XmlConstructor.tagger("img", True, False)(_href="#my_url"))
            <img href="#my_url">

        Same example, with best practices, creating a metaclass with the tagger method:

            >>> BR = XmlConstructor.tagger("br", True)
            >>> HR = XmlConstructor.tagger("hr", True)
            >>> IMG = XmlConstructor.tagger("img", True)
            >>> print(BR())
            <br>
            >>> instanceBR = BR()
            >>> instanceBR.close_void = True  # change state of the attribute
            >>> print(instanceBR)
            <br />
            >>> print(HR(_class="especial_hr"))
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

        BEST PRACTICE: To help in use, use the staticmethod tagger,
            in this way you can suppress some parameters.
        Using the tagger method you can create a metaclass of class XmlConstructor, see:

            >>> DIV = XmlConstructor.tagger("div")
            >>> IMG = XmlConstructor.tagger("img", True)
            >>> BR = XmlConstructor.tagger("br", True, True)
            >>> print(DIV())
            <div></div>
            >>> print(DIV("this", "is", "join", " its no. ", "<tag_evil>evil</tag_evil>"))
            <div>thisisjoin its no. &lt;tag_evil&gt;evil&lt;/tag_evil&gt;</div>
            >>> print(IMG(_class="images"))
            <img class="images">
            >>> print(BR())
            <br />
        """

        super(XmlConstructor, self).__init__()
        self.tag = tag
        self.before_xml = ""
        self.after_xml = ""
        self.close_void = close_void
        self.void = void
        self._parent = None
        self._root_parent = None
        self._was_copied = set()
        self.content = content
        self.kargs = {}
        self._escape_string = True
        self.attributes = attributes
        self._add_instance(tag, self)
        if tag:
            self._add_tag(tag)
            self.alternative_tag = tag
        else:
            self.alternative_tag = "empty_tag"
        self._indent_level = 0
        self._idx = 0
        self._humanized_idx = ""
        self._translate = {}
        self._all_children = {}
        self.src_attr_dict = None
        self.minify = True

    @classmethod
    def _cls_indent_size(cls, size: int=2) -> int:
        if isinstance(size, int):
            cls._indent_size = size
        else:
            raise TypeError("The size must be integer. given: %s" % type(size))
        return size

    @property
    def indent_size(self) -> int:
        """
        GET:

            Get current indentation of the class

        SET:

            Set the indentation of the xml method when the minification (minify attribute) is False
            and also the indentation of the humanize method.
            This property uses a classmethod, so a change reflects on all instances.

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
            >>> instanceDIV.minify = False  # minify is an instance method, this only reflects on this instance
            >>> print(instanceDIV)
            <div id="my_id">
              my content
            </div>
            >>> print(otherInstance)
            <div id="my_other_id">my other content</div>
            >>> otherInstance.indent_size = 4  # indent_size is classmethod, this reflect all instances
            >>> print(instanceDIV)
            <div id="my_id">
                my content
            </div>
            >>> print(otherInstance)
            <div id="my_other_id">my other content</div>
        """
        return self._indent_size

    @indent_size.setter
    def indent_size(self, size: int):
        self._cls_indent_size(size)

    @classmethod
    def _add_instance(cls, tag, instance):
        if instance.id not in cls._all_instances:
            cls._all_instances[instance.id] = instance

    @classmethod
    def _add_tag(cls, tag):
        if tag not in cls._tag_list:
            cls._tag_list.append(tag)

    @property
    def id(self) -> int:
        """
        Element id

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
    def tag(self) -> str:
        """
        GET:

            Get the tag name of instance

        SET:

            Set the tag of element
            @tag_name: Name of tag

        Example GET:

            >>> DIV = XmlConstructor.tagger('div')
            >>> my_element = DIV()
            >>> print(my_element.tag)
            div

        Example SET:

            >>> DIV = XmlConstructor.tagger('div')
            >>> new_element = DIV()
            >>> print(new_element)
            <div></div>
            >>> new_element.tag = 'button'
            >>> print(new_element)
            <button></button>

        """
        return self._tag

    @tag.setter
    def tag(self, tag_name: str):
        if isinstance(tag_name, str):
            self._tag = tag_name
        else:
            raise TypeError("The tag must be string")

    def append(self, value: "String or XmlConstructor instance"):
        """
        Add a new element in the content of the current element in the last position.
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
            >>> my_element = DIV()
            >>> print(my_element.alternative_tag)
            div
            >>> METACLASS_WITHOUT_TAG = XmlConstructor.tagger('')
            >>> my_element = METACLASS_WITHOUT_TAG("content")
            >>> print(my_element.alternative_tag)
            empty_tag
            >>> print(my_element.source_code())
            EMPTY_TAG(
                'content'
            )
            >>> print(my_element.children_indexes())
            [ROOT_PARENT]<empty_tag> {}
                [0]"content"
            }


        Example SET:

            >>> DIV = XmlConstructor.tagger('div')
            >>> new_element = DIV()
            >>> print(new_element)
            >>> new_element.tag = 'button'
            >>> print(new_element)
            <button></button>
        """
        return self._alternative_tag

    @alternative_tag.setter
    def alternative_tag(self, tag_name: str):
        self._alternative_tag = str(tag_name)

    @property
    def before_xml(self) -> str:
        """
        In some cases it is necessary to add a string before the generated xml,
        such as opening a comment, this is possible with this property

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
        In some cases it is necessary to add a string after the generated html,
        such as closing a comment, this is possible with this property

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
    def tag_begin(self) -> str:
        """
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
        if self._tag:
            if self.xml_attributes:
                if all([self.void and self.close_void]):
                    self._tag_begin = "<%s %s />" % (self.tag, self.xml_attributes)
                else:
                    self._tag_begin = "<%s %s>" % (self.tag, self.xml_attributes)
            else:
                if all([self.void and self.close_void]):
                    self._tag_begin = "<%s />" % (self.tag)
                else:
                    self._tag_begin = "<%s>" % (self.tag)
        else:
            self._tag_begin = ""
        return self._tag_begin

    @property
    def tag_end(self) -> str:
        """
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
            self._tag_end = "</%s>" % (self.tag)
        else:
            self._tag_end = ""
        return self._tag_end

    @property
    def void(self) -> bool:
        """
        There are elements without content that does not have an end tag,
        they are the void elements. With this property it is possible to set this.
        This property can be set by using the tagger method.

        GET:

            Get the void parameter

        SET:

            Set a void parameter
            So by setting the void parameter False, automatically
            the close_void parameter will also be set to False
            @value: True or False to set if element is void or not

        Example GET:

            >>> new_element = XmlConstructor.tagger("button")() # The default is False
            >>> print(new_element.void)
            False

        Example SET (True) using the tagger method:

            >>> new_element = XmlConstructor.tagger("br", void=True)()
            >>> print(new_element)
            <br>
            >>> new_element = XmlConstructor.tagger("hr", True)()
            >>> print(new_element)
            <hr>

        Example SET (Set False) using the tagger method:

            >>> new_element = XmlConstructor.tagger("div")()
            >>> print(new_element)
            <div></div>
            >>> new_element = XmlConstructor.tagger("h1", False)
            >>> print(new_element("My title"))
            <h1>My title</h1>

        Example SET change instance:

            >>> new_element = XmlConstructor.tagger("mypersonal_tag")()
            >>> print(new_element)
            <mypersonal_tag></mypersonal_tag>
            >>> new_element.void = True
            >>> print(new_element)
            <mypersonal_tag>
            >>> new_element.close_void = True
            >>> print(new_element)
            <mypersonal_tag />
            >>> new_element.void = False
            >>> print(new_element.close_void) # Close_void is False because the void changed to False
            False
            >>> print(new_element)
            <mypersonal_tag></mypersonal_tag>
        """
        return self._void

    @void.setter
    def void(self, value: bool):
        if isinstance(value, bool):
            self._void = value
            if value is False:
                self.close_void = value
        else:
            raise TypeError("The void must be boolean. given: %s" % type(value))

    @property
    def close_void(self) -> str:
        """
        In the void elements of html5 closing or not the tag is optional,
        if you are writing a html legacy (xhtml) with this property you
        can configure the closing of the tag.

        GET:

            Get the close_void parameter

        SET:

            Set a close_void parameter
            The change is only effective if the void parameter is also True.
            So by setting the close_void True parameter automatically
            the void parameter will also be set to True.
            The void parameter has precedence over the close_void using the tagger method.
            @value: True or False to set if the void element is closed or not

        Example GET:

            >>> new_element = XmlConstructor.tagger("button", True)()  # The default is False
            >>> print(new_element.close_void)
            False

        Example SET (Set False) using the tagger method:

            >>> new_element = XmlConstructor.tagger("hr", void=True)  # The default is False
            >>> print(new_element().close_void)
            False
            >>> print(new_element())
            <hr>

        Example SET (True) using the tagger method:

            >>> new_element = XmlConstructor.tagger("div", void=False, close_void=True)
            >>> print(new_element().close_void)  # Is False because the vois is False
            False
            >>> print(new_element())
            <div></div>
            >>> new_element = XmlConstructor.tagger("br", void=True, close_void=True)
            >>> print(new_element())
            <br />
            >>> new_element = XmlConstructor.tagger("hr", True, True)()
            >>> new_element.attributes = {"_class": "has_class"}
            >>> print(new_element)
            <hr class="has_class" />

        Example SET change instance:

            >>> new_element = XmlConstructor.tagger("hr")()
            >>> print(new_element)
            <hr></hr>
            >>> print(new_element.void)
            False
            >>> new_element.close_void = True # The void parameter automatically change to True
            >>> print(new_element.void)
            True
            >>> print(new_element)
            <hr />
            >>> new_element.close_void = False
            >>> print(new_element)
            <hr>
        """
        return self._close_void

    @close_void.setter
    def close_void(self, value: bool):
        if isinstance(value, bool):
            self._close_void = value
            if value is True:
                self.void = value
        else:
            raise TypeError("The close_void must be boolean. given: %s" % type(value))

    @property
    def content(self):
        """
        Get or Set content of element.
        Set List:
            >>> new_element=XmlConstructor.tagger("div", False)
            >>> new_element.content=['my', ' content']
            >>> print(new_element)
                <div>my content</div>

        Set String:
            >>> new_element=XmlConstructor.tagger("div", False)
            >>> new_element.content="my other content"
            >>> print(new_element)
                <div>my other content</div>

        Set XmlConstructor instance:
            >>> new_element=XmlConstructor.tagger("div", False)
            >>> other_tag=XmlConstructor.tagger("a", False, "click here", _href="#my_url")
            >>> new_element.content=other_tag
            >>> print(new_element)
                <div><a href="#my_url">click here</a></div>
        """
        class frozen_content(tuple):
            def __setitem__(self, i, v):
                raise SyntaxError("".join([
                    "To modify or add the content do directly in the instance,",
                    " example: my_instance[0] = \"new_value\""
                ]))
        return frozen_content(self._content)

    @content.setter
    def content(self, content):
        if isinstance(content, (list, tuple)):
            temp_content = []
            index = 0
            conf = []
            for x in content:
                if isinstance(x, XmlConstructor):
                    if x._parent is None:
                        conf.append(x.id)
                        x._parent = self
                        x._idx = index
                    else:
                        if (x._parent.id != self.id) or (x.id in conf):
                            if x.tag:
                                y = copy(x)
                                x._was_copied.add(y)
                                y._was_copied.add(x)
                                x._was_copied |= y._was_copied
                                y._was_copied = x._was_copied
                                x = y
                                x._parent = self
                                x._idx = index
                else:
                    x = str(x)
                temp_content.append(x)
                index += 1
            self._content = tuple(temp_content)
        else:
            self.content = (content, )  # recursive

    @property
    def xml_content(self):
        temp_xml_content = ""
        for x in self._content:
            if isinstance(x, XmlConstructor):
                temp_xml_content = "".join([temp_xml_content, x.xml()])
            else:
                if x in self._translate:
                    x = self._translate[x]
                if self._escape_string:
                    x = xssescape(x)
                temp_xml_content = "".join([temp_xml_content, x])

        self._xml_content = temp_xml_content
        return self._xml_content

    @property
    def root_parent(self):
        if self.parent is None:
            self._root_parent = self
            return self
        else:
            self._root_parent = self.parent.root_parent
            return self._root_parent

    @property
    def parent(self):
        return self._parent

    @property
    def attributes(self):
        """
        Get or Set attributes of tag element. Can set a dict(recomended)
            or a string.

        Set a dict:
            Each key of the attribute must begin with underline (_)
            (because of the keyword class and id), keys without underline
            will store in Kargs attribute.
            Example:
                >>> new_element=XmlConstructor.tagger('div', False)
                >>> new_element.attributes={"_class":"my_class", "_id":"my_id"}
                >>> print(new_element)
                    <div class="my_class" id="my_id"></div>

        Set a string:
            Example:
                >>> new_element.attributes='class="my_class_string"'
                >>> print(new_element)
                    <div class="my_class_string"></div>

        Get:
            Example:
                >>> new_element=XmlConstructor.tagger('div', False)
                >>> new_element.attributes={"_class":"my_class", "_id":"my_id"}
                >>> new_element.attributes
                     class="my_class" id="my_id"
        """
        class frozen_attributes(dict):
            def __setitem__(self, i, v):
                raise SyntaxError("".join([
                    "To modify or add an attribute do directly in the instance,",
                    " example: my_instance[\"_ my_attribute\"] = \"new_value\""
                ]))
        return frozen_attributes(self._attributes)

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
                    raise ValueError("Invalid caracter (\"%s\": %s) in attribute name: '%s'" % (i_caracter[c], c, k))
        else:
            raise TypeError("The key of atribute must is String, given: '%s'" % (type(k)))
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
            raise TypeError("The key of atribute must is String, given: '%s'" % (type(k)))

    @attributes.setter
    def attributes(self, attributes):
        if isinstance(attributes, str):
            a = self._vk(attributes.strip())
            self._attributes = {a: True}
            self._xml_attributes = a
        elif isinstance(attributes, dict):
            fill_attr = {}
            str_attr = ""
            for k in attributes.keys():
                k = self._vk(k)
                v = attributes[k]
                if k.startswith("_") and not (v is None or v is False):
                    if attributes[k] is True:
                        fill_attr[k] = True
                        str_attr = " ".join([str_attr, k[1:]])
                    else:
                        fill_attr[k] = v
                        if isinstance(v, (list, dict)):
                            v = json.dumps(v)
                            v = saxutils.quoteattr(v).replace(':', '&#58;')
                        else:
                            v = saxutils.quoteattr(v)
                        str_attr = " ".join([str_attr, "=".join([k[1:], v])])
                else:
                    self.kargs[k] = attributes[k]
            self._attributes = fill_attr
            self._xml_attributes = str_attr.strip()
        else:
            raise TypeError("The attributes must be a dict or string to set HTML attributes without values")

    @property
    def xml_attributes(self):
        self.attributes = self._attributes
        return self._xml_attributes

    def html(self, minify: bool=True, indent: int=2) -> str:
        return self.xml()

    def _humanized_content(self, indent_size=2):
        temp_xml_content = ""
        for x in self._content:
            if isinstance(x, XmlConstructor):
                if self.tag == "":
                    x._indent_level = self._indent_level
                else:
                    x._indent_level = self._indent_level + 1
                temp_xml_content = "".join([temp_xml_content, x.humanize()])
            else:
                if x in self._translate:
                    x = self._translate[x]
                if self._escape_string:
                    x = xssescape(x)
                if self.tag == "":
                    space = "".join(["\n", " " * ((self._indent_level) * (indent_size))])
                else:
                    space = "".join(["\n", " " * ((self._indent_level + 1) * (indent_size))])
                temp_xml_content = "".join([temp_xml_content, space, x])
        temp_xml_content
        return temp_xml_content

    def _humanized(self, indent_size=2):
        human = ""
        space = " " * (self._indent_level * indent_size)
        if self.content and not self.void:
            if self.tag == "":
                human = "".join([
                    self.tag_begin,
                    self._humanized_content(indent_size),
                    self.tag_end
                ])
            else:
                human = "".join([
                    self.tag_begin,
                    self._humanized_content(indent_size),
                    "\n",
                    space,
                    self.tag_end
                ])
        elif self.void:
            human = "".join([self.tag_begin])
        else:
            if self.tag == "":
                return ""
            else:
                human = "".join([self.tag_begin, "\n", space, self.tag_end])
        if self.tag == "":
            return human
        else:
            return "".join(["\n" if self._indent_level != 0 else "", space, human])

    @property
    def xml_humanized_content(self):
        self._xml_humanized_content = self._humanized_content(self._indent_size)
        return self._xml_humanized_content

    def humanize(self):
        return self._humanized(self._indent_size)

    def _indexescalc(self, last=""):
        n_last = last
        if self._parent:
            if self._parent._indent_level > 0:
                last = "".join(["[%s]" % self._parent._idx, last])
                n_last = self._parent._indexescalc(last)
        return n_last

    def children_indexes(self):
        """Shows the children elements indices of the parent element"""
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

    @property
    def src_attr_dict(self) -> "True, False or None":
        return self._src_attr_dict

    @src_attr_dict.setter
    def src_attr_dict(self, value: "True, False or None"):
        if isinstance(value, bool) or (value is None):
            self._src_attr_dict = value
        else:
            raise TypeError("The value must be boolean or None. given: %s" % type(value))

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
                        s += "%s%s=%s,\n" % (space, x, str_attr)
                    if s:
                        s = s[:-2]
                else:
                    s = "\n"
                    s += "%s**{\n" % (space)
                    c = self.attributes
                    for x in c:
                        if isinstance(c[x], str):
                            str_attr = c[x].__repr__()
                        else:
                            str_attr = c[x]
                        s += "    %s%s:%s,\n" % (space, x.__repr__(), str_attr)
                    s = s[:-2]
                    s += "\n%s}" % (space)
            elif self.root_parent.src_attr_dict is False:
                s = "\n"
                c = self.attributes
                for x in c:
                    if isinstance(c[x], str):
                        str_attr = c[x].__repr__()
                    else:
                        str_attr = c[x]
                    s += "%s%s=%s,\n" % (space, self._varg(x), str_attr)
                if s:
                    s = s[:-2]
            else:
                s = "\n"
                s += "%s**{\n" % (space)
                c = self.attributes
                for x in c:
                    if isinstance(c[x], str):
                        str_attr = c[x].__repr__()
                    else:
                        str_attr = c[x]
                    s += "    %s%s:%s,\n" % (space, x.__repr__(), str_attr)
                s = s[:-2]
                s += "\n%s}" % (space)
        return s

    def _src_content(self):
        t_src_content = ""
        for x in self._content:
            if isinstance(x, XmlConstructor):
                x._indent_level = self._indent_level + 1
                t_src_content = "".join([t_src_content, x.source_code()])
            else:
                if x in self._translate:
                    x = self._translate[x]
                if self._escape_string:
                    x = xssescape(x)
                space = "".join(["\n", " " * ((self._indent_level + 1) * (4))])
                t_src_content = "".join([t_src_content, space, x.__repr__(), ","])
        if not self.attributes:
            t_src_content = t_src_content[:-1]
        return t_src_content

    def source_code(self):
        src = ""
        space = " " * (self._indent_level * 4)
        if not self.void:
            src = "".join([
                self.tag.upper() if self.tag else self.alternative_tag.upper(), "(",
                self._src_content(),
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
        return "".join(["\n" if self._indent_level != 0 else "", space, src])

    @property
    def all_children(self):
        """
        lists all direct and indirect child elements
        """
        self._all_children = {}
        idx = 0
        for x in self:
            if isinstance(x, XmlConstructor):
                x._indent_level = self._indent_level + 1
                x._humanized_idx = x._indexescalc("[%s]" % x._idx if x._indent_level != 0 else "")
                self._all_children[x._humanized_idx] = x
                childs = x.all_children
                for y in childs:
                    self._all_children[y] = childs[y]
            else:
                if self._indent_level != 0:
                    self._all_children[self._indexescalc("[%s][%s]" % (self._idx, idx))] = x
                else:
                    self._all_children[self._indexescalc("[%s]" % (idx))] = x
            idx += 1
        return self._all_children

    def _xml_minified(self):
        xml = ""
        if self.content and not self.void:
            xml = "".join([self.tag_begin, self.xml_content, self.tag_end])
        elif self.void:
            xml = self.tag_begin
        else:
            xml = "".join([self.tag_begin, self.tag_end])
        xml = "".join([self.before_xml, xml, self.after_xml])
        return xml

    def xml(self):
        """
        Get xml(html) of element
            >>> new_element = XmlConstructor.tagger('div', False)
            >>> print(new_element().xml())
            <div></div>
        """
        if self.minify:
            xml = self._xml_minified()
        else:
            xml = self.humanize()
        return xml

    def json(self, **kargs):
        return json.dumps(self.xml(), **kargs)

    @property
    def introsprec(self):
        str_repr = "%s {id: %s, tag: %s}" % (self.__class__, self.id, self.tag)
        return str_repr

    @property
    def all_instances(self):
        """dict with all instances created"""
        return self._all_instances

    @property
    def tag_list(self):
        """list all tag used in instances"""
        return self._tag_list

    @property
    def was_copied(self):
        return self._was_copied

    def search(self, search):
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
                        for z in list_source_attrs.keys():
                            if z == "class":
                                if set(list_source_attrs[z].split(" ")) &\
                                        set(x.attributes["_%s" % z].split(" ")) ==\
                                        set(list_source_attrs[z].split(" ")):
                                    results.append(x)
                            else:
                                if list_source_attrs[z] == x.attributes["_%s" % z]:
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
        return results

    def reset_i18n(self):
        self._translate = {}

    def i18n(self, i18nInstance, dictionary, ignored_entries=None):
        self.reset_i18n()
        if not isinstance(i18nInstance, Translator):
            raise "The i18Insntance argument must be an instance" +\
                " of the phanterpwa.i18n.Translator object, given %s" % type(i18nInstance)

        for x in self:
            if isinstance(x, XmlConstructor):
                x.i18n(i18nInstance, dictionary, ignored_entries)
            elif isinstance(x, str):
                translated = None
                if isinstance(ignored_entries, (list, tuple)):
                    if x not in ignored_entries:
                        translated = i18nInstance.translator(x, dictionary=dictionary)
                else:
                    translated = i18nInstance.translator(x, dictionary=dictionary)
                if translated:
                    self._translate[x] = translated
        return self._translate

    @staticmethod
    def tagger(tag, void=False, close_void=False):
        class TAGGER(XmlConstructor):
            def __init__(self, *content, **attributes):
                XmlConstructor.__init__(self, tag, void, close_void, *content, **attributes)
        return TAGGER

    def __hash__(self):
        return hash(self.xml())

    def __str__(self):
        return self.xml()

    def __repr__(self):
        return self.introsprec

    def __bool__(self):
        return bool(self.content)

    def __add__(self, add):
        return "%s%s" % (self, add)

    def __radd__(self, radd):
        return "%s%s" % (radd, self)

    def __iter__(self):
        for c in self.content:
            yield c

    def __getitem__(self, i):
        if isinstance(i, str):
            if i in self._attributes:
                return self._attributes[i]
            else:
                raise ValueError("".join(["The index can be an integer to reference",
                " a content element or a string for the attributes, the given string",
                " was not found in the attributes, given: ", str(i)]))
        else:
            return self.content[i]

    def __setitem__(self, i, v):
        if isinstance(i, str):
            self._attributes[i] = v
        else:
            self.replace(i, v)

    def __getslice__(self, i, j):
        return self.content[i:j]

    def __len__(self):
        return len(self.content)
