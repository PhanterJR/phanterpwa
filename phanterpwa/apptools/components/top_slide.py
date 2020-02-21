import phanterpwa.apptools.helpers as helpers
from org.transcrypt.stubs.browser import __pragma__


__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = js_undefined = setTimeout = window = this = console =\
    localStorage = 0
__pragma__('noskip')


DIV = helpers.XmlConstructor.tagger("div")
I = helpers.XmlConstructor.tagger("i")

__pragma__('kwargs')


class TopSlide(helpers.XmlConstructor):
    def __init__(self, target_selector, *content, **parameters):
        self.target_selector = target_selector
        self.element_target = jQuery(self.target_selector)
        self._after_open = None
        if "after_open" in parameters:
            self._after_open = parameters["after_open"]
        if "_id" not in parameters:
            parameters["_id"] = "phanterpwa-component-topslide-wrapper"
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(
                parameters["_class"].strip(),
                " phanterpwa-component-topslide-wrapper"
            )
        else:
            parameters["_class"] = "phanterpwa-component-topslide-wrapper"
        content.insert(0, DIV(I(_class="fas fa-times"), _class="phanterpwa-component-topslide-close link"))
        helpers.XmlConstructor.__init__(self, "div", False, *content, **parameters)

    def switch(self):
        self.element_target = jQuery(self.target_selector)
        if self.element_target.find("#phanterpwa-component-topslide-wrapper").hasClass("enabled"):
            self.close()
        else:
            self.open()

    def close(self):
        self.element_target = jQuery(self.target_selector)
        self.element_target.find("#phanterpwa-component-topslide-wrapper").slideUp()

    def open(self):
        self.element_target = jQuery(self.target_selector)
        self.start()
        self.element_target.find("#phanterpwa-component-topslide-wrapper").slideDown()
        if self._after_open is not None and self._after_open is not js_undefined:
            self._after_open(self.element_target.find("#phanterpwa-component-topslide-wrapper"))

    def start(self):
        self.element_target = jQuery(self.target_selector)
        if self.element_target is not None and self.element_target is not js_undefined:
            self.element_target.find('#phanterpwa-component-topslide-wrapper').remove()
            self.append_to(self.element_target)
            self.element_target.find(".phanterpwa-component-topslide-close").off(
                "click.phanterpwa_component_topslide_close"
            ).on(
                "click.phanterpwa_component_topslide_close",
                self.close
            )


__pragma__('nokwargs')
