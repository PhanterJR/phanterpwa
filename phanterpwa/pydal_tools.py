import json
from phanterpwa.helpers import (
    FORM,
    DIV,
    I,
    INPUT,
    LABEL
)
from phanterpwa.xmlconstructor import (
    XmlConstructor
)
# from pydal import Field
from pydal.objects import (Set, Table, Field)
# from pydal.DAL import Table


class SubmitButton(XmlConstructor):
    def __init__(self, _id, label, **attributes):
        self.label = label
        initial_class = "phanterpwa-materialize-button-form-container"
        attributes["_id"] = _id
        self.button_attributes = attributes
        if "_class" in self.button_attributes:
            self.button_attributes["_class"] = " ".join([
                self.button_attributes['_class'].strip(),
                "btn phanterpwa-materialize-button-form link"])
        else:
            self.button_attributes["_class"] = "btn phanterpwa-materialize-button-form link"
        if "_title" not in self.button_attributes:
            if isinstance(self.label, str):
                self.button_attributes["_title"] = self.label

        XmlConstructor.__init__(self, 'div', False, _class=initial_class)
        self._update_content()

    def _update_content(self):
        attributes = self.button_attributes
        self.content = [
            DIV(
                DIV(self.label, **attributes),
                _class="button-form")
        ]


class CustomWidget():
    def __init__(self, name, label, _type, default=None, **phanterpwa):
        self.name = name
        self.label = label
        self.default = default
        self.type = _type
        self.phanterpwa = phanterpwa

    def as_dict(self):
        json_field = {
            'label': self.label,
            'default': self.default,
            'type': self.type
        }
        if self.phanterpwa:
            json_field["phanterpwa"] = self.phanterpwa
        return json_field

    def as_json(self, indent=2):
        return json.dumps(self.as_dict(), indent=indent)


class TextWidget(CustomWidget):
    def __init__(self, name, label, default=None, **phanterpwa):
        self.name = name
        self.label = label
        self.default = default
        self.type = 'string'
        self.phanterpwa = phanterpwa
        CustomWidget.__init__(
            self, name, label, "string", default, **phanterpwa)


class PasswordWidget(CustomWidget):
    def __init__(self, name, label, default=None, **phanterpwa):
        self.name = name
        self.label = label
        self.default = default
        self.type = 'password'
        self.phanterpwa = phanterpwa
        CustomWidget.__init__(
            self, name, label, "password", default, **phanterpwa)


class CheckedWidget(CustomWidget):
    def __init__(self, name, label, default=False, **phanterpwa):
        self.name = name
        self.label = label
        self.default = default
        self.type = 'boolean'
        self.phanterpwa = phanterpwa
        CustomWidget.__init__(
            self, name, label, "boolean", default, **phanterpwa)

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        if isinstance(value, bool):
            self._default = value


