import os, json
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..repositories import update_document_status
from ..services.rag_pipeline import index_document
from ..utils.logging import logger
import requests

def embedding_job(document_id: str, file_path: str):
    logger.info(f"[EmbeddingJob] {document_id} -> {file_path}")
    db: Session = SessionLocal()
    try:
        update_document_status(db, document_id, "CHUNKED")
        chunks, points = index_document(document_id, file_path)
        update_document_status(db, document_id, "READY")
        logger.info(f"[EmbeddingJob] Indexed {chunks} chunks as {points} points")
    except Exception as e:
        update_document_status(db, document_id, "FAILED")
        logger.exception("Embedding job failed")
        raise e
    finally:
        db.close()

def escalation_job(answer_id: str, question: str, notes: str | None):
    # mock call to external expert system
    payload = {"answer_id": answer_id, "question": question, "notes": notes}
    logger.info(f"[EscalationJob] POST to expert system: {payload}")
    # In real life: requests.post("https://expert-svc/api/escalate", json=payload, timeout=10)
    return {"status": "queued", "payload": payload}
