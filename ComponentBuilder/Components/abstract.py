class Component:
    def __init__(self, component):
        self.component = component

    @property
    def abs_location(self):
        return self.component["location"]

    @property
    def docker_compose_version(self):
        return "3.4"

