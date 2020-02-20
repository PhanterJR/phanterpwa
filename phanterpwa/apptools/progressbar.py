from org.transcrypt.stubs.browser import __pragma__
from phanterpwa.apptools import helpers
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
        self.start()

    def addEventProgressBar(self, event_name):
        events = self.element.attr("events")
        if events is js_undefined:
            self.element.attr("events", JSON.stringify([event_name]))
        else:
            events = set(JSON.parse(events))
            events.add(event_name)
            events = list(events)
            self.element.attr("events", JSON.stringify(events))

    def removeEventProgressBar(self, event_name):
        events = self.element.attr("events")
        if events is not js_undefined:
            events = set(JSON.parse(events))
            events.remove(event_name)
            events = JSON.stringify(list(events))
            if events != "[]":
                self.element.attr("events", events)
            else:
                self.element.removeAttr("events")
                self.element.find(".phanterpwa-main_progressbar-wrapper").removeClass("enabled")

    def forceStop(self):
        self.element.removeAttr("events")
        self.element.find(".phanterpwa-main_progressbar-wrapper").removeClass("enabled")

    def check_progressbar(self):
        events = self.element.attr('events')
        if events is not js_undefined:
            self.element.find(".phanterpwa-main_progressbar-wrapper").addClass("enabled")
        else:
            self.element.find(".phanterpwa-main_progressbar-wrapper").removeClass("enabled")

    def start(self):
        self.element.html(self.xml())
        window.setInterval(self.check_progressbar, 1000)

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
