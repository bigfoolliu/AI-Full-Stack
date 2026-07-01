# Week 2 Day 6 Real Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the create-page mock submit and documents-page local mock list with real backend integration against the Week 2 knowledge-base endpoints.

**Architecture:** Extend the frontend knowledge-base API helper with create and documents-fetch functions, then refactor `KnowledgeBaseCreateView.vue` and `KnowledgeBaseDocumentsView.vue` into API-driven pages. Keep the scope tight: only create and documents list flows become real; upload-page integration stays out of scope for this day.

**Tech Stack:** Vue 3, Axios, existing backend mock endpoints

---

### Task 1: Extend the frontend knowledge-base API helper

**Files:**
- Modify: `ai-knowledge-base/frontend/src/api/knowledge-bases.ts`

- [ ] **Step 1: Add create request types**

Expected:
- a request payload type for creating knowledge bases

- [ ] **Step 2: Add create and documents API helpers**

Expected helpers:
- `createKnowledgeBase(payload)`
- `getKnowledgeBaseDocuments(id)`

### Task 2: Refactor the create page to real submit behavior

**Files:**
- Modify: `ai-knowledge-base/frontend/src/views/KnowledgeBaseCreateView.vue`

- [ ] **Step 1: Replace mock submit with API-driven create**

Expected:
- submit calls backend create endpoint

- [ ] **Step 2: Add loading / success / error handling**

Expected:
- button reflects loading
- success message becomes API-backed
- failure shows readable error

- [ ] **Step 3: Keep minimal validation**

Expected:
- name remains required before request fires

### Task 3: Refactor the documents page to real list loading

**Files:**
- Modify: `ai-knowledge-base/frontend/src/views/KnowledgeBaseDocumentsView.vue`
- Modify: `ai-knowledge-base/frontend/src/style.css`

- [ ] **Step 1: Replace the local documents array**

Expected:
- documents data comes from backend

- [ ] **Step 2: Add loading / empty / error states**

Expected:
- page no longer depends on hardcoded list rows

- [ ] **Step 3: Preserve upload navigation**

Expected:
- documents page still routes to the upload page

### Task 4: Verify the Day 6 integration

**Files:**
- Verify: `ai-knowledge-base/frontend/src/api/knowledge-bases.ts`
- Verify: `ai-knowledge-base/frontend/src/views/KnowledgeBaseCreateView.vue`
- Verify: `ai-knowledge-base/frontend/src/views/KnowledgeBaseDocumentsView.vue`

- [ ] **Step 1: Run frontend build**

Run:

```bash
pnpm build
```

Expected:
- build succeeds

- [ ] **Step 2: Verify backend endpoints are usable**

Check:
- `POST /api/knowledge-bases`
- `GET /api/knowledge-bases/{id}/documents`

- [ ] **Step 3: Confirm Day 6 scope**

Expected:
- create page uses real backend create
- documents page uses real backend list
- loading / error / empty states exist
