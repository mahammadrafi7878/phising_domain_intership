import pymongo 
import pandas as pd 
import json 
from phising_domain.config import mongo_db

from dotenv import load_dotenv
print(f"loading environment variable")
load_dotenv()


#client = pymongo.MongoClient("mongodb+srv://shaikmahammadrafi:6302593782@cluster1.zjnuzoq.mongodb.net/?retryWrites=true&w=majority") 


DATABASE_NAME="phsing_domaain"
COLLECTION_NAME="website"
FILE_PATH='/config/workspace/phising_dataset.csv' 


def drop_column(data):
    if 'Unnamed: 0' in data.columns:
        data.remove('Unnamed: 0',axis=1,inplace=True)
    return data
 
df=pd.read_csv(FILE_PATH)   


drop_column(df)  

print(f'number of columns and number of rows data contains{df.shape}') 

json_records=list(json.loads(df.T.to_json()).values()) 
print(json_records[0])

mongo_db[DATABASE_NAME][COLLECTION_NAME].insert_many(json_records)