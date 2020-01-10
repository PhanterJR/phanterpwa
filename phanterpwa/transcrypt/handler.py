from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = console = __new__ = Date = URL = sessionStorage = \
    js_undefined = jQuery = this = 0

__pragma__('noskip')


class RequestRouteHandler():

    def __init__(self, request):
        self.requires_login = False
        self.autorized_roles = ["all"]
        self.autorized_ids = ["all"]
        self.route_on_back = window.PhanterPWA.get_current_route()
        cred = self.check_credentials()
        if cred is True:
            self.initialize()
            self.request = request
            window.PhanterPWA.Response = self
            self.start()
        else:
            window.PhanterPWA.open_code_route(cred, request)

    def check_credentials(self):
        auth_user = window.PhanterPWA.get_auth_user()
        roles = []
        has_authentication = False
        if auth_user is not None:
            has_authentication = True
            roles = auth_user.roles
        if isinstance(self.autorized_roles, list) and isinstance(self.requires_login, bool):
            if self.requires_login is True and has_authentication:
                if "all" in self.autorized_roles and "all" in self.autorized_ids:
                    return True
                elif len(set(roles).intersection(set(self.autorized_roles))) > 0 and "all" in self.autorized_ids:
                    return True
                elif "all" in self.autorized_roles and int(auth_user.id) in self.autorized_ids:
                    return True
                elif len(set(roles).intersection(
                        set(self.autorized_roles))) > 0 and int(auth_user.id) in self.autorized_ids:
                    return True
                else:
                    return 403
            else:
                if "all" in self.autorized_roles and "all" in self.autorized_ids:
                    return True
                elif has_authentication:
                    if len(set(roles).intersection(set(self.autorized_roles))) > 0 and "all" in self.autorized_ids:
                        return True
                    elif "all" in self.autorized_roles and int(auth_user.id) in self.autorized_ids:
                        return True
                    elif len(set(roles).intersection(
                            set(self.autorized_roles))) > 0 and int(auth_user.id) in self.autorized_ids:
                        return True
                    else:
                        return 403
                elif "anonymous" in self.autorized_roles and "all" in self.autorized_ids:
                    if has_authentication:
                        return 403
                    else:
                        return True
                else:
                    return 401
        else:
            return 500

    def on_click_back_button(self):
        window.PhanterPWA.open_route(self.route_on_back)
        
    def initialize(self):
        if window.PhanterPWA.DEBUG:
            console.info("method not used: RequestRouteHandler.initialize()")

    def start(self):
        if window.PhanterPWA.DEBUG:
            console.info("method not used: RequestRouteHandler.start()")
