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
    def __init__(self, target_element, *content, **parameters):
        self.target_element = jQuery(target_element)
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
        if self.target_element.find("#phanterpwa-component-topslide-wrapper").hasClass("enabled"):
            self.close()
        else:
            self.open()

    def close(self):
        self.target_element.find("#phanterpwa-component-topslide-wrapper").slideUp()

    def open(self):
        self.start()
        self.target_element.find("#phanterpwa-component-topslide-wrapper").slideDown()
        if self._after_open is not None and self._after_open is not js_undefined:
            self._after_open(self.target_element.find("#phanterpwa-component-topslide-wrapper"))

    def start(self):
        if self.target_element is not None and self.target_element is not js_undefined:
            self.target_element.find('#phanterpwa-component-topslide-wrapper').remove()
            self.target_element.append(self.jquery())
            self.target_element.find(".phanterpwa-component-topslide-close").off(
                "click.phanterpwa_component_topslide_close"
            ).on(
                "click.phanterpwa_component_topslide_close",
                self.close
            )


__pragma__('nokwargs')
