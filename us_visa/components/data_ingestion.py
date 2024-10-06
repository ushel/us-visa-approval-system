import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataInjectionArtifact
from us_visa.exception import USVisaException
from us_visa.logger import logging
from us_visa.data_access.usvisa_data import USVisaData

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig = DataIngestionConfig()):
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise USVisaException(e, sys)
        
    def export_data_into_feature_store(self) -> DataFrame:
        """
        Method Name : export_data_into_feature_store
        Description : This method will export data from mongodb to datafile
        
        Output : data is returned as artifact of data ingestion components
        On Failure : Write an exception log and then raise an exception
        """
        
        try:
            logging.info(f"Exporting data from mongodb")
            usvisa_data = USVisaData()
            dataframe = usvisa_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            
            logging.info(f"Shape of datafrmae: {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise USVisaException(e, sys)
    
    def split_data_as_train_test(self, dataframe:DataFrame) -> None:
        """
        Method Name: split_data_as_train_test
        Description: This method will split data into train and test datasets based on split ratio
        
        output : Folder is created in s3 bucket
        On Failure: Write an exception log and then raise an exception
        """
        
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")
        
        try:
            train_set, test_set = train_test_split(dataframe,test_size = self.data_ingestion_config.train_test_split_ratio)
            logging.info(f"Performed train test split on the dataframe")
            logging.info(f"Exited split_data_as_train_test method of Data_Ingestion class")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            
            logging.info(f"Exported train and test path.")
        except Exception as e:
            raise USVisaException(e, sys) from e
        
    def initiate_data_ingestion(self)->DataInjectionArtifact:
        """
        Method Name: initiate_data_ingestion
        Description: This method will initiate data ingestion components for training pipeline
        
        Output: Train set and test set are returned as the artifacts of data ingestion components
        On Failure: Write an exception log and then raise an exception
        
        """
        logging.info(f"Entered initiate_data_ingestion method of Data_ingestion class")
        
        try:
            dataframe = self.export_data_into_feature_store()
            logging.info(f"Got the data from mongodb")
            
            self.split_data_as_train_test(dataframe)
            logging.info(f"Performed train_test_split on the dataset.")
            
            logging.info(f"Exited initiate_data_ingestion method of Data_ingestion class.")
            
            data_ingestion_artifact = DataInjectionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path = self.data_ingestion_config.testing_file_path)
            
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise USVisaException(e, sys) from e
            
            
                    

