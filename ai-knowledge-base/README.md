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

### 前端（第 4 周新增）

- **Pinia 认证 Store**：登录/登出/fetchMe + localStorage token 持久化 + initAuth 初始化恢复
- **axios 拦截器**：请求自动注入 `Authorization: Bearer` header、401 响应自动跳转登录页
- **路由守卫**：Vue Router 全局前置守卫检查 isLoggedIn，未登录重定向到 `/login`
- **文档搜索**：文档列表页新增 `ElInput` 搜索框（300ms debounce） + snippet 高亮展示 + 搜索与状态筛选联动 + 搜索结果分页

### 前端（第 5 周新增）

- **文档处理按钮**：文档列表页每行新增"处理"按钮，调用 `POST /documents/{id}/process` 触发解析→切片→向量化→入库全流程
- **处理状态自动轮询**：触发处理后每 2 秒自动轮询文档列表，直到无文档处于"处理中"状态
- **文档内容查看**：新增"查看"按钮，`el-dialog` 弹窗展示文档解析后的文本内容
- **状态标签配色统一**：待处理→灰色、处理中→蓝色、已完成→绿色、处理失败→红色
- **状态筛选选项修复**：filter 值与后端 `_status_label` 对齐，新增"处理失败"选项

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

### 后端（第 4 周新增）

- **数据库基础设施**：SQLite + SQLAlchemy 2.0 ORM，User / KnowledgeBase / Document 三表模型
- **JWT 认证**：python-jose JWT 签发 + bcrypt 密码哈希 + OAuth2PasswordBearer + Depends 依赖注入保护所有路由
- **文档解析流水线**：PyMuPDF（fitz）PDF 逐页提取 + TXT 编码回退读取，状态流转 pending → parsing → completed / failed
- **FTS5 全文搜索**：SQLite FTS5 虚拟表 + MATCH 查询 + snippet 高亮 + JOIN documents 表获取状态/时间
- **新增接口**：`GET /content` 文档内容查看、`GET /search` 关键词搜索（支持 status 筛选 + 分页）

### 后端（第 5 周新增）

- **文档解析流水线升级**：新增 Word (.docx) 解析支持；状态标签从 `parsing` 改为 `processing`
- **Chunk 切分服务**：`chunk_service.py` 实现 `chunk_text()` 固定大小滑动窗口 + `recursive_chunk_text()` 段落→句子→固定回退；每个 chunk 携带完整元数据（doc_id / kb_id / chunk_index / page_number）
- **向量化与 Qdrant 集成**：`vector_service.py` 封装 Embedding API（DashScope text-embedding-v3, 1024 维）+ Qdrant collection 自动创建、batch upsert、语义搜索、按 kb_id 过滤、按 doc_id 删除
- **全流程编排**：`process_service.py` 串联 parse → chunk → embed → Qdrant → FTS；`POST /documents/{id}/process` 接口手动触发；幂等处理（重复触发先删后插）
- **语义检索**：`POST /api/knowledge-bases/{id}/search` 接口，支持 query + top_k + kb_id 过滤
- **配置泛化**：从 OpenAI 专用配置迁移为通用 `EMBEDDING_API_KEY`/`EMBEDDING_BASE_URL`/`EMBEDDING_MODEL`/`EMBEDDING_DIMENSION`
- **Docker Compose Qdrant**：`docker-compose.yml` 增加 Qdrant 服务（端口 6333/6334，数据持久化到 `data/qdrant/`）
- **Pre-commit 规范**：`.pre-commit-config.yaml` + ruff 格式化/排序 + prettier 前端格式化

### 联调情况

- 登录页已接入真实后端 `POST /api/login`（JWT 认证）
- 页面初始化可调用 `GET /api/me`（Token 鉴权）
- 知识库列表已通过 `GET /api/knowledge-bases` 渲染真实数据（支持搜索 + 分页）
- 新建知识库已调用 `POST /api/knowledge-bases` 并跳转到文档列表页
- 文档列表已调用 `GET /api/knowledge-bases/{id}/documents` 并渲染（支持状态筛选）
- 文件上传已调用 `POST /api/knowledge-bases/{id}/documents`（`UploadFile`）并保存到磁盘
- PDF/TXT 上传后自动解析，状态从"解析中"流转到"已完成"或"解析失败"
- 文档内容搜索已联调 `GET /api/knowledge-bases/{id}/search`，支持关键词 + 状态联合筛选 + 分页

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
- `backend/app/models/` — SQLAlchemy ORM 模型
- `backend/app/services/` — 文档解析 + 全文搜索
- `backend/app/core/` — 配置、数据库引擎、安全模块

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

## 第 4 周接口清单

第 1-3 周接口基础上，第 4 周完成了以下变更：

1. **全量接口数据库化** — 所有接口从 in-memory mock 迁移到 SQLite + SQLAlchemy
2. **JWT 认证替换硬编码登录** — `POST /api/login` + `GET /api/me` 使用真实 JWT 验证
3. **文档解析链路** — `POST /api/knowledge-bases/{id}/documents` 上传后自动解析 PDF/TXT
4. **新增 `GET /{id}/documents/{doc_id}/content`** — 查看文档解析内容（前 5000 字符）
5. **新增 `GET /{id}/search?q=&status=&page=&page_size=`** — FTS5 全文搜索，支持 snippet 高亮 + 状态筛选 + 分页

