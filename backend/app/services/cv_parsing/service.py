"""CV parsing service: one entry point that turns a CV file into a CandidateProfile.

Pipeline: load document (OCR if scanned) -> redact PII -> extract structured fields.
The three steps live in their own modules; this file only orchestrates them.
"""

import hashlib
import logging
import time
from datetime import date
from pathlib import Path

from app.schemas.cv import CandidateProfile
from app.services.cv_parsing import extractor, pii
from app.services.cv_parsing.document_loader import UnsupportedFormatError, load_document

logger = logging.getLogger(__name__)

MIN_DOCUMENT_CHARS = 40
OCR_CONFIDENCE_FACTOR = 0.85
OCR_WARNING = "Dokumen hasil scan, dibaca dengan OCR"


class UnreadableDocumentError(Exception):
    """The file has a supported format but no usable text could be read from it."""


def build_candidate_id(redacted_text: str, personal: dict[str, str]) -> str:
    """Stable id: the same person (same email) gets the same id on every upload."""
    identity = personal.get("email") or redacted_text
    return "C-" + hashlib.sha256(identity.lower().encode()).hexdigest()[:8].upper()


def parse_cv(
    path: Path,
    *,
    file_name: str | None = None,
    source: str = "upload",
    today: date | None = None,
) -> CandidateProfile:
    """Parse one CV file.

    Raises UnsupportedFormatError for an unknown extension and UnreadableDocumentError
    when the document is corrupt, empty or needs OCR that is not available.
    """
    started = time.perf_counter()
    text, method = _read(path)
    if len(text.strip()) < MIN_DOCUMENT_CHARS:
        raise UnreadableDocumentError("Dokumen tidak berisi teks yang dapat dibaca")

    redacted, personal = pii.redact(text)
    profile = extractor.extract(build_candidate_id(redacted, personal), redacted, today)
    profile.source = source
    profile.file_name = file_name or path.name
    profile.extraction_method = method
    profile.pii = personal
    if method == "ocr":
        profile.extraction_confidence = round(
            profile.extraction_confidence * OCR_CONFIDENCE_FACTOR, 2
        )
        profile.warnings.append(OCR_WARNING)

    # File names and extracted values can identify a person, so only counts are logged.
    logger.info(
        "Parsed CV %s: method=%s experiences=%d education=%d skills=%d "
        "confidence=%.2f warnings=%d in %.0f ms",
        profile.candidate_id,
        method,
        len(profile.experiences),
        len(profile.education),
        len(profile.skills),
        profile.extraction_confidence,
        len(profile.warnings),
        (time.perf_counter() - started) * 1000,
    )
    return profile


def _read(path: Path) -> tuple[str, str]:
    try:
        return load_document(path)
    except UnsupportedFormatError:
        raise
    except Exception as error:
        # PDF/DOCX libraries raise many unrelated error types for corrupt files, and a
        # missing Tesseract binary surfaces here too. All mean the same thing to the caller.
        logger.warning("Could not read %s document: %s", path.suffix, type(error).__name__)
        raise UnreadableDocumentError("Dokumen rusak atau tidak dapat dibaca") from error
