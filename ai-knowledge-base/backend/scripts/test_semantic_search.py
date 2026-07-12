import os
import tempfile
from pathlib import Path

from fpdf import FPDF

from app.core.config import EMBEDDING_API_KEY
from app.core.database import SessionLocal, init_db
from app.models import Document, KnowledgeBase
from app.services.process_service import process_document
from app.services.vector_service import VectorService


def _make_pdf(path: str, lines: int = 5):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)
    for i in range(lines):
        pdf.cell(text=f"Line {i} of test document. ", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(text="RAG is retrieval augmented generation.", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(text="Python is a programming language.", new_x="LMARGIN", new_y="NEXT")
    pdf.output(path)


def _create_test_doc(db, kb_id: int, content_keyword: str) -> int:
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    _make_pdf(tmp.name)

    upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", str(kb_id))
    os.makedirs(upload_dir, exist_ok=True)
    safe_name = f"test_{content_keyword}.pdf"
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


def test_search_basic():
    if not EMBEDDING_API_KEY:
        print("  [SKIP] 未设置 DASHSCOPE_API_KEY，跳过语义搜索测试")
        return

    init_db()
    db = SessionLocal()

    kb = KnowledgeBase(name="语义搜索测试", description="Day5 测试")
    db.add(kb)
    db.flush()

    doc_id = _create_test_doc(db, kb.id, "rag")
    process_document(doc_id, db)

    svc = VectorService()
    results = svc.search(query="RAG generation", kb_id=kb.id, limit=5)

    assert len(results) > 0, "语义搜索应返回结果"
    r = results[0]
    assert r["doc_id"] == doc_id, f"doc_id 应匹配 ({r['doc_id']} != {doc_id})"
    assert "RAG" in r["content"], f"内容应包含 'RAG' ({r['content']})"
    assert r["score"] > 0, f"score 应大于 0 ({r['score']})"
    assert r["filename"] != "", "filename 不应为空"
    assert "page_number" in r, "应包含 page_number 字段"
    assert "chunk_index" in r, "应包含 chunk_index 字段"

    db.close()
    print("  [PASS] 语义搜索结果完整，含 doc_id/content/score/filename/page_number/chunk_index")


def test_search_kb_filter():
    if not EMBEDDING_API_KEY:
        print("  [SKIP] 未设置 DASHSCOPE_API_KEY，跳过 kb filter 测试")
        return

    init_db()
    db = SessionLocal()

    kb1 = KnowledgeBase(name="语义搜索 KB1", description="Day5 测试 KB1")
    kb2 = KnowledgeBase(name="语义搜索 KB2", description="Day5 测试 KB2")
    db.add_all([kb1, kb2])
    db.flush()

    doc1_id = _create_test_doc(db, kb1.id, "kb1")
    process_document(doc1_id, db)

    doc2_id = _create_test_doc(db, kb2.id, "kb2")
    process_document(doc2_id, db)

    svc = VectorService()

    results_kb1 = svc.search(query="RAG", kb_id=kb1.id, limit=10)
    for r in results_kb1:
        assert r["kb_id"] == kb1.id, f"KB1 过滤失效: doc_id={r['doc_id']}, kb_id={r['kb_id']}"

    results_kb2 = svc.search(query="RAG", kb_id=kb2.id, limit=10)
    for r in results_kb2:
        assert r["kb_id"] == kb2.id, f"KB2 过滤失效: doc_id={r['doc_id']}, kb_id={r['kb_id']}"

    db.close()
    print("  [PASS] 不同知识库检索结果互不干扰")


def test_search_top_k():
    if not EMBEDDING_API_KEY:
        print("  [SKIP] 未设置 DASHSCOPE_API_KEY，跳过 top_k 测试")
        return

    init_db()
    db = SessionLocal()

    kb = KnowledgeBase(name="TopK 测试 KB", description="Day5 top_k 测试")
    db.add(kb)
    db.flush()

    doc_id = _create_test_doc(db, kb.id, "topk")
    process_document(doc_id, db)

    svc = VectorService()
    results = svc.search(query="document", kb_id=kb.id, limit=3)
    assert len(results) <= 3, f"top_k=3 应返回 <=3 条结果 ({len(results)})"

    results_5 = svc.search(query="document", kb_id=kb.id, limit=5)
    assert len(results_5) <= 5, f"top_k=5 应返回 <=5 条结果 ({len(results_5)})"
    assert len(results_5) >= len(results), "top_k=5 应 >= top_k=3 的结果数"

    db.close()
    print("  [PASS] top_k 参数正确限制返回条数")


def test_search_no_key():
    if EMBEDDING_API_KEY:
        print("  [SKIP] 已配置 DASHSCOPE_API_KEY，跳过无 key 测试")
        return

    svc = VectorService()
    try:
        svc.search(query="test", kb_id=1, limit=5)
        assert False, "无 API Key 时应抛出异常"
    except RuntimeError as e:
        assert "未设置" in str(e), f"错误信息应提示未设置 API Key: {e}"

    print("  [PASS] 无 API Key 时正确抛出异常")


if __name__ == "__main__":
    test_search_basic()
    test_search_kb_filter()
    test_search_top_k()
    test_search_no_key()
    print("\n所有测试通过!")
