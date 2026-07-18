from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.core.database import Base


class ChatMessage(Base):
    """聊天消息（角色+内容）。"""

    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, nullable=False, index=True)
    role = Column(String(32), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
