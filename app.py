import argparse
import os
import sys

from ConfigLoader import ConfigLoader
from ServiceBuilder.main import ServiceBuilder


class LazyFishApplication:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='LazyFish')
        self.parser.add_argument('generate')
        self.parser.add_argument('-f', '--file', type=argparse.FileType('r'), required=True)
        self.args = self.parser.parse_args()
        self.config = ConfigLoader(self.args.file.read()).load_file()

    def get_config(self):
        return self.config

    def process_config(self):
        location = sys.path.append(os.path.join(os.path.dirname(__file__), self.config["project"]["name"]))

        for service_name, service_specs in self.config['services'].items():
            service = {
                "name": service_name,
                "specs": service_specs,
                "location": location
            }
            ServiceBuilder(service).run()


LazyFishApplication().process_config()
