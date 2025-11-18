import json
import hashlib
from typing import List, Any, Dict
from tornado import (
    web
)
from ..security import (
    Serialize,
    SignatureExpired,
    BadSignature,
    URLSafeSerializer,
)
from phanterpwa.tools import checkbox_bool
from phanterpwa.i18n import browser_language


class DotDict(dict):
    """
    Safe dictionary with attribute-style access, JSON compatible
    and recursive conversion of nested dicts.

    Examples:
        >>> obj = DotDict({"name": "John", "data": {"age": 30}})
        >>> obj.name  # "John"
        >>> obj.data.age  # 30
        >>> isinstance(obj, dict)  # True
        >>> json.dumps(obj)  # Works perfectly
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the dictionary and recursively convert nested dicts
        """
        super().__init__(*args, **kwargs)
        self._convert_nested_dicts()

    def _convert_nested_dicts(self) -> None:
        """
        Recursively convert all nested dicts to DotDict
        and process lists containing dicts
        """
        for key, value in self.items():
            if isinstance(value, dict) and not isinstance(value, DotDict):
                # Convert dict to DotDict
                self[key] = DotDict(value)
            elif isinstance(value, list):
                # Process list - convert dicts inside the list
                self[key] = self._process_list(value)

    def _process_list(self, lst: List) -> List:
        """
        Process a list converting dicts to DotDict
        """
        processed_list = []
        for item in lst:
            if isinstance(item, dict) and not isinstance(item, DotDict):
                processed_list.append(DotDict(item))
            elif isinstance(item, list):
                processed_list.append(self._process_list(item))
            else:
                processed_list.append(item)
        return processed_list

    def __getattr__(self, name: str) -> Any:
        """
        Allow attribute access: obj.name
        """
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Allow attribute assignment: obj.name = value
        """
        if isinstance(value, dict) and not isinstance(value, DotDict):
            value = DotDict(value)
        elif isinstance(value, list):
            value = self._process_list(value)

        self[name] = value

    def __delattr__(self, name: str) -> None:
        """
        Allow attribute deletion: del obj.name
        """
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def to_dict(self) -> Dict:
        """
        Recursively convert to normal dict - 100% safe for JSON

        Returns:
            Dict: Normal version of dictionary, without DotDict
        """
        result = {}
        for key, value in self.items():
            if isinstance(value, DotDict):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, DotDict) else item for item in value
                ]
            else:
                result[key] = value
        return result

    def copy(self) -> 'DotDict':
        """
        Return a deep copy of the object

        Returns:
            DotDict: Copy of the object
        """
        return DotDict(self.to_dict())

    def update(self, other: Dict = None, **kwargs) -> None:
        """
        Update dictionary with other values, converting nested dicts

        Args:
            other: Another dictionary to update
            **kwargs: Key-value pairs to update
        """
        if other:
            if isinstance(other, dict):
                for key, value in other.items():
                    self[key] = value
            else:
                for key, value in other:
                    self[key] = value

        for key, value in kwargs.items():
            self[key] = value

        # Reconvert nested dicts after update
        self._convert_nested_dicts()

    def get_path(self, path: str, default: Any = None) -> Any:
        """
        Access by path using dots: obj.get_path('user.data.age')

        Args:
            path: Dot path to access nested values
            default: Default value if path doesn't exist

        Returns:
            Any: Found value or default
        """
        keys = path.split('.')
        current = self

        for key in keys:
            if isinstance(current, (dict, DotDict)) and key in current:
                current = current[key]
            else:
                return default

        return current

    def set_path(self, path: str, value: Any) -> None:
        """
        Set value by path using dots: obj.set_path('user.data.age', 30)

        Args:
            path: Dot path to set the value
            value: Value to be set
        """
        keys = path.split('.')
        current = self

        # Navigate to the second to last level
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], (dict, DotDict)):
                current[key] = DotDict()
            current = current[key]

        # Set value at the last level
        current[keys[-1]] = value

    # Method for JSON compatibility
    def __json__(self) -> Dict:
        """
        Special method that json.dumps() automatically looks for
        """
        return self.to_dict()


class PhanterPWARequestHandler(web.RequestHandler):
    def initialize(self, app_name, projectConfig, DALDatabase, Redis=None, i18nTranslator=None, logger_api=None, AuthActivityNoRelational=None):
        self.app_name = app_name
        self.AuthActivityNoRelational = AuthActivityNoRelational
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.Redis = Redis
        self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T  # translator

        # CORS Headers
        self._set_cors_headers()
        self._final_response_on_success = None

        # Integrated authentication system
        self._initialize_authentication_system()
        self._initialize_csrf_system()

        # Process client headers
        self._process_client_headers()

        self.phanterpwa_redis_cache = checkbox_bool(self.request.headers.get("phanterpwa-redis-cache", True))
        self.dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        if self.Redis:
            if self.phanterpwa_redis_cache is False:
                self._redis_invalidate()

    def phanterpwa_current_user_has_role(self, role):
        if self.phanterpwa_current_user_groups:
            if isinstance(role, (list, tuple, set)):
                if isinstance(role, (list, tuple)):
                    role = set(role)
                auth_user_roles = set([x.role for x in self.phanterpwa_current_user_groups])
                if role.intersection(auth_user_roles):
                    return True
                else:
                    return False
            elif isinstance(role, str):
                return self.phanterpwa_current_user_has_role(set([role]))
        return False

    def _set_cors_headers(self):
        # CORS Headers
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-authorization,"
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-redis-cache,",
                "phanterpwa-client-token,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT, DELETE, PATCH, HEAD')

    def _initialize_authentication_system(self):
        """Initialize integrated authentication system"""
        # Tokens
        self.phanterpwa_client_token = None  # Client token
        self.phanterpwa_authorization = None  # Authentication token

        # database data
        self.phanterpwa_current_client = None  # db data client
        self.phanterpwa_current_user = None  # db data user
        self.phanterpwa_current_user_groups = None  # select user groups

        # Verification flags
        self.phanterpwa_client_application_checked = None
        self.phanterpwa_client_token_checked = None
        self.phanterpwa_authorization_checked = None
        self.phanterpwa_user_token_checked = None

    def _initialize_csrf_system(self):
        self.phanterpwa_csrf_token_content = None
        self.phanterpwa_csrf_token_record = None
        self.phanterpwa_form_identify = None

    def _process_client_headers(self):
        """Process PhanterPWA specific headers"""
        # Language
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))

        if hasattr(self, 'i18nTranslator'):
            self.i18nTranslator.direct_translation = self.phanterpwa_language

        # Client info
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip

        # Tokens
        self.phanterpwa_application = self.request.headers.get('phanterpwa-application')
        self.phanterpwa_application_version = self.request.headers.get('phanterpwa-application-version')
        self.phanterpwa_client_token = self.request.headers.get('phanterpwa-client-token')
        self.phanterpwa_authorization = self.request.headers.get('phanterpwa-authorization')

    async def GET(self, *args, **kwargs) -> DotDict:
        """GET with optional authentication verification"""
        # By default, doesn't require authentication
        # Specific handlers can override and call check_user_token() if necessary
        pass

    async def POST(self, *args, **kwargs) -> DotDict:
        """POST with optional verification"""
        pass

    async def PATCH(self, *args, **kwargs) -> DotDict:
        """PATCH with optional verification"""
        pass

    async def PUT(self, *args, **kwargs) -> DotDict:
        """PUT with optional verification"""
        pass

    async def DELETE(self, *args, **kwargs) -> DotDict:
        """DELETE with optional verification"""
        pass

    async def OPTIONS(self, *args, **kwargs):
        """OPTIONS for CORS"""
        self.set_status(204)

    async def HEAD(self, *args, **kwargs):
        """HEAD for verification"""
        self.set_status(200)

    async def get(self, *args, **kwargs):
        if self.Redis:
            cache_key = self._generate_cache_key()
            data = self._redis_load(cache_key)
            if data:
                if isinstance(data, (dict, DotDict)):  # ✅ Only add flag if it's JSON
                    data["redis"] = True
                    code = data.get("code", 200)
                    self.set_status(code)
                self._final_response_on_success = data
                self.write(data)
                self.finish()
                return

        data = await self.GET(*args, **kwargs)

        if isinstance(data, (dict, DotDict)):
            code = data.get("code", 200)
            if 200 <= code < 300 and self.Redis:
                cache_key = self._generate_cache_key()
                self._redis_save(cache_key, data, self.projectConfig['BACKEND'][self.app_name].get('default_cache_response_redis_expire', 86400))
            self.set_status(code)
            self.write(data)
        elif data:
            self.write(data)
        self._final_response_on_success = data

    async def post(self, *args, **kwargs):
        data = await self.POST(*args, **kwargs)
        if isinstance(data, (dict, DotDict)):
            code = data.get("code", 200)
            if 200 <= code < 300:
                self._redis_invalidate()
            self.set_status(code)
            self.write(data)
            self._final_response_on_success = data

    async def patch(self, *args, **kwargs):
        data = await self.PATCH(*args, **kwargs)
        if isinstance(data, (dict, DotDict)):
            code = data.get("code", 200)
            if 200 <= code < 300:
                self._redis_invalidate()
            self.set_status(code)
            self.write(data)
            self._final_response_on_success = data

    async def put(self, *args, **kwargs):
        data = await self.PUT(*args, **kwargs)
        if isinstance(data, (dict, DotDict)):
            code = data.get("code", 200)
            if 200 <= code < 300:
                self._redis_invalidate()
            self.set_status(code)
            self.write(data)
            self._final_response_on_success = data

    async def delete(self, *args, **kwargs):
        data = await self.DELETE(*args, **kwargs)
        if isinstance(data, (dict, DotDict)):
            code = data.get("code", 200)
            self.set_status(code)
            if 200 <= code < 300:
                self._redis_invalidate()
            self.write(data)
            self._final_response_on_success = data

    async def options(self, *args, **kwargs):
        self.OPTIONS(*args, **kwargs)

    async def head(self, *args, **kwargs):
        self.HEAD(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def _redis_save(self, key, data, expire=86400) -> bool:
        if self.Redis and self.phanterpwa_redis_cache:
            try:
                if isinstance(data, (bytes, bytearray)):
                    # file cache
                    if expire:
                        self.Redis.setex(key, expire, data)
                    else:
                        self.Redis.set(key, data)
                else:
                    # (DotDict, Dict)
                    data_json = json.dumps(data)
                    if expire:
                        self.Redis.setex(key, expire, data_json)
                    else:
                        self.Redis.set(key, data_json)

                return True
            except Exception as e:
                if self.logger_api:
                    self.logger_api.error(f"❌ Redis save error key({key}): {e}")
                else:
                    print(f"❌ Redis save error key({key}): {e}")
                return False
        return False

    def _redis_load(self, key) -> DotDict:
        if self.Redis and self.phanterpwa_redis_cache:
            try:
                data = self.Redis.get(key)
                if data is None:
                    return None
                try:
                    return DotDict(json.loads(data))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # its bytes - direct return
                    return data

            except Exception as e:
                if self.logger_api:
                    self.logger_api.error(f"❌ Redis load error key({key}): {e}")
                else:
                    print(f"❌ Redis load error key({key}): {e}")
                return None

    def _redis_invalidate(self):
        """Invalidate all cache of a group"""
        if self.Redis:
            pattern = f"phanterpwa:{self.app_name}:handler:{self.__class__.__name__}:*"
            keys = self.Redis.keys(pattern)
            if keys:
                self.Redis.delete(*keys)

    def _generate_cache_key(self) -> str:
        """
        Simplified version but still very effective
        """
        # Essential elements for uniqueness
        components = [
            self.request.method,
            self.request.path,
        ]

        if self.dict_arguments:
            args_list = []
            # Preserve iteration order of arguments (usually insertion order)
            for key in self.dict_arguments:
                value_str = self.dict_arguments[key]
                args_list.append((key, value_str))
            components.append(json.dumps(args_list, separators=(',', ':')))

        # User context (if authenticated)
        if hasattr(self, 'phanterpwa_current_user') and self.phanterpwa_current_user:
            components.append(f"user:{self.phanterpwa_current_user.id}")

        # Language context
        if hasattr(self, 'phanterpwa_language'):
            components.append(self.phanterpwa_language)
        hash_components = hashlib.md5(":".join(str(c) for c in components).encode()).hexdigest()
        key_string = f"phanterpwa:{self.app_name}:handler:{self.__class__.__name__}:{hash_components}"
        return key_string

    def _request_summary(self) -> str:
        client_ip = self.request.headers.get('X-Real-IP') or\
            self.request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or\
            self.request.remote_ip
        summary = "{0} {1} ({2})".format(
            self.request.method,
            self.request.uri,
            client_ip,
        )
        if hasattr(self, "phanterpwa_current_user") and self.phanterpwa_current_user is not None:
            summary = "{0} {1} ({2} - {3})".format(
                self.request.method,
                self.request.uri,
                client_ip,
                self.phanterpwa_current_user.email
            )
        return summary
