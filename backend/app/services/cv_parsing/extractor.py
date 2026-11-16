"""Rule-based information extraction: redacted CV text -> structured profile.

Deterministic, free and offline. It recognises section headings and date ranges in
English and Indonesian, and maps skills through the taxonomy.
"""

from __future__ import annotations

import re
from datetime import date

from app.schemas.cv import CandidateProfile, EducationItem, ExperienceItem
from app.services import taxonomy
from app.services.cv_parsing.text_utils import chunk_text

SECTIONS = {
    "summary": r"summary|profile|profil|ringkasan|tentang saya|about me|objective",
    "experience": r"work experience|professional experience|experience|pengalaman kerja|pengalaman|riwayat pekerjaan|employment",
    "education": r"education|pendidikan|riwayat pendidikan|academic",
    "skills": r"skills?|technical skills|keahlian|keterampilan|kemampuan|software|competenc(?:y|ies)",
    "other": r"certifications?|sertifikasi|sertifikat|organi[sz]ations?|organisasi|languages?|bahasa|projects?|proyek|awards?|penghargaan|references?|referensi|portfolio|portofolio",
}
HEADING = re.compile(
    r"^\s*(?:" + "|".join(f"(?P<{k}>{v})" for k, v in SECTIONS.items()) + r")\s*:?\s*$",
    re.IGNORECASE,
)

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "mei": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "agu": 8,
    "ags": 8,
    "sep": 9,
    "oct": 10,
    "okt": 10,
    "nov": 11,
    "dec": 12,
    "des": 12,
}
MONTH = r"(?:jan|feb|mar|apr|may|mei|jun|jul|aug|agu|ags|sep|oct|okt|nov|dec|des)[a-z]*\.?"


def _point(p: str) -> str:
    return rf"(?:(?P<{p}m>{MONTH})\s+)?(?P<{p}y>(?:19|20)\d{{2}})"


PRESENT = r"present|now|current|sekarang|saat ini|kini"
DATE_RANGE = re.compile(
    _point("s")
    + r"\s*(?:-|to|s/d|sampai|hingga)\s*(?:"
    + _point("e")
    + rf"|(?P<present>{PRESENT}))",
    re.IGNORECASE,
)

DEGREES = [
    (6, r"\bs3\b|ph\.?d|doktor|doctor"),
    (5, r"\bs2\b|master|magister|m\.?sc|m\.?arch|\bmba\b"),
    (4, r"\bs1\b|\bd4\b|bachelor|sarjana|b\.?sc|b\.?arch|s\.?t\.|s\.?ars|s\.?ds|undergraduate"),
    (3, r"\bd3\b|diploma|ahli madya|a\.?md"),
    (2, r"\bsmk\b|\bsma\b|high school|stm"),
]
FIELDS = {
    "architecture": r"architectur|arsitektur",
    "interior design": r"interior",
    "civil engineering": r"civil engineering|teknik sipil|sipil",
    "urban planning": r"urban planning|planologi|perencanaan wilayah",
    "product design": r"product design|desain produk",
    "visual communication design": r"visual communication|komunikasi visual|dkv",
    "computer science": r"computer science|informatika|information technology|sistem informasi|ilmu komputer",
    "accounting": r"accounting|akuntansi",
    "management": r"management|manajemen",
}


def split_sections(text: str) -> dict[str, str]:
    current, buckets = "header", {"header": []}
    for line in text.splitlines():
        match = HEADING.match(line)
        if match:
            current = next(k for k, v in match.groupdict().items() if v)
            buckets.setdefault(current, [])
            continue
        buckets.setdefault(current, []).append(line)
    return {k: "\n".join(v).strip() for k, v in buckets.items()}


def _month_index(year: str, month: str | None, default_month: int) -> int:
    m = MONTHS.get((month or "")[:3].lower(), default_month)
    return int(year) * 12 + m


