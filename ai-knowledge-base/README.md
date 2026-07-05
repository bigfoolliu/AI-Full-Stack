# AI Knowledge Base

一个面向 AI 全栈转岗训练的最小知识库项目。按周推进，把前端、后端、联调和业务页一步步串成完整闭环。

## 项目简介

- 第 1 周：搭建"能跑起来的后台项目骨架"
- 第 2 周：从骨架推进到"知识库管理后台雏形"
- 第 3 周：全面引入 Element Plus，升级为"具备产品感的系统"

到第 3 周结束时，项目已具备：
- 6 个页面全部使用 Element Plus 组件，风格统一
- 知识库列表支持搜索、状态筛选、分页
- 拖拽式文件上传 + 后端真实文件存储
- 面包屑导航、loading/空状态/错误反馈完善

## 技术栈

### Frontend

- Vue 3 + TypeScript
- Vite
- Vue Router
- Pinia
- Axios
- **Element Plus（全面落地）** — ElTable / ElForm / ElUpload / ElPagination / ElSelect / ElBreadcrumb / ElCard / ElTag / ElStatistic / ElMessage / ElAlert

### Backend

- FastAPI
- Pydantic
- Uvicorn
- python-multipart（文件上传）

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

### 前端（第 3 周新增）

- **知识库列表页** — 全面 EP 化：`ElTable` + `ElPagination` 分页 + `ElInput` 搜索（300ms debounce）+ 搜索与分页联动
- **新建知识库页** — `ElForm` 内置验证规则（必填/长度/纯空格检测），创建成功后跳转到文档列表页
- **文档列表页** — `ElTable` + `ElTag` 状态标签 + `ElSelect` 状态筛选（全部/已完成/解析中/待处理）
- **文档上传页** — `ElUpload` 拖拽上传 + 50MB 限制 + 真实后端 `UploadFile` 文件存储 + 上传成功自动跳转
- **工作台页** — `ElCard` + `ElStatistic` 展示概览数据
- **登录页** — `ElForm` + `ElInput` + `ElButton` + `ElAlert` 错误提示 + 表单验证
- **面包屑导航** — `ElBreadcrumb` 动态显示页面路径
- 所有页面统一 loading、空状态、错误提示

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

### 后端（第 3 周新增）

- `GET /api/knowledge-bases` — 新增 `keyword`、`page`、`page_size` 参数（名称/描述过滤 + 分页）
- `GET /api/knowledge-bases/{id}/documents` — 新增 `status` 筛选参数
- `POST /api/knowledge-bases/{id}/documents` — 升级为 `UploadFile` 真实文件上传，保存到 `uploads/{kb_id}/`
- 静态文件服务挂载 `/uploads`
- `config.py` 新增 `UPLOAD_DIR` 配置

### 联调情况

- 登录页已接入真实后端 `POST /api/login`
- 页面初始化可调用 `GET /api/me`
- 知识库列表已通过 `GET /api/knowledge-bases` 渲染真实数据（支持搜索 + 分页）
- 新建知识库已调用 `POST /api/knowledge-bases` 并跳转到文档列表页
- 文档列表已调用 `GET /api/knowledge-bases/{id}/documents` 并渲染（支持状态筛选）
- 文件上传已调用 `POST /api/knowledge-bases/{id}/documents`（`UploadFile`）并保存到磁盘

## 项目目录结构

```text
ai-knowledge-base/
  frontend/   # Vue 3 前端项目
  backend/    # FastAPI 后端项目
  docs/       # 设计文档与执行计划
  README.md   # 项目总说明
```

### 说明

- `frontend/src/views/` — 6 个 Element Plus 业务页面
- `frontend/src/api/` — 后端接口封装
- `frontend/src/router/` — 路由 + 守卫
- `frontend/src/stores/` — Pinia 状态管理
- `backend/app/api/routes/` — FastAPI 路由
- `backend/app/schemas/` — Pydantic 数据模型
- `backend/app/core/` — 配置

