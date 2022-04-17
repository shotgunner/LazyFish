class Nosy:
    config = None

    @classmethod
    def load(cls, config):
        cls.config = config

    @classmethod
    def query(cls, component, query):
        return cls.config["services"][component][query]
