## 1. 本周目标

第 8 周的目标有两个主线：一是完成项目 1 的**容器化与一键部署**，让它真正成为一个可交付的作品集项目；二是补齐 Week 7 遗留的**Chunk 策略可配置**和**会话管理**功能。

到本周结束时，你应该具备以下成果：

- 前端 + 后端 + 数据库 + Qdrant + Redis 全容器化
- `docker-compose up` 一键启动
- Chunk 策略可在页面配置（chunk_size、overlap、切分方式）
- 会话删除 / 重命名
- 搜索与回答缓存能力（Redis）
- 架构图与项目文档完善
- 项目达到第一版可投递状态

这一周的唯一目标可以概括为：

**项目 1 可容器化一键启动，功能完整可演示，文档齐备可展示。**

---

## 2. 本周完成标准

如果这一周结束时，你能做到以下几点，就算顺利完成：

- [ ] 前端 Nginx + 后端容器化，`docker-compose up` 一键启动所有服务
- [ ] Chunk 策略参数可在页面配置并生效
- [ ] 会话支持删除和重命名
- [ ] Redis 接入缓存层（搜索缓存 / Session 缓存）
- [ ] 前端错误边界组件覆盖主要页面
- [ ] 有架构图（说明前端、后端、数据库、Qdrant、Redis、模型调用链路）
- [ ] README 补充容器化启动说明和环境变量说明

---

## 3. 本周项目范围

### 3.1 页面范围

1. 知识库设置页 `/knowledge-bases/:id/settings`（增加 Chunk 配置区域）
2. Chat 对话页 `/knowledge-bases/:id/chat`（增加会话删除/重命名操作）
3. 文档列表页（Chunk 配置入口联动）

### 3.2 接口范围

1. `GET /api/knowledge-bases/{id}/settings` — settings 增加 chunk_size / overlap / chunk_strategy 字段
2. `PUT /api/knowledge-bases/{id}/settings` — 同上
3. `DELETE /api/knowledge-bases/{id}/chat/sessions/{session_id}` — 删除会话
4. `PUT /api/knowledge-bases/{id}/chat/sessions/{session_id}` — 重命名会话

### 3.3 学习范围

- Dockerfile 编写（前端 Nginx + 后端 uvicorn）
- Docker Compose 多服务编排
- Redis 基础与缓存策略
- FastAPI BackgroundTasks 异步任务
- Vue 错误边界组件（ErrorBoundary）
- 架构图绘制（推荐 draw.io / Excalidraw）

---

## 4. 每日执行清单

## Day 1：Chunk 策略可配置

### 目标

将硬编码的 chunk_size、overlap、chunk_strategy 开放到页面配置，文档处理时读取。

### 任务清单

- [x] `knowledge_base_settings` 表增加 `chunk_size`、`overlap`、`chunk_strategy` 字段（默认值：512, 64, "recursive"）
- [x] Schema 增加对应字段和校验逻辑
- [x] 设置页增加 Chunk 参数配置区域
- [x] chunk_size 滑块（128-2048，步长 128）
- [x] overlap 滑块（0-512，步长 32，受 chunk_size 约束）
- [x] chunk_strategy 下拉选择（fixed / recursive）
- [x] `process_document` 接口读取知识库配置中的 chunk 参数
- [x] `chunk_service.py` 支持从外部传入参数，而非读取常量
- [x] 保存后下次文档处理时生效

### 验收标准

- [x] 可在页面调整 chunk_size 和 overlap
- [x] 修改后新上传/处理的文档按新参数切分
- [x] 存量文档不受影响

---

## Day 2：会话管理完善

### 目标

让会话列表支持删除和重命名，不再只能新建和切换。

### 任务清单

- [x] 创建 `DELETE /api/knowledge-bases/{id}/chat/sessions/{session_id}` 接口
- [x] 创建 `PUT /api/knowledge-bases/{id}/chat/sessions/{session_id}` 接口（支持 `title` 参数）
- [x] 删除会话时级联删除关联的 messages 和 feedback
- [x] Chat 页面左侧会话列表增加删除按钮（带二次确认）
- [x] 会话标题双击进入编辑模式，回车或失焦保存
- [x] 当前会话被删除后自动切换到最新会话或新建会话
- [x] 被重命名的会话在列表中实时更新

### 验收标准

- [x] 可以删除无用会话
- [x] 可以重命名会话标题
- [x] 删除的会话不再出现在列表中
- [x] 重命名的会话在刷新后保持新名称

---

## Day 3：前端错误边界与异常处理

### 目标

让前端不再是白屏或控制台报错，而是有优雅的错误提示和兜底 UI。

### 任务清单

- [x] 创建全局 ErrorBoundary 组件（Vue 3 `onErrorCaptured`）
- [x] 包裹路由页面组件，出错时展示兜底 UI
- [x] 包装 `axios` 响应拦截器，统一处理 401/403/404/500
- [x] 401 时自动跳转登录页
- [x] 页面级别 loading 状态完善（骨架屏或加载指示器）
- [x] 空状态组件统一（无知识库、无文档、无会话、无搜索结果的占位提示）
- [x] Toast 提示统一封装（Element Plus ElMessage + ElNotification）

### 验收标准

- [x] 后端挂掉时前端显示错误提示而非白屏
- [x] 网络错误时有明确反馈
- [x] 空状态有友好提示，而不是空白页

---

## Day 4：容器化 — 后端 Dockerfile

