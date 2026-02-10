import pandas as pd
import os
from pathlib import Path
import uuid
from app.configs.config import model 
from app.templates.prompt import AUGMENTATION_PROMPT
from langchain_core.messages import HumanMessage, SystemMessage
def process_xlsx_to_folder(file_path: str, output_folder: str = "kb_output"):
    """
    Parses an Excel file and saves each row as a separate .txt file.
    Organizes files into subfolders named after the sheets.
    """
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

# --- Usage ---
result = process_xlsx_to_folder("/home/ayan/WEBKNOT_AYAN/OFFICIAL/Conversational_AI/Source/Data/raw_data/Final.xlsx", "honda_knowledge_base")
print(result)