import os
import json
import hashlib
from phanterpwa.backend.decorators import (
    requires_authentication
)
from pydal.objects import (
    Field
)
from phanterpwa.i18n import browser_language
from tornado import (
    web
)
from phanterpwa.tools import (
    checkbox_bool
)
from phanterpwa.backend.dataforms import (
    datetime_converter,
    FormFromTableDAL as jsonForm
)

from phanterpwa.backend.request_handlers.auth import (
    arbritary_login
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
        action = args[1]
        db = self.DALDatabase
        remote_adress = self.projectConfig["BACKEND"]["api"]["http_address"]
        if id_user:
            if id_user == "new":
                msg = "New User"

                json_form = jsonForm(db.auth_user)
                json_form.add_extra_field(
                    Field('foto3x4', phanterpwa={
                        'type': 'image',
                        'position': 0,
                        'url': lambda row: "{0}/api/socios/{1}/image/".format(
                            remote_adress,
                            row.id
                        ),
                        'cutter': True,
                        'no-cache': True,
                    'group': 'group1',
                        '_class': 'p-col w1p100 w4p30'
                    })
                )
                auth_group = db(
                    (db.auth_group.role == "user")
                ).select(db.auth_group.ALL)
                json_form.add_extra_field(
                    Field('auth_group', label="Roles", phanterpwa={
                            "value": [
                                [x.id, "{0} - {1}".format(
                                    x.grade, x.role)] for x in auth_group
                            ],
                            "data_set": [
                                [x.id, "{0} - {1}".format(
                                    x.grade, x.role)] for x in db(db.auth_group).select(db.auth_group.ALL)
                            ],
                            "form": "auth_user",
                            "type": 'list_string',
                            "section": "List of user roles ",
                            "_class": "p-col w1p100"
                    })
                )
                json_form = json_form.as_dict()
                insert_widget = [
                    "widget",
                    [
                        "auth_group",
                        {
                            "label": "Roles",
                            "name": "auth_group",
                            "value": [],
                            "form": "auth_user",
                            "type": 'list_string',
                            "_class": "p-col w1p100"
                        }
                    ]
                ]
                # json_form["widgets"].append(insert_widget)
                to_write = {
                    "status": "OK",
                    "code": 200,
                    "message": msg,
                    "data": {
                        "auth_user": json_form
                    }
                }
                md5 = hashlib.md5()
                md5.update(str(to_write).encode("utf-8"))
                md5 = md5.hexdigest()
                to_write["hash"] = md5
                return self.write(to_write)
            elif action == "edit" or action == "view":
                q_auth_user = db(db.auth_user.id == id_user).select(db.auth_user.id).first()
                q_gallery = db(db.auth_user_phanterpwagallery.auth_user == id_user).select().first()
                if q_auth_user:
                    msg = "User (id:{0})".format(id_user)
                    json_form = jsonForm(db.auth_user, q_auth_user.id)
                    json_form.add_extra_field(
                        Field('foto3x4', phanterpwa={
                            'type': 'image',
                            'position': 0,
                            'url': lambda row: "{0}/api/admin/usermanager/{1}/image/".format(
                                remote_adress,
                                row.id
                            ),
                            'cutter': True,
                            'no-cache': True,
                        'group': 'group1',
                            '_class': 'p-col w1p100 w4p30'
                        })
                    )
                    auth_group = db(
                        (db.auth_membership.auth_user == id_user) &
                        (db.auth_group.id == db.auth_membership.auth_group)
                    ).select(db.auth_group.ALL)
                    json_form.add_extra_field(
                        Field('auth_group', label="Roles", phanterpwa={
                                "value": [
                                    [x.id, "{0} - {1}".format(
                                        x.grade, x.role)] for x in auth_group
                                ],
                                "data_set": [
                                    [x.id, "{0} - {1}".format(
                                        x.grade, x.role)] for x in db(db.auth_group).select(db.auth_group.ALL)
                                ],
                                "form": "auth_user",
                                "type": 'list_string',
                                "section": "List of user roles ",
                                "_class": "p-col w1p100"
                        })
                    )
                    json_form = json_form.as_dict()

                    to_write = {
                        "status": "OK",
                        "code": 200,
                        "message": msg,
                        "data": {
                            "gallery": json.loads(q_gallery.as_json()) if q_gallery else None,
                            "auth_user": json_form
                        }
                    }
                    md5 = hashlib.md5()
                    md5.update(str(to_write).encode("utf-8"))
                    md5 = md5.hexdigest()
                    to_write["hash"] = md5
                    return self.write(to_write)
                else:
                    msg = "User not found"
                    self.set_status(404)
                    return self.write({
                        "status": "Not Found",
                        "code": 404,
                        "message": msg,
                        "auth_user": None
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
                _orderby = db.auth_user[orderby]
            else:
                _orderby = db.auth_user.id

            if sort == "desc":
                _orderby = ~_orderby

            query = db.auth_user
            msg = "Users"
            if search and search_field:
                msg = "Search by \"{0}\" on \"{1}\"".format(search, search_field)
                if search_field in ["first_name", "last_name", "email"]:
                    query = db.auth_user[search_field].contains(search)
                elif search_field in ["activated", "permit_mult_login", "websocket_opened"]:
                    query = db.auth_user[search_field] == checkbox_bool(search)
                elif search_field in ["id", "grade"] and search.isdigit():
                    query = db.auth_group[search_field] == int(search)
                elif search_field in order_list:
                    query = db.auth_user[search_field] == search
            t_users = db(query).count()
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

            q_users = db(query).select(
                *[db.auth_user[x] for x in order_list],
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
                    'label': "Search fields",
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
                msg = "No record found"

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


class UserImage(web.RequestHandler):
    """
        url: '/api/admin/usermanager/<id_socio>/image/'
    """

    def initialize(self, *args, **kargs):
        self.app_name = kargs.get("app_name", None)
        self.projectConfig = kargs.get("projectConfig", None)
        self.DALDatabase = kargs.get("DALDatabase", None)
        self.i18nTranslator = kargs.get("i18nTranslator", None)
        logger_api = kargs.get("logger_api", None)
        if logger_api:
            self.logger_api = logger_api
        if self.i18nTranslator:
            self.T = self.i18nTranslator.T
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "".join([
                "phanterpwa-language,",
                "phanterpwa-application,",
                "phanterpwa-application-version,",
                "phanterpwa-client-token,",
                "cache-control"
            ])
        )
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        if self.request.headers.get("phanterpwa-language"):
            self.phanterpwa_language = self.request.headers.get("phanterpwa-language")
        else:
            self.phanterpwa_language = browser_language(self.request.headers.get("Accept-Language"))
        if self.i18nTranslator:
            self.i18nTranslator.direct_translation = self.phanterpwa_language

    def check_origin(self, origin):
        return True

    def options(self, *args):
        self.set_status(200)
        return self.write({"status": "OK"})

    #@check_url_token()
    def get(self, *args, **kargs):
        db = self.DALDatabase
        projectConfig = self.projectConfig
        """
        Receive request to create and response with a token csrf or captcha
        """
        id_user = args[0]

        buf_size = 512
        q_image = db(
            (db.auth_user_phanterpwagallery.phanterpwagallery == db.phanterpwagallery.id)
            & (db.auth_user_phanterpwagallery.auth_user == id_user)
        ).select(
            db.phanterpwagallery.folder,
            db.phanterpwagallery.alias_name,
            db.phanterpwagallery.filename
        ).last()
        if q_image:
            file = os.path.join(projectConfig['PROJECT']['path'],
                    'backapps', 'api', 'uploads', q_image.folder,
                        q_image.alias_name)
            self.set_header(
                'Content-Disposition', 'attachment; filename="{0}"'.format(
                    q_image.filename)
            )
            if os.path.isfile(file):
                self.set_status(200)
                with open(file, 'rb') as f:
                    while True:
                        data = f.read(buf_size)
                        if not data:
                            break
                        self.write(data)
                self.finish()
                return
        self.set_status(202)
        file = os.path.join(self.projectConfig['PROJECT']['path'],
                "backapps", self.app_name, 'statics', 'images', 'user.png')
        with open(file, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        self.finish()
        return


class RoleManager(web.RequestHandler):
    """
        url: '/api/admin/rolemanager/<id_role>'
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
        id_group = args[0]
        db = self.DALDatabase
        if id_group:
            return self.write({
                "status": 200,
                "message": "Hello world!"
            })
        else:
            limit = 100
            p_inicial = 0
            search = dict_arguments.get("search", "")
            search_field = dict_arguments.get("field", "grade")
            orderby = dict_arguments.get("orderby", "grade")
            sort = dict_arguments.get("sort", "asc")
            page = dict_arguments.get("page", "1")
            order_list = ["id", "grade", "role", "description"]

            if orderby in order_list:
                _orderby = db.auth_group[orderby]
            else:
                _orderby = db.auth_group.id

            if sort == "desc":
                _orderby = ~_orderby

            query = db.auth_group
            msg = "Roles"
            if search and search_field and (search_field in order_list):
                msg = "Search by \"{0}\" on \"{1}\"".format(search, search_field)
                if search_field in ["role", "description"]:
                    query = db.auth_group[search_field].contains(search)
                elif search_field in ["id", "grade"] and search.isdigit():
                    query = db.auth_group[search_field] == int(search)

            t_groups = db(query).count()
            displayed_records = t_groups
            if t_groups > limit:
                displayed_records = limit

            if (t_groups % limit) == 0:
                total_pages = t_groups / limit
            else:
                total_pages = (t_groups // limit) + 1

            if page.isdigit():
                page = int(page)
                if page > 1:
                    if page > total_pages:
                        page = total_pages

                    p_inicial = (page - 1) * limit
            else:
                page = 1

            q_groups = db(query).select(
                *[db.auth_group[x] for x in order_list],
                orderby=_orderby, limitby=(p_inicial, p_inicial + limit)
            )

            groups = {
                'searcher': {
                    'search': search,
                    'page': page,
                    'total_pages': total_pages,
                    'total_records': t_groups,
                    'displayed_records': displayed_records,
                    'field': search_field,
                    'sort_by': orderby,
                    'sort_order': sort,
                    'data_set': [
                        ["id", "ID"],
                        ["grade", "Grade"],
                        ["role", "Role"],
                        ["description", "Description"]
                    ],
                    'sortable': order_list
                },
                'search_fields': {
                    'label': "Search fields",
                    'value': search_field,
                    'data_set': [
                        ["id", "ID"],
                        ["grade", "Grade"],
                        ["role", "Role"],
                        ["description", "Description"]
                    ]
                },
                'vars': dict_arguments
            }

            if q_groups:
                groups['data'] = json.loads(q_groups.as_json())
            else:
                msg = "No record found"

        to_write = {
            "status": "OK",
            "uri": self.request.uri,
            "code": 200,
            "message": msg,
            "groups": groups if groups else None
        }
        md5 = hashlib.md5()
        md5.update(str(to_write).encode("utf-8"))
        md5 = md5.hexdigest()
        to_write["hash"] = md5
        self.set_status(200)
        return self.write(to_write)


class Impersonate(web.RequestHandler):
    """
        url: '/api/admin/impersonate/<id_role>'
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
        self.phanterpwa_remote_ip = self.request.headers.get("X-Real-IP") or \
            self.request.headers.get("X-Forwarded-For") or \
            self.request.remote_ip

    def check_origin(self, origin):
        return True

    def options(self, *args):
        self.set_status(200)
        self.write({"status": "OK"})

    @requires_authentication(roles_name="root")
    def get(self, *args, **kargs):
        id_user = args[0]
        db = self.DALDatabase
        q_user = db(db.auth_user.id == id_user).select()
        if q_user:
            email = q_user.first().email
            result = arbritary_login(
                self.app_name,
                self.projectConfig,
                db,
                email,
                self.phanterpwa_user_agent,
                self.request.remote_ip,
                self.phanterpwa_client_token
            )
            if result:
                self.set_status(200)
                self.write(result)
