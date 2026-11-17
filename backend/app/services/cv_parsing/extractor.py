"""Rule-based information extraction: redacted CV text -> structured profile.

Deterministic, free and offline. It recognises section headings and date ranges in
English and Indonesian, and maps skills through the taxonomy.
"""

from __future__ import annotations

import re
from datetime import date

from app.schemas.cv import CandidateProfile, EducationItem, ExperienceItem
from app.services import taxonomy
from app.services.cv_parsing.pii import INSTITUTION_MARK
from app.services.cv_parsing.text_utils import chunk_text

# Section headings as real CVs write them, in English and Indonesian. They are compared
# through `_heading_key`, so case, punctuation, plurals and letter-spaced headings
# ("W O R K  E X P E R I E N C E") all resolve to the same entry.
HEADINGS: dict[str, tuple[str, ...]] = {
    "summary": (
        "summary",
        "professional summary",
        "career summary",
        "executive summary",
        "profile",
        "professional profile",
        "personal profile",
        "profil",
        "profil singkat",
        "ringkasan",
        "ringkasan profil",
        "tentang saya",
        "about me",
        "about",
        "objective",
        "career objective",
        "deskripsi diri",
    ),
    "experience": (
        "experience",
        "work experience",
        "working experience",
        "professional experience",
        "job experience",
        "relevant experience",
        "employment",
        "employment history",
        "work history",
        "career history",
        "professional background",
        "internship experience",
        "pengalaman",
        "pengalaman kerja",
        "pengalaman bekerja",
        "pengalaman profesional",
        "pengalaman pekerjaan",
        "riwayat kerja",
        "riwayat pekerjaan",
        "riwayat karier",
        "riwayat karir",
    ),
    "education": (
        "education",
        "education level",
        "education background",
        "educational background",
        "education history",
        "formal education",
        "academic",
        "academic background",
        "academic history",
        "education and training",
        "pendidikan",
        "pendidikan formal",
        "riwayat pendidikan",
        "latar belakang pendidikan",
    ),
    "skills": (
        "skill",
        "technical skill",
        "hard skill",
        "soft skill",
        "soft and hard skill",
        "hard and soft skill",
        "key skill",
        "core skill",
        "software skill",
        "computer skill",
        "skills and expertise",
        "area of expertise",
        "areas of expertise",
        "expertise",
        "competency",
        "competencies",
        "core competency",
        "core competencies",
        "software",
        "tools",
        "keahlian",
        "keterampilan",
        "kemampuan",
        "kompetensi",
    ),
    "other": (
        "certification",
        "certificate",
        "licenses and certifications",
        "sertifikasi",
        "sertifikat",
        "lisensi dan sertifikasi",
        "training",
        "pelatihan",
        "course",
        "non formal education",
        "pendidikan non formal",
        "organization",
        "organisation",
        "organisasi",
        "organizational experience",
        "organisational experience",
        "organization experience",
        "pengalaman organisasi",
        "volunteer experience",
        "language",
        "bahasa",
        "project",
        "proyek",
        "award",
        "achievement",
        "key achievement",
        "penghargaan",
        "prestasi",
        "reference",
        "referensi",
        "portfolio",
        "portofolio",
        "publication",
        "publikasi",
        "additional information",
        "informasi tambahan",
        "interest",
        "hobby",
        "hobi",
    ),
}
MAX_HEADING_CHARS = 45
PROJECT_HEADINGS = {"project", "proyek"}
# Some CV builders print the heading on the same line as its first entry.
INLINE_HEADING = re.compile(
    r"^(Ringkasan|Riwayat [Kk]arier|Riwayat [Kk]arir|Riwayat [Pp]ekerjaan|Riwayat [Kk]erja"
    r"|Pengalaman [Kk]erja|Keahlian|Keterampilan|Pendidikan|Bahasa|Sertifikasi)\s+(?=[A-Z])"
)


