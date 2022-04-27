import phanterpwa.frontend.application as application
import phanterpwa.frontend.helpers as helpers
import phanterpwa.frontend.components.auth_user as auth_user
import phanterpwa.frontend.components.left_bar as left_bar
import auto.config as config
import gatehandlers.reqs as reqs
import gatehandlers.testsp as testsp
import gatehandlers.project as project
import gatehandlers.developer as developer
import gatehandlers.fontawesome as fontawesome
import gatehandlers.examples as examples
import gatehandlers.errors as errors
import gatehandlers.home as home
from org.transcrypt.stubs.browser import __pragma__


__pragma__("skip")
jQuery = window = console = WebSocket = __new__ = location = this = confirm = 0
__pragma__("noskip")


gates = {
    'home': home.Index,
    'examples': examples.Index,
    'fontawesome': fontawesome.Index,
    'developer': developer.Index,
    'project': project.Index,
    'test_phanterpwa': testsp.Index,
    'check_requeriments': reqs.Index,
    'examples': examples.Index,
    401: errors.Error_401,
    403: errors.Error_403,
    404: errors.Error_404
}


MyApp = application.PhanterPWA(config.CONFIG, gates)
MyApp.add_component(left_bar.LeftBarMainButton("#layout-main_button-container"))
MyApp.add_component(left_bar.LeftBar("#layout-left_bar-container"))
MyApp.open_current_way()

