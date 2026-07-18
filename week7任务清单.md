## 1. 本周目标

第 7 周的目标是在 Week 6 的 RAG 问答闭环之上，做效果调优和可配置能力。

到本周结束时，你应该具备以下成果：

- 检索参数配置页（Top-k、相似度阈值）
- Prompt 配置页（系统指令模板可编辑）
- 模型参数配置页（temperature、max_tokens）
- Chunk 策略可配置（chunk_size、overlap、切分方式）
- Metadata Filter 与 Hybrid Search
- 回答反馈按钮（赞成/反对）
- 现有测试覆盖核心服务

这一周的唯一目标可以概括为：

**能调参数、能看效果、能配置 Prompt、项目不只是 demo。**

---

## 2. 本周完成标准

如果这一周结束时，你能做到以下几点，就算顺利完成：

- [x] 检索参数（Top-k、阈值）可在页面配置并生效
- [x] Prompt 系统指令可在页面编辑并持久化
- [x] 模型参数（temperature、max_tokens）可在页面配置
- [ ] Chunk 策略参数可配置（chunk_size、overlap、切分方式）
- [x] 知识库问答支持 Metadata Filter（按文档名/状态过滤）
- [x] 支持 Hybrid Search（关键词 + 语义融合）
- [x] 回答下方有"有用/无用"反馈按钮
- [x] 核心服务层有测试覆盖

---

## 3. 本周项目范围

这一周主要做效果调优与可配置能力，不要扩展到新项目。

### 3.1 页面范围

1. 知识库设置页 `/knowledge-bases/:id/settings`（新增）
2. Chat 对话页 `/knowledge-bases/:id/chat`（增加反馈按钮）
3. 文档列表页（检索参数配置入口）

### 3.2 接口范围

1. `GET /api/knowledge-bases/{id}/settings` — 获取知识库配置
2. `PUT /api/knowledge-bases/{id}/settings` — 更新知识库配置
3. `POST /api/knowledge-bases/{id}/chat` — 增加参数透传（top_k、temperature 等）
4. `POST /api/knowledge-bases/{id}/chat/feedback` — 提交回答反馈

### 3.3 学习范围

只围绕这些知识点学：

- Chunk 策略对比（fixed vs recursive）
- Top-k 与相似度阈值对效果的影响
- Hybrid Search（FTS + 向量融合）
- Metadata Filter 应用场景
- Rerank 概念
- Prompt 模板设计
- 模型参数（temperature、top_p、max_tokens）

---

## 4. 每日执行清单

## Day 1：检索参数配置 ✅

### 目标

将硬编码的检索参数开放到页面配置，实时生效。

### 任务清单

- [x] 创建 `knowledge_base_settings` 表（id, kb_id, top_k, similarity_threshold, updated_at）
- [x] 创建 `GET /api/knowledge-bases/{id}/settings` 接口
- [x] 创建 `PUT /api/knowledge-bases/{id}/settings` 接口
- [x] 创建知识库设置页 `/knowledge-bases/:id/settings`
- [x] 设置页表单：Top-k 滑块（1-20）、相似度阈值滑块（0-1）
- [x] Chat 接口读取知识库配置中的检索参数
- [x] 保存后即时生效

### 验收标准

- [x] 可在页面调整检索参数
- [x] 调整后 Chat 接口按新参数检索
- 参数持久化到数据库

---

## Day 2：Prompt 配置 ✅

### 目标

让系统指令（system prompt）可在页面编辑，不再硬编码在代码中。

### 任务清单

- [x] 表已预置 `system_prompt` 字段（Day 1 已创建）
- [x] 设置页增加系统指令编辑区（多行文本框 + 恢复默认按钮）
- [x] Chat/Stream 接口使用知识库自定义 system_prompt
- [x] 检索到的上下文自动追加到 prompt 末尾（无需模板变量）
- [x] 提供默认 Prompt 模板一键恢复

### 验收标准

- [x] 修改 system_prompt 后 Chat 接口按新 prompt 回答
- [x] 不配置时使用系统默认 prompt
- 包含变量提示，降低配置门槛

---

## Day 3：模型参数配置 ✅

### 目标

让 temperature、max_tokens、model 名称可在页面配置。

### 任务清单

- [x] 表已预置 `temperature`、`max_tokens`、`model_name` 字段（Day 1 已创建）
- [x] 设置页增加模型参数配置区域
- [x] temperature 滑块（0-2，步长 0.1）
- [x] max_tokens 数字输入（256-8192）
- [x] model_name 下拉选择（`GET /api/models` 接口返回可用模型列表）
- [x] Chat/Stream 接口使用自定义模型参数
- [x] 保存后即时生效

