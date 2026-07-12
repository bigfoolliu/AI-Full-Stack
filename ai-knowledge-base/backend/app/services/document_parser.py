import os

import fitz
from docx import Document as DocxDocument


def parse_document(file_path: str, file_type: str) -> str:
    ext = file_type.lower()

    if ext == "pdf":
        return _parse_pdf(file_path)
    if ext in ("docx", "doc"):
        return _parse_docx(file_path)
    if ext == "txt":
        return _parse_txt(file_path)

    raise ValueError(f"不支持的文件类型: {file_type}")


def _parse_pdf(file_path: str) -> str:
    """
    解析 pdf 文件
    """

    try:
        doc = fitz.open(file_path)
        pages = []
        for page in doc:
            text = page.get_text()
            if text.strip():
                pages.append(text)
        doc.close()

        result = "\n\n".join(pages)
        if not result.strip():
            raise ValueError("PDF 文件未提取到文本内容")

        return result
    except Exception as e:
        raise RuntimeError(f"PDF 解析失败: {e}")


def _parse_docx(file_path: str) -> str:
    try:
        doc = DocxDocument(file_path)
        paragraphs = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                paragraphs.append(text)
        result = "\n\n".join(paragraphs)
        if not result.strip():
            raise ValueError("Word 文件未提取到文本内容")
        return result
    except Exception as e:
        raise RuntimeError(f"Word 解析失败: {e}")


def _parse_txt(file_path: str) -> str:
    """
    解析文本文件
    """

    encodings = ["utf-8", "gbk", "gb2312", "latin-1"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                content = f.read()
            if content.strip():
                return content
        except (UnicodeDecodeError, UnicodeError):
            continue

    with open(file_path, "r", encoding="latin-1") as f:
        return f.read()
