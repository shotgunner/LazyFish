import yaml


class YAMLConfigLoader:
    def __init__(self, file: str):
        with open(file, 'r') as f:
            self.content = f.read()

    def load_file(self):
        return yaml.safe_load(self.content)

