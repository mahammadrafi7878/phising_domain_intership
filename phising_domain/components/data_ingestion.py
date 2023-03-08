import os,sys 
from phising_domain.logger import logging 
from phising_domain.exception import PhisingException 
from phising_domain.entity import config_entity,artifact_entity
import pandas as phsing_domaain
import numpy as np
from phising_domain import utils 
from sklearn.model_selection import train_test_split 





class DataIngestion:
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>> *20'}  DATA INGESTION {'<<' *20 }")
            self.data_ingestion_config=data_ingestion_config 
        except Exception as e:
            raise PhisingException(e,sys)


    


    def initiate_data_ingestion(self):
        try:
            logging.info(f"Transforming received collection as data frame")
            df=utils.get_collection_as_dataframe(data_base_name=self.data_ingestion_config.data_base_name,collection_name=self.data_ingestion_config.collection_name)

            logging.info(f'Dropping index column')
            df.drop(['_id'],axis=1,inplace=True)

            logging.info(f"if dat contain 'na' values replacing them with numpy nan valyues")
            df.replace(to_replace='na',value=np.NAN,inplace=True)

            logging.info(f'data set contains duplicate values so droping duplicate values')
            df.drop_duplicates()

            logging.info(f'creating feature store file if not exists')
            feature_store_dir=os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)

            logging.info(f"Storing data frame into  a .csv file")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            logging.info(f"spiting data into train and test parts")
            train_df,test_df=train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=777)

            logging.info(f"creating a dataset file if not exists")
            dataset_dir=os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info(f"storing train data set into train file")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)

            logging.info(f"storing test file into test.csv file")
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)

            logging.info(f"preparing artifact")
            data_ingestion_artifact=artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path,
            ) 
            
            logging.info(f"data ingestion artifact : {data_ingestion_artifact}")
            return data_ingestion_artifact


        except Exception as e:
            raise PhisingException(e,sys)


