import os
from urllib.parse import urlparse
from docling.document_converter import DocumentConverter

def url_to_filename(url: str, ext: str = ".md") -> str:
    path = urlparse(url).path.strip("/")
    if not path:
        path = "home"
    filename = path.replace("/", "_")
    return filename + ext


def crawl_and_convert(
    list_of_urls: list,
    output_dir: str = r"C:\github_work\Conversational_AI\Source\data\crawled_data"
):
    os.makedirs(output_dir, exist_ok=True)

    converter = DocumentConverter()
    documents = []

    for url in list_of_urls:
        result = converter.convert(url)
        doc = result.document
        documents.append(doc)

        filename = url_to_filename(url)
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(doc.export_to_markdown())

        print(f"Saved: {file_path}")

    return documents


if __name__ == "__main__":
    urls = [
        "https://www.honda2wheelersindia.com/services/maintenance/extended-warranty",
        "https://www.honda2wheelersindia.com/services/maintenance/extended-warranty-plus",
        "https://www.honda2wheelersindia.com/services/maintenance/annual-maintenance-contract",
        "https://www.honda2wheelersindia.com/services/maintenance/road-side-assistance",
        "https://www.honda2wheelersindia.com/services/maintenance/ev-care",
        "https://www.honda2wheelersindia.com/services/maintenance/recall-campaign",
        "https://www.honda2wheelersindia.com/services/maintenance/recall-campaign/product-recall-listing",
        "https://www.honda2wheelersindia.com/services",
        "https://www.honda2wheelersindia.com/services/maintenance",
    ]

    crawl_and_convert(urls)