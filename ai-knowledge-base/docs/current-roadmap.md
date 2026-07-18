# Current Roadmap

## Current Priorities

### Week 9：项目 2 — AI 工单 Copilot

从第 9 周起，启动全新项目 2《AI 工单 Copilot》，不再扩展知识库项目。

核心方向：一个面向企业内部客服/运维的工单智能助手。

### Week 9 初步规划

1. **项目脚手架**：复用项目 1 的前端脚手架和后端基础组件，搭建新项目骨架
2. **工单系统核心**：
   - 工单创建（标题、描述、优先级、分类）
   - 工单流转（待处理、处理中、已完成、已关闭）
   - 工单列表（筛选、排序、分页）
3. **AI 辅助**：
   - 工单内容自动摘要
   - 相似工单推荐
   - 回复建议
4. **数据看板**：工单统计、处理时长、满意度分析
5. **测试与文档**：后端测试脚本，README 与架构图

## Completed

### Week 8：容器化 + 缓存 + 封版

- Chunk 策略（chunk_size/overlap/strategy）页面可配置，文档处理实时读取
- 会话删除（级联清理消息/反馈）、双击重命名、故障自动切换
- ErrorBoundary 全局错误兜底（所有路由页面）、EmptyState 空状态引导（3 个场景）、axios 统一 401/403/404/500 处理
- Toast 工具函数封装（ElMessage + ElNotification），所有页面 loading 状态完善
- 前端 Dockerfile（node:22 多阶段 → nginx:alpine）+ 后端 Dockerfile（uv-based python3.13-slim）
- docker-compose.yml 全服务编排（frontend + backend + qdrant + redis + postgres）
- Redis 7 容器化，连接池封装，FTS 搜索缓存 5min、语义搜索缓存 5min、会话列表缓存 30s，文档处理后自动失效
- 架构图（Mermaid）、README 容器化启动说明和环境变量表
- `make check` 全部通过

### Week 7：RAG 系统调优与工程化

- 知识库配置系统（knowledge_base_settings 表 + 全量参数页面可配）
- 检索/Prompt/模型/Hybrid Search/Rerank 实时生效
- Hybrid Search（FTS5 + Qdrant 向量 alpha 融合）
- Metadata Filter（按 filename/status 过滤）
- Rerank 本地策略（关键词密度 + 向量分数）
- Retrieval 指标（命中数、得分分布、耗时）
- 回答反馈、A/B 效果对比
- 全链路 docstring + 参数说明文档

### Week 6：LLM 集成与 RAG 对话

- DashScope Qwen LLM 接入，RAG 问答全链路
- SSE 流式输出 + 前端打字机效果
- 多轮对话 + 会话历史管理
- Chat 对话框、引用来源卡片

### Week 5：文档处理 Pipeline

- PDF/DOCX/TXT 解析，Chunk 切分（fixed + recursive）
- DashScope Embedding → Qdrant 向量存储
- 处理流程编排（parse → chunk → embed → Qdrant → FTS）
- 前端处理按钮 + 状态轮询

### Week 4：数据库 + JWT + 搜索

- SQLite + SQLAlchemy ORM
- JWT 认证 + bcrypt 密码哈希
- PyMuPDF PDF 解析 + 状态流转
- FTS5 全文搜索 + snippet 高亮

### Week 3：Element Plus 统一

- 6 个页面 EP 化，搜索+分页联动，拖拽文件上传
- 面包屑导航、loading/空状态

### Week 2：知识库 CRUD

- 新建/列表/详情，文档列表/上传

### Week 1：项目骨架

- 登录、dashboard、后端 mock

## Out of Scope For The Next Iteration

- 项目 1 新增功能（知识库复制/移动、Markdown 渲染增强、异步文档处理等）
- 多租户 / 权限模型
- CI/CD 和云基础设施
- 多 Provider Agent 工具链

## Default Verification

- frontend changes: `make frontend-build`
- backend changes: `make backend-test`
- changes spanning both: `make check`

## Working Rules

- Default code edit scope is this app directory, not the week-plan markdown files in the repo root.
- Keep route, schema, and service responsibilities separated.
- Update this roadmap when priorities or acceptance criteria change materially.
- Week 9+ targets Project 2 — a separate codebase.
