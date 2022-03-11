from azure_utils.common import read_config, update_config
import mlflow.azureml
from azureml.core import Workspace
from azureml.core.webservice import AciWebservice, Webservice
import os
from from_root import from_root


class azure_workspace:
    def __init__(self, config=None):
        self.config = config
        self.workspace = None
        self.model_image = None
        self.azure_model = None
        self.aci_service = None

    def create_azure_workspace(self):
        try:
            self.workspace = Workspace.create(name=self.config['azure_workspace_config']['workspace_name'],
                                              location=self.config['azure_workspace_config']['workspace_location'],
                                              resource_group=self.config['azure_workspace_config']['resource_group'],
                                              subscription_id=self.config['azure_workspace_config']['subscription_id'],
                                              exist_ok=True)

            return f"Workspace Created {self.workspace}"

        except Exception as e:
            return "Error Occurred While Creating Workspace"

    def build_image(self):
        try:
            self.model_image, self.azure_model = mlflow.azureml.build_image(
                model_uri=self.config['model_config']['model_uri'],
                workspace=self.workspace,
                model_name=self.config['model_config']['model_name'],
                image_name=self.config['model_config']['image_name'],
                description=self.config['model_config']['description'],
                synchronous=False)

            return self.model_image

        except Exception as e:
            return f"Error Occurred While building Image {e.__str__()}"

    def dev_deployment(self):
        aci_service_config = AciWebservice.deploy_configuration()
        self.aci_service = Webservice.deploy_from_image(name=self.config['model_config']['aci_service_name'],
                                                        image=self.model_image,
                                                        deployment_config=aci_service_config,
                                                        workspace=self.workspace)

        return self.aci_service


if __name__ == "__main__":
    path = os.path.join(from_root(), 'azure_configuration/azure_config.yaml')
    config = read_config(path)

    azure_dev = azure_workspace(config)

    azure_dev.create_azure_workspace()
    model_image = azure_dev.build_image()
    print(model_image)
    model_image.wait_for_creation(show_output=True)

    aci_service = azure_dev.dev_deployment()
    aci_service.wait_for_deployment(show_output=True)

    config['azure_endpoint']['scoring_uri'] = aci_service.scoring_uri
    update_config(path, config)
    print("Deployment for development stage Completed!")
