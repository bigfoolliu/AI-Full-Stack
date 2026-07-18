import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.knowledge_bases import router as knowledge_bases_router
from app.core.config import ALLOWED_ORIGINS, APP_NAME, JWT_SECRET, UPLOAD_DIR
from app.core.database import init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动时初始化数据库，关闭时清理。"""
    if JWT_SECRET == "super-secret-key-change-in-production":
        logger.warning("JWT_SECRET 使用默认值，请设置环境变量 JWT_SECRET 以保障生产环境安全")
    init_db()
    yield


app = FastAPI(title=APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(knowledge_bases_router)
