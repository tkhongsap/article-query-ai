import re
from typing import List
from llama_index.core import Document

def parse_markdown(file_path: str) -> List[Document]:
    """Parse a markdown file into a list of Document objects,
    each representing a news article with its metadata."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content into sections by '---'
    sections = re.split(r'\n---\n', content)

    documents = []
    for section in sections:
        if section.strip():
            # Extract metadata using regex and handle missing fields
            metadata = {
                "id": re.search(r'id:\s*(.*)', section).group(1).strip() if re.search(r'id:\s*(.*)', section) else None,
                "title": re.search(r'title:\s*(.*)', section).group(1).strip() if re.search(r'title:\s*(.*)', section) else None,
                "slug": re.search(r'slug:\s*(.*)', section).group(1).strip() if re.search(r'slug:\s*(.*)', section) else None,
                "publishedAt": re.search(r'publishedAt:\s*(.*)', section).group(1).strip() if re.search(r'publishedAt:\s*(.*)', section) else None,
                "locale": re.search(r'locale:\s*(.*)', section).group(1).strip() if re.search(r'locale:\s*(.*)', section) else None,
                "excerpt": re.search(r'excerpt:\s*(.*)', section).group(1).strip() if re.search(r'excerpt:\s*(.*)', section) else None,
                "category": re.search(r'category:\s*(.*)', section).group(1).strip() if re.search(r'category:\s*(.*)', section) else None,
                "tags": re.findall(r'tags:\s*\[(.*?)\]', section)[0].split(', ') if re.search(r'tags:\s*\[(.*?)\]', section) else []
            }

            # Extract highlights if present
            highlights_match = re.search(r'## Highlights\n(.*?)(?=\n##|$)', section, re.DOTALL)
            highlights = highlights_match.group(1).strip() if highlights_match else ""

            # Extract content after '## Content'
            content_match = re.search(r'## Content\n(.*?)(?=\n##|$)', section, re.DOTALL)
            content = content_match.group(1).strip() if content_match else ""

            # Optional: Extract credit if present
            credit_match = re.search(r'## Credit\n(.*?)(?=\n---|$)', section, re.DOTALL)
            credit = credit_match.group(1).strip() if credit_match else ""

            # Combine highlights, content, and credit
            full_content = "\n\n".join(filter(None, [highlights, content, credit]))

            # Create Document object with full content and metadata
            doc = Document(text=full_content, metadata=metadata)
            documents.append(doc)

    return documents
