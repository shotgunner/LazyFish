import argparse
import os

from Program.ConfigLoaders import YAMLConfigLoader
from ComponentBuilder.main import ComponentBuilder
from Program.nosy import Nosy


class LazyFishApplication:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='LazyFish')
        self.parser.add_argument('generate')
        self.parser.add_argument('-f', '--file', type=argparse.FileType('r'), required=True)
        self.args = self.parser.parse_args()
        self.config = YAMLConfigLoader(self.args.file.name).load_file()
        Nosy.load(self.config)

    @property
    def project_name(self):
        return self.config["project"]["name"]

    def make_project_directory(self):
        if not os.path.exists(self.project_name):
            os.mkdir(self.project_name)

    def process_config(self):
        for component_name, component_specs in self.config["components"].items():
            component = {
                "name": component_name,
                "specs": component_specs,
                "location": self.get_abs_location()
            }
            ComponentBuilder(component).run()

    def get_abs_location(self):
        return os.getcwd() + "/" + self.project_name

    def run(self):
        self.make_project_directory()
        self.process_config()


if __name__ == '__main__':
    LazyFishApplication().run()
