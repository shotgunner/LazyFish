import argparse
import os

from ConfigLoader import ConfigLoader
from ServiceBuilder.main import ServiceBuilder


class LazyFishApplication:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='LazyFish')
        self.parser.add_argument('generate')
        self.parser.add_argument('-f', '--file', type=argparse.FileType('r'), required=True)
        self.args = self.parser.parse_args()
        self.config = ConfigLoader(self.args.file.read()).load_file()

    @property
    def project_name(self):
        return self.config["project"]["name"]

    def make_project_directory(self):
        if not os.path.exists(self.project_name):
            os.mkdir(self.project_name)

    def process_config(self):
        for service_name, service_specs in self.config['services'].items():
            service = {
                "name": service_name,
                "specs": service_specs,
                "location": self.get_abs_location()
            }
            ServiceBuilder(service).run()

    def get_abs_location(self):
        return os.getcwd() + "/" + self.project_name


app = LazyFishApplication()
app.make_project_directory()
app.process_config()

