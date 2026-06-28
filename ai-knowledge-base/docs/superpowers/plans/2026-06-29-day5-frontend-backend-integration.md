# Day 5 Frontend Backend Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the frontend's fake auth flow with a real login and current-user integration against the Day 4 backend, while adding basic loading and error handling.

**Architecture:** Introduce a small `api/` layer around axios, move auth effects into the Pinia user store, and keep views/components thin. The login page will submit through the store, the store will persist the real backend token and user data, and the app shell will render real user info from `GET /api/me`.

**Tech Stack:** Vue 3, Pinia, Vue Router, Axios

---

### Task 1: Add the API layer

**Files:**
- Create: `ai-knowledge-base/frontend/src/api/http.ts`
- Create: `ai-knowledge-base/frontend/src/api/auth.ts`
- Modify: `ai-knowledge-base/frontend/package.json`

- [ ] **Step 1: Add axios as a frontend dependency**

Expected: `package.json` includes `axios`.

- [ ] **Step 2: Create the shared axios instance**

Expected behavior:
- base URL points to `http://127.0.0.1:8000`
- request interceptor attaches `Authorization` when token exists

- [ ] **Step 3: Create auth API helpers**

Expected helpers:
- `login(payload)`
- `getMe()`

### Task 2: Upgrade the user store from fake auth to real auth

**Files:**
- Modify: `ai-knowledge-base/frontend/src/stores/user.ts`

- [ ] **Step 1: Extend store state**

Expected state:
- `token`
- `username`
- `nickname`
- `isLoggedIn`
- `loginLoading`
- `loginError`

- [ ] **Step 2: Replace fake login with API-driven login**

Expected behavior:
- call `/api/login`
- persist returned token
- save returned `username` and `nickname`
- expose clear error state on failure

- [ ] **Step 3: Add `fetchMe()` and strengthen `restore()`**

Expected behavior:
- `restore()` reloads token from storage
- `fetchMe()` refreshes user identity from backend
- failed `fetchMe()` clears invalid local auth state

- [ ] **Step 4: Keep logout behavior simple**

Expected behavior:
- clear token
- clear user fields
- clear persisted local auth

### Task 3: Connect the login page to the real backend

**Files:**
- Modify: `ai-knowledge-base/frontend/src/views/LoginView.vue`
- Modify: `ai-knowledge-base/frontend/src/style.css`

- [ ] **Step 1: Submit the form through the store**

Expected behavior:
- username and password go to `store.login()`
- success redirects to `/dashboard`

- [ ] **Step 2: Add loading and error feedback**

Expected behavior:
- login button reflects loading state
- login failure shows backend message
- empty username/password still stays in minimal front-end validation scope

- [ ] **Step 3: Fix any small form-quality issues**

Expected:
- password input naming/ids are correct
- login hint text reflects the new real integration state

### Task 4: Show real user info in the app shell

**Files:**
- Modify: `ai-knowledge-base/frontend/src/App.vue`
- Modify: `ai-knowledge-base/frontend/src/style.css`

- [ ] **Step 1: Read real identity from the store**

Expected behavior:
- topbar shows nickname first
- fallback to username

- [ ] **Step 2: Trigger current-user refresh**

Expected behavior:
- when a token exists, the shell or store initialization pulls `/api/me`
- if fetch fails, user is reset to logged-out state

- [ ] **Step 3: Keep logout working**

Expected behavior:
- logout clears state
- user returns to `/login`

### Task 5: Verify the Day 5 integration

**Files:**
- Verify: `ai-knowledge-base/frontend/src/api/http.ts`
- Verify: `ai-knowledge-base/frontend/src/api/auth.ts`
- Verify: `ai-knowledge-base/frontend/src/stores/user.ts`
- Verify: `ai-knowledge-base/frontend/src/views/LoginView.vue`
- Verify: `ai-knowledge-base/frontend/src/App.vue`

- [ ] **Step 1: Run the frontend build**

Run:

```bash
pnpm build
```

Expected: build succeeds.

- [ ] **Step 2: Run the backend and frontend locally**

Expected:
- backend exposes `/api/login` and `/api/me`
- frontend can submit to backend

- [ ] **Step 3: Verify the happy path**

Expected:
- login form calls `/api/login`
- successful login enters dashboard
- topbar shows backend nickname

- [ ] **Step 4: Verify the failure path**

Expected:
- wrong password shows failure message
- user remains on login page

- [ ] **Step 5: Verify restored session behavior**

Expected:
- refresh with token present triggers `/api/me`
- real user info is restored into the shell