class WidgetFromFieldDALFromTableDAL():
    def __init__(self, table, field, record_id=None):
        self.table = table
        self._db = self.table._db
        self._field = field
        self._record = None
        self.record_id = record_id

    @property
    def record(self):
        return self._record

    @property
    def record_id(self):
        return self._record_id

    @record_id.setter
    def record_id(self, value):
        self._record_id = None
        if value:
            r = self.table[value]
            if r:
                self._record = r
                self._record_id = value
            else:
                raise ValueError("The record_id not find in table")

    @property
    def db(self):
        return self._db

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value):
        if isinstance(value, Table):
            self._table = value
        else:
            raise ValueError("The table must be a pydal Table instance.")

    def as_dict(self):
        json_field = dict()
        t = self.table[self._field].type
        if t.startswith("reference"):
            ref_table = t.split(" ")[1]
            ref_fields = []
            for f in self.db[ref_table].fields:
                ref_fields.append(f)
            data_ref_table = []
            data_ref_table_formated = []
            q_ref_table = self.db(self.db[ref_table]).select()
            fmt = None
            if self.db[ref_table]._format:
                fmt = self.db[ref_table]._format
            for q in q_ref_table:
                f_format = {}
                row = []
                for z in ref_fields:
                    if (self.db[ref_table][z].type == "datetime") or\
                            (self.db[ref_table][z].type == "date") or\
                            (self.db[ref_table][z].type == "time"):
                        row.append(q[z].isoformat())
                    else:
                        row.append(q[z])
                    f_format[z] = q[z]
                data_ref_table.append(row)
                if fmt:
                    if hasattr(fmt, '__call__'):
                        data_ref_table_formated.append(
                            [q.id, fmt(q) % f_format])
                    else:
                        data_ref_table_formated.append(
                            [q.id, fmt % f_format])
                else:
                    data_ref_table_formated = None

            default = self.table[self._field].default
            if self._record:
                default = self._record[self._field].id
            json_field = {
                'label': self.table[self._field].label,
                'default': default,
                'type': 'reference',
                'fields': ref_fields,
                'data': data_ref_table,
                'formatted': data_ref_table_formated
            }
        elif (t == "datetime") or\
                (t == "date") or\
                (t == "time"):
            default = self.table[self._field].default
            if self._record:
                default = self._record[self._field]
            if default:
                default = default.isoformat()
            json_field = {
                'label': self.table[self._field].label,
                'default': default,
                'type': self.table[self._field].type
            }
            if hasattr(self.table[self._field], "phanterpwa"):
                if "validators" in self.table[self._field].phanterpwa and\
                    "format" not in self.table[self._field].phanterpwa:
                    for v in self.table[self._field].phanterpwa['validators']:
                        if v.startswith("IS_DATE:"):
                            self.table[self._field].phanterpwa[
                                'format'] = v[8:]
                        elif v.startswith("IS_DATETIME:"):
                            self.table[self._field].phanterpwa[
                                'format'] = v[12:]

        else:
            if self._field == "id":
                default = None
                if self._record:
                    default = self._record[self._field]
                json_field = {
                    'label': self.table[self._field].label,
                    'default': default,
                    'type': 'id'
                }
            else:
                default = self.table[self._field].default
                if self._record:
                    default = self._record[self._field]
                json_field = {
                    'label': self.table[self._field].label,
                    'default': default,
                    'type': self.table[self._field].type
                }
        if hasattr(self.table[self._field], "phanterpwa"):
            json_field["phanterpwa"] = self.table[self._field].phanterpwa
        return json_field

    def as_xml(self):
        pass


class WidgetFromFieldDAL():
    def __init__(self, field, db=None):
        self._field = field
        self._db = db

    def as_dict(self):
        json_field = dict()
        t = self._field.type
        if t.startswith("reference"):
            if not self.db:
                raise SyntaxError("The db must be ")
            ref_table = t.split(" ")[1]
            ref_fields = []
            for f in self.db[ref_table].fields:
                ref_fields.append(f)
            data_ref_table = []
            data_ref_table_formated = []
            q_ref_table = self.db(self.db[ref_table]).select()
            fmt = None
            if self.db[ref_table]._format:
                fmt = self.db[ref_table]._format
            for q in q_ref_table:
                f_format = {}
                row = []
                for z in ref_fields:
                    if (self.db[ref_table][z].type == "datetime") or\
                            (self.db[ref_table][z].type == "date") or\
                            (self.db[ref_table][z].type == "time"):
                        row.append(q[z].isoformat())
                    else:
                        row.append(q[z])
                    f_format[z] = q[z]
                data_ref_table.append(row)
                if fmt:
                    if hasattr(fmt, '__call__'):
                        data_ref_table_formated.append(
                            [q.id, fmt(q) % f_format])
                    else:
                        data_ref_table_formated.append(
                            [q.id, fmt % f_format])
                else:
                    data_ref_table_formated = None

            default = self._field.default
            json_field = {
                'label': self._field.label,
                'default': default,
                'type': 'reference',
                'fields': ref_fields,
                'data': data_ref_table,
                'formatted': data_ref_table_formated
            }
        elif (t == "datetime") or\
                (t == "date") or\
                (t == "time"):
            default = self._field.default
            if self._record:
                default = self._record[self._field]
            if default:
                default = default.isoformat()
            json_field = {
                'label': self._field.label,
                'default': default,
                'type': self._field.type
            }
            if hasattr(self._field, "phanterpwa"):
                if "validators" in self._field.phanterpwa and\
                    "format" not in self._field.phanterpwa:
                    for v in self._field.phanterpwa['validators']:
                        if v.startswith("IS_DATE:"):
                            self._field.phanterpwa[
                                'format'] = v[8:]
                        elif v.startswith("IS_DATETIME:"):
                            self._field.phanterpwa[
                                'format'] = v[12:]

        else:
            if self._field == "id":
                default = None
                json_field = {
                    'label': self._field.label,
                    'default': default,
                    'type': 'id'
                }
            else:
                default = self._field.default
                json_field = {
                    'label': self._field.label,
                    'default': default,
                    'type': self._field.type
                }
        if hasattr(self._field, "phanterpwa"):
            json_field["phanterpwa"] = self._field.phanterpwa
        return json_field


