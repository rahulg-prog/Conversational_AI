class MasterPreProcessor:
    def __init__(self):
        pass 

    def preprocess_to_md(input_path, target_folder="cleaned_markdowns"):

        """
        Validates, cleans, and saves the file as a new .md file in a specific directory.
        """
        import re
        import os
        from pathlib import Path
        input_file = Path(input_path)

        # 1. Validation: Ensure it's a Markdown file
        if not input_file.exists():
            print(f"Error: {input_path} not found.")
            return
        
        if input_file.suffix.lower() != '.md':
            print(f"Skipping: {input_path} is not a .md file.")
            return

        # 2. Create the directory (Standard for your Linode/DevOps environments)
        os.makedirs(target_folder, exist_ok=True)

        # 3. Define output path (Keeps the .md extension)
        output_path = Path(target_folder) / input_file.name

        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 4. Cleaning Logic
        # Remove image tags: , <!image>, <image>, etc.
        content = re.sub(r'<!?--?\s?image\s?--?>', '', content)
        content = re.sub(r'<!image>', '', content)
        
        # Remove navigation and visual clutter
        content = re.sub(r'Social Link|Toggle Accordion|Arrow|Icon', '', content)

        # Remove the massive footer section (Corporate/Legal)
        content = content.split("© 2025")[0]

        # Normalize spacing while preserving Markdown structure
        content = re.sub(r'\n{3,}', '\n\n', content)
        final_md = content.strip()

        # 5. Persistent Save
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_md)
        
        print(f"Done! Cleaned Markdown saved.")
        print(f"Path: {output_path.absolute()}")

    def process_xlsx_to_folder(file_path: str, output_folder: str = "kb_output"):
        """
        Parses an Excel file and saves each row as a separate .txt file.
        Organizes files into subfolders named after the sheets.
        """
        import pandas as pd
        import os
        from pathlib import Path
        import uuid
        from app.configs.config import model 
        from app.templates.prompt import AUGMENTATION_PROMPT
        from langchain_core.messages import HumanMessage, SystemMessage
        # Initialize the base output directory
        base_dir = Path(output_folder)
        base_dir.mkdir(parents=True, exist_ok=True)

        # Read all sheets 
        all_sheets = pd.read_excel(file_path, sheet_name=None)
        
        saved_files_count = 0

        for sheet_name, df in all_sheets.items():
            # Clean the sheet name for file system compatibility
            clean_sheet_name = "".join([c for c in sheet_name if c.isalnum() or c in (' ', '_')]).strip()
            sheet_dir = base_dir / clean_sheet_name
            sheet_dir.mkdir(exist_ok=True)

            # Drop empty rows/cols to save storage and tokens
            df = df.dropna(how='all').reset_index(drop=True)

            for index, row in df.iterrows():
                # Build the text content
                chunk_elements = [f"Source_Sheet: {sheet_name}", f"Row_Index: {index}"]
                
                for col_name in df.columns:
                    val = row[col_name]
                    chunk_elements.append(f"{col_name}: {val if pd.notna(val) else 'N/A'}")
                
                chunk_text = "\n".join(chunk_elements)

                # Generate a unique filename: row_{index}_{short_uuid}.txt
                unique_id = str(uuid.uuid4())[:8]
                file_name = f"row_{index}_{unique_id}.txt"
                file_path = sheet_dir / file_name
                augmented_chunk = model.invoke([SystemMessage(content=AUGMENTATION_PROMPT)]+[HumanMessage(content=f"RAW PAIR :\n{chunk_text}")])
                # Write to file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(augmented_chunk.content)
                
                saved_files_count += 1

        return f"Successfully saved {saved_files_count} files in '{output_folder}'"

    def _save_metadata_to_json(self, documents, original_path, suffix="_metadata.json"):
            """Helper to extract metadata from a list of Documents and save to JSON."""
            import json
            from pathlib import Path
            metadata_list = [doc.metadata for doc in documents]
            # Create metadata filename based on original file (e.g., data.md -> data_metadata.json)
            output_path = Path(original_path).with_name(f"{Path(original_path).stem}{suffix}")
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(metadata_list, f, indent=4)
            print(f"Metadata saved to: {output_path}")

    def split_markdown_to_documents(self, input_file_path):
        from langchain_text_splitters import MarkdownHeaderTextSplitter
        from langchain_core.documents import Document
        from pathlib import Path
        input_path = Path(input_file_path)
        if not input_path.exists() or input_path.suffix.lower() != '.md':
            return []

        headers_to_split_on = [("##", "Section")]
        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        initial_splits = splitter.split_text(content)
        final_documents = []

        for i, doc in enumerate(initial_splits):
            section_name = doc.metadata.get("Section", "General")
            refined_content = f"## {section_name}\n\n{doc.page_content}"
            
            new_doc = Document(
                page_content=refined_content,
                metadata={
                    "source": input_path.name,
                    "section": section_name,
                    "chunk_index": i
                }
            )
            final_documents.append(new_doc)

        # NEW: Save metadata to file
        self._save_metadata_to_json(final_documents, input_path)
        
        return final_documents

    def text_to_document(self, text_path):
        from langchain_community.document_loaders import TextLoader
        
        loader = TextLoader(text_path)
        docs = loader.load()
        
        # NEW: Save metadata to file
        self._save_metadata_to_json(docs, text_path)
        
        return docs