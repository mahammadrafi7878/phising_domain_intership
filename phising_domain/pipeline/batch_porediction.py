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
        logging.info(f"creating prediction directory")
        os.makedirs(PREDICTION_DIR,exist_ok=True)

        logging.info(f'Creating model resolver object')
        model_resolver=ModelResolver(model_registery="saved_models")

        logging.info(f"reading input file :{input_file_path}")
        df=pd.read_csv(input_file_path)
        logging.info(f"replacing na values with np.nan")
        df.replace({'na':np.NAN},inplace=True)

        logging.info(f"Loading transformer to transform dataset")
        transfomer=load_object(file_path=model_resolver.get_latest_transformer_path())

        input_feature_names=list(transfomer.feature_names_in_)
        input_arr=transfomer.transform(df[input_feature_names])


        logging.info(f"loading the model to make predictions ")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr) 

        df["prediction"]=prediction

        prediction_file_name=os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")

        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        return prediction_file_path
    except Exception as e:
        raise PhisingException(e,sys)