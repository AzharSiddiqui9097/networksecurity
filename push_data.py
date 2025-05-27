import os
import sys
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging 

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self,database,collection,file_path):
        try:
            self.database = database
            self.collection = collection
            self.file_path = file_path
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self):
        try:
            data = pd.read_csv(self.file_path)
            records = json.loads(data.to_json(orient='records'))
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self):
        try:
            records = self.csv_to_json_convertor()
            mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            db = mongo_client[self.database]
            mongo_collections = db[self.collection]
            mongo_collections.insert_many(records)
            return len(records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__=='__main__':
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "Azhar"
    COLLECTION = "NetworkData"
    network_obj = NetworkDataExtract(database=DATABASE,collection=COLLECTION,file_path=FILE_PATH)
    no_of_records = network_obj.insert_data_mongodb()
    print(no_of_records)

