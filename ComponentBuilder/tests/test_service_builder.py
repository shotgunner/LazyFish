import os
import unittest

from main import ComponentBuilder
from tests.specs import get_list_of_services


class ServiceBuilderTest(unittest.TestCase):
    def setUp(self) -> None:

        self.general_config_location = os.getcwd() + "/" + "general_config.yml"

    def test_is_all_service_names_correct(self):
        for service in get_list_of_services(self.general_config_location)["services"]:
            self.service_builder = ComponentBuilder(service)
            self.assertEqual(self.service_builder.service_name, service["name"])

    def test_is_all_instances_of_correct_classes(self):
        for service in get_list_of_services(self.general_config_location)["services"]:
            self.service_builder = ComponentBuilder(service)
            self.assertIsInstance(self.service_builder.component_instance, self.service_builder.component_mapper[service["name"]])

    def test_is_location_added_to_the_specs(self):
        for service in get_list_of_services(self.general_config_location)["services"]:
            self.service_builder = ComponentBuilder(service)
            self.assertEqual(self.service_builder.component["location"], os.getcwd() + "/" + "example")


if __name__ == '__main__':
    unittest.main()
