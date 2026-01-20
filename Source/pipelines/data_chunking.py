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

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

class dataChunking:
    def __init__(self,records):
        try:
            self.config = load_config(r"C:\github_work\Conversational_AI\Source\config\config.yaml")
            self.records = records
            self.path = FolderOperation().create_folder(Path(f"{self.config['constant']['data_path']}/CS_{self.config['chunking']['chunk_size']}CO_{self.config['chunking']['chunk_overlap']}K_{self.config['retriever']['top_k']}"))
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
        return self.path,chunks

if __name__ == "__main__":
    try:
        from data_ingestion import DataIngestion

        data_ingestion = DataIngestion()
        records = data_ingestion.ingest_data()

        chunker = dataChunking(records)
        chunks = chunker.splitDocuments()
    except Exception as e:
        print(f"An error occurred: {e}")