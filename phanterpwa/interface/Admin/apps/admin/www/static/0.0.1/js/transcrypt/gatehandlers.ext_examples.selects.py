import phanterpwa.apptools.components.widgets as widgets
import phanterpwa.apptools.helpers as helpers
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
