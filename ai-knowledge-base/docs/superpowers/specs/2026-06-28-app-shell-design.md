# App Shell Design

## Goal

把 `frontend/src/App.vue` 从简单链接列表改成 Day 2 所需的最小后台壳子，承载 `/dashboard` 和 `/knowledge-bases` 两个后台页面。

## Scope

本次设计只覆盖后台壳子本身，不处理以下内容：

- 登录页独立布局
- Pinia 登录态
- 路由守卫
- 后端接口联调
- Element Plus 深度接入

## Chosen Direction

采用方案 A：经典后台壳子。

页面结构如下：

1. 左侧固定菜单
2. 顶部栏
3. 主内容区
4. `RouterView` 在主内容区内渲染

## Layout Structure

`App.vue` 负责全局壳子，不承担具体业务内容。

布局分为两列：

- 左列：深色侧边栏，展示系统名称和主导航
- 右列：浅色工作区，顶部显示当前页面标题和用户占位信息，下方显示页面内容

整体结构：

```text
App Shell
├─ Sidebar
│  ├─ Brand
│  └─ Nav Links
└─ Workspace
   ├─ Topbar
   └─ Main Content
      └─ RouterView
```

## Navigation

壳子内保留最小菜单项：

- `工作台` -> `/dashboard`
- `知识库` -> `/knowledge-bases`

`首页` 和 `关于` 不再作为后台主导航重点展示。

当前激活菜单应有明显高亮，依赖 `RouterLink` 的激活状态类完成。

## Topbar

顶部栏展示最小必要信息：

- 当前页面标题
- 右侧用户占位信息，例如 `刘同学`

页面标题根据当前路由计算：

- `/dashboard` -> `工作台`
- `/knowledge-bases` -> `知识库`
- 其他路由 -> `AI 知识库`

## Visual Style

视觉目标是“安静、专业、像后台工具”，不延续当前模板页风格。

约束如下：

- 侧边栏使用深色背景
- 工作区使用浅色背景
- 内容左对齐，不使用居中展示布局
- 标题层级清晰，避免过大的展示型字号
- 导航与顶部栏有清晰分隔
- 保持实现简单，不引入复杂装饰

## Router Behavior

`App.vue` 先作为全局壳子承载所有页面。

考虑到当前用户明确选择“最小后台壳子”，本次不拆登录页特殊布局。也就是说：

- `/dashboard` 和 `/knowledge-bases` 会直接受益于新壳子
- `/login` 当前也会落在壳子内，但这属于当前阶段接受的临时状态

后续 Day 3 或后续重构时，再把登录页从后台壳子中分离出去。

## Files To Modify

- Modify: `ai-knowledge-base/frontend/src/App.vue`
- Modify: `ai-knowledge-base/frontend/src/style.css`

如需让导航更干净，也可以在实现阶段顺带删除 `App.vue` 中旧的 `/`、`/about` 链接展示。

## Testing

完成后至少验证以下几点：

1. 页面能正常渲染新的左右布局
2. 可以点击进入 `/dashboard`
3. 可以点击进入 `/knowledge-bases`
4. 当前菜单项会高亮
5. 顶部标题会随当前路由变化
6. `RouterView` 内容出现在主内容区

## Non-Goals

以下内容即使看起来相关，也不在这次实现里：

- 组件拆分为 `Sidebar`、`Topbar` 单独文件
- 引入设计系统
- 重构所有视图页面样式
- 修复所有全局样式历史遗留问题

## Acceptance

满足以下条件即可认为这次设计达成：

- `App.vue` 不再是简单链接列表
- 前端看起来像一个后台系统骨架
- `dashboard` 和 `knowledge-bases` 能在壳子内容区中切换
- 代码改动范围小，便于 Day 2 继续推进
