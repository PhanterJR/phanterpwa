import phanterpwa.frontend.gatehandler as gatehandler
import phanterpwa.frontend.components.widgets as widgets
import phanterpwa.frontend.helpers as helpers
import plugins.codemirror as codemirror
import phanterpwa.frontend.components.left_bar as left_bar
import gatehandlers.ext_examples.inputs as inputs
import gatehandlers.ext_examples.selects as selects
import gatehandlers.ext_examples.menus as menus

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
                            DIV(
                                widgets.Preloaders("preload_android"),
                                _style="width:100%; text-align: center; padding-top: 100px; padding-bottom: 100px;"
                            ),
                            _id="projects_container"),
                        _class="card p-row e-padding_10"
                    ),
                    _id="input-container-example",
                    _class="phanterpwa-container p-container"
                )
            )
            html.html_to("#main-container")
            setTimeout(lambda: inputs.Inputs(self), 30)
        elif self.request.get_arg(0) == "selects":
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
                            DIV(
                                widgets.Preloaders("preload_android"),
                                _style="width:100%; text-align: center; padding-top: 100px; padding-bottom: 100px;"
                            ),
                            _id="projects_container"),
                        _class="card p-row e-padding_10"
                    ),
                    _id="selects-container-example",
                    _class="phanterpwa-container p-container"
                )
            )
            html.html_to("#main-container")
            setTimeout(lambda: selects.Selects(self), 30)
        elif self.request.get_arg(0) == "menus":
            self.menus = menus.MenuBox(self)
        elif self.request.get_arg(0) == "others":
            self.others = Others(self)
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
                                            "_class": "fas fa-ellipsis-v  promo-icon",
                                        }
                                    ),
                                    H2("Menus", _class="promo-title"),
                                    **{
                                        "_class": "link",
                                        "_phanterpwa-way": "examples/menus"
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
                                        "_phanterpwa-way": "examples/others"
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



class Others():
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
                        H2(I18N("Radiobox")),
                        HR(),
                        XSECTION(
                            LABEL("Value: True"),
                            DIV(
                                widgets.RadioBox(
                                    "radio1",
                                    value=True,
                                    label="Label Widget",
                                ),
                                _class="component_materialize"
                            ),
                        ),
                        XSECTION(
                            LABEL("Value: False"),
                            DIV(
                                widgets.RadioBox(
                                    "radio2",
                                    value=False,
                                    label="Label Widget",
                                ),
                                _class="component_materialize"
                            ),
                        ),
                        XSECTION(
                            LABEL("Value: False"),
                            DIV(
                                widgets.RadioBox(
                                    "radio4",
                                    value=False,
                                    label="Label Widget",
                                    name="my_radio"
                                ),
                                widgets.RadioBox(
                                    "radio5",
                                    value=False,
                                    label="Label Widget",
                                    name="my_radio"
                                ),
                                widgets.RadioBox(
                                    "radio6",
                                    value=False,
                                    label="Label Widget",
                                    name="my_radio"
                                ),
                                widgets.RadioBox(
                                    "radio7",
                                    value=False,
                                    label="Label Widget",
                                    name="my_radio"
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


