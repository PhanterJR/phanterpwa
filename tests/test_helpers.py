# -*- coding: utf-8 -*-
import unittest
import os
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
    B,
    SCRIPT
)
from phanterpwa.reversexml import (
    HtmlToXmlConstructor
)
from phanterpwa.xmlconstructor import XmlConstructor
from phanterpwa.i18n import (
    Translator
)
sample_content_test0 = """<div>
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
</div>"""
sample_test0_source_code00 = """DIV(
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
)"""
sample_test0_source_code01 = """from phanterpwa.helpers import (
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
"""
sample_test0_source_code02 = """from phanterpwa.xmlconstructor import XmlConstructor
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
SAMPLE_i18n1 = """<div>
  <p>
    <span phanterpwa_i18n='{"pt-BR": {"Apple": "Ma\\u00e7\\u00e3"}}'>Apple</span>
    <span phanterpwa_i18n='{"pt-BR": {"Orange": "Laranja"}, "pt-PT": {"Orange": "Laranja"}}'>Orange</span>
    <span phanterpwa_i18n='{"pt-PT": {"Grape": "Uva"}}'>Grape</span>
    Do not have translate
  </p>
</div>"""
SAMPLE_i18n2 = """<div>
  <p>
    Apple
    Orange
    Grape
    Do not have translate
  </p>
</div>"""
SAMPLE_i18n3 = """<div>
  <p>
    <i18n phanterpwa_i18n='{"pt-BR": {"Apple": "Ma\\u00e7\\u00e3"}}'>Apple</i18n>
    <i18n phanterpwa_i18n='{"pt-BR": {"Orange": "Laranja"}, "pt-PT": {"Orange": "Laranja"}}'>Orange</i18n>
    <i18n phanterpwa_i18n='{"pt-PT": {"Grape": "Uva"}}'>Grape</i18n>
    Do not have translate
  </p>
