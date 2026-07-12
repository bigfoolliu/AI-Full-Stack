import os
import tempfile
from pathlib import Path

from fpdf import FPDF

from app.core.config import EMBEDDING_API_KEY, UPLOAD_DIR
from app.core.database import SessionLocal, init_db
from app.models import Document, KnowledgeBase
from app.services.process_service import process_document
from app.services.vector_service import VectorService


def setup_kb_and_doc(db) -> tuple[int, str]:
    kb = KnowledgeBase(name="测试知识库", description="Day4 测试")
    db.add(kb)
    db.flush()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)
    for i in range(20):
        pdf.cell(text=f"This is line {i} of process test document. ", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(
        text="RAG is a technique that combines retrieval and generation.",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    pdf.output(tmp.name)

    upload_dir = os.path.join(UPLOAD_DIR, str(kb.id))
    os.makedirs(upload_dir, exist_ok=True)
    safe_name = "test_process.pdf"
    dest = os.path.join(upload_dir, safe_name)
    Path(tmp.name).rename(dest)

    from app.models import Document

    doc = Document(
        knowledge_base_id=kb.id,
        filename="test_process.pdf",
        status="pending",
        file_path=f"/uploads/{kb.id}/{safe_name}",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return doc.id, dest


def test_upload_sets_pending():
    init_db()
    db = SessionLocal()
    doc_id, _ = setup_kb_and_doc(db)

    doc = db.query(Document).filter(Document.id == doc_id).first()
    assert doc.status == "pending", f"上传后应为 pending，实际为 {doc.status}"

    db.close()
    print("  [PASS] 上传后 status = pending")


def test_process_document_success():
    init_db()
    db = SessionLocal()
    doc_id, file_path = setup_kb_and_doc(db)

    doc = process_document(doc_id, db)
    assert doc.status == "completed", f"处理后应为 completed，实际为 {doc.status}"
    assert doc.content and len(doc.content) > 0, "处理后应有文本内容"
    assert "RAG" in doc.content, "内容应包含原文本"

    db.close()
    print("  [PASS] 处理成功：status = completed，文本内容正确")


def test_process_document_updates_fts():
    init_db()
    db = SessionLocal()
    doc_id, _ = setup_kb_and_doc(db)

    process_document(doc_id, db)

    from app.services.search_service import search_documents

    doc = db.query(Document).filter(Document.id == doc_id).first()
    results = search_documents(db, kb_id=doc.knowledge_base_id, keyword="RAG")
    assert results.total > 0, f"FTS 应返回结果，实际 {results.total}"
    assert any("RAG" in r.snippet for r in results.items)

    db.close()
    print("  [PASS] FTS 索引正确，搜索 'RAG' 返回结果")


def test_process_document_with_vector():
    if not EMBEDDING_API_KEY:
        print("  [SKIP] 未设置 DASHSCOPE_API_KEY，跳过向量化验证")
        return

    init_db()
    db = SessionLocal()
    doc_id, _ = setup_kb_and_doc(db)

    process_document(doc_id, db)
    doc = db.query(Document).filter(Document.id == doc_id).first()

    svc = VectorService()
    results = svc.search("RAG generation", kb_id=doc.knowledge_base_id, limit=5)
    assert len(results) > 0, "向量搜索应返回结果"
    assert any("RAG" in r["content"] for r in results)

    db.close()
    print("  [PASS] Qdrant 向量入库正确，语义搜索返回结果")


def test_process_document_idempotent():
    if not EMBEDDING_API_KEY:
        print("  [SKIP] 未设置 DASHSCOPE_API_KEY，跳过幂等测试")
        return

    init_db()
    db = SessionLocal()
    doc_id, _ = setup_kb_and_doc(db)

    process_document(doc_id, db)
    svc = VectorService()
    results_before = svc.search("RAG", kb_id=1, limit=100)
    count_before = len(results_before)

    process_document(doc_id, db)
    results_after = svc.search("RAG", kb_id=1, limit=100)
    count_after = len(results_after)

    assert count_after == count_before, f"重复处理应更新而非叠加 (before={count_before}, after={count_after})"

    db.close()
    print("  [PASS] 重复调用幂等，旧 chunks 被正确替换")


def test_process_document_parse_failure():
    init_db()
    db = SessionLocal()

    doc = Document(
        knowledge_base_id=1,
        filename="invalid.xyz",
        status="pending",
        file_path="/uploads/1/nonexistent.txt",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    try:
        process_document(doc.id, db)
    except Exception:
        pass

    db.refresh(doc)
    assert doc.status == "failed", f"解析失败后应为 failed，实际为 {doc.status}"
    assert doc.content, "失败时 content 应包含错误信息"

    db.close()
    print("  [PASS] 解析失败：status = failed，错误信息已记录")


if __name__ == "__main__":
    test_upload_sets_pending()
    test_process_document_success()
    test_process_document_updates_fts()
    test_process_document_with_vector()
    test_process_document_idempotent()
    test_process_document_parse_failure()
    print("\n所有测试通过!")
