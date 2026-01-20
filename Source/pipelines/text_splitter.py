import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from config.settings_loader import load_config

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0,separators=["\n\n", "\n", ".", " ", ""])
class chunking:
    def __init__(self, document: str):
        self.config = CustomLogger.load_config("C:/github_work/Conversational_AI/Source/config/config.yaml")
        self.logger = CustomLogger().get_logger(__name__)
        self.document = document
        
    def chunk_text(self) -> list[str]:
        try:
            self.logger.info("Starting text chunking process.")
            chunks = text_splitter.split_text(self.document)
            self.logger.info(f"Text chunking completed. Number of chunks created: {len(chunks)}")
            return chunks
        except Exception as e:
            self.logger.error(f"An error occurred during text chunking: {e}")
            raise DocumentPortalException(e) from e