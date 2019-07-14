import unittest
from phanterpwa.helpers import (
    DIV,
    IMG,
    XML,
    A,
    TD,
    SPAN,
    CONCATENATE,
    HTML,
    HEAD,
    BODY,
    B
)
from phanterpwa.reversexml import (
    HtmlToXmlConstructor
)
from phanterpwa.xmlconstructor import XmlConstructor
from phanterpwa.i18n import (
    Translator
)

sample_html_to_xmlconstructor = """<div id="test02" enabled empty="=">
  <div style="background-color:blue; width:100%; height:40px;">
    OOOOOPAAAAA
  </div>
  <div json='{"teste": true}' testando-outro='["macaco", true, "boi"]' texto_com_aspas="queria muito &quot;tentar&quot; ou não 'tentar'" list_none="[null]" dict='{"testesss": true}' json_dums="[null, true, false]">
    <div>
      conteudo
    </div>
  </div>
  <b>crazy_helpers</b>
  &lt;b&gt;crazy_helpers&lt;/b&gt;
</div>
<div>&lt;main&gt;<b>xsscapedthis</b>&lt;/main&gt;</div>
&lt;div&gt;&lt;main&gt;<b>xsscapedthis</b>&lt;/main&gt;&lt;/div&gt;
<div></div>"""
sample_humanize = """<div>
  <div class="second">
    <a href="localhost">
      string link
    </a>
  </div>
  <img alt="ident equals second">
</div>"""
sample_humanize2 = """<div>
  <div class="second">
    <a href="localhost">
      string link
      <span class="inline">
        yes
      </span>
    </a>
  </div>
  <img alt="ident equals second">
  <div>
    extra_line1
  </div>
  <div>
    extra_line2
  </div>
</div>"""

sample_i18n_entries_to_verbete = """<div>Abacaxi<a href="abacaxi"></a>abacaxi<span class="entries">verbete this is ignored?</span></div>"""
sample_i18n_entries_to_verbete_without_ignore = """<div>Abacaxi<a href="abacaxi"></a>abacaxi<span class="entries">verbete isto é ignorado?</span></div>"""
sample_i18n_glingon_without_ignore_humanized = """<div>
  changed1
  <a href="abacaxi">
  </a>
  changed2
  <span class="entries">
    changed3
    changed4
  </span>
</div>"""
sample_i18n_Abacaxi_to_Pinnaple = """<div>Pinnaple<a href="abacaxi"></a>abacaxi<span class="entries">entries this is ignored?</span></div>"""
sample_map_index = """[ROOT_PARENT]<div> {}
    [0]<span> {"_class": "opaaa", "_id": "doideira"}
        [0][0]"conteudo"
        [0][1]<span> {}
    [1]<span> {}
        [1][0]<img> {}
    [2]<span> {}
        [2][0]<span> {}
        [2][1]\"novo_conteudo\""""

sample_map_index_concatenate_xml = """[ROOT_PARENT]<concatenate> {}
    [0]<div> {}
        [0][0]<span> {}
        [0][1]<concatenate> {}
            [0][1][0]<span> {}
            [0][1][1]<span> {}
        [0][2]<img> {}
    [1]<img> {}
    [2]<xml> {}
        [2][0]"<div id='xml_content'></div>\""""

sample_map_index_empty_concatenate = """[ROOT_PARENT]<div> {}
    [0]<concatenate> {}
        [0][0]<div> {"_class": "second"}
            [0][0][0]<a> {"_href": "localhost"}
                [0][0][0][0]"string link"
        [0][1]<img> {"_alt": "ident equals second"}
    [1]<concatenate> {}"""
sample_source_code = """CONCATENATE(
    DIV(
        SPAN(
        ),
        CONCATENATE(
            SPAN(
            ),
            SPAN(
            )
        ),
        IMG(
        )
    ),
    IMG(
    ),
    XML(
        "<div id='xml_content'></div>"
    )
)"""