### 验收标准

- [x] 可在页面调整 temperature 和 max_tokens
- [x] Chat 接口使用新参数调用 LLM
- [x] 参数持久化到数据库

---

## Day 4：Metadata Filter 与 Hybrid Search ✅

### 目标

让检索支持按元数据过滤，同时实现关键词 + 语义混合检索。

### 任务清单

- [x] Qdrant search 支持 `filename` 过滤（payload 精确匹配）
- [x] Chat/Search 接口支持 `filter` 参数（`{"filename": "xxx.pdf"}`）
- [x] 实现 Hybrid Search：FTS5 关键词 + Qdrant 向量结果融合
- [x] 融合策略：归一化得分后按 alpha 加权排序
- [x] 设置页增加 Hybrid Search 开关与 `hybrid_alpha` 权重滑块
- [x] 向量 upsert 时记录文档 `status` 到 payload

### 验收标准

- [x] 可按文档名过滤检索范围
- [x] Hybrid Search 返回 FTS + 向量融合结果
- [x] 可在设置页开关和调权重

---

## Day 5：回答反馈

### 目标

让用户可以对 AI 回答做"有用/无用"评价，为后续效果评估积累数据。

### 任务清单

- [x] 创建 `chat_feedback` 表（id, session_id, message_id, feedback, comment, created_at）
- [x] 创建 `POST /api/knowledge-bases/{id}/chat/feedback` 接口
- [x] Chat 页面每条 AI 回复下方增加反馈按钮（👍 👎）
- [x] 点击后记录反馈，按钮变为已选状态
- [x] 可选填写反馈备注

### 验收标准

- 每条 AI 回复可点击"有用/无用"
- 反馈数据持久化到数据库
- 同一消息不可重复提交

---

## Day 6：Rerank 与效果对比

### 目标

引入 Rerank 概念，让检索结果排序更准确，同时提供效果对比能力。

### 任务清单

- [x] 了解 Rerank 基本原理与常见模型
- [x] （可选）接入 Rerank API（如 Cohere / BGE）
- [x] 设置页增加 Rerank 开关配置
- [x] 同一问题使用不同参数对比回答效果
- [x] 记录检索指标（检索命中数、得分分布、回答耗时）

### 验收标准

- 理解 Rerank 的作用
- 能对比不同参数下的回答效果
- 了解如何通过反馈数据优化

---

## Day 7：整理、复盘、封版

### 目标

把第 7 周成果整理成干净的里程碑版本。

### 任务清单

- [ ] 检查所有接口命名和返回格式是否统一
- [ ] 验证配置 → 检索 → Prompt → 问答 → 反馈全链路
- [ ] 补充 `docs/` 下的配置参数说明
- [ ] 更新 README，补充第 7 周新增功能
- [ ] 确保 `make check` 全部通过
- [ ] 记录下周任务清单（Week 8）

### 验收标准

- RAG 全链路可配置、可调优
- 配置页面可用，参数持久化生效
- 项目可被别人快速理解和使用
- 第 7 周有一个可展示、可继续开发的优化版本

---

## 5. 本周接口清单汇总

第 7 周新增以下接口：

1. `GET /api/knowledge-bases/{id}/settings` — 获取知识库配置
2. `PUT /api/knowledge-bases/{id}/settings` — 更新知识库配置
3. `POST /api/knowledge-bases/{id}/chat/feedback` — 提交回答反馈

## 6. 本周页面清单汇总

| 页面 | 路径 | 类型 |
|------|------|------|
| 知识库设置页 | `/knowledge-bases/:id/settings` | 新增 |
| Chat 对话页 | `/knowledge-bases/:id/chat` | 修改（增加反馈按钮） |
| 文档列表页 | `/knowledge-bases/:id/documents` | 修改（增加设置入口） |

## 7. 本周知识点清单汇总

本周只围绕这些技术学习：

- Chunk 策略对比（fixed vs recursive）
- Top-k 与相似度阈值调优
- Hybrid Search（FTS + 向量融合）
- Metadata Filter
- Rerank
- Prompt 模板设计
- 模型参数（temperature、top_p、max_tokens）
- 回答反馈收集与分析

## 8. 本周完成后的状态

如果你能完成这份清单，第 7 周结束时你将拥有：

- 一个可配置检索参数的 RAG 系统
- 一个可编辑 Prompt 的知识库问答系统
- 一个可调节模型参数的对话界面
- Hybrid Search 与 Metadata Filter 检索增强
- 回答反馈收集能力
- 一份更完善的项目文档和测试覆盖

这一步很重要，因为它标志着你已经从"做出 RAG 问答"进入到 **「RAG 系统调优与工程化阶段」**。
