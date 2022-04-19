class Nosy:
    config = None

    @classmethod
    def load(cls, config):
        cls.config = config

    @classmethod
    def query(cls, component, query):
        return cls.config["components"][component][query]

    @classmethod
    def ask_project_name(cls):
        return cls.config["project"]["name"]
