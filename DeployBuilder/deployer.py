import glob
import os

from jinja2 import Template

from Program.nosy import Nosy


class Deploy:
    def __init__(self, component_builders: list):
        self.components = [i.component_instance for i in component_builders]
        self.file_mapper = {}
        self.absolute_location = self.components[0].absolute_project_location
        for jinja_file in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__))) + '/*.jinja'):
            with open(jinja_file, "r") as f:
                self.file_mapper[jinja_file.split("/")[-1]] = f.read()
        self.template_arguments = {
            "network_name": "{}-net".format(Nosy.ask_project_name()),
            "files": ["./{}/docker-compose.yml".format(i.folder_name) for i in self.components],
        }

    def render(self, file_name):
        with open(self.absolute_location + "/" + file_name, "w") as f:
            rendered_content = Template(
                self.file_mapper["{}.jinja".format(file_name)],
                trim_blocks=True,
                lstrip_blocks=True,
            ).render(**self.template_arguments)
            f.write(rendered_content)

    def run(self):
        os.chdir(self.components[0].absolute_project_location)
        self.render("deploy")
        self.render("global-docker-compose.yml")
