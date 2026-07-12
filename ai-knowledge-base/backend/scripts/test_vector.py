import time
from pathlib import Path

import httpx

from app.core.config import EMBEDDING_API_KEY, EMBEDDING_DIMENSION, QDRANT_URL
from app.services.chunk_service import chunk_text
from app.services.vector_service import VectorService


def qdrant_ready() -> bool:
    try:
        r = httpx.get(f"{QDRANT_URL}/collections", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def test_qdrant_connection():
    assert qdrant_ready(), f"Qdrant 不可达 ({QDRANT_URL})"
    print("  [PASS] Qdrant 连接正常")


def test_collection_creation():
    svc = VectorService(collection_name="test_week5_day3")
    collections = svc.qdrant.get_collections().collections
    names = {c.name for c in collections}
    assert "test_week5_day3" in names
    svc.qdrant.delete_collection("test_week5_day3")
    print("  [PASS] Collection 创建成功")


def test_embedding():
    if not EMBEDDING_API_KEY:
        print("  [SKIP] 未设置 DASHSCOPE_API_KEY，跳过 Embedding 测试")
        return

    svc = VectorService(collection_name="test_embed")

    texts = ["Hello World", "你好世界"]
    vectors = svc.embed_texts(texts)
    assert len(vectors) == 2
    assert len(vectors[0]) == EMBEDDING_DIMENSION
    assert len(vectors[1]) == EMBEDDING_DIMENSION
    svc.qdrant.delete_collection("test_embed")
    print(f"  [PASS] Embedding 生成正确 ({len(vectors[0])} 维)")


def test_upsert_and_search():
    if not EMBEDDING_API_KEY:
        print("  [SKIP] 未设置 DASHSCOPE_API_KEY，跳过 Upsert/Search 测试")
        return

    svc = VectorService(collection_name="test_upsert")
    chunks = chunk_text(
        "人工智能是计算机科学的一个重要分支。\n\n"
        "机器学习让计算机能够从数据中学习。\n\n"
        "深度学习是机器学习的一个子领域。",
        chunk_size=512,
        overlap=64,
        doc_id=1,
        kb_id=1,
    )
    assert len(chunks) > 0
    n = svc.upsert_chunks(chunks, filename="test.txt")
    assert n == len(chunks)

    time.sleep(1)

    results = svc.search("机器学习", kb_id=1, limit=5)
    assert len(results) > 0
    assert any("机器学习" in r["content"] for r in results)

    svc.qdrant.delete_collection("test_upsert")
    print(f"  [PASS] Upsert {n} 个 chunk，Search 返回 {len(results)} 条结果")


def test_search_without_kb_filter():
    if not EMBEDDING_API_KEY:
        print("  [SKIP] 未设置 DASHSCOPE_API_KEY，跳过跨知识库搜索测试")
        return

    svc = VectorService(collection_name="test_search_all")
    svc.upsert_chunks(
        [
            {
                "doc_id": 1,
                "kb_id": 1,
                "chunk_index": 0,
                "content": "Python是一种编程语言",
                "chunk_size": 512,
            }
        ],
        filename="doc1.txt",
    )
    svc.upsert_chunks(
        [
            {
                "doc_id": 2,
                "kb_id": 2,
                "chunk_index": 0,
                "content": "Java也是一种编程语言",
                "chunk_size": 512,
            }
        ],
        filename="doc2.txt",
    )
    time.sleep(1)

    results = svc.search("编程语言", kb_id=None, limit=10)
    assert len(results) >= 2, f"跨库搜索应返回全部结果，实际 {len(results)}"

    results_kb1 = svc.search("编程语言", kb_id=1, limit=10)
    assert len(results_kb1) >= 1
    assert all(r["kb_id"] == 1 for r in results_kb1)

    svc.qdrant.delete_collection("test_search_all")
    print(f"  [PASS] 跨库搜索 ({len(results)} 条) + 按 KB 过滤 ({len(results_kb1)} 条)")


def test_delete_chunks():
    if not EMBEDDING_API_KEY:
        print("  [SKIP] 未设置 DASHSCOPE_API_KEY，跳过删除测试")
        return

    svc = VectorService(collection_name="test_delete")
    svc.upsert_chunks(
        [
            {
                "doc_id": 10,
                "kb_id": 1,
                "chunk_index": 0,
                "content": "文档10的第一段",
                "chunk_size": 512,
            },
            {
                "doc_id": 10,
                "kb_id": 1,
                "chunk_index": 1,
                "content": "文档10的第二段",
                "chunk_size": 512,
            },
        ],
        filename="doc10.txt",
    )
    time.sleep(1)

    svc.delete_document_chunks(doc_id=10)
    time.sleep(1)

    results = svc.search("文档10", kb_id=None, limit=10)
    assert len(results) == 0, f"删除后应返回空结果，实际 {len(results)}"

    svc.qdrant.delete_collection("test_delete")
    print("  [PASS] 删除文档 chunks 成功")


def test_upsert_from_parser_and_chunker():
    if not EMBEDDING_API_KEY:
        print("  [SKIP] 未设置 DASHSCOPE_API_KEY，跳过全流程测试")
        return

    import tempfile

    from fpdf import FPDF

    from app.services.chunk_service import recursive_chunk_text
    from app.services.document_parser import parse_document

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)
    for i in range(30):
        pdf.cell(
            text=f"This is line {i} of the test document for vector search. ",
            new_x="LMARGIN",
            new_y="NEXT",
        )
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    pdf.output(tmp.name)

    text = parse_document(tmp.name, "pdf")
    chunks = recursive_chunk_text(text, chunk_size=200, overlap=30, doc_id=99, kb_id=5)

    svc = VectorService(collection_name="test_full_pipeline")
    n = svc.upsert_chunks(chunks, filename="vector_test.pdf")
    time.sleep(1)

    results = svc.search("test document", kb_id=5, limit=5)
    assert len(results) > 0

    svc.qdrant.delete_collection("test_full_pipeline")
    Path(tmp.name).unlink()
    print(f"  [PASS] 全流程 (解析→切分→向量化→搜索) 正确，{n} 个 chunk 写入，搜索到 {len(results)} 条")


if __name__ == "__main__":
    test_qdrant_connection()

    has_key = bool(EMBEDDING_API_KEY)

    test_collection_creation()

    if has_key:
        test_embedding()
        test_upsert_and_search()
        test_search_without_kb_filter()
        test_delete_chunks()
        test_upsert_from_parser_and_chunker()
    else:
        print("  [SKIP] Embedding/Search/Delete 测试 (设置 DASHSCOPE_API_KEY 后可运行)")
        print("  [SKIP] 全流程测试 (设置 DASHSCOPE_API_KEY 后可运行)")

    print("\n所有测试通过!")
