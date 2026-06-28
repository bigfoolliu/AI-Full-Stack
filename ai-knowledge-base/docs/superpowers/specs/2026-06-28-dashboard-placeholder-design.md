# Dashboard Placeholder Design

## Goal

把 `/dashboard` 从单个标题补成一个真正的工作台占位页，完成 Day 2 的后台首页骨架。

## Scope

本次只做静态工作台页面，不接业务逻辑。

包含：

- 欢迎区
- 页面说明
- 统计卡片
- 最近更新占位区
- 待处理事项占位区

不包含：

- 图表
- 实时数据
- 接口请求
- 登录态联动
- 可编辑工作台模块

## Layout

页面分为三个层级：

1. 欢迎区
2. 统计卡片区
3. 双列内容区

## Content

建议展示以下静态内容：

- 统计卡片：
  - 知识库总数
  - 文档总数
  - 处理中任务
- 最近更新的知识库
- 今日待处理事项

## Visual Style

继续沿用当前后台壳子的工具感视觉：

- 左对齐内容
- 卡片承载信息
- 轻阴影和轻边框
- 信息密度中等，便于后续替换成真实数据

## Files To Modify

- Modify: `ai-knowledge-base/frontend/src/views/DashboardView.vue`
- Modify: `ai-knowledge-base/frontend/src/style.css`

## Acceptance

- `/dashboard` 不再只是一个标题
- 页面有欢迎区和统计区
- 页面有两个下方占位模块
- 构建通过
