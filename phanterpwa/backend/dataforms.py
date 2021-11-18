import json
import types
import re
import time
import datetime
from phanterpwa.helpers import (
    FORM,
    DIV,
    I,
    INPUT,
    LABEL
)

from pydal.objects import (Set, Table, Field)
from pydal.validators import (
    IS_NOT_EMPTY,
    IS_DATE,
    IS_DATETIME,
    IS_TIME,
    IS_IN_SET,
    IS_EMAIL,
    IS_EMPTY_OR,
    IS_IN_DB
)

from phanterpwa.backend.pydal.extra_validations import IS_ACTIVATION_CODE

ref_values = re.compile(r"\$[0-9]{13}\:.*")


def datetime_formater(value):
    value = value.replace("%d", "dd").replace("%m", "MM").replace("%Y", "yyyy").replace(
        "%H", "HH").replace("%M", "mm").replace("%S", "ss")
    return value


def datetime_converter(iso_value, pattern="date", out_format="%Y-%m-%d %H:%M:%S", omit_errors=True):
    """
    @iso_value: The iso-value must be in the following format:
        "%Y-%m-%d %H:%M:%S" to date pattern

    @patter: There are three valid values: date, datetime and time
    @out_format: out strftime format
    @omit_errors: If it's True, on error returns None.
    """
    if pattern == "date":
        in_format = "%Y-%m-%d"
    elif pattern == "time":
        in_format = "%H:%M:%S"
    elif pattern == "datetime":
        in_format = "%Y-%m-%d %H:%M:%S"
    else:
        if omit_errors:
            print("the pattern is invalid. Given: {0}".format(pattern))
            return None
        else:
            raise ValueError("The pattern must be data, datetime or time")

    if omit_errors:
        try:
            strptime = time.strptime(str(iso_value), in_format)
            result = time.strftime(out_format, strptime)
        except Exception as e:
            print(e)
            return None
        else:
            return result
    else:
        strptime = time.strptime(str(iso_value), in_format)
        result = time.strftime(out_format, strptime)

    return result


class DataForm():
    _form_list = []

    def __init__(self, identifier, **parameters):
        DataForm._add_in_form_list(identifier)
        self.identifier = identifier
        self.table = parameters.get("table", None)
        self._id = parameters.get("id", None)
        self.uri = parameters.get("uri", None)

    def as_dict(self):
        FormFromTableDAL(self.table, self._id)

    @classmethod
    def _add_in_form_list(cls, identifier):
        cls._form_list.append(identifier)

    @property
    def form_list(self):
        return DataForm._form_list


