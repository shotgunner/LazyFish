import unittest
from Program.ConfigLoaders import ConfigHolder, YAMLConfigLoader


class ConfigHolderTestCase(unittest.TestCase):
    def test_config_fields(self):
        file = "tests/configs/test_config.yml"
        self.config = YAMLConfigLoader(file).load_file()
        config_holder = ConfigHolder(file)
        self.assertEqual(config_holder.project_name, self.config["project"]["name"])
        self.assertEqual(len(config_holder.components), 2)
        for key in self.config["components"]["nginx"].keys():
            self.assertEqual(config_holder.components["nginx"][key], self.config["components"]["nginx"][key])


if __name__ == '__main__':
    unittest.main()
