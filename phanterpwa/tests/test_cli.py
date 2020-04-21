# -*- coding: utf-8 -*-
import unittest
import os

# from phanterpwa.interface import (
#     cli
# )

# CURRENT_PATH = os.path.dirname(__file__)


# class TestCli(unittest.TestCase):

#     def test_Projects(self):
#         projects = cli.Projects(os.path.join(CURRENT_PATH, "test_cli_projects"))


    #     html_to_xmlconstructor_instance = HtmlToXmlConstructor("<html><head><meta charset=\"UTF-8\"></head><body><nav class=\"navbar\"><buttom>start</buttom></nav><main id=\"my_content\"><div class=\"row\"><div>my content</div></div></main></body></html>")

    #     self.assertEqual(
    #         html_to_xmlconstructor_instance.xmlconstructor_code(),
    #         sample_example_1
    #     )
    #     html_to_xmlconstructor_instance = HtmlToXmlConstructor("<div data-dict=\"i am in dict\" class=\"my_class\">content1</div><div class=\"my_class\">content2</div>")
    #     self.assertEqual(
    #         html_to_xmlconstructor_instance.xmlconstructor_code(),
    #         sample_example_2
    #     )
    #     html_to_xmlconstructor_instance = HtmlToXmlConstructor(sample)
    #     self.assertEqual(
    #         html_to_xmlconstructor_instance.xml(),
    #         sample
    #     )
    #     self.assertEqual(
    #         force_minify_string_content(html_to_xmlconstructor_instance).xml(),
    #         sample2
    #     )
    #     self.assertEqual(
    #         force_minify_string_content(html_to_xmlconstructor_instance).xmlconstructor_code(),
    #         sample3
    #     )

    # def test1_html_to_xmlconstructor(self):
    #     invert = HtmlToXmlConstructor(sample_html_to_xmlconstructor)
    #     self.assertEqual(invert.xml(), sample_html_to_xmlconstructor)
    #     invert.src_attr_dict = False
    #     self.assertRaises(ValueError, lambda: invert.source_code())
    #     invert.src_attr_dict = None
    #     self.assertTrue(isinstance(invert.source_code(), str))
    #     invert.src_attr_dict = True
    #     self.assertTrue(isinstance(invert.source_code(), str))




if __name__ == '__main__':
    unittest.main()
