# Current Roadmap

## Current Priorities

1. Chunk strategy configuration (Week 8):
   - add chunk_size / overlap / chunk_strategy to KnowledgeBaseSetting
   - settings page UI for chunk params
   - process_service reads chunk params from settings
2. Session management enhancement:
   - session delete and rename
   - link sessions to users (user_id in chat_sessions)
   - basic knowledge-base permission model
3. UX polish:
   - knowledge base copy / move
   - markdown rendering improvements (code highlighting)
   - typing animation optimization for streaming output
4. Engineering:
   - async document processing (FastAPI BackgroundTasks)
   - global error boundary components
   - search response caching

## Completed

- Week 7: RAG system tuning — configurable retrieval/prompt/model params, Hybrid Search, Metadata Filter, Rerank, Feedback, A/B comparison, metrics
- Week 6: LLM integration, RAG Q&A, SSE streaming, Chat dialog, session history
- Week 5: Document processing pipeline, chunking, vector search (Qdrant), FTS5
- Week 4: Database migration, JWT auth, document parsing, FTS5 full-text search
- Week 3: Element Plus adoption, search + pagination, real file upload
- Week 2: Knowledge base CRUD, document list + upload pages
- Week 1: Login, dashboard, backend skeleton

## Out of Scope For The Next Iteration

- new product pages unrelated to chat and session history
- deployment, CI/CD, and cloud infrastructure expansion
- multi-provider agent tooling or advanced orchestration

## Default Verification

- frontend changes: `make frontend-build`
- backend changes: `make backend-test`
- changes spanning both: `make check`

## Working Rules

- Default code edit scope is this app directory, not the week-plan markdown files in the repo root.
- Keep route, schema, and service responsibilities separated.
- Update this roadmap when priorities or acceptance criteria change materially.
