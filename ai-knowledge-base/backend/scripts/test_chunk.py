from app.services.chunk_service import chunk_text, recursive_chunk_text


def test_empty_text():
    assert chunk_text("") == []
    assert chunk_text("   ") == []
    assert recursive_chunk_text("") == []
    assert recursive_chunk_text("   ") == []
    print("  [PASS] 空文本返回空列表")


def test_short_text_single_chunk():
    text = "Hello World"
    result = chunk_text(text)
    assert len(result) == 1
    assert result[0]["content"] == text
    assert result[0]["chunk_index"] == 0
    print("  [PASS] 短文本返回单个 chunk")


def test_long_text_multi_chunk():
    text = "A" * 1500
    result = chunk_text(text, chunk_size=512, overlap=64)
    assert len(result) > 1
    total_len = sum(len(c["content"]) for c in result)
    assert total_len >= 1500
    print(f"  [PASS] 长文本正确切分为 {len(result)} 个 chunk (总计 {total_len} 字符)")


def test_overlap_between_chunks():
    text = "HelloWorld" * 200
    result = chunk_text(text, chunk_size=100, overlap=20)
    for i in range(1, len(result)):
        prev = result[i - 1]["content"]
        curr = result[i]["content"]
        has_overlap = prev[-(20):] in curr
        assert has_overlap, f"Chunk {i} 缺少 overlap"
    print("  [PASS] overlap 正确保留在相邻 chunk 之间")


def test_text_not_lost():
    text = "HelloWorld" * 200
    result = chunk_text(text, chunk_size=100, overlap=20)
    reconstructed = "".join(c["content"] for c in result)
    for ch in text:
        assert ch in reconstructed, f"字符 '{ch}' 在重构后丢失"
    print("  [PASS] 切分后文本内容未丢失")


def test_recursive_paragraph_splitting():
    text = "第一段内容。这是第一段。\n\n第二段内容。\n\n第三段内容。"
    result = recursive_chunk_text(text, chunk_size=512, overlap=64)
    assert len(result) == 3
    assert "第一段" in result[0]["content"]
    assert "第二段" in result[1]["content"]
    assert "第三段" in result[2]["content"]
    assert all(c["chunk_index"] == i for i, c in enumerate(result))
    print(f"  [PASS] 递归切分按段落正确分割为 {len(result)} 个 chunk")


def test_recursive_long_paragraph():
    text = "第一句。" + "第二句这句话内容很长用来测试。" * 50 + "第三句。"
    result = recursive_chunk_text(text, chunk_size=100, overlap=20)
    assert len(result) >= 2
    for chunk in result:
        assert len(chunk["content"]) <= 120
    print(f"  [PASS] 超长段落按句子切分为 {len(result)} 个 chunk")


def test_metadata_completeness():
    text = "Hello World"
    result = chunk_text(text, chunk_size=512, overlap=64, doc_id=42, kb_id=7)
    for chunk in result:
        assert chunk["doc_id"] == 42
        assert chunk["kb_id"] == 7
        assert chunk["chunk_index"] == 0
        assert chunk["page_number"] is None
        assert chunk["chunk_size"] == 512
        assert "content" in chunk
    print("  [PASS] 每个 chunk 携带完整元数据")


def test_overlap_clamped():
    text = "A" * 200
    result = chunk_text(text, chunk_size=100, overlap=200)
    for chunk in result:
        assert len(chunk["content"]) <= 100
    print("  [PASS] overlap 超过 chunk_size//2 时自动限制")


def test_chunk_integration_with_parser():
    import tempfile
    from pathlib import Path

    from fpdf import FPDF

    from app.services.document_parser import parse_document

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)
    for i in range(50):
        pdf.cell(text=f"Line number {i} of the test document. ", new_x="LMARGIN", new_y="NEXT")
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    pdf.output(tmp.name)

    text = parse_document(tmp.name, "pdf")
    chunks = recursive_chunk_text(text, chunk_size=200, overlap=30, doc_id=1, kb_id=1)

    assert len(chunks) >= 2
    assert all(c["doc_id"] == 1 for c in chunks)
    assert all(c["kb_id"] == 1 for c in chunks)
    total_content = "".join(c["content"] for c in chunks)
    assert "Line number" in total_content

    Path(tmp.name).unlink()
    print(f"  [PASS] 文档解析 + 递归切分串联正确 ({len(chunks)} 个 chunk)")


if __name__ == "__main__":
    test_empty_text()
    test_short_text_single_chunk()
    test_long_text_multi_chunk()
    test_overlap_between_chunks()
    test_text_not_lost()
    test_recursive_paragraph_splitting()
    test_recursive_long_paragraph()
    test_metadata_completeness()
    test_overlap_clamped()
    test_chunk_integration_with_parser()
    print("\n所有测试通过!")
