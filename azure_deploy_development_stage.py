from azure_utils.azure_mlflow_integration import azure_workspace
from azure_utils.common import read_config
from from_root import from_root
import os

path = os.path.join(from_root(), 'azure_configuration/azure_config.yaml')
config = read_config(path)
print(config)
azure_dev = azure_workspace(config)

if __name__ == "__main__":
    azure_dev.create_azure_workspace()
    azure_dev.build_image()
    response = azure_dev.dev_deployment()
    print(response)
