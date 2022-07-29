import unittest
from Program.ConfigLoaders import YAMLConfigLoader
from Program.main import LazyFishApplication
import sys


# class ProgramTestCase(unittest.TestCase):
#     def setUp(self):
#         sys.argv.extend('-f test_config.yml generate'.split())
#         self.app = LazyFishApplication()
#         self.config_file = YAMLConfigLoader('configs/test_config.yml').load_file()
#
#     def test_project_name(self):
#         self.assertEqual(self.app.project_name, self.config_file['project']['name'])

    # def test_get_abs_location(self):
    #     self.assertEqual(self.app.get_abs_location(), os.getcwd() + "/" + self.config_file['project']['name'])


if __name__ == '__main__':
    unittest.main()
