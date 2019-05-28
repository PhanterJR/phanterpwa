from phanterpwa.helpers import DIV, IMG, XML, A, TD, HtmlToXmlConstructor
from phanterpwa.xmlconstructor import XmlConstructor
import unittest

sample_html_to_xmlconstructor = """<div id="test02" enabled empty="=">
  <div style="background-color&#58;blue; width&#58;100%; height&#58;40px;">
    OOOOOPAAAAA
  </div>
  <div json='{"teste"&#58; true}' testando-outro='["macaco", true, "boi"]' texto_com_aspas="queria muito &quot;tentar&quot; ou não 'tentar'" list_none="[null]" dict='{"testesss"&#58; true}' json_dums="[null, true, false]">
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


class TestHelpers(unittest.TestCase):
    def test_tags(self):
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

    def test_invalid_atribute_name(self):
        i = [" ", "=", "'", '"', ">", "<", "/"]
        for x in i:
            b = "_any%sthings" % x
            attr = {b: "invalid_atribute_name"}
            self.assertRaises(ValueError, lambda attr=attr: DIV("any content", **attr))

    def test_put_obj_python_to_obj_javascript_in_attr(self):
        object_list = [None, "a_string", 1, '1', "2", False, True]
        object_dict = {"list": object_list, 'false': False}
        attr = {"_data-list": object_list, "_data-obj": object_dict}
        self.assertEqual(DIV(**attr).xml(), "".join(['<div data-list=\'[null,',
            ' "a_string", 1, "1", "2", false, true]\' data-obj=\'{"list"&#58; ',
            '[null, "a_string", 1, "1", "2", false, true], ',
            '"false"&#58; false}\'></div>']))

    def test_sanitize(self):
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
                    "<img alt=\"empty\"/>")
                s_tag = IMG(_src="/image.png").xml()
                self.assertEqual(XML(s_tag, sanitize=True,
                    permitted_tags=['img'],
                    allowed_attributes={'img': ['src', 'alt']}).xml(),
                    "<img src=\"/image.png\"/>")
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
                s_tag = T().xml()
                self.assertEqual(XML(s_tag, sanitize=True,
                    permitted_tags=[x.replace("/", "")],
                    allowed_attributes=allowed_attributes).xml(), "<%s></%s>" %
                    (x, x) if not x[-1] == "/" else "<%s>" % (x.replace("/", "/")))

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
            '<img src="/images/logo.png" alt="empty"/>')
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
        class EVIL(XmlConstructor):
            def __init__(self, *content, **attributes):
                XmlConstructor.__init__(self,
                    'evil',
                    False,
                    *content,
                    **attributes)
        s_tag = EVIL(DIV('valid'), _style="{backgrond-color: red;}").xml()
        self.assertEqual(XML(s_tag, sanitize=True,
            permitted_tags=['div'],
            allowed_attributes={'div': ['style']}).xml(),
            '&lt;evil&gt;<div>valid</div>&lt;/evil&gt;')
        self.assertEqual(XML(A(IMG(_src="/index.html"), _class="teste").xml(),
            sanitize=True,
        permitted_tags=['a', 'img']).xml(), '<img src="/index.html"/>')

        # tags deleted even allowed
        self.assertEqual(XML(IMG().xml(), sanitize=True,
            permitted_tags=['img']).xml(), "")
        self.assertEqual(XML(IMG(_src="invalid_url").xml(), sanitize=True,
            permitted_tags=['img']).xml(), "")
        self.assertEqual(XML(IMG(_class="teste").xml(), sanitize=True,
            permitted_tags=['img']).xml(), "")
        self.assertEqual(XML(A(_href="invalid_link").xml(), sanitize=True,
            permitted_tags=['a']).xml(), "")

    def test_html_to_xmlconstructor(self):
        invert = HtmlToXmlConstructor(sample_html_to_xmlconstructor)
        self.assertEqual(invert.xml(), sample_html_to_xmlconstructor)

    def test_search(self):
        repeat_el = [DIV(_repeat_attr="repeat"), DIV(_repeat_attr="repeat"), DIV(_repeat_attr="repeat")]
        experiment = TD("cool experiment")
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
        self.assertEqual(sample_search.search({"_id": "inside_a"}), [element])
        self.assertEqual(sample_search.search({"_strange_attr": "yes"}), [element2])
        self.assertEqual(sample_search.search({"_repeat_attr": "repeat"}), repeat_el)
        self.assertEqual([x.xml() for x in sample_search.search("experiment")], [experiment.xml(), experiment.xml()])


if __name__ == '__main__':
    unittest.main()
