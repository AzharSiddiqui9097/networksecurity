from datetime import datetime
import os
from networksecurity.constants import training_pipeline

class TrainingPipelineConfig:
        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        pipeline_name = training_pipeline.PIPELINE_NAME
        artifact_name = training_pipeline.ARTIFACT_DIR
        artifact_dir = os.path.join(artifact_name,timestamp)

class DataIngestionConfig:
    def __init__(self):
        self.data_ingestion_config = TrainingPipelineConfig()
        self.data_ingestion_dir = os.path.join(self.data_ingestion_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME)
        self.training_file_path = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE_NAME)
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.datbase_name = training_pipeline.DATA_INGESTION_DATABASE_NAME