import unittest

from ComponentBuilder.Components.WebApplication import flask
from tests.abstract_test_builder import AbstractServiceBuilder


class FlaskServiceBuilder(AbstractServiceBuilder):
    def setUp(self) -> None:
        self.config_file_location = "tests/configs/flask_config.yml"
        self.file_names_should_created = ["Dockerfile", "app.py", "docker-compose.yml", "requirements.txt"]
        self.component = flask

    def test_is_folder_and_files_created_properly_after_run(self):
        self.check_folder_and_files_created_properly_after_run()


if __name__ == '__main__':
    unittest.main()
