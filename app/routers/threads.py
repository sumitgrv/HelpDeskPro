from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..repositories import create_thread
from ..schemas import ThreadCreate

router = APIRouter(prefix="/v1/threads", tags=["threads"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("")
def create_thread_ep(payload: ThreadCreate, db: Session = Depends(get_db)):
    t = create_thread(db, payload.title or "New Thread", payload.user_id or "anonymous")
    return {"id": t.id, "title": t.title}
