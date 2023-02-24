from phising_domain.logger import logging 
from phising_domain.exception import PhisingException 
import pandas as pd 
import numpy as numpy 
import os,sys 
from phising_domain.utils import get_collection_as_dataframe

print(__name__)
if __name__ == '__main__':
     try:
          df=get_collection_as_dataframe(data_base_name='phsing_domaain', collection_name='website')
          print(df.shape)
     except Exception as e:
          raise PhisingException(e,sys)