from phising_domain.logger import logging
from phising_domain.exception import PhisingException 
import os,sys
from datetime import datetime



FILE_NAME="phising.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"   


TRANSFER_OBJECT_FILE_NAME="tranformer.pkl"

class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir=os.path.join(os.getcwd(),'artifacts',f"{datetime.now().strftime('%d%m%Y__%H%M%S')}")
        except Exception as e:
            raise PhisingException(e, sys)



class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_base_name="phsing_domaain"
            self.collection_name="website"
            self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_file_path=os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
            self.train_file_path=os.path.join(self.data_ingestion_dir,"data_set",TRAIN_FILE_NAME)
            self.test_file_path=os.path.join(self.data_ingestion_dir,"data_set",TEST_FILE_NAME)
            self.test_size=0.25
        except Exception as e:
            raise PhisingException(e, sys)

    def to_dict(self):
        try:
            return self.__dict__ 
        except Exception as e:
            raise PhisingException(e, sys)


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_validation_dir=os.path.join(training_pipeline_config.artifact_dir,"data_validation")
            self.report_file_path=os.path.join(self.data_validation_dir,"report.yaml")
            self.base_file_path=os.path.join('phising_dataset.csv') 
        except Exception as e:
            raise PhisingException(e,sys)
       

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir=os.path.join(training_pipeline_config.artifact_dir,'data_transformation')
            self.transformed_object_path=os.path.join(self.data_transformation_dir,'transformer',TRANSFER_OBJECT_FILE_NAME)
            self.transformed_train_path=os.path.join(self.data_transformation_dir,'transformed',TRAIN_FILE_NAME)
            self.transformed_test_path=os.path.join(self.data_transformation_dir,'transformer',TEST_FILE_NAME)
            self.transformed_train_path=os.path.join(self.data_transformation_dir,'transformer',TEST_FILE_NAME.replace("csv","npz"))
            self.transformed_test_path=os.path.join(self.data_transformation_dir,"transformer",TRAIN_FILE_NAME.replace("csv","npz"))
        except Exception as e:
            raise PhisingException(e,sys)
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...