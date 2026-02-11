# First, install the library: pip install ultimate-sitemap-parser
from usp.tree import sitemap_tree_for_homepage

# Target website
url = "https://www.honda2wheelersindia.com/"

# Fetch and recursively parse the sitemap tree
tree = sitemap_tree_for_homepage(url)

# Extract and print all URLs
for page in tree.all_pages():
    print(page.url)