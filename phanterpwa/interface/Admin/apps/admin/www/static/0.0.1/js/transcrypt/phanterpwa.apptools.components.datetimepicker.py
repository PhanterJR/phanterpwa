from phanterpwa.apptools import helpers
from phanterpwa.apptools import validations
# pragmas

from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = String = setTimeout = Date = RegExp = \
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')


INPUT = helpers.XmlConstructor.tagger("input", True)
I = helpers.XmlConstructor.tagger("i")
DIV = helpers.XmlConstructor.tagger("div")
FORM = helpers.XmlConstructor.tagger("form")
SPAN = helpers.XmlConstructor.tagger("span")
XML = helpers.XML
HR = helpers.XmlConstructor.tagger("hr", True)
I18N = helpers.I18N


__pragma__('kwargs')


class Datepickers():

    def __init__(self, target_selector, **parameters):
        self._days = [
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday'
        ]
        self._ordinaries = [
            "st",
            "nd",
            "rd",
            "th"
        ]
        self._months = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December'
        ]
        self._times = [
            'hours',
            'minutes',
            'seconds'
        ]
        self.ordinaries = list(self._ordinaries)
        self.namespace = __new__(Date().getTime())
        self.target_selector = target_selector
        self.days = list(self._days)
        self.months = list(self._months)
        self.times = list(self._times)
        self.date_type = "datetime"
        self.debug = window.PhanterPWA.DEBUG
        if "debug" in parameters:
            self.debug = parameters["debug"]
        if "date_type" in parameters:
            self._date_type(parameters['date_type'])
        self.now = __new__(Date())
        self.selected_date = __new__(Date(self.now.getFullYear(), self.now.getMonth(), self.now.getDate()))
        self.current_date = __new__(Date(self.now.getFullYear(), self.now.getMonth(), 1))
        if jQuery(self.target_selector).length > 0:
            if jQuery(self.target_selector)[0].hasAttribute("phanterpwa-datetimepicker-iso"):
                phanterpwa_datetimepicker_iso = jQuery(self.target_selector).attr("phanterpwa-datetimepicker-iso")
                console.log(phanterpwa_datetimepicker_iso)

                self.selected_date = __new__(Date(phanterpwa_datetimepicker_iso))
                console.log(self.selected_date)
                self.current_date = __new__(Date(self._apply_format("yyyy-MM-01 HH:ss:mm")))
        self.format = "yyyy-MM-dd"
        if self.date_type == "datetime":
            self.format = "yyyy-MM-dd HH:ss:mm"
        if "format" in parameters:
            self.format = self._map_escape_str(parameters['format'])

        self.format_in = "yyyy-MM-dd HH:ss:mm"
        if "current_date" in parameters:
            if "format" in parameters:
                self._read_formated(parameters['current_date'])
            else:
                self._selected_date(parameters['current_date'])

        self.onChoice = None
        if "onChoice" in parameters:
            self.onChoice = parameters["onChoice"]

        if "id_input_target" in parameters:
            self.id_input_target = parameters['id_input_target']

            if jQuery(self.id_input_target).length > 0:
                if validations.check_datetime(
                        jQuery(self.id_input_target).val(), self.format, self.date_type):
                    self._read_formated(jQuery(self.id_input_target).val())
                    iso_format = self._apply_format("yyyy-MM-dd HH:ss:mm")
                    jQuery(self.target_selector).attr("phanterpwa-datetimepicker-iso", iso_format)

    def _onChoice(self):
        if self.onChoice is not None and self.onChoice is not js_undefined:
            iso_format = self._apply_format("yyyy-MM-dd HH:ss:mm")
            jQuery(self.target_selector).attr("phanterpwa-datetimepicker-iso", iso_format)
            __pragma__('jsiter')
            data = {
                'iso': iso_format,
                'formated': self._apply_format(self.format),
            }
            __pragma__('nojsiter')
            self.onChoice(data)
        else:
            iso_format = self._apply_format("yyyy-MM-dd HH:ss:mm")
            jQuery(self.target_selector).attr("phanterpwa-datetimepicker-iso", iso_format)
            if jQuery(self.id_input_target).length > 0:
                jQuery(self.id_input_target).val(self._apply_format(self.format)).focus()
            if self.debug:
                console.info(self._apply_format(self.format))

    # def _patterns_format(self, value):
    #     if len(str(value)) == 1:

    def _sanitize_i18ns(self, value):
        reserved_letters = {
            "d": "&#100;",
            "M": "&#77;",
            "t": "&#116;",
            "o": "&#111;",
            "y": "&#121;",
            "H": "&#72;",
            "m": "&#109;",
            "s": "&#115;"
        }
        for x in reserved_letters.keys():
            if x in value:
                value = value.replace(x, reserved_letters[x])
        return value

    def _map_escape_str(self, value):
        reserved_letters = {
            r"\d": "&#100;",
            r"\M": "&#77;",
            r"\t": "&#116;",
            r"\o": "&#111;",
            r"\y": "&#121;",
            r"\H": "&#72;",
            r"\m": "&#109;",
            r"\s": "&#115;"
        }
        for x in reserved_letters.keys():
            if x in value:
                value = value.replace(x, reserved_letters[x])
        return value

    def _unsanitize_str(self, value):
        htmls_codes = {
            "&#100;": "d",
            "&#77;": "M",
            "&#116;": "t",
            "&#111;": "o",
            "&#121;": "y",
            "&#72;": "H",
            "&#109;": "m",
            "&#115;": "s"
        }
        for x in htmls_codes.keys():
            if x in value:
                value = value.replace(x, htmls_codes[x])
        return value

    def _read_formated(self, value):
        filted_format = self.format
        filted_value = self._sanitize_i18ns(self._map_escape_str(value))
        if "dddd" in filted_format:
            p = "|".join([self._sanitize_i18ns(x) for x in self.days])
            r = "{0}".format(p)
            r = __new__(RegExp(r))
            console.error(r)
            filted_value = filted_value.js_replace(r, "")
            filted_format = filted_format.replace("dddd", "")

        if "ddd" in filted_format:
            p = "|".join([self._sanitize_i18ns(x[:3]) for x in self.days])
            r = "{0}".format(p)
            r = __new__(RegExp(r))
            filted_value = filted_value.js_replace(r, "")
            filted_format = filted_format.replace("ddd", "")

        if "MMMM" in filted_format:
            p = "|".join([self._sanitize_i18ns(x) for x in self.months])
            r = "{0}".format(p)
            r = __new__(RegExp(r))
            filted_value = filted_value.js_replace(r, "")
            filted_format = filted_format.replace("MMMM", "")

        if "MMM" in filted_format:
            p = "|".join([self._sanitize_i18ns(x[:3]) for x in self.months])
            r = "{0}".format(p)
            r = __new__(RegExp(r))
            filted_value = filted_value.js_replace(r, "")
            filted_format = filted_format.replace("MMM", "")

        if "do" in filted_format or "Mo" in filted_format:
            o = [self._sanitize_i18ns(x) for x in self.ordinaries]
            r = "1" + o[0] + "|2" + o[1] + "|3" + o[2] + "|[0-9]{1,2}" + o[3]
            r = __new__(RegExp(r))
            filted_value = filted_value.js_replace(r, "")
            filted_format = filted_format.replace("do", "").replace("Mo", "")

        if "tt" in filted_format:
            r = self._sanitize_i18ns("/PM|AM/")
            r = __new__(RegExp(r))
            filted_value = filted_value.js_replace(r, "")
            filted_format = filted_format.replace("tt", "")

        day = None
        month = None
        year = None
        hour = "00"
        minute = "00"
        second = "00"

        if "dd" in filted_format:
            ini = filted_format.indexOf("dd")
            day = filted_value[ini:ini + 2]
        else:
            raise ValueError("The format must be 'dd' in your pattern")

        if "MM" in filted_format:
            ini = filted_format.indexOf("MM")
            month = filted_value[ini:ini + 2]
        else:
            raise ValueError("The format must be 'MM' in your pattern")

        if "yyyy" in filted_format:
            ini = filted_format.indexOf("yyyy")
            year = filted_value[ini:ini + 4]
        else:
            raise ValueError("The format must be 'yyyy' in your pattern")

        if "HH" in filted_format:
            ini = filted_format.indexOf("HH")
            hour = filted_value[ini:ini + 2]
        else:
            if self.date_type == "datetime":
                raise ValueError("The datetime format must be 'HH' in your pattern")

        if "mm" in filted_format:
            ini = filted_format.indexOf("mm")
            minute = filted_value[ini:ini + 2]
        else:
            if self.date_type == "datetime":
                raise ValueError("The datetime format must be 'mm' in your pattern")

        if "ss" in filted_format:
            ini = filted_format.indexOf("ss")
            second = filted_value[ini:ini + 2]
        else:
            if self.date_type == "datetime":
                raise ValueError("The datetime format must be 'ss' in your pattern")
        self.selected_date = __new__(Date("{0}-{1}-{2} {3}:{4}:{5}".format(year, month, day, hour, minute, second)))
        self.current_date = __new__(Date("{0}-{1}-01 {2}:{3}:{4}".format(year, month, hour, minute, second)))

    def _apply_format(self, value):
        smonth = self.selected_date.getMonth()
        sday = self.selected_date.getDate()
        sweek = self.selected_date.getDay()
        syear = self.selected_date.getFullYear()
        shour = self.selected_date.getHours()
        sminute = self.selected_date.getMinutes()
        ssecond = self.selected_date.getSeconds()

        if "dddd" in value:
            value = value.replace("dddd", self._sanitize_i18ns(self.days[sweek]))
        if "ddd" in value:
            value = value.replace("ddd", self._sanitize_i18ns(self.days[sweek][0:3]))
        if "dd" in value:
            value = value.replace("dd", self._zfill(sday, 2))
        if "do" in value:
            if sday == 1:
                ordi = self.ordinaries[0]
            elif sday == 2:
                ordi = self.ordinaries[1]
            elif sday == 3:
                ordi = self.ordinaries[2]
            else:
                ordi = self.ordinaries[3]
            nordi = "{0}{1}".format(sday, self._sanitize_i18ns(ordi))
            value = value.replace("do", nordi)

        if "MMMM" in value:
            value = value.replace("MMMM", self._sanitize_i18ns(self.months[smonth]))
        if "MMM" in value:
            value = value.replace("MMM", self._sanitize_i18ns(self.months[smonth][0:3]))
        if "MM" in value:
            console.log(smonth)
            value = value.replace("MM", self._zfill(smonth + 1, 2))
        if "Mo" in value:
            if (smonth + 1) == 1:
                ordi = self.ordinaries[0]
            elif (smonth + 1) == 2:
                ordi = self.ordinaries[1]
            elif (smonth + 1) == 3:
                ordi = self.ordinaries[2]
            else:
                ordi = self.ordinaries[3]
            nordi = "{0}{1}".format(smonth + 1, self._sanitize_i18ns(ordi))
            value = value.replace("Mo", nordi)

        if "yyyy" in value:
            value = value.replace("yyyy", syear)

        if "HH" in value:
            value = value.replace("HH", self._zfill(shour, 2))

        if "mm" in value:
            value = value.replace("mm", self._zfill(sminute, 2))

        if "ss" in value:
            value = value.replace("ss", self._zfill(ssecond, 2))

        AM_PM = "PM"
        if shour < 12:
            AM_PM = "AM"

        if "tt" in value:
            value = value.replace("tt", AM_PM)
        return self._unsanitize_str(value)

    def _zfill(self, number, size):
        console.log(number)
        number = int(number)
        number = str(number)
        s = number
        for x in range(size - len(number)):
            s = "0" + s
        return s

    def _date_type(self, value):
        if value != "datetime" and value != "date":
            raise ValueError(
                "The date_type must be 'datetime' or 'date'. Given '{0}'".format(value)
            )
        self.date_type = value

    def _selected_date(self, value):
        if self.date_type == "date":
            REGEX_BODY = __pragma__(
                'js',
                '{}',
                r'/^([0-9]{4}-[0-9]{2}-[0-9]{2})/'
            )
            if REGEX_BODY.test(value):
                self.selected_date = __new__(Date("{0} 00:00:00".format(value[0:10])))
                self.current_date = __new__(Date("{0}01 00:00:00".format(value[0:8])))
            else:
                raise ValueError("The current_date must be 'yyyy-mm-dd'. Example: 2019-01-01")

        elif self.date_type == "datetime":
            REGEX_BODY = __pragma__(
                'js',
                '{}',
                r'/^([0-9]{4}-[0-9]{2}-[0-9]{2}.{1}[0-9]{2}:[0-9]{2}:[0-9]{2})/'
            )
            if REGEX_BODY.test(value):
                self.selected_date = __new__(Date("{0} {1}".format(value[0:10], value[11:19])))
                self.current_date = __new__(Date("{0}01 {1}".format(value[0:8], value[11:19])))
            else:
                raise ValueError("The current_date must be 'yyyy-mm-dd'. Example: 2019-01-01")
        else:
            raise ValueError(
                "The date_type must be 'datetime' or 'date'. Given '{0}'".format(value)
            )

    def previus_year(self):
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        cmonth = self.current_date.getMonth()
        cday = self.current_date.getDate()
        cyear = self.current_date.getFullYear()
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear - 1,
            self._zfill(cmonth + 1, 2),
            self._zfill(cday, 2),
            self._zfill(chour, 2),
            self._zfill(cminute, 2),
            self._zfill(csecond, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def next_year(self):
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        cmonth = self.current_date.getMonth()
        cday = self.current_date.getDate()
        cyear = self.current_date.getFullYear()
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear + 1,
            self._zfill(cmonth + 1, 2),
            self._zfill(cday, 2),
            self._zfill(chour, 2),
            self._zfill(cminute, 2),
            self._zfill(csecond, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def previus_month(self):
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        cmonth = self.current_date.getMonth()
        cyear = self.current_date.getFullYear()
        calc_month = cmonth - 1
        if calc_month < 0:
            calc_month = 11
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear,
            self._zfill(calc_month + 1, 2),
            self._zfill(1, 2),
            self._zfill(chour, 2),
            self._zfill(cminute, 2),
            self._zfill(csecond, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def next_month(self):
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        cmonth = self.current_date.getMonth()
        cyear = self.current_date.getFullYear()
        calc_month = cmonth + 1
        if calc_month > 11:
            calc_month = 0
        sdate = self.selected_date.toJSON()
        snew_date = "{0} {1}:{2}:{3}".format(
            sdate[0:10],
            self._zfill(chour, 2),
            self._zfill(cminute, 2),
            self._zfill(csecond, 2),
        )
        self.selected_date = __new__(Date(snew_date))
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear,
            self._zfill(calc_month + 1, 2),
            self._zfill(1, 2),
            self._zfill(chour, 2),
            self._zfill(cminute, 2),
            self._zfill(csecond, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def previus_hour(self):
        cyear = self.current_date.getFullYear()
        cmonth = self.current_date.getMonth()
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        calc_hour = chour - 1
        if calc_hour < 0:
            calc_hour = 23
        sdate = self.selected_date.toJSON()
        snew_date = "{0} {1}:{2}:{3}".format(
            sdate[0:10],
            self._zfill(calc_hour, 2),
            self._zfill(cminute, 2),
            self._zfill(csecond, 2),
        )
        self.selected_date = __new__(Date(snew_date))
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear,
            self._zfill(cmonth + 1, 2),
            self._zfill(1, 2),
            self._zfill(calc_hour, 2),
            self._zfill(cminute, 2),
            self._zfill(csecond, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def next_hour(self):
        cyear = self.current_date.getFullYear()
        cmonth = self.current_date.getMonth()
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        calc_hour = chour + 1
        if calc_hour > 23:
            calc_hour = 0
        sdate = self.selected_date.toJSON()
        snew_date = "{0} {1}:{2}:{3}".format(
            sdate[0:10],
            self._zfill(calc_hour, 2),
            self._zfill(cminute, 2),
            self._zfill(csecond, 2),
        )
        self.selected_date = __new__(Date(snew_date))
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear,
            self._zfill(cmonth + 1, 2),
            self._zfill(1, 2),
            self._zfill(calc_hour, 2),
            self._zfill(cminute, 2),
            self._zfill(csecond, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def previus_minute(self):
        cyear = self.current_date.getFullYear()
        cmonth = self.current_date.getMonth()
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        calc_minute = cminute - 1
        if calc_minute < 0:
            calc_minute = 59
        sdate = self.selected_date.toJSON()
        snew_date = "{0} {1}:{2}:{3}".format(
            sdate[0:10],
            self._zfill(chour, 2),
            self._zfill(calc_minute, 2),
            self._zfill(csecond, 2),
        )
        self.selected_date = __new__(Date(snew_date))
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear,
            self._zfill(cmonth + 1, 2),
            self._zfill(1, 2),
            self._zfill(chour, 2),
            self._zfill(calc_minute, 2),
            self._zfill(csecond, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def next_minute(self):
        cyear = self.current_date.getFullYear()
        cmonth = self.current_date.getMonth()
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        calc_minute = cminute + 1
        if calc_minute > 59:
            calc_minute = 0
        sdate = self.selected_date.toJSON()
        snew_date = "{0} {1}:{2}:{3}".format(
            sdate[0:10],
            self._zfill(chour, 2),
            self._zfill(calc_minute, 2),
            self._zfill(csecond, 2),
        )
        self.selected_date = __new__(Date(snew_date))
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear,
            self._zfill(cmonth + 1, 2),
            self._zfill(1, 2),
            self._zfill(chour, 2),
            self._zfill(calc_minute, 2),
            self._zfill(csecond, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def previus_second(self):
        cyear = self.current_date.getFullYear()
        cmonth = self.current_date.getMonth()
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        calc_second = csecond - 1
        if calc_second < 0:
            calc_second = 59
        sdate = self.selected_date.toJSON()
        snew_date = "{0} {1}:{2}:{3}".format(
            sdate[0:10],
            self._zfill(chour, 2),
            self._zfill(cminute, 2),
            self._zfill(calc_second, 2),
        )
        self.selected_date = __new__(Date(snew_date))
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear,
            self._zfill(cmonth + 1, 2),
            self._zfill(1, 2),
            self._zfill(chour, 2),
            self._zfill(cminute, 2),
            self._zfill(calc_second, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def next_second(self):
        cyear = self.current_date.getFullYear()
        cmonth = self.current_date.getMonth()
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        calc_second = csecond + 1
        if calc_second > 59:
            calc_second = 0
        sdate = self.selected_date.toJSON()
        snew_date = "{0} {1}:{2}:{3}".format(
            sdate[0:10],
            self._zfill(chour, 2),
            self._zfill(cminute, 2),
            self._zfill(calc_second, 2),
        )
        self.selected_date = __new__(Date(snew_date))
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear,
            self._zfill(cmonth + 1, 2),
            self._zfill(1, 2),
            self._zfill(chour, 2),
            self._zfill(cminute, 2),
            self._zfill(calc_second, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def set_year(self, value):
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        REGEX_BODY = __pragma__(
            'js',
            '{}',
            r'/^([0-9]{4})/'
        )
        if REGEX_BODY.test(value):
            cmonth = self.current_date.getMonth()
            new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
                value,
                self._zfill(cmonth + 1, 2),
                self._zfill(1, 2),
                self._zfill(chour, 2),
                self._zfill(cminute, 2),
                self._zfill(csecond, 2),
            )
            self.current_date = __new__(Date(new_date))
            self.start()

    def set_month(self, value):
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        cyear = self.current_date.getFullYear()
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear,
            self._zfill(int(value) + 1, 2),
            self._zfill(1, 2),
            self._zfill(chour, 2),
            self._zfill(cminute, 2),
            self._zfill(csecond, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def set_hour(self, value):
        cyear = self.current_date.getFullYear()
        cmonth = self.current_date.getMonth()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        sdate = self.selected_date.toJSON()
        snew_date = "{0} {1}:{2}:{3}".format(
            sdate[0:10],
            self._zfill(int(value), 2),
            self._zfill(cminute, 2),
            self._zfill(csecond, 2),
        )
        self.selected_date = __new__(Date(snew_date))
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear,
            self._zfill(cmonth + 1, 2),
            self._zfill(1, 2),
            self._zfill(int(value), 2),
            self._zfill(cminute, 2),
            self._zfill(csecond, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def set_minute(self, value):
        cyear = self.current_date.getFullYear()
        cmonth = self.current_date.getMonth()
        chour = self.current_date.getHours()
        csecond = self.current_date.getSeconds()
        sdate = self.selected_date.toJSON()
        snew_date = "{0} {1}:{2}:{3}".format(
            sdate[0:10],
            self._zfill(chour, 2),
            self._zfill(value, 2),
            self._zfill(csecond, 2),
        )
        self.selected_date = __new__(Date(snew_date))
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear,
            self._zfill(cmonth + 1, 2),
            self._zfill(1, 2),
            self._zfill(chour, 2),
            self._zfill(value, 2),
            self._zfill(csecond, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def set_second(self, value):
        cyear = self.current_date.getFullYear()
        cmonth = self.current_date.getMonth()
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        sdate = self.selected_date.toJSON()
        snew_date = "{0} {1}:{2}:{3}".format(
            sdate[0:10],
            self._zfill(chour, 2),
            self._zfill(cminute, 2),
            self._zfill(value, 2),
        )
        self.selected_date = __new__(Date(snew_date))
        new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
            cyear,
            self._zfill(cmonth + 1, 2),
            self._zfill(1, 2),
            self._zfill(chour, 2),
            self._zfill(cminute, 2),
            self._zfill(value, 2),
        )
        self.current_date = __new__(Date(new_date))
        self.start()

    def set_selected(self, jsonDate):
        new_date = __new__(Date(jsonDate))
        self.selected_date = new_date
        self._onChoice()
        self.close()

    def show_months(self):
        container = DIV(
            _class='phanterpwa_datetimepicker_monthlist_container'
        )

        def _month(el):
            m = jQuery(el).attr('phanterpwa_datetimepicker_month')
            self.set_month(m)
        cmonth = self.current_date.getMonth()
        row_container = DIV(_class="phanterpwa_datetimepicker_row")
        for x in range(12):
            add_class = ""
            if cmonth == x:
                add_class = " selected"
            row_container.append(
                DIV(
                    I18N(self.months[x]),
                    _class="phanterpwa_datetimepicker_monthlist_month phanterpwa_datetimepicker_button{0}".format(
                        add_class
                    ),
                    _phanterpwa_datetimepicker_month=x

                )
            )
        container.append(row_container)
        # jQuery('#phanterpwa_datetimepicker_calendar_{0}'.format(self.namespace)).html("").append(container.xml())
        container.html_to('#phanterpwa_datetimepicker_calendar_{0}'.format(self.namespace))
        jQuery(
            '#phanterpwa_datetimepicker_calendar_{0} .phanterpwa_datetimepicker_monthlist_month'.format(self.namespace)
        ).on(
            'click',
            lambda: _month(this)
        )

    def show_years(self, inicial_year=None):
        container = DIV(
            _class='phanterpwa_datetimepicker_yearlist_container'
        )

        def _year(el):
            m = jQuery(el).attr('phanterpwa_datetimepicker_year')
            self.set_year(m)

        row_container = DIV(_class="phanterpwa_datetimepicker_row")
        cyear = self.current_date.getFullYear()
        if inicial_year is None:
            inicial_year = cyear - 17
        final_year = inicial_year + 35
        for x in range(inicial_year, final_year):
            add_class = ""
            if cyear == x:
                add_class = " selected"
            row_container.append(
                DIV(
                    x,
                    _class="phanterpwa_datetimepicker_yearlist_year phanterpwa_datetimepicker_button{0}".format(
                        add_class
                    ),
                    _phanterpwa_datetimepicker_year=x

                )
            )
        container.append(row_container)
        # jQuery('#phanterpwa_datetimepicker_month_and_calendar_{0}'.format(
        #     self.namespace)).html("").append(container.xml())
        container.html_to('#phanterpwa_datetimepicker_month_and_calendar_{0}'.format(
            self.namespace))
        jQuery(
            '#phanterpwa_datetimepicker_month_and_calendar_{0} .phanterpwa_datetimepicker_yearlist_year'.format(
                self.namespace)
        ).on(
            'click',
            lambda: _year(this)
        )
        jQuery(
            '#phanterpwa_datetimepicker_prev_year_{0}'.format(self.namespace)
        ).html(
            DIV(I(_class="fas fa-angle-double-left"), _class="phanterpwa_datetimepicker_button").xml()
        ).off(
            "click.phanterpwa_datetimepicker_prev_year"
        ).on(
            "click.phanterpwa_datetimepicker_prev_year",
            lambda: self.show_years(inicial_year - 35)
        )
        jQuery(
            '#phanterpwa_datetimepicker_next_year_{0}'.format(self.namespace)
        ).html(
            DIV(I(_class="fas fa-angle-double-right"), _class="phanterpwa_datetimepicker_button").xml()
        ).off(
            "click.phanterpwa_datetimepicker_next_year"
        ).on(
            "click.phanterpwa_datetimepicker_next_year",
            lambda: self.show_years(inicial_year + 35)
        )

    def show_hours(self):
        container = DIV(
            _class='phanterpwa_datetimepicker_hourlist_container'
        )

        def _hour(el):
            m = jQuery(el).attr('phanterpwa_datetimepicker_hour')
            self.set_hour(m)
        chour = self.current_date.getHours()
        row_container = DIV(_class="phanterpwa_datetimepicker_row")
        for x in range(24):
            add_class = ""
            if chour == x:
                add_class = " selected"
            row_container.append(
                DIV(
                    self._zfill(x, 2),
                    _class="phanterpwa_datetimepicker_hourlist_hour phanterpwa_datetimepicker_button{0}".format(
                        add_class
                    ),
                    _phanterpwa_datetimepicker_hour=x

                )
            )
        container.append(row_container)
        jQuery('#phanterpwa_datetimepicker_calendar_month_years_{0}'.format(
            self.namespace)).html("").append(container.xml())
        jQuery(
            '#phanterpwa_datetimepicker_calendar_month_years_{0} .phanterpwa_datetimepicker_hourlist_hour'.format(
                self.namespace
            )
        ).on(
            'click',
            lambda: _hour(this)
        )

    def show_minutes(self):
        container = DIV(
            _class='phanterpwa_datetimepicker_minutelist_container'
        )

        def _minute(el):
            m = jQuery(el).attr('phanterpwa_datetimepicker_minute')
            self.set_minute(m)
        cminute = self.current_date.getMinutes()
        row_container = DIV(_class="phanterpwa_datetimepicker_row")
        for x in range(60):
            add_class = ""
            if cminute == x:
                add_class = " selected"
            row_container.append(
                DIV(
                    self._zfill(x, 2),
                    _class="phanterpwa_datetimepicker_minutelist_minute phanterpwa_datetimepicker_button{0}".format(
                        add_class
                    ),
                    _phanterpwa_datetimepicker_minute=x

                )
            )
        container.append(row_container)
        # jQuery('#phanterpwa_datetimepicker_calendar_month_years_{0}'.format(
        #     self.namespace)).html("").append(container.xml())
        container.html_to('#phanterpwa_datetimepicker_calendar_month_years_{0}'.format(
            self.namespace))
        jQuery(
            '#phanterpwa_datetimepicker_calendar_month_years_{0} .phanterpwa_datetimepicker_minutelist_minute'.format(
                self.namespace)
        ).on(
            'click',
            lambda: _minute(this)
        )

    def show_seconds(self):
        container = DIV(
            _class='phanterpwa_datetimepicker_secondlist_container'
        )

        def _second(el):
            m = jQuery(el).attr('phanterpwa_datetimepicker_second')
            self.set_second(m)
        csecond = self.current_date.getSeconds()
        row_container = DIV(_class="phanterpwa_datetimepicker_row")
        for x in range(60):
            add_class = ""
            if csecond == x:
                add_class = " selected"
            row_container.append(
                DIV(
                    self._zfill(x, 2),
                    _class="phanterpwa_datetimepicker_secondlist_second phanterpwa_datetimepicker_button{0}".format(
                        add_class
                    ),
                    _phanterpwa_datetimepicker_second=x

                )
            )
        container.append(row_container)
        # jQuery('#phanterpwa_datetimepicker_calendar_month_years_{0}'.format(
        #     self.namespace)).html("").append(container.xml())
        container.html_to('#phanterpwa_datetimepicker_calendar_month_years_{0}'.format(
            self.namespace))
        jQuery(
            '#phanterpwa_datetimepicker_calendar_month_years_{0} .phanterpwa_datetimepicker_secondlist_second'.format(
                self.namespace)
        ).on(
            'click',
            lambda: _second(this)
        )

    def close(self):
        jQuery(self.target_selector).find(".phanterpwa-fixed-fulldisplay").removeClass("enabled")

        def delete_datepicker():
            if not jQuery(self.target_selector).find(".phanterpwa-fixed-fulldisplay").hasClass("enabled"):
                jQuery(self.target_selector).find(".phanterpwa-fixed-fulldisplay").remove()
        setTimeout(
            delete_datepicker,
            500
        )

    def start(self):
        cont = 0
        cmonth = self.current_date.getMonth()
        cday = self.current_date.getDate()
        cweek = self.current_date.getDay()
        cyear = self.current_date.getFullYear()
        chour = self.current_date.getHours()
        cminute = self.current_date.getMinutes()
        csecond = self.current_date.getSeconds()
        smonth = self.selected_date.getMonth()
        sday = self.selected_date.getDate()
        sweek = self.selected_date.getDay()
        syear = self.selected_date.getFullYear()
        shour = self.selected_date.getHours()
        sminute = self.selected_date.getMinutes()
        ssecond = self.selected_date.getSeconds()
        nmonth = self.now.getMonth()
        nday = self.now.getDate()
        nyear = self.now.getFullYear()
        AM_PM = "PM"
        if shour < 12:
            AM_PM = "AM"

        container = DIV(
            _id='phanterpwa_datetimepicker_{0}'.format(self.namespace),
            _class='phanterpwa_datetimepicker_wrapper',
        )
        container_calendar_month_years = DIV(
            DIV(
                DIV(
                    DIV(
                        I(_class="fas fa-angle-left"),
                        _class="phanterpwa_datetimepicker_button"),
                    _class='phanterpwa_datetimepicker_previusnext',
                    _id='phanterpwa_datetimepicker_prev_year_{0}'.format(self.namespace)
                ),
                DIV(
                    DIV(
                        cyear,
                        _class='phanterpwa_datetimepicker_button',
                        _id='phanterpwa_datetimepicker_year_{0}'.format(self.namespace)
                    ),
                    _class='phanterpwa_datetimepicker_year',
                ),
                DIV(
                    DIV(
                        I(_class="fas fa-angle-right"),
                        _class="phanterpwa_datetimepicker_button"),
                    _class='phanterpwa_datetimepicker_previusnext',
                    _id='phanterpwa_datetimepicker_next_year_{0}'.format(self.namespace)
                ),
                _class='phanterpwa_datetimepicker_row'
            ),
            _id='phanterpwa_datetimepicker_calendar_month_years_{0}'.format(self.namespace),
        )
        hour_container = DIV(
            DIV(
                HR(),

                DIV(
                    DIV(
                        DIV(
                            I(_class="fas fa-angle-left"),
                            _class="phanterpwa_datetimepicker_button"),
                        _id='phanterpwa_datetimepicker_prev_hour_{0}'.format(self.namespace),
                        _class='phanterpwa_datetimepicker_previusnext'
                    ),
                    DIV(
                        DIV(
                            self._zfill(chour, 2),
                            _class='phanterpwa_datetimepicker_button',
                            _id='phanterpwa_datetimepicker_hour_{0}'.format(self.namespace)
                        ),
                        _class='phanterpwa_datetimepicker_hour',
                    ),
                    DIV(
                        DIV(
                            I(_class="fas fa-angle-right"),
                            _class="phanterpwa_datetimepicker_button"),
                        _id='phanterpwa_datetimepicker_next_hour_{0}'.format(self.namespace),
                        _class='phanterpwa_datetimepicker_previusnext'
                    ),
                    _class="phanterpwa_datetimepicker_time_col"
                ),
                DIV(
                    DIV(
                        DIV(
                            I(_class="fas fa-angle-left"),
                            _class="phanterpwa_datetimepicker_button"),
                        _id='phanterpwa_datetimepicker_prev_minute_{0}'.format(self.namespace),
                        _class='phanterpwa_datetimepicker_previusnext'
                    ),
                    DIV(
                        DIV(
                            self._zfill(cminute, 2),
                            _class='phanterpwa_datetimepicker_button',
                            _id='phanterpwa_datetimepicker_minute_{0}'.format(self.namespace)
                        ),
                        _class='phanterpwa_datetimepicker_minute',
                    ),
                    DIV(
                        DIV(
                            I(_class="fas fa-angle-right"),
                            _class="phanterpwa_datetimepicker_button"),
                        _id='phanterpwa_datetimepicker_next_minute_{0}'.format(self.namespace),
                        _class='phanterpwa_datetimepicker_previusnext'
                    ),
                    _class="phanterpwa_datetimepicker_time_col"
                ),
                DIV(
                    DIV(
                        DIV(
                            I(_class="fas fa-angle-left"),
                            _class="phanterpwa_datetimepicker_button"),
                        _id='phanterpwa_datetimepicker_prev_second_{0}'.format(self.namespace),
                        _class='phanterpwa_datetimepicker_previusnext'
                    ),
                    DIV(
                        DIV(
                            self._zfill(csecond, 2),
                            _class='phanterpwa_datetimepicker_button',
                            _id='phanterpwa_datetimepicker_second_{0}'.format(self.namespace)
                        ),
                        _class='phanterpwa_datetimepicker_second',
                    ),
                    DIV(
                        DIV(
                            I(_class="fas fa-angle-right"),
                            _class="phanterpwa_datetimepicker_button"),
                        _id='phanterpwa_datetimepicker_next_second_{0}'.format(self.namespace),
                        _class='phanterpwa_datetimepicker_previusnext'
                    ),
                    _class="phanterpwa_datetimepicker_time_col"
                ),
                DIV(
                    self.times[0],
                    _class="phanterpwa_datetimepicker_time_col label"
                ),
                DIV(
                    self.times[1],
                    _class="phanterpwa_datetimepicker_time_col label"
                ),
                DIV(
                    self.times[2],
                    _class="phanterpwa_datetimepicker_time_col label"
                ),
                _class="phanterpwa_datetimepicker_row"
            ),
            _class="phanterpwa_datetimepicker_time_container"
        )
        calendar_and_month = DIV(
            DIV(
                DIV(
                    DIV(
                        I(_class="fas fa-angle-left"),
                        _class="phanterpwa_datetimepicker_button"),
                    _id='phanterpwa_datetimepicker_prev_month_{0}'.format(self.namespace),
                    _class='phanterpwa_datetimepicker_previusnext'
                ),
                DIV(
                    DIV(
                        I18N(self.months[cmonth]),
                        _class='phanterpwa_datetimepicker_button',
                        _id='phanterpwa_datetimepicker_month_{0}'.format(self.namespace)
                    ),
                    _class='phanterpwa_datetimepicker_month',
                ),
                DIV(
                    DIV(
                        I(_class="fas fa-angle-right"),
                        _class="phanterpwa_datetimepicker_button"),
                    _id='phanterpwa_datetimepicker_next_month_{0}'.format(self.namespace),
                    _class='phanterpwa_datetimepicker_previusnext'
                ),
                _class='phanterpwa_datetimepicker_row'
            ),
            _id='phanterpwa_datetimepicker_month_and_calendar_{0}'.format(self.namespace)
        )
        container_calendar = DIV(
            DIV(
                DIV(
                    DIV(I18N(self.days[0][:3]), _class="phanterpwa_datetimepicker_unit"),
                    _class='phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Sunday'
                ),
                DIV(
                    DIV(I18N(self.days[1][:3]), _class="phanterpwa_datetimepicker_unit"),
                    _class='phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Monday'
                ),
                DIV(
                    DIV(I18N(self.days[2][:3]), _class="phanterpwa_datetimepicker_unit"),
                    _class='phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Tuesday'
                ),
                DIV(
                    DIV(I18N(self.days[3][:3]), _class="phanterpwa_datetimepicker_unit"),
                    _class='phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Wednesday'
                ),
                DIV(
                    DIV(I18N(self.days[4][:3]), _class="phanterpwa_datetimepicker_unit"),
                    _class='phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Thursday'
                ),
                DIV(
                    DIV(I18N(self.days[5][:3]), _class="phanterpwa_datetimepicker_unit"),
                    _class='phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Friday'
                ),
                DIV(
                    DIV(I18N(self.days[6][:3]), _class="phanterpwa_datetimepicker_unit"),
                    _class='phanterpwa_datetimepicker_weekday phanterpwa_datetimepicker_Saturday'
                ),
                _class='phanterpwa_datetimepicker_row',
            ),
            _id='phanterpwa_datetimepicker_calendar_{0}'.format(self.namespace),
        )
        row_days = DIV(_class='phanterpwa_datetimepicker_row')
        for y in range(cweek):
            row_days.append(
                DIV(_class="phanterpwa_datetimepicker_day_empty phanterpwa_datetimepicker_{0}".format(self.days[y]))
            )
        inicial_day = 1
        for x in range(40):
            if inicial_day < 32:
                cont += 1
                new_date = "{0}-{1}-{2} {3}:{4}:{5}".format(
                    cyear,
                    self._zfill(cmonth + 1, 2),
                    self._zfill(inicial_day, 2),
                    self._zfill(chour, 2),
                    self._zfill(cminute, 2),
                    self._zfill(csecond, 2),
                )
                d = __new__(Date(new_date))
                if (d.getMonth() == cmonth) and (d.toJSON() is not None):
                    add_class = ""
                    if (d.getMonth() == nmonth) and (d.getFullYear() == nyear) and (d.getDate() == nday):
                        add_class += " phanterpwa_datetimepicker_its_now"
                    if self.selected_date is not None:
                        if (d.getMonth() == smonth) and (d.getFullYear() == syear) and (d.getDate() == sday):
                            add_class += " phanterpwa_datetimepicker_selected"

                    row_days.append(
                        DIV(
                            DIV(
                                d.getDate(),
                                _id="phanterpwa_datetimepicker_unit_{0}".format(self.namespace),
                                _class="phanterpwa_datetimepicker_unit",
                                _phanterpwa_datetimepicker_date=new_date
                            ),
                            _class="phanterpwa_datetimepicker_day phanterpwa_datetimepicker_{0}{1}".format(
                                self._days[d.getDay()],
                                add_class
                            )
                        )
                    )
            inicial_day += 1
        container_calendar.append(row_days)
        calendar_and_month.append(container_calendar)
        container_calendar_month_years.append(calendar_and_month)
        container.append(container_calendar_month_years)
        container.append(hour_container)
        summary = DIV(
            DIV(
                I(_class="fas fa-times"),
                _class='phanterpwa-models-close'),
            DIV(
                DIV(
                    SPAN(self._zfill(sday, 2)), ", ", I18N(self.months[smonth]),
                    _id="phanterpwa_datetimepicker_summary_day_and_month_{0}".format(self.namespace),
                    _class="phanterpwa_datetimepicker_summary_day_and_month"
                ),
                DIV(
                    I18N(self.days[sweek]),
                    _id="phanterpwa_datetimepicker_summary_week_{0}".format(self.namespace),
                    _class="phanterpwa_datetimepicker_summary_week"
                ),
                DIV(
                    syear,
                    _id="phanterpwa_datetimepicker_summary_year_{0}".format(self.namespace),
                    _class="phanterpwa_datetimepicker_summary_year"
                ),
                DIV(
                    "{0}:{1}:{2} {3}".format(
                        self._zfill(shour, 2),
                        self._zfill(sminute, 2),
                        self._zfill(ssecond, 2),
                        AM_PM
                    ),
                    _id="phanterpwa_datetimepicker_summary_hour_{0}".format(self.namespace),
                    _class="phanterpwa_datetimepicker_summary_hour"
                ),
                _class="phanterpwa_datetimepicker_row"
            ),
            DIV(
                DIV(
                    DIV(
                        _id="phanterpwa_datetimepicker_summary_current_data_{0}".format(self.namespace),
                    ),
                    _class="phanterpwa_datetimepicker_row"
                ),
                _class="phanterpwa_datetimepicker_summary_current_data"
            ),
            _class="phanterpwa_datetimepicker_summary_container"
        )
        c_dt = ""
        if self.date_type == "date":
            c_dt = " phanterpwa_datetimepicker_is_not_datetime"

        datetimepicker_container = DIV(
            summary,
            container,
            _class="phanterpwa_datetimepicker_container{0}".format(c_dt)
        )

        centralizer = DIV(
            DIV(
                DIV(
                    DIV(
                        DIV(
                            datetimepicker_container,
                            _id="phanterpwa-centralizer-center-{0}".format(self.namespace),
                            _class="phanterpwa-centralizer-center"
                        ),
                        _class="phanterpwa-centralizer-horizontal"

                    ),
                    _class="phanterpwa-centralizer-vertical"
                ),
                _class="phanterpwa-centralizer-wrapper"
            ),
            _class="phanterpwa-fixed-fulldisplay"
        )

        def _selecting(el):
            v = jQuery(el).attr('phanterpwa_datetimepicker_date')
            self.set_selected(v)

        def open_panel(el):
            setTimeout(
                lambda: jQuery(self.target_selector).find(".phanterpwa-fixed-fulldisplay").addClass("enabled"),
                100
            )

        if jQuery(self.target_selector).has(".phanterpwa-fixed-fulldisplay").length == 1:
            # jQuery(self.target_selector).find(".phanterpwa-fixed-fulldisplay").remove()
            # # jQuery(self.target_selector).append(centralizer.xml())
            # centralizer.append_to(self.target_selector)
            datetimepicker_container.html_to("#phanterpwa-centralizer-center-{0}".format(self.namespace))
            jQuery(self.target_selector).find(".phanterpwa-fixed-fulldisplay").addClass("enabled")
        else:
            # jQuery(self.target_selector).append(centralizer.xml())
            centralizer.append_to(self.target_selector)
            open_panel()

        jQuery(
            '#phanterpwa_datetimepicker_prev_year_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_prev_year"
        ).on(
            "click.phanterpwa_datetimepicker_prev_year",
            lambda: self.previus_year()
        )
        jQuery(
            '#phanterpwa_datetimepicker_next_year_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_next_year"
        ).on(
            "click.phanterpwa_datetimepicker_next_year",
            lambda: self.next_year()
        )
        jQuery(
            '#phanterpwa_datetimepicker_prev_month_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_prev_month"
        ).on(
            "click.phanterpwa_datetimepicker_prev_month",
            lambda: self.previus_month()
        )
        jQuery(
            '#phanterpwa_datetimepicker_next_month_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_next_month"
        ).on(
            "click.phanterpwa_datetimepicker_next_month",
            lambda: self.next_month()
        )

        jQuery(
            '#phanterpwa_datetimepicker_prev_hour_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_prev_hour"
        ).on(
            "click.phanterpwa_datetimepicker_prev_hour",
            lambda: self.previus_hour()
        )
        jQuery(
            '#phanterpwa_datetimepicker_next_hour_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_next_hour"
        ).on(
            "click.phanterpwa_datetimepicker_next_hour",
            lambda: self.next_hour()
        )

        jQuery(
            '#phanterpwa_datetimepicker_prev_minute_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_prev_minute"
        ).on(
            "click.phanterpwa_datetimepicker_prev_minute",
            lambda: self.previus_minute()
        )
        jQuery(
            '#phanterpwa_datetimepicker_next_minute_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_next_minute"
        ).on(
            "click.phanterpwa_datetimepicker_next_minute",
            lambda: self.next_minute()
        )

        jQuery(
            '#phanterpwa_datetimepicker_prev_second_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_prev_second"
        ).on(
            "click.phanterpwa_datetimepicker_prev_second",
            lambda: self.previus_second()
        )
        jQuery(
            '#phanterpwa_datetimepicker_next_second_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_next_second"
        ).on(
            "click.phanterpwa_datetimepicker_next_second",
            lambda: self.next_second()
        )

        jQuery(
            '#phanterpwa_datetimepicker_month_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_month"
        ).on(
            "click.phanterpwa_datetimepicker_month",
            lambda: self.show_months()
        )
        jQuery(
            '#phanterpwa_datetimepicker_year_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_year"
        ).on(
            "click.phanterpwa_datetimepicker_year",
            lambda: self.show_years()
        )
        jQuery(
            '#phanterpwa_datetimepicker_hour_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_hour"
        ).on(
            "click.phanterpwa_datetimepicker_hour",
            lambda: self.show_hours()
        )

        jQuery(
            '#phanterpwa_datetimepicker_minute_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_minute"
        ).on(
            "click.phanterpwa_datetimepicker_minute",
            lambda: self.show_minutes()
        )

        jQuery(
            '#phanterpwa_datetimepicker_second_{0}'.format(self.namespace)
        ).off(
            "click.phanterpwa_datetimepicker_second"
        ).on(
            "click.phanterpwa_datetimepicker_second",
            lambda: self.show_seconds()
        )

        jQuery(
            '#phanterpwa_datetimepicker_calendar_{0} {1} .phanterpwa_datetimepicker_unit'.format(
                self.namespace, '.phanterpwa_datetimepicker_day'
            )
        ).on(
            'click',
            lambda: _selecting(this)
        )
        jQuery(
            '#phanterpwa_datetimepicker_calendar_{0} {1} .phanterpwa_datetimepicker_unit'.format(
                self.namespace, '.phanterpwa_datetimepicker_day'
            )
        ).on(
            'click',
            lambda: _selecting(this)
        )
        jQuery(
            ".phanterpwa_datetimepicker_summary_container .phanterpwa-models-close"
        ).on("click", lambda: self.close())


__pragma__('nokwargs')
