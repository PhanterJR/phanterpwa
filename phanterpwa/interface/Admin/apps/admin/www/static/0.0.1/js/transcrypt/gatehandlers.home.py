import phanterpwa.apptools.gatehandler as gatehandler
import phanterpwa.apptools.helpers as helpers
import phanterpwa.apptools.components.left_bar as left_bar
import phanterpwa.apptools.components.snippets as snippets
from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = window = 0
__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")
I = helpers.XmlConstructor.tagger("i")
H1 = helpers.XmlConstructor.tagger("h1")
H2 = helpers.XmlConstructor.tagger("h2")
H3 = helpers.XmlConstructor.tagger("h3")
A = helpers.XmlConstructor.tagger("a")
I18N = helpers.I18N
__pragma__('kwargs')


class Index(gatehandler.Handler):
    def initialize(self):
        html = DIV(
            snippets.Centralizer(
                "phanterpwa-logo-wrapper",
                DIV(_class="phanterpwa-background-logo"),
                H1("PhanterPWA", _class="phanterpwa-the_title"),
                H3(
                    I18N(
                        "Full-Stack Progressive Web Applications framework written and programmable with Python.",

                    ),
                    _class="phanterpwa-the_subtitle"
                )
            )
        )
        html.html_to("#main-container")
        window.PhanterPWA.LOAD(**{
            "args": ["loads", "phanterpwa_logo.html"],
            "onComplete": self._after_load
        })
        AdminButton = left_bar.LeftBarButton(
            "phanterpwa-developer-button",
            "Development",
            I(_class="fas fa-users-cog"),
            **{
                "_phanterpwa-way": "developer",
                "position": "top",
                "ways": ["home"]
            }
        )
        teste = left_bar.LeftBarButton(
            "phanterpwa-components-button",
            "Components",
            I(_class="fas fa-code"),
            **{
                "_phanterpwa-way": "examples",
                "position": "top",
                "ways": ["home"]
            }
        )

        window.PhanterPWA.Components['left_bar'].add_button(AdminButton)
        window.PhanterPWA.Components['left_bar'].add_button(teste)

    def _after_load(self, data):
        xml = jQuery(
                "#phanterpwa-snippet-phanterpwa-logo-wrapper")
        xml.find(".phanterpwa-background-logo").html(data)
        xml.height(jQuery(window).height() - 60).css("width", "100%")
        jQuery(window).resize(lambda: xml.height(jQuery(window).height() - 60).css("width", "100%"))

__pragma__('nokwargs')
