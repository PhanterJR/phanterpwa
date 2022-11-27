from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = URL =\
    sessionStorage = this = FileReader = JSON = WebSocket = js_undefined = navigator = setTimeout = __new__ = Date = 0

__pragma__('noskip')


__pragma__('kwargs')


class Ajax():
    def __init__(self, http_address):
        self.remote_address = http_address
        self._headers = {
            'Cache-Control': 'no-store, must-revalidate, no-cache, max-age=0',
            'phanterpwa-application': window.PhanterPWA.CONFIG['PROJECT']['name'],
            'phanterpwa-application-version': window.PhanterPWA.CONFIG['PROJECT']['version']
        }

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

    def GET(self, *url_args, **parameters):
        _headers = dict(**self._headers)
        _datatype = parameters.get("datatype", "json")
        _url_vars = parameters.get("url_vars", None)
        _complete = parameters.get("complete", None)
        _crossDomain = parameters.get("crossDomain", True)
        _error = parameters.get("error", None)
        _success = parameters.get("success", None)
        _user_headers = parameters.get("headers", {})
        for x in _user_headers.keys():
            _headers[x] = _user_headers[x]
        _all_args = self._process_args(url_args)
        _all_vars = self._serialize_vars(_url_vars)
        _url = "{0}/{1}{2}".format(self.remote_address, _all_args, _all_vars)

        __pragma__('jsiter')
        ajax_param = {
            'url': _url,
            'type': "GET",
            'complete': lambda a, b, c: _complete(a, b, c),
            'success': _success,
            'error': _error,
            'datatype': _datatype,
            'crossDomain': _crossDomain,
            'headers': _headers
        }
        client_token = window.PhanterPWA.get_client_token()
        authorization = window.PhanterPWA.get_authorization()
        if client_token is not None:
            ajax_param['headers']['phanterpwa-client-token'] = client_token
        if authorization is not None:
            ajax_param['headers']['phanterpwa-authorization'] = authorization

        __pragma__('nojsiter')
        jQuery.ajax(ajax_param)

    def DELETE(self, *url_args, **parameters):
        _headers = dict(**self._headers)
        _datatype = parameters.get("datatype", "json")
        _url_vars = parameters.get("url_vars", None)
        _complete = parameters.get("complete", None)
        _crossDomain = parameters.get("crossDomain", True)
        _error = parameters.get("error", None)
        _success = parameters.get("success", None)
        _user_headers = parameters.get("headers", {})
        for x in _user_headers.keys():
            _headers[x] = _user_headers[x]
        _all_args = self._process_args(url_args)
        _all_vars = self._serialize_vars(_url_vars)
        _current_uri = "/{0}{1}".format()
        _url = "{0}/{1}{2}".format(self.remote_address, _all_args, _all_vars)

        __pragma__('jsiter')
        ajax_param = {
            'url': _url,
            'type': "DELETE",
            'complete': lambda a, b, c: _complete(a, b, c),
            'success': _success,
            'error': _error,
            'datatype': _datatype,
            'crossDomain': _crossDomain,
            'headers': _headers
        }
        client_token = window.PhanterPWA.get_client_token()
        authorization = window.PhanterPWA.get_authorization()
        if client_token is not None:
            ajax_param['headers']['phanterpwa-client-token'] = client_token
        if authorization is not None:
            ajax_param['headers']['phanterpwa-authorization'] = authorization

        __pragma__('nojsiter')
        jQuery.ajax(ajax_param)

    def POST(self, *url_args, **parameters):
        _headers = dict(**self._headers)
        _datatype = parameters.get("datatype", "json")
        _url_vars = parameters.get("url_vars", None)
        _complete = parameters.get("complete", None)
        _form_data = parameters.get("form_data", None)
        _crossDomain = parameters.get("crossDomain", True)
        _error = parameters.get("error", None)
        _success = parameters.get("success", None)
        _user_headers = parameters.get("headers", {})
        for x in _user_headers.keys():
            _headers[x] = _user_headers[x]
        _all_args = self._process_args(url_args)
        _all_vars = self._serialize_vars(_url_vars)
        _url = "{0}/{1}{2}".format(self.remote_address, _all_args, _all_vars)

        __pragma__('jsiter')
        ajax_param = {
            'url': _url,
            'type': "POST",
            'data': _form_data,
            'complete': lambda a, b, c: _complete(a, b, c),
            'success': _success,
            'error': _error,
            'datatype': _datatype,
            'crossDomain': _crossDomain,
            'headers': _headers
        }
        client_token = window.PhanterPWA.get_client_token()
        authorization = window.PhanterPWA.get_authorization()
        if client_token is not None:
            ajax_param['headers']['phanterpwa-client-token'] = client_token
        if authorization is not None:
            ajax_param['headers']['phanterpwa-authorization'] = authorization
        ISTYPEOF = __pragma__("js", "{}", "form_data instanceof FormData")
        if ISTYPEOF:
            ajax_param['processData'] = False
            ajax_param['contentType'] = False
        __pragma__('nojsiter')
        jQuery.ajax(ajax_param)

    def PUT(self, *url_args, **parameters):
        _headers = dict(**self._headers)
        _datatype = parameters.get("datatype", "json")
        _url_vars = parameters.get("url_vars", None)
        _complete = parameters.get("complete", None)
        _form_data = parameters.get("form_data", None)
        _crossDomain = parameters.get("crossDomain", True)
        _error = parameters.get("error", None)
        _success = parameters.get("success", None)
        _user_headers = parameters.get("headers", {})
        for x in _user_headers.keys():
            _headers[x] = _user_headers[x]
        _all_args = self._process_args(url_args)
        _all_vars = self._serialize_vars(_url_vars)
        _url = "{0}/{1}{2}".format(self.remote_address, _all_args, _all_vars)

        __pragma__('jsiter')
        ajax_param = {
            'url': _url,
            'type': "PUT",
            'data': _form_data,
            'complete': lambda a, b, c: _complete(a, b, c),
            'success': _success,
            'error': _error,
            'datatype': _datatype,
            'crossDomain': _crossDomain,
            'headers': _headers
        }
        client_token = window.PhanterPWA.get_client_token()
        authorization = window.PhanterPWA.get_authorization()
        if client_token is not None:
            ajax_param['headers']['phanterpwa-client-token'] = client_token
        if authorization is not None:
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


