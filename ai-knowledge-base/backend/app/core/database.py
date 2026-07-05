from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def init_db():
    from app.models import Base, Document, KnowledgeBase, User

    Base.metadata.create_all(bind=engine)

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
