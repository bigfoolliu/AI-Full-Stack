# Day 6 Knowledge Bases Business Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the knowledge-bases page into the first real business page by adding a backend list endpoint, fetching it from the frontend, and rendering list/loading/empty states.

**Architecture:** Add one lightweight mock list endpoint in the backend, then introduce a focused frontend API helper and refactor `KnowledgebasesView.vue` from static local data to API-driven state. Keep the UI structure already built on Day 2, but align the table to the backend contract and add loading / empty handling.

**Tech Stack:** FastAPI, Pydantic, Vue 3, Axios

---

### Task 1: Add the backend knowledge-bases schema and route

**Files:**
- Create: `ai-knowledge-base/backend/app/schemas/knowledge_base.py`
- Create: `ai-knowledge-base/backend/app/api/routes/knowledge_bases.py`
- Modify: `ai-knowledge-base/backend/app/main.py`

- [ ] **Step 1: Create the knowledge-base schema**

Expected model fields:
- `id`
- `name`
- `description`
- `document_count`
- `created_at`

- [ ] **Step 2: Implement `GET /api/knowledge-bases`**

Expected behavior:
- route lives under `/api`
- returns a mock list using the unified response format
- no database dependency introduced

- [ ] **Step 3: Register the new router**

Expected:
- `app.main` includes the knowledge-bases router alongside health and auth

### Task 2: Add the frontend knowledge-bases API layer

**Files:**
- Create: `ai-knowledge-base/frontend/src/api/knowledge-bases.ts`

- [ ] **Step 1: Create the list response types**

Expected types:
- single knowledge-base item
- list response structure

- [ ] **Step 2: Create `getKnowledgeBases()`**

Expected:
- uses existing shared axios instance
- calls `/api/knowledge-bases`

### Task 3: Refactor `KnowledgebasesView.vue` to API-driven rendering

**Files:**
- Modify: `ai-knowledge-base/frontend/src/views/KnowledgebasesView.vue`

- [ ] **Step 1: Remove the static local placeholder list**

Expected:
- no hardcoded knowledge-base table rows remain as the main data source

- [ ] **Step 2: Add state for `list`, `loading`, and `error`**

Expected:
- page can represent request lifecycle clearly

- [ ] **Step 3: Fetch data on mount**

Expected:
- call `getKnowledgeBases()`
- populate the table from backend data

- [ ] **Step 4: Align table columns to Day 6 contract**

Expected columns:
- 名称
- 描述
- 文档数量
- 创建时间
- 操作

- [ ] **Step 5: Add empty state rendering**

Expected:
- if backend returns an empty list, show a clear empty state instead of a blank table

### Task 4: Add the minimal Day 6 page states and styles

**Files:**
- Modify: `ai-knowledge-base/frontend/src/style.css`

- [ ] **Step 1: Preserve the current page shell**

Expected:
- title, toolbar, and list card remain visually consistent with existing admin pages

- [ ] **Step 2: Add loading and empty state styles**

Expected:
- loading state is clearly readable
- empty state looks intentional, not like missing markup

- [ ] **Step 3: Update any table cell styles needed for the new data shape**

Expected:
- description column reads cleanly
- document count and created time align well

### Task 5: Verify the Day 6 integration

**Files:**
- Verify: `ai-knowledge-base/backend/app/api/routes/knowledge_bases.py`
- Verify: `ai-knowledge-base/frontend/src/api/knowledge-bases.ts`
- Verify: `ai-knowledge-base/frontend/src/views/KnowledgebasesView.vue`

- [ ] **Step 1: Run backend verification**

Check:
- `GET /api/knowledge-bases`

Expected:
- returns mock list data in unified response format

- [ ] **Step 2: Run frontend build**

Run:

```bash
pnpm build
```

Expected:
- build succeeds after the page refactor

- [ ] **Step 3: Verify the rendered page**

Expected:
- page shows list data when backend returns rows
- page shows empty state when list is empty
- page keeps the Day 2 business-page layout intact
