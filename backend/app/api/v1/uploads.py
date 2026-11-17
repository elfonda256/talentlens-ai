"""Shared handling of uploaded documents: validation and a short-lived temporary copy."""

import shutil
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.core.config import Settings
from app.services.cv_parsing import SUPPORTED_SUFFIXES


def validate_upload(file: UploadFile, settings: Settings) -> str:
    """Returns the lower-case file extension, or raises 415 / 413."""
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise HTTPException(
            415, f"Format {suffix or 'tanpa ekstensi'} tidak didukung. Gunakan PDF, DOCX, atau TXT."
        )
    if file.size is not None and file.size > settings.max_upload_bytes:
        raise HTTPException(413, f"Ukuran berkas melebihi {settings.max_upload_mb} MB.")
    return suffix


@contextmanager
def temporary_copy(file: UploadFile, suffix: str) -> Iterator[Path]:
    """The uploaded document only exists on disk while it is being parsed."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / f"upload{suffix}"
        with path.open("wb") as target:
            shutil.copyfileobj(file.file, target)
        yield path
