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
H3 = helpers.XmlConstructor.tagger("h3")
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


codemirrorselectwearandroidnolabel = """
# your code

your_instance = widgets.Select(
    "selectwearandroidnolabel",
    placeholder="Placeholder Widget",
    data_set={
        "banana": "Banana",
        "abacate": "Abacate",
        "doce": "Doce"
    }
),

# your code
"""


codemirrorselectwearshadowsnolabel = """
# your code

your_instance = widgets.Select(
    "selectwearshadowsnolabel",
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


codemirrorselectwearelegantnolabel = """
# your code

your_instance = widgets.Select(
    "selectwearelegantnolabel",
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


codemirrorselectwearandroidicon = """
# your code

your_instance = widgets.Select(
    "selectwearandroidicon",
    label="Label Widget",
    placeholder="Placeholder Widget",
    icon=I(_class="fab fa-telegram-plane"),
    data_set={
        "banana": "Banana",
        "abacate": "Abacate",
        "doce": "Doce"
    }
),

# your code
"""


codemirrorselectwearshadowsicon = """
# your code

your_instance = widgets.Select(
    "selectwearshadowsicon",
    label="Label Widget",
    placeholder="Placeholder Widget",
    icon=I(_class="fab fa-telegram-plane"), 
    data_set={
        "banana": "Banana",
        "abacate": "Abacate",
        "doce": "Doce"
    },
    wear="shadows"
),

# your code
"""


codemirrorselectweareleganticon = """
# your code

your_instance = widgets.Select(
    "selectweareleganticon",
    label="Label Widget",
    placeholder="Placeholder Widget",
    icon=I(_class="fab fa-telegram-plane"), 
    data_set={
        "banana": "Banana",
        "abacate": "Abacate",
        "doce": "Doce"
    },
    wear="elegant"
),

# your code
"""


codemirrorselectwearandroidiconnolabel = """
# your code

your_instance = widgets.Select(
    "selectwearandroidiconnolabel",
    placeholder="Placeholder Widget",
    icon=I(_class="fab fa-telegram-plane"),
    data_set={
        "banana": "Banana",
        "abacate": "Abacate",
        "doce": "Doce"
    }
),

# your code
"""


codemirrorselectwearshadowsiconnolabel = """
# your code

your_instance = widgets.Select(
    "selectwearshadowsiconnolabel",
    placeholder="Placeholder Widget",
    icon=I(_class="fab fa-telegram-plane"),
    data_set={
        "banana": "Banana",
        "abacate": "Abacate",
        "doce": "Doce"
    },
    wear="shadows"
),

# your code
"""


codemirrorselectweareleganticonnolabel = """
# your code

your_instance = widgets.Select(
    "selectweareleganticonnolabel",
    placeholder="Placeholder Widget",
    icon=I(_class="fab fa-telegram-plane"),
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

cod_mult_sec_styles = """
import phanterpwa.frontend.components.widgets as widgets
import phanterpwa.frontend.helpers as helpers

CONCATENATE = helpers.CONCATENATE
DIV = helpers.XmlConstructor.tagger("div")
H3 = helpers.XmlConstructor.tagger("h3")

your_instance = CONTATENATE(
    H3("Style android"),
    DIV(
        widgets.MultSelect(
            "the_multiselect1stylesnolabelnoplaceholder",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
        ),
        widgets.MultSelect(
            "the_multiselect1stylesnolabelnoplaceh",
            placeholder="Placeholder Widget",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
        ),
        widgets.MultSelect(
            "the_multiselect1styles",
            label="Label Widget",
            placeholder="Placeholder Widget",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
        ),
        widgets.MultSelect(
            "the_multiselect1stylesnolabelicon",
            placeholder="Placeholder Widget",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
            icon=I(_class="fab fa-telegram-plane")
        ),
        widgets.MultSelect(
            "the_multiselect1stylesicon",
            label="Label Widget",
            placeholder="Placeholder Widget",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
            icon=I(_class="fab fa-telegram-plane")
        ),
        _class="widget_input_example"
    ),
    H3("Style shadows"),
    DIV(
        widgets.MultSelect(
            "the_multiselect1stylesshadowsnolabelnoplaceholder",
            wear="shadows",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
        ),
        widgets.MultSelect(
            "the_multiselect1stylesshadowsnolabelnoplaceh",
            placeholder="Placeholder Widget",
            wear="shadows",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
        ),
        widgets.MultSelect(
            "the_multiselect1stylesshadows",
            label="Label Widget",
            placeholder="Placeholder Widget",
            wear="shadows",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
        ),
        widgets.MultSelect(
            "the_multiselect1stylesshadowsnolabelicon",
            placeholder="Placeholder Widget",
            wear="shadows",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
            icon=I(_class="fab fa-telegram-plane")
        ),
        widgets.MultSelect(
            "the_multiselect1stylesshadowsicon",
            label="Label Widget",
            placeholder="Placeholder Widget",
            wear="shadows",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
            icon=I(_class="fab fa-telegram-plane")
        ),
        _class="widget_input_example"
    ),
    H3("Style elegant"),
    DIV(
        widgets.MultSelect(
            "the_multiselect1elegantnolabelnoplaceholder",
            wear="elegant",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
        ),
        widgets.MultSelect(
            "the_multiselect1elegantnolabelnoplaceh",
            placeholder="Placeholder Widget",
            wear="elegant",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
        ),
        widgets.MultSelect(
            "the_multiselect1elegant",
            label="Label Widget",
            placeholder="Placeholder Widget",
            wear="elegant",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
        ),
        widgets.MultSelect(
            "the_multiselect1elegantnolabelicon",
            placeholder="Placeholder Widget",
            wear="elegant",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
            icon=I(_class="fab fa-telegram-plane")
        ),
        widgets.MultSelect(
            "the_multiselect1eleganticon",
            label="Label Widget",
            placeholder="Placeholder Widget",
            wear="elegant",
            data_set={
                "banana": "Banana",
                "abacate": "Abacate",
                "doce": "Doce"
            },
            icon=I(_class="fab fa-telegram-plane")
        ),
        _class="widget_input_example"
    ),
)
"""


class Selects():
    def __init__(self, gatehandler):
        self.gatehandler = gatehandler
        gatehandler.Selects = self
        html = DIV(
            DIV(
                H2(I18N("Select - Styles (Wear)")),
                HR(),
                XSECTION(
                    LABEL(I18N("Examples"), ' 01 (wear, label, icon)'),
                    DIV(
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirrorselectwearandroidnolabel",
                            **{
                                "value": codemirrorselectwearandroidnolabel,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Select(
                                "selectwearandroidnolabel",
                                placeholder="Placeholder Widget",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                }
                            ),
                            _class="widget_input_example"
                        ),
                        BR(),
                        H3("Label example"),
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
                        BR(),
                        H3("Icon examples"),
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirrorselectwearandroidiconnolabel",
                            **{
                                "value": codemirrorselectwearandroidiconnolabel,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Select(
                                "selectwearandroidiconnolabel",
                                placeholder="Placeholder Widget",
                                icon=I(_class="fab fa-telegram-plane"),
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                }
                            ),
                            _class="widget_input_example"
                        ),
                        BR(),
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirrorselectwearandroidicon",
                            **{
                                "value": codemirrorselectwearandroidicon,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Select(
                                "selectwearandroidicon",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                icon=I(_class="fab fa-telegram-plane"),
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
                            "codemirrorselectwearshadowsnolabel",
                            **{
                                "value": codemirrorselectwearshadowsnolabel,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Select(
                                "selectwearshadowsnolabel",
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
                        BR(),
                        H3("Label Example"),
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
                        BR(),
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirrorselectwearshadowsiconnolabel",
                            **{
                                "value": codemirrorselectwearshadowsiconnolabel,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Select(
                                "selectwearshadowsiconnolabel",
                                placeholder="Placeholder Widget",
                                icon=I(_class="fab fa-telegram-plane"),
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                                wear="shadows"
                            ),
                            _class="widget_input_example"
                        ),
                        BR(),
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirrorselectwearshadowsicon",
                            **{
                                "value": codemirrorselectwearshadowsicon,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Select(
                                "selectwearshadowsicon",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                icon=I(_class="fab fa-telegram-plane"),
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
                            "codemirrorselectwearelegantnolabel",
                            **{
                                "value": codemirrorselectwearelegantnolabel,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Select(
                                "selectwearelegantnolabel",
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
                        BR(),
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
                        BR(),
                        H3("Icon examples"),
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirrorselectweareleganticonnolabel",
                            **{
                                "value": codemirrorselectweareleganticonnolabel,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Select(
                                "selectweareleganticonnolabel",
                                placeholder="Placeholder Widget",
                                icon=I(_class="fab fa-telegram-plane"),
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                                wear="elegant"
                            ),
                            _class="widget_input_example"
                        ),
                        H3("Icon example"),
                        STRONG(I18N("Code"), ":"),
                        codemirror.CodeMirrorHelper(
                            "codemirrorselectweareleganticon",
                            **{
                                "value": codemirrorselectweareleganticon,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        DIV(
                            widgets.Select(
                                "selectweareleganticon",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                icon=I(_class="fab fa-telegram-plane"),
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
                            "cod_mult_sec_styles",
                            **{
                                "value": cod_mult_sec_styles,
                                "mode": "python",
                                "lineNumbers": True
                            }
                        ),
                        STRONG(I18N("Results"), ":"),
                        H3("Style android"),
                        DIV(
                            widgets.MultSelect(
                                "the_multiselect1stylesnolabelnoplaceholder",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                            ),
                            widgets.MultSelect(
                                "the_multiselect1stylesnolabelnoplaceh",
                                placeholder="Placeholder Widget",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                            ),
                            widgets.MultSelect(
                                "the_multiselect1styles",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                            ),
                            widgets.MultSelect(
                                "the_multiselect1stylesnolabelicon",
                                placeholder="Placeholder Widget",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                                icon=I(_class="fab fa-telegram-plane")
                            ),
                            widgets.MultSelect(
                                "the_multiselect1stylesicon",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                                icon=I(_class="fab fa-telegram-plane")
                            ),
                            _class="widget_input_example"
                        ),
                        H3("Style shadows"),
                        DIV(
                            widgets.MultSelect(
                                "the_multiselect1stylesshadowsnolabelnoplaceholder",
                                wear="shadows",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                            ),
                            widgets.MultSelect(
                                "the_multiselect1stylesshadowsnolabelnoplaceh",
                                wear="shadows",
                                placeholder="Placeholder Widget",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                            ),
                            widgets.MultSelect(
                                "the_multiselect1stylesshadows",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                wear="shadows",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                            ),
                            widgets.MultSelect(
                                "the_multiselect1stylesshadowsnolabelicon",
                                placeholder="Placeholder Widget",
                                wear="shadows",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                                icon=I(_class="fab fa-telegram-plane")
                            ),
                            widgets.MultSelect(
                                "the_multiselect1stylesshadowsicon",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                wear="shadows",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                                icon=I(_class="fab fa-telegram-plane")
                            ),
                            _class="widget_input_example"
                        ),
                        H3("Style elegant"),
                        DIV(
                            widgets.MultSelect(
                                "the_multiselect1elegantnolabelnoplaceholder",
                                wear="elegant",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                            ),
                            widgets.MultSelect(
                                "the_multiselect1elegantnolabelnoplaceh",
                                placeholder="Placeholder Widget",
                                wear="elegant",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                            ),
                            widgets.MultSelect(
                                "the_multiselect1elegant",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                wear="elegant",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                            ),
                            widgets.MultSelect(
                                "the_multiselect1elegantnolabelicon",
                                placeholder="Placeholder Widget",
                                wear="elegant",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                                icon=I(_class="fab fa-telegram-plane")
                            ),
                            widgets.MultSelect(
                                "the_multiselect1eleganticon",
                                label="Label Widget",
                                placeholder="Placeholder Widget",
                                wear="elegant",
                                data_set={
                                    "banana": "Banana",
                                    "abacate": "Abacate",
                                    "doce": "Doce"
                                },
                                icon=I(_class="fab fa-telegram-plane")
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
                    LABEL(I18N("Example"), ' 03'),
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
        )
        # jQuery("#main-container").html(html.jquery())
        html.html_to("#selects-container-example")
