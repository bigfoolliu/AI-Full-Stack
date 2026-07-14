# Current Roadmap

## Current Priorities

1. Complete Week 6 Day 6 session persistence:
   - add `chat_sessions` and `chat_messages`
   - expose session list/create-update APIs
   - restore the active chat after refresh
2. Stabilize the RAG flow:
   - verify upload -> process -> search -> chat works end to end
   - tighten error handling around missing model or vector dependencies
3. Improve AI development readiness:
   - keep `AGENTS.md`, `Makefile`, and this roadmap aligned
   - prefer repeatable verification commands over ad hoc local steps

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
