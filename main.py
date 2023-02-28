from phising_domain.logger import logging 
from phising_domain.exception import PhisingException 
import pandas as pd 
import numpy as numpy 
import os,sys 
from phising_domain.utils import get_collection_as_dataframe
from phising_domain.components.data_ingestion import DataIngestion
from phising_domain.entity import config_entity,artifact_entity
from phising_domain.components.data_validation import DataValidation
from phising_domain.components.data_transformation import DataTransformation

print(__name__)
if __name__ == '__main__':
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()
          data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())
          data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
          print(data_ingestion.initiate_data_ingestion())
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
          
          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = DataValidation(data_validation_config=data_validation_config,
                         data_ingestion_artifact=data_ingestion_artifact)

          data_validation_artifact = data_validation.initiate_data_validation()



          data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
          data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact = data_transformation.initiate_data_transformation()


          
     except Exception as e:
          raise PhisingException(e,sys)