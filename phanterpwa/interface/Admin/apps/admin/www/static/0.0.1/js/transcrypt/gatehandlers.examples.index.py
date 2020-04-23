import phanterpwa.apptools.gatehandler as gatehandler
import phanterpwa.apptools.components.widgets as widgets
import phanterpwa.apptools.helpers as helpers
import plugins.codemirror as codemirror
import phanterpwa.apptools.components.left_bar as left_bar

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


class Index(gatehandler.Handler):
    def initialize(self):
        if self.request.get_arg(0) == "inputs":
            self.inputs = Inputs(self)
        elif self.request.get_arg(0) == "selects":
            self.selects = Selects(self)
        elif self.request.get_arg(0) == "textarea":
            self.selects = Textarea(self)
        else:
            html = CONCATENATE(
                DIV(
                    DIV(
                        DIV(
                            DIV("COMPONENTES", _class="phanterpwa-breadcrumb"),
                            _class="phanterpwa-breadcrumb-wrapper"
                        ),
                        _class="p-container"),
                    _class='title_page_container card'
                ),
                DIV(
                    DIV(
                        DIV(
                            DIV(
                                DIV(
                                    I(
                                        **{
                                            "_class": "fas fa-edit promo-icon",
                                        }
                                    ),
                                    H2("Inputs", _class="promo-title"),
                                    **{
                                        "_class": "link",
                                        "_phanterpwa-way": "examples/inputs"
                                    }
                                ),
                                **{"_class": "promo-container"}
                            ),
                            _class='p-col w1p100 w3p50 w4p25'
                        ),
                        DIV(
                            DIV(
                                DIV(
                                    I(
                                        **{
                                            "_class": "far fa-caret-square-down promo-icon",
                                        }
                                    ),
                                    H2("Selects", _class="promo-title"),
                                    **{
                                        "_class": "link",
                                        "_phanterpwa-way": "examples/selects"
                                    }
                                ),
                                **{"_class": "promo-container"}
                            ),
                            _class='p-col w1p100 w3p50 w4p25'),
                        DIV(
                            DIV(
                                DIV(
                                    I(
                                        **{
                                            "_class": "fas fa-file-signature  promo-icon",
                                        }
                                    ),
                                    H2("Others", _class="promo-title"),
                                    **{
                                        "_class": "link",
                                        "_phanterpwa-way": "examples/textarea"
                                    }
                                ),
                                **{"_class": "promo-container"}
                            ),
                            _class='p-col w1p100 w3p50 w4p25'),
                        DIV(
                            DIV(
                                DIV(
                                    I(
                                        **{
                                            "_class": "fas fa-flag promo-icon",
                                        }
                                    ),
                                    H2("Font Awesome", _class="promo-title"),
                                    **{
                                        "_class": "link",
                                        "_phanterpwa-way": "fontawesome"
                                    }
                                ),
                                **{"_class": "promo-container"}
                            ),
                            _class='p-col w1p100 w3p50 w4p25'),
                        _class='p-row card e-padding_20'
                    ),

                    _class="phanterpwa-container p-container"
                )
            )
            html.html_to("#main-container")
        BackButton1 = left_bar.LeftBarButton(
            "back_home",
            "Voltar",
            I(_class="fas fa-arrow-circle-left"),
            **{"_phanterpwa-way": "home",
                "position": "top",
                "ways": [lambda r: True if r == "examples" else False]}
        )
        BackButton2 = left_bar.LeftBarButton(
            "back_examples",
            "Voltar",
            I(_class="fas fa-arrow-circle-left"),
            **{"_phanterpwa-way": "examples",
                "position": "top",
                "ways": [lambda r: True if r.startswith("examples/") else False]}
        )
        window.PhanterPWA.Components['left_bar'].add_button(BackButton1)
        window.PhanterPWA.Components['left_bar'].add_button(BackButton2)

