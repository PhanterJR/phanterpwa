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


codemirrorfirstmenu = """
import phanterpwa.frontend.components.widgets as widgets
import phanterpwa.frontend.helpers as helpers
DIV = helpers.XmlConstructor.tagger("div")

html = DIV(
    widgets.MenuBox(
        "firstmenu",
        I(_class="fas fa-ellipsis-v"),
        DIV("Option1", _class="my_button_one"),
        DIV("Option2", _class="my_button_two")
    )
)

html.html_to("#your_target")
# your code
"""


codemirrormenu2 = """
# your code

your_instance = widgets.MenuBox(
    "firstmenu2",
    "My menu",
    DIV("Option1", _class="my_button_one"),
    DIV("Option2", _class="my_button_two"),
    **{
        "width": 200,
        "onOpen": lambda el: jQuery(el).find(
            ".phanterpwa-widget-menubox-option"
        ).off(
            "click.phanterpwa-awesome-icon",
        ).on(
            "click.phanterpwa-awesome-icon",
            lambda: window.PhanterPWA.flash("I'm clicked!")
        )
    }
)

# your code
"""


codemirrorsidebyside = """
# your code
your_menus = DIV(
    DIV(
        widgets.MenuBox(
            "sideleft",
            I(_class="fas fa-ellipsis-v"),
            DIV("Option1", _class="my_button_one"),
            DIV("Option2", _class="my_button_two")
        ),
        _class="p-col w1p10"
    ),
    DIV(
        " ",
        _class="p-col w1p80"
    ),
    DIV(
        widgets.MenuBox(
            "sideright",
            I(_class="fas fa-ellipsis-v"),
            DIV("Option1", _class="my_button_one"),
            DIV("Option2", _class="my_button_two")
        ),
        _class="p-col w1p10"
    ),
    _class="p-row"
)

# your code
"""


class MenuBox():
    def __init__(self, gatehandler):
        self.gatehandler = gatehandler
        html = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV("COMPONENTES", _class="phanterpwa-breadcrumb"),
                        DIV("MENUS", _class="phanterpwa-breadcrumb"),
                        _class="phanterpwa-breadcrumb-wrapper"
                    ),
                    _class="p-container"),
                _class='title_page_container card'
            ),
            DIV(
                DIV(
                    DIV(
                        H2(I18N("MenuBox")),
                        HR(),
                        XSECTION(
                            LABEL(I18N("Example"), ' 01'),
                            DIV(
                                STRONG(I18N("Code"), ":"),
                                codemirror.CodeMirrorHelper(
                                    "codemirrorfirstmenu",
                                    **{
                                        "value": codemirrorfirstmenu,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    widgets.MenuBox(
                                        "firstmenu",
                                        I(_class="fas fa-ellipsis-v"),
                                        DIV("Option1", _class="my_button_one"),
                                        DIV("Option2", _class="my_button_two")
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
                                    "codemirrormenu2",
                                    **{
                                        "value": codemirrormenu2,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    widgets.MenuBox(
                                        "firstmenu2",
                                        "My menu",
                                        DIV("Option1", _class="my_button_one"),
                                        DIV("Option2", _class="my_button_two"),
                                        **{
                                            "width": 200,
                                            "onOpen": lambda el: jQuery(el).find(
                                                ".phanterpwa-widget-menubox-option"
                                            ).off(
                                                "click.phanterpwa-awesome-icon",
                                            ).on(
                                                "click.phanterpwa-awesome-icon",
                                                lambda: window.PhanterPWA.flash("I'm clicked!")
                                            )
                                        }
                                    ),
                                    _class="widget_input_example"
                                ),
                                _class="e-padding_10"
                            ),
                        ),
                        XSECTION(
                            LABEL(I18N("Example"), ' 01 (wear="android")'),
                            DIV(
                                STRONG(I18N("Code"), ":"),
                                codemirror.CodeMirrorHelper(
                                    "codemirrorsidebyside",
                                    **{
                                        "value": codemirrorsidebyside,
                                        "mode": "python",
                                        "lineNumbers": True
                                    }
                                ),
                                STRONG(I18N("Results"), ":"),
                                DIV(
                                    DIV(
                                        DIV(
                                            widgets.MenuBox(
                                                "sideleft",
                                                I(_class="fas fa-ellipsis-v"),
                                                DIV("Option1", _class="my_button_one"),
                                                DIV("Option2", _class="my_button_two")
                                            ),
                                            _class="p-col w1p10"
                                        ),
                                        DIV(
                                            " ",
                                            _class="p-col w1p80"
                                        ),
                                        DIV(
                                            widgets.MenuBox(
                                                "sideright",
                                                I(_class="fas fa-ellipsis-v"),
                                                DIV("Option1", _class="my_button_one"),
                                                DIV("Option2", _class="my_button_two")
                                            ),
                                            _class="p-col w1p10"
                                        ),
                                        _class="p-row"
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
