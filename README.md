# Mlops-Azure-Integration

1. Create Conda Environment in the current Working directory.
```commandline
conda create --prefix ./env python=3.7 -y && conda activate ./env 

pip install azureml-sdk
pip install scikit-learn==0.22.2.post1
pip install mlflow==1.10.0
```


# Azure functionality
```
1. Azure Container Instances (ACI), similar to how you pushed an image to the Amazon AWS Elastic Container Registry (ECR).

2. Deploying a model to Azure (dev stage): 
Here, you use built-in azureml-sdk module code to push a model to Azure. 
However, this is a development stage deployment, 
so this model is not production-ready since its computational resources are limited.

3. Making predictions: 
Once the model has finished deployment, it is ready to be queried. 
This is done through an HTTP request. 
This is how you can verify that your model works once hosted on the cloud since it’s in the development stage.

4. Deploying to production: 
Here, you utilize MLFlow Azure module code to deploy the model to production by creating a container instance 
(or any other deployment configuration provided, like Azure Kubernetes Service).

5. Making predictions: 
Similar to how you query the model in the dev stage,
you query the model once it has been deployed to the production stage and run the batch query script from the previous chapter.

6. Deploying to production:
Here, you utilize MLFlow Azure module code to 
deploy the model to production by creating a container instance (or any other deployment configuration provided,
like Azure Kubernetes Service)

7. Switching models: 
MLFlow does not provide explicit functionality to switch your models, 
so you must delete the service and recreate it with another model run.

8. Removing the deployed model: 
Finally, you undo every deployment that you did and remove all resources. 
That is, you delete both the development and production branch services as well as the 
container registries and any additional services created once you are done.

```

# Steps:
1. Create WorkSpace And get this values
    - There are 2 ways to do it. First by Manually creating workspace and 2nd by using sdk.
```
workspace_name (azure-mlops-workspace )
subscription (The value where it says Subscription-ID)
resource_group (azure-mlops)
location (East-US)
```
2. Get your Run Id may be local or in any storage
```
https://azure.github.io/azureml-sdk-for-r/reference/aci_webservice_deployment_config.html
Represents a machine learning model deployed as a web service endpoint on Azure Container Instances.
One interesting bit of functionality that Azure provides is the ACI webservice. 
This webservice is specifically used for the purposes of debugging or testing some model under development, 
hence why it is suitable for use in the development stage.
```