class FormFromFieldsDAL():
    def __init__(self, table_name, *fields):
        self._table_name = table_name
        self._fields = fields
        self._extra_fields = dict()
        self.json_widgets = dict()
        self.widgets = dict()

    def _process(self):
        self.dict = {
            "table": self._table_name,
            "id": None,
            "json_widgets": self.json_widgets
        }
        for x in self.fields:
            json_widget = WidgetFromFieldDAL(x)
            self.json_widgets[x] = json_widget.as_dict()
            self.widgets[x] = json_widget.as_xml()

    def as_dict(self):
        self._process()
        return self.dict

    def as_json(self, indent=2):
        return json.dumps(self.as_dict(), indent=indent)

    def as_xml(self, show_id=False, submit_button=None):
        self.show_id = show_id
        self._xml = FORM(
            DIV(
                DIV(
                    I(
                        _class="fas fa-check"
                    ),
                    _id="phanterpwa-widget-check-{0}-csrf_token".format(self.table_name),
                    _class="phanterpwa-widget-check"
                ),
                DIV(
                    INPUT(
                        _id="phanterpwa-widget-input-{0}-csrf_token".format(self.table_name),
                        _name="csrf_token",
                        _phanterpwa_widget_validator=['IS_NOT_EMPTY'],
                        _phanterpwa_widget_table_name=self.table_name,
                        _type="hidden"
                    ),
                    LABEL(
                        "CSRF Token",
                        _for="phanterpwa-widget-input-{0}-csrf_token".format(self.table_name),
                    ),
                    _class='input-field'
                ),
                DIV(_class="phanterpwa-widget-error"),
                _id='phanterpwa-widget-{0}-csrf_token'.format(self.table_name),
                _class='phanterpwa-widget phanterpwa-widget-hidden easy_forced_hidden'
            ),
            _id="phanterpwa-jsonform-{0}".format(self.table_name),
            _class="phanterpwa-jsonform",
            _phanterpwa_jsonform=self.table_name
        )
        if submit_button is not None:
            self._buttons_container = DIV(
                submit_button,
                _class='buttons-form-container'
            )
        else:
            self._buttons_container = DIV(
                SubmitButton(
                    "phanterpwa-widget-submit_button-{0}".format(self.table_name),
                    "Submit",
                    _phanterpwa_widget_submit_button=True
                ),
                _class='buttons-form-container'
            )


