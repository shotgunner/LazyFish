import os

from Program.ConfigLoaders import YAMLConfigLoader


def get_list_of_components(filename):
    config_file_content = YAMLConfigLoader(filename).load_file()
    config_object = {"project": {"name": config_file_content["project"]["name"]},
                     "components": []}
    for component_name, component_specs in config_file_content['components'].items():
        config_object["components"].append({
            "name": component_name,
            "specs": component_specs,
            "location": os.getcwd() + "/" + config_file_content['project']['name']
        })

    return config_object