class WidgetFromFieldDALFromTableDAL():
    def __init__(self, table, field, record_id=None, data_view=False, simple_widget=False, custom_phanterpwa=None):
        self.table = table
        self._db = self.table._db
        self._data_view = data_view
        self._field = field
        self._record = None
        self.record_id = record_id
        self.section = None
        self.position = None
        self.group = None
        self.out_of_form = False
        self.simple_widget = simple_widget
        self.phanterpwa = dict()
        if custom_phanterpwa:
            self.phanterpwa = custom_phanterpwa

        if hasattr(self.table[self._field], "phanterpwa"):
            for x in self.table[self._field].phanterpwa:
                if x not in self.phanterpwa:
                    self.phanterpwa[x] = self.table[self._field].phanterpwa[x]

            if "data_view" in self.phanterpwa:
                self._data_view = self.phanterpwa["data_view"]
            if "position" in self.phanterpwa:
                self.position = self.phanterpwa["position"]
            if "section" in self.phanterpwa:
                self.section = self.phanterpwa["section"]
            elif "group" in self.phanterpwa:
                self.group = self.phanterpwa["group"]
            if "out_of_form" in self.phanterpwa and\
                    self.phanterpwa["out_of_form"] is True:
                self.out_of_form = True
            if "simple_widget" in self.phanterpwa and\
                    self.phanterpwa["simple_widget"] is True:
                self.simple_widget = True
        if "_class" not in self.phanterpwa:
            self.phanterpwa["_class"] = "p-col w1p100"

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if value is None:
            self._position = None
        elif isinstance(value, int):
            self._position = value
        elif str(value).isdigit():
            self._position = int(value)
        else:
            raise SyntaxError(
                "The position value must be intenger. Give: {0}".format(type(value)))

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
            r = self._db(self._db[self.table._tablename]._id == value).select().first()
            if r:
                self._record = r
                self._record_id = r.id
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

    def __ppwa_check_validators(self, validator):

        if isinstance(validator, IS_NOT_EMPTY):
            if "can_empty" not in self.phanterpwa:
                self.phanterpwa["can_empty"] = False
            return ["IS_NOT_EMPTY"]
        elif isinstance(validator, IS_DATETIME):
            if "format" not in self.phanterpwa:
                self.phanterpwa["validator_format"] = validator.format
                self.phanterpwa["format"] = datetime_formater(validator.format)
            return ["IS_DATETIME:{0}".format(datetime_formater(validator.format))]
        elif isinstance(validator, IS_DATE):
            if "format" not in self.phanterpwa:
                self.phanterpwa["validator_format"] = validator.format
                self.phanterpwa["format"] = datetime_formater(validator.format)
            return ["IS_DATE:{0}".format(datetime_formater(validator.format))]
        elif isinstance(validator, IS_TIME):
            if "format" not in self.phanterpwa:
                self.phanterpwa["validator_format"] = validator.format
                self.phanterpwa["format"] = datetime_formater(validator.format)
            return ["IS_TIME:{0}".format(datetime_formater(validator.format))]
        elif isinstance(validator, IS_ACTIVATION_CODE):
            return ["IS_ACTIVATION_CODE"]
        elif isinstance(validator, IS_EMAIL):
            return ["IS_EMAIL"]
        elif isinstance(validator, IS_IN_DB):
            if "data_set" not in self.phanterpwa:
                validator.build_set()
                table_name = validator.ktable
                if callable(self._db[table_name]._format):
                    theset = [self._db[table_name]._format(x) for x in self._db(self._db[table_name].id > 0).select()]
                elif self._db[table_name]._format and isinstance(self._db[table_name]._format, str):
                    theset = [self._db[table_name]._format % x.as_dict() for x in self._db(self._db[table_name].id > 0).select()]
                else:
                    theset = [x.id for x in self._db(self._db[table_name].id > 0).select()]
                return ["IS_IN_SET:{0}".format(json.dumps("{0}".format(theset)))]
            else:
                if callable(self.phanterpwa['data_set']):
                    theset = self.phanterpwa['data_set'](self.record)
                else:
                    theset = self.phanterpwa['data_set']
                self.phanterpwa['data_set'] = theset
                return ["IS_IN_SET:{0}".format(json.dumps("{0}".format(theset)))]
        elif isinstance(validator, IS_IN_SET):
            if "data_set" not in self.phanterpwa and "type" not in self.phanterpwa:
                self.phanterpwa["type"] = "select"
                self.phanterpwa["data_set"] = list(validator.theset)
            return ["IS_IN_SET:{0}".format(json.dumps("{0}".format(validator.theset)))]
        elif isinstance(validator, IS_EMPTY_OR):
            if "can_empty" not in self.phanterpwa and \
                    "validators" not in self.phanterpwa:
                self.phanterpwa["can_empty"] = True
            elif "validators" in self.phanterpwa and \
                    "IS_NOT_EMPTY" in self.phanterpwa["validators"]:
                self.phanterpwa["can_empty"] = False
            other = self.__ppwa_check_validators(validator.other)
            if other:
                if isinstance(other, (list, tuple)):
                    return ["IS_EMPTY_OR", *other]
                else:
                    return ["IS_EMPTY_OR", other]
            else:
                return []
        elif isinstance(validator, type(lambda: 0)):
            return []
        elif isinstance(validator, list):
            return [self.__ppwa_check_validators(x) for x in validator]

    def as_dict(self):
        json_field = dict()
        if not self.out_of_form:
            FieldInst = self.table[self._field]
            t = FieldInst.type
            def u_list(v_list):
                result = []
                if isinstance(v_list, list):
                    t = list(v_list)
                    for item in v_list:
                        if (isinstance(item, (list, tuple))):
                            result.extend(item)
                        elif item:
                            result.append(item)
                return result
            auto_validators = u_list(self.__ppwa_check_validators(FieldInst.requires))

            if "validators" not in self.phanterpwa:
                json_field["validators"] = auto_validators
            else:
                json_field["validators"] = self.phanterpwa["validators"]
            default = FieldInst.default
            if "can_empty" in self.phanterpwa:
                json_field["can_empty"] = self.phanterpwa["can_empty"]

            if t.startswith("reference"):

                if self._record_id:
                    if self._record[FieldInst]:
                        default = self._record[FieldInst].id
                    else:
                        default = None
                json_field['editable'] = self.phanterpwa.get("editable", False)
                ref_table = t.split(" ")[1]
                if "data_set" in self.phanterpwa:
                    if callable(self.phanterpwa['data_set']):
                        data_ref_table_formated = self.phanterpwa['data_set'](self.record)
                    else:
                        data_ref_table_formated = self.phanterpwa["data_set"]
                    if json_field['editable']:
                        if 'reference_field' not in self.phanterpwa:
                            raise SyntaxError("".join(["You placed in '", self._field,
                                "' the reference field as editable, it is necessary to",
                                    " define the field of the referenced table. e.g. ",
                                        "phanterpwa = {'editable': True, 'refence_field': 'field_of_referenced_table'}"]))
                        else:
                            json_field['reference_field'] = self.phanterpwa["reference_field"]
                    else:
                        json_field['reference_field'] = 'id'
                    json_field['reference_table'] = ref_table
                else:
                    if not self.db:
                        raise SyntaxError("The db must be DAL database instance")
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
                                if q[z]:
                                    row.append(q[z].isoformat())
                                else:
                                    row.append(q[z])
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
                            data_ref_table_formated = data_ref_table

                    json_field['fields'] = self.db[ref_table].fields
                    
                    if json_field['editable']:
                        if 'reference_field' not in self.phanterpwa:
                            raise SyntaxError("".join(["You placed in '", self._field,
                                "' the reference field as editable, it is necessary to",
                                    " define the field of the referenced table. e.g. ",
                                        "phanterpwa = {'editable': True, 'refence_field': 'field_of_referenced_table'}"]))
                        else:
                            json_field['reference_field'] = self.phanterpwa["reference_field"]
                    else:
                        json_field['reference_field'] = 'id'
                    json_field['reference_table'] = ref_table
                json_field['label'] = FieldInst.label
                json_field['value'] = default
                json_field['type'] = 'reference'
                json_field['data_set'] = data_ref_table_formated

            elif (t == "datetime") or\
                    (t == "date") or\
                    (t == "time"):
                default = FieldInst.default
                if self._record_id:
                    default = self._record[FieldInst]
                # print(type(default))
                # if default:
                #     default = default.isoformat()
                if "format" in self.phanterpwa:
                    dformat = self.phanterpwa["format"]
                elif t == "datetime":
                    dformat = "yyyy-MM-dd HH:mm:ss"
                elif t == "date":
                    dformat = "yyyy-MM-dd"
                elif t == "time":
                    dformat = "HH:mm:ss"
                if "validator_format" in self.phanterpwa and default:
                    formato_saida = self.phanterpwa["validator_format"]
                    json_field["validator_format"] = formato_saida
                    if t == "datetime":
                        if isinstance(default, datetime.datetime) or isinstance(default, datetime.date):
                            resultado = str(default.strftime(formato_saida))
                            default = default.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            tempo = time.strptime(str(default), '%Y-%m-%d %H:%M:%S')
                            resultado = str(time.strftime(formato_saida, tempo))
                    elif t == "date":
                        if isinstance(default, datetime.datetime) or isinstance(default, datetime.date):
                            resultado = str(default.strftime(formato_saida))
                            default = default.strftime('%Y-%m-%d')
                        else:
                            tempo = time.strptime(str(default), '%Y-%m-%d')
                            resultado = str(time.strftime(formato_saida, tempo))
                    elif t == "time":
                        if isinstance(default, datetime.datetime) or isinstance(default, datetime.date):
                            resultado = str(default.strftime(formato_saida))
                            default = default.strftime('%H:%M:%S')
                        else:
                            tempo = time.strptime(str(default), '%H:%M:%S')
                            resultado = str(time.strftime(formato_saida, tempo))
                    json_field['formatted'] = resultado
                elif default:
                    if t == "datetime":
                        general_format = '%Y-%m-%d %H:%M:%S'
                        json_field["validator_format"] = general_format
                        if isinstance(default, datetime.datetime) or isinstance(default, datetime.date):
                            resultado = str(default.strftime(general_format))
                            default = resultado
                        else:
                            tempo = time.strptime(str(default), general_format)
                            resultado = str(time.strftime(general_format, tempo))
                    elif t == "date":
                        general_format = '%Y-%m-%d'
                        json_field["validator_format"] = general_format
                        if isinstance(default, datetime.datetime) or isinstance(default, datetime.date):
                            resultado = str(default.strftime(general_format))
                            default = resultado
                        else:
                            tempo = time.strptime(str(default), general_format)
                            resultado = str(time.strftime(general_format, tempo))
                    elif t == "time":
                        general_format = '%H:%M:%S'
                        json_field["validator_format"] = general_format
                        if isinstance(default, datetime.datetime) or isinstance(default, datetime.date):
                            resultado = str(default.strftime(general_format))
                            default = resultado
                        else:
                            tempo = time.strptime(str(default), general_format)
                            resultado = str(time.strftime(formato_saida, tempo))
                    json_field['formatted'] = resultado
                else:
                    formato_saida = self.phanterpwa["validator_format"]
                    json_field["validator_format"] = formato_saida
                if self.simple_widget:
                    json_field['label'] = FieldInst.label
                    json_field['value'] = default
                    json_field['type'] = "string"
                    json_field['format'] = dformat
                    json_field['mask'] = str(dformat).replace(
                        "d", "#"
                    ).replace(
                        "M", "#"
                    ).replace(
                        "y", "#"
                    ).replace(
                        "H", "#"
                    ).replace(
                        "m", "#"
                    ).replace(
                        "s", "#"
                    )
                    new_validators = []
                    if "validators" in json_field and isinstance(json_field["validators"], list):
                        for x in json_field["validators"]:
                            if "IS_DATE" in x or "IS_TIME" in x:
                                new_validators.append("MASK:{0}".format(json_field['mask']))
                            else:
                                new_validators.append(x)
                        json_field["validators"] = new_validators
                else:
                    json_field['label'] = FieldInst.label
                    json_field['value'] = default
                    json_field['type'] = FieldInst.type
                    json_field['format'] = dformat
                    json_field['mask'] = dformat

            else:
                default = FieldInst.default
                if self._record_id:
                    default = self._record[FieldInst]
                if FieldInst.type == "id":
                    json_field['label'] = FieldInst.label
                    json_field['value'] = default
                    json_field['type'] = 'id'

                else:
                    json_field['label'] = FieldInst.label
                    json_field['value'] = default
                    json_field['type'] = FieldInst.type

                    if "format" in self.phanterpwa:
                        json_field["format"] = self.phanterpwa["format"]
                    if "data_set" in self.phanterpwa:
                        if FieldInst.type == "string":
                            json_field["type"] = "select"
                        if callable(self.phanterpwa['data_set']):
                            json_field["data_set"] = self.phanterpwa['data_set'](self.record)
                        elif isinstance(self.phanterpwa['data_set'], types.GeneratorType):
                            json_field["data_set"] = list(self.phanterpwa['data_set'])
                            self.phanterpwa['data_set'] = json_field["data_set"]
                        else:
                            json_field["data_set"] = self.phanterpwa["data_set"]
                    if "mask" in self.phanterpwa:
                        json_field["mask"] = self.phanterpwa["mask"]
                    if "type" in self.phanterpwa:
                        json_field["type"] = self.phanterpwa["type"]
                    if "cutter" in self.phanterpwa:
                        json_field["cutter"] = self.phanterpwa["cutter"]
                    if "width" in self.phanterpwa:
                        json_field["width"] = self.phanterpwa["width"]
                    if "height" in self.phanterpwa:
                        json_field["height"] = self.phanterpwa["height"]
                    if "view_width" in self.phanterpwa:
                        json_field["view_width"] = self.phanterpwa["view_width"]
                    if "view_height" in self.phanterpwa:
                        json_field["view_height"] = self.phanterpwa["view_height"]
            if "extra" in self.phanterpwa and self.record and callable(self.phanterpwa['extra']):
                json_field["extra"] = self.phanterpwa['extra'](self.record)
            if "url" in self.phanterpwa and self.record and callable(self.phanterpwa['url']):
                json_field["url"] = self.phanterpwa['url'](self.record)
            if "no-cache" in self.phanterpwa:
                json_field["no-cache"] = self.phanterpwa['no-cache']
            if "disabled" in self.phanterpwa:
                json_field["disabled"] = self.phanterpwa['disabled']
            if "editable" in self.phanterpwa:
                json_field["editable"] = self.phanterpwa['editable']
            for x in self.phanterpwa:
                if x.startswith("_"):
                    json_field[x] = self.phanterpwa[x]
            if self._data_view:
                json_field["data_view"] = True
            else:
                json_field["data_view"] = False
        return json_field

    def as_xml(self):
        return None


