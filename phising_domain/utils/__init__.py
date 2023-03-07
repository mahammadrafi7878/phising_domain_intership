import pandas as pd 
import numpy as np 
import os,sys
from phising_domain.logger import logging 
from phising_domain.exception import PhisingException 
from phising_domain.config import mongo_db
import yaml
import dill

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
        with open(file_path,"w") as file:
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


def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise SensorException(e, sys) from e



def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"the file path is not exist")
        with open(file_path,"rb") as file:
            return dill.load(file) 
    except Exception as e:
        raise PhisingException(e,sys)  


def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file,array)
    except Exception as e:
        raise PhisingException(e,sys) 



def load_numpy_array_data(file_path:str):
    try:
        with open(file_path,"rb") as file:
            return np.load(file)

    except Exception as e:
        raise PhisingException(e,sys)
