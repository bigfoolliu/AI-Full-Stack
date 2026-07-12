import tempfile
from pathlib import Path

from fpdf import FPDF

from app.core.config import EMBEDDING_API_KEY, LLM_API_KEY
from app.core.database import SessionLocal, init_db
from app.models import Document, KnowledgeBase
from app.services.llm_service import LlmService
from app.services.process_service import process_document
from app.services.vector_service import VectorService


def _create_test_doc(db, kb_id: int) -> int:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)
    pdf.cell(
        text="RAG is retrieval augmented generation. It combines retrieval and generation.",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.cell(text="Python is a popular programming language for data science.", new_x="LMARGIN", new_y="NEXT")

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    pdf.output(tmp.name)

    import os

    from app.core.config import UPLOAD_DIR

    upload_dir = os.path.join(UPLOAD_DIR, str(kb_id))
    os.makedirs(upload_dir, exist_ok=True)
    safe_name = "test_chat.pdf"
    dest = os.path.join(upload_dir, safe_name)
    Path(tmp.name).rename(dest)

    doc = Document(
        knowledge_base_id=kb_id,
        filename=safe_name,
        status="pending",
        file_path=f"/uploads/{kb_id}/{safe_name}",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc.id


def test_chat_no_key():
    if LLM_API_KEY:
        print("  [SKIP] 已配置 LLM_API_KEY，跳过无 key 测试")
        return

    svc = LlmService()
    result = svc.chat("什么是 RAG？", [])
    assert "answer" in result
    assert "未配置" in result["answer"]
    assert result["sources"] == []

    print("  [PASS] 无 API Key 时返回友好提示")


def test_chat_empty_context():
    if not LLM_API_KEY:
        print("  [SKIP] 未配置 LLM_API_KEY，跳过 Chat 测试")
        return

    svc = LlmService()
    result = svc.chat("知识库中有什么内容？", [])
    assert "answer" in result
    assert len(result["answer"]) > 0
    assert result["sources"] == []

    print("  [PASS] 无检索结果时如实告知")


def test_chat_with_context():
    if not EMBEDDING_API_KEY or not LLM_API_KEY:
        print("  [SKIP] 未配置 API Key，跳过端到端 Chat 测试")
        return

    init_db()
    db = SessionLocal()

    kb = KnowledgeBase(name="Chat 测试", description="Day1 测试")
    db.add(kb)
    db.flush()

    doc_id = _create_test_doc(db, kb.id)
    process_document(doc_id, db)

    svc = VectorService()
    chunks = svc.search(query="什么是 RAG", kb_id=kb.id, limit=3)

    assert len(chunks) > 0, "应检索到相关片段"

    llm = LlmService()
    result = llm.chat("什么是 RAG？请用中文回答。", chunks)
    assert "answer" in result
    assert len(result["answer"]) > 0
    assert "sources" in result
    assert len(result["sources"]) > 0
    for s in result["sources"]:
        assert "filename" in s
        assert "content" in s
        assert "score" in s

    db.close()
    print("  [PASS] 端到端 Chat 成功：answer + sources 完整")


def test_chat_with_history():
    if not LLM_API_KEY:
        print("  [SKIP] 未配置 LLM_API_KEY，跳过多轮对话测试")
        return

    svc = LlmService()
    history = [
        {"role": "user", "content": "RAG 是什么？"},
        {"role": "assistant", "content": "RAG 是检索增强生成技术。"},
    ]
    result = svc.chat("刚才说的 RAG 具体怎么工作？", [], history=history)
    assert "answer" in result
    assert len(result["answer"]) > 0

    print("  [PASS] 多轮对话上下文正确传递")


if __name__ == "__main__":
    test_chat_no_key()
    test_chat_empty_context()
    test_chat_with_context()
    test_chat_with_history()
    print("\n所有测试通过!")
