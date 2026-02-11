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
    # Redwing Motorcycles
    "https://www.honda2wheelersindia.com/motorcycle/shine-100",
    "https://www.honda2wheelersindia.com/motorcycle/shine-100-dx",
    "https://www.honda2wheelersindia.com/motorcycle/livo",
    "https://www.honda2wheelersindia.com/motorcycle/shine-125",
    "https://www.honda2wheelersindia.com/motorcycle/shine-125-limited-edition",
    "https://www.honda2wheelersindia.com/motorcycle/sp-125",
    "https://www.honda2wheelersindia.com/motorcycle/sp-125-anniversary-edition",
    "https://www.honda2wheelersindia.com/motorcycle/CB125-Hornet",
    "https://www.honda2wheelersindia.com/motorcycle/unicorn",
    "https://www.honda2wheelersindia.com/motorcycle/sp-160",
    "https://www.honda2wheelersindia.com/motorcycle/hornet-2-0",
    "https://www.honda2wheelersindia.com/motorcycle/nx200",

    # BigWing Motorcycles
    "https://www.honda2wheelersindia.com/motorcycle/CB-300F",
    "https://www.honda2wheelersindia.com/motorcycle/CB350",
    "https://www.honda2wheelersindia.com/motorcycle/CB350C",
    "https://www.honda2wheelersindia.com/motorcycle/CB350C-Special-Edition",
    "https://www.honda2wheelersindia.com/motorcycle/cb350-hness",
    "https://www.honda2wheelersindia.com/motorcycle/CB350RS",
    "https://www.honda2wheelersindia.com/motorcycle/nx-500",
    "https://www.honda2wheelersindia.com/motorcycle/CB650R",
    "https://www.honda2wheelersindia.com/motorcycle/CBR650R",
    "https://www.honda2wheelersindia.com/motorcycle/Hornet-750",
    "https://www.honda2wheelersindia.com/motorcycle/xl750-transalp",
    "https://www.honda2wheelersindia.com/motorcycle/hornet-1000-sp",
    "https://www.honda2wheelersindia.com/motorcycle/x-adv",
    "https://www.honda2wheelersindia.com/motorcycle/gold-wing",

    # Scooters
    "https://www.honda2wheelersindia.com/scooter/activa110",
    "https://www.honda2wheelersindia.com/scooter/activa110-anniversary-edition",
    "https://www.honda2wheelersindia.com/scooter/dio-110",
    "https://www.honda2wheelersindia.com/scooter/activa125",
    "https://www.honda2wheelersindia.com/scooter/activa125-anniversary-edition",
    "https://www.honda2wheelersindia.com/scooter/dio-125",
    "https://www.honda2wheelersindia.com/scooter/dio125-x-edition",

    # EV (Electric Vehicles)
    "https://www.honda2wheelersindia.com/e2w/products/activa-e",
    "https://www.honda2wheelersindia.com/e2w/products/qc1"
]
    crawl_and_convert(urls)