import os
import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

logger = CustomLogger().get_logger(__name__)

class FolderOperation:
    def __init__(self):
        pass
    
    def create_folder(self,folder_path: str):
        """
        Creates a folder if it does not already exist.

        Args:
            folder_path (str): The path of the folder to be created.
        """
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
                logger.info(f"BY UTILS: Folder created successfully at: {folder_path}")
            else:
                logger.info(f"BY UTILS: Folder already exists at: {folder_path}")
                
        except Exception as e:
            logger.error(f"Error occurred while creating folder: {str(e)}")
            raise DocumentPortalException(e, sys)

if __name__ == "__main__":
    # Example usage
    test_path = "test_folder"
    FO = FolderOperation()
    FO.create_folder(test_path)