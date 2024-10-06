from us_visa.configuration.mongo_db_connection import MongoDBClient
from us_visa.constants import DATABASE_NAME
from us_visa.exception import USVisaException
import pandas as pd
import sys
from typing import Optional
import numpy as np


class USVisaData:
    """
    This class help to export entire range db record as pandas dataframe.
    
    """
    
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise USVisaException(e, sys)
        
    def export_collection_as_dataframe(self, collection_name:str, database_name:Optional[str] = None) -> pd.DataFrame:
        
        try:
        
            """
            export entire collection as dataframe:
            return pd.DataFrame of collection
            """
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.database[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            if "id" in df.columns.to_list():
                df = df.drop(columns=["id"],axis=1)
            df.replace({"na":np.nan},inplace = True)
            return df
        except Exception as e:
            raise USVisaException(e, sys)
