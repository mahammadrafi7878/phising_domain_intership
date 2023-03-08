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
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise PhisingException(e,sys) 

     
    @classmethod
    def get_data_transformation(cls):
        try: 
            simple_imputer=SimpleImputer(strategy='constant',fill_value=0)  
            pipeline=Pipeline(steps=[('imputer',simple_imputer)])
            return pipeline
        except Exception as e:
            raise PhisingException(e, sys)
            



    
    def initiate_data_transformation(self):
        try:
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            

            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            
            target_feature_train_arr=train_df[TARGET_COLUMN]
            target_feature_test_arr=test_df[TARGET_COLUMN]

            

            transformation_pipeline=DataTransformation.get_data_transformation()
            transformation_pipeline.fit(input_feature_train_df)
             

            input_feature_train_arr=transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr=transformation_pipeline.transform(input_feature_test_df) 


            smt=SMOTETomek(sampling_strategy='minority',random_state=77)
            input_feature_train_arr,target_feature_train_arr=smt.fit_resample(input_feature_train_arr,target_feature_train_arr)
            input_feature_test_arr,target_feature_test_arr=smt.fit_resample(input_feature_test_arr,target_feature_test_arr)


            train_arr=np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr=np.c_[input_feature_test_arr,target_feature_test_arr]


            
            
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,array=test_arr)

            utils.save_object(self.data_transformation_config.transformed_object_path,obj=transformation_pipeline)
            

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transformed_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                
            )

            return data_transformation_artifact
            

        except exception as e:
            raise PhisingException(e,sys)