后端返回统一格式：`ApiResponse{code, message, data}`，分页数据为 `PaginatedData{items, total, page, page_size}`。

## 第 4 周页面清单

第 4 周在 EP 改造完成的 6 个页面上，核心变更：

| 页面 | 路径 | 变更 |
|------|------|------|
| 登录页 | `/login` | 改造：调用 Pinia authStore.login() + axios 拦截器 |
| 文档列表/搜索 | `/knowledge-bases/:id/documents` | 新增 ElInput 搜索框 + snippet 片段列 + 搜索/状态联动 + 分页 |
| 工作台 | `/dashboard` | 不变 |
| 知识库列表 | `/knowledge-bases` | 不变 |
| 新建知识库 | `/knowledge-bases/create` | 不变 |
| 文档上传 | `/knowledge-bases/:id/upload` | 不变 |

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

## 第 5 周接口清单

第 5 周新增以下接口：

1. `POST /api/documents/{id}/process` — 触发文档解析 → 切分 → 向量化 → 入库
2. `GET /api/knowledge-bases/{id}/documents` — 知识库下文档列表（含中文状态标签）
3. `POST /api/knowledge-bases/{id}/search` — 按知识库语义检索（Qdrant 向量相似度）

## 第 5 周页面清单

| 页面 | 路径 | 变更 |
|------|------|------|
| 文档列表/状态 | `/knowledge-bases/:id/documents` | 新增"处理"按钮 + loading 态 + 轮询刷新；新增"查看"按钮 + 内容弹窗；修复状态标签配色；修复筛选选项 |

## 第 5 周完成内容总结

- **文档解析升级**：新增 Word (.docx) 解析，状态标签从 `parsing`→`processing`
- **Chunk 切分服务**：固定大小滑动窗口 + 递归切分策略，携带完整元数据
- **向量化与 Qdrant**：DashScope text-embedding-v3 → 1024 维向量 → Qdrant 存储，支持语义搜索与 kb_id 过滤
- **全流程编排**：上传→手动触发处理→parse→chunk→embed→Qdrant+FTS，状态自动流转，幂等处理
- **前后端状态联动**：前端"处理"按钮触发后端流水线，轮询刷新状态，正确配色显示
- **Docker Compose 集成**：Qdrant 容器化运行，数据持久化到 `data/qdrant/`
- **Pre-commit 规范**：ruff 格式化 + prettier 前端格式化，代码风格统一

第 5 周的项目已经从"真实后端系统"推进到 **「RAG 最小闭环」**。

## 第 6 周接口清单

第 6 周新增以下接口：

1. `POST /api/knowledge-bases/{id}/chat` — 知识库问答（返回完整回答 + 引用来源）
2. `POST /api/knowledge-bases/{id}/chat/stream` — 知识库问答（SSE 流式）
3. `GET /api/knowledge-bases/{id}/chat/sessions` — 会话列表
4. `POST /api/knowledge-bases/{id}/chat/sessions` — 创建/更新会话

## 第 6 周页面清单

| 页面 | 路径 | 变更 |
|------|------|------|
| Chat 对话页 | `/knowledge-bases/:id/chat` | 新增：完整对话页面 |
| 知识库详情页 | `/knowledge-bases/:id/documents` | 新增"问答"入口按钮 |

## 第 6 周完成内容总结

- **LLM 接入**：集成 DashScope Qwen API（OpenAI 兼容格式），支持 `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL` 自定义配置
- **RAG 问答**：`POST /api/knowledge-bases/{id}/chat` 实现 query → 向量检索 → 上下文组装 → LLM 生成回答的全链路
- **流式输出（SSE）**：`POST /api/knowledge-bases/{id}/chat/stream` 逐 token 推送 + 引用来源 + 完成标记，前端 `fetch` + `ReadableStream` 逐字渲染
- **前端 Chat 对话框**：`ChatView.vue` 支持消息收发、Markdown 渲染（markdown-it）、打字机效果、引用来源卡片展示
- **多轮对话**：前端维护 history 列表，后端 `_build_messages()` 按 token 预算截断早期消息
- **会话历史管理**：`chat_sessions` + `chat_messages` 数据库表，前端左侧会话列表（新建/切换），刷新后自动恢复 active_session
- **交互体验**：Enter 发送 / Shift+Enter 换行、重新提问、重试机制、错误提示、空知识库引导

第 6 周的项目已经从 **「RAG 最小闭环」**推进到 **「AI 应用工程：对话与推理阶段」**。

## 下周计划（Week 7）

### 1. 质量与工程化

- 补充后端测试覆盖（单元测试 + 集成测试）
- 前端错误边界与异常处理完善
- 前后端类型一致性检查

### 2. 功能迭代

- 会话删除 / 重命名
- 会话与用户关联
- 知识库权限基础

### 3. 性能优化

- 文档处理异步化（Celery / 后台任务）
- 流式响应延迟优化
- 搜索响应时间优化

## 当前阶段定位

当前版本适合作为：

- 第 5 周阶段性里程碑（RAG 最小闭环）
- 后续 Week 6 引入 LLM 问答与流式对话的基础版本
- AI 全栈转岗过程中的练习项目
