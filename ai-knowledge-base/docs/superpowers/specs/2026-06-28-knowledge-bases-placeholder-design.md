# Knowledge Bases Placeholder Design

## Goal

把 `/knowledge-bases` 从单个标题改成 Day 2 所需的知识库列表占位页，完成前端后台页面骨架。

## Scope

本次只做静态占位页面，不接业务逻辑。

包含：

- 页面标题
- 页面说明
- 搜索输入框
- 新建知识库按钮
- 假数据表格
- 底部辅助说明

不包含：

- 实时搜索
- 分页
- 新建弹窗
- 接口请求
- 真实编辑/删除操作

## Layout

页面分为三个区域：

1. 头部说明区
2. 工具栏
3. 列表表格区

## Table Fields

表格使用静态假数据，字段如下：

- 知识库名称
- 文档数
- 状态
- 更新时间
- 操作

## Visual Style

沿用当前后台壳子的视觉语言：

- 左对齐信息结构
- 白色列表卡片
- 轻边框和轻阴影
- 搜索输入框和主按钮形成工具栏
- 状态字段有明显视觉区分

## Files To Modify

- Modify: `ai-knowledge-base/frontend/src/views/KnowledgebasesView.vue`
- Modify: `ai-knowledge-base/frontend/src/style.css`

## Acceptance

- 页面不再只显示一个标题
- 有搜索框和新建按钮
- 有假数据表格
- 构建通过
