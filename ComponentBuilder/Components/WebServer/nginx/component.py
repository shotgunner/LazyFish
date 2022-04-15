import os

from Components.abstract import Component
from jinja2 import Template
import glob


class Nginx(Component):
    def __init__(self, component):
        super().__init__(component)
        self.file_mapper = {}
        for jinja_file in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__))) +'/*.jinja'):
            with open(jinja_file, "r") as f:
                self.file_mapper[jinja_file.split("/")[-1]] = f.read()

    @property
    def template_arguments(self):
        return {
            "internal_port": self.component["specs"]["internal-port"],
            "external_port": self.component["specs"]["external-port"],
            "locations": self.generate_locations(),
        }

    def generate_locations(self):
        locations = []
        # 'kooft:flask/kooft'
        for location_item in self.component["specs"]["config"]["locations"]:
            path, remote_uri = location_item.split(":")
            location = {
                "path": path,
                "proxy_pass": True
            }

        return self.component["specs"]["config"]

    def run(self):
        with open(self.abs_location + "/" + "nginx.conf", "w") as f:
            rendered_content = Template(self.file_mapper["config.nginx.jinja"]).render(**self.template_arguments)
            print(rendered_content)
            f.write(rendered_content)

        with open(self.abs_location + "/" + "Dockerfile", "w") as f:
            f.write("Dockerfile is here")

        with open(self.abs_location + "/" + "docker-compose.yml", "w") as f:
            f.write("docker-compose is here")