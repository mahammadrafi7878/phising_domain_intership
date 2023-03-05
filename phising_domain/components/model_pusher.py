from phising_domain.exception import PhisingException 
from phising_domain.logger import logging 
from phising_domain.predictor import ModelResolver 
from phising_domain.entity.config_entity import ModelPusherConfig 
import os,sys 
from phising_domain.utils import save_object,load_object 
from phising_domain.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ModelPusherArtifact 


class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,
                 model_trainer_artifact:ModelTrainerArtifact,
                 data_transformation_artifact:DataTransformationArtifact,
                 ):

                try:
                    self.model_pusher_config=model_pusher_config
                    self.model_trainer_artifact=model_trainer_artifact
                    self.data_transformation_artifact=data_transformation_artifact 
                except Exception as e:
                    raise PhisingException(e,sys)

    def initiate_model_pusher(self):
        try:
            transfomer=load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model=load_object(file_path=self.data_transformation_artifact.model_path)

            save_object(file_path=self.model_pusher_config.pusher_transformation_path, obj=transfomer)
            save_object(file_path=self.model_pusher_config.pusher_model-path, obj=model)

            transformer_path=self.model_resolver.get_latest_transformer_path()
            model_path=self.model_resolver.get_latest_model_path() 

            save_object(file_path=transformer_path, obj=transformer)
            save_object(file_path=model_path, obj=model)

            model_pusher_artifact=ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
             saved_model_dir=self.model_pusher_config.saved_model_dir)

            return model_pusher_artifact
        except Exception as e:
            raise PhisingException(e,sys)