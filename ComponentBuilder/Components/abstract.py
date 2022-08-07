class Component:
    def __init__(self, component):
        self.component = component

    @property
    def config(self):
        return self.component["specs"]["config"]

    @property
    def absolute_location(self):
        return self.component["location"]

    @property
    def absolute_project_location(self):
        return '/'.join(self.absolute_location.split("/")[:-1])

    @property
    def docker_compose_version(self):
        return "3.4"

    @property
    def name(self):
        return self.component["name"]

    @property
    def folder_name(self):
        return self.component["specs"]["folder_name"]

    @property
    def internal_port(self):
        return self.component["specs"]["internal-port"]

    @property
    def external_port(self):
        return self.component["specs"]["external-port"]

    @property
    def app_route(self):
        return self.component["specs"]["config"]["locations"][0].split(":")[0]

    @property
    def component_locations(self):
        return self.component["specs"]["config"]["locations"]

