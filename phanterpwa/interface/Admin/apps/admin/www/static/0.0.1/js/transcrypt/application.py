import phanterpwa.apptools.application as application
import phanterpwa.apptools.helpers as helpers
import phanterpwa.apptools.components.auth_user as auth_user
import phanterpwa.apptools.components.left_bar as left_bar
import config
import gatekeeper
from org.transcrypt.stubs.browser import __pragma__

__pragma__("skip")
jQuery = window = console = WebSocket = __new__ = location = this = confirm = 0
__pragma__("noskip")


I = helpers.XmlConstructor.tagger("i")
I18N = helpers.I18N


MyApp = application.PhanterPWA(config.CONFIG, gatekeeper.gates)
MyApp.add_component(left_bar.LeftBarMainButton("#layout-main_button-container"))
MyApp.add_component(left_bar.LeftBar("#layout-left_bar-container"))
MyApp.open_current_way()
