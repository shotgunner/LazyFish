import os
import unittest

from main import ServiceBuilder
from tests.specs import get_list_of_services, project_location


class ServiceBuilderTest(unittest.TestCase):
    def test_is_all_service_names_correct(self):
        for service in get_list_of_services("general_config.yml"):
            self.service_builder = ServiceBuilder(service)
            self.assertEqual(self.service_builder.service_name, service["name"])

    def test_is_all_instances_of_correct_classes(self):
        for service in get_list_of_services("general_config.yml"):
            self.service_builder = ServiceBuilder(service)
            self.assertIsInstance(self.service_builder.service_instance, self.service_builder.service_mapper[service["name"]])

    def test_is_location_added_to_the_specs(self):
        for service in get_list_of_services("general_config.yml"):
            self.service_builder = ServiceBuilder(service)
            self.assertEqual(self.service_builder.service["location"], project_location)


class NginxServiceBuilderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.service_builder = ServiceBuilder(get_list_of_services("nginx_config.yml")[0])

    def test_is_folder_and_files_created_properly_after_run(self):
        self.service_builder.run()
        directory = self.service_builder.service["specs"]["name"]
        self.assertTrue(os.path.exists(directory), msg="Folder {} not created".format(directory))
        self.assertEqual(self.service_builder.service_instance.abs_location, "{}/{}".format(project_location, directory))
        os.rmdir(directory)

        self.assertTrue(os.path.exists(directory + "/nginx.conf"), msg="File nginx.conf not created")


if __name__ == '__main__':
    unittest.main()
