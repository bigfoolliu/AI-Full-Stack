# Shell User Login Entry Design

## Goal

让后台壳子右上角的用户区成为一个明确的登录入口，点击后跳转到 `/login`。

## Scope

本次改动只覆盖以下内容：

- `frontend/src/App.vue`
- `frontend/src/style.css`

不处理以下内容：

- 登录态判断
- 退出登录
- 权限控制
- 登录页内容修改

## Chosen Approach

采用 `RouterLink` 包裹整个用户区，而不是在普通 `div` 上绑定点击事件。

原因：

- 语义更自然
- 路由跳转实现更简单
- 自带更好的键盘可访问性
- 能继续沿用现有后台壳子结构

## Interaction

用户点击右上角用户区时：

1. 触发路由跳转
2. 进入 `/login`

用户区在视觉上应表现为可点击：

- hover 时有轻微背景反馈
- focus 时有明显可见的聚焦态
- 保持原有头像、姓名和说明文案结构

## Acceptance

满足以下条件即可认为达成：

- 右上角用户区可点击
- 点击后进入 `/login`
- 构建通过
- 视觉风格与当前后台壳子一致
