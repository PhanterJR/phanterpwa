import phanterpwa.apptools.helpers as helpers
from org.transcrypt.stubs.browser import __pragma__


__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = js_undefined = setTimeout = window = this = console =\
    localStorage = 0
__pragma__('noskip')


DIV = helpers.XmlConstructor.tagger("div")
FORM = helpers.XmlConstructor.tagger("form")
I = helpers.XmlConstructor.tagger("i")
CONCATENATE = helpers.CONCATENATE


__pragma__('kwargs')


class Modal():
    def __init__(self, target_selector, **parameters):
        self.target_selector = target_selector
        self.target_element = jQuery(target_selector)
        self.title = ""
        self.content = ""
        self.footer = ""
        self.header_height = 80
        self.footer_height = 80
        self._max_content_height = 400
        self._form = parameters.get("form", None)
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
        wrapper_content = CONCATENATE(
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
        )
        if self._form is not None:
            if ["_class"] in parameters:
                parameters["_class"] = "{0}{1}".format(parameters["_class"], " phanterpwa-form")
            else:
                parameters["_class"] = "phanterpwa-form"
            parameters["_id"] = "form-{0}".format(self._form)
            parameters["_phanterpwa-form"] = self._form
            self.modal_wrapper = FORM(
                wrapper_content,
                **parameters
            )
        else:
            self.modal_wrapper = DIV(
                wrapper_content,
                **parameters
            )
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
        )

    def switch_modal(self):
        modal_container = jQuery(self.target_selector).find(".phanterpwa-component-modal-container")
        if modal_container.hasClass("enabled"):
            self.close()
        else:
            self.open()

    def close(self):
        modal_container = jQuery(self.target_selector).find(".phanterpwa-component-modal-container")
        modal_container.addClass("closing")
        setTimeout(
            lambda: modal_container.removeClass("enabled"),
            500
        )

    def _close_on_click_container(self, event, target_element):
        if (event.target is target_element):
            self.close()

    def open(self):
        self.start()
        modal_container = jQuery(self.target_selector).find(".phanterpwa-component-modal-container")
        modal_container.addClass("enabled")
        if callable(self._after_open):
            self._after_open(modal_container)

        def change_position_and_zindex(el):
            widget_name = jQuery(el).attr("phanterpwa-widget")
            widget = window.PhanterPWA.Request.widgets.get(widget_name, None)
            if widget is not None:
                widget.set_z_index("1006")
                widget.set_recalc_on_scroll(True)

        modal_container.find(
            "{0}, {1}, {2}".format(
                "phanterpwa-widget.phanterpwa-widget-select",
                "phanterpwa-widget.phanterpwa-widget-menubox",
                "tr.phanterpwa-widget-table-pagination"
            )
        ).each(
            lambda: change_position_and_zindex(this)
        )

    def _calc_content_height(self):
        h = jQuery(window).height()
        self._max_content_height = h - self.header_height - self.footer_height - 20
        if h <= 0:
            h = 0
        self.target_element = jQuery(self.target_selector)
        self.target_element.find(
            ".phanterpwa-component-modal-header-container"
        ).css(
            "height",
             self.header_height
        )
        self.target_element.find(
            ".phanterpwa-component-modal-wrapper"
        ).css(
            "padding-bottom",
            self.footer_height
        ).css(
            "padding-top",
            self.header_height

        )
        self.target_element.find(
            ".phanterpwa-component-modal-footer-container"
        ).css(
            "height",
            self.footer_height
        )
        self.target_element.find(
            ".phanterpwa-component-modal-content-container"
        ).css(
            "max-height",
            self._max_content_height
        )

    def start(self):
        self.target_element = jQuery(self.target_selector)
        self.target_element.find('.phanterpwa-component-modal-container.phanterpwa-fixed-fulldisplay').remove()
        self.modal_container.append_to(self.target_selector)
        self._calc_content_height()
        jQuery(window).resize(lambda: self._calc_content_height())
        self.target_element.find(".phanterpwa-centralizer-horizontal").off(
            "click.phanterpwa-component-modal-container"
        ).on(
            "click.phanterpwa-component-modal-container",
            lambda e: self._close_on_click_container(e, this)
        )
        self.target_element.find(".phanterpwa-centralizer-center").off(
            "click.phanterpwa-component-modal-container"
        ).on(
            "click.phanterpwa-component-modal-container",
            lambda e: self._close_on_click_container(e, this)
        )
        self.target_element.find(".phanterpwa-component-modal-close").off(
            "click.phanterpwa-component-modal-container"
        ).on(
            "click.phanterpwa-component-modal-container",
            self.close
        )


__pragma__('nokwargs')
