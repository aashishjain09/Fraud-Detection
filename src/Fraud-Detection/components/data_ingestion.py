import os
from pathlib import Path
import urllib.request as request
import zipfile
from Fraud-Detection.logging import logger
from Fraud-Detection.utils.common import get_size
from Fraud-Detection.entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):  # -> str:
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL, 
                filename=self.config.local_data_file
            )
            logger.info(f"{filename} downloaded with headers: \n {headers}")
            # logger.info(f"Downloading file from: {self.config.source_URL} to {self.config.local_data_file}")
            # request.urlretrieve(self.config.source_URL, self.config.local_data_file)
            # logger.info(f"Downloaded file size: {get_size(self.config.local_data_file)}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")
            # logger.info(f"File already exists at {self.config.local_data_file}")

        # return self.config.local_data_file

    def extract_zip_file(self):  # -> str:
        """
        zip_file_path: str
        Extracts the zip file to the specified directory.
        Function returns None.
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        
        # if not os.path.exists(self.config.unzip_dir):
        #     logger.info(f"Extracting zip file to: {self.config.unzip_dir}")
        #     with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
        #         zip_ref.extractall(self.config.unzip_dir)
        #     logger.info(f"Extracted files to: {self.config.unzip_dir}")
        # else:
        #     logger.info(f"Unzip directory already exists at {self.config.unzip_dir}")

        # return self.config.unzip_dir
