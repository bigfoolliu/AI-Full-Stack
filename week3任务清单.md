# Week 3 任务清单

## 1. 本周目标

第 3 周的目标不是加新业务功能，而是把第 1-2 周手写的前端 UI 全面升级为 Element Plus 组件风格，并补上搜索/分页/上传组件这些后台常用交互能力。

到本周结束时，你应该具备以下成果：

- 所有手写表格已替换为 Element Plus `ElTable`
- 所有手写表单已替换为 Element Plus `ElForm`
- 上传页已替换为 Element Plus `ElUpload`
- 知识库列表支持搜索和分页
- 所有交互提示已统一为 `ElMessage`
- 页面 UI 风格一致、交互体验完整

这一周的唯一目标可以概括为：

**让项目从"能用的后台雏形"升级为"像样的后台产品"。**

---

## 2. 本周完成标准

如果这一周结束时，你能做到以下几点，就算顺利完成：

- [ ] 知识库列表使用 Element Plus 表格渲染
- [ ] 新建知识库页使用 Element Plus 表单 + 验证
- [ ] 上传页使用 Element Plus 上传组件
- [ ] 知识库列表支持搜索（前端 + 后端配合）
- [ ] 知识库列表支持分页
- [ ] 错误/成功提示全部使用 `ElMessage`
- [ ] Dashboard / 文档列表等页面也完成了 Element Plus 化
- [ ] README 里已经补充第 3 周完成内容与下周计划

---

## 3. 本周项目范围

这一周保持"前端 UI 升级 + 交互补全"，不涉及数据库替换和后端重构。

### 3.1 页面范围

6 个页面全部覆盖，重点改造 3 个：

1. 知识库列表页 `/knowledge-bases` — 表格 + 分页 + 搜索
2. 新建知识库页 `/knowledge-bases/create` — 表单
3. 文档上传页 `/knowledge-bases/:id/upload` — 上传组件
4. 文档列表 / 状态页 `/knowledge-bases/:id/documents` — 表格 + 标签
5. 工作台 `/dashboard` — 卡片 + 列表
6. 登录页 `/login` — 保持统一风格

### 3.2 接口范围

本周对后端接口做最小扩展，不引入数据库：

1. `GET /api/knowledge-bases` — 新增 `keyword`、`page`、`page_size` 查询参数
2. `GET /api/knowledge-bases/{id}/documents` — 新增 `status` 筛选参数
3. `POST /api/knowledge-bases/{id}/documents` — 升级为真实 `UploadFile` 文件上传

其余接口保持不动。

### 3.3 学习范围

只围绕这些知识点学：

- Element Plus Table 组件
- Element Plus Form 组件 + 表单验证
- Element Plus Upload 组件
- Element Plus Pagination 分页
- Element Plus Message / Notification
- Element Plus Tag / Button / Card
- Vue 3 组件封装思路
- FastAPI 文件上传（`UploadFile`）
- 前后端搜索/分页联调

---

## 4. 推荐目录结构

保持现有目录结构不变，本周主要改动在已有文件内部：

```text
frontend/src/
  views/          # 改造已有 6 个页面
  api/            # 新增/修改接口参数
  router/         # 无需改动
  stores/         # 无需改动
```

---

## 5. 每日执行清单

## Day 1：Element Plus 表格 + 消息提示

### 目标

把最显眼的知识库列表页从手写表格升级为 Element Plus 表格，并统一消息提示。

### 任务清单

- [x] 检查并确保 Element Plus 已全局注册（main.ts）
- [x] 用 `ElTable` + `ElTableColumn` 替换 `KnowledgeBasesView.vue` 的手写 `<table>`
- [x] 用 `ElButton` 替换手写按钮
- [x] 用 `ElMessage` 替换所有页面中的手写错误/成功提示
- [x] 用 `ElTag` 替换文档状态标签
- [x] 用 `ElCard` 替换页面中的卡片容器样式

### 今日输出

- 知识库列表使用 Element Plus 表格组件
- 所有页面的消息提示统一为 `ElMessage`
- 按钮样式统一为 Element Plus

### 验收标准

- [ ] 知识库列表渲染正常，样式是 Element Plus 风格
- [ ] 创建知识库成功/失败后有 ElMessage 弹窗
- [ ] 文档列表状态显示 ElTag

---

## Day 2：Element Plus 表单 + 分页

### 目标

把新建知识库页升级为 Element Plus 表单，并为列表页增加分页能力。

### 任务清单

- [ ] 用 `ElForm` + `ElFormItem` + `ElInput` 替换 `KnowledgeBaseCreateView.vue` 手写表单
- [ ] 用 `ElForm` 内置验证规则替换手写验证
- [ ] 为知识库列表页增加 `ElPagination` 分页组件
- [ ] 后端 `GET /api/knowledge-bases` 支持 `page`、`page_size` 参数
- [ ] 前端分页逻辑与后端参数联动

### 今日重点

表单验证和分页逻辑是后台系统最常用的交互能力。

### 验收标准

- [ ] 新建知识库表单使用 Element Plus，验证规则正常
- [ ] 知识库列表底部分页组件可用，翻页后数据变化

---

## Day 3：Element Plus 上传组件 + 真实文件上传

### 目标

把上传页从手写 `<input type="file">` 升级为 Element Plus Upload，并打通后端真实文件存储。

### 任务清单

- [ ] 用 `ElUpload` 替换 `KnowledgeBaseUploadView.vue` 的手写文件选择区域
- [ ] 配置 `ElUpload` action 指向后端上传端点
- [ ] 后端 `POST /api/knowledge-bases/{id}/documents` 改为接收 `UploadFile`
- [ ] 后端将上传文件保存到本地 `uploads/` 目录
- [ ] 上传成功后返回文档记录，前端显示上传结果
- [ ] 上传页增加进度提示和上传成功/失败状态

