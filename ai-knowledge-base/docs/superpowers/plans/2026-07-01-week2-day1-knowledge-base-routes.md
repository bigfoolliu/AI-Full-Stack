# Week 2 Day 1 Knowledge Base Routes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the first three Week 2 knowledge-base workflow routes and placeholder pages, and wire navigation from the knowledge-bases list so the business page flow becomes visible.

**Architecture:** Keep the scope intentionally tiny. Extend the existing router with three new routes, add three focused placeholder views, and add navigation entry points from the current knowledge-bases list page. Do not implement forms, uploads, or real document logic yet.

**Tech Stack:** Vue 3, Vue Router

---

### Task 1: Add the new Week 2 routes

**Files:**
- Modify: `ai-knowledge-base/frontend/src/router/index.ts`

- [ ] **Step 1: Import the new placeholder views**

Expected imports:
- `KnowledgeBaseCreateView`
- `KnowledgeBaseDocumentsView`
- `KnowledgeBaseUploadView`

- [ ] **Step 2: Register the three new routes**

Expected routes:
- `/knowledge-bases/create`
- `/knowledge-bases/:id/documents`
- `/knowledge-bases/:id/upload`

### Task 2: Create the three placeholder view files

**Files:**
- Create: `ai-knowledge-base/frontend/src/views/KnowledgeBaseCreateView.vue`
- Create: `ai-knowledge-base/frontend/src/views/KnowledgeBaseDocumentsView.vue`
- Create: `ai-knowledge-base/frontend/src/views/KnowledgeBaseUploadView.vue`

- [ ] **Step 1: Create the create-page placeholder**

Expected:
- page title
- short description

- [ ] **Step 2: Create the documents-page placeholder**

Expected:
- page title
- route param `id` visible in context
- short description

- [ ] **Step 3: Create the upload-page placeholder**

Expected:
- page title
- route param `id` visible in context
- short description

### Task 3: Add navigation entry points from the knowledge-bases page

**Files:**
- Modify: `ai-knowledge-base/frontend/src/views/KnowledgebasesView.vue`

- [ ] **Step 1: Wire the create button to the create page**

Expected:
- `新建知识库` navigates to `/knowledge-bases/create`

- [ ] **Step 2: Replace or extend row actions**

Expected:
- one action enters `/knowledge-bases/:id/documents`
- one action enters `/knowledge-bases/:id/upload`

### Task 4: Verify the Day 1 route skeleton

**Files:**
- Verify: `ai-knowledge-base/frontend/src/router/index.ts`
- Verify: `ai-knowledge-base/frontend/src/views/KnowledgebasesView.vue`
- Verify: new placeholder views

- [ ] **Step 1: Run frontend build**

Run:

```bash
pnpm build
```

Expected:
- build succeeds

- [ ] **Step 2: Confirm route skeleton behavior**

Expected:
- can navigate from the list page to create page
- can navigate from the list page to documents page
- can navigate from the list page to upload page
