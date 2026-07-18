from sqlalchemy import Column, DateTime, Integer, String, func

from app.core.database import Base


class ChatSession(Base):
    """聊天会话（归属某知识库）。"""

    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    knowledge_base_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False, default="新对话")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
