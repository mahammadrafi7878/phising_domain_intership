from phising_domain.predictor import ModelResolver 
from phising_domain.exception import PhisingException 
from phising_domain.logger import logging 
from phising_domain.entity import config_entity,artifact_entity 
from phising_domain.utils import load_object
from phising_domain.config import TARGET_COLUMN 
import pandas as pd 
import os,sys 
from sklearn.metrics import f1_score 



class ModelEvaluation:
    def __init__(self,model_evaluation_config:config_entity.ModelEvaluationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionartifact,
                 data_transformtuon_artifact:artifact_entity.DataTransformationartifact,
                 model_trainer_artifact:artifact_entity.ModelTrainerArtifact
                 ):
                 try:
                    self.model_evaluation_config=model_evaluation_config
                    self.data_ingestion_artifact=data_ingestion_artifact
                    self.data_transformation_artifact=data_ingestion_artifact 
                    self.model_trainer_artifact=model_trainer_artifact
                    self.model_resolver=ModelResolver()

                 except Exception as e:
                    raise PhisingException(e,sys)  

    
    def initiate_model_evaluation(self):
        try:
            latest_dir_path=self.model_resolver.get_latest_dir_path() 
            if latest_dir_path ==None:
                model_eval_artifact=artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,improved_accuracy=None)
                return model_eval_artifact

            transformer_path=self.model_resolver.get_latest_transformer_path() 
            model_path=self.model_resolvar.get_latest_model_path()


            transformer=load_object(file_path=transformer_path)
            model=load_object(file_path=model_path)

            current_transformer=load_object(file_path=self.data_transformation_artifact.transform_object_path) 
            current_model=load_object(file_path=self.model_trainer_artifact.model_path)


            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df=test_df[TARGET_COLUMN]
            y_true=target_df 

                
            y_pred=model.predict(test_df[TARGET_COLUMN])
            previous_model_score=f1_score(y_true=y_true,y_pred=y_pred)  

            y_pred2=current_model.predict(test_df[TARGET_COLUMN])
            current_model__score=f1_score(y_true=y_true,y_pred=y_pred2)


            if current_model__score<previous_model_score:
                raise Exception("current model is not good ")

            model_eval_artifact=artifact_entity.ModelEvaluationArtifact(is_true_model_accepted=True,
                                           improved_accuracy=current_model__score-previous_model_score)

            return model_eval_artifact

            
        except Exception as e:
            raise PhisingException(e, sys)
        