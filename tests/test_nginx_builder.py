import unittest

from ComponentBuilder.Components.WebServer import nginx
from tests.abstract_test_builder import AbstractServiceBuilder


class NginxServiceBuilder(AbstractServiceBuilder):
    def setUp(self) -> None:
        self.config_file_location = "tests/configs/nginx_config.yml"

    def test_is_folder_and_files_created_properly_after_run(self):
        self.check_folder_and_files_created_properly_after_run()

