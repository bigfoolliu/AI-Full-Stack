import re

CHUNK_DEFAULTS = {"chunk_size": 512, "overlap": 64}


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_DEFAULTS["chunk_size"],
    overlap: int = CHUNK_DEFAULTS["overlap"],
    doc_id: int | None = None,
    kb_id: int | None = None,
) -> list[dict]:
    if not text.strip():
        return []

    overlap = min(overlap, chunk_size // 2)
    step = chunk_size - overlap
    chunks = []

    for i in range(0, max(len(text), 1), step):
        if i >= len(text):
            break
        content = text[i : i + chunk_size]
        if not content.strip():
            continue
        chunks.append(
            {
                "doc_id": doc_id,
                "kb_id": kb_id,
                "chunk_index": len(chunks),
                "content": content,
                "page_number": None,
                "chunk_size": chunk_size,
            }
        )

    return chunks


def _make_chunk(
    content: str,
    chunk_size: int,
    doc_id: int | None,
    kb_id: int | None,
) -> dict:
    return {
        "doc_id": doc_id,
        "kb_id": kb_id,
        "chunk_index": 0,
        "content": content,
        "page_number": None,
        "chunk_size": chunk_size,
    }


def recursive_chunk_text(
    text: str,
    chunk_size: int = CHUNK_DEFAULTS["chunk_size"],
    overlap: int = CHUNK_DEFAULTS["overlap"],
    doc_id: int | None = None,
    kb_id: int | None = None,
) -> list[dict]:
    if not text.strip():
        return []

    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if len(para) <= chunk_size:
            chunks.append(_make_chunk(para, chunk_size, doc_id, kb_id))
            continue

        sentences = re.split(r"(?<=[。！？；\n])\s*", para)
        buffer = ""
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue

            if len(sent) > chunk_size:
                if buffer:
                    chunks.append(_make_chunk(buffer, chunk_size, doc_id, kb_id))
                    buffer = ""
                chunks.extend(chunk_text(sent, chunk_size, overlap, doc_id, kb_id))
                continue

            if len(buffer) + len(sent) <= chunk_size:
                buffer = (buffer + sent).strip() if buffer else sent
            else:
                chunks.append(_make_chunk(buffer, chunk_size, doc_id, kb_id))
                buffer = sent

        if buffer:
            chunks.append(_make_chunk(buffer, chunk_size, doc_id, kb_id))

    for i, chunk in enumerate(chunks):
        chunk["chunk_index"] = i

    return chunks
