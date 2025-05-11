from Fraud-Detection.config.configuration import ConfigurationManager
from Fraud-Detection.components.data_validation import DataValidation
from Fraud-Detection.logging import logger

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        data_validation = DataValidation(config=ConfigurationManager().get_data_validation_config())
        data_validation.validate_all_files_exist()