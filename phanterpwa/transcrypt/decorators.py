from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = Hammer =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')


__pragma__('kwargs')


def check_if_has_role(roles):
    roles = set(roles.roles)

    def decorator(f):

        def exec_if_has_role_decorator():
            auth_user = window.PhanterPWA.get_auth_user()
            if auth_user is None or auth_user is js_undefined:
                if window.PhanterPWA.CONFIG.PROJECT.debug:
                    console.info(
                        "The user is not allowed")
            else:
                roles_user = set(auth_user.roles)
                if roles_user.intersection(roles):
                    return f(has_role=True)
                else:
                    if window.PhanterPWA.CONFIG.PROJECT.debug:
                        console.info(
                            "The user hasn't the required role")
            return f(has_role=False)
        return exec_if_has_role_decorator
    return decorator


__pragma__('nokwargs')
