# Week 4 任务清单

## 1. 本周目标

Week 4 的目标是将项目从 **"mock 原型"升级为"真实后端系统"**。

到本周结束时，你应该具备以下成果：

- 所有数据从内存 mock 迁移到 SQLite + SQLAlchemy
- 登录认证从硬编码升级为 JWT 真实认证
- 上传的 PDF/TXT 文档可解析出文本内容并存储
- 文档内容支持 FTS5 全文检索
- 所有后端接口都有真实 DB 支撑

这一周的唯一目标可以概括为：

**让项目从"mock 演示"升级为"有数据库支撑的真实系统"。**

---

## 2. 本周完成标准

如果这一周结束时，你能做到以下几点，就算顺利完成：

- [ ] 所有 API 不再使用内存 mock 数据，全部走 SQLite + SQLAlchemy
- [ ] 登录使用 JWT Token，密码加密存储
- [ ] 上传 PDF/TXT 后可提取文本内容
- [ ] 文档内容支持 FTS5 全文搜索
- [ ] 所有后端接口经过 curl 验证
- [ ] README 已经补充第 4 周完成内容与下周计划

---

## 3. 本周项目范围

### 3.1 新增依赖

```toml
sqlalchemy>=2.0
aiosqlite
python-jose[cryptography]
passlib[bcrypt]
PyMuPDF         # PDF 解析（fitz）
```

安装方式：

```bash
uv add sqlalchemy aiosqlite "python-jose[cryptography]" "passlib[bcrypt]" PyMuPDF
```

### 3.2 数据库模型

```text
User           — id, username, password_hash, nickname, created_at
KnowledgeBase  — id, name, description, created_at
Document       — id, knowledge_base_id, filename, status, content, file_path, created_at
```

### 3.3 接口范围

**改造接口（数据源改为 DB，参数保持不变）：**

1. `POST /api/login` — 从 mock 改为 JWT 验证
2. `GET /api/me` — 从 mock 改为查 User 表 + Token 鉴权
3. `GET /api/knowledge-bases` — 从 mock 改为 DB 分页查询（keyword、page、page_size）
4. `POST /api/knowledge-bases` — 写入 DB
5. `GET /api/knowledge-bases/{id}` — 查 DB
6. `GET /api/knowledge-bases/{id}/documents` — 查 DB，status 筛选
7. `POST /api/knowledge-bases/{id}/documents` — 上传 + 解析 + 写入 DB

**新增接口：**

8. `GET /api/knowledge-bases/{id}/documents/{doc_id}/content` — 文档内容查看
9. `GET /api/knowledge-bases/{id}/search?q=keyword` — FTS5 全文搜索

### 3.4 页面范围

**改造页面：**

1. 登录页 `/login` — 调用 Pinia authStore 维护登录态
2. 文档列表/搜索页 `/knowledge-bases/:id/documents` — 新增关键词搜索框

**不改造页面（数据源后台切换，UI 不变）：**

3. 工作台 `/dashboard`
4. 知识库列表 `/knowledge-bases`
5. 新建知识库 `/knowledge-bases/create`
6. 文档上传页 `/knowledge-bases/:id/upload`

**新增文件：**

7. 前端 `src/stores/auth.ts` — Pinia 认证 store

### 3.5 学习范围

- SQLAlchemy 2.0 ORM（declarative_base、Column、relationship、session、query）
- JWT 原理与实现（jose.jwt encode/decode、exp 过期）
- passlib 密码哈希（bcrypt）
- FastAPI 依赖注入（Depends + get_db + get_current_user）
- PyMuPDF（fitz）PDF 文本提取
- SQLite FTS5 全文搜索（CREATE VIRTUAL TABLE、MATCH、snippet）
- Pinia 状态管理（auth store + localStorage 持久化）
- axios 拦截器（请求注入 Token + 401 跳转）

---

## 4. 推荐目录结构

