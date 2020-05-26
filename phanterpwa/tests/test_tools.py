import os
import unittest
from phanterpwa.tools import (
    interpolate,
    sass_change_vars,
    sass_map_vars,
    config,
    text_normalize,
    string_escape,
    one_space,
    split_seconds,
    join_seconds,
    humanize_seconds
)
from phanterpwa.i18n import Translator

CURRENT_PATH = os.path.dirname(__file__)
my_translator = Translator(os.path.join(CURRENT_PATH, "test_tools_humanize_seconds"), "humanize_seconds")

SAMPLE_tools = """$STROKEWIDTH: 8px /*teste*/
$_BORDERRADIUS: 100%
$BORDERRADIUS: 100%
$border-dark: rgba($base-color, 0.88)
\t$SIM: #9px
$black: #000 !default
.phanterpwa-components-preloaders-android
  $STROKEWIDTH: 8px //teste
  $CONTAINERWIDTH: 60px
  // $NAO: 70
  /* $NAO2: 70 */
  *
    box-sizing: border-box
  .left
      float: left {{important}}
  .right
      float: right !important
  .preloader-wrapper
    display: inline-block
    position: relative
    width: {{no_var}}
    height: $CONTAINERWIDTH"""
SAMPLE_tools2 = """$STROKEWIDTH: 8px /*teste*/
$_BORDERRADIUS: 100%
$BORDERRADIUS: 100%
$border-dark: rgba($base-color, 0.88)
\t$SIM: #9px
$black: #000 !default
.phanterpwa-components-preloaders-android
  $STROKEWIDTH: 8px //teste
  $CONTAINERWIDTH: 60px
  // $NAO: 70
  /* $NAO2: 70 */
  *
    box-sizing: border-box
  .left
      float: left !important
  .right
      float: right !important
  .preloader-wrapper
    display: inline-block
    position: relative
    width: $CONTAINERWIDTH
    height: $CONTAINERWIDTH"""

SAMPLE_tools3 = """$STROKEWIDTH: 15px
$_BORDERRADIUS: 100%
$BORDERRADIUS: 100%
$border-dark: rgba($base-color, 0.88)
\t$SIM: #9px
$black: #000 !default
.phanterpwa-components-preloaders-android
  $STROKEWIDTH: 15px
  $CONTAINERWIDTH: 200px
  // $NAO: 70
  /* $NAO2: 70 */
  *
    box-sizing: border-box
  .left
      float: left !important
  .right
      float: right !important
  .preloader-wrapper
    display: inline-block
    position: relative
    width: $CONTAINERWIDTH
    height: $CONTAINERWIDTH"""


