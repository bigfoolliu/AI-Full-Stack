# Backend

Day 4 的后端目标是给前端提供最小 mock 用户服务，支撑第一次真实联调。

## Run

在 `backend/` 目录下运行：

```bash
python main.py
```

或：

```bash
uv run uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`
- `POST /api/login`
- `GET /api/me`

## Mock Login

当前固定账号密码：

- `username`: `admin`
- `password`: `123456`
