import uuid
from sqlalchemy.orm import Session
from . import models

def new_id() -> str:
    return str(uuid.uuid4())

def create_document(db: Session, filename: str, owner_id: str, mime_type: str, size: int, status: str):
    doc = models.Document(id=new_id(), filename=filename, owner_id=owner_id, mime_type=mime_type, size=size, status=status)
    db.add(doc); db.commit(); db.refresh(doc)
    return doc

def update_document_status(db: Session, doc_id: str, status: str):
    doc = db.get(models.Document, doc_id)
    if doc:
        doc.status = status
        db.commit()
    return doc

def create_thread(db: Session, title: str, user_id: str):
    t = models.Thread(id=new_id(), title=title, user_id=user_id)
    db.add(t); db.commit(); db.refresh(t)
    return t

def add_message(db: Session, thread_id: str, role: str, content: str):
    m = models.Message(id=new_id(), thread_id=thread_id, role=role, content=content)
    db.add(m); db.commit(); db.refresh(m)
    return m

def create_answer(db: Session, thread_id: str, question: str, answer: str):
    a = models.Answer(id=new_id(), thread_id=thread_id, question=question, answer=answer)
    db.add(a); db.commit(); db.refresh(a)
    return a

def add_citation(db: Session, answer_id: str, document_id: str, chunk_id: str, score: float):
    c = models.Citation(id=new_id(), answer_id=answer_id, document_id=document_id, chunk_id=chunk_id, score=score)
    db.add(c); db.commit(); db.refresh(c)
    return c

def add_feedback(db: Session, answer_id: str, rating: str, notes: str | None):
    f = models.Feedback(id=new_id(), answer_id=answer_id, rating=rating, notes=notes)
    db.add(f); db.commit(); db.refresh(f)
    return f