</div>"""
SAMPLE_i18n_method0 = """<div>
  Can I use formatter method? {{response}}
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
</div>"""
SAMPLE_i18n_method1 = """<div>
  <span phanterpwa_i18n='{"pt-BR": {"Can I use formatter method? {{response}}": "Posso usar o m\\u00e9todo formatter? {{response}}"}}'>Can I use formatter method? {{response}}</span>
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
</div>"""
SAMPLE_i18n_method2 = """<div>
  <i18n phanterpwa_i18n='{"pt-BR": {"Can I use formatter method? {{response}}": "Posso usar o m\\u00e9todo formatter? {{response}}"}}'>Can I use formatter method? {{response}}</i18n>
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
</div>"""
SAMPLE_i18n_method3 = """<div>
  Can I use formatter method? {{response}}
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
</div>"""
SAMPLE_i18n_method4 = """<div>
  Can I use formatter method? {{response}}
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
</div>"""
SAMPLE_i18n_method5 = """<div>
  Can I use formatter method? {{response}}
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
</div>"""
SAMPLE_i18n_method6 = """<div>
  Posso usar o método formatter? {{response}}
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
</div>"""
SAMPLE_i18n_method7 = """<div>
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
</div>"""
sample_sass = """$COLOR: orange
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
      border-radius: $BORDERRADIUS"""
sample_css = """.example_container * {
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



class TestHelpers(unittest.TestCase):
    def test0_documentation_examples(self):

        # Main class examples
        class DIV(XmlConstructor):
            def __init__(self, *content, **attributes):
                XmlConstructor.__init__(self, "div", False, *content, **attributes)
        self.assertEqual(DIV().xml(), '<div></div>')
        self.assertEqual(
            DIV().xml(),
            '<div></div>'
        )
        DIV = XmlConstructor.tagger("div")
        IMG = XmlConstructor.tagger("img", True)
        HR = XmlConstructor.tagger("hr", True)
        BR = XmlConstructor.tagger("br", True)
        UL = XmlConstructor.tagger("div")
        HTML = XmlConstructor.tagger('html')
        P = XmlConstructor.tagger('p')
        STRONG = XmlConstructor.tagger("strong")
        A = XmlConstructor.tagger("a")
        BUTTON = XmlConstructor.tagger('button')
        self.assertEqual(
            DIV("My content", _class="my_atribute_class").xml(),
            '<div class="my_atribute_class">My content</div>'
        )
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

        # __init__()
        instenceBR = BR()
        self.assertEqual(
            instenceBR.xml(),
            '<br>'
        )
        self.assertEqual(
            XmlConstructor.tagger("hr", True)(_class="especial_hr").xml(),
            '<hr class="especial_hr">'
        )
        self.assertEqual(
            XmlConstructor.tagger("img", True)(_href="#my_url").xml(),
            '<img href="#my_url">'
        )
        instanceBR = BR()
        self.assertEqual(
            instanceBR.xml(),
            '<br>'
        )
        instanceBR.close_void = True
        self.assertEqual(
            instanceBR.xml(),
            '<br />'
        )
        instanceHR = HR(_class="especial_hr")
        self.assertEqual(
            instanceHR.xml(),
            '<hr class="especial_hr" />'
        )
        instanceBR.close_void = False
        self.assertEqual(
            instanceHR.xml(),
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
        BR = XmlConstructor.tagger("br", True)
        instanceBR = BR()
        self.assertEqual(
            instanceBR.xml(),
            '<br>'
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

        # introspect
        instanceDIV = DIV()
        self.assertEqual(
            instanceDIV.introspect,
            "<class 'phanterpwa.xmlconstructor.XmlConstructor.tagger.<locals>.TAGGER'> {id: %s, tag: div}" % instanceDIV.id
        )

        # all_instances
        XmlConstructor._all_instances = {}
        instanceDIV = DIV(SPAN() * 3)
        self.assertEqual(
            set([instanceDIV]).union(set([x for x in instanceDIV.content])),
            set([instanceDIV.all_instances[x] for x in instanceDIV.all_instances])
        )

        # tag_list
        XmlConstructor._tag_list = []
        instanceDIV = DIV(SPAN() * 3)
        self.assertEqual(
            set(instanceDIV.tag_list),
            set(['div', 'span'])
        )

        # was_copied
        sourceInstance = SPAN("Is this the same instance? get id")
        containerDIV = DIV(sourceInstance, sourceInstance, sourceInstance)
        self.assertEqual(
            containerDIV.xml(),
            '<div><span>Is this the same instance? get id</span><span>Is this the same instance? get id</span><span>Is this the same instance? get id</span></div>'
        )
        sourceInstance.content = "changed!"
        self.assertEqual(
            containerDIV.xml(),
            '<div><span>changed!</span><span>Is this the same instance? get id</span><span>Is this the same instance? get id</span></div>'
        )
        for x in sourceInstance.was_copied:
            x.content = "changed!"
        self.assertEqual(
            containerDIV.xml(),
            '<div><span>changed!</span><span>changed!</span><span>changed!</span></div>'
        )

        # root_parent and parent
        child_instance = DIV("I am a child")
        root_parent = DIV(SPAN(child_instance), SPAN())
        self.assertEqual(
            root_parent.xml(),
            '<div><span><div>I am a child</div></span><span></span></div>'
        )
        self.assertEqual(
            child_instance.xml(),
            '<div>I am a child</div>'
        )
        self.assertEqual(
            child_instance.parent.xml(),
            '<span><div>I am a child</div></span>'
        )
        self.assertEqual(
            child_instance.root_parent.xml(),
            '<div><span><div>I am a child</div></span><span></span></div>'
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

        # xml_content
        html = DIV(SPAN(DIV()), SPAN())
        self.assertEqual(
            html.xml(),
            '<div><span><div></div></span><span></span></div>'
        )
        self.assertEqual(
            html.xml_content,
            '<span><div></div></span><span></span>'
        )

        # xml_attributes
        instanceDIV = DIV(_id="my_id", _class="my_class")
        self.assertEqual(
            instanceDIV.xml_attributes,
            'id="my_id" class="my_class"'
        )

        # xml_humanized_content
        instanceDIV = DIV(SPAN("My content"), DIV("Other content"))
        self.assertEqual(
            instanceDIV.xml_humanized_content,
            '\n  <span>\n    My content\n  </span>\n  <div>\n    Other content\n  </div>'
        )

        # all_children
        instanceDIV = DIV(SPAN(A(BUTTON("the direct parent is button"))))
        comp = {
            '[0]': 'index: [0] - xml: <span><a><button>the direct parent is button</button></a></span>',
            '[0][0]': 'index: [0][0] - xml: <a><button>the direct parent is button</button></a>',
            '[0][0][0]': 'index: [0][0][0] - xml: <button>the direct parent is button</button>',
            '[0][0][0][0]': 'index: [0][0][0][0] - xml: the direct parent is button',
        }
        for x in instanceDIV.all_children:
            self.assertEqual('index: {0} - xml: {1}'.format(x, instanceDIV.all_children[x]),
                comp[x]
            )

        # tag
        instanceDIV = DIV()
        self.assertEqual(
            instanceDIV.tag,
            'div'
        )
        my_instance = DIV()
        self.assertEqual(
            my_instance.xml(),
            '<div></div>'
        )
        my_instance.tag = 'button'
        self.assertEqual(
            my_instance.xml(),
            '<button></button>'
        )

        # void
        my_instance = XmlConstructor.tagger("button", False)()
        self.assertEqual(
            my_instance.void,
            False
        )
        my_instance = XmlConstructor.tagger("br", void=True)()
        self.assertEqual(
            my_instance.xml(),
            '<br>'
        )
        my_instance = XmlConstructor.tagger("hr", True)()
        self.assertEqual(
            my_instance.xml(),
            '<hr>'
        )
        my_instance = XmlConstructor.tagger("div")()
        self.assertEqual(
            my_instance.xml(),
            '<div></div>'
        )
        my_instance = XmlConstructor.tagger("h1", False)
        self.assertEqual(
            my_instance("My title").xml(),
            '<h1>My title</h1>'
        )
        my_instance = XmlConstructor.tagger("mypersonal_tag")()
        self.assertEqual(
            my_instance.xml(),
            '<mypersonal_tag></mypersonal_tag>'
        )
        my_instance.void = True
        self.assertEqual(
            my_instance.xml(),
            '<mypersonal_tag>'
        )
        my_instance.void = False
        self.assertEqual(
            my_instance.xml(),
            '<mypersonal_tag></mypersonal_tag>'
        )

        # close_void
        my_instance = XmlConstructor.tagger("meta", True)(_charset="utf-8")
        self.assertEqual(
            my_instance.xml(),
            '<meta charset="utf-8">'
        )
        self.assertEqual(
            my_instance.close_void,
            False
        )
        my_instance = XmlConstructor.tagger("hr", void=True)()
        self.assertEqual(
            my_instance.close_void,
            False
        )
        self.assertEqual(
            my_instance.xml(),
            '<hr>'
        )
        my_instance = XmlConstructor.tagger("div", void=False)()
        self.assertEqual(
            my_instance.close_void,
            False
        )
        self.assertEqual(
            my_instance.xml(),
            '<div></div>'
        )
        my_instance = XmlConstructor.tagger("br", void=True)()
        my_instance.close_void = True
        self.assertEqual(
            my_instance.xml(),
            '<br />'
        )
        my_instance2 = XmlConstructor.tagger("hr", True)()
        my_instance2.attributes = {"_class": "has_class"}
        self.assertEqual(
            my_instance2.xml(),
            '<hr class="has_class" />'
        )
        my_instance = XmlConstructor.tagger("hr")()
        self.assertEqual(
            my_instance.xml(),
            '<hr></hr>'
        )
        my_instance.close_void = True
        self.assertEqual(
            my_instance.xml(),
            '<hr></hr>'
        )
        my_instance.void = True
        self.assertEqual(
            my_instance.xml(),
            '<hr />'
        )
        my_instance.close_void = False
        self.assertEqual(
            my_instance.xml(),
            '<hr>'
        )

        # minify
        instanceDIV = DIV(DIV("content", _id="id_child"), _id="id_parent", _class="my_div")
        otherInstanceDIV = DIV("other_instance", _id="id_other")
        self.assertEqual(
            otherInstanceDIV.minify,
            True
        )
        self.assertEqual(
            instanceDIV.minify,
            True
        )
        self.assertEqual(
            instanceDIV.xml(),
            '<div id="id_parent" class="my_div"><div id="id_child">content</div></div>'
        )
        self.assertEqual(
            otherInstanceDIV.xml(),
            '<div id="id_other">other_instance</div>'
        )
        instanceDIV.minify = False
        self.assertEqual(
            otherInstanceDIV.minify,
            False
        )
        self.assertEqual(
            instanceDIV.xml(),
            '<div id="id_parent" class="my_div">\n  <div id="id_child">\n    content\n  </div>\n</div>'
        )
        self.assertEqual(
            otherInstanceDIV.xml(),
            '<div id="id_other">\n  other_instance\n</div>'
        )
        instanceDIV.minify = True

        # indent_size
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
        instanceDIV.minify = False
        self.assertEqual(
            instanceDIV.xml(),
            '<div id="my_id">\n  my content\n</div>'
        )
        self.assertEqual(
            otherInstance.xml(),
            '<div id="my_other_id">\n  my other content\n</div>'
        )
        instanceDIV.indent_size = 4
        self.assertEqual(
            instanceDIV.xml(),
            '<div id="my_id">\n    my content\n</div>'
        )
        instanceDIV.minify = True
        instanceDIV.indent_size = 2
        self.assertEqual(
            otherInstance.xml(),
            '<div id="my_other_id">my other content</div>'
        )

        # escape_string
        instanceSPAN = SPAN("<evil>I will destroy you.</evil>")
        self.assertEqual(
            instanceSPAN.xml(),
            '<span>&lt;evil&gt;I will destroy you.&lt;/evil&gt;</span>'
        )
        instanceSPAN.escape_string=False
        self.assertEqual(
            instanceSPAN.xml(),
            '<span><evil>I will destroy you.</evil></span>'
        )
        self.assertEqual(
            DIV("<other_evil>", instanceSPAN, "</other_evil>").xml(),
            '<div>&lt;other_evil&gt;<span><evil>I will destroy you.</evil></span>&lt;/other_evil&gt;</div>'
        )

        # alternative_tag
        instanceDIV = DIV()
        self.assertEqual(
            instanceDIV.alternative_tag,
            'div'
        )
        METACLASS_WITHOUT_TAG = XmlConstructor.tagger('')
        instanceEmptyTag = METACLASS_WITHOUT_TAG("content")
        self.assertEqual(
            instanceEmptyTag.alternative_tag,
            'empty_tag'
        )
        self.assertEqual(
            instanceEmptyTag.source_code(),
            "EMPTY_TAG(\n    'content'\n)"
        )
        self.assertEqual(
            instanceEmptyTag.children_indexes(),
            '[ROOT_PARENT]<empty_tag> {}\n    [0]"content"'
        )
        instanceEmptyTag.alternative_tag = "new_alternative_name_to_tag"
        self.assertEqual(
            instanceEmptyTag.source_code(),
            "NEW_ALTERNATIVE_NAME_TO_TAG(\n    'content'\n)"
        )
        self.assertEqual(
            instanceEmptyTag.children_indexes(),
            '[ROOT_PARENT]<new_alternative_name_to_tag> {}\n    [0]"content"'
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

        # after_xml
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

        # content
        d_content = DIV("content")
        Instance = DIV("This", "is", d_content)
        self.assertEqual(
            Instance.xml(),
            '<div>Thisis<div>content</div></div>'
        )
        self.assertEqual(
            Instance.content,
            ('This', 'is', d_content)
        )
        instanceDIV = XmlConstructor.tagger("div")()
        instanceDIV.content = "my new content"
        self.assertEqual(
            instanceDIV.xml(),
            '<div>my new content</div>'
        )
        instanceDIV = DIV()
        instanceA = A("click ", STRONG("here"), _href="#my_url")
        instanceDIV.content = instanceA
        self.assertEqual(
            instanceDIV.xml(),
            '<div><a href="#my_url">click <strong>here</strong></a></div>'
        )
        other_element = DIV([SPAN("Hello"), HR(), "World"])
        list_el = [other_element, other_element]
        set_el = set(list_el)
        tuple_el = (list_el, HR(), set_el, "final string")
        new_element = DIV()
        new_element.content = ['my_', 'content', SPAN('span, span, span'), tuple_el]
        self.assertEqual(
            new_element.humanize(),
            sample_content_test0
        )
        instanceDIV1 = DIV("content")
        instanceDIV1.content = dict(_id="my_id")
        self.assertEqual(
            instanceDIV1.xml(),
            '<div id="my_id"></div>'
        )
        instanceDIV.content = lambda: (SPAN("span * 3") * 3) + DIV("plus")
        self.assertEqual(
            instanceDIV.xml(),
            '<div><span>span * 3</span><span>span * 3</span><span>span * 3</span><div>plus</div></div>'
        )
        instanceDIV1.content = ["new_content", dict(_class="my_class")]
        self.assertEqual(
            instanceDIV1.xml(),
            '<div class="my_class">new_content</div>'
        )
        BR = XmlConstructor.tagger("br", True)
        instanceDIV1.content = [set(["new_content", "new_content"]), [BR() * 2], {'_class': 'new_class'}]
        instanceDIV1.close_void = True
        self.assertEqual(
            instanceDIV1.xml(),
            '<div class="new_class">new_content<br /><br /></div>'
        )
        instanceDIV1.close_void = False

        # attributes
        instanceDIV.attributes = {"_class": "my_class", "_id": "my_id"}
        instanceDIV.attributes
        {"_class": "my_class", "_id": "my_id"}
        instanceBUTTON = BUTTON("Disabled Button")
        instanceBUTTON.attributes = 'disabled'
        self.assertEqual(
            instanceBUTTON.xml(),
            '<button disabled>Disabled Button</button>'
        )
        instanceDIV = DIV("My Content", _class="this will be replaced", go_to_kargs="go_to_kargs")
        instanceDIV.attributes = {"_class": "my_class", "_id": "my_id"}
        self.assertEqual(
            instanceDIV.xml(),
            '<div class="my_class" id="my_id">My Content</div>'
        )
        instanceDIV = DIV(_class="my_class", _underline="_underline", without_underline="without_underline")
        self.assertEqual(
            instanceDIV.xml(),
            '<div class="my_class" underline="_underline"></div>'
        )
        self.assertEqual(
            instanceDIV.attributes,
            {'_class': 'my_class', '_underline': '_underline'}
        )
        self.assertEqual(
            instanceDIV.kargs,
            {'without_underline': 'without_underline'}
        )
        instanceDIV.attributes = {"_teste": lambda: "false"}
        self.assertEqual(
            instanceDIV.xml(),
            '<div teste=false></div>'
        )
        self.assertTrue(
            callable(instanceDIV['_teste']),
        )
        instanceDIV = DIV(_id="my_class", _bye=None, _class=False)
        self.assertEqual(
            instanceDIV.xml(),
            '<div id="my_class"></div>'
        )
        self.assertEqual(
            instanceDIV.attributes,
            {'_id': 'my_class'}
        )
        instanceDIV.content = lambda: (SPAN("span * 3") * 3) + DIV("plus")
        self.assertEqual(
            instanceDIV.xml(),
            '<div id="my_class"><span>span * 3</span><span>span * 3</span><span>span * 3</span><div>plus</div></div>'
        )

        # src_attr_dict
        instanceDIV = DIV(HR(), SPAN(_class="the valid karg"))
        instanceDIV.attributes = {"_invalid-attr-in-karg": "the_key_is_valis_in_html5"}
        self.assertEqual(
            instanceDIV.source_code(),
            "DIV(\n    HR(\n    ),\n    SPAN(\n        _class='the valid karg'\n    ),\n    **{\n        '_invalid-attr-in-karg': 'the_key_is_valis_in_html5'\n    }\n)"
        )
        instanceDIV.src_attr_dict = True
        self.assertEqual(
            instanceDIV.source_code(),
            "DIV(\n    HR(\n    ),\n    SPAN(\n        **{\n            '_class': 'the valid karg'\n        }\n    ),\n    **{\n        '_invalid-attr-in-karg': 'the_key_is_valis_in_html5'\n    }\n)"
        )
        instanceDIV.src_attr_dict = False
        self.assertRaises(ValueError, lambda: instanceDIV.source_code())
        instanceDIV.src_attr_dict = None

        # i18nInstance
        instanceDIV = DIV(P("Monkey"))
        self.assertEqual(
            instanceDIV.humanize(),
            '<div>\n  <p>\n    Monkey\n  </p>\n</div>'
        )
        i18nMyInstance = Translator("path_of_languages", debug=True)
        i18nMyInstance.translate("pt-BR", "Monkey", "Macaco")
        i18nMyInstance.translate("fr", "Monkey", "Singe")
        i18nMyInstance.translate("es", "Monkey", "Mono")
        instanceDIV.i18nInstance = i18nMyInstance
        self.assertEqual(
            instanceDIV.humanize(),
            '<div>\n  <p>\n    <span phanterpwa_i18n=\'{"es": {"Monkey": "Mono"}, "fr": {"Monkey": "Singe"}, "pt-BR": {"Monkey": "Macaco"}}\'>Monkey</span>\n  </p>\n</div>'
        )
        instanceDIV.dictionary = 'fr'
        self.assertEqual(
            instanceDIV.humanize(),
            '<div>\n  <p>\n    Singe\n  </p>\n</div>'
        )

        # tag_translation
        i18nMyInstance = Translator("path_of_languages", debug=True)
        i18nMyInstance.translate("pt-BR", "Apple", "Maçã")
        i18nMyInstance.translate("pt-BR", "Orange", "Laranja")
        i18nMyInstance.translate("pt-PT", "Orange", "Laranja")
        i18nMyInstance.translate("pt-PT", "Grape", "Uva")
        instanceDIV = DIV(P("Apple", "Orange", "Grape", "Do not have translate"))
        instanceDIV.i18nInstance = i18nMyInstance
        self.assertEqual(
            instanceDIV.tag_translation,
            "span"
        )
        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_i18n1
        )
        instanceDIV.tag_translation = None

        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_i18n2
        )
        instanceDIV.tag_translation = "i18n"

        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_i18n3
        )

        # dictionary
        instanceDIV = DIV(P("The book is on the table"))
        self.assertEqual(
            instanceDIV.humanize(),
            '<div>\n  <p>\n    The book is on the table\n  </p>\n</div>'
        )
        i18nMyInstance = Translator("path_of_languages", debug=True)
        i18nMyInstance.translate("pt-BR", "The book is on the table", "O livro está sobre a mesa")
        i18nMyInstance.translate("fr", "The book is on the table", "Le livre est sur la table")
        i18nMyInstance.translate("es", "The book is on the table", "El libro está sobre la mesa")
        instanceDIV.i18nInstance = i18nMyInstance
        self.assertEqual(
            instanceDIV.humanize(),
            '<div>\n  <p>\n    <span phanterpwa_i18n=\'{"es": {"The book is on the table": "El libro est\\u00e1 sobre la mesa"}, "fr": {"The book is on the table": "Le livre est sur la table"}, "pt-BR": {"The book is on the table": "O livro est\\u00e1 sobre a mesa"}}\'>The book is on the table</span>\n  </p>\n</div>'
        )
        instanceDIV.dictionary = 'fr'
        self.assertEqual(
            instanceDIV.humanize(),
            '<div>\n  <p>\n    Le livre est sur la table\n  </p>\n</div>'
        )

        # do_not_translate
        instanceDIV = DIV(P("The colors ", " Blue ", "and", " Green ", "are not translated."))
        self.assertEqual(
            instanceDIV.xml(),
            '<div><p>The colors  Blue and Green are not translated.</p></div>'
        )
        i18nMyInstance = Translator("path_of_languages", debug=True)
        i18nMyInstance.translate("pt-BR", "The colors ", "As cores ")
        i18nMyInstance.translate("pt-BR", " Blue ", " Azul ")
        i18nMyInstance.translate("pt-BR", "and", "e")
        i18nMyInstance.translate("pt-BR", " Green ", "Verde")
        i18nMyInstance.translate("pt-BR", "are not translated.", "não são traduzidas.")
        instanceDIV.i18nInstance = i18nMyInstance
        self.assertEqual(
            instanceDIV.humanize(),
            '<div>\n  <p>\n    <span phanterpwa_i18n=\'{"pt-BR": {"The colors ": "As cores "}}\'>The colors </span>\n    <span phanterpwa_i18n=\'{"pt-BR": {" Blue ": " Azul "}}\'> Blue </span>\n    <span phanterpwa_i18n=\'{"pt-BR": {"and": "e"}}\'>and</span>\n    <span phanterpwa_i18n=\'{"pt-BR": {" Green ": "Verde"}}\'> Green </span>\n    <span phanterpwa_i18n=\'{"pt-BR": {"are not translated.": "n\\u00e3o s\\u00e3o traduzidas."}}\'>are not translated.</span>\n  </p>\n</div>'
        )
        instanceDIV.do_not_translate = [" Blue ", " Green "]
        self.assertEqual(
            instanceDIV.humanize(),
            '<div>\n  <p>\n    <span phanterpwa_i18n=\'{"pt-BR": {"The colors ": "As cores "}}\'>The colors </span>\n     Blue \n    <span phanterpwa_i18n=\'{"pt-BR": {"and": "e"}}\'>and</span>\n     Green \n    <span phanterpwa_i18n=\'{"pt-BR": {"are not translated.": "n\\u00e3o s\\u00e3o traduzidas."}}\'>are not translated.</span>\n  </p>\n</div>'
        )
        instanceDIV.dictionary = "pt-BR"
        self.assertEqual(
            instanceDIV.humanize(),
            '<div>\n  <p>\n    As cores \n     Blue \n    e\n     Green \n    não são traduzidas.\n  </p>\n</div>'
        )

        # delimiters
        instanceDIV = DIV("{{Change_this}} or not ", "[[change]]")
        self.assertEqual(
            instanceDIV.xml(),
            "<div>{{Change_this}} or not [[change]]</div>"
        )
        instanceDIV.formatter(Change_this="Changed", change="hooooo nooooooo!")
        self.assertEqual(
            instanceDIV.xml(),
            "<div>Changed or not [[change]]</div>"
        )
        self.assertEqual(
            instanceDIV.delimiters,
            ['{{', '}}']
        )
        instanceDIV.delimiters = ["[[", "]]"]
        self.assertEqual(
            instanceDIV.delimiters,
            ['[[', ']]']
        )
        self.assertEqual(
            instanceDIV.xml(),
            "<div>{{Change_this}} or not hooooo nooooooo!</div>"
        )
        # sass_file(), sass, sass_vars and css()
        if os.path.exists("new_sass.sass"):
            os.remove("new_sass.sass")
        self.assertRaises(SyntaxError, lambda: DIV().sass_vars)
        self.assertEqual(
            instanceDIV.sass_file("my_sass.sass", {"COLOR": "orange", "BORDERRADIUS": "100%"}, "new_sass.sass"),
            sample_sass
        )
        with open('new_sass.sass', 'r', encoding='utf-8') as f:
            c = f.read()
            self.assertEqual(
                c,
                sample_sass
            )
        self.assertEqual(
          instanceDIV.sass_vars,
          {'COLOR': 'orange', 'CONTAINERWIDTH': '60px', 'CONTAINERHEIGHT': '60px', 'BORDERRADIUS': '100%'}
        )
        with open('my_sass.sass', 'r', encoding='utf-8') as f:
            c = f.read()
            self.assertEqual(
                c,
                instanceDIV.sass_file("my_sass.sass")
            )
        instanceDIV.sass_vars = {"COLOR": "orange", "BORDERRADIUS": "100%"}
        self.assertEqual(
          instanceDIV.sass,
          sample_sass
        )
        self.assertEqual(
            instanceDIV.css(minify=False),
            sample_css
        )
        # formatter() and formatter_list_keys
        instanceDIV = DIV(
            SPAN(
                "This is value one: {{value-one}}",
                "{this is ignored}"
            ),
            A("{{message_link}}", _href="{{attr_indefined}}"),
            SPAN("I want repeat: {{repeat}} {{repeat}} {{repeat}}.")
        )
        self.assertEqual(
            set(instanceDIV.formatter_list_keys),
            set(['value-one', 'message_link', 'repeat', 'attr_indefined'])
        )
        self.assertEqual(
            instanceDIV.humanize(),
            '<div>\n  <span>\n    This is value one&#58; {{value-one}}\n    {this is ignored}\n  </span>\n  <a href="{{attr_indefined}}">\n    {{message_link}}\n  </a>\n  <span>\n    I want repeat&#58; {{repeat}} {{repeat}} {{repeat}}.\n  </span>\n</div>'
        )
        instanceDIV.formatter({
            "value-one": "1",
            "repeat": "Ha",
            "message_link": "click here!",
            "attr_indefined": "http://localhost",
            "this is ignored": "is it works?"
        })
        SAMPLE_formatter = '<div>\n  <span>\n    This is value one&#58; 1\n    {this is ignored}\n  </span>\n  <a href="http://localhost">\n    click here!\n  </a>\n  <span>\n    I want repeat&#58; Ha Ha Ha.\n  </span>\n</div>'
        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_formatter
        )
        instanceDIV.formatter(
            {"value-one": "1", "this is ignored": "is it works?"},
            repeat="Ha",
            message_link="click here!",
            attr_indefined="http://localhost"
        )
        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_formatter
        )
        instanceDIV.formatter(**{
            "value-one": "1",
            "repeat": "Ha",
            "message_link": "click here!",
            "attr_indefined": "http://localhost",
            "this is ignored": "is it works?"
        })
        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_formatter
        )

        # children_indexes()
        from phanterpwa.helpers import (HTML, HEAD, META, TITLE, BODY, MAIN, XML, FOOTER)
        instanceHTML = HTML(
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
        self.assertEqual(
            instanceHTML.html(minify=False),
            '<html>\n  <head>\n    <meta charset="utf-8">\n    <title>\n      PhanterPWA\n    </title>\n  </head>\n  <body>\n    <main>\n      <strong>xml instance not escape</strong>\n      &lt;strong&gt;this will escape&lt;strong&gt;\n    </main>\n    <footer>\n      PhanterJR\n    </footer>\n  </body>\n</html>'
        )
        self.assertEqual(
            instanceHTML.children_indexes(),
            '[ROOT_PARENT]<html> {}\n    [0]<head> {}\n        [0][0]<meta> {"_charset": "utf-8"}\n        [0][1]<title> {}\n            [0][1][0]"PhanterPWA"\n    [1]<body> {}\n        [1][0]<main> {}\n            [1][0][0]<xml> {}\n                [1][0][0][0]"<strong>xml instance not escape</strong>"\n            [1][0][1]"<strong>this will escape<strong>"\n        [1][1]<footer> {}\n            [1][1][0]"PhanterJR"'
        )

        # source_code()
        XmlConstructor._all_instances = {}
        instanceDIV = DIV(XML("<strong>not escape</strong>"), HR(), SPAN("without xml?", _class="the valid karg"))
        instanceDIV.attributes = {"_invalid-attr-in-karg": "the_key_is_valis_in_html5"}
        self.assertEqual(
            instanceDIV.source_code(),
            sample_test0_source_code00
        )

        self.assertEqual(
            instanceDIV.source_code(add_imports=True, phanterpwa_helpers=True),
            sample_test0_source_code01
        )
        instanceDIV.close_void=True
        self.assertEqual(
            instanceDIV.source_code(add_imports=True, instance_name="MY_INSTANCE"),
            sample_test0_source_code02
        )
        instanceDIV.close_void=False

        # html()
        instanceDIV = DIV(DIV(BR(), HR(), SPAN()), _class="my_class", _underline="_underline", without_underline="without_underline")
        instanceDIV.minify = False
        instanceDIV.indent_size = 4
        instanceDIV.close_void = True
        self.assertEqual(
            instanceDIV.html(),
            '<div class="my_class" underline="_underline"><div><br><hr><span></span></div></div>'
        )
        self.assertEqual(
            instanceDIV.html(False, 8),
            '<div class="my_class" underline="_underline">\n        <div>\n                ' +
                '<br>\n                <hr>\n                <span>\n                ' +
                '</span>\n        </div>\n</div>'
        )
        self.assertEqual(
            instanceDIV.html(minify=False, close_void=True),
            '<div class="my_class" underline="_underline">\n  <div>\n    <br />\n    <hr />\n    ' +
                '<span>\n    </span>\n  </div>\n</div>'
        )
        self.assertEqual(
            instanceDIV.humanize(),
            '<div class="my_class" underline="_underline">\n    <div>\n        <br />\n        ' +
                '<hr />\n        <span>\n        </span>\n    </div>\n</div>'
        )
        instanceDIV.minify = True
        self.assertEqual(
            instanceDIV.xml(),
            '<div class="my_class" underline="_underline"><div><br /><hr /><span></span></div></div>'
        )
        instanceDIV.minify = False
        self.assertEqual(
            instanceDIV.xml(),
            '<div class="my_class" underline="_underline">\n    <div>\n        <br />\n        ' +
                '<hr />\n        <span>\n        </span>\n    </div>\n</div>'
        )
        instanceDIV.minify = True
        instanceDIV.indent_size = 2
        instanceDIV.close_void = False

        # humanize()
        instanceDIV = DIV(DIV(BR(), HR(), SPAN()), _class="my_class", _underline="_underline", without_underline="without_underline")
        self.assertEqual(
            instanceDIV.humanize(),
            '<div class="my_class" underline="_underline">\n  <div>\n    <br>\n    <hr>\n    <span>\n    </span>\n  </div>\n</div>'
        )
        instanceDIV.close_void = True
        self.assertEqual(
            instanceDIV.humanize(),
            '<div class="my_class" underline="_underline">\n  <div>\n    <br />\n    <hr />\n    <span>\n    </span>\n  </div>\n</div>'
        )
        instanceDIV.indent_size = 4
        self.assertEqual(
            instanceDIV.humanize(),
            '<div class="my_class" underline="_underline">\n    <div>\n        <br />\n        <hr />\n        <span>\n        </span>\n    </div>\n</div>'
        )
        instanceDIV.minify = True
        instanceDIV.indent_size = 2
        instanceDIV.close_void = False

        # xml()
        instanceDIV = DIV(DIV(BR(), HR(), SPAN()), _class="my_class", _underline="_underline")
        instanceDIV.indent_size = 4
        instanceDIV.close_void = True
        self.assertEqual(
            instanceDIV.xml(),
            '<div class="my_class" underline="_underline"><div><br /><hr /><span></span></div></div>'
        )
        instanceDIV.minify = False
        self.assertEqual(
            instanceDIV.xml(),
            '<div class="my_class" underline="_underline">\n    <div>\n        <br />\n        <hr />\n        <span>\n        </span>\n    </div>\n</div>'
        )
        instanceDIV.indent_size = 8
        instanceDIV.close_void = False
        self.assertEqual(
            instanceDIV.xml(),
            '<div class="my_class" underline="_underline">\n        <div>\n                <br>\n                <hr>\n                <span>\n                </span>\n        </div>\n</div>'
        )
        instanceDIV.indent_size = 2
        instanceDIV.minify = True

        # json()
        instanceDIV = DIV(DIV("multline\nline01\nline02"), SPAN("it's red", _style="color:red;"), HR())
        self.assertEqual(
            instanceDIV.xml(),
            '<div><div>multline\nline01\nline02</div><span style="color:red;">it&#x27;s red</span><hr></div>'
        )
        self.assertEqual(
            instanceDIV.json(),
            '"<div><div>multline\\nline01\\nline02</div><span style=\\"color:red;\\">it&#x27;s red</span><hr></div>"'
        )
        instanceSCRIPT = SCRIPT(XML('$("#my_id").html(%s);' % instanceDIV.json()))
        self.assertEqual(
            instanceSCRIPT.xml(),
            '<script>$("#my_id").html(\"<div><div>multline\\nline01\\nline02</div><span style=\\"color:red;\\">it&#x27;s red</span><hr></div>\");</script>'
        )

        # search()
        instanceHR = HR(_class="one two")
        id_to_search = instanceHR.id
        sampleSEARCH = HTML(
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
        search = SPAN("long_content")
        result = sampleSEARCH.search(search)
        self.assertEqual(
            str("located %s" % len(result)),
            'located 1'
        )
        self.assertEqual(
            [result[0].xml()],
            ["<span>long_content</span>"]
        )
        search = "long_content"
        result = sampleSEARCH.search(search)
        self.assertEqual(
            str("located %s" % len(result)),
            'located 2'
        )
        self.assertEqual(
            set([x.xml() for x in result]),
            set(['<div class="one" style="color:   white">long_content<span>long_content</span></div>', '<span>long_content</span>'])
        )
        search = "content"
        result = sampleSEARCH.search(search)
        self.assertEqual(
            str("located %s" % len(result)),
            'located 4'
        )
        self.assertEqual(
            set([x.xml() for x in result]),
            set(['<div class="one" style="color:   white">long_content<span>long_content</span></div>', '<span>content<hr class="one two"></span>', '<div class="two" style="color:   white;  display   : none;">content</div>', '<span>long_content</span>'])
        )
        result = sampleSEARCH.search({'_style': "  display:   none;"})
        self.assertEqual(
            str("located %s" % len(result)),
            'located 2'
        )
        self.assertEqual(
            set([x.xml() for x in result]),
            set([
                '<div class="two" style="color:   white;  display   : none;">content</div>',
                '<div style="display:none;"><div class="two" style="color:   white;  display   : none;">content</div><span>content<hr class="one two"></span><hr class="one two"><div class="one" style="color:   white">long_content<span>long_content</span></div></div>'
            ])
        )
        result = sampleSEARCH.search({'_style': "  display:   none;", '_class': 'two'})
        self.assertEqual(
            str("located %s" % len(result)),
            'located 1'
        )
        self.assertEqual(
            set([x.xml() for x in result]),
            set(['<div class="two" style="color:   white;  display   : none;">content</div>'])
        )
        result = sampleSEARCH.search({'_class': 'two'})
        self.assertEqual(
            str("located %s" % len(result)),
            'located 3'
        )
        self.assertEqual(
            set([x.xml() for x in result]),
            set([
                '<hr class="one two">', '<hr class="one two">',
                '<div class="two" style="color:   white;  display   : none;">content</div>'
            ])
        )
        result = sampleSEARCH.search({'_class': 'two one'})
        self.assertEqual(
            str("located %s" % len(result)),
            'located 2'
        )
        self.assertEqual(
            set([x.xml() for x in result]),
            set(['<hr class="one two">', '<hr class="one two">'])
        )
        result = sampleSEARCH.search(id_to_search)
        self.assertEqual(
            str("located %s" % len(result)),
            'located 1'
        )
        self.assertEqual(
            set([x.xml() for x in result]),
            set(['<hr class="one two">'])
        )
        result = sampleSEARCH.search([id_to_search, SPAN("long_content"), "multiple"])
        self.assertEqual(
            str("located %s" % len(result)),
            'located 3'
        )
        self.assertEqual(
            set([x.xml() for x in result]),
            set(['<div>multiple</div>', '<span>long_content</span>', '<hr class="one two">'])
        )

        # i18n
        instanceDIV = DIV(
                "Can I use formatter method? {{response}}",
                P("Monkey", ". Don't have translation this and not has translation of ", "Camel", " in Spanish"),
                P("Do not exist translation"),
                P("Apple", "Orange", "Grape", "Do not have translate"),
                P("The book is on the table", " is ignored")
            )
        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_i18n_method0
        )
        i18nMyInstance = Translator("path_of_languages", debug=True)
        i18nMyInstance.translate("pt-PT", "Orange", "Laranja")
        i18nMyInstance.translate("pt-PT", "Grape", "Uva")
        i18nMyInstance.translate("pt-BR", "Apple", "Maçã")
        i18nMyInstance.translate("pt-BR", "Orange", "Laranja")
        i18nMyInstance.translate("pt-BR", "The book is on the table", "O livro está sobre a mesa")
        i18nMyInstance.translate("pt-BR", "Camel", "Camelo")
        i18nMyInstance.translate("pt-BR", "It is must be ignored", "Isto pode ser ignorado")
        i18nMyInstance.translate("pt-BR", "Can I use formatter method? {{response}}", "Posso usar o método formatter? {{response}}")
        i18nMyInstance.translate("fr", "The book is on the table", "Le livre est sur la table")
        i18nMyInstance.translate("fr", "Monkey", "Singe")
        i18nMyInstance.translate("es", "The book is on the table", "El libro está sobre la mesa")
        i18nMyInstance.translate("es", "Monkey", "Mono")
        instanceDIV.i18n(i18nMyInstance, tag_translation="span", do_not_translate=["It is must be ignored", "The book is on the table"])
        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_i18n_method1
        )
        instanceDIV.i18n(i18nMyInstance, tag_translation="i18n", do_not_translate=["It is must be ignored", "The book is on the table"])
        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_i18n_method2
        )
        instanceDIV.i18n(i18nMyInstance, dictionary="es" , do_not_translate=["It is must be ignored"])
        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_i18n_method3
        )
        instanceDIV.i18n(i18nMyInstance, dictionary="fr" , do_not_translate=["It is must be ignored"])
        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_i18n_method4
        )
        instanceDIV.i18n(i18nMyInstance, dictionary="pt-PT" , do_not_translate=["It is must be ignored"])
        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_i18n_method5
        )
        instanceDIV.i18n(i18nMyInstance, dictionary="pt-BR" , do_not_translate=["It is must be ignored"])
        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_i18n_method6
        )
        instanceDIV.formatter(response="SIM (YES)")
        self.assertEqual(
            instanceDIV.humanize(),
            SAMPLE_i18n_method7
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

        # tagger

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
            ' "a_string", 1, "1", "2", false, true]\' data-obj=\'{"list": ',
            '[null, "a_string", 1, "1", "2", false, true], ',
            '"false": false}\'></div>']))

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
        EVIL = XmlConstructor.tagger('evil', False)
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
        conten_result = set([sample_search[1][0], sample_search[2]])
        self.assertEqual(set(sample_search.search("inside")), conten_result)
        # search by attrs
        element = sample_search[1][0]
        element2 = sample_search[3][0]
        element3 = sample_search[0]
        element4 = sample_search[2]
        element5 = sample_search[3][1]
        self.assertEqual(sample_search.search({"_id": "inside_a"}), [element])
        self.assertEqual(sample_search.search({"_strange_attr": "yes"}), [element2])
        self.assertEqual(set(sample_search.search({"_repeat_attr": "repeat"})), set(repeat_el))
        self.assertEqual([x.xml() for x in sample_search.search("experiment")], [experiment.xml(), experiment.xml()])
        self.assertEqual(set(sample_search.search({"_class": "one"})), set([element3, element4]))
        self.assertEqual(sample_search.search({"_class": "one two"}), [element3])
        self.assertEqual(sample_search.search({"_class": "two one"}), [element3])
        self.assertEqual(set(sample_search.search({"class": "one"})), set([element3, element4]))
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
        sample_i18n.i18n(Trans, 'pt-BR', do_not_translate=[" this is ignored?"])
        self.assertNotEqual(original, sample_i18n)
        self.assertEqual(sample_i18n_entries_to_verbete, sample_i18n.xml())
        sample_i18n.i18n(Trans, 'pt-BR')
        self.assertEqual(sample_i18n_entries_to_verbete_without_ignore, sample_i18n.xml())
        sample_i18n.i18n(Trans, 'en-US', do_not_translate=[" this is ignored?"])
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

    def test14_avanced_content(self):
        Instance = DIV(["This", "is", DIV("content")], {"_class": "testando"})
        Instance2 = DIV(*["This", "is", DIV("content")], **{"_class": "testando"})
        Instance3 = DIV()
        Instance3.content = ["This", "is", DIV("content")]
        Instance3.attributes = {"_class": "testando"}
        self.assertEqual(Instance.xml(), Instance2.xml())
        self.assertEqual(Instance3.xml(), Instance2.xml())



if __name__ == '__main__':
    unittest.main()
