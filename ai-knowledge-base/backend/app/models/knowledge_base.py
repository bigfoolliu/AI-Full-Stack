"""
知识库模型
"""

from sqlalchemy import Column, DateTime, Integer, String, func

from app.core.database import Base


class KnowledgeBase(Base):
    """知识库（文档集合）。"""

    __tablename__ = "knowledge_bases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String(512), default="")
    created_at = Column(DateTime, server_default=func.now())
