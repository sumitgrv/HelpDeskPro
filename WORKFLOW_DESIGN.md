# Workflow Design

## Document Ingestion — State Machine

States: `UPLOADED -> QUEUED_EMBEDDING -> CHUNKED -> EMBEDDED -> INDEXED -> READY | FAILED`

Transitions:
1. `UPLOADED` (metadata saved) → enqueue **EmbeddingJob** → `QUEUED_EMBEDDING`
2. Worker loads file → chunk → `CHUNKED`
3. Generate embeddings → `EMBEDDED`
4. Upsert vectors to Qdrant → `INDEXED`
5. On success mark document `READY`, else `FAILED`

## Database Schema (simplified)

- **documents**(id, filename, owner_id, mime_type, size, status, created_at, updated_at)
- **chunks**(id, document_id, chunk_index, content, embedding (nullable))
- **threads**(id, title, user_id, created_at, updated_at)
- **messages**(id, thread_id, role ['user','assistant','system'], content, created_at)
- **answers**(id, thread_id, question, answer, created_at)
- **citations**(id, answer_id, document_id, chunk_id, score)
- **feedback**(id, answer_id, rating ['HELPFUL','NOT_HELPFUL'], notes, created_at)

See models in `app/models.py`.

## API Overview

- `POST /v1/documents` — upload
- `GET /v1/documents` — list
- `GET /v1/documents/{doc_id}` — get
- `POST /v1/chat/query` — ask a question (optional `thread_id`)
- `POST /v1/threads` — new thread
- `GET /v1/threads/{thread_id}` — thread details with messages
- `POST /v1/feedback` — submit feedback
- `POST /fallback/search` — mock enterprise search (internal)

## Background Jobs

- `EmbeddingJob(document_id)` — chunk → embed → index in Qdrant
- `EscalationJob(answer_id)` — simulate expert escalation HTTP call

Error handling: retries with exponential backoff (RQ), status flags on documents.
