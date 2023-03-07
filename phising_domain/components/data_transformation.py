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



class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise PhisingException(e,sys) 

     
     
    def get_data_transformation(self,input_feature_train_df,input_feature_test_df,target_feature_train_df,target_feature_test_df):
        try:   
            smt=SMOTETomek(sampling_strategy="minority")
            smt=SMOTETomek(random_state=44)
            input_feature_train_arr,target_feature_train_df=smt.fit_resample(input_feature_train_df,target_feature_train_df)

            input_feature_test_arr,target_feature_test_df=smt.fit_resample(input_feature_test_df,target_feature_test_df) 

            train_arr=np.c_[input_feature_train_arr,target_feature_train_df]
            test_arr=np.c_[input_feature_test_arr,target_feature_test_df]

            return train_arr,test_arr

        except Exception as e:
            raise PhisingException(e, sys)
            



    
    def initiate_data_transformation(self):
        try:
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_test_df=test_df[TARGET_COLUMN]

            

            transformation_pipeline=self.get_data_transformation(input_feature_train_df=input_feature_train_df, input_feature_test_df=input_feature_test_df, target_feature_train_df=target_feature_train_df, target_feature_test_df=target_feature_test_df)
            train_arr_data,test_arr_data=transformation_pipeline


            
            
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,array=train_arr_data)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,array=test_arr_data)

            utils.save_object(self.data_transformation_config.transformed_object_path,obj=transformation_pipeline)
            

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transformed_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                
            )

            return data_transformation_artifact
            

        except exception as e:
            raise PhisingException(e,sys)