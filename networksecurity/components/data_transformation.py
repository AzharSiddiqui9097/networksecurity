import os
import sys
import pandas as pd
import numpy as np

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants import training_pipeline
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_objects,save_numpy_array_data

class DataTransformation:
    def __init__(self):
        try:
            self.data_validation_artifact = DataValidation()
            self.data_transformation_configuration = DataTransformationConfig()
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def read_data(self,file_path):
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def 
