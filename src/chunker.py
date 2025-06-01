# src/chunker.py

from typing import List, Tuple
from langchain.docstore.document import Document
import tiktoken

# Use the right encoding for your target model (e.g., 'cl100k_base' for GPT-4, Ada-002, etc.)
ENCODING = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(ENCODING.encode(text))

def smart_chunk(
    elements: List[Tuple[str, str]],
    max_tokens: int = 1000
) -> List[Document]:
    """
    Chunk structured document elements into LangChain Document objects,
    respecting max token limits and preserving metadata.
    """
    chunks = []
    current_text = ""
    current_meta = {"section": None, "categories": []}
    current_tokens = 0

    for category, text in elements:
        # Start new chunk on Section/Title
        if category in ["Title", "SectionHeader"]:
            if current_text:
                chunks.append(Document(page_content=current_text.strip(), metadata=current_meta))
            current_meta = {"section": text, "categories": []}
            current_text = ""
            current_tokens = 0
        else:
            current_meta["categories"].append(category)

        # Count tokens
        tokens = count_tokens(text)
        if current_tokens + tokens > max_tokens:
            # Save current chunk and reset
            chunks.append(Document(page_content=current_text.strip(), metadata=current_meta))
            current_text = ""
            current_tokens = 0
            current_meta = {"section": current_meta["section"], "categories": []}

        # Add text
        current_text += f"{text}\n"
        current_tokens += tokens

    # Append last chunk
    if current_text:
        chunks.append(Document(page_content=current_text.strip(), metadata=current_meta))

    return chunks