以下目录主要属于本地开发环境产物，不是项目核心成果本身：

- `frontend/node_modules/`
- `frontend/dist/`
- `backend/.venv/`
- `.idea/`
- `__pycache__/`
- `uploads/`

## 本地启动方式

### 启动后端

```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 启动前端

```bash
cd frontend
npm run dev
```

后端默认运行在 `http://127.0.0.1:8000`，前端在 `http://localhost:5173`。

## 第 3 周接口清单

第 1-2 周接口基础上，第 3 周扩展了以下参数：

1. `GET /api/knowledge-bases` — 新增 `keyword`（搜索）、`page`（分页页码）、`page_size`（每页条数）
2. `GET /api/knowledge-bases/{id}/documents` — 新增 `status`（文档状态筛选）
3. `POST /api/knowledge-bases/{id}/documents` — 升级为 `UploadFile` 文件上传，返回 `file_size`、`file_path`

后端返回统一分页格式：`PaginatedData{items, total, page, page_size}`。

## 第 3 周页面清单

第 1-2 周的 6 个页面全部完成 Element Plus 改造：

| 页面 | 路径 | 核心 EP 组件 |
|------|------|-------------|
| 登录页 | `/login` | ElForm / ElInput / ElButton / ElAlert |
| 工作台 | `/dashboard` | ElCard / ElStatistic / ElTag |
| 知识库列表 | `/knowledge-bases` | ElTable / ElPagination / ElInput + Search icon |
| 新建知识库 | `/knowledge-bases/create` | ElForm / ElInput / ElButton |
| 文档列表/状态 | `/knowledge-bases/:id/documents` | ElTable / ElTag / ElSelect |
| 文档上传 | `/knowledge-bases/:id/upload` | ElUpload（drag）/ ElIcon / ElButton |

## 建议保留的截图

建议至少保留这 6 张页面截图，方便后续做周复盘、项目展示或简历整理：

1. 登录页（ElForm 风格）
2. 工作台页（ElStatistic 概览卡片）
3. 知识库列表页（ElTable + 搜索框 + 分页）
4. 新建知识库页（ElForm 验证）
5. 文档列表 / 状态页（ElTable + 状态筛选 ElSelect）
6. 文档上传页（ElUpload 拖拽区域）

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

## 第 3 周完成内容总结

- **Element Plus 全面落地**：6 个页面全部使用 EP 组件，统一风格
- **搜索 + 分页**：知识库列表支持关键词搜索（300ms debounce）和后端分页联动
- **状态筛选**：文档列表页支持按"已完成/解析中/待处理"筛选
- **真实文件上传**：ElUpload 拖拽上传，后端基于 `UploadFile` 保存到 `uploads/{kb_id}/`
- **交互打磨**：面包屑导航、ElAlert 错误提示、上传中禁用返回、创建后自动跳转文档列表页
- **后端扩展**：分页返回格式 `PaginatedData`、keyword/status 参数、uplloads 静态文件服务

第 3 周的项目已经从"知识库管理后台雏形"推进到"具备产品感的系统"。

## 下周计划（Week 4）

### 1. 后端数据库

- 引入 SQLite + SQLAlchemy，替换 in-memory mock 数据
- 用户、知识库、文档表模型定义
- Alembic 迁移管理

### 2. 文档解析流水线

- PDF / TXT 文档内容解析
- 文本分块（chunking）策略
- 解析状态管理（待处理 → 解析中 → 已完成）

### 3. 语义搜索

- 引入文本 Embedding（如 sentence-transformers）
- 基于向量相似度的检索替代关键词搜索
- 搜索结果显示片段高亮

### 4. 认证完善

- JWT 续期 / 刷新机制
- 权限细分（管理员 / 普通用户）

## 当前阶段定位

当前版本适合作为：

- 第 3 周阶段性里程碑
- 后续 Week 4 引入数据库、文档解析、语义搜索的稳定基础版本
- AI 全栈转岗过程中的练习项目
