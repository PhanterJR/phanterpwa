import phanterpwa.transcrypt.helpers as helpers
from org.transcrypt.stubs.browser import __pragma__


__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = js_undefined = setTimeout = window = this = console =\
    localStorage = 0
__pragma__('noskip')


DIV = helpers.XmlConstructor.tagger("div")
I = helpers.XmlConstructor.tagger("i")

__pragma__('kwargs')


class Modal():
    def __init__(self, target_element, **parameters):
        self.target_element = jQuery(target_element)
        self.title = ""
        self.content = ""
        self.footer = ""
        self.header_height = 80
        self.footer_height = 80
        self._max_content_height = 400
        if "title" in parameters:
            self.title = parameters["title"]
        if "content" in parameters:
            self.content = parameters["content"]
        if "footer" in parameters:
            self.footer = parameters["footer"]
        if "header_height" in parameters:
            self.header_height = parameters["header_height"]
        if "footer_height" in parameters:
            self.footer_height = parameters["footer_height"]
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(
                parameters["_class"].strip(),
                " phanterpwa-component-modal-wrapper phanterpwa-container"
            )
        else:
            parameters["_class"] = "phanterpwa-component-modal-wrapper phanterpwa-container"
        if "after_open" in parameters:
            self._after_open = parameters["after_open"]
        self.modal_wrapper = DIV(
            DIV(
                DIV(
                    I(_class="fas fa-times"),
                    _class="phanterpwa-component-modal-close link"
                ),
                DIV(
                    self.title,
                    _class="phanterpwa-component-modal-title"
                ),
                _class="phanterpwa-component-modal-header-container"
            ),
            DIV(
                self.content,
                _class="phanterpwa-component-modal-content-container"
            ),
            DIV(
                self.footer,
                _class="phanterpwa-component-modal-footer-container"
            ),
            **parameters
        ).jquery()
        self.modal_container = DIV(
            DIV(
                DIV(
                    DIV(
                        DIV(
                            self.modal_wrapper,
                            _class="phanterpwa-centralizer-center"
                        ),
                        _class="phanterpwa-centralizer-horizontal"
                    ),
                    _class="phanterpwa-centralizer-vertical"
                ),
                _class="phanterpwa-centralizer-wrapper"
            ),
            _class="phanterpwa-component-modal-container phanterpwa-fixed-fulldisplay"
        ).jquery()

    def switch_modal(self):
        if self.modal_container.hasClass("enabled"):
            self.close()
        else:
            self.open()

    def close(self):
        self.modal_container.addClass("closing")
        setTimeout(
            lambda: self.modal_container.removeClass("enabled"),
            500
        )

    def _close_on_click_container(self, event, target_element):
        if (event.target is target_element):
            self.close()

    def open(self):
        self.start()
        self.modal_container.addClass("enabled")
        if self._after_open is not None and self._after_open is not js_undefined:
            self._after_open(self.modal_container)

    def _calc_content_height(self):
        h = jQuery(window).height()
        self._max_content_height = h - self.header_height - self.footer_height - 20
        if h <= 0:
            h = 0
        self.modal_container.find(
            ".phanterpwa-component-modal-header-container"
        ).css(
            "height",
             self.header_height
        )
        self.modal_container.find(
            ".phanterpwa-component-modal-wrapper"
        ).css(
            "padding-bottom",
            self.footer_height
        ).css(
            "padding-top",
            self.header_height

        )
        self.modal_container.find(
            ".phanterpwa-component-modal-footer-container"
        ).css(
            "height",
            self.footer_height
        )
        self.modal_container.find(
            ".phanterpwa-component-modal-content-container"
        ).css(
            "max-height",
            self._max_content_height
        )

    def start(self):
        self.target_element.find('.phanterpwa-component-modal-container.phanterpwa-fixed-fulldisplay').remove()
        if self.target_element is not None and self.target_element is not js_undefined:
            if window.PhanterPWA is not js_undefined:
                window.PhanterPWA.DOMXmlWriter.append(self.target_element, self.modal_container)
            else:
                self.target_element.append(self.modal_container)
        self._calc_content_height()
        jQuery(window).resize(lambda: self._calc_content_height())
        self.modal_container.find(".phanterpwa-centralizer-horizontal").off(
            "click.phanterpwa-component-modal-container"
        ).on(
            "click.phanterpwa-component-modal-container",
            lambda e: self._close_on_click_container(e, this)
        )
        self.modal_container.find(".phanterpwa-centralizer-center").off(
            "click.phanterpwa-component-modal-container"
        ).on(
            "click.phanterpwa-component-modal-container",
            lambda e: self._close_on_click_container(e, this)
        )
        self.modal_container.find(".phanterpwa-component-modal-close").off(
            "click.phanterpwa-component-modal-container"
        ).on(
            "click.phanterpwa-component-modal-container",
            self.close
        )


__pragma__('nokwargs')
