import phanterpwa.frontend.helpers as helpers
from org.transcrypt.stubs.browser import __pragma__


__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = js_undefined = setTimeout = window = this = console =\
    localStorage = 0
__pragma__('noskip')


DIV = helpers.XmlConstructor.tagger("div")
I = helpers.XmlConstructor.tagger("i")


__pragma__('kwargs')


class Pagination(object):
    """docstring for Pagination"""

    def __init__(self, target_element, **paramaters):
        self.target_element = jQuery(target_element)
        self._current_page = 1
        self._pages_list = [1]
        self._max_pages_on_screen = 11

    def start(self):
        html = DIV(
            _class="phanterpwa-pagination-wrapper"
        )


__pragma__('nokwargs')
