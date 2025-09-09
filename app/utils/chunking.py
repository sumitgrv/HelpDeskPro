import re
from typing import List

def simple_markdown_chunk(text: str, max_tokens: int = 500) -> List[str]:
    # very rough chunker by paragraphs / headings
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) < max_tokens:
            current += (p + "\n\n")
        else:
            if current.strip():
                chunks.append(current.strip())
            current = p + "\n\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks
