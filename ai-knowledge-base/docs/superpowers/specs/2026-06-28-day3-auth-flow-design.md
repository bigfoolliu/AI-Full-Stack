# Day 3 Auth Flow Design

## Goal

让前端具备最基础的登录态和路由守卫能力，在没有后端接口的前提下完成 Day 3 的最小闭环。

## Scope

本次只做前端侧假登录流程。

包含：

- `Pinia` 用户状态 `store`
- 本地保存假 token 和用户名
- 登录成功跳转到 `/dashboard`
- 未登录访问后台页时跳转到 `/login`
- 顶部栏展示当前用户信息
- 支持退出登录并返回登录页

不包含：

- 后端登录接口
- `GET /api/me`
- 真实鉴权
- 刷新 token
- 权限细分

## Core Flow

1. 用户访问 `/login`
2. 输入用户名和密码
3. 点击登录
4. 前端写入假 token 和用户名
5. 跳转到 `/dashboard`
6. 访问 `/dashboard` 和 `/knowledge-bases` 需要登录
7. 退出登录后清空本地状态并回到 `/login`

## State Design

使用一个最小用户 store，存储：

- `token`
- `username`
- `isLoggedIn`

提供的最小方法：

- `login(username)`
- `logout()`
- `restore()`

本地持久化使用 `localStorage`。

## Router Design

为需要登录的页面加路由元信息：

- `/dashboard`
- `/knowledge-bases`

全局前置守卫逻辑：

- 未登录访问受保护页面 -> 跳 `/login`
- 已登录访问 `/login` -> 跳 `/dashboard`

## App Shell Design

顶部栏从 store 读取当前用户名。

右上角区域不再只是“跳到登录页”，而是：

- 已登录时显示用户名和一个退出按钮
- 点击退出后执行登出并跳转到 `/login`

## Files To Modify

- Modify: `ai-knowledge-base/frontend/src/main.ts`
- Create: `ai-knowledge-base/frontend/src/stores/user.ts`
- Modify: `ai-knowledge-base/frontend/src/router/index.ts`
- Modify: `ai-knowledge-base/frontend/src/App.vue`
- Modify: `ai-knowledge-base/frontend/src/views/LoginView.vue`
- Modify: `ai-knowledge-base/frontend/src/style.css`

## Acceptance

- 未登录访问后台页会被拦截
- 点击登录可以进入后台
- 顶部栏显示当前用户
- 点击退出后回到登录页
- 构建通过