text1 = """
All objects can be incorporated into Web pages, for this it is only necessary to use the <strong>html_to</strong>, <strong>append_to</strong> or <strong>insert_to</strong> methods, they can also be merged with the html helpers, directly or through variables, below an example of how to use and the necessary imports.
"""
text1_pt_br = """
Todos os objetos podem ser incorporados em páginas da Web, para isto é só usar os métodos <strong>html_to</strong>, <strong>append_to</strong> ou <strong>insert_to</strong>, tambem podem ser mesclados com os helpers html, diretamente ou através de variáveis, abaixo um exemplo de como usar e os imports necessários.
"""
first_example1 = """import phanterpwa.apptools.components.widgets as widgets
import phanterpwa.apptools.helpers as helpers

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

input1_source = """import phanterpwa.apptools.components.widgets as widgets
import phanterpwa.apptools.helpers as helpers

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

input2_source = """import phanterpwa.apptools.components.widgets as widgets
import phanterpwa.apptools.helpers as helpers

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

input3_source = """import phanterpwa.apptools.components.widgets as widgets
import phanterpwa.apptools.helpers as helpers

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
        html = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV("COMPONENTES", _class="phanterpwa-breadcrumb"),
                        DIV("INPUT", _class="phanterpwa-breadcrumb"),
                        _class="phanterpwa-breadcrumb-wrapper"
                    ),
                    _class="p-container"),
                _class='title_page_container card'
            ),
            DIV(
                DIV(
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
                ),
                _class="phanterpwa-container p-container"
            )
        )
        html.html_to("#main-container")


codemirrorselectwearandroid = """
# your code

your_instance = widgets.Select(
    "selectwearandroid",
    label="Label Widget",
    placeholder="Placeholder Widget",
    data_set={
        "banana": "Banana",
        "abacate": "Abacate",
        "doce": "Doce"
    }
),

# your code
"""


codemirrorselectwearshadows = """
# your code

your_instance = widgets.Select(
    "selectwearshadows",
    label="Label Widget",
    placeholder="Placeholder Widget",
    data_set={
        "banana": "Banana",
        "abacate": "Abacate",
        "doce": "Doce"
    },
    wear="shadows"
),

# your code
"""


codemirrorselectwearelegant = """
# your code

your_instance = widgets.Select(
    "selectwearelegant",
    label="Label Widget",
    placeholder="Placeholder Widget",
    data_set={
        "banana": "Banana",
        "abacate": "Abacate",
        "doce": "Doce"
    },
    wear="elegant"
),

# your code
"""


codemirrorsimpleselect = """
# your code

your_instance = widgets.Select(
    "simpleselect",
    label="Label Widget",
    data_set={
        "banana": "banana",
        "abacate": "abacate",
        "doce": "doce"
    }
)

# your code
"""


codemirrorselectcanempty = """
# your code

your_instance = widgets.Select(
    "selectcanempty",
    label="Label Widget",
    can_empty=True,
    data_set={
        "banana": "banana",
        "abacate": "abacate",
        "doce": "doce"
    }
)

# your code
"""


codemirrorselectcanempty = """
# your code

your_instance = widgets.Select(
    "selectcanempty",
    label="Label Widget",
    can_empty=True,
    data_set={
        "banana": "banana",
        "abacate": "abacate",
        "doce": "doce"
    }
)

# your code
"""


codemirrorselectcanemptyplaceholder = """
# your code

your_instance = widgets.Select(
    "selectcanemptyplaceholder",
    label="Label Widget",
    placeholder="Placeholder Widget",
    can_empty=True,
    data_set={
        "banana": "banana",
        "abacate": "abacate",
        "doce": "doce"
    }
)

# your code
"""


codemirrorselectcanemptyeditableplaceholder = """
# your code

your_instance = widgets.Select(
    "selectcanemptyeditableplaceholder",
    label="Label Widget",
    placeholder="Placeholder Widget",
    editable=True,
    can_empty=True,
    data_set={
        "banana": "banana",
        "abacate": "abacate",
        "doce": "doce"
    }
)

# your code
"""


codemirrorselectcanemptyeditable = """
# your code

your_instance = widgets.Select(
    "selectcanemptyeditable",
    label="Label Widget",
    editable=True,
    can_empty=True,
    data_set={
        "banana": "banana",
        "abacate": "abacate",
        "doce": "doce"
    }
)

# your code
"""

