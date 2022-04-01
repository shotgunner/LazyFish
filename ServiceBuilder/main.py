from ServiceBuilder.WebServer.nginx.service import Nginx
from ServiceBuilder.WebApplication.django.service import Django


class ServiceBuilderAPP:
    def __init__(self, service_name):
        self.service_name = service_name
        self.service_dictionary = {
            "django": Django,
            "nginx": Nginx
        }
        self.service_instance = self.service_dictionary[self.service_name]()

    def run(self):
        return self.service_instance.run()
