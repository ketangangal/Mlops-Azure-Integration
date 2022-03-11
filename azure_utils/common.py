import yaml


def read_config(config_path):
    with open(config_path) as config_file:
        content = yaml.load(config_file, Loader=yaml.FullLoader)
        config_file.close()

    return content


def update_config(config_path, data):
    with open(config_path, 'w') as config_file:
        config_file.write(yaml.dump(data, default_flow_style=False))

    return "Done"
