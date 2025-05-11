from Fraud-Detection.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from Fraud-Detection.logging import logger

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>>> stage {STAGE_NAME} completed successfully!")
except Exception as e:
    logger.exception(e)
    raise e