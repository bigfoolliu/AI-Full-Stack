# Week 2 Day 4 Knowledge Base CRUD Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the backend knowledge-bases route into a minimal CRUD foundation by adding create and detail endpoints on top of the existing in-memory mock list.

**Architecture:** Keep the implementation intentionally lightweight. Reuse the current `knowledge_bases.py` route module and `knowledge_base.py` schema module, add one request schema for creation, and continue storing knowledge-base records in a simple in-memory list for Week 2 purposes.

**Tech Stack:** FastAPI, Pydantic

---

### Task 1: Extend the knowledge-base schema

**Files:**
- Modify: `ai-knowledge-base/backend/app/schemas/knowledge_base.py`

- [ ] **Step 1: Keep the existing list item schema**

Expected:
- `KnowledgeBaseItem` remains the response shape used by list/detail endpoints

- [ ] **Step 2: Add the create request schema**

Expected fields:
- `name`
- `description`

### Task 2: Extend the route module with create and detail endpoints

**Files:**
- Modify: `ai-knowledge-base/backend/app/api/routes/knowledge_bases.py`

- [ ] **Step 1: Preserve the current list endpoint**

Expected:
- `GET /api/knowledge-bases` still returns the existing mock list

- [ ] **Step 2: Add `POST /api/knowledge-bases`**

Expected behavior:
- accept `name` and `description`
- create a new item in the in-memory list
- return the created item inside the unified response structure

- [ ] **Step 3: Add `GET /api/knowledge-bases/{id}`**

Expected behavior:
- return a single knowledge-base item when found
- return a failure response when the id does not exist

### Task 3: Verify the minimal CRUD behavior

**Files:**
- Verify: `ai-knowledge-base/backend/app/api/routes/knowledge_bases.py`
- Verify: `ai-knowledge-base/backend/app/schemas/knowledge_base.py`

- [ ] **Step 1: Start or reuse the local backend**

Expected:
- backend serves the updated knowledge-bases routes

- [ ] **Step 2: Verify list, create, and detail**

Check:
- `GET /api/knowledge-bases`
- `POST /api/knowledge-bases`
- `GET /api/knowledge-bases/{id}`

Expected:
- all endpoints return the unified response format

- [ ] **Step 3: Verify missing-id behavior**

Expected:
- non-existent knowledge-base id returns a clear failure response
