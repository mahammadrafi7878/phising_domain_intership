import pandas as pd 
import numpy as np 
import os,sys
from phising_domain.logger import logging 
from phising_domain.exception import PhisingException 
from phising_domain.config import mongo_db


def get_collection_as_dataframe(data_base_name:str,collection_name:str):
    try:
        df=pd.DataFrame(list(mongo_db[data_base_name][collection_name].find()))
        return df
        
    except Exception as e:
        raise PhisingException(e,sys)