import io
import os

from ComponentBuilder.Components.WebApplication import flask
from ComponentBuilder.Components.WebServer import nginx
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


def get_necessary_files_for(component):
    component_files_holder = {
        "nginx": ["Dockerfile", "nginx.conf", "docker-compose.yml"],
        "flask": ["Dockerfile", "app.py", "docker-compose.yml", "requirements.txt"]
    }
    return component_files_holder[component]


def get_component_module_address(component):
    component_modules_holder = {
        "nginx": nginx.__file__,
        "flask": flask.__file__,
    }
    return component_modules_holder[component.name]