```text
backend/app/
  core/
    __init__.py        # 新增
    config.py          # 更新：DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES
    database.py        # 新增：engine + SessionLocal + Base + init_db
    security.py        # 新增：JWT 生成/验证 + 密码哈希 + get_current_user
  models/              # 新增：SQLAlchemy 模型
    __init__.py
    user.py
    knowledge_base.py
    document.py
  schemas/
    auth.py            # 更新：新增 TokenResponse
    knowledge_base.py  # 更新：新增 DocumentContent
    common.py          # 不变
  api/
    routes/
      auth.py              # 重写：JWT 登录 + 获取当前用户
      knowledge_bases.py   # 重写：所有接口走 DB
      health.py            # 不变
  services/            # 新增：业务逻辑层
    __init__.py
    document_parser.py # PDF/TXT 解析
    search_service.py  # FTS5 搜索封装
  main.py              # 更新：添加 startup 事件 init_db

frontend/src/
  stores/
    auth.ts            # 新增：Pinia 认证 store
  api/
    request.ts         # 更新：axios 拦截器注入 Token + 401 处理
  views/
    LoginView.vue          # 更新：调用 authStore.login()
    KnowledgeBaseDocumentsView.vue  # 更新：新增搜索框
  router/
    index.ts           # 更新：导航守卫检查登录态
```

---

## 5. 每日执行清单

### Day 1：项目目录结构调整 + 数据库基础设施

#### 目标

建立 SQLAlchemy 基础设施，创建数据库模型，完成数据库初始化。

#### 任务清单

- [x] 安装新依赖：`uv add sqlalchemy aiosqlite "python-jose[cryptography]" "passlib[bcrypt]" PyMuPDF`
- [x] 创建 `app/core/__init__.py`
- [x] 创建 `app/core/database.py`：engine（SQLite `aiosqlite`）、SessionLocal、Base、init_db
- [x] 更新 `app/core/config.py`：添加 DATABASE_URL、JWT_SECRET、JWT_ALGORITHM、JWT_EXPIRE_MINUTES
- [x] 创建 `app/models/` 目录 + `__init__.py`（导出所有模型）
- [x] 创建 `app/models/user.py`：User（id、username、password_hash、nickname、created_at）
- [x] 创建 `app/models/knowledge_base.py`：KnowledgeBase（id、name、description、created_at）
- [x] 创建 `app/models/document.py`：Document（id、kb_id、filename、status、content、file_path、created_at）
- [x] 在 `app/main.py` 中添加 startup event，启动时调用 init_db
- [x] 用 `sqlite3` 命令行验证表已创建

#### 今日重点

- `init_db` 不仅要创建表，还应该插入初始 mock 数据（示例知识库 + 管理员用户），保证旧功能不断
- `SessionLocal` 要基于 `create_engine(..., check_same_thread=False)` 开启 SQLite 多线程支持

#### 验收标准

- [x] 启动后端后自动创建 `knowledge_base.db` 文件
- [x] 数据库中包含 users、knowledge_bases、documents 三张表
- [x] 表结构包含上述所有字段
- [x] startup 后数据库有初始数据（管理员用户 + 示例知识库）

---

### Day 2：迁移知识库 + 文档 API 到 DB

#### 目标

将所有 GET/POST 知识库和文档接口从 mock 数据迁移到 SQLAlchemy 查询。

#### 任务清单

- [x] 实现 `get_db` 依赖（yield SessionLocal）
- [x] 重写 `GET /api/knowledge-bases`：`db.query(KnowledgeBase)`，支持 keyword 模糊匹配 + page/page_size
- [x] 重写 `POST /api/knowledge-bases`：创建 KnowledgeBase 记录写入 DB
- [x] 重写 `GET /api/knowledge-bases/{id}`：按 id 查 DB，不存在返回 404
- [x] 重写 `GET /api/knowledge-bases/{id}/documents`：`db.query(Document).filter(kb_id=...)`，支持 status 筛选
- [x] 重写 `POST /api/knowledge-bases/{id}/documents`：保存 UploadFile 到磁盘 + 创建 Document 记录写入 DB
- [x] 删除 `MOCK_KNOWLEDGE_BASES` 和 `MOCK_DOCUMENTS`
- [x] 用 curl 验证所有接口返回正确

#### 今日重点

- 所有 mock 常量和硬编码数据全部删除
- 分页、搜索、筛选的逻辑不变，只换数据源
- `get_db` 做成 FastAPI 依赖统一管理 session 生命周期