class CustomField():
    def __init__(self, table, field, record_id=None, data_view=False):
        self.table = table
        self._db = self.table._db
        self._data_view = data_view
        self._field = field
        self._record = None
        self.record_id = record_id
        self.position = None
        self.section = None
        self.group = None
        self.out_of_form = False
        self.phanterpwa = dict()

        if hasattr(self._field, "phanterpwa"):
            for x in self._field.phanterpwa:
                if x not in self.phanterpwa:
                    self.phanterpwa[x] = self._field.phanterpwa[x]

            if "data_view" in self.phanterpwa:
                self._data_view = self.phanterpwa["data_view"]
            if "position" in self.phanterpwa:
                self.position = self.phanterpwa["position"]
            if "section" in self.phanterpwa:
                self.section = self.phanterpwa["section"]
            elif "group" in self.phanterpwa:
                self.group = self.phanterpwa["group"]
            if "out_of_form" in self.phanterpwa and\
                    self.phanterpwa["out_of_form"] is True:
                self.out_of_form = True
            if "simple_widget" in self.phanterpwa and\
                    self.phanterpwa["simple_widget"] is True:
                self.simple_widget = True
        if "_class" not in self.phanterpwa:
            self.phanterpwa["_class"] = "p-col w1p100"

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if value is None:
            self._position = None
        elif isinstance(value, int):
            self._position = value
        elif str(value).isdigit():
            self._position = int(value)
        else:
            raise SyntaxError(
                "The position value must be intenger. Give: {0}".format(type(value)))

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
            r = self._db(self._db[self.table._tablename]._id == value).select().first()
            if r:
                self._record = r
                self._record_id = r.id
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

    def __ppwa_check_validators(self, validator):

        if isinstance(validator, IS_NOT_EMPTY):
            if "can_empty" not in self.phanterpwa:
                self.phanterpwa["can_empty"] = False
            return ["IS_NOT_EMPTY"]
        elif isinstance(validator, IS_DATETIME):
            if "format" not in self.phanterpwa:
                self.phanterpwa["validator_format"] = validator.format
                self.phanterpwa["format"] = datetime_formater(validator.format)
            return ["IS_DATETIME:{0}".format(datetime_formater(validator.format))]
        elif isinstance(validator, IS_DATE):
            if "format" not in self.phanterpwa:
                self.phanterpwa["validator_format"] = validator.format
                self.phanterpwa["format"] = datetime_formater(validator.format)
            return ["IS_DATE:{0}".format(datetime_formater(validator.format))]
        elif isinstance(validator, IS_TIME):
            if "format" not in self.phanterpwa:
                self.phanterpwa["validator_format"] = validator.format
                self.phanterpwa["format"] = datetime_formater(validator.format)
            return ["IS_TIME:{0}".format(datetime_formater(validator.format))]
        elif isinstance(validator, IS_ACTIVATION_CODE):
            return ["IS_ACTIVATION_CODE"]
        elif isinstance(validator, IS_EMAIL):
            return ["IS_EMAIL"]
        elif isinstance(validator, IS_IN_DB):
            validator.build_set()
            table_name = validator.ktable
            if callable(self._db[table_name]._format):
                theset = [self._db[table_name]._format(x) for x in self._db(self._db[table_name].id > 0).select()]
            elif self._db[table_name]._format and isinstance(self._db[table_name]._format, str):
                theset = [self._db[table_name]._format % x.as_dict() for x in self._db(self._db[table_name].id > 0).select()]
            else:
                theset = [x.id for x in self._db(self._db[table_name].id > 0).select()]
            return ["IS_IN_SET:{0}".format(json.dumps("{0}".format(theset)))]
        elif isinstance(validator, IS_IN_SET):
            if "data_set" not in self.phanterpwa and "type" not in self.phanterpwa:
                self.phanterpwa["type"] = "select"
                self.phanterpwa["data_set"] = list(validator.theset)
            return ["IS_IN_SET:{0}".format(json.dumps("{0}".format(validator.theset)))]
        elif isinstance(validator, IS_EMPTY_OR):
            if "can_empty" not in self.phanterpwa and \
                    "validators" not in self.phanterpwa:
                self.phanterpwa["can_empty"] = True
            elif "validators" in self.phanterpwa and \
                    "IS_NOT_EMPTY" in self.phanterpwa["validators"]:
                self.phanterpwa["can_empty"] = False
            other = self.__ppwa_check_validators(validator.other)
            if other:
                if isinstance(other, (list, tuple)):
                    return ["IS_EMPTY_OR", *other]
                else:
                    return ["IS_EMPTY_OR", other]
            else:
                return []
        elif isinstance(validator, type(lambda: 0)):
            return []
        elif isinstance(validator, list):
            return [self.__ppwa_check_validators(x) for x in validator]

    def as_dict(self):
        json_field = dict()
        if not self.out_of_form:
            FieldInst = self._field
            t = FieldInst.type
            def u_list(v_list):
                result = []
                if isinstance(v_list, list):
                    t = list(v_list)
                    for item in v_list:
                        if (isinstance(item, (list, tuple))):
                            result.extend(item)
                        elif item:
                            result.append(item)
                return result
            auto_validators = u_list(self.__ppwa_check_validators(FieldInst.requires))

            if "validators" not in self.phanterpwa:
                json_field["validators"] = auto_validators
            else:
                json_field["validators"] = self.phanterpwa["validators"]
            default = FieldInst.default
            if "can_empty" in self.phanterpwa:
                json_field["can_empty"] = self.phanterpwa["can_empty"]

            if t.startswith("reference"):

                if self._record_id:
                    if self._record[FieldInst]:
                        default = self._record[FieldInst].id
                    else:
                        default = None
                if not self.db:
                    raise SyntaxError("The db must be DAL database instance")
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
                            if q[z]:
                                row.append(q[z].isoformat())
                            else:
                                row.append(q[z])
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
                        data_ref_table_formated = data_ref_table

                json_field['label'] = FieldInst.label
                json_field['value'] = default
                json_field['type'] = 'reference'
                json_field['fields'] = self.db[ref_table].fields
                json_field['data_set'] = data_ref_table_formated
                json_field['editable'] = self.phanterpwa.get("editable", False)
                if json_field['editable']:
                    if 'reference_field' not in self.phanterpwa:
                        raise SyntaxError("".join(["You placed in '", self._field,
                            "' the reference field as editable, it is necessary to",
                                " define the field of the referenced table. e.g. ",
                                    "phanterpwa = {'editable': True, 'refence_field': 'field_of_referenced_table'}"]))
                    else:
                        json_field['reference_field'] = self.phanterpwa["reference_field"]
                else:
                    json_field['reference_field'] = 'id'
                json_field['reference_table'] = ref_table

            elif (t == "datetime") or\
                    (t == "date") or\
                    (t == "time"):
                default = FieldInst.default
                if self._record_id:
                    default = self._record[FieldInst]
                # print(type(default))
                # if default:
                #     default = default.isoformat()
                if "format" in self.phanterpwa:
                    dformat = self.phanterpwa["format"]
                elif t == "datetime":
                    dformat = "yyyy-MM-dd HH:mm:ss"
                elif t == "date":
                    dformat = "yyyy-MM-dd"
                elif t == "time":
                    dformat = "HH:mm:ss"
                if "validator_format" in self.phanterpwa and default:
                    formato_saida = self.phanterpwa["validator_format"]
                    json_field["validator_format"] = formato_saida
                    if t == "datetime":
                        if isinstance(default, datetime.datetime) or isinstance(default, datetime.date):
                            resultado = str(default.strftime(formato_saida))
                            default = default.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            tempo = time.strptime(str(default), '%Y-%m-%d %H:%M:%S')
                            resultado = str(time.strftime(formato_saida, tempo))
                    elif t == "date":
                        if isinstance(default, datetime.datetime) or isinstance(default, datetime.date):
                            resultado = str(default.strftime(formato_saida))
                            default = default.strftime('%Y-%m-%d')
                        else:
                            tempo = time.strptime(str(default), '%Y-%m-%d')
                            resultado = str(time.strftime(formato_saida, tempo))
                    elif t == "time":
                        if isinstance(default, datetime.datetime) or isinstance(default, datetime.date):
                            resultado = str(default.strftime(formato_saida))
                            default = default.strftime('%H:%M:%S')
                        else:
                            tempo = time.strptime(str(default), '%H:%M:%S')
                            resultado = str(time.strftime(formato_saida, tempo))
                    json_field['formatted'] = resultado
                elif default:
                    if t == "datetime":
                        general_format = '%Y-%m-%d %H:%M:%S'
                        json_field["validator_format"] = general_format
                        if isinstance(default, datetime.datetime) or isinstance(default, datetime.date):
                            resultado = str(default.strftime(general_format))
                            default = resultado
                        else:
                            tempo = time.strptime(str(default), general_format)
                            resultado = str(time.strftime(general_format, tempo))
                    elif t == "date":
                        general_format = '%Y-%m-%d'
                        json_field["validator_format"] = general_format
                        if isinstance(default, datetime.datetime) or isinstance(default, datetime.date):
                            resultado = str(default.strftime(general_format))
                            default = resultado
                        else:
                            tempo = time.strptime(str(default), general_format)
                            resultado = str(time.strftime(general_format, tempo))
                    elif t == "time":
                        general_format = '%H:%M:%S'
                        json_field["validator_format"] = general_format
                        if isinstance(default, datetime.datetime) or isinstance(default, datetime.date):
                            resultado = str(default.strftime(general_format))
                            default = resultado
                        else:
                            tempo = time.strptime(str(default), general_format)
                            resultado = str(time.strftime(formato_saida, tempo))
                    json_field['formatted'] = resultado
                else:
                    formato_saida = self.phanterpwa["validator_format"]
                    json_field["validator_format"] = formato_saida

                json_field['label'] = FieldInst.label
                json_field['value'] = default
                json_field['type'] = FieldInst.type
                json_field['format'] = dformat
                json_field['mask'] = dformat

            else:
                default = FieldInst.default
                if "value" in self.phanterpwa:
                    default = self.phanterpwa["value"]
                if FieldInst.type == "id":
                    json_field['label'] = FieldInst.label
                    json_field['value'] = default
                    json_field['type'] = 'id'

                else:
                    json_field['label'] = FieldInst.label
                    json_field['value'] = default
                    json_field['type'] = FieldInst.type

                    if "format" in self.phanterpwa:
                        json_field["format"] = self.phanterpwa["format"]
                    if "data_set" in self.phanterpwa:
                        if FieldInst.type == "string":
                            json_field["type"] = "select"
                        if callable(self.phanterpwa['data_set']):
                            json_field["data_set"] = self.phanterpwa['data_set'](self.record)
                        else:
                            json_field["data_set"] = self.phanterpwa["data_set"]
                    if "mask" in self.phanterpwa:
                        json_field["mask"] = self.phanterpwa["mask"]
                    if "type" in self.phanterpwa:
                        json_field["type"] = self.phanterpwa["type"]
                    if "cutter" in self.phanterpwa:
                        json_field["cutter"] = self.phanterpwa["cutter"]
                    if "width" in self.phanterpwa:
                        json_field["width"] = self.phanterpwa["width"]
                    if "height" in self.phanterpwa:
                        json_field["height"] = self.phanterpwa["height"]
                    if "view_width" in self.phanterpwa:
                        json_field["view_width"] = self.phanterpwa["view_width"]
                    if "view_height" in self.phanterpwa:
                        json_field["view_height"] = self.phanterpwa["view_height"]
            if "extra" in self.phanterpwa and self.record and callable(self.phanterpwa['extra']):
                json_field["extra"] = self.phanterpwa['extra'](self.record)
            if "url" in self.phanterpwa and self.record and callable(self.phanterpwa['url']):
                json_field["url"] = self.phanterpwa['url'](self.record)

            if "no-cache" in self.phanterpwa:
                json_field["no-cache"] = self.phanterpwa['no-cache']
            if "disabled" in self.phanterpwa:
                json_field["disabled"] = self.phanterpwa['disabled']
            if "editable" in self.phanterpwa:
                json_field["editable"] = self.phanterpwa['editable']
            for x in self.phanterpwa:
                if x.startswith("_"):
                    json_field[x] = self.phanterpwa[x]
            if self._data_view:
                json_field["data_view"] = True
            else:
                json_field["data_view"] = False
        return json_field

    def as_xml(self):
        return None


