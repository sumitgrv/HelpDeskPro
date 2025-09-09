from pydantic import BaseModel
from typing import Optional, List

class ThreadCreate(BaseModel):
    title: Optional[str] = None
    user_id: Optional[str] = None

class QueryRequest(BaseModel):
    question: str
    thread_id: Optional[str] = None
    top_k: int = 5

class FeedbackCreate(BaseModel):
    answer_id: str
    rating: str
    notes: Optional[str] = None
