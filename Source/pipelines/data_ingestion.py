import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from config.settings_loader import load_config

import json

# Instantiate CustomLogger to call the instance method get_logger
logger = CustomLogger().get_logger(__name__)

class DataIngestion:
    def __init__(self):
        try:
            self.config = load_config()
            self.clean_data_path = Path(self.config['data_ingestion']['clean_data'])
            self.raw_data_path = Path(self.config['data_ingestion']['raw_data'])
        except Exception as e:
            raise DocumentPortalException(e, sys) from e
        
    def load_data(self):
        try:
            with open(self.raw_data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except Exception as e:
            raise DocumentPortalException(e, sys) from e

    def ingest_data(self):
        try:
            logger.info("Starting data ingestion process.")
            self.data = self.load_data()
            logger.info("data loaded successfully.")
            records = []
            for section_key, items in self.data.items():
                if not isinstance(items, list):
                    continue

                for item in items:
                    records.append({
                        "section": section_key,
                        "id": item.get("id"),
                        "category": item.get("category"),
                        "subcategory": item.get("subcategory"),
                        "title": item.get("title"),
                        "content": item.get("content")
                    })
            logger.info("Data ingestion completed successfully.")
            return records
        except Exception as e:
            logger.error(f"Error during data ingestion: {e}")
            raise DocumentPortalException(e, sys) from e

if __name__ == "__main__":
    try:
        data_ingestion = DataIngestion()
        records = data_ingestion.ingest_data()
        print(f"Ingested {len(records)} records.")
    except Exception as e:
        print(f"An error occurred: {e}")