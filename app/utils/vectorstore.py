import os
from pathlib import Path
import json
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings 
from langchain_core.documents import Document
from app.utils.masterpreprocess import MasterPreProcessor


class VectorStore:
    def __init__(self, index_path="faiss_index", model="text-embedding-3-small"):
        self.master_processor = MasterPreProcessor() 
        self.embeddings = OpenAIEmbeddings(model=model)
        self.index_path = index_path

    def create_documents(self, folder_path):
        """Iterates through folder and creates LangChain Document objects."""
        all_documents = []
        folder = Path(folder_path)
        
        for file in folder.iterdir():
            if file.suffix.lower() == '.md':
                # Use your header-based splitting logic
                docs = self.master_processor.split_markdown_to_documents(str(file))
                all_documents.extend(docs)
            elif file.suffix.lower() == '.txt':
                # Use your text loader logic
                docs = self.master_processor.text_to_document(str(file))
                all_documents.extend(docs)
        
        return all_documents

    def convert_to_vectorstore(self, documents):
        """Creates or updates a FAISS vector store."""
        if not documents:
            print("No new documents to add.")
            return

        if os.path.exists(self.index_path):
            # Update existing index
            print(f"Updating existing index at {self.index_path}...")
            existing_db = FAISS.load_local(
                self.index_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
            existing_db.add_documents(documents)
            existing_db.save_local(self.index_path)
            print("Update complete.")
        else:
            # Create new index
            print("Creating new FAISS index...")
            db = FAISS.from_documents(documents, self.embeddings)
            db.save_local(self.index_path)
            print(f"New index saved to {self.index_path}.")

    def trigger_process(self, data_folder):
        """Main entry point to run the ingestion pipeline."""
        print(f"Starting ingestion from: {data_folder}")
        
        # Step 1: Process files into LangChain Document objects
        docs = self.create_documents(data_folder)
        
        # Step 2: Convert/Update Vector Store
        self.convert_to_vectorstore(docs)
        print("Pipeline execution finished successfully.")