# Day 4 Backend Mock Auth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the backend into a minimal FastAPI app package and add mock `login` / `me` endpoints, unified responses, and local CORS support for the frontend.

**Architecture:** Move the current single-file backend into a lightweight `app/` package with separated route modules, shared Pydantic response schemas, and a small config module. Keep auth fully mocked: a fixed username/password pair returns a fixed token and a fixed user, while `GET /api/me` returns mock user data without real token parsing.

**Tech Stack:** FastAPI, Pydantic, Uvicorn, CORSMiddleware

---

### Task 1: Create the minimal backend package structure

**Files:**
- Create: `ai-knowledge-base/backend/app/main.py`
- Create: `ai-knowledge-base/backend/app/api/routes/health.py`
- Create: `ai-knowledge-base/backend/app/api/routes/auth.py`
- Create: `ai-knowledge-base/backend/app/schemas/common.py`
- Create: `ai-knowledge-base/backend/app/schemas/auth.py`
- Create: `ai-knowledge-base/backend/app/core/config.py`
- Modify: `ai-knowledge-base/backend/main.py`

- [ ] **Step 1: Create the package directories**

Create:

```text
backend/app/
backend/app/api/routes/
backend/app/schemas/
backend/app/core/
```

- [ ] **Step 2: Leave a compatibility entry in the root `main.py`**

Expected: existing local run habits can still forward to the new `app.main:app` location instead of hard-breaking.

### Task 2: Define shared schemas and config

**Files:**
- Create: `ai-knowledge-base/backend/app/schemas/common.py`
- Create: `ai-knowledge-base/backend/app/schemas/auth.py`
- Create: `ai-knowledge-base/backend/app/core/config.py`

- [ ] **Step 1: Create the unified response schema**

Expected model shape:
- `code`
- `message`
- `data`

- [ ] **Step 2: Create auth request/response schemas**

Expected models:
- `LoginRequest`
- `UserInfo`
- `LoginResponseData`

- [ ] **Step 3: Create the minimal config module**

Expected config values:
- app name
- allowed origins list
- mock username/password/token

### Task 3: Implement health and auth routes

**Files:**
- Create: `ai-knowledge-base/backend/app/api/routes/health.py`
- Create: `ai-knowledge-base/backend/app/api/routes/auth.py`

- [ ] **Step 1: Implement `GET /health` with unified response**

Expected response:

```json
{
  "code": 0,
  "message": "ok",
  "data": { "status": "ok" }
}
```

- [ ] **Step 2: Implement `POST /api/login`**

Expected behavior:
- accept `username` and `password`
- if mock credentials match, return mock token + mock user
- if they do not match, return a failure response

- [ ] **Step 3: Implement `GET /api/me`**

Expected behavior:
- return a fixed mock user payload
- do not require real token parsing yet

### Task 4: Build the FastAPI app entrypoint and CORS

**Files:**
- Create: `ai-knowledge-base/backend/app/main.py`
- Modify: `ai-knowledge-base/backend/main.py`

- [ ] **Step 1: Create the new FastAPI app entrypoint**

Expected:
- app instance created in `app/main.py`
- health router included
- auth router included

- [ ] **Step 2: Add base CORS middleware**

Expected:
- allow `http://localhost:5173`
- allow standard methods and headers for local frontend work

- [ ] **Step 3: Update the root `main.py` shim**

Expected:
- running `python main.py` still starts the new app

### Task 5: Update backend metadata and docs

**Files:**
- Modify: `ai-knowledge-base/backend/pyproject.toml`
- Modify: `ai-knowledge-base/backend/README.md`

- [ ] **Step 1: Adjust entrypoint or project notes if needed**

Expected: project metadata reflects the new app location if necessary.

- [ ] **Step 2: Add a minimal backend README**

Expected README content:
- what the backend does at Day 4
- how to run it
- available endpoints

### Task 6: Verify the Day 4 backend

**Files:**
- Verify: `ai-knowledge-base/backend/app/main.py`
- Verify: `ai-knowledge-base/backend/app/api/routes/health.py`
- Verify: `ai-knowledge-base/backend/app/api/routes/auth.py`

- [ ] **Step 1: Start the backend locally**

Run one of:

```bash
python main.py
```

or

```bash
uv run uvicorn app.main:app --reload
```

- [ ] **Step 2: Verify the three required endpoints**

Check:
- `GET /health`
- `POST /api/login`
- `GET /api/me`

Expected: all respond with the unified response format.

- [ ] **Step 3: Verify Day 5 readiness**

Expected:
- frontend local origin is allowed by CORS
- login and user-profile endpoints now exist for real front-end integration