def _heading_key(text: str) -> str:
    key = re.sub(r"[^a-z]", "", text.lower().replace("&", "and"))
    return key


HEADING_KEYS = {
    _heading_key(phrase): section for section, phrases in HEADINGS.items() for phrase in phrases
}


def heading_of(line: str) -> str | None:
    """The section a line announces, or None when the line is ordinary content."""
    stripped = line.strip()
    # A heading is short and is not the tail of a wrapped sentence ("... problem-solving\nskills.")
    if not stripped or len(stripped) > MAX_HEADING_CHARS or stripped[-1] in ".,;":
        return None
    key = _heading_key(stripped)
    return HEADING_KEYS.get(key) or HEADING_KEYS.get(key.removesuffix("s"))


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
    (2, r"\bsmkn?\b|\bsman?\b|high school|vocational|sekolah menengah|stm"),
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
        section, rest = heading_of(line), ""
        if section is None:
            inline = INLINE_HEADING.match(line)
            if inline and HEADING_KEYS[_heading_key(inline.group(1))] not in buckets:
                section, rest = HEADING_KEYS[_heading_key(inline.group(1))], line[inline.end() :]
        # "Project:" under a job lists that job's projects; it does not end the experience section
        if (
            section == "other"
            and current == "experience"
            and _heading_key(line).removesuffix("s") in PROJECT_HEADINGS
        ):
            section = None
        if section is None:
            buckets.setdefault(current, []).append(line)
            continue
        current = section
        buckets.setdefault(current, [])
        if rest:
            buckets[current].append(rest)
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


# "(1 tahun 2 bulan)" next to a date range repeats the dates; it is not a job title
DURATION_NOTE = re.compile(
    r"\(?\s*\d+\s*(?:tahun|thn|bulan|bln|years?|yrs?|months?|mos?)\b"
    r"(?:\s*\d+\s*(?:bulan|bln|months?|mos?)\b)?\s*\)?",
    re.IGNORECASE,
)
COMPANY_HINT = re.compile(
    r"^(?:PT|CV|UD|Studio|Biro|Yayasan)\b\.?"
    r"|\b(?:Tbk|Ltd|Inc|Corp|Group|Persero|Consultants?|Konsultan|Contractor|Kontraktor)\b",
    re.IGNORECASE,
)
HEADER_SPLIT = re.compile(r"\s+\|\s+|\s+@\s+|\s+at\s+|\s+di\s+|\s+-\s+|,\s+")
BULLET = re.compile(r"^\s*[-*\u2022\u25cf\u25aa\u2023\uf0b7]")
MAX_LABEL_WORDS = 5


def _is_label(line: str) -> bool:
    """A short standalone line such as a job title or a company name, not a sentence."""
    text = line.strip()
    return (
        bool(text)
        and not BULLET.match(line)
        and len(text.split()) <= MAX_LABEL_WORDS
        and text[0].isupper()
        and text[-1] not in ".,;:"
        and not DATE_RANGE.search(text)
    )


def _split_header(header: str) -> tuple[str, str]:
    parts = [part.strip() for part in HEADER_SPLIT.split(header, maxsplit=1)]
    title = parts[0] if parts else ""
    company = parts[1] if len(parts) > 1 else ""
    return title, company


