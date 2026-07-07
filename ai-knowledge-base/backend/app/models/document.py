"""
文档模型
"""

from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    knowledge_base_id = Column(Integer, nullable=False, index=True)
    filename = Column(String(256), nullable=False)
    status = Column(String(32), default="pending")
    content = Column(Text, default="")
    file_path = Column(String(512), default="")
    created_at = Column(DateTime, server_default=func.now())
