import os
import sys
import numpy as np
import pandas as pd
import pymongo
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from sklearn.model_selection import train_test_split

load_dotenv()
MONGO_DB_URL = os.getenv('MONGO_DB_URL')

class DataIngestion:
    data_ingestion_configuration = DataIngestionConfig()

    def export_collection_as_dataframe(self):
        try:
            database = self.data_ingestion_configuration.database_name
            collection = self.data_ingestion_configuration.collection_name
            mongo = pymongo.MongoClient(MONGO_DB_URL)
            db = mongo[database]
            collections = db[collection]
            df  = pd.DataFrame(list(collections.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns="_id")
            df.replace(['NA', 'null', None], np.nan,inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_configuration.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index = False,header = True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
           train_set,test_set = train_test_split(dataframe,test_size=self.data_ingestion_configuration.train_test_split_ratio,random_state=42)
           logging.info("Performed Test and Train split on the Dataframe")
           logging.info("Exited split_data_as_train_test_method of Data Ingestion class")
           train_file_path = self.data_ingestion_configuration.training_file_path
           os.makedirs(os.path.dirname(train_file_path),exist_ok=True)
           logging.info("Exporting Train and Test file")
           train_set.to_csv(train_file_path,index=False,header=True)
           test_set.to_csv(self.data_ingestion_configuration.testing_file_path,index = False, header = True)
           logging.info("Exported Train and Test File path")

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            return self.data_ingestion_configuration.training_file_path,self.data_ingestion_configuration.testing_file_path
        except Exception as e:
            raise NetworkSecurityException(e,sys)

