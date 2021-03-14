import phanterpwa.frontend.helpers as helpers
import phanterpwa.frontend.components.widgets as widgets
from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = M = js_undefined = window =\
    __new__ = FormData = console = localStorage = document = this = CodeMirror = 0
__pragma__('noskip')


DIV = helpers.XmlConstructor.tagger("div")


__pragma__('kwargs')


class CodeMirrorHelper(widgets.Widget):
    def __init__(self, identifier, **parameters):
        self.code_mirror_parameters = dict()
        for x in parameters.keys():
            if not x.startswith("_"):
                self.code_mirror_parameters[x] = parameters[x]
        parameters["_id"] = identifier
        if "_class" in parameters:
            parameters["_class"] = "{0}{1}".format(
                parameters["_class"].strip(),
                " phanterpwa-plugin-codemirrorhelper"
            )
        else:
            parameters["_class"] = "phanterpwa-plugin-codemirrorhelper"
        self._codemirror_target = window.PhanterPWA.get_id(identifier)
        html = DIV(_id=self._codemirror_target, _class="source_code-codemirror-wrapper")
        widgets.Widget.__init__(self, identifier, html, **parameters)

    def reload(self):
        self.start()

    def start(self):
        self.CodeMirror = CodeMirror(jQuery("#{0}".format(self._codemirror_target)).html("")[0],
            self.code_mirror_parameters)


__pragma__('nokwargs')