#### 验收标准

- [x] `GET /api/knowledge-bases` 返回从 DB 查询的数据
- [x] `POST /api/knowledge-bases` 创建的数据写入 DB
- [x] 分页、搜索、筛选功能与 DB 联动正常
- [x] 不存在的 id 返回 404

---

### Day 3：JWT 认证

#### 目标

从硬编码 mock 登录升级为 JWT 真实认证。

#### 任务清单

- [x] 创建 `app/core/security.py`
  - `create_access_token(data: dict)` — 生成 JWT（使用 `jose.jwt.encode` + exp）
  - `verify_password(plain: str, hashed: str) -> bool` — passlib bcrypt 验证
  - `get_password_hash(password: str) -> str` — passlib bcrypt 哈希
  - `get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db))` — 解析 Token 查 DB
  - 异常处理：Token 过期/无效 → HTTPException 401
- [x] 重写 `POST /api/login`
  - 验证用户名密码（查 User 表 + verify_password）
  - 返回 JWT access_token + user 信息
  - 密码错误返回 401
- [x] 重写 `GET /api/me`
  - 使用 `get_current_user` 依赖
  - 返回当前用户 UserInfo
- [x] 知识库和文档接口添加 `Depends(get_current_user)` 保护
- [x] init_db 时创建默认管理员用户（密码哈希存储，username=admin, password=123456）
- [x] 删除 `MOCK_USERNAME`、`MOCK_PASSWORD`、`MOCK_TOKEN`、`MOCK_USER` 配置项
- [x] 用 curl 验证登录、鉴权、401 流程

#### 今日重点

- `OAuth2PasswordBearer(tokenUrl="/api/login")` 是 FastAPI 内置的 Token 提取方案
- `get_current_user` 做成 FastAPI 依赖后，所有接口只需加 `Depends(get_current_user)` 即可保护

#### 验收标准

- [x] 使用错误密码登录返回 401
- [x] 正确登录后返回有效的 JWT Token
- [x] 使用 Token 可调用 `/api/me` 获取用户信息
- [x] 无 Token 或 Token 过期返回 401
- [x] 知识库接口在无 Token 时返回 401

---

### Day 4：前端认证适配 + 全局 token 管理

#### 目标

前端适配 JWT 认证流程，所有请求自动携带 Token。

#### 任务清单

- [ ] 创建 `src/stores/auth.ts`（Pinia store）
  - state: `token`（localStorage 持久化）、`user`（UserInfo | null）
  - getter: `isLoggedIn`
  - action: `login(username, password)` → 调用 `POST /api/login` → 存储 token + user
  - action: `logout()` → 清除 token + user → router.push('/login')
  - action: `initAuth()` → 从 localStorage 恢复 token → 调用 `/api/me` 验证有效性
- [ ] 更新 `src/api/request.ts`（axios 拦截器）
  - 请求拦截器：从 authStore 读取 token，加到 `Authorization: Bearer xxx`
  - 响应拦截器：401 时调用 `authStore.logout()` 并跳转登录页
- [ ] 更新 `LoginView.vue`
  - 调用 `authStore.login()` 替代直接调 API
  - 登录成功后 `router.push('/dashboard')`
  - 错误时展示 ElAlert
- [ ] 更新 `router/index.ts`
  - 全局前置守卫：检查 `authStore.isLoggedIn`
  - 未登录且不在 `/login` → 重定向到 `/login`
  - 已登录时访问 `/login` → 重定向到 `/dashboard`
- [ ] 在 `App.vue` 或 `ShellTopbar.vue` 中添加退出按钮（调用 `authStore.logout()`）
- [ ] 在入口 `main.ts` 中初始化 authStore：`app.use(createPinia())` + 调用 `authStore.initAuth()`

#### 今日重点

这是前端第一次真正管理认证状态。Pinia store + axios 拦截器 + 路由守卫形成完整认证闭环。

#### 验收标准

- [ ] 未登录状态下访问后台页面自动跳转登录页
- [ ] 登录后请求自动携带 `Authorization: Bearer xxx`
- [ ] Token 过期或被清除后自动跳转登录页
- [ ] 退出登录清除本地 Token 并跳转登录页
- [ ] 已登录后访问 `/login` 自动重定向到工作台

