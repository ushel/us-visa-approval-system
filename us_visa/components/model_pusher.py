import sys

from us_visa.cloud_storage.aws_storage import SimpleStorageService
from us_visa.exception import USVisaException
from us_visa.logger import logging
from us_visa.entity.artifact_entity import ModelPusherArtifact, ModelEvaluatorArtifact
from us_visa.entity.config_entity import ModelPusherConfig
from us_visa.entity.s3_estimator import USVisaEstimator

class ModelPusher:
    def __init__(self, model_evalutation_artifact: ModelEvaluatorArtifact,
                 model_pusher_config:ModelPusherConfig):
        """
        :Param model_evalutation_artifact: Output reference of data evaluation artifact stage
        :param model_pusher_config: Configuration for model pusher
        """
        
        self.s3 = SimpleStorageService()
        self.model_evalutation_artifact = model_evalutation_artifact
        self.model_pusher_config = model_pusher_config
        self.usvisa_estimator = USVisaEstimator(bucket_name = model_pusher_config.bucket_name,
                                                 model_path=model_pusher_config.s3_model_key_path)
        
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Method Name: initiate_model_pusher
        Description: This method is used to initiate all steps of the model pusher.
        
        Output: Returns Model Pusher object
        On Failure: Write an exception log and then raise an exception
        """
        logging.info("Entered inititate_model_pusher method for ModelTrainer class.")
        try:
            logging.info("Uploading artifacts folder to s3 bucket.")
            self.usvisa_estimator.save_model(from_file=self.model_evalutation_artifacts.trained_model_path)
            
            model_pusher_artifact = ModelPusherArtifact(bucket_name = self.model_pusher_config.bucket_name,
                                                        s3_model_path=self.model_pusher_config.s3_model_key_path)
            
            logging.info("Uploaded artifacts folder to s3 bucket.")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initate_model_pusher method of ModelTrainer class.")
            
            return model_pusher_artifact
        except Exception as e:
            raise USVisaException(e, sys) from e
        
        
        