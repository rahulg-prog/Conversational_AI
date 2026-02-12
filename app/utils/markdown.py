from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document

def split_markdown_to_documents(input_file_path):
    """
    Splits a markdown file by '##' headers and returns a list of LangChain Document objects.
    """
    input_path = Path(input_file_path)
    
    # 1. Validation
    if not input_path.exists() or input_path.suffix.lower() != '.md':
        print(f"Error: Valid .md file not found at {input_file_path}")
        return []

    # 2. Configure Splitter (Splitting strictly by '##')
    # Metadata will track which 'Section' the text belongs to
    headers_to_split_on = [("##", "Section")]
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

    # 3. Read and Split
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # split_text returns a list of Document objects
    initial_splits = splitter.split_text(content)

    final_documents = []

    # 4. Refine Document Objects for FAISS
    for i, doc in enumerate(initial_splits):
        section_name = doc.metadata.get("Section", "General")
        refined_content = f"## {section_name}\n\n{doc.page_content}"
        new_doc = Document(
            page_content=refined_content,
            metadata={
                "source": input_path.name,
                "section": section_name,
                "chunk_index": i
            }
        )
        final_documents.append(new_doc)

    print(f"Created {len(final_documents)} Document objects from '{input_path.name}'.")
    return final_documents