import phanterpwa.frontend.components.widgets as widgets
import phanterpwa.frontend.helpers as helpers
import plugins.codemirror as codemirror
from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = M = js_undefined = window =\
    __new__ = FormData = console = localStorage = document = this = 0
__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")
LABEL = helpers.XmlConstructor.tagger("label")
I = helpers.XmlConstructor.tagger("i")
H2 = helpers.XmlConstructor.tagger("h2")
FORM = helpers.XmlConstructor.tagger("form")
SPAN = helpers.XmlConstructor.tagger("span")
IMG = helpers.XmlConstructor.tagger("img", True)
HR = helpers.XmlConstructor.tagger("hr", True)
UL = helpers.XmlConstructor.tagger("ul")
STRONG = helpers.XmlConstructor.tagger("strong")
LI = helpers.XmlConstructor.tagger("li")
INPUT = helpers.XmlConstructor.tagger("input", True)
BR = helpers.XmlConstructor.tagger("br", True)
P = helpers.XmlConstructor.tagger("p")
A = helpers.XmlConstructor.tagger("a")
I18N = helpers.I18N
CONCATENATE = helpers.CONCATENATE
XML = helpers.XML
XSECTION = helpers.XSECTION



text1 = """
All objects can be incorporated into Web pages, for this it is only necessary to use the <strong>html_to</strong>, <strong>append_to</strong> or <strong>insert_to</strong> methods, they can also be merged with the html helpers, directly or through variables, below an example of how to use and the necessary imports.
"""
text1_pt_br = """
Todos os objetos podem ser incorporados em páginas da Web, para isto é só usar os métodos <strong>html_to</strong>, <strong>append_to</strong> ou <strong>insert_to</strong>, tambem podem ser mesclados com os helpers html, diretamente ou através de variáveis, abaixo um exemplo de como usar e os imports necessários.
"""
first_example1 = """import phanterpwa.frontend.components.widgets as widgets
import phanterpwa.frontend.helpers as helpers

DIV = helpers.XmlConstructor.tagger("div")

helper_instance = DIV(
    widgets.Input(
        "android",
        label="Label Widget",
        placeholder="Placeholder Widget",
    ),
    _class="widget_input_example"
)
helper_instance.html_to("#your-container")

new_widget_instance = widgets.Input(
    "other_identifier",
    label="Label Widget"
)
new_widget_instance.append_to("#your-container")

using_jquery = widgets.Input(
    "other_identifier",
    label="Label Widget"
)

element_jquery = using_jquery.jquery()
jQuery("#your-container").append(element_jquery)

"""

input1_source = """import phanterpwa.frontend.components.widgets as widgets
import phanterpwa.frontend.helpers as helpers

DIV = helpers.XmlConstructor.tagger("div")

helper_instance = DIV(
    widgets.Input(
        "android",
        label="Label Widget",
        placeholder="Placeholder Widget",
    ),
    _class="widget_input_example"
)
helper_instance.html_to("#your-container")
"""

input2_source = """import phanterpwa.frontend.components.widgets as widgets
import phanterpwa.frontend.helpers as helpers

DIV = helpers.XmlConstructor.tagger("div")

helper_instance = DIV(
    widgets.Input(
        "shadows",
        label="Label Widget",
        placeholder="Placeholder Widget",
        wear="shadows"
    ),
    _class="widget_input_example"
)
helper_instance.html_to("#your-container")
"""

input3_source = """import phanterpwa.frontend.components.widgets as widgets
import phanterpwa.frontend.helpers as helpers

DIV = helpers.XmlConstructor.tagger("div")

helper_instance = DIV(
    widgets.Input(
        "elegant",
        label="Label Widget",
        placeholder="Placeholder Widget",
        wear="elegant"
    ),
    _class="widget_input_example"
)
helper_instance.html_to("#your-container")
"""

input4_source = """
# your imports
# your code

your_instance = widgets.Input(
    "password",
    label="Label Widget",
    placeholder="Placeholder Widget",
    kind="password"
)

# your code
"""

