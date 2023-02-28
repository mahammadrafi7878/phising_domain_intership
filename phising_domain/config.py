import os,sys 
import pymongo 
from dataclasses import dataclass 

from dotenv import load_dotenv
print(f"loading .env variable ")
load_dotenv() 


@dataclass
class EnvironmentVariable:
    mongo_db_url=os.getenv('MONGO_DB_URL')  

object=EnvironmentVariable()
mongo_db=pymongo.MongoClient(object.mongo_db_url) 


TARGET_COLUMN='phishing'