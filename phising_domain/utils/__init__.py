import pandas as pd 
import numpy as np 
import os,sys
from phising_domain.logger import logging 
from phising_domain.exception import PhisingException 
from phising_domain.config import mongo_db
import yaml


def get_collection_as_dataframe(data_base_name:str,collection_name:str):
    try:
        df=pd.DataFrame(list(mongo_db[data_base_name][collection_name].find()))
        return df
        
    except Exception as e:
        raise PhisingException(e,sys)

def write_yaml_file(file_path,data):
    try:
        file_dir=os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"wb") as file:
            yaml.dump(data,file)
    except Exception as e:
        raise PhisingException(e,sys) 


def convert_columns_float(df,exclude_columns):
    try:
        for column in  df.columns:
            if column not in exclude_columns:
                df[column]=df[column].astype(float)
        return df
    except Exception as e:
        raise SensorException(e, sys)    