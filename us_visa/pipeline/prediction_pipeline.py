import os
import sys

import numpy as np 
import pandas as pd 
from us_visa.entity.config_entity import USVisaPredictionConfig, USVisaPredictionConfiguration
from us_visa.entity.s3_estimator import USVisaEstimator
from us_visa.exception import USVisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file
from pandas import DataFrame

class USVisaData:
    def __init__(self,
                 continent,
                 education_of_employees,
                 has_job_experience,
                 requires_job_training,
                 no_of_employees,
                 region_of_employment,
                 prevailing_wage,
                 unit_of_wage,
                 full_time_position,
                 company_age):
        
        """
        USVisa Data constructor
        
        Input: all features of the trained model for prediction
        
        """
        try:
            self.continent = continent
            self.education_of_employees = education_of_employees
            self.has_job_experience = has_job_experience
            self.requires_job_training = requires_job_training
            self.no_of_employees = no_of_employees
            self.region_of_employment = region_of_employment
            self.prevailing_wage = prevailing_wage
            self.unit_of_wage = unit_of_wage
            self.full_time_position = full_time_position
            self.company_age = company_age
        except Exception as e:
            raise USVisaException(e,sys) from e
        
        
    def get_usvisa_input_data_frame(self) -> DataFrame:
        """
        This function returns a DataFrame from USVisaData class input
        """
        try:
            usvisa_input_dict = self.get_usvisa_data_as_dict()
            return DataFrame(usvisa_input_dict)
        except Exception as e:
            raise USVisaException(e,sys) from e
        
    def get_usvisa_data_as_dict(self):
        """_
        This function returns a dictionary from USVisaData class input
        """
        logging.info("Entered get_usvisa_data_as_dict method as USVisaData class")
        try:
            input_data = {
                "continent": [self.continent],
                "education_of_employees": [self.education_of_employees],
                "has_job_experience": [self.has_job_experience],
                "requires_job_training": [self.requires_job_training],
                "no_of_employees": [self.no_of_employees],
                "region_of_employment": [self.region_of_employment],
                "prevailing_wage": [self.prevailing_wage],
                "unit_of_wage": [self.unit_of_wage],
                "full_time_position": [self.full_time_position],
                "company_age": [self.company_age],
            }
            logging.info("Created usvisa data dict")
            logging.info("Exited get_usvisa_data_as_dict method as USVisa class")
            
            return input_data
        except Exception as e:
            raise USVisaException(e,sys) from e
        
class USVisaClassifier:
    def __init__(self,prediction_pipeline_config:USVisaPredictionConfig = USVisaPredictionConfig(), ) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise USVisaException(e, sys) from e
        
    def predict(self,dataframe) -> str:
        """
        This is the method of USVisaClassifier
        Returns: Prediction in string format
        """
        
        try:
            logging.info("Entered predict method od USVisaClassifier class")
            model = USVisaEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result = model.predict(dataframe)
            
            return result
        except Exception as e:
            raise USVisaException(e,sys) from e
                
            