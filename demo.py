# import sys
# from us_visa.logger import logging
# from us_visa.exception import USvisaException

# logging.info("Welcome to our custom log")

# try:
#     a = 1/"10"
# except Exception as e:
#     logging.info(e)
#     raise USvisaException(e,sys) from e


# from us_visa.constants import DATABASE_NAME
# print(DATABASE_NAME, "Welcome")

# from us_visa.constants import *   #To import all the constants from the file...

# print(DATABASE_NAME, "Welcome")

# print(COLLECTION_NAME, "Welcome")

from us_visa.pipeline.training_pipeline import TrainPipeline

pipeline = TrainPipeline()
pipeline.run_pipeline()