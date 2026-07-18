"""
数据库操作
"""

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def init_db():
    """初始化所有表、FTS 虚拟表及种子数据。"""
    from app.models import (  # noqa: F401
        Base,
        ChatFeedback,
        ChatMessage,
        ChatSession,
        Document,
        KnowledgeBase,
        KnowledgeBaseSetting,
        User,
    )

    Base.metadata.create_all(bind=engine)

    _migrate_kb_settings(engine)

    with engine.connect() as conn:
        conn.exec_driver_sql("""\
CREATE VIRTUAL TABLE IF NOT EXISTS document_fts USING fts5(
    doc_id UNINDEXED,
    kb_id UNINDEXED,
    filename,
    content,
    tokenize='unicode61'
)
""")
        conn.commit()

    session = SessionLocal()
    try:
        existing_user = session.query(User).filter(User.username == "admin").first()
        if not existing_user:
            from app.core.security import get_password_hash

            admin = User(
                username="admin",
                password_hash=get_password_hash("123456"),
                nickname="Admin",
            )
            session.add(admin)
            session.flush()

            kb1 = KnowledgeBase(name="员工手册", description="公司内部员工手册与规章制度")
            kb2 = KnowledgeBase(name="产品文档", description="产品技术文档与用户手册")
            kb3 = KnowledgeBase(name="项目管理", description="项目流程与最佳实践")
            session.add_all([kb1, kb2, kb3])
            session.flush()

            doc1 = Document(
                knowledge_base_id=kb1.id,
                filename="入职指南.pdf",
                status="pending",
                file_path="",
            )
            doc2 = Document(
                knowledge_base_id=kb1.id,
                filename="考勤制度.pdf",
                status="pending",
                file_path="",
            )
            doc3 = Document(
                knowledge_base_id=kb2.id,
                filename="API参考手册.pdf",
                status="pending",
                file_path="",
            )
            session.add_all([doc1, doc2, doc3])

        session.commit()
    finally:
        session.close()


def _migrate_kb_settings(engine):
    """为已有的 knowledge_base_settings 表补充 Week 8 新增的 chunk 列。"""
    inspector = inspect(engine)
    columns = {c["name"] for c in inspector.get_columns("knowledge_base_settings")}
    migrations = [
        ("chunk_size", "INTEGER NOT NULL DEFAULT 512"),
        ("overlap", "INTEGER NOT NULL DEFAULT 64"),
        ("chunk_strategy", "VARCHAR(16) NOT NULL DEFAULT 'recursive'"),
    ]
    with engine.connect() as conn:
        for col_name, col_type in migrations:
            if col_name not in columns:
                conn.exec_driver_sql(f"ALTER TABLE knowledge_base_settings ADD COLUMN {col_name} {col_type}")
        conn.commit()
