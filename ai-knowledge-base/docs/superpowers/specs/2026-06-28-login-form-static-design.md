# Login Form Static Design

## Goal

把 `/login` 页面从简单标题替换成一个可输入的静态登录表单，让从后台壳子跳转到登录页的链路完整可见。

## Scope

本次只做登录页静态表单，不做登录逻辑。

包含：

- 页面标题
- 简短说明
- 用户名输入框
- 密码输入框
- 登录按钮

不包含：

- 跳转到 `/dashboard`
- 表单校验
- 接口请求
- token 存储
- 路由守卫

## Layout

登录页保持当前项目的安静后台风格，不做营销页样式。

结构：

1. 页面容器
2. 居中登录卡片
3. 卡片标题和说明
4. 表单区域
5. 底部辅助提示

## Interaction

- 用户名和密码输入框可正常输入
- 登录按钮可见且可点击
- 按钮本次不触发任何提交逻辑

## Styling

- 维持和后台壳子一致的配色语言
- 卡片使用白底、轻边框、柔和阴影
- 输入框和按钮尺寸统一
- 页面整体阅读方向清晰，不堆过多元素

## Files To Modify

- Modify: `ai-knowledge-base/frontend/src/views/LoginView.vue`
- Modify: `ai-knowledge-base/frontend/src/style.css`

## Acceptance

- `/login` 不再只显示一个标题
- 页面具备真实登录表单外观
- 输入框可输入
- 构建通过
