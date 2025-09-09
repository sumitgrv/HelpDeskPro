from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..schemas import FeedbackCreate
from ..repositories import add_feedback
from ..workers.queue import queue
from ..workers.jobs import escalation_job

router = APIRouter(prefix="/v1/feedback", tags=["feedback"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("")
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    fb = add_feedback(db, payload.answer_id, payload.rating, payload.notes)
    if payload.rating == "NOT_HELPFUL":
        queue.enqueue(escalation_job, payload.answer_id, "unknown-question", payload.notes)
    return {"id": fb.id, "status": "recorded"}
