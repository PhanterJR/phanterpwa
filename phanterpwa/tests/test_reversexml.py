# -*- coding: utf-8 -*-
import unittest
import os

from phanterpwa.reversexml import (
    HtmlToXmlConstructor,
    force_minify_string_content
)


sample_example_1 = """HTML(
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
)"""
sample_example_2 = """CONCATENATE(
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
)"""

sample_html_to_xmlconstructor = """<div id="test02" enabled empty="=">
  <div style="background-color:blue; width:100%; height:40px;">
    OOOOOPAAAAA
    OBA
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

sample = '''
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
'''

sample2 = '''<html><head><meta charset="utf-8"></head><body> Forces the minification of the string content by removing multiple empty spaces, line breaks, tabs replacing with a single space. </body></html>'''

sample3 = '''HTML(
    HEAD(
        META(
            _charset='utf-8'
        )
    ),
    BODY(
        ' Forces the minification of the string content by removing multiple empty spaces, line breaks, tabs replacing with a single space. '
    )
)'''


class TestReverseXml(unittest.TestCase):

    def test0_documentation_examples(self):

        html_to_xmlconstructor_instance = HtmlToXmlConstructor("<html><head><meta charset=\"UTF-8\"></head><body>" +
            "<nav class=\"navbar\"><buttom>start</buttom></nav><main id=\"my_content\"><div class=\"row\"><div>my" +
            " content</div></div></main></body></html>")

        self.assertEqual(
            html_to_xmlconstructor_instance.xmlconstructor_code(),
            sample_example_1
        )
        html_to_xmlconstructor_instance = HtmlToXmlConstructor("<div data-dict=\"i am in dict\" class=\"my_class\">" +
            "content1</div><div class=\"my_class\">content2</div>")
        self.assertEqual(
            html_to_xmlconstructor_instance.xmlconstructor_code(),
            sample_example_2
        )
        html_to_xmlconstructor_instance = HtmlToXmlConstructor(sample)
        self.assertEqual(
            html_to_xmlconstructor_instance.xml(),
            sample
        )
        self.assertEqual(
            force_minify_string_content(html_to_xmlconstructor_instance).xml(),
            sample2
        )
        self.assertEqual(
            force_minify_string_content(html_to_xmlconstructor_instance).xmlconstructor_code(),
            sample3
        )

    def test1_html_to_xmlconstructor(self):
        invert = HtmlToXmlConstructor(sample_html_to_xmlconstructor)
        self.assertEqual(invert.xml(), sample_html_to_xmlconstructor)
        invert.src_attr_dict = False
        self.assertRaises(ValueError, lambda: invert.source_code())
        invert.src_attr_dict = None
        self.assertTrue(isinstance(invert.source_code(), str))
        invert.src_attr_dict = True
        self.assertTrue(isinstance(invert.source_code(), str))


if __name__ == '__main__':
    unittest.main()
