import uuid
from typing import List, Tuple
from qdrant_client.models import PointStruct
from ..utils.chunking import simple_markdown_chunk
from ..services.embeddings import embed_texts
from ..services.qdrant_service import ensure_collection, upsert_points, search
from ..config import settings
from ..utils.logging import logger
import json
import os

def load_file_bytes(path: str) -> str:
    # very simple loader; assumes text-like files or uses fallback
    if path.lower().endswith(".md") or path.lower().endswith(".txt"):
        return open(path, "r", encoding="utf-8", errors="ignore").read()
    if path.lower().endswith(".pdf"):
        # avoid heavy deps; in real project use pymupdf or pdfminer
        try:
            import fitz  # pymupdf
            doc = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception:
            return ""
    if path.lower().endswith(".docx"):
        try:
            import docx
            d = docx.Document(path)
            return "\n".join([p.text for p in d.paragraphs])
        except Exception:
            return ""
    # fallback
    return open(path, "rb").read().decode("utf-8", errors="ignore")

def index_document(document_id: str, file_path: str) -> Tuple[int, int]:
    text = load_file_bytes(file_path)
    chunks = simple_markdown_chunk(text, max_tokens=1200)
    vectors = embed_texts(chunks)
    ensure_collection(dim=len(vectors[0]))
    points = []
    for idx, (chunk, vec) in enumerate(zip(chunks, vectors)):
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vec,
            payload={
                "document_id": document_id,
                "chunk_index": idx,
                "content": chunk
            }
        ))
    upsert_points(points)
    return len(chunks), len(points)

def generate_answer(question: str, context_chunks: List[str]) -> str:
    # Simple template; if OPENAI_API_KEY is present we could use OpenAI via requests.
    # To keep docker-friendly and offline capable, we do a rule-based summarization.
    header = "You are HelpDeskPro, an assistant that answers using the provided knowledge.
"
    instruction = "Answer the user's question using only the context. Cite sources as [doc:chunk] indices.

"
    ctx = "\n---\n".join([f"[{i}] {c[:1000]}" for i, c in enumerate(context_chunks)])
    body = f"Context:\n{ctx}\n\nQuestion: {question}\nAnswer:"
    answer = header + instruction + body
    # naive composition: echo top chunks
    synthesis = "\n".join([f"- See [{i}] for details." for i in range(len(context_chunks))])
    return f"{question}\n\nBased on the knowledge base:\n{synthesis}"
