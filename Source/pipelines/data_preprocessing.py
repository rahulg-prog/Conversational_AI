import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from config.settings_loader import load_config
import os

config = load_config()

import re

def remove_newsletter_from_file(file_path: str):
    """
    Removes everything from '### Signup for Newsletter'
    till the end of the markdown file.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"### Signup for Newsletter[\s\S]*"
    cleaned_content = re.sub(pattern, "", content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cleaned_content)

    print(f"✅ Cleaned file: {file_path}")
    
remove_newsletter_from_file()