def _duration(match: re.Match, today: date) -> tuple[int, int]:
    start = _month_index(match.group("sy"), match.group("sm"), 1)
    if match.group("present"):
        end = today.year * 12 + today.month
    else:
        end = _month_index(match.group("ey"), match.group("em"), 12 if not match.group("sm") else 1)
        if not match.group("em") and not match.group("sm"):
            end = int(match.group("ey")) * 12 + 1  # "2020 - 2022" is read as 24 months
    return start, max(end, start + 1)


def parse_experiences(section: str, today: date | None = None) -> tuple[list[ExperienceItem], int]:
    today = today or date.today()
    lines = [line for line in section.splitlines() if line.strip()]
    items: list[ExperienceItem] = []
    intervals: list[tuple[int, int]] = []
    current: ExperienceItem | None = None
    for idx, line in enumerate(lines):
        match = DATE_RANGE.search(line)
        if match:
            start, end = _duration(match, today)
            header = (line[: match.start()] + " " + line[match.end() :]).strip(" |-,()")
            carried = ""
            if current and current.description:
                # the line right before a date often holds the title/company
                desc_lines = current.description.splitlines()
                if not header or len(header) < 4:
                    carried = desc_lines.pop()
                    current.description = "\n".join(desc_lines)
            elif not header and idx > 0 and not items:
                carried = lines[idx - 1]
            header = header or carried
            parts = [
                p.strip()
                for p in re.split(
                    r"\s+\|\s+|\s+@\s+|\s+at\s+|\s+di\s+|\s+-\s+|,\s+", header, maxsplit=1
                )
            ]
            current = ExperienceItem(
                title=parts[0] if parts else "",
                company=parts[1] if len(parts) > 1 else "",
                start=str((start - 1) // 12),
                end="present" if match.group("present") else str((end - 1) // 12),
                months=end - start,
            )
            items.append(current)
            intervals.append((start, end))
        elif current:
            current.description = (current.description + "\n" + line.strip(" -")).strip()
    total, last_end = 0, 0
    for start, end in sorted(intervals):  # merge overlapping periods
        start = max(start, last_end)
        if end > start:
            total += end - start
            last_end = end
    return items, total


def parse_education(section: str) -> list[EducationItem]:
    items = []
    for line in section.splitlines():
        low = line.lower()
        level = next((lvl for lvl, pat in DEGREES if re.search(pat, low)), 0)
        field = next((name for name, pat in FIELDS.items() if re.search(pat, low)), "")
        if level or field:
            if items and not items[-1].field and field and not level:
                items[-1].field = field
                continue
            if items and items[-1].level == 0 and level and not field:
                items[-1].level = level
                continue
            items.append(EducationItem(degree=line.strip()[:120], level=level, field=field))
    return items


def extract(candidate_id: str, redacted_text: str, today: date | None = None) -> CandidateProfile:
    sections = split_sections(redacted_text)
    warnings: list[str] = []

    experiences, total_months = parse_experiences(sections.get("experience", ""), today)
    if not sections.get("experience"):
        warnings.append("Bagian pengalaman kerja tidak ditemukan")
    education = parse_education(sections.get("education", ""))
    if not education:
        warnings.append("Bagian pendidikan tidak terbaca")

    skills = taxonomy.find_skills(redacted_text)
    body = "\n".join(
        sections.get(k, "") for k in ("summary", "experience", "skills", "other", "education")
    )
    chunks = chunk_text(body)

    # Simple confidence score: how many core sections were read successfully
    found = sum(bool(x) for x in (experiences, education, skills, sections.get("skills")))
    confidence = round(0.4 + 0.15 * found, 2)

    return CandidateProfile(
        candidate_id=candidate_id,
        redacted_text=redacted_text,
        summary=sections.get("summary", "")[:400],
        experiences=experiences,
        total_experience_months=total_months,
        education=education,
        skills=skills,
        chunks=chunks,
        extraction_confidence=min(confidence, 1.0),
        warnings=warnings,
    )
