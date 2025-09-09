from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..schemas import QueryRequest
from ..repositories import add_message, create_answer, add_citation
from ..services.embeddings import embed_texts
from ..services.qdrant_service import search
from ..services.rag_pipeline import generate_answer
from ..config import settings
import json

router = APIRouter(prefix="/v1/chat", tags=["chat"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/query")
def query(payload: QueryRequest, db: Session = Depends(get_db)):
    thread_id = payload.thread_id
    if not thread_id:
        # create implicit thread
        from ..repositories import create_thread
        t = create_thread(db, title="Auto Thread", user_id="anonymous")
        thread_id = t.id

    add_message(db, thread_id, "user", payload.question)

    # retrieve
    qvec = embed_texts([payload.question])[0]
    results = search(qvec, top_k=payload.top_k)
    context = [r.payload.get("content", "") for r in results]
    answer_text = generate_answer(payload.question, context)

    a = create_answer(db, thread_id, payload.question, answer_text)

    for r in results:
        add_citation(db, a.id, r.payload.get("document_id",""), r.id if isinstance(r.id,str) else str(r.id), float(r.score))

    add_message(db, thread_id, "assistant", answer_text)
    sources = [{"chunk_id": str(r.id), "score": float(r.score)} for r in results]
    return {"thread_id": thread_id, "answer_id": a.id, "answer": answer_text, "sources": sources}
