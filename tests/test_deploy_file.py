import os

from DeployBuilder.deployer import Deploy
import DeployBuilder
from tests.abstract_test_builder import AbstractServiceBuilder


class DeployTestCase(AbstractServiceBuilder):
    def setUp(self) -> None:
        self.config_file_location = "tests/configs/general_config.yml"

    def do_deploy(self) -> None:
        Deploy(self.component_builders).run()

    def test_is_deploy_file_created(self):
        self.check_folder_and_files_created_properly_after_run()
        self.do_deploy()
        os.chdir(self.project_location)
        self.assertTrue(os.path.exists("global-docker-compose.yml"), msg="File deploy not created")
        self.assert_two_file_equal("global-docker-compose.yml", os.path.dirname(DeployBuilder.__file__) + "/examples/global-docker-compose.yml")

        self.assertTrue(os.path.exists("deploy"), msg="File deploy not created")
        self.assert_two_file_equal("deploy", os.path.dirname(DeployBuilder.__file__) + "/examples/deploy")