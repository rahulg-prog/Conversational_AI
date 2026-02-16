import os
import sys
from pathlib import Path
from typing import List

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

logger = CustomLogger().get_logger(__name__)

class FolderOperation:
    def __init__(self):
        pass

    def create_folder(self, folder_path: str):
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
                logger.info(f"BY UTILS: Folder created successfully at: {folder_path}")
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Error occurred while creating folder: {str(e)}")
            raise DocumentPortalException(e, sys)

    def list_files(self, folder_path: str, recursive: bool = True) -> List[str]:
        """
        Return a list of file paths inside `folder_path`.
        - `recursive=True` walks subdirectories (default).
        - `recursive=False` lists only immediate files.
        """
        try:
            folder = Path(folder_path)
            if not folder.exists() or not folder.is_dir():
                raise DocumentPortalException(f"Folder not found: {folder_path}", sys)

            if recursive:
                files = [str(p) for p in folder.rglob("*") if p.is_file()]
            else:
                files = [str(p) for p in folder.iterdir() if p.is_file()]

            return files

        except DocumentPortalException:
            raise
        except Exception as e:
            logger.error(f"Error listing files in {folder_path}: {e}")
            raise DocumentPortalException(e, sys)

if __name__ == "__main__":
    # Example usage
    test_path = "test_folder"
    FO = FolderOperation()
    FO.create_folder(test_path)
    print(FO.list_files(test_path))