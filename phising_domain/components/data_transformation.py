from phising_domain.entity import config_entity,artifact_entity 
from phising_domain.logger import logging 
from phising_domain.exception import PhisingException 
import os,sys 
from typing import Optional 
import pandas as pd 
import numpy as np 
from phising_domain import utils 
from imblearn.combine import SMOTETomek
from phising_domain.config import TARGET_COLUMN 
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer 


class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'<<' *20} DATA TRANSFORMATION {'>>' *20}  ")
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise PhisingException(e,sys) 

     
    @classmethod
    def get_data_transformation(cls):
        try:
            logging.info(f"creating a pipoeline for imputing missing values")
            simple_imputer=SimpleImputer(strategy='constant',fill_value=0)  
            pipeline=Pipeline(steps=[('imputer',simple_imputer)])
            return pipeline
        except Exception as e:
            raise PhisingException(e, sys)
            



    
    def initiate_data_transformation(self):
        try:
            logging.info(f"reading train data")
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info("reading test data")
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            logging.info(f"dividing iput and output features")
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            
            target_feature_train_arr=train_df[TARGET_COLUMN]
            target_feature_test_arr=test_df[TARGET_COLUMN]

            
            logging.info(f"initiating transformation pipeline")
            transformation_pipeline=DataTransformation.get_data_transformation()
            transformation_pipeline.fit(input_feature_train_df)
             
            
            input_feature_train_arr=transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr=transformation_pipeline.transform(input_feature_test_df) 

            logging.info(f"this data set is imbalanced dataset so need to samoling technique")
            smt=SMOTETomek(sampling_strategy='minority',random_state=77)

            logging.info("before resampling in training set input: {input_feature_train_df.shape}  and target :{target_feature_train_arr.shape}")
            input_feature_train_arr,target_feature_train_arr=smt.fit_resample(input_feature_train_arr,target_feature_train_arr)
            logging.info(f"after resampling training set input{input_feature_train_arr.shape} and target:{target_feature_train_arr.shape}")

            logging.info(f"Before resampling in testing set Input: {input_feature_test_df.shape} Target:{target_feature_test_arr.shape}")
            input_feature_test_arr,target_feature_test_arr=smt.fit_resample(input_feature_test_arr,target_feature_test_arr)
            logging.info(f"After resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")

            logging.info(f"converting data new created data into an array")
            train_arr=np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr=np.c_[input_feature_test_arr,target_feature_test_arr]


            
            logging.info(f"storing  transformed train and transformed test dsatra in a file and transformation path")
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,array=test_arr)

            utils.save_object(self.data_transformation_config.transformed_object_path,obj=transformation_pipeline)
            
            logging.info(f"preparing data transformation artifact")
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transformed_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                
            )
            
            logging.info(f" data transformation artifact : {data_transformation_artifact}")
            return data_transformation_artifact
            

        except exception as e:
            raise PhisingException(e,sys)