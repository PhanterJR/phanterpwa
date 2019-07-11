import unittest
import os
import glob
from phanterpwa.i18n import (
    Translator
)

sample1 = """[
  "hello world!"
]"""

sample2 = """{
  "hello world!": "hello world!"
}"""

sample4 = """{
  "abacaxi": "abacaxi",
  "hello world!": "hello world!"
}"""

sample5 = """{
  "abacaxi": "pineapple",
  "hello world!": "hello world!"
}"""


files = glob.glob(os.path.join("test_i18n_languages", "*.json"))
for x in files:
    os.remove(x)


class TestI18n(unittest.TestCase):
    def test1_created_file(self):
        Trans = Translator("test_i18n_languages")
        self.assertTrue(os.path.exists("test_i18n_languages"))
        self.assertTrue(os.path.exists(os.path.join("test_i18n_languages", "entries.json")))
        Trans.add_language("pt-BR")
        self.assertTrue(os.path.exists(os.path.join("test_i18n_languages", "pt-BR.json")))

    def test2_persistence(self):
        if os.path.exists(os.path.join("test_i18n_languages", "entries.json")):
            os.remove(os.path.join("test_i18n_languages", "entries.json"))
        # Test create a new entries.json
        Trans = Translator("test_i18n_languages")
        if os.path.exists(os.path.join("test_i18n_languages", "pt-PT.json")):
            os.remove(os.path.join("test_i18n_languages", "pt-PT.json"))
        # Test create a new pt-PT.json
        Trans.add_language("pt-PT")
        # Test add entrie without save
        Trans.T("hello world!")
        with open(os.path.join("test_i18n_languages", "entries.json"), "r") as f:
            self.assertEqual(f.readlines(), ['[]'])
        with open(os.path.join("test_i18n_languages", "pt-PT.json"), "r") as f:
            self.assertEqual(f.readlines(), ['{}'])
        Trans.save()
        # Test entrie after save
        with open(os.path.join("test_i18n_languages", "entries.json"), "r") as f:
            self.assertEqual(f.read(), sample1)
        with open(os.path.join("test_i18n_languages", "pt-PT.json"), "r") as f:
            self.assertEqual(f.read(), sample2)

    def test3_attr_translate(self):
        if os.path.exists(os.path.join("test_i18n_languages", "en-US.json")):
            os.remove(os.path.join("test_i18n_languages", "en-US.json"))
        Trans = Translator("test_i18n_languages")
        # Translate just en-US language
        Trans.translate("en-US", "abacaxi", "pineapple")
        Trans.save()
        # abacaxi translate is abacaxi
        with open(os.path.join("test_i18n_languages", "pt-BR.json"), "r") as f:
            self.assertEqual(f.read(), sample4)
        with open(os.path.join("test_i18n_languages", "pt-PT.json"), "r") as f:
            self.assertEqual(f.read(), sample4)
        # abacaxi translate is pineapple
        with open(os.path.join("test_i18n_languages", "en-US.json"), "r") as f:
            self.assertEqual(f.read(), sample5)

    def test4_attr_translator(self):
        Trans = Translator("test_i18n_languages")
        self.assertEqual("dont exists", Trans.translator("dont exists", "pt-BR"))
        self.assertEqual("abacaxi", Trans.translator("abacaxi", "pt-BR"))
        self.assertEqual("pineapple", Trans.translator("abacaxi", "en-US"))




if __name__ == '__main__':
    unittest.main()
