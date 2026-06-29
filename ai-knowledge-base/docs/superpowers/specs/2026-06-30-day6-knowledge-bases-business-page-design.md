# Day 6 Knowledge Bases Business Page Design

## Goal

让知识库页面从“前端占位表格”升级成第一次具备真实业务感的页面：前端通过真实后端接口获取知识库列表，并在页面中渲染结果、处理加载态和空状态。

## Scope

本次设计聚焦知识库列表页的第一次真实业务联调。

包含：

- 后端增加 `GET /api/knowledge-bases`
- 前端增加知识库接口封装
- `KnowledgebasesView.vue` 改为接口驱动渲染
- 表格字段对齐后端返回结构
- 增加 loading 状态
- 增加 empty 状态
- 保留“新建知识库”按钮作为后续扩展入口

不包含：

- 新建知识库弹窗
- 编辑知识库
- 删除知识库
- 搜索接口
- 分页接口
- 数据库存储
- 上传文档流程

## Current State

当前项目状态：

- 前端知识库页已经有静态页面结构
- 页面中已有：
  - 标题
  - 搜索框
  - 新建按钮
  - 表格
- 但当前表格数据仍为前端本地常量
- 后端还没有 `GET /api/knowledge-bases`

这意味着 Day 6 的核心不是再搭页面壳子，而是把知识库页第一次真正接上业务数据。

## Chosen Approach

采用“最小可扩展业务页”方案：

1. 后端新增知识库列表 mock 接口
2. 前端新增知识库接口请求封装
3. 知识库页面改为真实请求接口
4. 页面增加 loading / empty 状态

### Why

这个方案有三个优点：

1. 完整符合 Day 6 的任务目标
2. 让知识库页第一次摆脱“纯静态占位”
3. 不会把复杂度提前拉到搜索、分页、弹窗和数据库

## Data Contract

Day 6 的知识库数据结构统一为：

```json
{
  "id": 1,
  "name": "产品知识库",
  "description": "产品文档与FAQ",
  "document_count": 3,
  "created_at": "2026-06-28 20:00:00"
}
```

统一响应格式仍沿用 Day 4 的后端约定：

```json
{
  "code": 0,
  "message": "ok",
  "data": []
}
```

## Backend Design

后端新增知识库路由模块。

建议文件：

```text
backend/app/api/routes/knowledge_bases.py
backend/app/schemas/knowledge_base.py
```

### Responsibilities

- `knowledge_bases.py`
  - 提供 `GET /api/knowledge-bases`
  - 返回 mock 列表数据

- `knowledge_base.py`
  - 定义单条知识库模型
  - 供接口响应使用

### Endpoint

`GET /api/knowledge-bases`

响应示例：

```json
{
  "code": 0,
  "message": "ok",
  "data": [
    {
      "id": 1,
      "name": "产品知识库",
      "description": "产品文档与FAQ",
      "document_count": 3,
      "created_at": "2026-06-28 20:00:00"
    }
  ]
}
```

Day 6 阶段返回固定 mock 数据即可，不接数据库。

## Frontend Design

前端新增接口文件：

```text
frontend/src/api/knowledge-bases.ts
```

### Responsibilities

- `knowledge-bases.ts`
  - 封装 `getKnowledgeBases()`

- `KnowledgebasesView.vue`
  - 请求列表接口
  - 管理页面加载和空数据状态
  - 渲染真实返回列表

## Page Structure

知识库页面保持当前后台工具风格，结构继续沿用已有页面骨架：

1. 页面标题与说明
2. 搜索框与“新建知识库”按钮
3. 数据表格
4. 辅助说明 / 状态区域

## Table Columns

Day 6 表格字段应调整为：

1. 名称
2. 描述
3. 文档数量
4. 创建时间
5. 操作

说明：

- 当前静态页面里的“状态”与“更新时间”字段应让位给本次接口约定
- “操作”列仍保留“查看”“编辑”这类占位动作即可

## UI States

Day 6 至少要有这 3 种状态：

### 1. Loading

- 页面首次请求列表时显示加载提示
- 可以是轻量文本，也可以是表格区域占位文案

### 2. Success

- 表格渲染后端返回数据

### 3. Empty

- 当 `data` 为空数组时，显示空状态提示

## Search and Create Button

Day 6 阶段：

- 搜索框只保留 UI，不接真实筛选逻辑
- “新建知识库”按钮只保留视觉入口，不打开弹窗

这样可以保证页面具备业务感，同时不把范围扩散。

## Error Handling

Day 6 只做最小错误处理：

- 请求失败时可显示一条简单错误提示
- 不做复杂重试机制
- 不引入全局错误系统

## Files To Create Or Modify

- Create: `ai-knowledge-base/backend/app/api/routes/knowledge_bases.py`
- Create: `ai-knowledge-base/backend/app/schemas/knowledge_base.py`
- Modify: `ai-knowledge-base/backend/app/main.py`
- Create: `ai-knowledge-base/frontend/src/api/knowledge-bases.ts`
- Modify: `ai-knowledge-base/frontend/src/views/KnowledgebasesView.vue`
- Modify: `ai-knowledge-base/frontend/src/style.css`

## Acceptance Criteria

满足以下条件即可视为 Day 6 设计达成：

- 后端存在 `GET /api/knowledge-bases`
- 前端知识库页请求真实接口
- 页面能渲染接口返回数据
- 页面具备 loading 状态
- 页面具备 empty 状态
- 页面整体具有明显业务感，不再只是静态模板

## Non Goals

以下内容明确不属于 Day 6：

- 新建知识库完整流程
- 搜索后端联动
- 分页
- 编辑删除真实行为
- 文档上传
- 向量化或 AI 能力接入
