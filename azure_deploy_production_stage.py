from azure_utils.common import read_config, update_config
import mlflow.azureml
import requests
import json
import os
from from_root import from_root
from azure_utils.common import read_config
import pandas as pd
from azureml.core import Workspace


def query(scoring_uri=None, inputs=None):
    headers = {"Content-Type": "application/json"}
    response = requests.post(scoring_uri, data=inputs, headers=headers)
    return json.loads(response.text)


def prod_deployment(config=None):
    workspace = Workspace.create(name=config['azure_workspace_config']['workspace_name'],
                                 location=config['azure_workspace_config']['workspace_location'],
                                 resource_group=config['azure_workspace_config']['resource_group'],
                                 subscription_id=config['azure_workspace_config']['subscription_id'],
                                 exist_ok=True)

    azure_service, azure_model = mlflow.azureml.deploy(model_uri=config['model_config']['model_uri'],
                                                       workspace=workspace,
                                                       service_name=config['model_config']['aci_service_name'],
                                                       model_name=config['model_config']['model_name'],
                                                       synchronous=True)

    return azure_service


if __name__ == "__main__":
    # Create Deployment Model
    path = os.path.join(from_root(), 'azure_configuration/azure_config.yaml')
    config = read_config(path)
    azure_service = prod_deployment(config)

    # Update Azure Config File
    config['azure_endpoint']['scoring_uri'] = azure_service.scoring_uri
    update_config(path, config)

    # Generate Data
    data = pd.read_json(
        '{"fixed acidity":{"0":7.4},"volatile acidity":{"0":0.7},"citric acid":{"0":0},"residual sugar":{"0":1.9},'
        '"chlorides":{"0":0.076},"free sulfur dioxide":{"0":11},"total sulfur dioxide":{"0":34},"density":{'
        '"0":0.9978},"pH":{"0":3.51},"sulphates":{"0":0.56},"alcohol":{"0":9.4}}')

    input_json = data.to_json(orient='split')

    # Azure Production Prediction
    scoring_uri = config['azure_endpoint']['scoring_uri']
    response = query(scoring_uri, input_json)

    print(response)
