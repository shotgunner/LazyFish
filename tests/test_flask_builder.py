import os
import shutil
import unittest
import io

from ComponentBuilder.Components.WebApplication import flask
from ComponentBuilder.main import ComponentBuilder

from Program.ConfigLoaders import YAMLConfigLoader
from Program.nosy import Nosy
from tests.specs import get_list_of_components


class NginxServiceBuilderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.config_file_location = "tests/configs/flask_config.yml"
        self.test_folder_location = os.getcwd()
        print(self.test_folder_location)
        self.nginx_config_dictionary = get_list_of_components(self.config_file_location)
        self.component_builder = ComponentBuilder(self.nginx_config_dictionary["components"][0])
        self.project_location = self.test_folder_location + "/" + self.nginx_config_dictionary["project"]["name"]
        self.component_name = self.nginx_config_dictionary["components"][0]["specs"]["name"]
        if not os.path.exists(self.project_location):
            os.mkdir(self.project_location)

    def test_is_folder_and_files_created_properly_after_run(self):
        Nosy.load(YAMLConfigLoader(self.config_file_location).load_file())
        self.component_builder.run()
        os.chdir(self.project_location)
        component_directory = self.component_builder.component["specs"]["name"]
        self.assertTrue(os.path.exists(component_directory), msg="Folder {} not created".format(component_directory))
        self.assertEqual(self.component_builder.component["location"], "{}/{}".format(self.project_location, self.component_name))
        self.assertEqual(self.component_builder.component_instance.abs_location, "{}/{}".format(self.project_location, component_directory))

        self.assertTrue(os.path.isfile(component_directory + "/app.py"), msg="File app.py not created")
        self.assertTwoFileEqual(component_directory + "/app.py",
                                os.path.dirname(flask.__file__) + "/examples/app.py")

        self.assertTrue(os.path.isfile(component_directory + "/Dockerfile"), msg="File Dockerfile not created")
        self.assertTwoFileEqual(component_directory + "/Dockerfile",
                                os.path.dirname(flask.__file__) + "/examples/Dockerfile")

        self.assertTrue(os.path.isfile(component_directory + "/requirements.txt"), msg="File requirements.txt not created")
        self.assertTwoFileEqual(component_directory + "/requirements.txt",
                                os.path.dirname(flask.__file__) + "/examples/requirements.txt")

        self.assertTrue(os.path.isfile(component_directory + "/docker-compose.yml"), msg="File docker-compose.yml not created")
        self.assertTwoFileEqual(component_directory + "/docker-compose.yml",
                                os.path.dirname(flask.__file__) + "/examples/docker-compose.yml")

    def assertTwoFileEqual(self, file_1, file_2):
        with io.open(file_1) as f1, io.open(file_2) as f2:
            self.assertListEqual(list(f1), list(f2), msg="Files {} and {} are not equal".format(file_1, file_2))

    def tearDown(self) -> None:
        os.chdir(self.test_folder_location)
        shutil.rmtree(self.project_location)


if __name__ == '__main__':
    unittest.main()
