import os

from Components.WebApplication.flask.component import Flask
from Components.WebServer.nginx.component import Nginx
from Components.WebApplication.django.component import Django


class ComponentBuilder:
    def __init__(self, component):
        self.component = component
        self.component_mapper = {
            "flask": Flask,
            "django": Django,
            "nginx": Nginx
        }
        self.component_instance = self.component_mapper[self.component_type](self.component)

    @property
    def service_abstract_type(self):
        return self.component["specs"]["type"].split('/')[0]

    @property
    def component_type(self):
        return self.component["specs"]["type"].split('/')[1]

    @property
    def service_name(self):
        return self.component["specs"]["name"]

    def make_service_directory(self):
        os.chdir(self.component["location"])
        if not os.path.exists(self.service_name):
            os.mkdir(self.service_name)

    def cd(self, path):
        self.component["location"] += "/" + path

    def run(self):
        self.make_service_directory()
        self.cd(self.service_name)
        return self.component_instance.run()


