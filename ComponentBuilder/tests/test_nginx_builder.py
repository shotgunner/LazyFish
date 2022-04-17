import os
import shutil
import unittest
import io

from ConfigLoaders import YAMLConfigLoader
from main import ComponentBuilder
from nosy import Nosy
from tests.specs import get_list_of_services
from ComponentBuilder.Components.WebServer import nginx


class NginxServiceBuilderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_folder_location = os.getcwd()
        self.nginx_config_dictionary = get_list_of_services("nginx_config.yml")
        self.component_builder = ComponentBuilder(self.nginx_config_dictionary["services"][0])
        self.project_location = self.test_folder_location + "/" + self.nginx_config_dictionary["project"]["name"]
        self.component_name = self.nginx_config_dictionary["services"][0]["specs"]["name"]
        if not os.path.exists(self.project_location):
            os.mkdir(self.project_location)

    def test_is_folder_and_files_created_properly_after_run(self):
        Nosy.load(YAMLConfigLoader("general_config.yml").load_file())
        self.component_builder.run()
        component_directory = self.component_builder.component["specs"]["name"]
        self.assertTrue(os.path.exists(component_directory), msg="Folder {} not created".format(component_directory))
        self.assertEqual(self.component_builder.component["location"], "{}/{}".format(self.project_location, self.component_name))
        self.assertEqual(self.component_builder.component_instance.abs_location, "{}/{}".format(self.project_location, component_directory))

        self.assertTrue(os.path.isfile(component_directory + "/nginx.conf"), msg="File nginx.conf not created")
        self.assertListEqual(list(io.open(component_directory + "/nginx.conf")),
                             list(io.open(os.path.dirname(nginx.__file__) + "/examples/config.nginx")))
        self.assertTrue(os.path.isfile(component_directory + "/Dockerfile"), msg="File Dockerfile not created")
        self.assertTrue(os.path.isfile(component_directory + "/docker-compose.yml"), msg="File docker-compose.yml not created")



    def tearDown(self) -> None:
        os.chdir(self.test_folder_location)
        shutil.rmtree(self.project_location)


if __name__ == '__main__':
    unittest.main()
