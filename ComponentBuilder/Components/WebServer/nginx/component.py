import os

from jinja2 import Template
import glob


from ComponentBuilder.Components.abstract import Component
from Program.nosy import Nosy


class Nginx(Component):
    def __init__(self, component):
        super().__init__(component)
        self.file_mapper = {}
        for jinja_file in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__))) + '/*.jinja'):
            with open(jinja_file, "r") as f:
                self.file_mapper[jinja_file.split("/")[-1]] = f.read()

    @property
    def template_arguments(self):
        return {
            "internal_port": self.internal_port,
            "external_port": self.external_port,
            "locations": self.generate_nginx_location_directives(),
            "nginx_image_with_version": "nginx:1.21",
            "docker_compose": self.generate_docker_compose_variables(),
        }

    def generate_docker_compose_variables(self):
        project_name = Nosy.ask_project_name()
        docker_compose_variables = {
            "version": self.docker_compose_version,
            "service_name": self.name,
            "build_dir": "{}".format(self.folder_name),
            "volumes": [
                "./{}/nginx.conf:/etc/nginx/conf.d/config.conf".format(self.folder_name),
            ],
            "network_name": "{}-net".format(project_name),
        }

        return docker_compose_variables

    def generate_nginx_location_directives(self):
        locations = []
        for location_item in self.component_locations:
            path, remote_uri = location_item.split(":")
            location = {
                "path": "~* ^/{}(.*)".format(path),
                "proxy_pass": True,
                "service_name": remote_uri.split("/")[0],
                "service_path": remote_uri.split("/")[1],
                "service_port": Nosy.query(component=remote_uri.split("/")[0], query="internal-port"),
            }
            locations.append(location)

        return locations

    def run(self):
        self.render("nginx.conf")
        self.render("Dockerfile")
        self.render("docker-compose.yml")

        self.go_back_to_project_directory()

    def render(self, file_name):
        with open(self.absolute_location + "/" + file_name, "w") as f:
            rendered_content = Template(
                self.file_mapper["{}.jinja".format(file_name)],
                trim_blocks=True,
                lstrip_blocks=True,
            ).render(**self.template_arguments)
            f.write(rendered_content)

    @staticmethod
    def go_back_to_project_directory():
        os.chdir("..")
