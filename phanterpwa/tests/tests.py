import unittest
from phanterpwa.tests import test_cli
from phanterpwa.tests import test_components_preloaders
from phanterpwa.tests import test_helpers
from phanterpwa.tests import test_i18n
from phanterpwa.tests import test_reversexml
from phanterpwa.tests import test_tools
from phanterpwa.tests import test_configer

test_list = [
    "test_cli",
    "test_components_preloaders",
    "test_helpers",
    "test_i18n",
    "test_reversexml",
    "test_tools",
    "test_configer",
]


def run():
    suite = unittest.TestLoader().loadTestsFromModule(test_cli)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromModule(test_components_preloaders)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromModule(test_helpers)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromModule(test_i18n)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromModule(test_reversexml)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromModule(test_tools)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromModule(test_configer)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    run()
