"""Regression guard: the integrated parser must return exactly what the original PoC returned.

`fixtures/golden_profiles.json` was produced by running the original `cv-screening-poc`
parser (before any refactoring) on the files in `fixtures/cvs/`.
"""

import json
import shutil

import pytest

from app.services.cv_parsing import parse_cv
from tests.conftest import FIXTURES, REFERENCE_DATE, SAMPLE_CVS

GOLDEN = json.loads((FIXTURES / "golden_profiles.json").read_text(encoding="utf-8"))
SCANNED = "cv_laras_scan.pdf"
# Fields the parser gained after the PoC. Everything the PoC produced must still be identical.
ADDED_IN_QA_PHASE_2 = {"section_confidence", "education_in_progress"}
TEXT_BASED = sorted(name for name in GOLDEN if name != SCANNED)


@pytest.mark.parametrize("file_name", TEXT_BASED)
def test_output_matches_original_parser(file_name):
    profile = parse_cv(SAMPLE_CVS / file_name, today=REFERENCE_DATE)

    assert profile.model_dump(exclude=ADDED_IN_QA_PHASE_2) == GOLDEN[file_name]


@pytest.mark.skipif(shutil.which("tesseract") is None, reason="Tesseract is not installed")
def test_scanned_pdf_is_read_through_ocr():
    """OCR text varies slightly between Tesseract versions, so only stable facts are checked."""
    profile = parse_cv(SAMPLE_CVS / SCANNED, today=REFERENCE_DATE)
    expected = GOLDEN[SCANNED]

    assert profile.extraction_method == "ocr"
    assert "Dokumen hasil scan, dibaca dengan OCR" in profile.warnings
    assert {"autocad", "sketchup", "technical_drawing"} <= set(profile.skills)
    assert profile.total_experience_months == expected["total_experience_months"]
    assert [e.field for e in profile.education] == [e["field"] for e in expected["education"]]