def parse_experiences(section: str, today: date | None = None) -> tuple[list[ExperienceItem], int]:
    today = today or date.today()
    lines = [line for line in section.splitlines() if line.strip()]
    items: list[ExperienceItem] = []
    intervals: list[tuple[int, int]] = []
    current: ExperienceItem | None = None
    skip_next = False
    for idx, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
        match = DATE_RANGE.search(line)
        if not match:
            if current:
                current.description = (current.description + "\n" + line.strip(" -")).strip()
            continue

        start, end = _duration(match, today)
        rest = line[: match.start()] + " " + line[match.end() :]
        header = DURATION_NOTE.sub(" ", rest).strip(" |-,()")
        carried = ""
        if current and current.description:
            # the line right before a date often holds the title/company
            desc_lines = current.description.splitlines()
            if not header or len(header) < 4:
                carried = desc_lines.pop()
                current.description = "\n".join(desc_lines)
        elif not header and idx > 0 and not items:
            carried = lines[idx - 1]
        title, company = _split_header(header or carried)

        # The role or the company can sit on its own line right under the dates
        following = lines[idx + 1] if idx + 1 < len(lines) else ""
        company_first = bool(COMPANY_HINT.search(title))
        if _is_label(following) and (company_first or (carried and not company)):
            # "PT Example - City" (or just the employer) with the dates, the role underneath
            title, company, skip_next = following.strip(), (header or carried), True
        elif _is_label(following) and not company and COMPANY_HINT.search(following):
            company, skip_next = following.strip(), True
        elif company_first and company and not COMPANY_HINT.search(company):
            title, company = company, title  # "PT Example, Drafter"

        current = ExperienceItem(
            title=title,
            company=company,
            start=str((start - 1) // 12),
            end="present" if match.group("present") else str((end - 1) // 12),
            months=end - start,
        )
        items.append(current)
        intervals.append((start, end))
    total, last_end = 0, 0
    for start, end in sorted(intervals):  # merge overlapping periods
        start = max(start, last_end)
        if end > start:
            total += end - start
            last_end = end
    return items, total


ONGOING_WORD = re.compile(rf"\b(?:{PRESENT}|ongoing|berjalan)\b", re.IGNORECASE)
END_DATE = re.compile(
    rf"(?:(?P<m>{MONTH})\s+)?(?P<y>(?:19|20)\d{{2}})(?!.*(?:19|20)\d{{2}})", re.IGNORECASE
)
COMPLETION_NOTE = re.compile(
    r"expected|perkiraan|selesai|lulus|graduat|completion|ongoing|berjalan", re.IGNORECASE
)
STUDY_CUE = re.compile(
    r"jurusan|program studi|prodi|fakultas|faculty|department|major|teknik|engineering|studies|ilmu",
    re.IGNORECASE,
)
NOT_A_DEGREE = re.compile(
    r"^\s*(?:relevant coursework|coursework|mata kuliah|gpa|ipk|thesis|skripsi|tugas akhir"
    r"|journal|jurnal|publication|publikasi)\b",
    re.IGNORECASE,
)


def _is_ongoing(line: str, today: date) -> bool:
    """True when the study period on this line has not ended: "2021 - Present", or an end date still ahead."""
    if ONGOING_WORD.search(line):
        return True
    end = END_DATE.search(line)
    if not end:
        return False
    if not end.group("m"):
        return int(end.group("y")) > today.year  # "2026" alone: graduated some time that year
    return _month_index(end.group("y"), end.group("m"), 12) > today.year * 12 + today.month


def parse_education(
    section: str, today: date | None = None
) -> tuple[list[EducationItem], list[EducationItem]]:
    """Returns (completed, in_progress). Only completed entries count as a degree held."""
    today = today or date.today()
    items: list[EducationItem] = []
    ongoing: list[bool] = []
    dated: list[bool] = []  # whether the entry's study period is already known
    pending: bool | None = None  # a period printed above the degree it belongs to
    lines_since_item = 0
    for line in section.splitlines():
        lines_since_item += 1
        low = line.lower()
        if NOT_A_DEGREE.match(line):
            continue
        level = next((lvl for lvl, pat in DEGREES if re.search(pat, low)), 0)
        field = next((name for name, pat in FIELDS.items() if re.search(pat, low)), "")
        has_period = bool(ONGOING_WORD.search(line) or END_DATE.search(line))
        if not (level or field):
            if has_period:
                # A period on its own line belongs to the entry just above it ("Expected
                # completion Oct 2023"), or else to the degree printed underneath.
                follows_entry = (
                    bool(items)
                    and not dated[-1]
                    and INSTITUTION_MARK not in line
                    and (lines_since_item <= 2 or bool(COMPLETION_NOTE.search(line)))
                )
                if follows_entry:
                    ongoing[-1], dated[-1] = _is_ongoing(line, today), True
                else:
                    pending = _is_ongoing(line, today)
            continue
        if not level and not has_period and not STUDY_CUE.search(line):
            continue  # a stray word such as "Time Management" is not a field of study
        open_entry = bool(items) and not dated[-1] and not has_period
        if open_entry and not items[-1].field and field and not level:
            items[-1].field = field
            continue
        if open_entry and items[-1].level == 0 and level and not field:
            items[-1].level = level
            continue
        items.append(EducationItem(degree=line.strip()[:120], level=level, field=field))
        ongoing.append(_is_ongoing(line, today) if has_period else bool(pending))
        dated.append(has_period or pending is not None)
        pending, lines_since_item = None, 0
    completed = [item for item, running in zip(items, ongoing, strict=True) if not running]
    in_progress = [item for item, running in zip(items, ongoing, strict=True) if running]
    return completed, in_progress


EXPERIENCE_NOT_FOUND = "Bagian pengalaman kerja tidak ditemukan"
EXPERIENCE_NO_ENTRIES = (
    "Bagian pengalaman kerja ditemukan, tetapi tidak ada jabatan bertanggal yang terbaca"
)
EDUCATION_NOT_READ = "Bagian pendidikan tidak terbaca"
EDUCATION_IN_PROGRESS_ONLY = (
    "Pendidikan yang terbaca masih ditempuh; belum ada jenjang yang selesai"
)


def section_confidence(
    sections: dict[str, str],
    experiences: list[ExperienceItem],
    education: list[EducationItem],
    education_in_progress: list[EducationItem],
    skills: list[str],
) -> dict[str, float]:
    """How well each section was read, from 0 (not found) to 1 (found and fully structured).

    0 means "unknown", not "the candidate has none": scoring leaves such a component out.
    """
    if experiences:
        titled = sum(1 for item in experiences if len(item.title) >= 3)
        experience = 0.6 + 0.4 * titled / len(experiences)
    else:
        experience = 0.3 if sections.get("experience") else 0.0

    studies = education + education_in_progress
    if studies:
        has_level = any(item.level for item in studies)
        has_field = any(item.field for item in studies)
        schooling = 0.6 + 0.2 * has_level + 0.2 * has_field
    else:
        schooling = 0.3 if sections.get("education") else 0.0

    if not skills:
        skill = 0.0
    else:
        skill = 1.0 if sections.get("skills") else 0.7
    return {
        "summary": 1.0 if sections.get("summary") else 0.0,
        "experience": round(experience, 2),
        "education": round(schooling, 2),
        "skills": skill,
    }


def extract(candidate_id: str, redacted_text: str, today: date | None = None) -> CandidateProfile:
    sections = split_sections(redacted_text)
    warnings: list[str] = []

    experiences, total_months = parse_experiences(sections.get("experience", ""), today)
    if not sections.get("experience"):
        warnings.append(EXPERIENCE_NOT_FOUND)
    elif not experiences:
        warnings.append(EXPERIENCE_NO_ENTRIES)
    education, education_in_progress = parse_education(sections.get("education", ""), today)
    if not education:
        warnings.append(EDUCATION_IN_PROGRESS_ONLY if education_in_progress else EDUCATION_NOT_READ)

    skills = taxonomy.find_skills(redacted_text)
    order = ("summary", "experience", "skills", "other", "education")
    if not sections.get("experience"):
        # No recognised structure: keep the unclassified text so it can still be matched
        order = ("header", *order)
    body = "\n".join(sections.get(k, "") for k in order)
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
        education_in_progress=education_in_progress,
        skills=skills,
        chunks=chunks,
        extraction_confidence=min(confidence, 1.0),
        section_confidence=section_confidence(
            sections, experiences, education, education_in_progress, skills
        ),
        warnings=warnings,
    )
