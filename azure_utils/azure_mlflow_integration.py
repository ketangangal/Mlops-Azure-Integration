import azureml
import mlflow.azureml
from azureml.core import Workspace


class Azure_Integration:
    def __init__(self, config=None):
        self.config = config
        self.workspace = None
        self.model_uri = None

    def create_azure_workspace(self):
        try:
            workspace = Workspace.create(name=self.config['azure_workspace_config']['workspace_name'],
                                         location=self.config['azure_workspace_config']['workspace_location'],
                                         resource_group=self.config['azure_workspace_config']['resource_group'],
                                         subscription_id=self.config['azure_workspace_config']['subscription_id'],
                                         exist_ok=True)
            self.workspace = workspace
            return self.workspace

        except Exception as e:
            return f"Error Occurred While Connecting {e.__str__()}"

    def create_docker_image(self):
        try:
            model_image, azure_model = mlflow.azureml.build_image(model_uri=self.config['model_config']['model_uri'],
                                                                  workspace=self.workspace,
                                                                  model_name="ElasticNetModel",
                                                                  image_name="Azure-Model-Image",
                                                                  description="Sklearn Model",
                                                                  synchronous=False)
            return model_image, azure_model

        except Exception as e:
            return f"Error Occurred While creating Image {e.__str__()}"
