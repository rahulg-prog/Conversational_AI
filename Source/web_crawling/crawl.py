import asyncio
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import requests
from xml.etree import ElementTree

async def crawl_sequential(urls: List[str]):
    print("\n=== Sequential Crawling with Session Reuse ===")

    browser_config = BrowserConfig(
        headless=True,
        # For better performance in Docker or low-memory environments:
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )

    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )

    # Create the crawler (opens the browser)
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    try:
        session_id = "session1"  # Reuse the same session across all URLs
        for url in urls:
            result = await crawler.arun(
                url=url,
                config=crawl_config,
                session_id=session_id
            )
            if result.success:
                print(f"Successfully crawled: {url}")
                # Save markdown to a file
                import re, os
                safe_filename = re.sub(r'[^a-zA-Z0-9_-]', '_', url.replace('https://', '').replace('http://', ''))
                output_dir = "scraped_markdown"
                os.makedirs(output_dir, exist_ok=True)
                file_path = os.path.join(output_dir, f"{safe_filename}.md")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(result.markdown.raw_markdown)
                print(f"Saved markdown to {file_path}")
            else:
                print(f"Failed: {url} - Error: {result.error_message}")
    finally:
        # After all URLs are done, close the crawler (and the browser)
        await crawler.close()

def get_pydantic_ai_docs_urls():
    import os
    
    # Get the path to sitemap.txt in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sitemap_file = os.path.join(script_dir, "sitemap.txt")
    
    try:
        # Read the local sitemap.txt file
        with open(sitemap_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Wrap content in root element for proper XML parsing
        xml_content = f"<urlset>{content}</urlset>"
        root = ElementTree.fromstring(xml_content)
        
        # Extract all URLs from the <loc> tags
        urls = [loc.text for loc in root.findall('.//loc')]
        
        return urls
    except Exception as e:
        print(f"Error reading sitemap: {e}")
        return []

async def main():
    urls = get_pydantic_ai_docs_urls()
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        await crawl_sequential(urls)
    else:
        print("No URLs found to crawl")

if __name__ == "__main__":
    asyncio.run(main())