multselect1_source = """
# your code

your_instance = widgets.MultSelect(
    "the_multiselect1",
    label="Label Widget",
    placeholder="Placeholder Widget",
    data_set={
        "banana": "Banana",
        "abacate": "Abacate",
        "doce": "Doce"
    },
)

# your code

"""
multselect2_source = """
# your code

your_instance = widgets.MultSelect(
    "the_multiselect2",
    label="Label Widget",
    placeholder="Placeholder Widget",
    editable=True,
    data_set={
        "banana": "Banana",
        "abacate": "Abacate",
        "doce": "Doce"
    },
)

# your code

"""


class Selects():
    def __init__(self, gatehandler):
        self.gatehandler = gatehandler
        html = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV("COMPONENTES", _class="phanterpwa-breadcrumb"),
                        DIV("SELECT", _class="phanterpwa-breadcrumb"),
                        _class="phanterpwa-breadcrumb-wrapper"
                    ),
                    _class="p-container"),
                _class='title_page_container card'
            ),
            DIV(
                DIV(
                    DIV(
                        H2(I18N("Select - Styles (Wear)")),
                        HR(),
                        XSECTION(
                            LABEL(I18N("Example"), ' 01 (wear="android")'),
                            DIV(
                                STRONG(I18N("Code"), ":"),
                                codemirror.CodeMirrorHelper(
                                    "codemirrorselectwearandroid",
                                    **{
                                        "value": codemirrorselectwearandroid,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    widgets.Select(
                                        "selectwearandroid",
                                        label="Label Widget",
                                        placeholder="Placeholder Widget",
                                        data_set={
                                            "banana": "Banana",
                                            "abacate": "Abacate",
                                            "doce": "Doce"
                                        }
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
                                    "codemirrorselectwearshadows",
                                    **{
                                        "value": codemirrorselectwearshadows,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    widgets.Select(
                                        "selectwearshadows",
                                        label="Label Widget",
                                        placeholder="Placeholder Widget",
                                        data_set={
                                            "banana": "Banana",
                                            "abacate": "Abacate",
                                            "doce": "Doce"
                                        },
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
                                    "codemirrorselectwearelegant",
                                    **{
                                        "value": codemirrorselectwearelegant,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    widgets.Select(
                                        "selectwearelegant",
                                        label="Label Widget",
                                        placeholder="Placeholder Widget",
                                        data_set={
                                            "banana": "Banana",
                                            "abacate": "Abacate",
                                            "doce": "Doce"
                                        },
                                        wear="elegant"
                                    ),
                                    _class="widget_input_example"
                                ),
                                _class="e-padding_10"
                            ),
                        ),
                        H2(I18N("Select - Parameters")),
                        HR(),
                        XSECTION(
                            LABEL(I18N("Example"), ' 01'),
                            DIV(
                                STRONG(I18N("Code"), ":"),
                                codemirror.CodeMirrorHelper(
                                    "codemirrorsimpleselect",
                                    **{
                                        "value": codemirrorsimpleselect,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    widgets.Select(
                                        "simpleselect",
                                        label="Label Widget",
                                        data_set={
                                            "banana": "banana",
                                            "abacate": "abacate",
                                            "doce": "doce"
                                        }
                                    ),
                                    _class="widget_input_example"
                                ),
                                _class="e-padding_10"
                            ),
                        ),
                        XSECTION(
                            LABEL(I18N("Example"), ' 02 (can_empty="True")'),
                            DIV(
                                STRONG(I18N("Code"), ":"),
                                codemirror.CodeMirrorHelper(
                                    "codemirrorselectcanempty",
                                    **{
                                        "value": codemirrorselectcanempty,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    widgets.Select(
                                        "selectcanempty",
                                        label="Label Widget",
                                        can_empty=True,
                                        data_set={
                                            "banana": "banana",
                                            "abacate": "abacate",
                                            "doce": "doce"
                                        }
                                    ),
                                    _class="widget_input_example"
                                ),
                                _class="e-padding_10"
                            ),
                        ),
                        XSECTION(
                            LABEL(I18N("Example"), ' 03 (can_empty=True, placeholder="Placeholder Widget")'),
                            DIV(
                                STRONG(I18N("Code"), ":"),
                                codemirror.CodeMirrorHelper(
                                    "codemirrorselectcanemptyplaceholder",
                                    **{
                                        "value": codemirrorselectcanemptyplaceholder,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    widgets.Select(
                                        "selectcanemptyplaceholder",
                                        label="Label Widget",
                                        placeholder="Placeholder Widget",
                                        can_empty=True,
                                        data_set={
                                            "banana": "banana",
                                            "abacate": "abacate",
                                            "doce": "doce"
                                        }
                                    ),
                                    _class="widget_input_example"
                                ),
                                _class="e-padding_10"
                            ),
                        ),
                        XSECTION(
                            LABEL(I18N("Example"), ' 04 (editable=True, can_empty=True)'),
                            DIV(
                                STRONG(I18N("Code"), ":"),
                                codemirror.CodeMirrorHelper(
                                    "codemirrorselectcanemptyeditable",
                                    **{
                                        "value": codemirrorselectcanemptyeditable,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    widgets.Select(
                                        "selectcanemptyeditable",
                                        label="Label Widget",
                                        editable=True,
                                        can_empty=True,
                                        data_set={
                                            "banana": "banana",
                                            "abacate": "abacate",
                                            "doce": "doce"
                                        }
                                    ),
                                    _class="widget_input_example"
                                ),
                                _class="e-padding_10"
                            ),
                        ),
                        XSECTION(
                            LABEL(I18N("Example"),
                                ' 05 (editable=True, can_empty=True, placeholder="Placeholder Widget")'),
                            DIV(
                                STRONG(I18N("Code"), ":"),
                                codemirror.CodeMirrorHelper(
                                    "codemirrorselectcanemptyeditableplaceholder",
                                    **{
                                        "value": codemirrorselectcanemptyeditableplaceholder,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    widgets.Select(
                                        "selectcanemptyeditableplaceholder",
                                        label="Label Widget",
                                        placeholder="Placeholder Widget",
                                        editable=True,
                                        can_empty=True,
                                        data_set={
                                            "banana": "banana",
                                            "abacate": "abacate",
                                            "doce": "doce"
                                        }
                                    ),
                                    _class="widget_input_example"
                                ),
                                _class="e-padding_10"
                            ),
                        ),
                        H2(I18N("MultiSelect")),
                        HR(),
                        XSECTION(
                            LABEL(I18N("Example"), ' 01'),
                            DIV(
                                STRONG(I18N("Code"), ":"),
                                codemirror.CodeMirrorHelper(
                                    "codemirrormultselect1",
                                    **{
                                        "value": multselect1_source,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    widgets.MultSelect(
                                        "the_multiselect1",
                                        label="Label Widget",
                                        placeholder="Placeholder Widget",
                                        data_set={
                                            "banana": "Banana",
                                            "abacate": "Abacate",
                                            "doce": "Doce"
                                        },
                                    ),
                                    _class="widget_input_example"
                                ),
                                _class="e-padding_10"
                            ),
                        ),
                        XSECTION(
                            LABEL(I18N("Example"), ' 02'),
                            DIV(
                                STRONG(I18N("Code"), ":"),
                                codemirror.CodeMirrorHelper(
                                    "codemirrormultselect2",
                                    **{
                                        "value": multselect2_source,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    widgets.MultSelect(
                                        "the_multiselect2",
                                        label="Label Widget",
                                        placeholder="Placeholder Widget",
                                        editable=True,
                                        data_set={
                                            "banana": "Banana",
                                            "abacate": "Abacate",
                                            "doce": "Doce"
                                        },
                                    ),
                                    _class="widget_input_example"
                                ),
                                _class="e-padding_10"
                            ),
                        ),

                        _class="card e-padding_20"
                    ),
                    _class="new-container"
                ),
                _class="phanterpwa-container p-container"
            )
        )
        # jQuery("#main-container").html(html.jquery())
        html.html_to("#main-container")


class Textarea():
    def __init__(self, gatehandler):
        self.gatehandler = gatehandler
        html = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV("COMPONENTES", _class="phanterpwa-breadcrumb"),
                        DIV("TEXTAREA", _class="phanterpwa-breadcrumb"),
                        _class="phanterpwa-breadcrumb-wrapper"
                    ),
                    _class="p-container"),
                _class='title_page_container card'
            ),
            DIV(
                DIV(
                    DIV(
                        H2(I18N("Textboxs")),
                        HR(),
                        XSECTION(
                            LABEL("Type: Password"),
                            DIV(
                                widgets.Textarea(
                                    "textare1",
                                    label="Label Widget",
                                ),
                                _class="component_materialize"
                            ),
                        ),
                        XSECTION(
                            LABEL("Type: Password"),
                            DIV(
                                widgets.Textarea(
                                    "textare2",
                                    label="Label Widget",
                                    wear="shadows"
                                ),
                                _class="component_shadows"
                            ),
                        ),
                        XSECTION(
                            LABEL("Type: Password"),
                            DIV(
                                widgets.Textarea(
                                    "textare3",
                                    label="Label Widget",
                                    wear="elegant"
                                ),
                                _class="component_shadows"
                            ),
                        ),
                        H2(I18N("Dropdown")),
                        HR(),
                        XSECTION(
                            LABEL("Value: True"),
                            DIV(
                                DIV(
                                    DIV(
                                        widgets.MenuBox(
                                            "drop1",
                                            xml_menu=UL(
                                                LI(SPAN("Editar", _class="botao_editar_socio")),
                                                LI(SPAN("Visualizar", _class="botao_visualizar_socio")),
                                                _class='dropdown-content'
                                            )
                                        ),
                                        _class="p-col w1p10"
                                    ),
                                    DIV(
                                        " ",
                                        _class="p-col w1p80"
                                    ),
                                    DIV(
                                        widgets.MenuBox(
                                            "drop2",
                                            xml_menu=UL(
                                                LI(SPAN("Editar", _class="botao_editar_socio")),
                                                LI(SPAN("Visualizar", _class="botao_visualizar_socio")),
                                                _class='dropdown-content'
                                            )
                                        ),
                                        _class="p-col w1p10"
                                    ),
                                    _class="p-row"
                                ),
                                _class="component_materialize"
                            ),
                        ),
                        H2(I18N("Checkbox")),
                        HR(),
                        XSECTION(
                            LABEL("Value: True"),
                            DIV(
                                widgets.CheckBox(
                                    "check1",
                                    value=True,
                                    label="Label Widget",
                                ),
                                _class="component_materialize"
                            ),
                        ),
                        XSECTION(
                            LABEL("Value: False"),
                            DIV(
                                widgets.CheckBox(
                                    "check2",
                                    value=False,
                                    label="Label Widget",
                                ),
                                _class="component_materialize"
                            ),
                        ),
                        XSECTION(
                            LABEL("Value: False"),
                            DIV(
                                widgets.CheckBox(
                                    "check3",
                                    value=False,
                                    label="Label Widget",
                                    wear="elegant"
                                ),
                                _class="component_materialize"
                            ),
                        ),
                        H2(I18N("ListString")),
                        HR(),
                        XSECTION(
                            LABEL("Value: [\"Value01\", \"Value02\", \"Value03\"]"),
                            DIV(
                                widgets.ListString(
                                    "liststring1",
                                    value=["Value01", "Value02", "Value03"],
                                    label="Label Widget",
                                ),
                                _class="component_materialize"
                            ),
                        ),
                        XSECTION(
                            LABEL("data_set: [\"Value04\", \"Value05\"] and editable: False"),
                            DIV(
                                widgets.ListString(
                                    "liststring2",
                                    value=["Value01", "Value02", "Value03"],
                                    label="Label Widget",
                                    data_set=["Value04", "Value05"],
                                    editable=False
                                ),
                                _class="component_materialize"
                            ),
                        ),
                        _class="card e-padding_20"
                    ),
                    _class="new-container"
                ),
                _class="phanterpwa-container p-container"
            )
        )
        jQuery("#main-container").html(html.jquery())


