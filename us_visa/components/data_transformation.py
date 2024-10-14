import sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek,SMOTEENN
from sklearn.pipeline import Pipeline 
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer

from us_visa.constants import TARGET_COLUMN, TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from us_visa.entity.config_entity import DataTransformationConfig 
from us_visa.entity.artifact_entity import DataTransformationArtifact,DataInjectionArtifact, DataValidationArtifact
from us_visa.exception import USVisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import save_object, save_numpy_array_data,read_yaml_file,drop_columns
from us_visa.entity.estimator import TargetValueMapping

class DataTransformation:
    def __init__(self, data_ingestion_artifact:DataInjectionArtifact,
                       data_transformation_config:DataTransformationConfig,
                       data_validation_artifact:DataValidationArtifact):
        
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: Configuration for data transformation
        :param data_validation_artifact: Output reference of data validation artifact stage
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path = SCHEMA_FILE_PATH)
        except Exception as e:
            raise USVisaException(e, sys) from e
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USVisaException(e, sys) from e
        
    def get_data_transformer_object(self) -> Pipeline:
        """
        Method Name: get_data_transformer_object
        Description: This method created and returns the data transformation pipeline object
        
        Output:  data transformer object is created and returned
        On Failure: Write an exception log and then raise an exception
        """
        try:
            logging.info(f"Got numerical cols from schema config")
            
            numerical_transformer = StandardScaler()
            oh_transformer = OneHotEncoder()
            ordinal_encoder = OrdinalEncoder()
            
            logging.info(f"Initialized StandardScaler, OneHotEncoder, OrdinalEncoder")
            
            oh_columns = self._schema_config['oh_columns']
            or_columns = self._schema_config['or_columns']
            transform_columns = self._schema_config['transform_columns']
            num_features = self._schema_config['num_features']

            logging.info("initialize PowerTransformer")
            
            transform_pipe = Pipeline(steps = [
                ('transformer',PowerTransformer(method='yeo-johnson'))
            ])
            preprocessor = ColumnTransformer(
                [
                    ('OneHotEncoder', oh_transformer, oh_columns),
                    ('OrdinalEncoder', ordinal_encoder, or_columns),
                    ('Transformer', transform_pipe, transform_columns),
                    ('StandardScaler', numerical_transformer, num_features)
                ]
            )
            
            logging.info(f"Created preprocessor object from ColumnTransformer")
            
            logging.info(f"Excited get_data_transformer_object method of DataTransformation class")
            
            return preprocessor
        
        except Exception as e:
            raise USVisaException(e, sys) from e
        
    def initiate_data_transformation(self,) -> DataTransformationArtifact:
        """
        Method Name: initiate_data_transformation
        Description: This method initiates the data transformation pipeline
        
        Output:  data transformation artifact object is created and returned
        On Failure: Write an exception log and then raise an exception
        """
        try:
            if self.data_validation_artifact.validation_status:
                logging.info(f"Starting data transformation.")
                preprocessor = self.get_data_transformer_object()
                logging.info(f"Got the preprocessor object.")
                
                train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)
                
                input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis= 1)
                target_feature_train_df = train_df[TARGET_COLUMN]
                
                logging.info(f"Got train features and test features of Training dataset")
                
                input_feature_train_df['company_age'] = CURRENT_YEAR - input_feature_train_df['yr_of_estab']
                
                logging.info(f"Added company_age column to the Training dataset.")
                
                drop_cols = self._schema_config['drop_columns']
                
                logging.info(f"Drop the columns in drop_cols of Training dataset.")
                
                input_feature_train_df = drop_columns(df=input_feature_train_df, cols = drop_cols)
                
                # logging.info(f"Got input dataset features.[{input_feature_train_df}]")
                
                target_feature_train_df = target_feature_train_df.replace(
                    TargetValueMapping()._asdict()
                )
                
                logging.info(f"Got input dataset features.[{target_feature_train_df}]")
                
                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
                
                target_feature_test_df = test_df[TARGET_COLUMN]
                
                input_feature_test_df['company_age'] = CURRENT_YEAR-input_feature_test_df['yr_of_estab']
                
                logging.info(f"Added company_age column to the Test dataset.")
                
                # logging.info(f"printing input features before dropping columns[{input_feature_train_df}]")
                input_feature_test_df = drop_columns(df=input_feature_test_df, cols = drop_cols)
                # logging.info(f"printing input features after dropping columns[{input_feature_train_df}]")
                
                logging.info(f"Drop the columns in drop_cols of Test dataset.")
                
                target_feature_test_df = target_feature_test_df.replace(TargetValueMapping()._asdict())
                
                logging.info(f"Got train features and test features of Testing dataset.")
                logging.info(f"Applying preprocessing object on training dataframe and testing dataframe.")
                
                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
                
                logging.info(f"Used the preprocessor object to transform the train feature")
                
                input_feature_test_arr = preprocessor.transform(input_feature_test_df)
                
                logging.info(f"Final Train test [{input_feature_train_arr}]")
                logging.info(f"Final target set[{target_feature_train_df}]")
                logging.info(f"Used the preprocessor object to transform the test feature")
                
                logging.info(f"Applying SMOTEENN on Training dataset.")
                
                smt = SMOTEENN(sampling_strategy="minority") #Handle imbalance in dataset.
                input_feature_train_final, target_feature_train_final = smt.fit_resample(input_feature_train_arr, target_feature_train_df)
                
                logging.info(f"Applied SMOTEENN on training dataset.")
                logging.info(f"Applying SMOTEENN on teting dataset.")
                
                input_feature_test_final, target_feature_test_final = smt.fit_resample(input_feature_test_arr, target_feature_test_df)
                
                logging.info(f"Applied SMOTEENN on testing dataset.")
                
                logging.info(f"Created train array and test array.")
                
                train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
                
                test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]
                
                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)

                logging.info(f"Saved the preprocessor object.")
                
                logging.info(f"Exited initiate_data_transformation method of Data_transformation class.")
                
                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )                
                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)
        except Exception as e:
            raise USVisaException(e, sys) from e
        
                