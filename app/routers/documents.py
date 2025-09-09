import os
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..repositories import create_document, update_document_status
from ..workers.queue import queue
from ..workers.jobs import embedding_job
from ..models import DocStatus

router = APIRouter(prefix="/v1/documents", tags=["documents"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("")
def upload_document(file: UploadFile = File(...), owner_id: str = Form("anonymous"), db: Session = Depends(get_db)):
    if not file.filename:
        raise HTTPException(400, "No file")
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(file.file.read())
    doc = create_document(db, filename=file.filename, owner_id=owner_id, mime_type=file.content_type or "", size=os.path.getsize(filepath), status=DocStatus.UPLOADED)
    update_document_status(db, doc.id, DocStatus.QUEUED_EMBEDDING)
    queue.enqueue(embedding_job, doc.id, filepath)
    return {"id": doc.id, "status": DocStatus.QUEUED_EMBEDDING, "filename": doc.filename}
