import os
import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from config.settings_loader import load_config
logger = CustomLogger().get_logger(__name__)

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

class DataEmbedding:
    def __init__(self,chunks):
        try:
            load_dotenv()
            self.config = load_config()
            self.chunks = chunks
            self.embeddings = OpenAIEmbeddings(
                model=self.config['model']['embedding_model'],
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            self.persist_directory = self.config['embedding']['persist_directory']
        except Exception as e:
            raise DocumentPortalException(e, sys) from e
        
    def create_embeddings(self):
        try:
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
