# Shell User Login Entry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the shell's top-right user block act as a login entry that routes to `/login`.

**Architecture:** Keep the existing admin shell intact. Replace the passive user container in `App.vue` with a `RouterLink` and add small interactive styles in `style.css` so the control reads as clickable without changing the overall layout.

**Tech Stack:** Vue 3, Vue Router, global CSS

---

### Task 1: Convert the shell user block into a route link

**Files:**
- Modify: `ai-knowledge-base/frontend/src/App.vue`

- [ ] **Step 1: Replace the passive user container**

Change the top-right user block from a `div` to a `RouterLink` targeting `/login`, keeping the same child content structure.

- [ ] **Step 2: Keep the existing layout intact**

Expected: the avatar, name, and subtitle still render in the topbar, but the entire block is now clickable.

### Task 2: Add small interaction styles

**Files:**
- Modify: `ai-knowledge-base/frontend/src/style.css`

- [ ] **Step 1: Preserve the existing shell-user layout styles**

Expected: the link still looks like the current user block by default.

- [ ] **Step 2: Add click affordance**

Add:
- `border-radius`
- `padding`
- hover background
- focus-visible outline

### Task 3: Verify the change

**Files:**
- Verify: `ai-knowledge-base/frontend/src/App.vue`
- Verify: `ai-knowledge-base/frontend/src/style.css`

- [ ] **Step 1: Run the build**

Run:

```bash
pnpm build
```

Expected: build succeeds.

- [ ] **Step 2: Confirm intended behavior**

Expected:
- Shell user block is visually clickable
- Route target is `/login`
- Existing shell layout still looks correct
