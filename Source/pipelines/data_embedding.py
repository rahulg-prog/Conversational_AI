import os
import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from config.settings_loader import load_config
from utils.folder_operation import FolderOperation
logger = CustomLogger().get_logger(__name__)

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

class DataEmbedding:
    def __init__(self,chunks,path=None):
        try:
            load_dotenv()
            self.config = load_config()
            self.chunks = chunks
            self.path = path
            self.embeddings = OpenAIEmbeddings(
                model=self.config['model']['embedding_model'],
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            self.persist_directory = f"{self.path}/{self.config['embedding']['persist_directory']}"
        except Exception as e:
            raise DocumentPortalException(e, sys) from e
        
    def create_embeddings(self):
        try:
            if False == FolderOperation().create_folder(self.persist_directory):
                logger.info(f"Persist directory already exists at: {self.persist_directory}")
                print(f"Persist directory already exists at: {self.persist_directory}")
                return ""
            logger.info("Starting data embedding process.")
            vector_store = Chroma.from_texts(
                texts=[chunk["text"] for chunk in self.chunks],
                embedding=self.embeddings,
                metadatas=[chunk["metadata"] for chunk in self.chunks],
                persist_directory=self.persist_directory
            )
            vector_store.persist()
            logger.info("Data embedding completed and persisted successfully.")
            return vector_store
        except Exception as e:
            logger.error(f"Error during data embedding: {e}")
            raise DocumentPortalException(e, sys) from e

if __name__ == "__main__":
    try:
        from data_chunking import dataChunking
        from data_ingestion import DataIngestion

        # Ingest data
        data_ingestion = DataIngestion()
        records = data_ingestion.ingest_data()

        # Chunk data
        data_chunking = dataChunking(records)
        path, chunks = data_chunking.splitDocuments()

        # Embed data
        data_embedding = DataEmbedding(chunks,path = path)
        vector_store = data_embedding.create_embeddings()

    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise DocumentPortalException(e, sys) from e