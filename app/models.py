from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Enum, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import enum
from .db import Base

class DocStatus(str, enum.Enum):
    UPLOADED = "UPLOADED"
    QUEUED_EMBEDDING = "QUEUED_EMBEDDING"
    CHUNKED = "CHUNKED"
    EMBEDDED = "EMBEDDED"
    INDEXED = "INDEXED"
    READY = "READY"
    FAILED = "FAILED"

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[str] = mapped_column(String, nullable=True)
    mime_type: Mapped[str] = mapped_column(String, nullable=True)
    size: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String, default=DocStatus.UPLOADED)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    document_id: Mapped[str] = mapped_column(String, ForeignKey("documents.id"))
    chunk_index: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[str] = mapped_column(Text, nullable=True)  # store as JSON string for debugging
    document = relationship("Document", back_populates="chunks")

class Thread(Base):
    __tablename__ = "threads"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    thread_id: Mapped[str] = mapped_column(String, ForeignKey("threads.id"))
    role: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Answer(Base):
    __tablename__ = "answers"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    thread_id: Mapped[str] = mapped_column(String, ForeignKey("threads.id"))
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Citation(Base):
    __tablename__ = "citations"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    answer_id: Mapped[str] = mapped_column(String, ForeignKey("answers.id"))
    document_id: Mapped[str] = mapped_column(String, ForeignKey("documents.id"))
    chunk_id: Mapped[str | None] = mapped_column(String, ForeignKey("chunks.id"), nullable=True)  # Nullable since chunks may not be in DB
    score: Mapped[float] = mapped_column(Float, default=0.0)

class FeedbackRating(str, enum.Enum):
    HELPFUL = "HELPFUL"
    NOT_HELPFUL = "NOT_HELPFUL"

class Feedback(Base):
    __tablename__ = "feedback"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    answer_id: Mapped[str] = mapped_column(String, ForeignKey("answers.id"))
    rating: Mapped[str] = mapped_column(String)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
