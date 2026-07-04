# AI Knowledge Base

一个面向 AI 全栈转岗训练的最小知识库项目。当前阶段目标不是一次做全，而是按周推进，把前端、后端、联调和业务页一步步串成完整闭环。

## 项目简介

这个项目用于练习一个典型 AI 应用后台的基础能力：

第 1 周重点是把"能跑起来的后台项目骨架"搭出来。
第 2 周重点是从骨架推进到"知识库管理后台雏形"。

到第 2 周结束时，项目已具备：
- 登录页与后台壳子
- 前后端完整联调
- 知识库列表 / 创建 / 文档管理 / 上传完整业务流
- 后端知识库 CRUD 雏形与文档接口

## 技术栈

### Frontend

- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- Axios
- Element Plus（已安装）

### Backend

- FastAPI
- Pydantic
- Uvicorn

## 当前已完成功能

### 前端（第 1 周）

- 登录页 `/login`
- 后台主布局（侧边栏 + 顶部栏）
- 工作台页 `/dashboard`
- 知识库列表页 `/knowledge-bases`
- 登录态管理与路由守卫
- 基于真实后端接口的登录联调
- 顶部栏显示后端返回的用户信息

### 前端（第 2 周新增）

- 新建知识库页 `/knowledge-bases/create` — 表单 + 验证 + 后端联调
- 文档列表 / 状态页 `/knowledge-bases/:id/documents` — 真实接口渲染
- 文档上传页 `/knowledge-bases/:id/upload` — 文件选择 + 上传入口

### 后端（第 1 周）

- `GET /health`
- `POST /api/login`
- `GET /api/me`
- `GET /api/knowledge-bases`
- 统一接口返回格式
- 基础 CORS
- 最小 mock 用户与知识库数据

### 后端（第 2 周新增）

- `POST /api/knowledge-bases` — 新建知识库
- `GET /api/knowledge-bases/{id}` — 知识库详情
- `GET /api/knowledge-bases/{id}/documents` — 文档列表
- `POST /api/knowledge-bases/{id}/documents` — 上传文档（name 字段占位）
- 内存数据结构的 CRUD 雏形

### 联调情况

- 登录页已接入真实后端 `POST /api/login`
- 页面初始化可调用 `GET /api/me`
- 知识库列表已通过 `GET /api/knowledge-bases` 渲染真实数据
- 新建知识库已调用 `POST /api/knowledge-bases` 并展示结果
- 文档列表已调用 `GET /api/knowledge-bases/{id}/documents` 并渲染

## 项目目录结构

```text
ai-knowledge-base/
  frontend/   # Vue 3 前端项目
  backend/    # FastAPI 后端项目
  docs/       # 设计文档与执行计划
  README.md   # 项目总说明
```

### 说明

- `frontend/src/`：前端页面、路由、store、API 封装
- `backend/app/`：后端应用主入口、路由、schema、配置
- `docs/superpowers/`：按天整理的设计和执行计划文档

以下目录主要属于本地开发环境产物，不是项目核心成果本身：

- `frontend/node_modules/`
- `frontend/dist/`
- `backend/.venv/`
- `.idea/`
- `__pycache__/`

## 本地启动方式

### 启动后端

进入后端目录：

```bash
cd backend
```

推荐启动方式：

```bash
.venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 启动前端

进入前端目录：

```bash
cd frontend
```

启动开发服务器：

```bash
pnpm dev
```

## 第 2 周接口清单

第 1 周基础接口之上，第 2 周新增了以下业务接口：

1. `POST /api/knowledge-bases` — 创建知识库
2. `GET /api/knowledge-bases/{id}` — 知识库详情
3. `GET /api/knowledge-bases/{id}/documents` — 文档列表
4. `POST /api/knowledge-bases/{id}/documents` — 上传文档

第 1 周已完成的接口继续保持：

1. `GET /health`
2. `POST /api/login`
3. `GET /api/me`
4. `GET /api/knowledge-bases` — 知识库列表

## 第 2 周页面清单

第 1 周的 3 个页面基础上，第 2 周新增了以下业务页面：

1. 新建知识库页 `/knowledge-bases/create`
2. 文档列表 / 状态页 `/knowledge-bases/:id/documents`
3. 文档上传页 `/knowledge-bases/:id/upload`

第 1 周已完成的页面继续保持：

1. 登录页 `/login`
2. 工作台页 `/dashboard`
3. 知识库列表页 `/knowledge-bases`

## 建议保留的截图

建议至少保留这 6 张页面截图，方便后续做周复盘、项目展示或简历整理：

1. 登录页
2. 工作台页
3. 知识库列表页
4. 新建知识库页
5. 文档列表 / 状态页
6. 文档上传页

## 第 1 周完成内容总结

- 完成了前端后台骨架
- 完成了登录页和最小登录态管理
- 完成了前后端第一次真实登录联调
- 完成了知识库列表页的第一次真实接口渲染
- 完成了后端最小 mock 用户服务与知识库列表接口

第 1 周的项目已经从"模板工程"推进到"可继续扩展的业务后台基础版本"。

## 第 2 周完成内容总结

- 完成了知识库创建页面与后端 POST 接口联调
- 完成了文档列表 / 状态页与后端 GET 接口联调
- 完成了文档上传页的文件选择与上传入口
- 后端扩展了知识库 CRUD（POST + GET detail）与文档接口（GET list + POST upload）
- 所有新增页面保持与后台风格一致，具备 loading、空状态、错误提示
- 页面之间的业务流转已经完整：列表 → 创建、列表 → 文档、文档 → 上传

第 2 周的项目已经从"登录 + 后台模板"推进到"知识库管理后台雏形"。

## 下周计划（Week 3）

Week 3 建议重点推进以下方向：

1. 引入 Element Plus 组件（表格、表单、上传、消息提示），替换手写样式
2. 为知识库列表页增加搜索 / 筛选 / 分页能力
3. 文档上传接入真实后端文件上传接口
4. 后端引入数据库（SQLite 起步），替换内存数据结构
5. 增加文档解析 / 切片的基础后端逻辑
6. 引入简单的向量化与检索概念

## 当前阶段定位

当前版本适合作为：

- 第 2 周阶段性里程碑
- 后续 Week 3 引入数据库、Element Plus 组件、搜索分页的稳定基础版本
- AI 全栈转岗过程中的练习项目雏形