### 目标

把后端打包成可发布的 Docker 镜像，不再依赖本地 Python 环境。

### 任务清单

- [x] 创建 `backend/Dockerfile`
- [x] 使用多阶段构建（依赖安装 → 运行时）
- [x] 设置 `WORKDIR`、`COPY` 顺序优化缓存
- [x] 安装 `uv` 依赖管理
- [x] 暴露 8000 端口
- [x] 设置 `CMD` 启动 uvicorn
- [x] 编写 `.dockerignore`（排除 .venv、__pycache__、.git）
- [x] 本地构建并验证启动成功

### 验收标准

- [x] `docker build -t kb-backend backend/` 构建成功
- [x] 容器启动后 `/health` 可访问

---

## Day 5：容器化 — 前端 Dockerfile + 全量 Compose

### 目标

前端打包为 Nginx 镜像，所有服务通过 `docker-compose up` 一键启动。

### 任务清单

- [x] 创建 `frontend/Dockerfile`
- [x] 多阶段构建：`npm ci && npm run build` → `nginx:alpine` 运行
- [x] 创建 `frontend/nginx.conf`（路由重写支持 Vue Router history 模式）
- [x] 更新根目录 `docker-compose.yml`，加入所有服务：
  - [x] `frontend` 服务（nginx:alpine）
  - [x] `backend` 服务（uvicorn）
  - [x] `db` 服务（PostgreSQL 16）
  - [x] `qdrant` 服务
  - [x] `redis` 服务
- [x] 服务间网络、依赖顺序、健康检查配置
- [x] 环境变量通过 `.env` 文件传递
- [x] `docker-compose up` 一键启动全栈验证

### 验收标准

- [x] `docker-compose up` 启动后浏览器可访问前端页面
- [x] 前端可正常调用后端接口
- [x] 知识库、文档、Chat 全链路在容器环境下正常

---

## Day 6：Redis 接入与缓存

### 目标

引入 Redis 作为缓存层，提升搜索响应速度和会话体验。

### 任务清单

- [x] 安装 `redis-py` 依赖
- [x] 配置 Redis 连接（`REDIS_URL` 环境变量）
- [x] 封装 `redis_client.py`（连接池 + 基础 get/set）
- [x] 搜索缓存：相同 query + top_k 组合缓存 5 分钟
- [x] 会话列表缓存：知识库会话列表缓存 30 秒
- [x] 缓存失效策略：文档重新处理后清除该知识库的搜索缓存
- [x] 添加 `CACHE_ENABLED` 开关，可在页面或环境变量中关闭

### 验收标准

- [x] 重复搜索相同问题明显变快（命中缓存）
- [x] 文档重新处理后缓存自动失效
- [x] 关闭缓存后恢复到直查模式

---

## Day 7：整理、复盘、封版

### 目标

把第 8 周成果整理成可展示的里程碑版本，体系达到第一版可投递状态。

### 任务清单

- [x] 检查容器化环境下的全链路功能是否正常
- [x] 补充架构图（前端 → Nginx → Backend → PostgreSQL / Redis / Qdrant → LLM）
- [x] 更新 README：
  - [x] 容器化启动说明
  - [x] 环境变量完整说明
  - [x] 目录结构说明
  - [x] 架构图
- [x] 更新 `docs/current-roadmap.md`
- [x] 确保 `make check` 全部通过
- [x] 审视项目完整度，列出 Week 9 面向项目 2 的计划

### 验收标准

- [x] 通过 `git clone && docker-compose up` 可完整启动项目
- [x] 项目 README 和架构图完整
- [x] 项目达到可向面试官展示的状态
- [x] 项目 2 的启动计划已就绪

---

## 5. 本周接口清单汇总

第 8 周新增以下接口：

1. `DELETE /api/knowledge-bases/{id}/chat/sessions/{session_id}` — 删除会话
2. `PUT /api/knowledge-bases/{id}/chat/sessions/{session_id}` — 重命名会话

现有接口变更：

- `GET/PUT /api/knowledge-bases/{id}/settings` — 增加 chunk_size、overlap、chunk_strategy 字段

## 6. 本周页面清单汇总

| 页面 | 路径 | 类型 |
|------|------|------|
| 知识库设置页 | `/knowledge-bases/:id/settings` | 修改（增加 Chunk 配置区域） |
| Chat 对话页 | `/knowledge-bases/:id/chat` | 修改（增加会话删除/重命名） |

## 7. 本周知识点清单汇总

- Dockerfile 编写与多阶段构建
- Docker Compose 多服务编排
- Nginx 反向代理与前端路由重写
- Redis 缓存策略
- FastAPI BackgroundTasks
- Vue 3 错误边界与异常处理
- 架构图绘制
- 项目交付全流程

## 8. 本周完成后的状态

如果你能完成这份清单，第 8 周结束时你将拥有：

- 一个可 `docker-compose up` 一键启动的完整项目
- 一个前后端全容器化的可交付作品
- Chunk 策略可配置的灵活 RAG 系统
- 会话管理完善的对话应用
- Redis 缓存的性能优化
- 完善的文档和架构图
- 一个可正式放入简历的项目材料

这一步很重要，因为它标志着你已经从**「RAG 系统调优与工程化阶段」**进入**「项目交付与作品集阶段」**。从第 9 周开始，将启动项目 2《AI 客服 / 工单 Copilot》，展示你不仅会做知识库，还会做业务 AI 系统。