class TestTools(unittest.TestCase):
    def test01_interpolate(self):
        self.assertEqual(
            interpolate(SAMPLE_tools, {"no_var": "$CONTAINERWIDTH", "not_exist": "None", "important": "!important"}),
            SAMPLE_tools2
        )
        self.assertEqual(
            interpolate(SAMPLE_tools, {"no_var2": "$CONTAINERWIDTH", "not_exist2": "None", "important2": "!important"}),
            SAMPLE_tools
        )

    def test02_sass_map_vars(self):
        SAMPLE = {
            "STROKEWIDTH": "8px",
            "BORDERRADIUS": "100%",
            "_BORDERRADIUS": "100%",
            "border-dark": "rgba($base-color, 0.88)",
            "SIM": "#9px",
            "black": "#000 !default",
            "CONTAINERWIDTH": "60px"
        }
        res = sass_map_vars(SAMPLE_tools2)
        for x in res:
            self.assertEqual(
                SAMPLE[x],
                res[x]
            )

        self.assertEqual(
            sass_map_vars("ssdf dfdsd sdsdf\n sdfsdf"),
            {}
        )

    def test03_sass_change_vars(self):
        self.assertEqual(
            sass_change_vars(SAMPLE_tools2, {"STROKEWIDTH": "15px",
                "CONTAINERWIDTH": "200px", "NOT_EXIST": "600px"}),
            SAMPLE_tools3
        )
        self.assertEqual(
            sass_change_vars(SAMPLE_tools2, {"STROKEWIDTH2": "15px",
                "CONTAINERWIDTH2": "200px", "NOT_EXIST": "600px"}),
            SAMPLE_tools2
        )

    def test04_config(self):
        if os.path.exists(os.path.join(CURRENT_PATH, "subfolder", "config.json")):
            os.remove(os.path.join(CURRENT_PATH, "subfolder", "config.json"))
        if os.path.exists(os.path.join(CURRENT_PATH, "subfolder", "cfg.json")):
            os.remove(os.path.join(CURRENT_PATH, "subfolder", "cfg.json"))
        if os.path.exists(os.path.join(CURRENT_PATH, "test_folder")):
            import glob
            c = glob.glob(os.path.join(CURRENT_PATH, "test_folder", "*"))
            for x in c:
                os.remove(x)
            os.removedirs(os.path.join(CURRENT_PATH, "test_folder"))
        self.assertEqual(os.path.exists(os.path.join(CURRENT_PATH, "subfolder", "config.json")), False)
        self.assertEqual(os.path.exists(os.path.join(CURRENT_PATH, "subfolder", "cfg.json")), False)
        self.assertEqual(os.path.exists(os.path.join(CURRENT_PATH, "test_folder")), False)
        config(os.path.join(CURRENT_PATH, "test_folder"))
        self.assertEqual(os.path.exists(os.path.join(CURRENT_PATH, "test_folder.json")), True)
        os.remove(os.path.join(CURRENT_PATH, "test_folder.json"))
        self.assertEqual(os.path.exists(os.path.join(CURRENT_PATH, "test_folder.json")), False)
        config(os.path.join(CURRENT_PATH, "test_folder", "cfg.json"))
        self.assertEqual(os.path.exists(os.path.join(CURRENT_PATH, "test_folder", "cfg.json")), True)
        config(os.path.join(CURRENT_PATH, "test_folder", "cfg"))
        self.assertEqual(os.path.exists(os.path.join(CURRENT_PATH, "test_folder", "cfg.json")), True)
        config(os.path.join(CURRENT_PATH, "test_folder", "cfgij"))
        self.assertEqual(os.path.exists(os.path.join(CURRENT_PATH, "test_folder", "cfgij.json")), True)
        config(os.path.join(CURRENT_PATH, "test_folder"))
        self.assertEqual(os.path.exists(os.path.join(CURRENT_PATH, "test_folder", "config.json")), True)
        content = {"teste": "one"}
        change = {"teste": "two", "new": "one"}
        acumulate = {"teste": "two", "new": "one", "just": "three"}
        res = config(os.path.join(CURRENT_PATH, "test_folder"), content)
        self.assertEqual(res, content)
        res = config(os.path.join(CURRENT_PATH, "test_folder"), change)
        self.assertEqual(res, change)
        res = config(os.path.join(CURRENT_PATH, "test_folder"), {"just": "three"})
        self.assertEqual(res, acumulate)
        res = config(os.path.join(CURRENT_PATH, "test_folder"), {"just": "three"}, rewrite=True)
        self.assertEqual(res, {"just": "three"})

    def test05_text_normalize(self):
        self.assertEqual(
            text_normalize("Maçã"),
            "MACA"
        )
        self.assertEqual(
            text_normalize("Maçã", False),
            "Maca"
        )

    def test06_string_escape(self):
        self.assertEqual(
            string_escape("<div>the content</div>"),
            '&lt;div&gt;the content&lt;/div&gt;'
        )
        result = string_escape({
            "one": "<div style='test'>one</div>",
            "two": ["<div>two</div>"],
            "three": ("<div>three</div>",),
            "four": {"<div>four</div>"},
            "five": {
                "five_one": ["<br>", ("<input>", "<hr>"), {"<a href='link'></a>"}]
            }
        })
        self.assertEqual(
            result["one"],
            '&lt;div style=&#39;test&#39;&gt;one&lt;/div&gt;'
        )
        self.assertEqual(
            result["two"],
            ["&lt;div&gt;two&lt;/div&gt;"]
        )
        self.assertEqual(
            result["three"],
            ["&lt;div&gt;three&lt;/div&gt;"]
        )
        self.assertEqual(
            result["four"],
            ['&lt;div&gt;four&lt;/div&gt;']
        )
        self.assertEqual(
            result["five"]["five_one"],
            ["&lt;br&gt;", ["&lt;input&gt;", "&lt;hr&gt;"], ["&lt;a href=&#39;link&#39;&gt;&lt;/a&gt;"]]
        )

    def test07_one_space(self):
        self.assertEqual(
            one_space("   My    long \r\n text. \tTabulation,      spaces,     spaces.         "),
            "My long text. Tabulation, spaces, spaces."
        )

    def test08_split_seconds(self):
        self.assertEqual(
            split_seconds(123456789),
            {'year': 3, 'month': 11, 'day': 3, 'hour': 21, 'minute': 33, 'second': 9}
        )
        self.assertEqual(
            split_seconds(121),
            {'minute': 2, 'second': 1}
        )
        self.assertEqual(
            split_seconds(3659),
            {'hour': 1, 'second': 59}
        )

    def test09_join_seconds(self):
        self.assertEqual(
            join_seconds({'year': 1, 'hour': 1, 'second': 1}),
            31539601
        )
        self.assertEqual(
            join_seconds({'year': 1, 'second': 3601}),
            31539601
        )
        self.assertEqual(
            join_seconds({'year': 1, 'minute': 60, 'second': 1}),
            31539601
        )

    def test10_humanize_seconds(self):
        self.assertEqual(
            humanize_seconds(123456789),
            '3 years, 11 months, 3 days, 21 hours, 33 minutes and 9 seconds'
        )
        self.assertEqual(
            humanize_seconds(121),
            '2 minutes and 1 second'
        )
        {'minute': 2, 'second': 1}
        self.assertEqual(
            humanize_seconds(3659),
            '1 hour and 59 seconds'
        )
        self.assertEqual(
            my_translator.translate("pt-BR", "year", "ano"),
            {"pt-BR": {"year": "ano"}}
        )
        self.assertEqual(
            my_translator.translate("pt-BR", "years", "anos"),
            {"pt-BR": {"years": "anos"}}
        )
        self.assertEqual(
            my_translator.translate("pt-BR", "month", "mês"),
            {"pt-BR": {"month": "mês"}}
        )
        self.assertEqual(
            my_translator.translate("pt-BR", "months", "meses"),
            {"pt-BR": {"months": "meses"}}
        )
        self.assertEqual(
            my_translator.translate("pt-BR", "day", "dia"),
            {"pt-BR": {"day": "dia"}}
        )
        self.assertEqual(
            my_translator.translate("pt-BR", "days", "dias"),
            {"pt-BR": {"days": "dias"}}
        )
        self.assertEqual(
            my_translator.translate("pt-BR", "hour", "hora"),
            {"pt-BR": {"hour": "hora"}}
        )
        self.assertEqual(
            my_translator.translate("pt-BR", "hours", "horas"),
            {"pt-BR": {"hours": "horas"}}
        )
        self.assertEqual(
            my_translator.translate("pt-BR", "minute", "minuto"),
            {"pt-BR": {"minute": "minuto"}}
        )
        self.assertEqual(
            my_translator.translate("pt-BR", "minutes", "minutos"),
            {"pt-BR": {"minutes": "minutos"}}
        )
        self.assertEqual(
            my_translator.translate("pt-BR", "second", "segundo"),
            {"pt-BR": {"second": "segundo"}}
        )
        self.assertEqual(
            my_translator.translate("pt-BR", "seconds", "segundos"),
            {"pt-BR": {"seconds": "segundos"}}
        )
        my_translator.direct_translation = "pt-BR"
        self.assertEqual(
            humanize_seconds(123456789, my_translator),
            '3 anos, 11 meses, 3 dias, 21 horas, 33 minutos and 9 segundos'
        )
        my_translator.direct_translation = "en-US"
        self.assertEqual(
            humanize_seconds(123456789, my_translator),
            '3 years, 11 months, 3 days, 21 hours, 33 minutes and 9 seconds'
        )
        self.assertEqual(
            humanize_seconds(3659, my_translator),
            '1 hour and 59 seconds'
        )
        my_translator.direct_translation = "pt-BR"
        self.assertEqual(
            humanize_seconds(3659, my_translator),
            '1 hora and 59 segundos'
        )
        my_translator.translate("pt-BR", "and ", "e ")
        self.assertEqual(
            humanize_seconds(3659, my_translator),
            '1 hora e 59 segundos'
        )

if __name__ == '__main__':
    unittest.main()
