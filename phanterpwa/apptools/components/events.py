import phanterpwa.apptools.helpers as helpers
import phanterpwa.apptools.application as application
from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = js_undefined = window = setTimeout = document = console = this = \
    __new__ = FormData = console = localStorage = 0
__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")

__pragma__('kwargs')


class Event():
    def __init__(self, identifier):
        self.identifier = identifier

    def reload(self):
        if window.PhanterPWA.DEBUG:
            console.info("The Event {0} reload".format(self.identifier))

    def start(self):
        if window.PhanterPWA.DEBUG:
            console.info("The Component {0} starts".format(self.identifier))


class WayHiperlinks(Event):
    def __init__(self):
        Event.__init__(self, "WayHiperlinks")

    def _open_way(self, el):
        r = application.WayRequest()
        r.element = el
        window.PhanterPWA.Request = r
        r.open_way(jQuery(el).attr('phanterpwa-way'))

    def reload(self, **context):
        self.start(**context)

    def start(self, **context):
        target_selector = context.get("selector", "body")
        if jQuery("body").hasClass("phanterpwa-lock"):
            jQuery("[phanterpwa-way]").off("click.phanterpwa-way")
        else:
            jQuery(target_selector).find("[phanterpwa-way]").off(
                "click.phanterpwa-way"
            ).on(
                "click.phanterpwa-way",
                lambda: self._open_way(this)
            )


class Waves(Event):
    def __init__(self):
        Event.__init__(self, "Waves")

    def _bind(self, el, ev):
        el = jQuery(el)
        pY = ev.pageY - el.offset().top
        pX = ev.pageX - el.offset().left

        wave = DIV(
            _class="wave"
        ).jquery()
        el.append(wave.css("left", pX).css("top", pY).animate({
            "top": pY - 300,
            "left": pX - 300,
            "width": 600,
            "height": 600,
            "opacity": 0
        }, 1000))
        setTimeout(lambda: wave.remove(), 2000)

    def reload(self, **context):
        self.start(**context)

    def start(self, **context):
        target_selector = context.get("target", "body")

        jQuery(target_selector).find(".wave_on_click").off("click.phanterpwa-event-wave").on(
            "click.phanterpwa-event-wave",
            lambda event: self._bind(this, event)
        )


class WidgetsInput(Event):
    def __init__(self):
        Event.__init__(self, "WidgetsInput")
        self.focus = False
        self.has_val = None

    def reload(self):
        for x in window.PhanterPWA.Request.widgets.keys():
            if callable(window.PhanterPWA.Request.widgets[x].reload):
                window.PhanterPWA.Request.widgets[x].reload()

    def _cleck_element(self, instance):
        if jQuery(instance.target_selector).length == 0:
            return False
        return True

    def start(self):
        for x in window.PhanterPWA.Request.widgets.keys():
            if callable(window.PhanterPWA.Request.widgets[x].start):
                window.PhanterPWA.Request.widgets[x].start()


__pragma__('nokwargs')
