import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from config.settings_loader import load_config
from docling.document_converter import DocumentConverter
from pathlib import Path
from typing import Union, List
import os

config = load_config()

class DoclingMarkdownConverter:
    def __init__(self, output_dir: str = config["data_ingestion"]["markdown_data"]):
        self.converter = DocumentConverter()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def convert(self, sources: Union[str, List[str]]):
        """
        Accepts a single source or list of sources.
        """
        if isinstance(sources, str):
            sources = [sources]

        for source in sources:
            self._process_source(source)

    def _process_source(self, source: str):
        try:
            doc = self.converter.convert(source).document
            markdown_content = doc.export_to_markdown()

            file_name = self._generate_filename(source)
            file_path = self.output_dir / f"{file_name}.md"

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            print(f"✅ Saved: {file_path}")

        except Exception as e:
            print(f"❌ Failed to process {source}: {e}")

    def _generate_filename(self, source: str) -> str:
        if source.startswith("http"):
            name = source.rstrip("/").split("/")[-1] or "index"
        else:
            name = Path(source).stem
        return name
    
# -----------------------
# Example Usage
# -----------------------

if __name__ == "__main__":
    from web_crawl.list import all_pages
    converter = DoclingMarkdownConverter()

    # Single input
    # for i in all_pages:
    #     converter.convert(i)
        
    converter.convert(
        r"C:\github_work\Conversational_AI\Source\data\raw_data\Final.xlsx"
    )

    # # Multiple mixed inputs
    # converter.convert([
    #     "https://example.com/page",
    #     "sample.pdf",
    #     "document.docx",
    #     "financials.xlsx"
    # ])
