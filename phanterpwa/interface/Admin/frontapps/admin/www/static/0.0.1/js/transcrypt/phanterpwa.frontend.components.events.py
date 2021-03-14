import phanterpwa.frontend.helpers as helpers
import phanterpwa.frontend.application as application
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
        window.PhanterPWA.open_way(jQuery(el).attr('phanterpwa-way'))
        window.PhanterPWA.Request.element = el


    def _bind(self, el, forced=False):
        el = jQuery(el)
        if not window.PhanterPWA.check_event_namespace(el, "click", "phanterpwa-way") or forced:
            el.off(
                "click.phanterpwa-way"
            ).on(
                "click.phanterpwa-way",
                lambda: self._open_way(this)
            )
            if window.PhanterPWA.DEBUG:
                console.info("Reload Event WayHiperlinks")

    def reload(self, **context):
        self.start(**context)

    def start(self, **context):
        target_selector = context.get("selector", "body")
        if jQuery("body").hasClass("phanterpwa-lock"):
            jQuery("[phanterpwa-way]").off("click.phanterpwa-way")
        else:
            jQuery(target_selector).find("[phanterpwa-way]").each(lambda: self._bind(this))


class Waves(Event):
    def __init__(self):
        Event.__init__(self, "Waves")

    def _on_click(self, el, ev):
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

    def _bind(self, el, forced=False):
        el = jQuery(el)
        if not window.PhanterPWA.check_event_namespace(el, "click", "phanterpwa-event-wave") or forced:
            el.off("click.phanterpwa-event-wave").on(
                "click.phanterpwa-event-wave",
                lambda event: self._on_click(this, event)
            )
            if window.PhanterPWA.DEBUG:
                console.info("Reload Event Wave")

    def start(self, **context):
        target_selector = context.get("target", "body")
        jQuery(target_selector).find(".wave_on_click").each(lambda: self._bind(this))


# class WidgetsInput(Event):
#     def __init__(self):
#         Event.__init__(self, "WidgetsInput")
#         self.focus = False
#         self.has_val = None

#     def reload(self):
#         for x in window.PhanterPWA.Request.widgets.keys():
#             window.PhanterPWA.Request.widgets[x]._reload()

#     def _cleck_element(self, instance):
#         if jQuery(instance.target_selector).length == 0:
#             return False
#         return True

#     def start(self):
#         for x in window.PhanterPWA.Request.widgets.keys():
#             window.PhanterPWA.Request.widgets[x].start()


__pragma__('nokwargs')
