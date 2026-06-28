# Day 3 Auth Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the Day 3 front-end auth baseline using a Pinia user store, local fake token persistence, route guards, login redirect, and logout flow.

**Architecture:** Keep auth state centralized in a small Pinia store backed by `localStorage`. The router will protect dashboard routes through route meta and a global guard, the login page will call `store.login()` and redirect, and the app shell will read user state to display the current user and expose a logout action.

**Tech Stack:** Vue 3, Pinia, Vue Router, localStorage

---

### Task 1: Create the user auth store

**Files:**
- Create: `ai-knowledge-base/frontend/src/stores/user.ts`

- [ ] **Step 1: Create a minimal Pinia user store**

The store should manage:
- token
- username
- computed login state
- restore/login/logout methods

- [ ] **Step 2: Persist auth state locally**

Use `localStorage` so refreshes can restore the fake login state.

### Task 2: Protect routes and wire store restore

**Files:**
- Modify: `ai-knowledge-base/frontend/src/router/index.ts`
- Modify: `ai-knowledge-base/frontend/src/main.ts`

- [ ] **Step 1: Mark protected routes**

Add route meta to:
- `/dashboard`
- `/knowledge-bases`

- [ ] **Step 2: Add a global beforeEach guard**

Expected:
- unauthenticated protected access redirects to `/login`
- authenticated access to `/login` redirects to `/dashboard`

- [ ] **Step 3: Restore auth state before the app runs**

Expected: refreshed sessions can continue using the locally stored fake token.

### Task 3: Wire login and logout behavior into UI

**Files:**
- Modify: `ai-knowledge-base/frontend/src/views/LoginView.vue`
- Modify: `ai-knowledge-base/frontend/src/App.vue`
- Modify: `ai-knowledge-base/frontend/src/style.css`

- [ ] **Step 1: Make the login form submit into the store**

Expected:
- username is required for the fake login
- successful submit writes fake auth state
- page redirects to `/dashboard`

- [ ] **Step 2: Make the topbar show real store-backed user info**

Expected:
- username comes from store
- top-right control exposes logout

- [ ] **Step 3: Add any small supporting styles**

Expected:
- logout affordance is clear
- topbar remains visually stable

### Task 4: Verify the auth flow

**Files:**
- Verify: `ai-knowledge-base/frontend/src/stores/user.ts`
- Verify: `ai-knowledge-base/frontend/src/router/index.ts`
- Verify: `ai-knowledge-base/frontend/src/views/LoginView.vue`
- Verify: `ai-knowledge-base/frontend/src/App.vue`

- [ ] **Step 1: Run the build**

Run:

```bash
pnpm build
```

Expected: build succeeds.

- [ ] **Step 2: Confirm the Day 3 flow**

Expected:
- protected routes redirect when logged out
- login enters dashboard
- username appears in topbar
- logout returns to login
