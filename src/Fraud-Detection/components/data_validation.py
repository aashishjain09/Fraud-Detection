import os
from Fraud-Detection.entity import DataValidationConfig
from Fraud-Detection.logging import logger

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files_exist(self) -> bool:
        try:
            data_dir = os.path.join("artifacts", "data_ingestion")
            existing_files = set(os.listdir(data_dir))
            required_files = set(self.config.ALL_REQUIRED_FILES)

            validation_status = required_files.issubset(existing_files)

            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status
        except Exception as e:
            logger.error(f"Error occurred during validation: {e}")
            return False