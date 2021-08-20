import os
import re
import ast
import json
import hashlib
from phanterpwa.backend.decorators import (
    requires_authentication,
    check_private_csrf_token
)

from pydal.objects import (
    Field
)
from pydal.validators import (
    IS_EMAIL,
    IS_NOT_EMPTY,
    IS_NOT_IN_DB
)
from phanterpwa.i18n import browser_language
from tornado import (
    web
)
from phanterpwa.tools import (
    generate_activation_code,
    checkbox_bool,
    string_escape as E
)
from phanterpwa.backend.dataforms import (
    FieldsDALValidateDictArgs,
    datetime_converter,
    FormFromTableDAL as jsonForm
)

from phanterpwa.backend.request_handlers.auth import (
    arbritary_login
)
from phanterpwa.gallery.cutter import PhanterpwaGalleryCutter
from phanterpwa.gallery.integrationDAL import PhanterpwaGalleryUserImage
new_group_re = re.compile(r"\$[0-9]{13}\:(.{0,})")


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
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, PUT, DELETE')
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

    @check_private_csrf_token(form_identify=["phanterpwa-form-auth_user"])
    @requires_authentication(roles_name="root")
    def put(self, *args, **kargs):
        db = self.DALDatabase
        id_user = args[0]
        q_user = db(db.auth_user.id == id_user).select()
        if not q_user:
            message = "The id user not exist."
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': message,
                'i18n': {
                    'message': self.T(message)
                }
            })
        else:
            q_user = q_user.first()
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        dict_arguments['id'] = id_user
        first_name = dict_arguments['first_name']
        last_name = dict_arguments['last_name']
        email_now = q_user.email
        new_email = dict_arguments['email']
        two_factor = checkbox_bool(dict_arguments.get('two_factor', False))
        multiple_login = checkbox_bool(dict_arguments.get('permit_mult_login', False))
        activated = checkbox_bool(dict_arguments.get('activated', False))

        db.auth_user.email.requires = [IS_EMAIL()]
        table = db.auth_user
        result = FieldsDALValidateDictArgs(
            dict_arguments,
            *[table[x] for x in table.fields if x in ["first_name", "last_name"]],
            table["email"] if new_email != email_now else None
        )
        r = result.validate()
        if r:
            message = 'The form has errors'
            i18n_errors = {}
            for x in result.errors:
                tran = self.T(result.errors[x])
                i18n_errors[x] = tran
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': message,
                'errors': result.errors,
                'i18n': {
                    'message': self.T(message),
                    'errors': i18n_errors
                }
            })
        else:
            if dict_arguments["auth_group"]:
                try:
                    auth_group = ast.literal_eval(json.loads(dict_arguments["auth_group"]))
                except Exception:
                    auth_group = ast.literal_eval(dict_arguments["auth_group"])
                if isinstance(auth_group, list):
                    ids_groups = []
                    for x in auth_group:
                        role = None
                        if new_group_re.match(x):
                            role = new_group_re.findall(x)[0]
                            q_group = db(db.auth_group.role == role).select()
                            if q_group:
                                ids_groups.append(q_group.first().id)
                            else:
                                id_new_group = db.auth_group.insert(
                                    role=role,
                                    grade=2
                                )
                                ids_groups.append(id_new_group)
                        elif str(x).isdigit():
                            ids_groups.append(int(x))
                    if ids_groups:
                        db(
                            (db.auth_membership.auth_user == id_user) &
                            (~db.auth_membership.auth_group.belongs(ids_groups))
                        ).delete()
                        q_auth_membership = db(
                            (db.auth_membership.auth_user == id_user) &
                            (db.auth_membership.auth_group.belongs(ids_groups))
                        ).select()
                        novos_dependentes = set(ids_groups).difference(set([x.auth_group for x in q_auth_membership]))
                        for x in novos_dependentes:
                            db.auth_membership.insert(
                                auth_user=id_user,
                                auth_group=x
                            )
                    else:
                        db(
                            (db.auth_membership.auth_user == id_user)
                        ).delete()
                    db.commit()

            email_change = False
            first_name_change = False
            last_name_change = False
            image_change = False
            two_factor_change = False
            multiple_login_change = False
            activated_change = False

            if(first_name != q_user.first_name):
                q_user.update_record(first_name=first_name)
                first_name_change = True

            if(last_name != q_user.last_name):
                q_user.update_record(last_name=last_name)
                last_name_change = True

            if(two_factor != q_user.two_factor_login):
                q_user.update_record(two_factor_login=two_factor)
                two_factor_change = True

            if(multiple_login != q_user.permit_mult_login):
                q_user.update_record(permit_mult_login=multiple_login)
                multiple_login_change = True

            if(activated != q_user.activated):
                q_user.update_record(activated=activated)
                activated_change = True


            if self.request.files and\
                "phanterpwa-gallery-file-input" in self.request.files:
                imageBytes = self.request.files["phanterpwa-gallery-file-input"][0]['body']
                filename = self.request.files["phanterpwa-gallery-file-input"][0]['filename']
                cutterSizeX = dict_arguments['phanterpwa-gallery-input-cutterSizeX']
                cutterSizeY = dict_arguments['phanterpwa-gallery-input-cutterSizeY']
                cut_file = PhanterpwaGalleryCutter(
                    imageName=filename,
                    imageBytes=imageBytes,
                    cutterSizeX=cutterSizeX,
                    cutterSizeY=cutterSizeY
                )
                if 'phanterpwa-gallery-input-autoCut' in dict_arguments and\
                    dict_arguments['phanterpwa-gallery-input-autoCut']:
                    cutedImage = cut_file.auto_cut()
                else:
                    positionX = dict_arguments['phanterpwa-gallery-input-positionX']
                    positionY = dict_arguments['phanterpwa-gallery-input-positionY']
                    newSizeX = dict_arguments['phanterpwa-gallery-input-newSizeX']
                    newSizeY = dict_arguments['phanterpwa-gallery-input-newSizeY']
                    cutedImage = cut_file.specific_cut(
                        newSizeX=newSizeX,
                        newSizeY=newSizeY,
                        positionX=positionX,
                        positionY=positionY
                    )
                upload_image = PhanterpwaGalleryUserImage(
                    id_user,
                    self.DALDatabase,
                    self.projectConfig
                )
                image_change = upload_image.set_image(
                    *cutedImage
                )
            activate = q_user.activated
            if new_email != email_now:
                activation_code = generate_activation_code()
                self.Translator_email.direct_translation = self.phanterpwa_language
                keys_formatter = dict(
                    app_name=self.projectConfig['PROJECT']['name'],
                    user_name="{0} {1}".format(
                        first_name,
                        last_name
                    ),
                    code=activation_code,
                    time_expires=humanize_seconds(
                        self.projectConfig['BACKEND'][self.app_name]['default_time_activation_code_expire'],
                        self.Translator_email
                    ),
                    copyright=interpolate(self.projectConfig['CONTENT_EMAILS']['copyright'], {'now': datetime.now().year}),
                    link_to_your_page=self.projectConfig['CONTENT_EMAILS']['link_to_your_site']
                )
                email_password.text.formatter(keys_formatter)
                text_email = email_activation_code.text.html(
                    minify=True,
                    translate=True,
                    formatter=keys_formatter,
                    i18nInstance=self.Translator_email,
                    dictionary=self.phanterpwa_language,
                    do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                    escape_string=False
                )
                html_email = email_activation_code.html.html(
                    minify=True,
                    translate=True,
                    formatter=keys_formatter,
                    i18nInstance=self.Translator_email,
                    dictionary=self.phanterpwa_language,
                    do_not_translate=["\n", " ", "\n\n", "&nbsp;"],
                    escape_string=False
                )

                e_mail = MailSender(
                    self.projectConfig['EMAIL']['default_sender'],
                    self.projectConfig['EMAIL']['password'],
                    new_email,
                    subject="Activation code",
                    text_mensage=text_email,
                    html_mensage=html_email,
                    server=self.projectConfig['EMAIL']['server'],
                    port=self.projectConfig['EMAIL']['port'],
                    use_tls=self.projectConfig['EMAIL']['use_tls'],
                    use_ssl=self.projectConfig['EMAIL']['use_ssl']
                )
                result = ""
                try:
                    if self.projectConfig["PROJECT"]["debug"]:
                        self.logger_api.warning("ACTIVATION CODE: {0}".format(activation_code))
                    else:
                        self.logger_api.warning("Email from '{0}' to '{1}' -> Activation Code: {2}".format(
                            self.projectConfig['EMAIL']['default_sender'],
                            new_email,
                            activation_code
                        ))
                        e_mail.send()
                except Exception as e:
                    result = "Email from '{0}' to '{1}' don't send! -> Error: {2} -> password: {3}".format(
                        self.projectConfig['EMAIL']['default_sender'], dict_arguments['email'], e, activation_code)
                    self.logger_api.error(result, exc_info=True)
                    message = "There was an error trying to send the email."
                    message_i18n = self.T("There was an error trying to send the email.")
                    self.DALDatabase.rollback()
                    self.set_status(400)
                    return self.write({
                        'status': 'Bad Request',
                        'code': 400,
                        'message': message,
                        'i18n': {'message': message_i18n}
                    })
                else:
                    q_user.update_record(
                        activation_code=activation_code.split("-")[0],
                        timeout_to_resend_activation_email=datetime.now() +
                            timedelta(seconds=self.projectConfig['BACKEND'][self.app_name]['default_time_activation_code_expire'])
                    )
                    activate = False
                    q_user.update_record(email=new_email, activated=activate)
                    q_list = self.DALDatabase(
                        (self.DALDatabase.email_user_list.auth_user == id_user) &
                        (self.DALDatabase.email_user_list.email == email_now)
                    ).select().first()
                    if q_list:
                        q_list.update_record(
                            datetime_changed=datetime.now()
                        )
                    else:
                        self.DALDatabase.email_user_list.insert(
                            auth_user=id_user,
                            email=email_now
                        )
                    email_change = True

            q_role = self.DALDatabase(
                (self.DALDatabase.auth_membership.auth_user == id_user) &
                (self.DALDatabase.auth_group.id == self.DALDatabase.auth_membership.auth_group)
            ).select(
                self.DALDatabase.auth_group.id, self.DALDatabase.auth_group.role, orderby=self.DALDatabase.auth_group.grade
            )
            roles = [x.role for x in q_role]
            dict_roles = {x.id: x.role for x in q_role}
            roles_id = [x.id for x in q_role]
            role = None
            if roles:
                role = roles[-1]
            q_client = self.DALDatabase(
                (self.DALDatabase.client.auth_user == id_user)
            ).delete()
            self.DALDatabase.commit()
            user_image = PhanterpwaGalleryUserImage(id_user, self.DALDatabase, self.projectConfig)
            self.set_status(200)
            return self.write({
                'status': 'OK',
                'code': 200,
                'message': 'Account was successfully changed',
                'auth_user': {
                    'id': str(id_user),
                    'first_name': E(first_name),
                    'last_name': E(last_name),
                    'email': new_email,
                    'remember_me': False,
                    'roles': roles,
                    'role': role,
                    'dict_roles': dict_roles,
                    'roles_id': roles_id,
                    'activated': activate,
                    'image': user_image.id_image,
                    'two_factor': q_user.two_factor_login,
                    'multiple_login': q_user.permit_mult_login,
                    'locale': q_user.locale,
                    'social_login': None
                },
                'i18n': {
                    'message': self.T('Account was successfully changed'),
                    'auth_user': {'role': self.T(role)}
                }
            })

    @requires_authentication(roles_name="root")
    def delete(self, *args, **kargs):
        db = self.DALDatabase
        id_user = args[0]
        q_user = db(db.auth_user.id == id_user).select().first()
        if not q_user:
            message = "The id user not exist."
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': message,
                'i18n': {
                    'message': self.T(message)
                }
            })
        else:
            db(db.auth_user.id == q_user.id).delete()
            db.commit()
            self.set_status(200)
            return self.write({
                'status': 'OK',
                'code': 200,
                'message': 'The account was successfully deleted',
                'i18n': {
                    'message': self.T('The account was successfully deleted'),
                }
            })


    def options(self, *args):
        self.set_status(200)
        self.write({
            "status": "OK",
        })


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
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT')
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
        action = args[1]
        db = self.DALDatabase

        if id_group:
            if id_group == "new":
                msg = "New Role"

                json_form = jsonForm(db.auth_group)
                auth_group = db(
                    (db.auth_group.role == "user")
                ).select(db.auth_group.ALL)
                json_form = json_form.as_dict()
                to_write = {
                    "status": "OK",
                    "code": 200,
                    "message": msg,
                    "data": {
                        "auth_role": json_form
                    }
                }
                md5 = hashlib.md5()
                md5.update(str(to_write).encode("utf-8"))
                md5 = md5.hexdigest()
                to_write["hash"] = md5
                return self.write(to_write)
            elif action == "edit" or action == "view":
                q_auth_role = db(db.auth_group.id == id_group).select(db.auth_group.id).first()
                if q_auth_role:
                    msg = "Role (id:{0})".format(id_group)
                    json_form = jsonForm(db.auth_group, q_auth_role.id)
                    auth_group = db(
                        (db.auth_membership.auth_group== id_group) &
                        (db.auth_group.id == db.auth_membership.auth_group)
                    ).select(db.auth_group.ALL)
                    json_form = json_form.as_dict()

                    to_write = {
                        "status": "OK",
                        "code": 200,
                        "message": msg,
                        "data": {
                            "auth_role": json_form
                        }
                    }
                    md5 = hashlib.md5()
                    md5.update(str(to_write).encode("utf-8"))
                    md5 = md5.hexdigest()
                    to_write["hash"] = md5
                    return self.write(to_write)
                else:
                    msg = "Role not found"
                    self.set_status(404)
                    return self.write({
                        "status": "Not Found",
                        "code": 404,
                        "message": msg,
                        "auth_role": None
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


    @check_private_csrf_token(form_identify=["phanterpwa-form-auth_group"])
    @requires_authentication(roles_name="root")
    def post(self, *args, **kargs):
        db = self.DALDatabase

        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        grade = dict_arguments.get("grade", 0)
        grade_error = None
        if str(grade).isdigit() and int(grade) < 99:
            dict_arguments['grade'] = int(grade)
        else:
            grade_error = "The grade must be an integer and less than 99"


        db.auth_group.role.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.auth_group.role)]
        table = db.auth_group
        result = FieldsDALValidateDictArgs(
            dict_arguments,
            *[table[x] for x in table.fields]
        )
        r = result.validate()
        if r or grade_error:
            if r and grade_error:
                result.errors["grade"] = grade_error
                data_error = result.errors
            elif grade_error:
                data_error = {"grade": grade_error}
            else:
                data_error = result.errors

            i18n_errors = {}
            for x in data_error:
                tran = self.T(data_error[x])
                i18n_errors[x] = tran
            message = 'The form has errors'
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': message,
                'errors': data_error,
                'i18n': {
                    'message': self.T(message),
                    'errors': i18n_errors
                }
            })
        else:
            result.insert(table)
            q_role = db(db.auth_group.id == result.id).select().first()
            if q_role:
                self.set_status(200)
                db.commit()
                return self.write({
                    'status': 'OK',
                    'code': 200,
                    'message': 'Group was successfully changed',
                    'auth_group': {
                        'id': str(id_role),
                        'role': E(q_role.role),
                        'grade': q_role.grade,
                        'description': E(q_role.description)
                    },
                    'i18n': {
                        'message': self.T('Group was successfully changed'),
                        'auth_role': {'role': self.T(q_role.role)}
                    }
                })
        self.set_status(400)
        return self.write({
            'status': 'Bad Request',
            'code': 400,

        })


    @check_private_csrf_token(form_identify=["phanterpwa-form-auth_group"])
    @requires_authentication(roles_name="root")
    def put(self, *args, **kargs):
        db = self.DALDatabase
        id_role = args[0]
        q_role = db(db.auth_group.id == id_role).select()
        if not q_role:
            message = "The id role not exist."
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': message,
                'i18n': {
                    'message': self.T(message)
                }
            })
        else:
            q_role = q_role.first()
        dict_arguments = {k: self.request.arguments.get(k)[0].decode('utf-8') for k in self.request.arguments}
        dict_arguments['id'] = id_role

        table = db.auth_group
        result = FieldsDALValidateDictArgs(
            dict_arguments,
            *[table[x] for x in table.fields]
        )
        r = result.validate()
        if r:
            message = 'The form has errors'
            i18n_errors = {}
            for x in result.errors:
                tran = self.T(result.errors[x])
                i18n_errors[x] = tran
            self.set_status(400)
            return self.write({
                'status': 'Bad Request',
                'code': 400,
                'message': message,
                'errors': result.errors,
                'i18n': {
                    'message': self.T(message),
                    'errors': i18n_errors
                }
            })
        else:
            q_role = db(db.auth_group.id == id_role).select().first()
            result.update(table, q_role.id)
            self.set_status(200)
            return self.write({
                'status': 'OK',
                'code': 200,
                'message': 'Group was successfully changed',
                'auth_group': {
                    'id': str(id_role),
                    'role': E(q_role.role),
                    'grade': q_role.grade,
                    'description': E(q_role.description)
                },
                'i18n': {
                    'message': self.T('Group was successfully changed'),
                    'auth_role': {'role': self.T(q_role.role)}
                }
            })


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
