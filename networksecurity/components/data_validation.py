from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os,sys
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self):
        try:
            self.data_ingestion_artifact = DataIngestion()
            self.data_validation_configuration = DataValidationConfig()
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame):
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def detect_dataset_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,threshold=0.05):
        try:
            status = True
            report = {}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({col:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }})
            drift_report_file_path = self.data_validation_configuration.drift_report_file_path

            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(drift_report_file_path,content=report)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self):
        try:
            train_file_path,test_file_path = self.data_ingestion_artifact.initiate_data_ingestion()
            train_dataframe = pd.read_csv(train_file_path)
            test_dataframe = pd.read_csv(test_file_path)
            status = self.validate_number_of_columns(train_dataframe)
            if status == False:
                error_message_train = "Train Dataframe doesn't contain all columns"
            status = self.validate_number_of_columns(test_dataframe)
            if status == False:
                error_message_test = "Test Dataframe doesn't contain all columns" 
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            os.makedirs(os.path.dirname(self.data_validation_configuration.valid_test_file_path),exist_ok=True)
            train_dataframe.to_csv(
                self.data_validation_configuration.valid_train_file_path, index=False, header=True

            )

            test_dataframe.to_csv(
                self.data_validation_configuration.valid_test_file_path, index=False, header=True
            )
            # valid_train_file_path,valid_test_file_path= self.data_ingestion_artifact.initiate_data_ingestion()
            return status,train_file_path,test_file_path,self.data_validation_configuration.drift_report_file_path
        except Exception as e:
            raise NetworkSecurityException(e,sys)