class TestHelpers(unittest.TestCase):
    def test0_documentation_examples(self):
        # Main class examples
        class DIV(XmlConstructor):
            def __init__(self, *content, **attributes):
                XmlConstructor.__init__(self, "div", False, False, *content, **attributes)
        self.assertEqual(DIV().xml(), '<div></div>')
        self.assertEqual(
            DIV().xml(),
            '<div></div>'
        )
        self.assertEqual(
            DIV("My content", _class="my_atribute_class").xml(),
            '<div class="my_atribute_class">My content</div>'
        )
        self.assertEqual(
            DIV("My content", _class="my_atribute_class").xml(),
            '<div class="my_atribute_class">My content</div>'
        )
        DIV = XmlConstructor.tagger("div")
        HR = XmlConstructor.tagger("hr", True)
        IMG = XmlConstructor.tagger("img", True)
        BR = XmlConstructor.tagger("br", True, False)
        UL = XmlConstructor.tagger("div")
        HTML = XmlConstructor.tagger('html')
        P = XmlConstructor.tagger('p')
        instanceDIV = DIV("My content", _class="my_atribute_class")
        self.assertEqual(
            instanceDIV.xml(),
            '<div class="my_atribute_class">My content</div>'
        )
        new_instance = DIV("line0", "\nline1")
        self.assertEqual(
            new_instance.xml(),
            '<div>line0\nline1</div>'
        )
        # Examples __init__
        self.assertEqual(
            XmlConstructor.tagger("br", True, False)().xml(),
            '<br>'
        )
        self.assertEqual(
            XmlConstructor.tagger("br", True, True)().xml(),
            '<br />'
        )
        self.assertEqual(
            XmlConstructor.tagger("hr", True, False)(_class="especial_hr").xml(),
            '<hr class="especial_hr">'
        )
        self.assertEqual(
            XmlConstructor.tagger("img", True, False)(_href="#my_url").xml(),
            '<img href="#my_url">'
        )
        self.assertEqual(
            BR().xml(),
            '<br>'
        )
        instanceBR = BR()
        instanceBR.close_void = True  # change state of the attribute
        self.assertEqual(
            instanceBR.xml(),
            '<br />'
        )
        self.assertEqual(
            HR(_class="especial_hr").xml(),
            '<hr class="especial_hr">'
        )
        self.assertEqual(
            IMG(_href="#my_url").xml(),
            '<img href="#my_url">'
        )
        self.assertEqual(
            DIV().xml(),
            '<div></div>'
        )
        self.assertEqual(
            DIV("this", "is", "join", " its no. ", "<tag_evil>evil</tag_evil>").xml(),
            '<div>thisisjoin its no. &lt;tag_evil&gt;evil&lt;/tag_evil&gt;</div>'
        )
        self.assertEqual(
            IMG(_class="images").xml(),
            '<img class="images">'
        )
        BR = XmlConstructor.tagger("br", True, True)
        self.assertEqual(
            BR().xml(),
            '<br />'
        )
        # examples indent_size
        instanceDIV = DIV("my content", _id="my_id")
        otherInstance = DIV("my other content", _id="my_other_id")
        self.assertEqual(
            instanceDIV.xml(),
            '<div id="my_id">my content</div>'
        )
        self.assertEqual(
            otherInstance.xml(),
            '<div id="my_other_id">my other content</div>'
        )
        instanceDIV.minify = False  # @minify is an instance method, this only reflects on this instance
        self.assertEqual(
            instanceDIV.xml(),
            '<div id="my_id">\n  my content\n</div>'
        )
        self.assertEqual(
            otherInstance.xml(),
            '<div id="my_other_id">my other content</div>'
        )
        otherInstance.indent_size = 4  # @indent_size is classmethod, this reflect all instances
        self.assertEqual(
            instanceDIV.xml(),
            '<div id="my_id">\n    my content\n</div>'
        )
        self.assertEqual(
            otherInstance.xml(),
            '<div id="my_other_id">my other content</div>'
        )
        # id
        instanceUL = UL()
        other_instanceUL = DIV()
        self.assertTrue(isinstance(instanceUL.id, int))
        id_instanceUL = instanceUL.id
        self.assertTrue(isinstance(other_instanceUL.id, int))
        id_other_instanceUL = other_instanceUL.id
        new_elements = DIV(instanceUL, other_instanceUL)
        self.assertEqual(new_elements.search(id_instanceUL), [instanceUL])
        self.assertEqual(new_elements.search(id_other_instanceUL), [other_instanceUL])
        self.assertEqual(new_elements[1], other_instanceUL)
        # tag
        my_element = XmlConstructor.tagger('div')
        my_element = DIV()
        self.assertEqual(
            my_element.tag,
            'div'
        )
        new_element = XmlConstructor.tagger('div')
        new_element = DIV()
        self.assertEqual(
            new_element.xml(),
            '<div></div>'
        )
        new_element.tag = 'button'
        self.assertEqual(
            new_element.xml(),
            '<button></button>'
        )
        # append
        my_instance = DIV()
        self.assertEqual(
            my_instance.xml(),
            '<div></div>'
        )
        my_instance.append("content0")
        self.assertEqual(
            my_instance.xml(),
            '<div>content0</div>'
        )
        my_instance.append("content1")
        self.assertEqual(
            my_instance.xml(),
            '<div>content0content1</div>'
        )
        # insert
        my_instance = DIV()
        self.assertEqual(
            my_instance.xml(),
            '<div></div>'
        )
        my_instance.insert(0, "content0")
        self.assertEqual(
            my_instance.xml(),
            '<div>content0</div>'
        )
        my_instance.insert(0, "content-1")
        self.assertEqual(
            my_instance.xml(),
            '<div>content-1content0</div>'
        )
        my_instance.insert(1, "content-1.5")
        self.assertEqual(
            my_instance.xml(),
            '<div>content-1content-1.5content0</div>'
        )
        # replace
        SPAN = XmlConstructor.tagger("span")
        HR = XmlConstructor.tagger("hr", True)
        my_instance = DIV(SPAN(), HR(), DIV())
        self.assertEqual(
            my_instance.xml(),
            '<div><span></span><hr><div></div></div>'
        )
        my_instance.replace(2, SPAN())
        self.assertEqual(
            my_instance.xml(),
            '<div><span></span><hr><span></span></div>'
        )
        # alternative_tag
        my_element = DIV()
        self.assertEqual(
            my_element.alternative_tag,
            'div'
        )
        METACLASS_WITHOUT_TAG = XmlConstructor.tagger('')
        my_element = METACLASS_WITHOUT_TAG("content")
        self.assertEqual(
            my_element.alternative_tag,
            'empty_tag'
        )
        self.assertEqual(
            my_element.source_code(),
            "EMPTY_TAG(\n    'content'\n)"
        )
        self.assertEqual(
            my_element.children_indexes(),
            '[ROOT_PARENT]<empty_tag> {}\n    [0]"content"'
        )
        # before_xml
        my_comment = P("My comment")
        self.assertEqual(
            my_comment.xml(),
            '<p>My comment</p>'
        )
        self.assertEqual(
            my_comment.before_xml,
            ""
        )
        my_comment.before_xml = '<!--This is a comment.-->'
        self.assertEqual(
            my_comment.xml(),
            '<!--This is a comment.--><p>My comment</p>'
        )
        is_html5 = HTML()
        self.assertEqual(
            is_html5.xml(),
            "<html></html>"
        )
        is_html5.before_xml = "<!DOCTYPE html>"
        self.assertEqual(
            is_html5.xml(),
            "<!DOCTYPE html><html></html>"
        )
        # after
        is_comment = P("This is a comment")
        is_not_comment = P("This is not a comment")
        html = HTML(is_comment, is_not_comment)
        self.assertEqual(
            html.xml(),
            '<html><p>This is a comment</p><p>This is not a comment</p></html>'
        )
        self.assertEqual(
            is_comment.after_xml,
            ''
        )
        is_comment.before_xml = '<!--'
        is_comment.after_xml = '-->'
        self.assertEqual(
            is_comment.after_xml,
            '-->'
        )
        self.assertEqual(
            is_comment.xml(),
            '<!--<p>This is a comment</p>-->'
        )
        self.assertEqual(
            html.xml(),
            '<html><!--<p>This is a comment</p>--><p>This is not a comment</p></html>'
        )
        # tag_begin
        instance_element = DIV()
        instance_element.attributes = {"_class": "my_class", "_id": "my_id"}
        self.assertEqual(
            instance_element.xml(),
            '<div class="my_class" id="my_id"></div>'
        )
        self.assertEqual(
            instance_element.tag_begin,
            '<div class="my_class" id="my_id">'
        )
        # tag_end
        instance_element = DIV(**{"_class": "my_class", "_id": "my_id"})
        self.assertEqual(
            instance_element.tag_end,
            '</div>'
        )
        instance_element = HR()
        self.assertEqual(
            instance_element.tag_end,
            ''
        )
        # void
        new_element = XmlConstructor.tagger("button", False)()
        self.assertEqual(
            new_element.void,
            False
        )
        new_element = XmlConstructor.tagger("br", void=True)()
        self.assertEqual(
            new_element.xml(),
            '<br>'
        )
        new_element = XmlConstructor.tagger("hr", True)()
        self.assertEqual(
            new_element.xml(),
            '<hr>'
        )
        new_element = XmlConstructor.tagger("div")()
        self.assertEqual(
            new_element.xml(),
            '<div></div>'
        )
        new_element = XmlConstructor.tagger("h1", False)
        self.assertEqual(
            new_element("My title").xml(),
            '<h1>My title</h1>'
        )
        new_element = XmlConstructor.tagger("mypersonal_tag")()
        self.assertEqual(
            new_element.xml(),
            '<mypersonal_tag></mypersonal_tag>'
        )
        new_element.void = True
        self.assertEqual(
            new_element.xml(),
            '<mypersonal_tag>'
        )
        new_element.close_void = True
        self.assertEqual(
            new_element.xml(),
            '<mypersonal_tag />'
        )
        new_element.void = False
        self.assertEqual(
            new_element.close_void,
            False
        )
        self.assertEqual(
            new_element.xml(),
            '<mypersonal_tag></mypersonal_tag>'
        )
        # close_void
        new_element = XmlConstructor.tagger("button", True)()
        self.assertEqual(
            new_element.close_void,
            False
        )
        new_element = XmlConstructor.tagger("hr", void=True)
        self.assertEqual(
            new_element().close_void,
            False
        )
        self.assertEqual(
            new_element().xml(),
            '<hr>'
        )
        new_element = XmlConstructor.tagger("div", void=False, close_void=True)
        self.assertEqual(
            new_element().close_void,
            False
        )
        self.assertEqual(
            new_element().xml(),
            '<div></div>'
        )
        new_element = XmlConstructor.tagger("br", void=True, close_void=True)
        self.assertEqual(
            new_element().xml(),
            '<br />'
        )
        new_element = XmlConstructor.tagger("hr", True, True)()
        new_element.attributes = {"_class": "has_class"}
        self.assertEqual(
            new_element.xml(),
            '<hr class="has_class" />'
        )
        new_element = XmlConstructor.tagger("hr")()
        self.assertEqual(
            new_element.xml(),
            '<hr></hr>'
        )
        self.assertEqual(
            new_element.void,
            False
        )
        new_element.close_void = True
        self.assertEqual(
            new_element.void,
            True
        )
        self.assertEqual(
            new_element.xml(),
            '<hr />'
        )
        new_element.close_void = False
        self.assertEqual(
            new_element.xml(),
            '<hr>'
        )

    def test1_tags(self):
        self.assertEqual(HTML(HEAD(), BODY()).xml(), "<!DOCTYPE html><html><head></head><body></body></html>")
        self.assertEqual(DIV().xml(), "<div></div>")
        self.assertEqual(IMG().xml(), "<img>")
        self.assertEqual(DIV(_id="my_id").xml(), "<div id=\"my_id\"></div>")
        self.assertEqual(IMG(_src="crazy").xml(), "<img src=\"crazy\">")
        self.assertEqual(
            DIV(_class="my_class", _mytrueattr=True).xml(),
            "<div class=\"my_class\" mytrueattr></div>")
        self.assertEqual(
            DIV(_id="my_id", _none=None, _false=False, without_underline="serius?").xml(),
            "<div id=\"my_id\"></div>")
        self.assertEqual(
            DIV("<b>xsscapedthis</b>").xml(), "<div>&lt;b&gt;xsscapedthis&lt;/b&gt;</div>")
        self.assertEqual(
            DIV(XML("<b>don'txmlscapedthis</b>")).xml(), "<div><b>don'txmlscapedthis</b></div>")

    def test2_invalid_atribute_name(self):
        i = [" ", "=", "'", '"', ">", "<", "/"]
        for x in i:
            b = "_any%sthings" % x
            attr = {b: "invalid_atribute_name"}
            self.assertRaises(ValueError, lambda attr=attr: DIV("any content", **attr))

    def test3_put_obj_python_to_obj_javascript_in_attr(self):
        object_list = [None, "a_string", 1, '1', "2", False, True]
        object_dict = {"list": object_list, 'false': False}
        attr = {"_data-list": object_list, "_data-obj": object_dict}
        self.assertEqual(DIV(**attr).xml(), "".join(['<div data-list=\'[null,',
            ' "a_string", 1, "1", "2", false, true]\' data-obj=\'{"list"&#58; ',
            '[null, "a_string", 1, "1", "2", false, true], ',
            '"false"&#58; false}\'></div>']))

    def test4_sanitize(self):
        permitted_tags = [
            'div',
            'td',
            'b',
            'br/',
            'strong',
            'span',
            'img/',
            'a',
        ]
        allowed_attributes = {
            'a': ['href', 'title'],
            'img': ['src', 'alt'],
            'blockquote': ['type'],
            'td': ['colspan'],
        }

        # test permitted
        for x in permitted_tags:

            if x == "img/":  # alt or src attribute is required. src has to have a valid href
                s_tag = IMG(_alt="empty").xml()
                self.assertEqual(XML(s_tag, sanitize=True,
                    permitted_tags=['img'],
                    allowed_attributes={'img': ['src', 'alt']}).xml(),
                    "<img alt=\"empty\">")
                s_tag = IMG(_src="/image.png").xml()
                self.assertEqual(XML(s_tag, sanitize=True,
                    permitted_tags=['img'],
                    allowed_attributes={'img': ['src', 'alt']}).xml(),
                    "<img src=\"/image.png\">")
            elif x == "a":  # It has to have a valid href or title or not tag empty
                s_tag = A("this is a link", _href="http://web2py.com/").xml()
                self.assertEqual(XML(s_tag, sanitize=True,
                    permitted_tags=['a'],
                    allowed_attributes={'a': ['href', 'title']}).xml(),
                    "<a href=\"http://web2py.com/\">this is a link</a>")
                s_tag = A("without href", _title="this is a link?").xml()
                self.assertEqual(XML(s_tag, sanitize=True,
                    permitted_tags=['a'],
                    allowed_attributes={'a': ['href', 'title']}).xml(),
                    '<a title="this is a link?">without href</a>')
                s_tag = A(_title="empty_tag").xml()
                self.assertEqual(XML(s_tag, sanitize=True,
                    permitted_tags=['a'],
                    allowed_attributes={'a': ['href', 'title']}).xml(),
                    '<a title="empty_tag"></a>')
            else:
                class T(XmlConstructor):
                    def __init__(self, *content, **attributes):
                        XmlConstructor.__init__(self,
                            x if not x[-1:] == "/" else x[0:-1],
                            False if not x[-1:] == "/" else True,
                            *content,
                            **attributes)
                s_tag = T()
                self.assertEqual(XML(s_tag, sanitize=True,
                    permitted_tags=[x.replace("/", "")],
                    allowed_attributes=allowed_attributes).xml(), "<%s></%s>" %
                    (x, x) if not x[-1] == "/" else "<%s>" % (x.replace("/", "")))

        # test tag out of list
        out_of_list = [
            'blockquote', 'i', 'li', 'ol', 'ul', 'p', 'cite', 'code', 'pre',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'table', 'tbody', 'thead', 'tfoot', 'tr'
            'strong']
        for x in out_of_list:
            class T(XmlConstructor):
                def __init__(self, *content, **attributes):
                    XmlConstructor.__init__(self,
                        x if not x[-1:] == "/" else x[0:-1],
                        False if not x[-1:] == "/" else True,
                        *content,
                        **attributes)
            self.assertEqual(XML(T().xml(), sanitize=True,
                permitted_tags=permitted_tags,
                allowed_attributes=allowed_attributes).xml(), "&lt;%s&gt;&lt;/%s&gt;" %
                (x, x))

        # test unusual tags
        for x in ["evil", "n0c1v3"]:
            class T(XmlConstructor):
                def __init__(self, *content, **attributes):
                    XmlConstructor.__init__(self,
                        x,
                        False,
                        *content,
                        **attributes)
            self.assertEqual(XML(T().xml(), sanitize=True,
                permitted_tags=permitted_tags,
                allowed_attributes=allowed_attributes).xml(), "&lt;%s&gt;&lt;/%s&gt;" %
                (x, x))

        # test allowed_attributes
        s_tag = TD("content_td", _colspan="2", _extra_attr="invalid").xml()
        self.assertEqual(XML(s_tag, sanitize=True, permitted_tags=['td'], allowed_attributes={'td': ['colspan']}).xml(),
            '<td colspan="2">content_td</td>')
        s_tag = A("link", _href="http://web2py.com/", _title="my_title").xml()
        self.assertEqual(XML(s_tag, sanitize=True,
            permitted_tags=['a'],
            allowed_attributes={'a': ['href', 'title']}).xml(),
            '<a href="http://web2py.com/" title="my_title">link</a>')
        s_tag = IMG(_alt="empty", _src="/images/logo.png").xml()
        self.assertEqual(XML(s_tag, sanitize=True,
            permitted_tags=['img'],
            allowed_attributes={'img': ['src', 'alt']}).xml(),
            '<img src="/images/logo.png" alt="empty">')
        s_tag = DIV("content", _style="{backgrond-color: red;}").xml()
        self.assertEqual(XML(s_tag, sanitize=True,
            permitted_tags=['div'],
            allowed_attributes={'div': ['style']}).xml(),
            '<div style="{backgrond-color: red;}">content</div>')
        self.assertEqual(XML(A("oh no!", _href="invalid_link").xml(),
            sanitize=True,
            permitted_tags=['a']).xml(), 'oh no!')
        self.assertEqual(XML(DIV("", _onclick="evil()").xml(),
            sanitize=True,
            permitted_tags=['div']).xml(), '<div></div>')

        # valid inside invalid
        EVIL = XmlConstructor.tagger('evil', False, False)
        s_tag = EVIL(DIV('valid'), _style="{backgrond-color: red;}").xml()
        self.assertEqual(XML(s_tag, sanitize=True,
            permitted_tags=['div'],
            allowed_attributes={'div': ['style']}).xml(),
            '&lt;evil&gt;<div>valid</div>&lt;/evil&gt;')
        self.assertEqual(XML(A(IMG(_src="/index.html"), _class="teste").xml(),
            sanitize=True,
        permitted_tags=['a', 'img']).xml(), '<img src="/index.html">')

        # tags deleted even allowed
        self.assertEqual(XML(IMG().xml(), sanitize=True,
            permitted_tags=['img']).xml(), "")
        self.assertEqual(XML(IMG(_src="invalid_url").xml(), sanitize=True,
            permitted_tags=['img']).xml(), "")
        self.assertEqual(XML(IMG(_class="teste").xml(), sanitize=True,
            permitted_tags=['img']).xml(), "")
        self.assertEqual(XML(A(_href="invalid_link").xml(), sanitize=True,
            permitted_tags=['a']).xml(), "")

    def test5_html_to_xmlconstructor(self):
        invert = HtmlToXmlConstructor(sample_html_to_xmlconstructor)
        self.assertEqual(invert.xml(), sample_html_to_xmlconstructor)
        invert.src_attr_dict = False
        self.assertRaises(ValueError, lambda: invert.source_code())
        invert.src_attr_dict = None
        self.assertTrue(isinstance(invert.source_code(), str))
        invert.src_attr_dict = True
        self.assertTrue(isinstance(invert.source_code(), str))

    def test6_search(self):
        repeat_el = [DIV(_repeat_attr="repeat"), DIV(_repeat_attr="repeat"), DIV(_repeat_attr="repeat")]
        experiment = TD("cool experiment")
        id_exp = experiment.id
        sample_search = DIV(
            DIV("class numbers", _class="one two"),
            A(
                DIV("inside A", _id="inside_a"),
                _href="/index.html"),
            DIV("It has the keyword inside too", _class="one without_two"),
            DIV(
                DIV(_strange_attr="yes"),
                DIV(_enabled=True),
                *repeat_el,
                _class="seach by same xml"),
            DIV("dad", experiment),
            A(experiment)
        )
        # no location
        self.assertEqual(sample_search.search(DIV()), [])
        self.assertEqual(sample_search.search(A()), [])
        self.assertEqual(sample_search.search({"_strange_attr": "no"}), [])
        # search by content
        conten_result = [sample_search[1][0], sample_search[2]]
        self.assertEqual(sample_search.search("inside"), conten_result)
        # search by attrs
        element = sample_search[1][0]
        element2 = sample_search[3][0]
        element3 = sample_search[0]
        element4 = sample_search[2]
        element5 = sample_search[3][1]
        self.assertEqual(sample_search.search({"_id": "inside_a"}), [element])
        self.assertEqual(sample_search.search({"_strange_attr": "yes"}), [element2])
        self.assertEqual(sample_search.search({"_repeat_attr": "repeat"}), repeat_el)
        self.assertEqual([x.xml() for x in sample_search.search("experiment")], [experiment.xml(), experiment.xml()])
        self.assertEqual(sample_search.search({"_class": "one"}), [element3, element4])
        self.assertEqual(sample_search.search({"_class": "one two"}), [element3])
        self.assertEqual(sample_search.search({"_class": "two one"}), [element3])
        self.assertEqual(sample_search.search({"class": "one"}), [element3, element4])
        self.assertEqual(sample_search.search({"enabled": True}), [element5])
        # search by id
        self.assertEqual(sample_search.search(id_exp)[0], experiment)
        self.assertEqual(sample_search.search(id_exp)[0].xml(), experiment.xml())

    def test7_append_insert(self):
        to_test = DIV()
        to_test.append(A(_example="gt"))
        self.assertEqual(DIV(A(_example="gt")).xml(), to_test.xml())
        to_test.append(SPAN())
        self.assertEqual(DIV(A(_example="gt"), SPAN()).xml(), to_test.xml())
        to_test.insert(1, IMG(_alt="is_image"))
        self.assertEqual(DIV(A(_example="gt"), IMG(_alt="is_image"), SPAN()).xml(), to_test.xml())

    def test8_humanize(self):
        sample = DIV(
            DIV(
                A("string link", _href="localhost"),
                _class="second"
            ),
            IMG(_alt="ident equals second"),
        )
        self.assertEqual(sample.humanize(), sample_humanize)
        sample = DIV(
            CONCATENATE(
                DIV(
                    A("string link", _href="localhost"),
                    _class="second"
                ),
                IMG(_alt="ident equals second"),
            )
        )
        sample.append(CONCATENATE())
        self.assertEqual(sample.humanize(), sample_humanize)
        sample = CONCATENATE(
            DIV(
                DIV(
                    A("string link", _href="localhost"),
                    _class="second"
                ),
                IMG(_alt="ident equals second"),
            )
        )
        self.assertEqual(sample.humanize(), sample_humanize)
        sample = CONCATENATE(
            DIV(
                DIV(
                    A(
                        CONCATENATE(
                            "string link",
                            SPAN("yes", _class="inline")
                        ),
                        _href="localhost"
                    ),
                    _class="second"
                ),
                IMG(_alt="ident equals second"),
                CONCATENATE(
                    DIV("extra_line1"),
                    DIV("extra_line2")
                )
            )
        )
        self.assertEqual(sample.humanize(), sample_humanize2)

    def test9_i18n(self):
        sample_i18n = DIV(
            "Abacaxi",
            A(_href="abacaxi"),
            XML("abacaxi"),
            SPAN("entries", " this is ignored?", _class="entries")
        )
        Trans = Translator("test_helpers_languages")
        Trans.translate("pt-BR", "entries", "verbete")
        Trans.translate("pt-BR", " this is ignored?", " isto é ignorado?")
        Trans.translate("en-US", "Abacaxi", "Pinnaple")
        Trans.translate("glingon", "Abacaxi", "changed1")
        Trans.translate("glingon", "abacaxi", "changed2")
        Trans.translate("glingon", "entries", "changed3")
        Trans.translate("glingon", " this is ignored?", "changed4")
        original = sample_i18n.xml()
        sample_i18n.i18n(Trans, 'pt-BR', ignored_entries=[" this is ignored?"])
        self.assertNotEqual(original, sample_i18n)
        self.assertEqual(sample_i18n_entries_to_verbete, sample_i18n.xml())
        sample_i18n.i18n(Trans, 'pt-BR')
        self.assertEqual(sample_i18n_entries_to_verbete_without_ignore, sample_i18n.xml())
        sample_i18n.i18n(Trans, 'en-US', ignored_entries=[" this is ignored?"])
        self.assertEqual(sample_i18n_Abacaxi_to_Pinnaple, sample_i18n.xml())
        sample_i18n.i18n(Trans, 'glingon')
        self.assertEqual(sample_i18n_glingon_without_ignore_humanized, sample_i18n.humanize())

    def test10_map_indexes_and_all_children(self):
        map_0 = SPAN(_class="opaaa", _id="doideira")
        map_00 = "conteudo"
        map_01 = SPAN()
        map_0.append(map_00)
        map_0.append(map_01)
        map_1 = SPAN()
        map_10 = IMG()
        map_1.append(map_10)
        map_2 = SPAN()
        map_20 = SPAN()
        map_21 = "novo_conteudo"
        map_2.append(map_20)
        map_2.append(map_21)
        sample_indexes = DIV()
        sample_indexes.append(map_0)
        sample_indexes.append(map_1)
        sample_indexes.append(map_2)
        sample_all_children = {
            '[0]': map_0,
            '[0][0]': map_00,
            '[0][1]': map_01,
            '[1]': map_1,
            '[1][0]': map_10,
            '[2]': map_2,
            '[2][0]': map_20,
            '[2][1]': map_21,
        }
        self.assertDictEqual(sample_all_children, sample_indexes.all_children)
        self.assertEqual(sample_indexes.children_indexes(), sample_map_index)
        self.assertEqual(sample_indexes[0], map_0)
        self.assertEqual(sample_indexes[0][0], map_00)
        self.assertEqual(sample_indexes[0][1], map_01)
        self.assertEqual(sample_indexes[1], map_1)
        self.assertEqual(sample_indexes[1][0], map_10)
        self.assertEqual(sample_indexes[2], map_2)
        self.assertEqual(sample_indexes[2][0], map_20)
        self.assertEqual(sample_indexes[2][1], map_21)
        concate_container = CONCATENATE()
        concate_container.append(sample_indexes)
        self.assertEqual(concate_container[0][0], map_0)
        self.assertEqual(concate_container[0][0][0], map_00)
        self.assertEqual(concate_container[0][0][1], map_01)
        self.assertEqual(concate_container[0][1], map_1)
        self.assertEqual(concate_container[0][1][0], map_10)
        self.assertEqual(concate_container[0][2], map_2)
        self.assertEqual(concate_container[0][2][0], map_20)
        self.assertEqual(concate_container[0][2][1], map_21)
        sample_concatenate = CONCATENATE(
            DIV(
                SPAN(),
                CONCATENATE(
                    SPAN(),
                    SPAN()
                ),
                IMG(),
            ),
            IMG(),
            XML("<div id='xml_content'></div>")
        )
        self.assertEqual(sample_concatenate.children_indexes(), sample_map_index_concatenate_xml)
        sample_empty_concatenate = DIV(
            CONCATENATE(
                DIV(
                    A("string link", _href="localhost"),
                    _class="second"
                ),
                IMG(_alt="ident equals second")
            )
        )
        sample_empty_concatenate.append(CONCATENATE())
        self.assertEqual(sample_empty_concatenate.children_indexes(), sample_map_index_empty_concatenate)

    def test11_source_code(self):
        s1 = CONCATENATE(
            DIV(
                SPAN(
                ),
                CONCATENATE(
                    SPAN(
                    ),
                    SPAN(
                    ),
                ),
                IMG(
                ),
            ),
            IMG(
            ),
            XML(
                "<div id='xml_content'></div>",
            ),
        )
        self.assertEqual(s1.source_code(), sample_source_code)

    def test12_root_parent(self):
        son = A()
        sample2 = CONCATENATE(
            DIV(
                SPAN(
                ),
                CONCATENATE(
                    SPAN(
                    ),
                    SPAN(
                    ),
                ),
                IMG(
                ),
            ),
            IMG(
            ),
            XML(
                "<div id='xml_content'></div>",
            ),
        )
        sample2[0][1][1].append(son)
        father = DIV()
        father.append(sample2)
        self.assertEqual(father.id, son.root_parent.id)
        self.assertEqual(sample2.parent.id, father.id)

    def test13_instances_copy(self):
        son = B()
        father = DIV(son, son, SPAN(son, HEAD(son, son)))
        self.assertEqual(len(son.was_copied), 5)
        self.assertEqual(len(son.was_copied.difference(set([son]))), 4)
        self.assertEqual(len(set(father.search(son)).difference(set([son]))), 4)


if __name__ == '__main__':
    unittest.main()