input5_source = """
# your code

your_instance = widgets.Input(
    "date",
    label="Label Widget",
    placeholder="Placeholder Widget",
    kind="date"
)

# your code
"""

input6_source = """
# your code

your_instance = widgets.Input(
    "datetime",
    label="Label Widget",
    value="2020-02-02 03:12:33",
    placeholder="Placeholder Widget",
    kind="datetime"
)

# your code
"""

input7_source = """
# your code

your_instance = widgets.Input(
    "datetime2",
    label="Label Widget",
    value="02/02/2020 03:12:33",
    placeholder="Placeholder Widget",
    kind="datetime",
    format="dd/MM/yyyy HH:mm:ss"
)

# your code
"""

input8_source = """
# your code

your_instance = widgets.Input(
    "iconify",
    label="Label Widget",
    placeholder="Placeholder Widget",
    icon=I(_class="fab fa-sistrix"),
    icon_on_click=lambda: window.PhanterPWA.flash(**{"html": I18N("Fui Clicado!")})
)

# your code
"""
input_8_source = """
# your code

your_instance = widgets.Input(
    "iconify_password",
    label="Label Widget",
    value="password",
    kind="password",
    placeholder="Placeholder Widget",
    icon=I(_class="fab fa-sistrix")
)

# your code
"""
input9_source = """
# your code

your_instance = widgets.Input(
    "iconify_datetime",
    label="Label Widget",
    placeholder="Placeholder Widget",
    kind="datetime",
    icon=I(_class="far fa-calendar-alt")
)

# your code
"""

input10_source = """
# your code

your_instance = widgets.Input(
    "iconify_date",
    label="Label Widget",
    placeholder="Placeholder Widget",
    kind="date",
    icon=I(_class="far fa-calendar-alt"),
    format="dd/MM/yyyy"
)

# your code
"""


