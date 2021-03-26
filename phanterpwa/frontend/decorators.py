#?from org.transcrypt.stubs.browser import __pragma__
# __pragma__ ('ecom')
#?__pragma__('alias', "jQuery", "$")
#?__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = Hammer =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

#?__pragma__('noskip')


#?__pragma__('kwargs')


def requires_authentication(users_id=None, users_email=None, roles_id=None, roles_name=None):
    def decorator(f):

        def requires_authentication_decorator(self, *args, **kargs):
            self.status = 200
            if any([users_id is not None, users_email is not None, roles_id is not None, roles_name is not None]):
                if isinstance(users_id, (list, tuple)):
                    if self.current_user.id in users_id:
                        return f(self, *args, **kargs)
                if isinstance(users_id, int):
                    if self.current_user.id == users_id:
                        return f(self, *args, **kargs)
                if isinstance(users_email, (list, tuple)):
                    if self.current_user.email in users_email:
                        return f(self, *args, **kargs)
                if isinstance(users_email, str):
                    if users_email == self.current_user.email:
                        return f(self, *args, **kargs)
                if isinstance(self.current_user.roles, list):
                    if isinstance(roles_id, int):
                        for x in self.current_user.roles_id:
                            if x == roles_id:
                                return f(self, *args, **kargs)
                    if isinstance(roles_name, str):
                        for x in self.current_user.roles:
                            if x == roles_name:
                                return f(self, *args, **kargs)
                    if isinstance(roles_id, (list, tuple)):
                        for x in self.current_user.roles_id:
                            if x in roles_id:
                                return f(self, *args, **kargs)
                    if isinstance(roles_name, (list, tuple)):
                        for x in self.current_user.roles:
                            if x in roles_name:
                                return f(self, *args, **kargs)
                self.status = 403
                return self._error(403)
            elif self.current_user is None or self.current_user is js_undefined:
                self.status = 403
                return self._error(403)
            else:
                return f(self, *args, **kargs)

        return requires_authentication_decorator
    return decorator


def requires_no_authentication():
    def decorator(f):
        def requires_no_authentication_decorator(self, *args, **kargs):
            self.status = 200
            if self.phanterpwa_current_user is None or self.phanterpwa_current_user is js_undefined:
                return f(self, *args, **kargs)
            else:
                self.status = 403
                return self._error(403)
        return requires_no_authentication_decorator
    return decorator

def check_authorization(authorization_test=False, on_error=None):
    def decorator(f):
        def check_authorization_decorator(responseObj):
            test = False
            if callable(authorization_test):
                test = authorization_test()

            if test is True:
                window.PhanterPWA.Response = responseObj
                return f(responseObj)
            else:
                code = 401
                if window.PhanterPWA.logged():
                    code = 403

                if callable(on_error):
                    on_error(code,  responseObj._request, responseObj)
                else:
                    window.PhanterPWA.open_code_way(code, responseObj._request, responseObj)
                
        return check_authorization_decorator
    return decorator

#?__pragma__('nokwargs')
# __pragma__ ('noecom')