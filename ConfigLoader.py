import yaml


class ConfigLoader:
    def __init__(self, content: str):
        self.content = content

    def load_file(self):
        return yaml.safe_load(self.content)

