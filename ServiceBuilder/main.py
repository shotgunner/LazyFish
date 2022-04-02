from WebApplication.flask.service import Flask
from WebServer.nginx.service import Nginx
from WebApplication.django.service import Django


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
    def name(self):
        return self.service["name"]

    def run(self):
        return self.service_instance.run()


