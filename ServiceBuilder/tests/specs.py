from ConfigLoader import ConfigLoader

project_name = "test_project"
project_location = '.'


def get_list_of_services(filename):
    with open(filename, 'r') as f:
        config_file_content = ConfigLoader(f.read()).load_file()
        list_of_services = []
        for service_name, service_specs in config_file_content['services'].items():
            list_of_services.append({
                "name": service_name,
                "specs": service_specs,
                "location": project_location
            })

    return list_of_services


