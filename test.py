from phising_domain.logger import logging 
from phising_domain.exception import PhisingException 
import pandas as pd 
import numpy as numpy 
import os,sys 
from phising_domain.utils import get_collection_as_dataframe
from phising_domain.components.data_ingestion import DataIngestion
from phising_domain.entity import config_entity,artifact_entity
from phising_domain.components.data_validation import DataValidation

print(__name__)
if __name__ =='__main__':
    try:
        train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
        for i in train_df.dtypes:
            print(i)
    except Exception as e:
        raise PhisingException(e,sys)