class FormFromTableDAL():
    def __init__(self, table, record_id=None, fields=None):
        self.table = table
        self._db = self.table._db
        if fields:
            self.fields = fields
        else:
            self._fields = self.table.fields
        self._record = None
        self._extra_fields = dict()
        self.record_id = record_id
        self.json_widgets = dict()
        self.widgets = dict()

    def add_extra_field(self, value):
        if isinstance(value, CustomWidget):
            if value.name in self.fields:
                raise ValueError("The name of extra field must be unique.")
            self._extra_fields[value.name] = value

    @property
    def record_id(self):
        return self._record_id

    @record_id.setter
    def record_id(self, value):
        self._record_id = None
        if value:
            r = self.table[value]
            if r:
                self._record = r
                self._record_id = value
            else:
                raise ValueError("The record_id not find in table")

    @property
    def record(self):
        return self._record

    @property
    def db(self):
        return self._db

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        new_list = list()
        if isinstance(value, (list, tuple)):
            for l in value:
                if l in self.table.fields:
                    new_list.append(l)
            self._fields = new_list
        else:
            raise TypeError("The fields must be list or tuple. Given: {0}".format(type(value)))

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value):
        if isinstance(value, Table):
            self._table = value
        else:
            raise ValueError("The table must be a pydal Table instance.")

    def _process(self):
        self.dict = {
            "table": self.table._tablename,
            "id": self.record_id,
            "json_widgets": self.json_widgets
        }
        for x in self.fields:
            json_widget = WidgetFromFieldDALFromTableDAL(self.table, x, self.record_id)
            self.json_widgets[x] = json_widget.as_dict()
            self.widgets[x] = json_widget.as_xml()
        for e in self._extra_fields:
            self.json_widgets[e] = self._extra_fields[e].as_dict()
            self.widgets[e] = self._extra_fields[e].as_xml()

    def as_dict(self):
        self._process()
        return self.dict

    def as_json(self, indent=2):
        return json.dumps(self.as_dict(), indent=indent)

    def as_xml(self, show_id=False, submit_button=None):
        self.show_id = show_id
        self._xml = FORM(
            DIV(
                DIV(
                    I(
                        _class="fas fa-check"
                    ),
                    _id="phanterpwa-widget-check-{0}-csrf_token".format(self.table_name),
                    _class="phanterpwa-widget-check"
                ),
                DIV(
                    INPUT(
                        _id="phanterpwa-widget-input-{0}-csrf_token".format(self.table_name),
                        _name="csrf_token",
                        _phanterpwa_widget_validator=['IS_NOT_EMPTY'],
                        _phanterpwa_widget_table_name=self.table_name,
                        _type="hidden"
                    ),
                    LABEL(
                        "CSRF Token",
                        _for="phanterpwa-widget-input-{0}-csrf_token".format(self.table_name),
                    ),
                    _class='input-field'
                ),
                DIV(_class="phanterpwa-widget-error"),
                _id='phanterpwa-widget-{0}-csrf_token'.format(self.table_name),
                _class='phanterpwa-widget phanterpwa-widget-hidden easy_forced_hidden'
            ),
            _id="phanterpwa-jsonform-{0}".format(self.table_name),
            _class="phanterpwa-jsonform",
            _phanterpwa_jsonform=self.table_name
        )
        if submit_button is not None:
            self._buttons_container = DIV(
                submit_button,
                _class='buttons-form-container'
            )
        else:
            self._buttons_container = DIV(
                SubmitButton(
                    "phanterpwa-widget-submit_button-{0}".format(self.table_name),
                    "Submit",
                    _phanterpwa_widget_submit_button=True
                ),
                _class='buttons-form-container'
            )


class FieldsDALValidateDictArgs(object):

    def __init__(self, dict_args, *fields):
        super(FieldsDALValidateDictArgs, self).__init__()
        self.dict_args = dict_args
        self.fields = fields
        self._errors = {}
        self._verified = {}
        self._ignored = {}

    @property
    def errors(self):
        self.validate()
        return self._errors

    @property
    def dict_args(self):
        return self._dict_args

    @dict_args.setter
    def dict_args(self, dict_args):
        if isinstance(dict_args, dict):
            self._dict_args = dict_args
        else:
            raise TypeError(
                "The dict_args must be dict object. given: %s" % type(dict_args)
            )

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, list_fields):
        n_l = list()
        for x in list_fields:
            if isinstance(x, Field):
                n_l.append(x)
            else:
                if x is not None:
                    raise TypeError(
                        "The fields must be pydal.Field object. given: %s" % type(x)
                    )
        self._fields = n_l

    @property
    def verified(self):
        self.validate()
        return self._verified

    @property
    def ignored(self):
        self.validate()
        return self._ignored

    def validate(self):
        self._errors = {}
        self._verified = {}
        self._ignored = {}
        for f in self.dict_args:
            ig = True
            for F in self.fields:
                if F.name == f:
                    ig = False
                    result = F.validate(self.dict_args[f])
                    if result[1] is not None:
                        self._errors[f] = result[1]
                    else:
                        self._verified[f] = self.dict_args[f]
            if ig:
                self._ignored[f] = self.dict_args[f]

        if self._errors:
            return self._errors

    def insert_on(self, dbtable, commit=True):
        self.validate()
        if not self.errors and isinstance(dbtable, Table):
            rep = dbtable.validate_and_insert(**self.verified)
            dbtable._db._adapter.reconnect()
            if rep.errors:
                dbtable._db.rollback()
            elif rep.id and commit:
                dbtable._db.commit()
            return rep
        else:
            if not self.errors:
                raise "The dbtable must be pydal.DAL.Table object. given: {0}.".format(type(dbtable))

    def update_on(self, dbset, commit=True):
        self.validate()
        if not self.errors and isinstance(dbset, Set):
            rep = dbset.validate_and_update(**self.verified)
            dbset._db._adapter.reconnect()
            if rep.errors:
                dbset._db.rollback
            elif rep.id and commit:
                dbset._db.commit()
            return rep
        else:
            if not self.errors:
                raise "The dbtable must be pydal.Objects.Set object. given: {0}.".format(type(dbset))