class FormFromTableDAL():
    def __init__(self, table, record_id=None, fields=None, custom_validates={}, data_view=False, simple_form=False):
        self.table = table
        self._db = self.table._db
        self._data_view = data_view
        self.simple_form = simple_form
        if fields:
            self.fields = fields
        else:
            self._fields = self.table.fields
        self._record = None
        self._extra_fields = {}
        self.record_id = record_id
        self.json_widgets = []
        self.xml_wigets = {}
        self._widgets = {}
        self._errors = {}
        self._ok = {}
        self._verified = {}
        self._ignored = {}
        self._changed = {}
        self.custom_validates = custom_validates
        self._custom_phanterpwa = dict()

    @property
    def custom_phanterpwa(self):
        return self._custom_phanterpwa

    def add_extra_field(self, value):
        if isinstance(value, Field):
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

    def validate(self, **dict_args):
        self._process()
        self._errors = {}
        self._verified = {}
        self._ok = {}
        self._ignored = {}
        for key in dict_args:
            new_value = dict_args[key]
            if key in self._widgets and key in self.fields:
                if key in self.custom_validates:
                    if callable(self.custom_validates):
                        r = self.custom_validates[Field_instance.name](new_value)
                        if len(r) == 2 and isinstance(r, (tuple, list)):
                            if r[1] is not None:
                                self._errors[key] = r[1]
                            else:
                                self._ok[key] = dict_args[key]
                        else:
                            raise ValueError("The custom validate must return tuple or list with 2 values")
                    else:
                        raise ValueError("The custom_validate must be callable.")
                else:
                    w = self._widgets[key]
                    if ("type" in w) and w["type"] == "reference":
                        
                        t_name = w['reference_table']
                        f_name = w['reference_field']
                        if "editable" in w and w["editable"]:
                            if isinstance(new_value, str) and ref_values.match(new_value):
                                v_splited = "".join(new_value.split(":")[1:])
                                id_ = 0
                                q = self._db(self._db[t_name][f_name] == v_splited).select().first()
                                if q:
                                    id_ = q.id
                                else:
                                    id_ = self._db[t_name].insert(**{f_name: v_splited})
                                    q = self._db(self._db[t_name]['id'] == id_).select().first()
                                    q.update_record()
                                    self._db.commit()
                                if id_:
                                    dict_args[key] = id_
                                    self._ok[key] = dict_args[key]
                                else:
                                    me = w.get("message_error", "The new value for some reason cannot be added.")
                                    self._errors[key] = me
                            else:
                                if self.table[key].validate(new_value)[1] is not None:
                                    self._errors[key] = self.table[key].validate(new_value)[1]

                        else:
                            if self.table[key].validate(new_value)[1] is not None:
                                self._errors[key] = self.table[key].validate(new_value)[1]
                        if dict_args[key]:
                            self._verified[key] = int(dict_args[key])
                        else:
                            self._verified[key] = None
                    elif ("type" in w) and (w["type"] == "date" or w["type"] == "datetime" or w["type"] == "time"):
                        t = w["type"]
                        if dict_args[key]:
                            if t == "datetime":
                                validator_format = w.get("validator_format", '%Y-%m-%d %H:%M:%S')
                                tempo = time.strptime(str(dict_args[key]), validator_format)
                                resultado = time.strftime('%Y-%m-%d %H:%M:%S', tempo)
                            elif t == "date":
                                validator_format = w.get("validator_format", '%Y-%m-%d')
                                tempo = time.strptime(str(dict_args[key]), validator_format)
                                resultado = time.strftime('%Y-%m-%d', tempo)
                            elif t == "time":
                                validator_format = w.get("validator_format", '%H:%M:%S')
                                tempo = time.strptime(str(dict_args[key]), validator_format)
                                resultado = time.strftime('%H:%M:%S', tempo)
                            self._verified[key] = resultado
                        else:
                            self._verified[key] = None

                    else:
                        if self.table[key].validate(new_value)[1] is not None:
                            self._errors[key] = self.table[key].validate(new_value)[1]
                        else:
                            self._ok[key] = dict_args[key]
                        if dict_args[key]:
                            self._verified[key] = dict_args[key]
                        else:
                            self._verified[key] = None

            else:
                self._ignored[key] = dict_args[key]
        return self._errors

    def update_or_insert(self, **dict_args):
        self._changed = {}
        val = self.validate(**dict_args)
        if val:
            return val
        else:
            if self.record_id:
                r = self._db(self._db[self.table._tablename]._id == self.record_id).select(
                    ).first().update_record(**self._verified)
                self._record = r
            else:
                r = self.table.insert(**self._verified)
                self._record = self.table[r]
                self.record_id = r
            for key in self._verified:
                if key in self._widgets and key in self.fields:
                    if self._verified[key] and 'value' in self._widgets[key] and self._widgets[key]['value']:
                        if self._widgets[key]['type'] == "reference":
                            if int(self._verified[key]) != int(self._widgets[key]['value']):
                                self._changed[key] = [self._verified[key], self._widgets[key]['value']]
                        elif self._widgets[key]['type'] == 'date' or\
                                self._widgets[key]['type'] == 'datetime' or self._widgets[key]['type'] == 'time':
                            if self._verified[key] != self._widgets[key]['value']:
                                self._changed[key] = [self._verified[key], self._widgets[key]['value']]
                        elif str(self._verified[key]) != str(self._widgets[key]['value']):
                            self._changed[key] = [self._verified[key], self._widgets[key]['value']]
                    elif (self._verified[key] and 'value' in self._widgets[key]) or ('value' in self._widgets[key] and self._widgets[key]['value']):
                        self._changed[key] = [self._verified[key], self._widgets[key]['value']]
                    self._widgets[key]['value'] = self._verified[key]
            self._db.commit()
            self._process()

    def _process(self):
        self.dict = {
            "table": self.table._tablename,
            "id": self.record_id,
            "data_view": self._data_view,
            "widgets": self.json_widgets
        }
        self._widgets = dict()
        section = dict()
        group = dict()
        for x in self.fields:
            if x in self.custom_phanterpwa:
                json_widget = WidgetFromFieldDALFromTableDAL(self.table, x, self.record_id, data_view=self._data_view, simple_widget=self.simple_form, custom_phanterpwa=self.custom_phanterpwa[x])
            else:
                json_widget = WidgetFromFieldDALFromTableDAL(self.table, x, self.record_id, data_view=self._data_view, simple_widget=self.simple_form)
            self._widgets[x] = json_widget.as_dict()
            if x is not "id" or self.record_id:
                if json_widget.section:
                    if json_widget.section in section:
                        section[json_widget.section][1][1].append(["widget", [x, json_widget.as_dict()]])
                    else:
                        section[json_widget.section] = ["section",
                            [json_widget.section, [["widget", [x, json_widget.as_dict()]]]]]
                        self.json_widgets.append(section[json_widget.section])
                elif json_widget.group:
                    if json_widget.group in group:
                        group[json_widget.group][1][1].append(["widget", [x, json_widget.as_dict()]])
                    else:
                        group[json_widget.group] = ["group", [json_widget.group,
                            [["widget", [x, json_widget.as_dict()]]]]]
                        self.json_widgets.append(group[json_widget.group])
                elif json_widget.out_of_form:
                    pass
                else:
                    self.json_widgets.append(["widget", [x, json_widget.as_dict()]])
        for e in self._extra_fields:
            # self.json_widgets[e] = self._extra_fields[e].as_dict()
            # self._widgets[x] = self.json_widgets[e].as_dict()
            json_widget = CustomField(self.table, self._extra_fields[e], self.record_id, self._data_view)
            #WidgetFromFieldDALFromTableDAL(self.table, x, self.record_id, data_view=self._data_view)
            self._widgets[e] = json_widget.as_dict()
            if x is not "id" or self.record_id:
                if json_widget.section:
                    if json_widget.section in section:
                        if json_widget.position or json_widget.position == 0:
                            section[json_widget.section][1][1].insert(json_widget.position, ["widget", [e, json_widget.as_dict()]])
                        else:
                            section[json_widget.section][1][1].append(["widget", [e, json_widget.as_dict()]])
                    else:
                        section[json_widget.section] = ["section",
                            [json_widget.section, [["widget", [e, json_widget.as_dict()]]]]]
                        self.json_widgets.append(section[json_widget.section])
                elif json_widget.group:
                    if json_widget.group in group:
                        if json_widget.position or json_widget.position == 0:
                            group[json_widget.group][1][1].insert(json_widget.position, ["widget", [e, json_widget.as_dict()]])
                        else:
                            group[json_widget.group][1][1].append(["widget", [e, json_widget.as_dict()]])
                    else:
                        group[json_widget.group] = ["group", [json_widget.group,
                            [["widget", [e, json_widget.as_dict()]]]]]
                        self.json_widgets.append(group[json_widget.group])
                elif json_widget.out_of_form:
                    pass
                else:
                    if json_widget.position or json_widget.position == 0:
                        self.json_widgets.insert(json_widget.position, ["widget", [e, json_widget.as_dict()]])
                    else:
                        self.json_widgets.append(["widget", [e, json_widget.as_dict()]])

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
                    INPUT(**{
                        "_id": "phanterpwa-widget-input-input-{0}-csrf_token".format(self.table_name),
                        "_name": "csrf_token",
                        "_data-validators": ['IS_NOT_EMPTY'],
                        "_data-form": self.table_name,
                        "_type": "hidden"
                    }),
                ),
                _id='phanterpwa-widget-input-input-{0}-csrf_token'.format(self.table_name),
                _class='phanterpwa-widget phanterpwa-widget-hidden e-display_hidden'
            ),
            _id="phanterpwa-widget-form-{0}".format(self.table_name),
            _class="phanterpwa-widget phanterpwa-widget-form",
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

    def insert(self, dbtable, commit=True):
        id_record = dbtable.insert(
            **self.dict_args
        )
        if id_record and commit:
            dbtable._db.commit()
            return id_record
        else:
            return None

    def update(self, dbtable, row_id, commit=True):
        id_record = dbtable[row_id].update_record(
            **self.dict_args
        )
        if id_record and commit:
            dbtable._db.commit()
            return id_record
        else:
            return None


    def validate_and_insert(self, dbtable, commit=True):
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
                raise "The dbtable must be pydal.DAL.Table instance. given: {0}.".format(type(dbtable))

    def validate_and_update(self, dbset, commit=True):
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
                raise "The dbtable must be pydal.Objects.Set instance. given: {0}.".format(type(dbset))
