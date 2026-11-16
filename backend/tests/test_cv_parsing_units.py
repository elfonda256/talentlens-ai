"""Unit tests for the three parsing steps and the service that joins them."""

import logging
from datetime import date

import pytest

from app.services.cv_parsing import (
    UnreadableDocumentError,
    UnsupportedFormatError,
    extractor,
    parse_cv,
    pii,
)
from app.services.cv_parsing.document_loader import load_document
from app.services.cv_parsing.service import build_candidate_id
from tests.conftest import REFERENCE_DATE, SAMPLE_CVS

CV_TEXT = """SITI RAHMAWATI
siti.rahmawati@example.com | 081234567890
Tempat, Tanggal Lahir: Semarang, 1 Januari 1995
Jenis Kelamin: Perempuan
Agama: Islam
Status: Menikah
Alamat: Jl. Merdeka 1, Semarang

PROFIL
Arsitek dengan pengalaman pada proyek desain dan bangun.

PENGALAMAN KERJA
Arsitek Junior | PT Contoh | Jan 2022 - Des 2023
- Menyusun gambar kerja dengan AutoCAD dan SketchUp

PENDIDIKAN
S1 Arsitektur, Universitas Katolik Contoh, 2021

KEAHLIAN
AutoCAD, SketchUp
"""


# ---------- PII redaction ----------


def test_redaction_removes_sensitive_lines_and_keeps_them_separately():
    redacted, personal = pii.redact(CV_TEXT)

    lowered = redacted.lower()
    for leaked in ("siti", "perempuan", "islam", "menikah", "merdeka", "katolik", "@example.com"):
        assert leaked not in lowered
    assert "[NAMA]" in redacted and "[EMAIL]" in redacted and "[INSTITUSI]" in redacted
    assert personal["name"] == "Siti Rahmawati"
    assert personal["email"] == "siti.rahmawati@example.com"
    assert personal["phone"] == "081234567890"
    assert personal["gender"] == "Perempuan"


def test_redaction_keeps_job_relevant_content():
    redacted, _ = pii.redact(CV_TEXT)

    assert "AutoCAD" in redacted and "Arsitek Junior" in redacted and "S1 Arsitektur" in redacted


def test_swapping_personal_attributes_does_not_change_redacted_text():
    swapped = (
        CV_TEXT.replace("SITI RAHMAWATI", "BUDI SANTOSO")
        .replace("siti.rahmawati", "budi.santoso")
        .replace("Perempuan", "Laki-laki")
        .replace("Islam", "Hindu")
        .replace("Universitas Katolik Contoh", "Institut Teknologi Lain")
    )

    assert pii.redact(CV_TEXT)[0] == pii.redact(swapped)[0]


# ---------- Extraction ----------


def test_overlapping_jobs_are_not_counted_twice():
    section = (
        "Architect | PT A | Jan 2022 - Dec 2023\n- drawing\n"
        "Drafter | PT B | Jul 2023 - Jun 2024\n- drafting"
    )

    items, total_months = extractor.parse_experiences(section)

    assert [item.title for item in items] == ["Architect", "Drafter"]
    assert [item.company for item in items] == ["PT A", "PT B"]
    assert total_months == 29


def test_current_job_is_measured_up_to_the_reference_date():
    section = "Engineer | PT A | Jan 2026 - Present\n- work"

    _, at_march = extractor.parse_experiences(section, today=date(2026, 3, 15))
    _, at_november = extractor.parse_experiences(section, today=date(2026, 11, 16))

    assert (at_march, at_november) == (2, 10)


def test_indonesian_cv_is_extracted():
    redacted, _ = pii.redact(CV_TEXT)

    profile = extractor.extract("C-TEST", redacted, REFERENCE_DATE)

    assert profile.experiences[0].title == "Arsitek Junior"
    assert profile.total_experience_months == 23
    assert (profile.education[0].level, profile.education[0].field) == (4, "architecture")
    assert {"autocad", "sketchup", "technical_drawing"} <= set(profile.skills)
    assert profile.warnings == []


def test_missing_sections_lower_confidence_and_add_warnings():
    profile = extractor.extract("C-TEST", "Just a short note without any CV sections.")

    assert profile.extraction_confidence == 0.4
    assert "Bagian pengalaman kerja tidak ditemukan" in profile.warnings
    assert "Bagian pendidikan tidak terbaca" in profile.warnings


# ---------- Loading ----------


@pytest.mark.parametrize("file_name", ["cv_raka.pdf", "cv_nadia.docx", "cv_fajar.txt"])
def test_text_formats_are_loaded_without_ocr(file_name):
    text, method = load_document(SAMPLE_CVS / file_name)

    assert method == "text"
    assert len(text) > 300


def test_unknown_extension_is_rejected(tmp_path):
    path = tmp_path / "cv.xlsx"
    path.write_bytes(b"not a cv")

    with pytest.raises(UnsupportedFormatError):
        parse_cv(path)


# ---------- Service ----------


def test_candidate_id_follows_the_email_not_the_file():
    pdf = parse_cv(SAMPLE_CVS / "cv_raka.pdf", today=REFERENCE_DATE)
    txt = parse_cv(SAMPLE_CVS / "cv_raka_reapply.txt", today=REFERENCE_DATE)

    assert pdf.candidate_id == txt.candidate_id
    assert build_candidate_id("any text", {"email": "A@B.com"}) == build_candidate_id(
        "other text", {"email": "a@b.com"}
    )


def test_corrupt_pdf_is_reported_as_unreadable(tmp_path):
    path = tmp_path / "broken.pdf"
    path.write_bytes(b"%PDF-1.4 this is not really a pdf")

    with pytest.raises(UnreadableDocumentError):
        parse_cv(path)


def test_nearly_empty_document_is_reported_as_unreadable(tmp_path):
    path = tmp_path / "empty.txt"
    path.write_text("CV", encoding="utf-8")

    with pytest.raises(UnreadableDocumentError):
        parse_cv(path)


def test_log_line_has_counts_but_no_personal_data(caplog):
    with caplog.at_level(logging.INFO, logger="app.services.cv_parsing.service"):
        profile = parse_cv(SAMPLE_CVS / "cv_raka.pdf", today=REFERENCE_DATE)

    message = caplog.records[-1].getMessage()
    assert profile.candidate_id in message and "skills=" in message
    assert "raka" not in message.lower() and "@" not in message
