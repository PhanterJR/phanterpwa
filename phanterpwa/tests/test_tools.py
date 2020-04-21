import os
import unittest
from phanterpwa.tools import (
    interpolate,
    sass_change_vars,
    sass_map_vars,
    config
)

CURRENT_PATH = os.path.dirname(__file__)

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


if __name__ == '__main__':
    unittest.main()
