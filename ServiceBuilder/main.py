import os

from Components.WebApplication.flask.service import Flask
from Components.WebServer.nginx.service import Nginx
from Components.WebApplication.django.service import Django


class ServiceBuilder:
    def __init__(self, service):
        self.service = service
        self.service_mapper = {
            "flask": Flask,
            "django": Django,
            "nginx": Nginx
        }
        self.service_instance = self.service_mapper[self.service_type](self.service)

    @property
    def service_abstract_type(self):
        return self.service["specs"]["type"].split('/')[0]

    @property
    def service_type(self):
        return self.service["specs"]["type"].split('/')[1]

    @property
    def service_name(self):
        return self.service["specs"]["name"]

    def make_service_directory(self):
        if not os.path.exists(self.service_name):
            os.mkdir(self.service_name)

    def cd(self, path):
        self.service["location"] += "/" + path

    def run(self):
        self.make_service_directory()
        self.cd(self.service_name)
        return self.service_instance.run()


