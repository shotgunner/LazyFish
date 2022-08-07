import os
import unittest


from ComponentBuilder.main import ComponentBuilder
from tests.utils import get_list_of_components


class ServiceBuilderTest(unittest.TestCase):
    def setUp(self) -> None:

        self.general_config_location = os.getcwd() + "/" + "tests/configs/general_config.yml"

    def test_is_all_service_names_correct(self):
        for component in get_list_of_components(self.general_config_location)["components"]:
            self.component_builder = ComponentBuilder(component)
            self.assertEqual(self.component_builder.component["specs"]["folder_name"], component["specs"]["folder_name"])

    def test_is_all_instances_of_correct_classes(self):
        for service in get_list_of_components(self.general_config_location)["components"]:
            self.component_builder = ComponentBuilder(service)
            self.assertIsInstance(self.component_builder.component_instance, self.component_builder.component_mapper[service["name"]])

    def test_is_location_added_to_the_specs(self):
        for service in get_list_of_components(self.general_config_location)["components"]:
            self.component_builder = ComponentBuilder(service)
            self.assertEqual(self.component_builder.component["location"], os.getcwd() + "/" + "example")