class Websocket():
    def __init__(self, websocket_address):
        self.remote_address = websocket_address
        self._headers = {
            'Cache-Control': 'no-store, must-revalidate, no-cache, max-age=0',
            'phanterpwa-application': window.PhanterPWA.CONFIG['PROJECT']['name'],
            'phanterpwa-application-version': window.PhanterPWA.CONFIG['PROJECT']['version']
        }
        self._opened = False
        self.websocket_address = websocket_address
        self.comulative_time = 300
        self.last_ws = None
        self.manual_connection = False
        self.manual_close = False
        self.onClose = None
        self.onError = None
        self.onMessage = None
        self.onOpen = None
        self.show_alert_reconnect = False
        setTimeout(lambda: self.connect(), self.comulative_time)

    def send(self, message):
        if self._opened:
            self._ws.send(message)

    def close(self):
        self.manual_close = True
        self._ws.close()

    def _onClose(self, evt):
        self._opened = False
        if window.PhanterPWA.DEBUG:
            console.info("Closing websocket")
        if not self.manual_close:
            setTimeout(lambda: self.start(), self.comulative_time)
        else:
            self.manual_close = False
        if callable(self.onClose):
            self.onClose(evt)

    def _onError(self, evt):
        if window.PhanterPWA.DEBUG:
            console.info("Error on websocket", evt)
        if self.comulative_time > 9000 and not self.manual_connection:
                window.PhanterPWA.flash("Lost server connection!")
                self.manual_connection = True
        else:
            self.comulative_time = self.comulative_time + 1000
        if callable(self.onError):
            self.onError(evt)

    def _onMessage(self, evt):
        if window.PhanterPWA.DEBUG:
            console.info(evt.data)
        if callable(self.onMessage):
            self.onMessage(evt)

    def _onOpen(self, evt):
        self.comulative_time = 0
        self._opened = True
        if window.PhanterPWA.DEBUG:
            console.info("Opening websocket")
        self.send("command_online")
        if callable(self.onOpen):
            self.onOpen(evt)

    def _binds(self):
        self._ws.onopen = lambda evt: self._onOpen(evt)
        self._ws.onmessage = lambda evt: self._onMessage(evt)
        self._ws.onerror = lambda evt: self._onError(evt)
        self._ws.onclose = lambda evt: self._onClose(evt)

    def connect(self):
        if not self.manual_connection:
            self._ws = __new__(WebSocket(self.websocket_address))
            self._authorization = window.PhanterPWA.get_authorization()
            self._config = window.PhanterPWA.CONFIG
            self._binds()
        else:
            if callable(self.onConectionProblem):
                self.onConectionProblem(self)
            else:
                console.alert("Connection problem! You need to reconnect!")

    def reconnect(self):
        self.manual_connection = False
        self.comulative_time = 0
        self._ws = __new__(WebSocket(self.websocket_address))
        self._authorization = window.PhanterPWA.get_authorization()
        self._config = window.PhanterPWA.CONFIG
        self._binds()

    def _process_args(self, args):
        s_args = ""
        if isinstance(args, list):
            return args
        else:
            return None

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
            return jsdict
        else:
            t = jQuery.param(_vars)
            if t is not None or t is not js_undefined:
                return t
            else:
                return ""

    def GET(self, *url_args, **parameters):
        _headers = dict(**self._headers)
        _datatype = parameters.get("datatype", "json")
        _url_vars = parameters.get("url_vars", None)
        _complete = parameters.get("complete", None)
        _crossDomain = parameters.get("crossDomain", True)
        _error = parameters.get("error", None)
        _success = parameters.get("success", None)
        _user_headers = parameters.get("headers", {})
        for x in _user_headers.keys():
            _headers[x] = _user_headers[x]
        _all_args = self._process_args(url_args)
        _all_vars = self._serialize_vars(_url_vars)
        _url = "{0}/{1}{2}".format(self.remote_address, _all_args, _all_vars)

        __pragma__('jsiter')
        ajax_param = {
            'url': _url,
            'type': "GET",
            'complete': lambda a, b, c: _complete(a, b, c),
            'success': _success,
            'error': _error,
            'datatype': _datatype,
            'crossDomain': _crossDomain,
            'headers': _headers
        }
        client_token = window.PhanterPWA.get_client_token()
        authorization = window.PhanterPWA.get_authorization()
        if client_token is not None:
            ajax_param['headers']['phanterpwa-client-token'] = client_token
        if authorization is not None:
            ajax_param['headers']['phanterpwa-authorization'] = authorization

        __pragma__('nojsiter')
        self.send(ajax_param)

    def DELETE(self, *url_args, **parameters):
        _headers = dict(**self._headers)
        _datatype = parameters.get("datatype", "json")
        _url_vars = parameters.get("url_vars", None)
        _complete = parameters.get("complete", None)
        _crossDomain = parameters.get("crossDomain", True)
        _error = parameters.get("error", None)
        _success = parameters.get("success", None)
        _user_headers = parameters.get("headers", {})
        for x in _user_headers.keys():
            _headers[x] = _user_headers[x]
        _all_args = self._process_args(url_args)
        _all_vars = self._serialize_vars(_url_vars)
        _current_uri = "/{0}{1}".format()
        _url = "{0}/{1}{2}".format(self.remote_address, _all_args, _all_vars)

        __pragma__('jsiter')
        ajax_param = {
            'url': _url,
            'type': "DELETE",
            'complete': lambda a, b, c: _complete(a, b, c),
            'success': _success,
            'error': _error,
            'datatype': _datatype,
            'crossDomain': _crossDomain,
            'headers': _headers
        }
        client_token = window.PhanterPWA.get_client_token()
        authorization = window.PhanterPWA.get_authorization()
        if client_token is not None:
            ajax_param['headers']['phanterpwa-client-token'] = client_token
        if authorization is not None:
            ajax_param['headers']['phanterpwa-authorization'] = authorization

        __pragma__('nojsiter')
        self.send(ajax_param)

    def POST(self, *url_args, **parameters):
        _headers = dict(**self._headers)
        _datatype = parameters.get("datatype", "json")
        _url_vars = parameters.get("url_vars", None)
        _complete = parameters.get("complete", None)
        _form_data = parameters.get("form_data", None)
        _crossDomain = parameters.get("crossDomain", True)
        _error = parameters.get("error", None)
        _success = parameters.get("success", None)
        _user_headers = parameters.get("headers", {})
        for x in _user_headers.keys():
            _headers[x] = _user_headers[x]
        _all_args = self._process_args(url_args)
        _all_vars = self._serialize_vars(_url_vars)
        _url = "{0}/{1}{2}".format(self.remote_address, _all_args, _all_vars)

        __pragma__('jsiter')
        ajax_param = {
            'url': _url,
            'type': "POST",
            'data': _form_data,
            'complete': lambda a, b, c: _complete(a, b, c),
            'success': _success,
            'error': _error,
            'datatype': _datatype,
            'crossDomain': _crossDomain,
            'headers': _headers
        }
        client_token = window.PhanterPWA.get_client_token()
        authorization = window.PhanterPWA.get_authorization()
        if client_token is not None:
            ajax_param['headers']['phanterpwa-client-token'] = client_token
        if authorization is not None:
            ajax_param['headers']['phanterpwa-authorization'] = authorization
        ISTYPEOF = __pragma__("js", "{}", "form_data instanceof FormData")
        if ISTYPEOF:
            ajax_param['processData'] = False
            ajax_param['contentType'] = False
        __pragma__('nojsiter')
        self.send(ajax_param)

    def PUT(self, *url_args, **parameters):
        _headers = dict(**self._headers)
        _datatype = parameters.get("datatype", "json")
        _url_vars = parameters.get("url_vars", None)
        _complete = parameters.get("complete", None)
        _form_data = parameters.get("form_data", None)
        _crossDomain = parameters.get("crossDomain", True)
        _error = parameters.get("error", None)
        _success = parameters.get("success", None)
        _user_headers = parameters.get("headers", {})
        for x in _user_headers.keys():
            _headers[x] = _user_headers[x]
        _all_args = self._process_args(url_args)
        _all_vars = self._serialize_vars(_url_vars)
        _url = "{0}/{1}{2}".format(self.remote_address, _all_args, _all_vars)

        __pragma__('jsiter')
        ajax_param = {
            'url': _url,
            'type': "PUT",
            'data': _form_data,
            'complete': lambda a, b, c: _complete(a, b, c),
            'success': _success,
            'error': _error,
            'datatype': _datatype,
            'crossDomain': _crossDomain,
            'headers': _headers
        }
        client_token = window.PhanterPWA.get_client_token()
        authorization = window.PhanterPWA.get_authorization()
        if client_token is not None:
            ajax_param['headers']['phanterpwa-client-token'] = client_token
        if authorization is not None:
            ajax_param['headers']['phanterpwa-authorization'] = authorization
        ISTYPEOF = __pragma__("js", "{}", "form_data instanceof FormData")
        if ISTYPEOF:
            ajax_param['processData'] = False
            ajax_param['contentType'] = False
        __pragma__('nojsiter')
        self.send(ajax_param)

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
