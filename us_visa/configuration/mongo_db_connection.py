import sys
from us_visa.exception import USVisaException
from us_visa.logger import logging

import os 
from us_visa.constants import DATABASE_NAME,MONGODB_URL_KEY
import pymongo
import certifi

ca = certifi.where()

class MongoDBClient:
    """
    Class Name : export_data_into_feature_store
    Description : This method exports the dataframe from the mongodb feature store as dataframe
    
    output : connection to mongodb database
    On Failure : raise an exception
    
    """
    client = None
    
    def __init__(self,database_name = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment Key: {MONGODB_URL_KEY} is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful")
        except Exception as e:
            raise USVisaException(e,sys)
        




# DB_name = "US_VISA"
# COLLECTION_NAME = "visa_data"
# CONNECTION_URL = "mongodb+srv://utkarsh:utkarsh@cluster0.wtdbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"