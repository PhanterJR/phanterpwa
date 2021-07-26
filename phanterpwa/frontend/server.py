from phanterpwa.frontend import helpers
from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = URL =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')


__pragma__('kwargs')


I18N = helpers.I18N
class ApiServer():

    def __init__(self):
        self.remote_address = window.PhanterPWA.CONFIG["APP"]["http_address"]

    @staticmethod
    def _process_args(args):
        s_args = ""
        ISINSTANCEOF = __pragma__("js", "{}", "args instanceof Array")
        if isinstance(args, list) or ISINSTANCEOF:
            s_args = "/".join(args)
        if s_args != "":
            s_args = "{0}/".format(s_args)
        return s_args

    @staticmethod
    def _process_parameters(parameters):
        _vars = dict()
        for x in parameters.keys():
            if x == "_":
                _vars[x] = parameters[x]
            elif x.startswith("_") and len(x) > 1:
                _vars[x[1:]] = parameters[x]
        if len(_vars.keys()) > 0:
            return _vars
        else:
            return parameters.get("url_vars", None)

    @staticmethod
    def _serialize_vars(_vars):
        ISTYPEOF = __pragma__("js", "{}", "_vars instanceof FormData")
        if _vars is None or _vars is js_undefined:
            return ""
        elif ISTYPEOF:
            return ""
        elif isinstance(_vars, dict):
            __pragma__('jsiter')
            jsdict = {}
            __pragma__('nojsiter')
            has_value = False
            for x in _vars.keys():
                has_value = True
                if _vars[x] is not None and _vars[x] is not js_undefined:
                    jsdict[x] = _vars[x]
            if has_value:
                return "?{0}".format(jQuery.param(jsdict))
            else:
                return ""
        else:
            t = jQuery.param(_vars)
            if t is not None or t is not js_undefined:
                return "?{0}".format(t)
            else:
                return ""

    def GET(self, *args, **parameters):
        url_vars = None
        onComplete = None
        headers = {
            'Cache-Control': 'no-store, must-revalidate, no-cache, max-age=0',
            'phanterpwa-application': window.PhanterPWA.CONFIG['PROJECT']['name'],
            'phanterpwa-application-version': window.PhanterPWA.CONFIG['PROJECT']['version']
        }
        reload_phanterpwa = parameters.get("reload", True)
        url_args = parameters.get("url_args", None)
        if len(args) > 0:
            url_args = args
        url_vars = self._process_parameters(parameters)
        onComplete = parameters.get("onComplete", lambda: console.info("GET") if window.PhanterPWA.DEBUG else "")
        if "headers" in parameters:
            if parameters["headers"] is not None:
                for x in parameters["headers"]:
                    headers[x] = parameters["headers"][x]
        date_stamp = __new__(Date().getTime())
        window.PhanterPWA.ProgressBar.addEventProgressBar("GET_" + date_stamp)
        client_token = localStorage.getItem("phanterpwa-client-token")
        authorization = sessionStorage.getItem("phanterpwa-authorization")
        all_args = self._process_args(url_args)
        all_vars = self._serialize_vars(url_vars)
        current_uri = "/{0}{1}".format(all_args, all_vars)
        url = "{0}{1}".format(self.remote_address, current_uri)
        if "get_cache" in parameters:
            if callable(parameters["get_cache"]):
                get_cache = parameters["get_cache"]
                if current_uri in window.PhanterPWA.Cache:
                    get_cache(window.PhanterPWA.Cache[current_uri])

        def _after_sucess(data):
            data_hash = data.hash
            data_uri = data.uri
            if data_hash is not js_undefined and data_uri is not js_undefined:
                if data_uri not in window.PhanterPWA.Cache:
                    window.PhanterPWA.Cache[data_uri] = data
                else:
                    if data_hash != window.PhanterPWA.Cache[data_uri].hash:
                        window.PhanterPWA.Cache[data_uri] = data

            window.PhanterPWA.ProgressBar.removeEventProgressBar("GET_" + date_stamp)

        def _after_error(data, ajax_status):
            window.PhanterPWA.ProgressBar.removeEventProgressBar("GET_" + date_stamp)
            self.on_ajax_error(data, ajax_status)

        __pragma__('jsiter')
        ajax_param = {
            'url': url,
            'type': "GET",
            'complete': lambda a, b, c: (onComplete(a, b, c), window.PhanterPWA.reload() if reload_phanterpwa else None),
            'success': _after_sucess,
            'error': _after_error,
            'datatype': 'json',
            'crossDomain': True,
            'headers': headers
        }
        if client_token is not None:
            ajax_param['headers']['phanterpwa-client-token'] = client_token
        if authorization is not None and authorization is not js_undefined:
            ajax_param['headers']['phanterpwa-authorization'] = authorization
        else:
            authorization = localStorage.getItem("phanterpwa-authorization")
            if authorization is not None and authorization is not js_undefined:
                ajax_param['headers']['phanterpwa-authorization'] = authorization
        __pragma__('nojsiter')
        jQuery.ajax(ajax_param)

    def DELETE(self, *args, **parameters):
        url_vars = None
        onComplete = None
        headers = {
            'Cache-Control': 'no-store, must-revalidate, no-cache, max-age=0',
            'phanterpwa-application': window.PhanterPWA.CONFIG['PROJECT']['name'],
            'phanterpwa-application-version': window.PhanterPWA.CONFIG['PROJECT']['version']
        }
        reload_phanterpwa = parameters.get("reload", True)
        url_args = parameters.get("url_args", None)
        if len(args) > 0:
            url_args = args
        url_vars = self._process_parameters(parameters)
        onComplete = parameters.get("onComplete", lambda: console.info("DELETE") if window.PhanterPWA.DEBUG else "")
        if "headers" in parameters:
            if parameters["headers"] is not None:
                for x in parameters["headers"]:
                    headers[x] = parameters["headers"][x]
        date_stamp = __new__(Date().getTime())
        window.PhanterPWA.ProgressBar.addEventProgressBar("DELETE_" + date_stamp)
        client_token = localStorage.getItem("phanterpwa-client-token")
        authorization = sessionStorage.getItem("phanterpwa-authorization")
        url = "{0}/{1}{2}".format(self.remote_address, self._process_args(url_args), self._serialize_vars(url_vars))
        def _after_error(data, ajax_status):
            window.PhanterPWA.ProgressBar.removeEventProgressBar("DELETE_" + date_stamp)
            self.on_ajax_error(data, ajax_status)
        __pragma__('jsiter')
        ajax_param = {
            'url': url,
            'type': "DELETE",
            'complete': lambda a, b, c: (onComplete(a, b, c), window.PhanterPWA.reload() if reload_phanterpwa else None),
            'success': lambda: window.PhanterPWA.ProgressBar.removeEventProgressBar("DELETE_" + date_stamp),
            'error': _after_error,
            'datatype': 'json',
            'crossDomain': True,
            'headers': headers
        }
        if client_token is not None:
            ajax_param['headers']['phanterpwa-client-token'] = client_token
        if authorization is not None and authorization is not js_undefined:
            ajax_param['headers']['phanterpwa-authorization'] = authorization
        else:
            authorization = localStorage.getItem("phanterpwa-authorization")
            if authorization is not None and authorization is not js_undefined:
                ajax_param['headers']['phanterpwa-authorization'] = authorization
        __pragma__('nojsiter')
        jQuery.ajax(ajax_param)

    def POST(self, *args, **parameters):
        form_data = None
        onComplete = None
        headers = {
            'Cache-Control': 'no-store, must-revalidate, no-cache, max-age=0',
            'phanterpwa-application': window.PhanterPWA.CONFIG['PROJECT']['name'],
            'phanterpwa-application-version': window.PhanterPWA.CONFIG['PROJECT']['version']
        }
        reload_phanterpwa = parameters.get("reload", True)
        url_args = parameters.get("url_args", None)
        if len(args) > 0:
            url_args = args
        if "form_data" in parameters:
            form_data = parameters["form_data"]
        onComplete = parameters.get("onComplete", lambda: console.info("POST") if window.PhanterPWA.DEBUG else "")
        if "headers" in parameters:
            if parameters["headers"] is not None:
                for x in parameters["headers"]:
                    headers[x] = parameters["headers"][x]
        date_stamp = __new__(Date().getTime())
        window.PhanterPWA.ProgressBar.addEventProgressBar("POST_" + date_stamp)
        client_token = localStorage.getItem("phanterpwa-client-token")
        authorization = sessionStorage.getItem("phanterpwa-authorization")
        url = "{0}/{1}".format(self.remote_address, self._process_args(url_args))
        def _after_error(data, ajax_status):
            window.PhanterPWA.ProgressBar.removeEventProgressBar("POST_" + date_stamp)
            self.on_ajax_error(data, ajax_status)
        __pragma__('jsiter')
        ajax_param = {
            'url': url,
            'type': "POST",
            'data': form_data,
            'complete': lambda a, b, c: (onComplete(a, b, c), window.PhanterPWA.reload() if reload_phanterpwa else None),
            'success': lambda: window.PhanterPWA.ProgressBar.removeEventProgressBar("POST_" + date_stamp),
            'error': _after_error,
            'datatype': 'json',
            'crossDomain': True,
            'headers': headers
        }
        if client_token is not None:
            ajax_param['headers']['phanterpwa-client-token'] = client_token
        if authorization is not None and authorization is not js_undefined:
            ajax_param['headers']['phanterpwa-authorization'] = authorization
        else:
            authorization = localStorage.getItem("phanterpwa-authorization")
            if authorization is not None and authorization is not js_undefined:
                ajax_param['headers']['phanterpwa-authorization'] = authorization
        ISTYPEOF = __pragma__("js", "{}", "form_data instanceof FormData")
        if ISTYPEOF:
            ajax_param['processData'] = False
            ajax_param['contentType'] = False
        __pragma__('nojsiter')
        jQuery.ajax(ajax_param)

    def PUT(self, *args, **parameters):
        form_data = None
        onComplete = None
        headers = {
            'Cache-Control': 'no-store, must-revalidate, no-cache, max-age=0',
            'phanterpwa-application': window.PhanterPWA.CONFIG['PROJECT']['name'],
            'phanterpwa-application-version': window.PhanterPWA.CONFIG['PROJECT']['version']
        }
        reload_phanterpwa = parameters.get("reload", True)
        url_args = parameters.get("url_args", None)
        if len(args) > 0:
            url_args = args
        if "form_data" in parameters:
            form_data = parameters["form_data"]
        onComplete = parameters.get("onComplete", lambda: console.info("PUT") if window.PhanterPWA.DEBUG else "")
        if "headers" in parameters:
            if parameters["headers"] is not None:
                for x in parameters["headers"]:
                    headers[x] = parameters["headers"][x]
        date_stamp = __new__(Date().getTime())
        window.PhanterPWA.ProgressBar.addEventProgressBar("PUT_" + date_stamp)
        client_token = localStorage.getItem("phanterpwa-client-token")
        authorization = sessionStorage.getItem("phanterpwa-authorization")
        url = "{0}/{1}".format(self.remote_address, self._process_args(url_args))
        def _after_error(data, ajax_status):
            window.PhanterPWA.ProgressBar.removeEventProgressBar("PUT_" + date_stamp)
            self.on_ajax_error(data, ajax_status)
        __pragma__('jsiter')
        ajax_param = {
            'url': url,
            'type': "PUT",
            'data': form_data,
            'complete': lambda a, b, c: (onComplete(a, b, c), window.PhanterPWA.reload() if reload_phanterpwa else None),
            'success': lambda: window.PhanterPWA.ProgressBar.removeEventProgressBar("PUT_" + date_stamp),
            'error': _after_error,
            'datatype': 'json',
            'crossDomain': True,
            'headers': headers
        }
        if client_token is not None:
            ajax_param['headers']['phanterpwa-client-token'] = client_token
        if authorization is not None and authorization is not js_undefined:
            ajax_param['headers']['phanterpwa-authorization'] = authorization
        else:
            authorization = localStorage.getItem("phanterpwa-authorization")
            if authorization is not None and authorization is not js_undefined:
                ajax_param['headers']['phanterpwa-authorization'] = authorization
        ISTYPEOF = __pragma__("js", "{}", "form_data instanceof FormData")
        if ISTYPEOF:
            ajax_param['processData'] = False
            ajax_param['contentType'] = False
        __pragma__('nojsiter')
        jQuery.ajax(ajax_param)

    def getClientToken(self, callback=None):
        def onComplete(data, ajax_status):
            if ajax_status == "success":
                auth_user = data.responseJSON.auth_user
                if (auth_user == "anonymous") or (auth_user == "logout"):
                    sessionStorage.removeItem("phanterpwa-authorization")
                    sessionStorage.removeItem("auth_user")
                    localStorage.removeItem("phanterpwa-authorization")
                    localStorage.removeItem("auth_user")
                client_token = data.responseJSON.client_token
                url_token = data.responseJSON.url_token
                if (url_token is not js_undefined):
                    localStorage.setItem('phanterpwa-url-token', url_token)

                if (client_token is not js_undefined):
                    localStorage.setItem("phanterpwa-client-token", client_token)
                    if callback is not None and callback is not js_undefined:
                        callback(data, ajax_status)
            else:
                if data.status == 0:
                    console.info("Server Problem!")
                elif data.status == 400:
                    sessionStorage.js_clear()
                    localStorage.js_clear()

        client_token = localStorage.getItem("phanterpwa-client-token")
        session_authorization = sessionStorage.getItem("phanterpwa-authorization")

        if client_token is None or client_token is js_undefined:
            sessionStorage.removeItem("phanterpwa-authorization")
            sessionStorage.removeItem("auth_user")
        if session_authorization is None or session_authorization is js_undefined:
            local_authorization = localStorage.getItem("phanterpwa-authorization")
            if local_authorization is None or local_authorization is js_undefined:
                sessionStorage.removeItem("phanterpwa-authorization")
                sessionStorage.removeItem("auth_user")
                localStorage.removeItem("phanterpwa-authorization")
                localStorage.removeItem("auth_user")

        return self.GET(**{'url_args': ['api', 'client'], 'onComplete': onComplete})

    def reSignCredentials(self):
        date_stamp = __new__(Date().getTime())
        last_resing = sessionStorage.getItem("last_resing")
        authorization = sessionStorage.getItem("phanterpwa-authorization")
        auth_user = sessionStorage.getItem("auth_user")
        if auth_user is None or auth_user is js_undefined:
            auth_user = localStorage.getItem("auth_user")
        lets_go_resign = False
        if last_resing is not None and last_resing is not js_undefined:
            timeout_last_resign = window.PhanterPWA.CONFIG['CONFIGJS']['timeout_to_resign'] * 1000
            if (int(last_resing) + int(timeout_last_resign)) < int(date_stamp):
                lets_go_resign = True
                sessionStorage.setItem("last_resing", date_stamp)
        else:
            sessionStorage.setItem("last_resing", date_stamp)
            lets_go_resign = True

        def onComplete(data, ajax_status):
            json = data.responseJSON
            if ajax_status == "success":
                if json.url_token is not None and json.url_token is not js_undefined:
                    localStorage.setItem('phanterpwa-url-token', json.url_token)
                if json.client_token is not None and json.client_token is not js_undefined:
                    localStorage.setItem('phanterpwa-client-token', json.client_token)
                if json.authorization is not None and json.authorization is not js_undefined:
                    if auth_user["remember_me"] is True:
                        localStorage.setItem('phanterpwa-authorization', json.authorization)
                    else:
                        localStorage.setItem('phanterpwa-authorization', json.authorization)
        if lets_go_resign and authorization is not None and authorization is not js_undefined:
            if auth_user is not None and auth_user is not js_undefined:
                self.GET(**{
                    "url_args": ["api", "resigncredentials"],
                    "url_vars": {"_": date_stamp},
                    "onComplete": onComplete
                })

    def on_ajax_error(self, data, status):
        json = data.responseJSON
        message = I18N("Unexpected error!", **{"_pt-br": "Erro inesperado!"})
        reasons = None
        if json is not None and json is not js_undefined:
            if json.i18n is not None and json.i18n is not js_undefined:
                if json.i18n.message is not None and json.i18n is not js_undefined:
                    message = json.i18n.message
                if json.i18n.reasons is not None and json.i18n is not js_undefined:
                    reasons = json.i18n.reasons
            else:
                if json.message is not None and json.message is not js_undefined:
                    message = json.message
                if json.reasons is not None and json.reasons is not js_undefined:
                    reasons = json.reasons
        if data.status == 401 or data.status == 403:
            if window.PhanterPWA.logged():
                if data.status == 401:
                    if json.specification == "client deleted":
                        self.getClientToken(callback=lambda: (
                                window.PhanterPWA.reload_component("auth_user"),
                                window.PhanterPWA.reload_component("left_bar")
                            )
                        )
                window.PhanterPWA.open_code_way(data.status, window.PhanterPWA.Request, window.PhanterPWA.Response, reasons)
        else:
            window.PhanterPWA.flash(**{'html': message})


__pragma__('nokwargs')
