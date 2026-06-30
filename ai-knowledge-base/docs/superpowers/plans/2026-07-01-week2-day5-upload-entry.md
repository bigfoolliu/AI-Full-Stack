# Week 2 Day 5 Upload Entry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Introduce the first upload workflow surface by adding mock document endpoints in the backend and turning the upload placeholder page into a real upload-entry page with file selection, submit action, and clear status messaging.

**Architecture:** Keep upload behavior lightweight and local. Extend the existing `knowledge_bases.py` route module with mock document list/create endpoints using an in-memory data structure. On the frontend, keep `KnowledgeBaseUploadView.vue` UI-focused for now: allow file selection and show a simple local success/error message without attempting real file persistence or full upload integration yet.

**Tech Stack:** FastAPI, Pydantic, Vue 3

---

### Task 1: Add mock document endpoints to the backend

**Files:**
- Modify: `ai-knowledge-base/backend/app/api/routes/knowledge_bases.py`

- [ ] **Step 1: Add a mock document store**

Expected:
- mock documents grouped by knowledge-base id

- [ ] **Step 2: Add `GET /api/knowledge-bases/{id}/documents`**

Expected:
- existing knowledge base returns mock document list
- missing knowledge base returns a failure response

- [ ] **Step 3: Add `POST /api/knowledge-bases/{id}/documents`**

Expected:
- accepts minimal mock upload payload
- appends a new mock document record
- returns unified response format

### Task 2: Turn the upload placeholder into a real upload-entry page

**Files:**
- Modify: `ai-knowledge-base/frontend/src/views/KnowledgeBaseUploadView.vue`
- Modify: `ai-knowledge-base/frontend/src/style.css`

- [ ] **Step 1: Add route-aware upload page structure**

Expected:
- title
- description
- current knowledge-base id
- back button

- [ ] **Step 2: Add file selection UI**

Expected:
- file input
- selected file name display
- upload button

- [ ] **Step 3: Add minimal local submission feedback**

Expected:
- no file selected -> error
- file selected -> success message
- no real upload integration yet

### Task 3: Verify the Day 5 upload entry

**Files:**
- Verify: `ai-knowledge-base/backend/app/api/routes/knowledge_bases.py`
- Verify: `ai-knowledge-base/frontend/src/views/KnowledgeBaseUploadView.vue`

- [ ] **Step 1: Verify backend document endpoints**

Check:
- `GET /api/knowledge-bases/{id}/documents`
- `POST /api/knowledge-bases/{id}/documents`

- [ ] **Step 2: Run frontend build**

Run:

```bash
pnpm build
```

Expected:
- build succeeds

- [ ] **Step 3: Confirm Day 5 scope**

Expected:
- upload page now exists as a meaningful business entry
- backend now has upload-related mock endpoints
- Week 2 Day 6 can build on top of this instead of starting from scratch
