import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

import re
from pathlib import Path
from typing import Union, List

class MarkdownCleaner:

    def __init__(self):
        self.default_strings_to_remove = [
            "<!-- image -->"
        ]

    def process(self, paths: Union[str, List[str]]):
        """
        Accepts single file path or list of file paths.
        """
        if isinstance(paths, str):
            paths = [paths]

        for file_path in paths:
            self._clean_file(Path(file_path))

    def _clean_file(self, file_path: Path):
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = self._remove_newsletter(content)
        content = self._remove_exact_strings(content)
        content = self._remove_markdown_links(content)
        content = self._remove_extra_blank_lines(content)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Cleaned: {file_path}")

    def _remove_newsletter(self, content: str) -> str:
        pattern = r"### Signup for Newsletter[\s\S]*"
        return re.sub(pattern, "", content)

    def _remove_exact_strings(self, content: str) -> str:
        for string in self.default_strings_to_remove:
            content = content.replace(string, "")
        return content

    def _remove_markdown_links(self, content: str) -> str:
        content = re.sub(r"\[[^\]]*\]\([^)]*\)", "", content)
        content = re.sub(r"\(\s*\)", "", content)
        return content

    def _remove_extra_blank_lines(self, content: str) -> str:
        return re.sub(r"\n{3,}", "\n\n", content)

if __name__ == "__main__":
    from utils.folder_operation import FolderOperation
    FO = FolderOperation()
    markdown_files = FO.list_files(r"C:\github_work\Conversational_AI\Source\data\crawled_data", recursive=False)
    cleaner = MarkdownCleaner()
    cleaner.process(markdown_files)

    # # Single file
    # cleaner.process("path/to/file.md")

    # # Multiple files
    # cleaner.process([
    #     "file1.md",
    #     "file2.md",
    #     "file3.md"
    # ])