---

### Day 5：PDF / TXT 文档解析

#### 目标

上传文档后能自动提取文本内容，完成"上传 → 解析 → 入 DB"的完整链路。

#### 任务清单

- [ ] 创建 `app/services/__init__.py`
- [ ] 创建 `app/services/document_parser.py`
  - `parse_document(file_path: str, file_type: str) -> str`
  - PDF 解析：`fitz.open()` → 逐页提取 text
  - TXT 解析：`open().read()` 按 UTF-8 读取
  - 异常处理：解析失败抛出异常，由调用方处理
- [ ] 更新 `POST /api/knowledge-bases/{id}/documents`
  - 上传保存文件后，调用 `parse_document`
  - 更新 Document.status：`pending` → `parsing` → `completed`
  - 解析出的文本写入 Document.content 字段
  - 解析失败时 status → `failed`，content 记录错误信息
- [ ] 创建 `GET /api/knowledge-bases/{id}/documents/{doc_id}/content`
  - 返回文档 ID、文件名、状态、文本内容（前 5000 字符）等
- [ ] 用 curl 验证上传 PDF/TXT 后的解析效果

#### 今日重点

- 当前做同步解析，文档较大时请求会卡住，后续可改为 Celery 异步
- 解析内容是 RAG 的基石，确保提取的文本干净完整
- 状态流转必须准确，前端依赖状态显示

#### 验收标准

- [ ] 上传 PDF 后能提取出文本内容，存入 Document.content
- [ ] 上传 TXT 后能提取出文本内容
- [ ] 文档 status 正确流转：pending → parsing → completed
- [ ] 解析失败的文档 status → failed
- [ ] 通过 `/content` 接口可查看解析结果

---

### Day 6：FTS5 全文搜索

#### 目标

为文档内容建立全文索引，支持关键词搜索。

#### 任务清单

- [ ] 在 `app/models/document.py` 或单独模块中定义 FTS5 虚拟表 `document_fts`
  - 包含列：`doc_id`、`kb_id`、`filename`、`content`
  - 使用 `CREATE VIRTUAL TABLE document_fts USING fts5(...)`
- [ ] 创建 `app/services/search_service.py`
  - `create_fts_index(db, document)` — 为解析完成的文档建立 FTS5 索引
  - `search_documents(db, kb_id: int, keyword: str, page, page_size) -> PaginatedData`
  - 使用 FTS5 MATCH 查询，返回 snippet 高亮片段
  - 结果包含：文档 ID、文件名、kb_id、片段、匹配得分
- [ ] 文档解析完成后自动调用 `create_fts_index` 建索引
- [ ] 创建 `GET /api/knowledge-bases/{id}/search?q=keyword&page=1&page_size=10`
  - 调用 search_service
  - 返回 PaginatedData 格式
- [ ] 用 curl 验证 FTS5 搜索（精确匹配、模糊匹配、中文分词效果）

#### 今日重点

- SQLite FTS5 支持中文，但默认分词器对中文支持有限。如果中文分词效果不好，可以接受，Week 5 的 Embedding 语义搜索会彻底解决这个问题
- FTS5 的核心用法：`SELECT * FROM document_fts WHERE content MATCH ?`

#### 验收标准

- [ ] 搜索关键词可召回相关文档
- [ ] 搜索结果包含文档摘要/高亮片段
- [ ] 搜索接口支持分页
- [ ] FTS5 索引随文档解析自动更新
- [ ] 新上传+解析的文档可被搜索到

---

### Day 7：前端搜索交互 + 整理收尾

#### 目标

让用户能在文档列表页中搜索文档内容，记录本周完成内容。

#### 任务清单

- [ ] 更新 `KnowledgeBaseDocumentsView.vue`
  - 在状态筛选 `ElSelect` 旁增加关键词搜索 `ElInput`（v-model、300ms debounce）
  - 调用 `GET /api/knowledge-bases/{id}/search?q=xxx`
  - 搜索结果以当前表格形式展示：文件名、状态、内容片段（从 snippet 截取）
  - 搜索与状态筛选联动（q + status 同时传）
