from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = URL =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')


__pragma__('kwargs')


class ApiServer():

    def __init__(self):
        self.remote_address = window.PhanterPWA.CONFIG.CONFIGJS.api_server_address

    def _process_args(self, args):
        s_args = ""
        if isinstance(args, list):
            s_args = "/".join(args)
        if s_args != "":
            s_args = "{0}/".format(s_args)
        return s_args

    def _serialize_vars(self, _vars):
        ISTYPEOF = __pragma__("js", "{}", "_vars instanceof FormData")
        if _vars is None or _vars is js_undefined:
            return ""
        elif ISTYPEOF:
            return ""
        elif isinstance(_vars, dict):
            __pragma__('jsiter')
            jsdict = {}
            __pragma__('nojsiter')
            for x in _vars.keys():
                if _vars[x] is not None and _vars[x] is not js_undefined:
                    jsdict[x] = _vars[x]
            return "?{0}".format(jQuery.param(jsdict))
        else:
            t = jQuery.param(_vars)
            if t is not None or t is not js_undefined:
                return "?{0}".format(t)
            else:
                return ""

    def GET(self, **parameters):
        url_args = None
        url_vars = None
        onComplete = None
        headers = {
            'Cache-Control': 'no-store, must-revalidate, no-cache, max-age=0',
            'phanterpwa-application': window.PhanterPWA.CONFIG['PROJECT']['name'],
            'phanterpwa-application-version': window.PhanterPWA.CONFIG['PROJECT']['version']
        }
        if "url_args" in parameters:
            url_args = parameters["url_args"]
        if "url_vars" in parameters:
            url_vars = parameters["url_vars"]
        if "onComplete" in parameters:
            onComplete = parameters["onComplete"]
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

        __pragma__('jsiter')
        ajax_param = {
            'url': url,
            'type': "GET",
            'complete': onComplete,
            'success': _after_sucess,
            'error': lambda: window.PhanterPWA.ProgressBar.removeEventProgressBar("GET_" + date_stamp),
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

    def DELETE(self, **parameters):
        url_args = None
        url_vars = None
        onComplete = None
        headers = {
            'Cache-Control': 'no-store, must-revalidate, no-cache, max-age=0',
            'phanterpwa-application': window.PhanterPWA.CONFIG['PROJECT']['name'],
            'phanterpwa-application-version': window.PhanterPWA.CONFIG['PROJECT']['version']
        }
        if "url_args" in parameters:
            url_args = parameters["url_args"]
        if "url_vars" in parameters:
            url_vars = parameters["url_vars"]
        if "onComplete" in parameters:
            onComplete = parameters["onComplete"]
        if "headers" in parameters:
            if parameters["headers"] is not None:
                for x in parameters["headers"]:
                    headers[x] = parameters["headers"][x]
        date_stamp = __new__(Date().getTime())
        window.PhanterPWA.ProgressBar.addEventProgressBar("DELETE_" + date_stamp)
        client_token = localStorage.getItem("phanterpwa-client-token")
        authorization = sessionStorage.getItem("phanterpwa-authorization")
        url = "{0}/{1}{2}".format(self.remote_address, self._process_args(url_args), self._serialize_vars(url_vars))

        __pragma__('jsiter')
        ajax_param = {
            'url': url,
            'type': "DELETE",
            'complete': onComplete,
            'success': lambda: window.PhanterPWA.ProgressBar.removeEventProgressBar("DELETE_" + date_stamp),
            'error': lambda: window.PhanterPWA.ProgressBar.removeEventProgressBar("DELETE_" + date_stamp),
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

    def POST(self, **parameters):
        url_args = None
        form_data = None
        onComplete = None
        headers = {
            'Cache-Control': 'no-store, must-revalidate, no-cache, max-age=0',
            'phanterpwa-application': window.PhanterPWA.CONFIG['PROJECT']['name'],
            'phanterpwa-application-version': window.PhanterPWA.CONFIG['PROJECT']['version']
        }
        if "url_args" in parameters:
            url_args = parameters["url_args"]
        if "form_data" in parameters:
            form_data = parameters["form_data"]
        if "onComplete" in parameters:
            onComplete = parameters["onComplete"]
        if "headers" in parameters:
            if parameters["headers"] is not None:
                for x in parameters["headers"]:
                    headers[x] = parameters["headers"][x]
        date_stamp = __new__(Date().getTime())
        window.PhanterPWA.ProgressBar.addEventProgressBar("POST_" + date_stamp)
        client_token = localStorage.getItem("phanterpwa-client-token")
        authorization = sessionStorage.getItem("phanterpwa-authorization")
        url = "{0}/{1}".format(self.remote_address, self._process_args(url_args))

        __pragma__('jsiter')
        ajax_param = {
            'url': url,
            'type': "POST",
            'data': form_data,
            'complete': onComplete,
            'success': lambda: window.PhanterPWA.ProgressBar.removeEventProgressBar("POST_" + date_stamp),
            'error': lambda: window.PhanterPWA.ProgressBar.removeEventProgressBar("POST_" + date_stamp),
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

    def PUT(self, **parameters):
        url_args = None
        form_data = None
        onComplete = None
        headers = {
            'Cache-Control': 'no-store, must-revalidate, no-cache, max-age=0',
            'phanterpwa-application': window.PhanterPWA.CONFIG['PROJECT']['name'],
            'phanterpwa-application-version': window.PhanterPWA.CONFIG['PROJECT']['version']
        }
        if "url_args" in parameters:
            url_args = parameters["url_args"]
        if "form_data" in parameters:
            form_data = parameters["form_data"]
        if "onComplete" in parameters:
            onComplete = parameters["onComplete"]
        if "headers" in parameters:
            if parameters["headers"] is not None:
                for x in parameters["headers"]:
                    headers[x] = parameters["headers"][x]
        date_stamp = __new__(Date().getTime())
        window.PhanterPWA.ProgressBar.addEventProgressBar("PUT_" + date_stamp)
        client_token = localStorage.getItem("phanterpwa-client-token")
        authorization = sessionStorage.getItem("phanterpwa-authorization")
        url = "{0}/{1}".format(self.remote_address, self._process_args(url_args))

        __pragma__('jsiter')
        ajax_param = {
            'url': url,
            'type': "PUT",
            'data': form_data,
            'complete': onComplete,
            'success': lambda: window.PhanterPWA.ProgressBar.removeEventProgressBar("PUT_" + date_stamp),
            'error': lambda: window.PhanterPWA.ProgressBar.removeEventProgressBar("PUT_" + date_stamp),
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


__pragma__('nokwargs')
