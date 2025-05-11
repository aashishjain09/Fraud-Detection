from Fraud-Detection.config.configuration import ConfigurationManager
from Fraud-Detection.components.data_ingestion import DataIngestion
from Fraud-Detection.logging import logger

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        data_ingestion = DataIngestion(config=ConfigurationManager().get_data_ingestion_config())
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()