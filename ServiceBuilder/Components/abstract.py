class Component:
    def __init__(self, service):
        self.service = service

    @property
    def abs_location(self):
        return self.service["location"]