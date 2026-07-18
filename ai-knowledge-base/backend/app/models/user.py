"""
用户模型
"""

from sqlalchemy import Column, DateTime, Integer, String, func

from app.core.database import Base


class User(Base):
    """系统用户（登录认证）。"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    nickname = Column(String(64), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