class Inputs():
    def __init__(self, gatehandler):
        self.gatehandler = gatehandler
        gatehandler.Inputs = self
        html = DIV(
            DIV(
                P(I18N(text1, **{"_pt-BR": text1_pt_br, "sanitize": False})),

                H2(I18N("Styles (waer)")),
                HR(),
                XSECTION(
                    LABEL(I18N("Example"), ' 01 (wear="android")'),
                    DIV(
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirror1",
                            **{
                                "value": input1_source,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Input(
                                "android",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                            ),
                            _class="widget_input_example"
                        ),
                        _class="e-padding_10"
                    ),
                ),
                XSECTION(
                    LABEL(I18N("Example"), ' 02 (wear="shadows")'),
                    DIV(
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirror2",
                            **{
                                "value": input2_source,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Input(
                                "shadows",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                wear="shadows"
                            ),
                            _class="widget_input_example"
                        ),
                        _class="e-padding_10"
                    ),
                ),
                XSECTION(
                    LABEL(I18N("Example"), ' 03 (wear="elegant")'),
                    DIV(
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirror3",
                            **{
                                "value": input3_source,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Input(
                                "elegant",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                wear="elegant"
                            ),
                            _class="widget_input_example"
                        ),
                        _class="e-padding_10"
                    ),
                ),
                H2(I18N("Types (kind)")),
                HR(),
                XSECTION(
                    LABEL(I18N("Example"), ' 01 (kind="password")'),
                    DIV(
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirror4",
                            **{
                                "value": input4_source,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Input(
                                "password",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                kind="password"
                            ),
                            _class="widget_input_example"
                        ),
                        _class="e-padding_10"
                    ),
                ),
                XSECTION(
                    LABEL(I18N("Example"), ' 02 (kind="date")'),
                    DIV(
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirror5",
                            **{
                                "value": input5_source,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Input(
                                "date",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                kind="date"
                            ),
                            _class="widget_input_example"
                        ),
                        _class="e-padding_10"
                    ),
                ),
                XSECTION(
                    LABEL(I18N("Example"), ' 03 (kind="datetime")'),
                    DIV(
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirror6",
                            **{
                                "value": input6_source,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Input(
                                "datetime",
                                label="Label Widget",
                                value="2020-02-02 03:12:33",
                                placeholder="Placeholder Widget",
                                kind="datetime"
                            ),
                            _class="widget_input_example"
                        ),
                        BR(),
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirror7",
                            **{
                                "value": input7_source,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ' (format="dd/MM/yyyy HH:mm:ss"):'),
                        DIV(
                            widgets.Input(
                                "datetime2",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                kind="datetime",
                                value="02/02/2020 03:12:33",
                                format="dd/MM/yyyy HH:mm:ss"
                            ),
                            _class="widget_input_example"
                        ),
                        _class="e-padding_10"
                    ),
                ),
                H2(I18N("Iconify (icon)")),
                HR(),
                XSECTION(
                    LABEL(I18N("Example"), ' 01 (icon=I(_class="fab fa-sistrix"))'),

                    DIV(
                        widgets.Input(
                            "iconify",
                            label="Label Widget",
                            placeholder="Placeholder Widget",
                            icon=I(_class="fab fa-sistrix"),
                            icon_on_click=lambda: window.PhanterPWA.flash(**{"html": I18N("Fui Clicado!")})
                        ),
                        _class="widget_input_example"
                    ),
                    codemirror.CodeMirrorHelper(
                        "codemirror8",
                        **{
                            "value": input8_source,
                            "mode": "python",
                            "lineNumbers": True
                        }
                    ),
                ),
                XSECTION(
                    LABEL(I18N("Example"), ' 02 (kind="password", icon=I(_class="fas fa-eye"))'),

                    DIV(
                        widgets.Input(
                            "iconify_password",
                            label="Label Widget",
                            value="password",
                            placeholder="Placeholder Widget",
                            kind="password",
                            icon=I(_class="fas fa-eye")
                        ),
                        _class="widget_input_example"
                    ),
                    codemirror.CodeMirrorHelper(
                        "codemirror_8",
                        **{
                            "value": input_8_source,
                            "mode": "python",
                            "lineNumbers": True
                        }
                    ),
                ),
                XSECTION(
                    LABEL(I18N("Example"), ' 03 (I(_class="far fa-calendar-alt") e kind="datetime"))'),
                    P(
                        I18N(
                            "Neste exemplo adicionamos um ícone de calendário, observe que o parâmatro kind é datetime e não iremos adicionar uma ação ao botão, clique e veja o que acontece."
                        )
                    ),
                    DIV(
                        widgets.Input(
                            "iconify_datetime",
                            label="Label Widget",
                            placeholder="Placeholder Widget",
                            kind="datetime",
                            icon=I(_class="far fa-calendar-alt")
                        ),
                        _class="widget_input_example"
                    ),
                    codemirror.CodeMirrorHelper(
                        "codemirror9",
                        **{
                            "value": input9_source,
                            "mode": "python",
                            "lineNumbers": True
                        }
                    ),
                ),
                XSECTION(
                    LABEL(I18N("Example"), ' 04 (I(_class="far fa-calendar-alt"), kind="date") e format="dd/MM/yyyy")'),
                    P(
                        I18N(
                            "Como você pode observar, com o kind='date', 'icon' definido e sem uma ação para o icon automaticamente foi utilizado o datetimepicker, agora vamos tentar com o date colocando format='dd/MM/yyyy'."
                        )
                    ),
                    DIV(
                        widgets.Input(
                            "iconify_date",
                            label="Label Widget",
                            placeholder="Placeholder Widget",
                            kind="date",
                            icon=I(_class="far fa-calendar-alt"),
                            format="dd/MM/yyyy",
                            value="01/03/1980"
                        ),
                        _class="widget_input_example"
                    ),
                    codemirror.CodeMirrorHelper(
                        "codemirror10",
                        **{
                            "value": input10_source,
                            "mode": "python",
                            "lineNumbers": True
                        }
                    ),
                ),
                _class="card e-padding_20"
            ),
            _class="new-container"
        )
        html.html_to("#input-container-example")
