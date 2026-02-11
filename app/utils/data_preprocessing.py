import re
import os
from pathlib import Path

def preprocess_to_md(input_path, target_folder="cleaned_markdowns"):
    """
    Validates, cleans, and saves the file as a new .md file in a specific directory.
    """
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

# Example Usage
# preprocess_to_md("services_maintenance_extended-warranty.md", target_folder="cleaned_docs")
# Example usage for your local path structure
# preprocess_to_md("/home/ayan/WEBKNOT_AYAN/OFFICIAL/Conversational_AI/Source/Data/crawled_data/services_maintenance_annual-maintenance-contract.md", target_folder="processed_output")


import os

dir_path = "/home/ayan/WEBKNOT_AYAN/OFFICIAL/Conversational_AI/Source/Data/crawled_data"

file_paths = [
    os.path.join(dir_path, f)
    for f in os.listdir(dir_path)
    if os.path.isfile(os.path.join(dir_path, f))
]

for f in file_paths:
    preprocess_to_md(f)
