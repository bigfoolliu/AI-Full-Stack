# Current Roadmap

## Current Priorities

1. Stabilize the RAG flow (Week 7):
   - supplement backend test coverage (unit + integration)
   - improve frontend error boundaries and exception handling
   - check frontend/backend type consistency
2. Iterate session features:
   - session delete / rename
   - link sessions to users
   - basic knowledge-base permission model
3. Performance:
   - async document processing (Celery / background tasks)
   - streaming response latency improvements
   - search response time optimization

## Completed

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
