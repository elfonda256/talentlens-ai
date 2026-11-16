"""Reads a CV file (PDF, DOCX, TXT) into plain text, falling back to OCR for scanned PDFs."""

from __future__ import annotations

from pathlib import Path

from app.services.cv_parsing.text_utils import normalize

SUPPORTED_SUFFIXES = (".pdf", ".docx", ".txt", ".md")
MIN_TEXT_CHARS = 80  # below this, a PDF is treated as a scan


class UnsupportedFormatError(ValueError):
    """The file extension is not one the loader can read."""

    def __init__(self, suffix: str):
        super().__init__(f"Format berkas tidak didukung: {suffix}")
        self.suffix = suffix


def _pdf_text(path: Path) -> str:
    import pdfplumber

    with pdfplumber.open(path) as pdf:
        return "\n".join((page.extract_text() or "") for page in pdf.pages)


def _pdf_ocr(path: Path) -> str:
    """Local OCR with Tesseract; tries English + Indonesian, then English only."""
    import pypdfium2 as pdfium
    import pytesseract

    pdf = pdfium.PdfDocument(str(path))
    pages = []
    for page in pdf:
        image = page.render(scale=2.0).to_pil()
        try:
            pages.append(pytesseract.image_to_string(image, lang="eng+ind"))
        except pytesseract.TesseractError:
            pages.append(pytesseract.image_to_string(image, lang="eng"))
    return "\n".join(pages)


def _docx_text(path: Path) -> str:
    import docx

    document = docx.Document(str(path))
    lines = [p.text for p in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            lines.append(" | ".join(cell.text for cell in row.cells))
    return "\n".join(lines)


def load_document(path: Path) -> tuple[str, str]:
    """Returns (text, method) where method is 'text' or 'ocr'."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        text = _pdf_text(path)
        if len(text.strip()) >= MIN_TEXT_CHARS:
            return _clean(text), "text"
        return _clean(_pdf_ocr(path)), "ocr"
    if suffix == ".docx":
        return _clean(_docx_text(path)), "text"
    if suffix in {".txt", ".md"}:
        return _clean(path.read_text(encoding="utf-8", errors="ignore")), "text"
    raise UnsupportedFormatError(suffix)


def _clean(text: str) -> str:
    return "\n".join(normalize(line) for line in text.splitlines())
