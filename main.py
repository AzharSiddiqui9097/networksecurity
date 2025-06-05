import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig

if __name__=="__main__":
    try:
        # dataingestion = DataIngestion()
        # train_path,test_path = dataingestion.initiate_data_ingestion()
        datavalidation = DataValidation()
        _,_,_,_ = datavalidation.initiate_data_validation()


    except Exception as e:
        raise NetworkSecurityException(e,sys)