import os 
from datetime import date 

DATABASE_NAME = 'US_VISA'

COLLECTION_NAME = 'visa_data'

MONGODB_URL_KEY = "mongodb+srv://utkarsh:utkarsh@cluster0.wtdbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

PIPELINE_NAME: str = "usvisa"
ARTIFACT_DIR: str ="artifact"

MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

FILE_NAME: str = "EasyVisa.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

'''
Data ingestion related constant
'''

DATA_INGESTION_COLLECTION_NAME: str = "visa_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_score"
DATA_INGESTION_INJESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2