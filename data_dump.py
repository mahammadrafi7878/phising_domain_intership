import pymongo 
import pandas as pd 
import json 


client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB") 


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

client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_records)