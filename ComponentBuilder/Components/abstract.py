class Component:
    def __init__(self, component):
        self.component = component

    @property
    def abs_location(self):
        return self.component["location"]