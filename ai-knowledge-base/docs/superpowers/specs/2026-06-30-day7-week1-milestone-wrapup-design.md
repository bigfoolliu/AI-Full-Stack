# Day 7 Week 1 Milestone Wrap-Up Design

## Goal

把第 1 周已经完成的成果整理成一个干净、可展示、可继续开发的里程碑版本，而不是继续往项目里堆功能。

## Scope

本次聚焦整理、复盘、封版。

包含：

- 检查目录结构是否清晰
- 检查页面与接口命名是否统一
- 补全项目根 README 第一版
- 记录本周完成内容
- 记录下周任务清单
- 说明需要保留的页面截图清单
- 给出阶段性封版建议

不包含：

- 新增业务功能
- 新增后端接口
- 再做页面重构
- 再扩展认证或知识库能力

## Why Day 7 Matters

前 6 天已经做完了：

- 登录页
- 后台壳子
- 工作台页
- 知识库页
- 登录联调
- 知识库列表联调
- 最小后端 mock 用户服务

如果 Day 7 不做整理，这一周的成果很容易变成“自己知道做了什么，但别人看不懂、下周回来也接得费劲”的状态。

Day 7 的价值不是开发速度，而是可维护性和可展示性。

## Chosen Approach

采用“里程碑封版”方案。

### Why

这个方案最适合当前阶段，因为它：

1. 符合第 1 周本来就应该收口的目标
2. 防止 Day 7 继续滑回功能开发
3. 能直接为下周继续做知识库功能打基础
4. 同时也方便未来做简历/作品集整理

## Current Project State

当前项目已经具备这几个模块：

### Frontend

- `/login`
- `/dashboard`
- `/knowledge-bases`
- `Pinia` 登录态
- axios 请求层
- 登录和用户接口联调
- 知识库列表接口联调

### Backend

- `GET /health`
- `POST /api/login`
- `GET /api/me`
- `GET /api/knowledge-bases`

### Docs

- 已有 Day 1 到 Day 6 的设计和执行计划文档
- 但项目根 README 仍未承担“对外说明项目”的职责

## Day 7 Deliverables

Day 7 的交付物建议包含 4 类：

### 1. 项目可读说明

最重要的是根 README 第一版：

- 项目简介
- 技术栈
- 当前已完成功能
- 项目目录结构
- 本地启动方式
- 本周接口清单
- 本周页面清单
- 下周计划

### 2. 项目结构说明

对当前目录进行最小清理判断：

- 哪些目录是项目结构的一部分
- 哪些目录只是本地开发产物

重点识别：

- `.venv`
- `node_modules`
- `dist`
- `.idea`
- `__pycache__`

这一步不一定要求删除，但至少要在 README 或整理计划中明确它们的角色。

### 3. 本周成果总结

建议整理成面向自己和他人都能读懂的列表：

- 前端完成了什么
- 后端完成了什么
- 已联调到什么程度
- 当前项目还处于什么阶段

### 4. 下周计划

明确 Week 2 的方向，避免下周回来重新找感觉。

建议重点包括：

- 知识库创建流程
- 列表操作联动
- 搜索/筛选
- 文档上传入口
- 更完整的后端业务接口

## README Design

根 README 是 Day 7 的第一优先级。

建议结构如下：

```text
1. 项目简介
2. 技术栈
3. 当前已完成功能
4. 项目目录结构
5. 本地启动方式
6. 本周接口清单
7. 本周页面清单
8. 下周计划
```

### README Style

- 面向第一次打开仓库的人
- 语言清晰直接
- 不写长篇背景故事
- 不写过多内部过程性废话
- 重点是“这是什么、做到哪了、怎么跑、接下来做什么”

## Screenshot Strategy

Day 7 不一定强制把截图文件提交进仓库，但应至少明确截图清单，方便阶段性展示。

建议保留：

- 登录页截图
- 工作台页截图
- 知识库列表页截图

如果截图不提交仓库，也应在 Day 7 输出里记录“建议保留哪些页面截图”。

## Naming Review

Day 7 应做一次轻量命名复核，重点看：

- 页面路径与视图文件名是否一致
- 接口路径是否清晰
- 前后端字段命名是否统一

重点关注：

- `knowledge-bases`
- `knowledge_base`
- `document_count`
- `created_at`

这一步只做检查与必要小修，不做大规模重构。

## Milestone Definition

如果满足下面这些条件，就可以把第 1 周视为一个稳定 milestone：

- 项目根 README 可读
- 前后端都能本地启动
- 页面和接口命名基本统一
- Week 1 的页面和接口边界清晰
- 下周计划明确

## Files To Create Or Modify

- Modify: `ai-knowledge-base/README.md`
- Optionally modify: `ai-knowledge-base/backend/README.md`
- Optionally modify: `ai-knowledge-base/frontend/README.md`
- Optionally review only: `.gitignore`, 目录结构、命名一致性

## Acceptance Criteria

满足以下条件即可认为 Day 7 设计达成：

- 项目能被别人快速理解
- 你自己下周回来不会忘记进度
- 第 1 周成果形成阶段性版本
- 没有在 Day 7 再继续扩散功能范围

## Non Goals

以下内容明确不在 Day 7：

- 新增功能开发
- 后端新增更多业务接口
- 前端新增交互逻辑
- 重新设计整套 UI
