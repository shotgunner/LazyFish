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
            "internal_port": self.component["specs"]["internal-port"],
            "main_py_route": self.component["specs"]["config"]["locations"][0].split(":")[-1],
            "python_docker_image_with_version": self.get_python_docker_image_with_version(),
            "flask_version": "2.1.3",
            "docker_compose": self.generate_docker_compose_variables(),
        }

    def generate_docker_compose_variables(self):
        project_name = Nosy.ask_project_name()
        docker_compose_variables = {
            "version": self.docker_compose_version,
            "service_name": self.component["specs"]["name"],
            "build_dir": "{}/{}".format(project_name, self.component["name"]),
            "network_name": "{}-net".format(project_name),
        }

        return docker_compose_variables

    def get_python_docker_image_with_version(self):
        python_version = "3.9"
        if self.component["specs"]["config"].get("python-version"):
            python_version = self.component["specs"]["config"]["python-version"]
        return "python:{}".format(python_version)

    def run(self):
        self.render("app.py")
        self.render("requirements.txt")
        self.render("Dockerfile")
        self.render("docker-compose.yml")

        self.go_back_to_project_directory()

    def render(self, file_name):
        with open(self.abs_location + "/" + file_name, "w") as f:
            rendered_content = Template(
                self.file_mapper["{}.jinja".format(file_name)],
                trim_blocks=True,
                lstrip_blocks=True,
            ).render(**self.template_arguments)
            f.write(rendered_content)

    @staticmethod
    def go_back_to_project_directory():
        os.chdir("..")
