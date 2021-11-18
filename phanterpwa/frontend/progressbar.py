from org.transcrypt.stubs.browser import __pragma__
from phanterpwa.frontend import helpers
__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = String = setTimeout = Date = RegExp = \
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')


DIV = helpers.XmlConstructor.tagger("div")


class ProgressBar():
    """docstring for ProgressBar"""
    def __init__(self, id_container):
        self.element = jQuery(id_container)
        self.events_set = set()
        self.start()

    def addEventProgressBar(self, event_name):
        self.events_set.add(event_name)

    def removeEventProgressBar(self, event_name):
        try:
            self.events_set.remove(event_name)
        except:
            if window.PhanterPWA.DEBUG:
                console.info("Error on remove event of progressbar")

    def forceStop(self):
        self.events_set = set()
        self.element.find(".phanterpwa-main_progressbar-wrapper").removeClass("enabled")

    def check_progressbar(self):
        if len(self.events_set) == 0:
            self.element.find(".phanterpwa-main_progressbar-wrapper").removeClass("enabled")
        else:
            self.element.find(".phanterpwa-main_progressbar-wrapper").addClass("enabled")


    def start(self):
        self.element.html(self.xml())
        window.setInterval(self.check_progressbar, 30)

    def xml(self):
        return DIV(
            DIV(
                DIV(
                    _class="phanterpwa-main_progressbar-movement",
                ),
                _class="phanterpwa-main_progressbar"
            ),
            _class="phanterpwa-main_progressbar-wrapper enabled"
        ).jquery()
