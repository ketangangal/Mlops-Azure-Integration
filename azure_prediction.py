import requests
import json
import os
from from_root import from_root
from azure_utils.common import read_config
import pandas as pd


def query(scoring_uri=None, inputs=None):
    headers = {"Content-Type": "application/json"}
    response = requests.post(scoring_uri, data=inputs, headers=headers)
    return json.loads(response.text)


if __name__ == "__main__":
    path = os.path.join(from_root(), 'azure_configuration/azure_config.yaml')
    config = read_config(path)
    scoring_uri = config['azure_endpoint']['scoring_uri']

    data = pd.read_json('{"fixed acidity":{"0":7.4},"volatile acidity":{"0":0.7},"citric acid":{"0":0},"residual '
                        'sugar":{"0":1.9},"chlorides":{"0":0.076},"free sulfur dioxide":{"0":11},"total sulfur '
                        'dioxide":{"0":34},"density":{"0":0.9978},"pH":{"0":3.51},"sulphates":{"0":0.56},"alcohol":{'
                        '"0":9.4}}')
    input_json = data.to_json(orient='split')

    response = query(scoring_uri, input_json)
    print(response)
