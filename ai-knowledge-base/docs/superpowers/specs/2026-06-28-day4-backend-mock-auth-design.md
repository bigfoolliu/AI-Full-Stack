# Day 4 Backend Mock Auth Design

## Goal

把后端从“只有健康检查”推进到“可为前端提供最小用户服务”的状态，为 Day 5 的第一次前后端真实联调做好准备。

## Scope

本次只做最小 mock 用户服务，不引入真实认证系统。

包含：

- 规划最小后端目录结构
- 保留并统一 `GET /health`
- 增加 `POST /api/login`
- 增加 `GET /api/me`
- 统一接口返回格式
- 配置基础 `CORS`
- 增加最小配置文件结构

不包含：

- 数据库
- JWT
- 密码加密
- 用户表
- 权限系统
- 真实 token 解析

## Current State

当前后端只有一个单文件应用：

- `backend/main.py`
- 已有 `FastAPI` 实例
- 已有 `GET /health`
- 已有 `GET /`

当前结构适合 Day 1，但不适合继续承载 Day 4 和 Day 5 的接口扩展，因此需要先做一次轻量整理。

## Chosen Approach

采用“最小可联调后端”方案：

1. 进行一次轻量目录拆分
2. 保持 `health` 与 `auth` 路由分离
3. 使用 `Pydantic` schema 定义请求和响应结构
4. 使用 mock 用户和 mock token 完成接口返回
5. 用基础 `CORSMiddleware` 允许前端本地联调

## Directory Structure

建议调整为：

```text
backend/
  app/
    main.py
    api/
      routes/
        health.py
        auth.py
    schemas/
      common.py
      auth.py
    core/
      config.py
  pyproject.toml
  README.md
```

### Responsibility Split

- `app/main.py`
  负责创建 FastAPI 应用、注册中间件、挂载路由

- `app/api/routes/health.py`
  负责健康检查接口

- `app/api/routes/auth.py`
  负责登录和当前用户接口

- `app/schemas/common.py`
  负责统一响应模型

- `app/schemas/auth.py`
  负责登录请求模型、用户信息模型、登录响应数据模型

- `app/core/config.py`
  负责最小配置项，例如应用名、允许的前端地址

## API Design

### 1. `GET /health`

用途：

- 提供健康检查
- 同时开始对齐统一响应格式

响应示例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "status": "ok"
  }
}
```

### 2. `POST /api/login`

用途：

- 为前端登录页提供第一次真实接口联调目标

请求示例：

```json
{
  "username": "admin",
  "password": "123456"
}
```

响应示例：

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

### 3. `GET /api/me`

用途：

- 为前端顶部栏和页面初始化提供最小用户信息接口

响应示例：

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

## Mock Auth Rules

Day 4 不实现真实认证，只实现可联调的 mock 行为。

建议约定：

- 只接受一组固定账号密码：
  - `username = "admin"`
  - `password = "123456"`
- 登录成功返回固定 `mock-token`
- 登录失败返回非 0 的 `code` 和明确的错误信息
- `GET /api/me` 暂时直接返回固定用户信息，不解析真实 token

这样做的价值在于：

- 前端能完成第一次真实接口调用
- 不会把复杂认证逻辑提前塞进 Day 4
- Day 5 能专注在联调而不是后端认证体系

## Response Format

统一响应格式定义为：

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

约定如下：

- `code = 0` 表示成功
- `code != 0` 表示失败
- `message` 传达人类可读结果
- `data` 承载业务数据

## CORS Design

为 Day 5 前端联调，至少需要允许：

- `http://localhost:5173`

初期建议只放这一个来源，保持简单明确。

## Config Design

Day 4 的配置只做最小结构，不引入复杂环境系统。

建议配置项包括：

- `app_name`
- `allowed_origins`

后续如果 Day 5/Day 6 需要扩展，再考虑更复杂的配置方式。

## Error Handling

Day 4 只做最小错误处理：

- 登录参数错误或账号密码不匹配时返回失败响应
- 不需要做全局异常体系
- 不需要引入日志平台

## Files To Create Or Modify

- Create: `ai-knowledge-base/backend/app/main.py`
- Create: `ai-knowledge-base/backend/app/api/routes/health.py`
- Create: `ai-knowledge-base/backend/app/api/routes/auth.py`
- Create: `ai-knowledge-base/backend/app/schemas/common.py`
- Create: `ai-knowledge-base/backend/app/schemas/auth.py`
- Create: `ai-knowledge-base/backend/app/core/config.py`
- Modify: `ai-knowledge-base/backend/pyproject.toml`
- Modify: `ai-knowledge-base/backend/README.md`
- Remove or deprecate: `ai-knowledge-base/backend/main.py`

## Acceptance Criteria

满足以下条件即可视为 Day 4 设计达成：

- 后端目录结构已从单文件升级为最小可扩展结构
- `GET /health` 可用且使用统一响应格式
- `POST /api/login` 可用
- `GET /api/me` 可用
- 前端本地可通过 `CORS` 访问后端
- Day 5 已具备真实联调所需的最小接口基础

## Non-Goals

以下内容明确不在本次实现范围：

- 真实认证体系
- 生产级用户管理
- 数据库存储
- Redis
- 刷新 token
- 权限与角色模型
