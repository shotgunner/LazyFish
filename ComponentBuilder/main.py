import os

from ComponentBuilder.Components.WebApplication.django.component import Django
from ComponentBuilder.Components.WebApplication.flask.component import Flask
from ComponentBuilder.Components.WebServer.nginx.component import Nginx


class ComponentBuilder:
    def __init__(self, component):
        self.component = component
        self.component_mapper = {
            "flask": Flask,
            "django": Django,
            "nginx": Nginx
        }
        self.component_instance = self.component_mapper[self.component["name"]](self.component)

    def make_service_directory(self):
        os.chdir(self.component_instance.absolute_location)
        if not os.path.exists(self.component_instance.folder_name):
            os.mkdir(self.component_instance.folder_name)

    def cd(self, path):
        self.component["location"] += "/" + path

    def run(self):
        self.make_service_directory()
        self.cd(self.component_instance.folder_name)
        return self.component_instance.run()


