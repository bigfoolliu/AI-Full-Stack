# Repository Guidelines

## Project Structure & Module Organization

This repository mixes training notes with a working app. The main product lives in `ai-knowledge-base/`.

- `ai-knowledge-base/frontend/` — Vue 3 + TypeScript client (`src/views`, `src/api`, `src/router`, `src/stores`)
- `ai-knowledge-base/backend/` — FastAPI service (`app/api/routes`, `app/models`, `app/schemas`, `app/services`, `app/core`)
- `ai-knowledge-base/docs/` — design specs and implementation plans
- `week*.md` and `AI全栈转岗.md` — planning and learning notes, not runtime code

Keep changes scoped to the app unless the task explicitly targets the training documents.

## Build, Test, and Development Commands

- `make frontend-dev` — start the Vite dev server
- `make backend-dev` — run the FastAPI app with reload on port 8000
- `make qdrant-up` — start the local Qdrant dependency
- `make frontend-build` — type-check and build the frontend
- `make backend-test` — run the backend validation scripts
- `make check` — run the default repo verification sequence

## Coding Style & Naming Conventions

Use 2-space indentation in Vue/TypeScript and 4-space indentation in Python. Follow existing file naming:

- Vue views/components: `PascalCase.vue`
- TypeScript API modules: lowercase or kebab-style existing pattern, e.g. `knowledge-bases.ts`
- Python modules: `snake_case.py`

Backend formatting follows Ruff settings in `backend/pyproject.toml` (`line-length = 120`). Frontend formatting uses Prettier already listed in `frontend/package.json`.

## Testing Guidelines

This repo currently relies on targeted backend scripts and frontend build validation rather than a full test suite. For backend changes, add or update a focused script under `ai-knowledge-base/backend/scripts/test_*.py`. For frontend changes, run `npm run build` and verify the affected flow manually.

Name new test scripts by feature, for example `test_search.py` or `test_sessions.py`.

For AI-assisted work, do not claim a change is complete until you have run the relevant verification command:

- frontend-only changes: `make frontend-build`
- backend-only changes: `make backend-lint` and `make backend-test`
- full-stack changes: `make check`

## Commit & Pull Request Guidelines

Recent commits use short, scope-based messages such as `week6 day5`. Keep commit messages brief and specific; `weekN dayN` is acceptable for milestone work, but feature-focused messages are better for isolated fixes.

Pull requests should include:

- a short summary of the change
- affected paths or features
- verification commands you ran
- screenshots for UI changes

## Security & Configuration Tips

Do not commit API keys, local database files, uploaded documents, or build artifacts. Review config usage in `ai-knowledge-base/backend/app/core/config.py` before adding new environment variables, and prefer repo-local examples over hardcoded secrets.

## Agent-Specific Instructions

Default edit scope is `ai-knowledge-base/`. Do not modify `week*.md` or other training notes unless the task explicitly asks for it.

Route changes through the existing layers:

- frontend HTTP calls in `frontend/src/api/`
- page logic in `frontend/src/views/`
- backend routes in `backend/app/api/routes/`
- schemas in `backend/app/schemas/`
- business logic in `backend/app/services/`

Prefer small, local edits over broad refactors. When adding new setup or workflow steps, update this file, the root `Makefile`, or `ai-knowledge-base/docs/current-roadmap.md` so future agents inherit the same instructions.
