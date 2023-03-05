from phising_domain.entity import config_entity,artifact_entity 
from phising_domain.logger import logging 
from phising_domain.exception import PhisingException 
import os,sys 
from typing import Optional 
import pandas as pd 
import numpy as np 
from phising_domain import utils 
from sklearn.preprocessing import RobustScaler
from imblearn.combine import SMOTETomek
from phising_domain.config import TARGET_COLUMN 
from sklearn.pipeline import Pipeline



class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise PhisingException(e,sys) 

    def drop_column(data):
        if 'Unnamed: 0' in data.columns:
            data.remove('Unnamed: 0',axis=1,inplace=True)
        return data
 
    



    
    def initiate_data_transformation(self):
        try:
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_test_df=test_df[TARGET_COLUMN]

            
            smt=SMOTETomek(sampling_strategy="minority")
            smt=SMOTETomek(random_state=77)
            input_feature_train_arr,target_feature_train_df=smt.fit_resample(input_feature_train_df,target_feature_train_df)

            input_feature_test_arr,target_feature_test_df=smt.fit_resample(input_feature_test_df,target_feature_test_df) 

            train_arr=np.c_[input_feature_train_arr,target_feature_train_df]
            test_arr=np.c_[input_feature_test_arr,target_feature_test_df]
            

            transformation_pipeline=self.initiate_data_transformation()
            
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