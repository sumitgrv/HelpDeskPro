from fastapi import FastAPI
from .db import init_db
from .routers import health, documents, chat, threads, feedback, search_fallback

def create_app():
    app = FastAPI(title="HelpDeskPro RAG API", version="1.0.0")
    init_db()
    app.include_router(health.router)
    app.include_router(documents.router)
    app.include_router(chat.router)
    app.include_router(threads.router)
    app.include_router(feedback.router)
    app.include_router(search_fallback.router)
    return app

app = create_app()
