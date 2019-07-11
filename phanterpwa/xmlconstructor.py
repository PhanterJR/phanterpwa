# -*- coding: utf-8 -*-
from .xss import xssescape
from .i18n import Translator
from xml.sax import saxutils
import json
from copy import copy


class XmlConstructor(object):
    """
    Helper to constroi html tags.
    With this class you can create other predefined tags. Example:
    >>> class DIV(TagConstructor):
            def __init__(self, *content, **attributes):
                TagConstructor.__init__(self, "div", False, *content, **attributes)
    >>> print(DIV())
        <div></div>
    >>> print(DIV("My content", _class="my_atribute_class"))
        <div class="my_atribute_class">My content</div>
    """
    _ident_level = 2
    _all_tags = {}

    def __init__(self, tag, singleton=False, *content, **attributes):
        """
        @tag = name of tag. Example: div, img, br

        @singleton = if True, the tag does not need to close.

            Example:
                XmlConstructor("br", True)
                    produce '<br>'
                XmlConstructor("hr", True)
                    produce '<hr>'
                XmlConstructor("img", True, _href="#my_url")
                    produce '<img href="#myurl">'
            if False, the tag will be close,
                XmlConstructor("div")
                    produce '<div></div>'
                XmlConstructor("h1", False, "My title")
                    produce '<h1>My title</h1>'
                XmlConstructor("button", False, "my_content", _class="my_class")
                    produce '<button class="my_class">"my_content"</button>'

        @content = Content of element. exemple: XmlConstructor("this is", " my content")

        @attributes = Element attributes. Each key of the attribute must begin
            with underline (_) (because of the keyword class and id),
            keys without underline will create a Exeption. Example:
            XmlConstructor(_class="my_class", _style="display:block")
        """

        super(XmlConstructor, self).__init__()
        self.tag = tag
        self.singleton = singleton
        self.content = content
        self.kargs = {}
        self.attributes = attributes
        self._parent = None
        if tag:
            self._add_tag(tag, self)
        self._ident_size = 2
        self._ident_level = 0
        self._idx = 0
        self._translate = {}

    @classmethod
    def ident_size(cls, size):
        cls._ident_size = size
        return size

    @property
    def id(self):
        return id(self)

    @property
    def tag(self):
        """
        Get or Set tag of element
        Set:
            >>> new_tag=XmlConstructor('div', False)
            >>> print(new_tag)
                <div></div>
            new_tag.tag='button'
            >>> print(new_tag)
                <button></button>

        Get:
            >>> new_tag=XmlConstructor('div', False)
            >>> print(new_tag.tag)
                div
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        if isinstance(tag, str):
            self._tag = tag
        else:
            raise TypeError("The tag must be string")
    
    def append(self, value):
        t = list(self._content)
        t.append(value)
        self.content = t

    def insert(self, position, value):
        t = list(self._content)
        t.insert(position, value)
        self.content = t

    def replace(self, position, value):
        t = list(self._content)
        t[position] = value
        self.content = t

    @property
    def tag_begin(self):
        """
        Get begin tag.

        Get:
            Example:
                >>> new_element = TagConstructor('div', False)
                >>> new_element.attributes = {"_class": "my_class", "_id": "my_id"}
                >>> print(new_element.tag_begin)
                    <div class="my_class" id="my_id">
        """
        if self._tag:
            if self.xml_attributes:
                self._tag_begin = "<%s %s>" % (self.tag, self.xml_attributes)
            else:
                self._tag_begin = "<%s>" % (self.tag)
        else:
            self._tag_begin = ""
        return self._tag_begin

    @property
    def tag_end(self):
        """
        Get begin tag.

        Get:
            Example:
                >>> new_element = TagConstructor('div', False)
                >>> new_element.attributes = {"_class": "my_class", "_id": "my_id"}
                >>> print(new_element.tag_end)
                    </div>
        """
        if self._tag and not self.singleton:
            self._tag_end = "</%s>" % (self.tag)
        else:
            self._tag_end = ""
        return self._tag_end

    @property
    def singleton(self):
        """
        Get or Set if element is singleton or not
        Set True:
            >>> new_tag=XmlConstructor("br", True)
            >>> print(new_tag)
                <br>
            >>> new_tag=XmlConstructor("hr", True)
            >>> print(new_tag)
                <hr>
            >>> new_tag=XmlConstructor("img", True, _href="#my_url")
            >>> print(new_tag)
                <img href="#myurl">
        Set False:
            >>> new_tag=XmlConstructor("div")
            >>> print(new_tag)
                <div></div>
            >>> new_tag=XmlConstructor("h1", False, "My title")
            >>> print(new_tag)
                <h1>My title</h1>
            >>> new_tag=XmlConstructor("button", False, "my_content", _class="my_class")
            >>> print(new_tag)
                <button class="my_class">"my_content"</button>
        Get:
            >>> new_tag=XmlConstructor("button", False, "my_content", _class="my_class")
            >>> print(new_tag.singleton)
                F     b vbjg hiyalse
        """
        return self._singleton

    @singleton.setter
    def singleton(self, singleton):
        if isinstance(singleton, bool):
            self._singleton = singleton
        else:
            raise TypeError("The singleton must be boolean")

    @property
    def content(self):
        """
        Get or Set content of element.
        Set List:
            >>> new_tag=XmlConstructor("div", False)
            >>> new_tag.content=['my', ' content']
            >>> print(new_tag)
                <div>my content</div>

        Set String:
            >>> new_tag=XmlConstructor("div", False)
            >>> new_tag.content="my other content"
            >>> print(new_tag)
                <div>my other content</div>

        Set XmlConstructor instance:
            >>> new_tag=XmlConstructor("div", False)
            >>> other_tag=XmlConstructor("a", False, "click here", _href="#my_url")
            >>> new_tag.content=other_tag
            >>> print(new_tag)
                <div><a href="#my_url">click here</a></div>
        """
        return self._content

    @content.setter
    def content(self, content):
        if isinstance(content, (list, tuple)):
            temp_content = []
            index = 0
            for x in content:
                if isinstance(x, XmlConstructor):
                    if not x._parent:
                        x._parent = self
                        x._idx = index
                    else:
                        if x._parent.id != self.id:
                            if x.tag:
                                y = copy(x)
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
                x = xssescape(x)
                temp_xml_content = "".join([temp_xml_content, x])

        self._xml_content = temp_xml_content
        return self._xml_content

    @property
    def xml_content_for_humans(self):
        temp_xml_content = ""
        for x in self._content:
            if isinstance(x, XmlConstructor):
                if self.tag == "":
                    x._ident_level = self._ident_level
                else:
                    x._ident_level = self._ident_level + 1
                temp_xml_content = "".join([temp_xml_content, x.humanize()])
            else:
                if x in self._translate:
                    x = self._translate[x]
                x = xssescape(x)
                if self.tag == "":
                    space = "".join(["\n", " " * ((self._ident_level) * (self._ident_size))])
                else:
                    space = "".join(["\n", " " * ((self._ident_level + 1) * (self._ident_size))])
                temp_xml_content = "".join([temp_xml_content, space, x])

        self._xml_content_for_humans = temp_xml_content
        return self._xml_content_for_humans

    @property
    def parent(self):
        return self._parent

    @property
    def attributes(self):
        """
        Get or Set atributes of tag element. Can set a dict(recomended)
            or a string.

        Set a dict:
            Each key of the attribute must begin with underline (_)
            (because of the keyword class and id), keys without underline
            will store in Kargs attribute.
            Example:
                >>> new_tag=XmlConstructor('div', False)
                >>> new_tag.attributes={"_class":"my_class", "_id":"my_id"}
                >>> print(new_tag)
                    <div class="my_class" id="my_id"></div>

        Set a string:
            Example:
                >>> new_tag.attributes='class="my_class_string"'
                >>> print(new_tag)
                    <div class="my_class_string"></div>

        Get:
            Example:
                >>> new_tag=XmlConstructor('div', False)
                >>> new_tag.attributes={"_class":"my_class", "_id":"my_id"}
                >>> new_tag.attributes
                     class="my_class" id="my_id"
        """
        return self._attributes

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
                    raise ValueError("Invalid caracter (%s) in attribute name: '%s'" % (i_caracter[c], c))
        else:
            raise TypeError("The key of atribute must is String, dado: '%s'" % (type(k)))
        return k

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

    @property
    def html(self):
        return self.xml()

    def humanize(self):
        human = ""
        space = " " * (self._ident_level * self._ident_size)
        if self.content and not self.singleton:
            if self.tag == "":
                human = "".join([
                    self.tag_begin,
                    self.xml_content_for_humans,
                    self.tag_end
                ])
            else:
                human = "".join([
                    self.tag_begin,
                    self.xml_content_for_humans,
                    "\n",
                    space,
                    self.tag_end
                ])
        elif self.singleton:
            human = "".join([self.tag_begin])
        else:
            if self.tag == "":
                return ""
            else:
                human = "".join([self.tag_begin, "\n", space, self.tag_end])
        if self.tag == "":
            return human
        else:
            return "".join(["\n" if self._ident_level != 0 else "", space, human]).replace('&#58;', ':')

    def xml(self):
        """
        Get xml(html) of element
            >>> new_tag = XmlConstructor('div', False)
            >>> print(new_tag.xml())
            <div></div>
        """
        xml = ""
        if self.content and not self.singleton:
            xml = "".join([self.tag_begin, self.xml_content, self.tag_end])
        elif self.singleton:
            xml = self.tag_begin
        else:
            xml = "".join([self.tag_begin, self.tag_end])
        return xml

    @property
    def json(self):
        return json.dumps(self.xml())

    @property
    def introsprec(self):
        str_repr = "%s {id: %s, tag: %s}" % (self.__class__, self.id, self.tag)
        return str_repr

    @classmethod
    def _add_tag(cls, tag, instance):
        cls._all_tags[tag] = instance

    @property
    def all_tags(self):
        return self._all_tags

    @property
    def instances_list(self):
        return self._instances_list

    def search(self, search):
        results = []
        if isinstance(search, XmlConstructor):
            for x in self.content:
                if isinstance(x, XmlConstructor):
                    if x.xml() == search.xml():
                        results.append(x)
                    resul_rec = x.search(search)
                    for r in resul_rec:
                        results.append(r)
            return results
        elif isinstance(search, dict):
            list_source_attrs = {y[1:] if y.startswith("_") else y: search[y] for y in search}
            for x in self.content:
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
            for x in self.content:
                if isinstance(x, XmlConstructor):
                    resul_rec = x.search(search)
                    for r in resul_rec:
                        results.append(r)
                else:
                    if search in str(x):
                        results.append(self)
        elif isinstance(search, int):
            results = []
            for x in self.content:
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

        for x in self.content:
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
        return self.content[i]

    def __getslice__(self, i, j):
        return self.content[i:j]

    def __len__(self):
        return len(self.content)
