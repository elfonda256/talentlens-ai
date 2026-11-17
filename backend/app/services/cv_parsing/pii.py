"""PII redaction for blind screening.

Personal attributes are removed BEFORE extraction, embedding or any LLM call, so they
cannot influence a score. Their values are returned separately, only so the candidate
can be contacted after a decision is made.
"""

from __future__ import annotations

import re

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
# Indonesian mobile numbers as people type them: 0812..., +62 812..., +62-812-..., + 62812...
PHONE = re.compile(r"(?:\+\s?62|\b62|\b0)[\s-]?8[\d\s-]{6,13}\d")
LONG_ID = re.compile(r"\b\d{16}\b")  # national ID pattern: removed and never stored
# "born in Bandung, 19 February 2003" inside a sentence reveals age and origin
BIRTH = re.compile(r"\b(?:born|lahir)\b[^.]{0,80}?\b(?:19|20)\d{2}\b", re.IGNORECASE)
BIRTH_MARK = "[TANGGAL LAHIR]"
CONTACT_MARK = "[KONTAK]"
CONTACT_LINES = 8  # the contact block sits at the top of a CV
_PLACEHOLDER_ONLY = re.compile(r"\[(?:EMAIL|TELEPON)\]|[\s|,;:+\-/]")

# A campus name can be a proxy for religion, region or social status, so it is masked,
# including the proper nouns around the keyword ("Example State University of Technology").
_DEGREE_WORDS = (
    "Sarjana|Bachelors?|Master|Magister|Diploma|Doctor|Arsitektur|Architecture|Teknik"
    "|Engineering|Desain|Design|Interior|Jurusan|Fakultas|Faculty|Lulusan|Alumni|Graduated"
)
_NAME_WORD = r"[A-Z][A-Za-z.'-]+"
# A degree word right before the keyword is the degree, not part of the campus name
_LEADING_WORD = rf"(?!(?:{_DEGREE_WORDS})\b){_NAME_WORD}"
INSTITUTION = re.compile(
    rf"(?:{_LEADING_WORD}[ \t]+){{0,3}}"
    r"\b(?i:Universitas|Institut|Politeknik|Sekolah Tinggi|Akademi|University|Institute"
    r"|Polytechnic|College)\b"
    rf"(?:[ \t]+(?:of|Negeri|{_NAME_WORD}|\d+(?![\d-])))" + r"{0,5}"
)
INSTITUTION_MARK = "[INSTITUSI]"

# Labelled lines that carry sensitive attributes (common on Indonesian CVs)
SENSITIVE_LABELS = {
    "gender": r"jenis kelamin|gender|sex",
    "birth": r"tempat[,/ ]*\s*tanggal lahir|tanggal lahir|ttl|date of birth|place of birth|dob|born",
    "age": r"usia|umur|age",
    "religion": r"agama|religion",
    "marital_status": r"status pernikahan|status perkawinan|status|marital status",
    "nationality": r"kewarganegaraan|nationality|suku",
    "address": r"alamat|address|domisili",
    "photo": r"foto|photo",
}
LABEL_LINE = re.compile(
    r"^\s*(?P<label>" + "|".join(SENSITIVE_LABELS.values()) + r")\s*[:\-]\s*(?P<value>.+)$",
    re.IGNORECASE,
)
SECTION_HINT = re.compile(
    r"experience|pengalaman|education|pendidikan|skill|keahlian|keterampilan|summary|profil|ringkasan",
    re.IGNORECASE,
)


def _label_key(label: str) -> str:
    for key, pattern in SENSITIVE_LABELS.items():
        if re.fullmatch(pattern, label.strip(), re.IGNORECASE):
            return key
    return "other"


def mask(text: str) -> str:
    """Masks personal data that can sit anywhere in a text: email, phone, ID number, birth date.

    Used on the whole CV during redaction and again on every quote that leaves the system.
    """
    text = EMAIL.sub("[EMAIL]", text)
    text = PHONE.sub("[TELEPON]", text)
    text = LONG_ID.sub("[ID]", text)
    return BIRTH.sub(BIRTH_MARK, text)


def _mask_contact_lines(text: str) -> str:
    """A top line with an email or phone usually also carries the address, so all of it goes."""
    lines = text.splitlines()
    for i, line in enumerate(lines[:CONTACT_LINES]):
        has_contact = "[EMAIL]" in line or "[TELEPON]" in line
        if has_contact and _PLACEHOLDER_ONLY.sub("", line):
            lines[i] = CONTACT_MARK
    return "\n".join(lines)


def redact(text: str) -> tuple[str, dict[str, str]]:
    """Returns (redacted_text, pii)."""
    pii: dict[str, str] = {}
    lines = text.splitlines()

    # Name: the first non-empty line that is not a section heading
    for i, line in enumerate(lines[:5]):
        stripped = line.strip()
        if stripped and stripped.lower() not in {
            "curriculum vitae",
            "cv",
            "resume",
            "daftar riwayat hidup",
        }:
            if not SECTION_HINT.search(stripped) and len(stripped.split()) <= 5:
                pii["name"] = stripped.title()
                lines[i] = "[NAMA]"
            break

    out = []
    for line in lines:
        match = LABEL_LINE.match(line)
        if match:
            key = _label_key(match.group("label"))
            if key != "photo":
                pii[key] = match.group("value").strip()
            continue  # the whole sensitive line is dropped
        out.append(line)
    redacted = "\n".join(out)

    email = EMAIL.search(redacted)
    if email:
        pii["email"] = email.group(0)
    phone = PHONE.search(redacted)
    if phone:
        pii["phone"] = re.sub(r"[\s+-]", "", phone.group(0)).replace("+", "")
    redacted = _mask_contact_lines(mask(redacted))
    institutions = INSTITUTION.findall(redacted)
    if institutions:
        pii["institution"] = "; ".join(i.strip() for i in institutions)
        redacted = INSTITUTION.sub(INSTITUTION_MARK, redacted)

    name = pii.get("name")
    if name:
        redacted = re.sub(re.escape(name), "[NAMA]", redacted, flags=re.IGNORECASE)
    return redacted, pii
