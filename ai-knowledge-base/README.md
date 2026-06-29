# AI Knowledge Base

一个面向 AI 全栈转岗训练的最小知识库项目。当前阶段目标不是一次做全，而是按周推进，把前端、后端、联调和业务页一步步串成完整闭环。

## 项目简介

这个项目用于练习一个典型 AI 应用后台的基础能力：

- 登录页与后台壳子
- 前后端登录联调
- 知识库列表业务页
- 最小后端 mock 用户服务与业务列表接口

第 1 周重点是把“能跑起来的后台项目骨架”搭出来，而不是直接追求复杂 AI 能力。

## 技术栈

### Frontend

- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- Axios
- Element Plus（已安装）

### Backend

- FastAPI
- Pydantic
- Uvicorn

## 当前已完成功能

### 前端

- 登录页 `/login`
- 后台主布局（侧边栏 + 顶部栏）
- 工作台页 `/dashboard`
- 知识库列表页 `/knowledge-bases`
- 登录态管理与路由守卫
- 基于真实后端接口的登录联调
- 顶部栏显示后端返回的用户信息

### 后端

- `GET /health`
- `POST /api/login`
- `GET /api/me`
- `GET /api/knowledge-bases`
- 统一接口返回格式
- 基础 CORS
- 最小 mock 用户与知识库数据

### 联调情况

- 登录页已接入真实后端 `POST /api/login`
- 页面初始化可调用 `GET /api/me`
- 知识库页面已通过 `GET /api/knowledge-bases` 渲染真实接口返回的 mock 列表

## 项目目录结构

```text
ai-knowledge-base/
  frontend/   # Vue 3 前端项目
  backend/    # FastAPI 后端项目
  docs/       # 设计文档与执行计划
  README.md   # 项目总说明
```

### 说明

- `frontend/src/`：前端页面、路由、store、API 封装
- `backend/app/`：后端应用主入口、路由、schema、配置
- `docs/superpowers/`：按天整理的设计和执行计划文档

以下目录主要属于本地开发环境产物，不是项目核心成果本身：

- `frontend/node_modules/`
- `frontend/dist/`
- `backend/.venv/`
- `.idea/`
- `__pycache__/`

## 本地启动方式

### 启动后端

进入后端目录：

```bash
cd backend
```

推荐启动方式：

```bash
.venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 启动前端

进入前端目录：

```bash
cd frontend
```

启动开发服务器：

```bash
pnpm dev
```

## 本周接口清单

第 1 周完成了以下最小接口：

1. `GET /health`
2. `POST /api/login`
3. `GET /api/me`
4. `GET /api/knowledge-bases`

## 本周页面清单

第 1 周完成了以下页面：

1. 登录页 `/login`
2. 工作台页 `/dashboard`
3. 知识库列表页 `/knowledge-bases`

## 建议保留的截图

建议至少保留这 3 张页面截图，方便后续做周复盘、项目展示或简历整理：

1. 登录页
2. 工作台页
3. 知识库列表页

## 第 1 周完成内容总结

- 完成了前端后台骨架
- 完成了登录页和最小登录态管理
- 完成了前后端第一次真实登录联调
- 完成了知识库列表页的第一次真实接口渲染
- 完成了后端最小 mock 用户服务与知识库列表接口

第 1 周的项目已经从“模板工程”推进到“可继续扩展的业务后台基础版本”。

## 下周计划

Week 2 建议重点推进以下方向：

1. 知识库创建流程
2. 知识库搜索 / 筛选
3. 列表操作联动（查看 / 编辑）
4. 后端知识库 CRUD 雏形
5. 文档上传入口
6. 更完整的错误处理和页面状态管理

## 当前阶段定位

当前版本适合作为：

- 第 1 周阶段性里程碑
- 后续继续开发的稳定基础版本
- AI 全栈转岗过程中的练习项目雏形
