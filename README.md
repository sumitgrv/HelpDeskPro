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

### Prerequisites
- Docker and Docker Compose installed
- Git (to clone the repository)

### Steps

1. **Clone the repository** (if not already cloned)
   ```bash
   git clone <repository-url>
   cd HelpDeskPro
   ```

2. **Create environment file**
   ```bash
   # On Linux/Mac:
   cp .env.example .env
   
   # On Windows (PowerShell):
   Copy-Item .env.example .env
   ```
   Edit `.env` file to adjust secrets, URLs, model names, etc. (defaults work for Docker setup)

3. **Start all services**
   ```bash
   docker compose up --build
   ```
   This will build and start all services. The first build may take 10-15 minutes due to PyTorch installation.

4. **Access the services**
   - **API**: http://localhost:8200 (API docs at http://localhost:8200/docs)
   - **UI**: http://localhost:8501
   - **Qdrant Dashboard**: http://localhost:6333 (web UI)
   - **Redis**: localhost:6379
   - **PostgreSQL**: localhost:5432 (user: postgres, password: postgres, db: helpdeskpro)

### Running in Background
```bash
docker compose up --build -d
```

### View Logs
```bash
docker compose logs -f
```

### Stop Services
```bash
docker compose down
```

## Development (without Docker)

### Prerequisites
- Python 3.11+
- PostgreSQL 16+ (or use SQLite for testing)
- Redis 7+
- Qdrant (can run via Docker: `docker run -p 6333:6333 qdrant/qdrant`)

### Setup

1. **Create virtual environment**
   ```bash
   # On Linux/Mac:
   python -m venv .venv
   source .venv/bin/activate
   
   # On Windows (PowerShell):
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install CPU-only PyTorch first** (to avoid CUDA dependencies)
   ```bash
   pip install torch --index-url https://download.pytorch.org/whl/cpu
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** with local development settings:
   ```bash
   # Copy the example file
   # On Linux/Mac:
   cp .env.example .env
   
   # On Windows:
   Copy-Item .env.example .env
   ```
   Then edit `.env` to use localhost URLs:
   ```bash
   DATABASE_URL=sqlite:///./helpdeskpro.db  # or postgresql://postgres:postgres@localhost:5432/helpdeskpro
   REDIS_URL=redis://localhost:6379/0
   QDRANT_URL=http://localhost:6333
   API_URL=http://localhost:8200
   ```

5. **Start required services** (if not using Docker)
   - PostgreSQL: Run locally or use SQLite
   - Redis: `redis-server` or `docker run -p 6379:6379 redis:7`
   - Qdrant: `docker run -p 6333:6333 qdrant/qdrant`

### Running Services

**Terminal 1 - API Server:**
```bash
uvicorn app.main:app --reload --port 8200
```

**Terminal 2 - Worker (for background jobs):**
```bash
rq worker -u redis://localhost:6379/0 helpdeskpro
```

**Terminal 3 - UI:**
```bash
streamlit run ui/streamlit_app.py
```

Access:
- API: http://localhost:8200/docs
- UI: http://localhost:8501

## Features

- Upload PDFs/DOCX/Markdown → chunk + embed in background → store in **Qdrant** with metadata in **Postgres**.
- **RAG Q&A** with conversation threads and source citations.
- **Feedback** (HELPFUL / NOT_HELPFUL) stored and triggers **escalation job** on NOT_HELPFUL.
- **Fallback Search**: mock enterprise search API when retrieval is empty/low score.
- **Evaluation**: example `eval/evaluate_rag.py` with `ragas` to score retrieval quality.
- **Tests**: `pytest` + a few example unit tests.

See `PROJECT_STRUCTURE.md`, `WORKFLOW_DESIGN.md`, and `API-SPECIFICATION.yml` for detailed design.
