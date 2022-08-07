import os

from jinja2 import Template
import glob


from ComponentBuilder.Components.abstract import Component
from Program.nosy import Nosy


class Flask(Component):
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
            "main_py_route": self.app_route,
            "python_docker_image_with_version": "python:3.9",
            "flask_version": "2.1.3",
            "docker_compose": self.generate_docker_compose_variables(),
        }

    def generate_docker_compose_variables(self):
        project_name = Nosy.ask_project_name()
        docker_compose_variables = {
            "version": self.docker_compose_version,
            "service_name": self.name,
            "build_dir": "{}".format(self.folder_name),
            "network_name": "{}-net".format(project_name),
        }

        return docker_compose_variables

    def run(self):
        self.render("app.py")
        self.render("requirements.txt")
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
