"""Text helpers shared by the loader and the extractor."""

from __future__ import annotations

import re


def normalize(text: str) -> str:
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2022", "-")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [p.strip(" -\t") for p in parts if len(p.strip(" -\t")) > 3]


def chunk_text(text: str, max_chars: int = 170) -> list[str]:
    """Line/sentence based chunks; enough for CVs, which are mostly bullet points."""
    chunks, buf = [], ""
    for sent in split_sentences(text):
        if len(buf) + len(sent) + 1 > max_chars and buf:
            chunks.append(buf)
            buf = sent
        else:
            buf = f"{buf} {sent}".strip()
    if buf:
        chunks.append(buf)
    return chunks
