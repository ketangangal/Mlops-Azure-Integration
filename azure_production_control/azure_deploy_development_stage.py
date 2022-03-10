from azureml.core.webservice import AciWebservice, Webservice
aci_service_name = "sklearn-model-dev"
aci_service_config = AciWebservice.deploy_configuration()
aci_service = Webservice.deploy_from_image(name=aci_service_name,
              image=model_image,
              deployment_config=aci_service_config,
              workspace=workspace)