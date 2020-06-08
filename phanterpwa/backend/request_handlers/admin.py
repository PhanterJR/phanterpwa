import json
import hashlib
from phanterpwa.backend.decorators import (
    requires_authentication
)
from phanterpwa.i18n import browser_language
from tornado import (
    web
)


class UserManager(web.RequestHandler):
    """
        url: '/api/admin/usermanager/<id_user>'
    """

    def initialize(self, app_name, projectConfig, DALDatabase, i18nTranslator=None, logger_api=None):
        self.app_name = app_name
        self.projectConfig = projectConfig
        self.DALDatabase = DALDatabase
        self.i18nTranslator = i18nTranslator
        if logger_api:
            self.logger_api = logger_api
        if i18nTranslator:
            self.T = i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "phanterpwa-authorization,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language
        self.phanterpwa_user_agent = str(self.request.headers.get('User-Agent'))
        self.phanterpwa_remote_ip = str(self.request.remote_ip)

    def check_origin(self, origin):
        return True

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})

    @requires_authentication(roles_name="root")
    def get(self, *args, **kargs):
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        id_user = args[0]
        if id_user:
            return self.write({
                "status": 200,
                "message": "Hello world!"
            })
        else:
            limit = 100
            p_inicial = 0
            search = dict_arguments.get("search", "")
            search_field = dict_arguments.get("field", "id")
            orderby = dict_arguments.get("orderby", "id")
            sort = dict_arguments.get("sort", "asc")
            page = dict_arguments.get("page", "1")
            order_list = ["id", "first_name", "last_name", "email",
                "permit_mult_login", "activated", "websocket_opened"]
            if orderby in order_list:
                _orderby = self.DALDatabase.auth_user[orderby]
            else:
                _orderby = self.DALDatabase.auth_user.id

            if sort == "desc":
                _orderby = ~_orderby

            query = self.DALDatabase.auth_user
            msg = "Lista de Usuários"
            if search and search_field:
                if search_field in ["first_name", "last_name", "email"]:
                    msg = "Search by \"{0}\" on \"{1}\"".format(search, search_field)
                    query = self.DALDatabase.socios.nome_completo_normalizado.contains(text_normalize(search))
                elif search_field in order_list:
                    query = self.DALDatabase.socios[search_field] == search
            t_users = self.DALDatabase(query).count()
            displayed_records = t_users
            if t_users > limit:
                displayed_records = limit

            if (t_users % limit) == 0:
                total_pages = t_users / limit
            else:
                total_pages = (t_users // limit) + 1

            if page.isdigit():
                page = int(page)
                if page > 1:
                    if page > total_pages:
                        page = total_pages

                    p_inicial = (page - 1) * limit
            else:
                page = 1

            q_users = self.DALDatabase(query).select(
                *[self.DALDatabase.auth_user[x] for x in order_list],
                orderby=_orderby, limitby=(p_inicial, p_inicial + limit)
            )

            users = {
                'searcher': {
                    'search': search,
                    'page': page,
                    'total_pages': total_pages,
                    'total_records': t_users,
                    'displayed_records': displayed_records,
                    'field': search_field,
                    'sort_by': orderby,
                    'sort_order': sort,
                    'data_set': [
                        ["id", "ID"],
                        ["first_name", "First Name"],
                        ["last_name", "Last Name"],
                        ['email', "E-mail"],
                        ["permit_mult_login", "Allows Multiple Logins"],
                        ["activated", "Activated"],
                        ["websocket_opened", "Online"]
                    ],
                    'sortable': order_list
                },
                'search_fields': {
                    'label': "Campos de pesquisa",
                    'value': search_field,
                    'data_set': [
                        ["id", "ID"],
                        ["first_name", "First Name"],
                        ["last_name", "Last Name"],
                        ['email', "E-mail"],
                        ["permit_mult_login", "Allows Multiple Logins"],
                        ["activated", "Activated"],
                        ["websocket_opened", "Online"]
                    ]
                },
                'vars': dict_arguments
            }

            if q_users:
                users['data'] = json.loads(q_users.as_json())
            else:
                msg = "Não foi localizado nenhum registro"

        to_write = {
            "status": "OK",
            "uri": self.request.uri,
            "code": 200,
            "message": msg,
            "users": users if users else None
        }
        md5 = hashlib.md5()
        md5.update(str(to_write).encode("utf-8"))
        md5 = md5.hexdigest()
        to_write["hash"] = md5
        self.set_status(200)
        return self.write(to_write)
