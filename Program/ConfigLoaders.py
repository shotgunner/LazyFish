import yaml


class YAMLConfigLoader:
    def __init__(self, file: str):
        with open(file, 'r') as f:
            self.content = f.read()

    def load_file(self) -> dict:
        return yaml.safe_load(self.content)


class ConfigHolder:
    def __init__(self, file: str):
        self.config = YAMLConfigLoader(file).load_file()

    @property
    def project_name(self) -> str:
        return self.config["project"]["name"]

    @property
    def components(self) -> dict:
        return self.config["components"]

    @property
    def component(self, name: str) -> dict:
        return {

        }

    # self.component["specs"]["name"]
    # self.component["specs"]["internal-port"]
    # self.component["specs"]["external-port"]
    # self.component["location"]