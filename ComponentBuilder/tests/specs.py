import os
from ConfigLoaders import YAMLConfigLoader


def get_list_of_services(filename):
    config_file_content = YAMLConfigLoader(filename).load_file()
    config_object = {"project": {"name": config_file_content["project"]["name"]},
                     "services": []}
    for service_name, service_specs in config_file_content['services'].items():
        config_object["services"].append({
            "name": service_name,
            "specs": service_specs,
            "location": os.getcwd() + "/" + config_file_content['project']['name']
        })

    return config_object