### 今日重点

这是文件上传第一次真正落地，ElUpload 的配置和后端 UploadFile 处理是核心。

### 验收标准

- [ ] 上传页使用 Element Plus Upload 组件
- [ ] 选择文件后可点击上传，后端保存文件到磁盘
- [ ] 上传成功后有明确反馈

---

## Day 4：搜索 / 筛选功能

### 目标

让知识库列表页的搜索框真正可用，文档列表页增加状态筛选。

### 任务清单

- [ ] 前端搜索框绑定 `v-model`，输入后触发查询
- [ ] 后端 `GET /api/knowledge-bases` 支持 `keyword` 查询参数（按名称/描述过滤）
- [ ] 搜索时带上 loading 状态
- [ ] 文档列表页增加状态筛选下拉（`ElSelect` + `ElOption`）
- [ ] 后端 `GET /api/knowledge-bases/{id}/documents` 支持 `status` 筛选参数
- [ ] 搜索和筛选与分页联动

### 验收标准

- [ ] 在搜索框输入后，知识库列表按关键词过滤
- [ ] 选择文档状态筛选后，文档列表按状态过滤
- [ ] 搜索/筛选和分页同时使用时逻辑正确

---

## Day 5：剩余页面 Element Plus 化

### 目标

把工作台页、文档列表页改造为 Element Plus 风格，保持 UI 一致性。

### 任务清单

- [ ] 用 `ElCard` + `ElStatistic`（或近似组件）替换 Dashboard 手写卡片
- [ ] 用 `ElTable` 替换文档列表页手写表格
- [ ] 用 `ElTag` 统一替换所有状态标签样式
- [ ] 用 `ElButton` 统一替换所有操作按钮
- [ ] 检查 6 个页面的间距、字体、颜色是否统一
- [ ] 登录页保持简洁，与后台风格协调

### 验收标准

- [ ] 工作台页面使用 Element Plus 组件，风格统一
- [ ] 文档列表页使用 Element Plus 表格
- [ ] 6 个页面视觉风格无明显差异

---

## Day 6：交互打磨

### 目标

补充后台常用交互细节，提升使用体验。

### 任务清单

- [ ] 为列表页增加 `ElBreadcrumb` 面包屑导航
- [ ] 完善 loading 状态（使用 `ElLoading` 或 `v-loading`）
- [ ] 完善空状态展示（使用 `ElEmpty`）
- [ ] 完善错误状态展示（使用 `ElAlert`）
- [ ] 创建知识库成功后跳转到文档列表页
- [ ] 上传文档成功后跳转到文档列表页
- [ ] 优化页面标题和说明文字

### 今日重点

交互细节决定一个后台项目是否"像个产品"。

### 验收标准

- [ ] 加载数据时有 loading 反馈
- [ ] 数据为空时有空状态提示
- [ ] 创建/上传成功后自动跳转
- [ ] 页面有面包屑或导航指示

---

## Day 7：整理、复盘、封版

### 目标

不要继续加功能，把第 3 周成果整理成一个干净的里程碑版本。

### 任务清单

- [ ] 检查所有页面 Element Plus 组件使用是否一致
- [ ] 检查搜索/分页/上传功能是否正常
- [ ] 补全 README 中第 3 周完成内容
- [ ] 为已改造页面保留新截图
- [ ] 记录本周完成内容
- [ ] 记录下周任务清单
- [ ] 提交一个阶段性版本

### README 第三版至少要包含

1. 当前技术栈（可标注 Element Plus 已全面落地）
2. 当前业务页面说明
3. 本周新增搜索/分页/上传能力
4. 当前接口清单
5. 本地启动方式
6. 下周计划

### 验收标准

- [ ] 项目已全面使用 Element Plus 组件，风格统一
- [ ] 所有交互反馈不再依赖手写样式
- [ ] 搜索/分页/上传三项能力完整可用
- [ ] README 已更新到第 3 周阶段

---

## 6. 本周接口清单汇总

第 3 周主要在已有接口基础上扩展参数：

1. `GET /api/knowledge-bases` — 新增 `keyword`、`page`、`page_size` 查询参数
2. `GET /api/knowledge-bases/{id}/documents` — 新增 `status` 筛选参数
3. `POST /api/knowledge-bases/{id}/documents` — 升级为 `UploadFile` 真实文件上传

---

## 7. 本周页面清单汇总

第 3 周改造已有 6 个页面，不新增页面：

1. 登录页 `/login` — 风格微调
2. 工作台 `/dashboard` — ElCard 替换
3. 知识库列表页 `/knowledge-bases` — ElTable + ElPagination + 搜索
4. 新建知识库页 `/knowledge-bases/create` — ElForm
5. 文档列表 / 状态页 `/knowledge-bases/:id/documents` — ElTable + ElTag
6. 文档上传页 `/knowledge-bases/:id/upload` — ElUpload

---

## 8. 本周知识点清单汇总

本周只围绕这些技术学习：

- Element Plus Table
- Element Plus Form + 验证
- Element Plus Upload
- Element Plus Pagination
- Element Plus Message / Notification
- Element Plus Tag / Button / Card / Empty / Breadcrumb
- FastAPI UploadFile 文件上传
- 前后端搜索/分页/筛选联调

---

## 9. 本周完成后的状态

如果你能完成这份清单，第 3 周结束时你将拥有：

- 一个全面使用 Element Plus 的现代化后台 UI
- 具备搜索、分页、筛选能力的知识库列表
- 一个可用的文件上传功能
- 一致的交互反馈（loading、empty、error、message）
- 一个比第 2 周更像"产品"的项目版本

这一步很重要，因为它标志着你的项目会从"雏形"推进到"具备产品感的系统"。