- [ ] 更新 `src/api/knowledge-bases.ts`
  - 新增 `searchKnowledgeBaseDocuments(id: number, params: {q?, status?, page?, pageSize?})`
- [ ] 全局功能检查
  - [ ] 完整链路：登录 → 创建知识库 → 上传 PDF → 等待解析 → 搜索 → 看到结果
  - [ ] 用 curl 验证所有 9 个接口
  - [ ] 确认 `.gitignore` 排除 `*.db` 和 `uploads/` 下实际文件
- [ ] 更新 README（第 4 周完成内容：DB、JWT、解析、FTS5）
- [ ] 记录下周计划（Week 5：Qdrant + Embedding + 语义检索 + RAG 问答）

#### 验收标准

- [ ] 前端文档列表页支持关键词搜索
- [ ] 搜索与状态筛选可同时使用
- [ ] 完整链路：登录 → 创建知识库 → 上传 PDF → 解析完成 → 搜索到内容
- [ ] README 已更新到第 4 周阶段

---

## 6. 本周接口清单汇总

| 方法 | 路径 | 变更类型 | 说明 |
|------|------|----------|------|
| POST | `/api/login` | 改造 | 从 mock 改为 JWT 验证 |
| GET | `/api/me` | 改造 | 从 mock 改为 Token 鉴权查 DB |
| GET | `/api/knowledge-bases` | 改造 | 数据源改为 DB，参数不变 |
| POST | `/api/knowledge-bases` | 改造 | 写入 DB |
| GET | `/api/knowledge-bases/{id}` | 改造 | 查 DB |
| GET | `/api/knowledge-bases/{id}/documents` | 改造 | 查 DB |
| POST | `/api/knowledge-bases/{id}/documents` | 改造 | 上传 + 解析 + 入 DB |
| GET | `/api/knowledge-bases/{id}/documents/{doc_id}/content` | 新增 | 文档内容查看 |
| GET | `/api/knowledge-bases/{id}/search?q=` | 新增 | FTS5 全文搜索 |

---

## 7. 本周页面清单汇总

| 页面 | 路径 | 变更 |
|------|------|------|
| 登录页 | `/login` | 改造：调用 authStore.login() |
| 文档列表/搜索 | `/knowledge-bases/:id/documents` | 改造：新增搜索框 |
| 工作台 | `/dashboard` | 不变 |
| 知识库列表 | `/knowledge-bases` | 不变 |
| 新建知识库 | `/knowledge-bases/create` | 不变 |
| 文档上传 | `/knowledge-bases/:id/upload` | 不变 |

**新增前端文件：**

| 文件 | 说明 |
|------|------|
| `src/stores/auth.ts` | Pinia 认证 store，管理 token/user/isLoggedIn |

---

## 8. 本周知识点清单汇总

- **SQLAlchemy 2.0 ORM**：declarative_base、Column 类型、relationship、Session 生命周期
- **JWT**：python-jose 的 encode/decode、exp 过期时间、OAuth2PasswordBearer
- **passlib**：bcrypt 哈希与验证
- **FastAPI 依赖注入**：Depends + get_db + get_current_user 组合使用
- **PyMuPDF（fitz）**：PDF 文档逐页文本提取
- **SQLite FTS5**：虚拟表创建、MATCH 查询、snippet 高亮
- **Pinia**：auth store 设计、localStorage 持久化、initAuth 恢复
- **axios 拦截器**：请求注入 Authorization header、响应 401 自动跳转
- **Vue Router 导航守卫**：全局前置守卫鉴权

---

## 9. 本周完成后的状态

如果你能完成这份清单，第 4 周结束时你将拥有：

- 一个使用 SQLite + SQLAlchemy 的真实后端（不再有内存 mock 数据）
- JWT 认证替代了硬编码 mock 登录（前端 Pinia store + 拦截器 + 路由守卫）
- 上传的 PDF/TXT 文档可自动提取文本内容
- 文档内容支持 FTS5 全文搜索，前端可搜索文档内容
- 项目从"mock 原型"正式升级为"真实后端系统"

**无缝衔接 Week 5：Qdrant + Embedding + 语义检索 + RAG 问答链路。**
