import os
import unittest
from phanterpwa.tools import (
    interpolate,
    sass_change_vars,
    sass_map_vars,
    config
)

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


class TestHelpers(unittest.TestCase):
    def test1_interpolate(self):
        self.assertEqual(
            interpolate(SAMPLE_tools, {"no_var": "$CONTAINERWIDTH", "not_exist": "None", "important": "!important"}),
            SAMPLE_tools2
        )
        self.assertEqual(
            interpolate(SAMPLE_tools, {"no_var2": "$CONTAINERWIDTH", "not_exist2": "None", "important2": "!important"}),
            SAMPLE_tools
        )

    def test2_sass_map_vars(self):
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
        print(res)
        for x in res:
            self.assertEqual(
                SAMPLE[x],
                res[x]
            )

        self.assertEqual(
            sass_map_vars("ssdf dfdsd sdsdf\n sdfsdf"),
            {}
        )

    def test3_sass_change_vars(self):
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

    def test4_config(self):
        if os.path.exists("config.json"):
            os.remove("config.json")
        if os.path.exists("cfg.json"):
            os.remove("cfg.json")
        if os.path.exists("test_folder"):
            import glob
            c = glob.glob(os.path.join("test_folder", "*"))
            for x in c:
                os.remove(x)
            os.removedirs("test_folder")
        self.assertEqual(os.path.exists("config.json"), False)
        self.assertEqual(os.path.exists("cfg.json"), False)
        self.assertEqual(os.path.exists("test_folder"), False)
        config("test_folder")
        self.assertEqual(os.path.exists("test_folder.json"), True)
        os.remove("test_folder.json")
        self.assertEqual(os.path.exists("test_folder.json"), False)
        config(os.path.join("test_folder", "cfg.json"))
        self.assertEquals(os.path.exists(os.path.join("test_folder", "cfg.json")), True)
        config(os.path.join("test_folder", "cfg"))
        self.assertEquals(os.path.exists(os.path.join("test_folder", "cfg.json")), True)
        config(os.path.join("test_folder", "cfgij"))
        self.assertEquals(os.path.exists(os.path.join("test_folder", "cfgij.json")), True)
        config(os.path.join("test_folder"))
        self.assertEquals(os.path.exists(os.path.join("test_folder", "config.json")), True)
        content = {"teste": "one"}
        change = {"teste": "two", "new": "one"}
        acumulate = {"teste": "two", "new": "one", "just": "three"}
        res = config(os.path.join("test_folder"), content)
        self.assertEquals(res, content)
        res = config(os.path.join("test_folder"), change)
        self.assertEquals(res, change)
        res = config(os.path.join("test_folder"), {"just": "three"})
        self.assertEquals(res, acumulate)
        res = config(os.path.join("test_folder"), {"just": "three"}, rewrite=True)
        self.assertEquals(res, {"just": "three"})


if __name__ == '__main__':
    unittest.main()
