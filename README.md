# HelpDeskPro — Knowledge-Centered Support System (GenAI + RAG)

A production-ready reference implementation of a Retrieval-Augmented Generation (RAG) backend with document ingestion, semantic search, conversation threads, feedback logging, async background jobs, third‑party fallback search, and a simple Streamlit UI for customer support agents.

## Stack

- **Backend**: FastAPI (Python 3.11)
- **DB**: PostgreSQL (SQLAlchemy 2.x, Alembic optional)
- **Vector DB**: Qdrant
- **Background Jobs**: RQ + Redis
- **Embeddings**: sentence-transformers (`all-MiniLM-L6-v2` by default)
- **LLM**: Pluggable (OpenAI via `OPENAI_API_KEY`) or local Hugging Face `text-generation` fallback
- **UI**: Streamlit
- **Evaluation**: ragas (optional script)

## Quick Start

```bash
# 1) clone the repo, then create .env from example
cp .env.example .env
# adjust secrets, URLs, model names, etc.

# 2) start everything
docker compose up --build
```

Services:
- API: http://localhost:8000 (docs at `/docs`)
- UI: http://localhost:8501
- Qdrant: http://localhost:6333 (web UI)
- Redis: localhost:6379
- Postgres: localhost:5432

## Development (without docker)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# worker
rq worker -u ${REDIS_URL:-redis://redis:6379/0} helpdeskpro
# UI
streamlit run ui/streamlit_app.py
```

## Features

- Upload PDFs/DOCX/Markdown → chunk + embed in background → store in **Qdrant** with metadata in **Postgres**.
- **RAG Q&A** with conversation threads and source citations.
- **Feedback** (HELPFUL / NOT_HELPFUL) stored and triggers **escalation job** on NOT_HELPFUL.
- **Fallback Search**: mock enterprise search API when retrieval is empty/low score.
- **Evaluation**: example `eval/evaluate_rag.py` with `ragas` to score retrieval quality.
- **Tests**: `pytest` + a few example unit tests.

See `PROJECT_STRUCTURE.md`, `WORKFLOW_DESIGN.md`, and `API-SPECIFICATION.yml` for detailed design.
