import os
from urllib.parse import urlparse
from docling.document_converter import DocumentConverter

def url_to_filename(url: str, ext: str = ".md") -> str:
    """Converts a URL into a safe filename."""
    path = urlparse(url).path.strip("/")
    if not path:
        path = "home"
    filename = path.replace("/", "_")
    return filename + ext

def crawl_and_convert(
    list_of_urls: list,
    output_dir: str = r"C:\Users\TECQNIO\Documents\conv_ai\Conversational_AI\Source\Data\2_crawled_data"
):
    """Processes a list of URLs and saves them as Markdown using Docling."""
    os.makedirs(output_dir, exist_ok=True)
    converter = DocumentConverter()
    
    for url in list_of_urls:
        try:
            print(f"Processing: {url}")
            result = converter.convert(url)
            doc = result.document
            
            filename = url_to_filename(url)
            file_path = os.path.join(output_dir, filename)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(doc.export_to_markdown())
            
            print(f"Successfully Saved: {filename}")
        except Exception as e:
            print(f"Failed to process {url}: {e}")

if __name__ == "__main__":
    # Path to your uploaded txt file
    file_path = "Conversational_AI\Source\web_crawl\urls.txt"
    
    # 1. Load URLs from the text file
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            # Read lines and strip whitespace/newlines
            urls = [line.strip() for line in f if line.strip()]
        
        # 2. Process the loaded URLs
        print(f"Loaded {len(urls)} URLs from {file_path}. Starting processing...")
        crawl_and_convert(urls)
    else:
        print(f"Error: {file_path} not found.")