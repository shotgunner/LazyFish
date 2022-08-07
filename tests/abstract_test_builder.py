import os
import shutil
import unittest
import io

from ComponentBuilder.main import ComponentBuilder

from Program.ConfigLoaders import YAMLConfigLoader
from Program.nosy import Nosy
from tests.utils import get_list_of_components, get_necessary_files_for, get_component_module_address


class AbstractServiceBuilder(unittest.TestCase):
    def __init__(self, method_name):
        super().__init__(method_name)
        self.config_file_location = None

    def setup_location(self):
        self.test_folder_location = os.getcwd()
        self.config_dictionary = get_list_of_components(self.config_file_location)
        self.component_builders = [ComponentBuilder(component) for component in self.config_dictionary["components"]]
        self.project_location = self.test_folder_location + "/" + self.config_dictionary["project"]["name"]
        self.component_name = self.config_dictionary["components"][0]["specs"]["folder_name"]
        if not os.path.exists(self.project_location):
            os.mkdir(self.project_location)

    def check_folder_and_files_created_properly_after_run(self):
        self.setup_location()
        Nosy.load(YAMLConfigLoader(self.config_file_location).load_file())
        for component_builder in self.component_builders:
            component_builder.run()
            os.chdir(self.project_location)
            component_directory = component_builder.component_instance.folder_name
            self.assertTrue(os.path.exists(component_directory), msg="Folder {} not created".format(component_directory))
            self.assertEqual(component_builder.component_instance.absolute_location, "{}/{}".format(self.project_location, component_directory))
            for file_name in get_necessary_files_for(component_builder.component_instance.name):
                self.assertTrue(os.path.isfile(component_directory + f"/{file_name}"), msg=f"File {file_name} not created")
                self.assert_two_file_equal(component_directory + f"/{file_name}", os.path.dirname(get_component_module_address(component_builder.component_instance)) + f"/examples/{file_name}")

    def assert_two_file_equal(self, file_1, file_2):
        with io.open(file_1) as f1, io.open(file_2) as f2:
            self.assertListEqual(list(f1), list(f2), msg="Files {} and {} are not equal".format(file_1, file_2))

    def tearDown(self) -> None:
        os.chdir(self.test_folder_location)
        shutil.rmtree(self.project_location)
