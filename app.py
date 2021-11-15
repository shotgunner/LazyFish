import argparse

from ConfigLoader import ConfigLoader


class LazyFishApplication:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='LazyFish')
        self.parser.add_argument('generate')
        self.parser.add_argument('-f', '--file', type=argparse.FileType('r'), required=True)
        self.args = self.parser.parse_args()
        self.config = ConfigLoader(self.args.file.read()).load_file()

    def get_config(self):
        return self.config


print(LazyFishApplication().get_config())
