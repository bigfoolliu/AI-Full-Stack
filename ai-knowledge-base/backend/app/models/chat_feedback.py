from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.core.database import Base


class ChatFeedback(Base):
    """聊天反馈（有用/无用）记录。"""

    __tablename__ = "chat_feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, nullable=False, index=True)
    message_id = Column(Integer, nullable=False, index=True)
    feedback = Column(String(16), nullable=False)
    comment = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
