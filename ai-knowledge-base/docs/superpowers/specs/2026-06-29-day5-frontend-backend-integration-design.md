# Day 5 Frontend Backend Integration Design

## Goal

完成第一次真实前后端联调，让前端不再依赖 Day 3 的假登录逻辑，而是通过真实后端接口完成登录、用户信息获取和顶部栏展示。

## Scope

本次设计覆盖真实联调与最小体验补齐。

包含：

- 安装并封装 `axios`
- 配置后端 `baseURL`
- 增加请求拦截器
- 登录页调用 `POST /api/login`
- 登录成功后保存真实 token
- 页面初始化调用 `GET /api/me`
- 顶部栏显示后端返回的真实用户昵称
- 增加登录失败提示
- 增加登录提交 loading 状态
- 增加 `GET /api/me` 失败时的最小兜底处理

不包含：

- 刷新 token
- 权限细分
- 全局消息提示系统
- 复杂错误码体系
- 后端 token 真实校验升级

## Current State

当前项目状态：

- 前端已经有登录页、后台壳子、工作台页和知识库页
- `Pinia` 用户状态已经存在
- 路由守卫已经存在
- 但用户登录仍是前端本地 mock 行为
- 顶部栏用户名仍来自前端 store 的假数据
- 后端已经具备：
  - `POST /api/login`
  - `GET /api/me`
  - `GET /health`

这意味着 Day 5 的核心不是再造结构，而是把 Day 3 的 fake auth 替换成真实接口调用。

## Chosen Approach

采用 `store 驱动型联调` 方案。

### Why

把登录、token 存储、用户恢复、拉取当前用户、退出登录这条链路集中在 `Pinia user store` 里，有三个好处：

1. 页面逻辑更轻，`LoginView` 和 `App.vue` 只负责触发和展示
2. token 与用户信息状态不会散落在多个文件里
3. Day 6 以后扩展请求拦截、用户初始化和权限控制时更自然

## Architecture

Day 5 的前端结构建议如下：

```text
frontend/src/
  api/
    http.ts
    auth.ts
  stores/
    user.ts
  views/
    LoginView.vue
  App.vue
```

### Responsibility Split

- `api/http.ts`
  - 创建 axios 实例
  - 配置 `baseURL`
  - 挂载请求拦截器

- `api/auth.ts`
  - 封装 `login(payload)`
  - 封装 `getMe()`

- `stores/user.ts`
  - 管理 token、username、nickname
  - 管理登录、恢复、拉取当前用户、退出登录
  - 管理登录 loading 与错误状态

- `views/LoginView.vue`
  - 采集用户名和密码
  - 调用 store 登录
  - 展示 loading 与错误提示

- `App.vue`
  - 在应用初始化或已登录状态下读取 store 中的真实用户信息
  - 顶部栏展示真实昵称
  - 提供退出按钮

## API Contract Usage

### `POST /api/login`

请求：

```json
{
  "username": "admin",
  "password": "123456"
}
```

成功响应：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "token": "mock-token",
    "user": {
      "id": 1,
      "username": "admin",
      "nickname": "Admin"
    }
  }
}
```

失败响应：

```json
{
  "code": 1,
  "message": "用户名或密码错误",
  "data": null
}
```

### `GET /api/me`

响应：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "id": 1,
    "username": "admin",
    "nickname": "Admin"
  }
}
```

## Store Design

`user store` 从 Day 3 的 fake auth store 升级为真实联调 store。

建议状态包括：

- `token`
- `username`
- `nickname`
- `isLoggedIn`
- `loginLoading`
- `loginError`

建议方法包括：

- `restore()`
  - 从本地恢复 token

- `login(username, password)`
  - 调用 `/api/login`
  - 成功后保存 token 与用户信息
  - 失败后写入错误提示

- `fetchMe()`
  - 调用 `/api/me`
  - 同步真实用户昵称

- `logout()`
  - 清空本地 token 和用户信息

## Axios Design

### Base URL

Day 5 最小版本直接使用本地地址：

- `http://127.0.0.1:8000`

先不引入复杂环境管理。

### Request Interceptor

请求拦截器只做一件事：

- 如果本地有 token，则带上 `Authorization` 头

即使当前后端还没有真正解析 token，这一步也值得先搭好，因为它是后续真实认证结构的基础。

## Login Page Design

登录页需要从“静态表单”升级为“真实联调表单”。

新增行为：

1. 点击登录后进入 loading
2. 调用后端 `/api/login`
3. 成功后保存真实 token 和用户信息
4. 跳转到 `/dashboard`
5. 失败时展示错误提示

保留现有页面结构，不做大范围视觉改造。

## Topbar Design

顶部栏应从 store 中读取真实用户数据。

显示优先级：

1. `nickname`
2. `username`
3. 默认占位文本

退出按钮继续保留，但退出行为应基于真实 store 状态清空。

## Error Handling

Day 5 只做最小错误处理：

- 登录失败显示后端返回的 `message`
- 登录中按钮禁用或显示 loading
- `GET /api/me` 失败时清空本地状态，并回到 `/login` 或保持未登录状态

不做全局弹窗或复杂错误恢复机制。

## Files To Create Or Modify

- Create: `ai-knowledge-base/frontend/src/api/http.ts`
- Create: `ai-knowledge-base/frontend/src/api/auth.ts`
- Modify: `ai-knowledge-base/frontend/src/stores/user.ts`
- Modify: `ai-knowledge-base/frontend/src/views/LoginView.vue`
- Modify: `ai-knowledge-base/frontend/src/App.vue`
- Modify: `ai-knowledge-base/frontend/src/style.css`

## Acceptance Criteria

满足以下条件即可视为 Day 5 设计达成：

- 登录页提交后会真实调用后端登录接口
- 登录成功后保存后端返回的 token
- 登录成功后跳转到后台
- 页面初始化可通过 `GET /api/me` 获取用户信息
- 顶部栏显示后端返回的真实昵称
- 登录失败时页面有明确提示
- 登录过程中有最小 loading 反馈

## Non Goals

以下内容明确不在 Day 5 范围：

- token 刷新
- 权限粒度控制
- 接口缓存
- 全局通知系统
- 多角色用户模型
