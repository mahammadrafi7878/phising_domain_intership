from phising_domain.exception import PhisingException 
from phising_domain.logger import logging 
import os,sys 
import pandas as pd 
import numpy as np 
from phising_domain.utils import load_object 
from datetime import datetime 
from phising_domain.predictor import ModelResolver 


PREDICTION_DIR='prediction'

def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)

        model_resolver=ModelResolver(model_registery="saved_models")

        df=pd.read_csv(input_file_path)
        df.replace({'na':np.NAN},inplace=true)

        transfomer=load_object(file_path=model_resolver.get_latest_transformer_path())

        input_feature_names=list(transformers.input_feature_names_in_)
        input_arr=transformer.transform(df[input_feature_names])

        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr) 

        df["prediction"]=prediction
    except Exception as e:
        raise PhisingException(e,sys)