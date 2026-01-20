import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
logger = CustomLogger().get_logger(__name__)
from config.settings_loader import load_config

from langchain_text_splitters import RecursiveCharacterTextSplitter

class dataChunking:
    def __init__(self,records):
        try:
            self.config = load_config()
            self.records = records
        except Exception as e:
            raise DocumentPortalException(e, sys) from e
        
    def splitDocuments(self):
        logger.info("Starting document chunking process.")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config['chunking']['chunk_size'],
            chunk_overlap=self.config['chunking']['chunk_overlap'],
            separators=["\n\n", "\n", ".", " ", ""]
        )

        chunks = []

        for record in self.records:
            if not record["content"]:
                continue

            split_texts = splitter.split_text(record["content"])

            for i, text in enumerate(split_texts):
                chunks.append({
                    "chunk_id": f"{record['id']}__chunk_{i}",
                    "text": text,
                    "metadata": {
                        "section": record["section"],
                        "category": record["category"],
                        "subcategory": record["subcategory"],
                        "title": record["title"],
                        "source_id": record["id"]
                    }
                })
        logger.info(f"Document chunking completed. Generated {len(chunks)} chunks.")
        return chunks

if __name__ == "__main__":
    try:
        from data_ingestion import DataIngestion

        data_ingestion = DataIngestion()
        records = data_ingestion.ingest_data()

        chunker = dataChunking(records)
        chunks = chunker.splitDocuments()
    except Exception as e:
        print(f"An error occurred: {e}")