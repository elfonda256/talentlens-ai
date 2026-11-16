"""PII redaction for blind screening.

Personal attributes are removed BEFORE extraction, embedding or any LLM call, so they
cannot influence a score. Their values are returned separately, only so the candidate
can be contacted after a decision is made.
"""

from __future__ import annotations

import re

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?:\+62|62|0)8[\d\s-]{7,13}\d")
# A campus name can be a proxy for religion, region or social status, so it is masked
INSTITUTION = re.compile(
    r"\b(?:Universitas|Institut|Politeknik|Sekolah Tinggi|Akademi|University|Institute|Polytechnic|College)\b[^,\n|]*",
    re.IGNORECASE,
)
LONG_ID = re.compile(r"\b\d{16}\b")  # national ID pattern: removed and never stored

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
        pii["phone"] = re.sub(r"[\s-]", "", phone.group(0))
    redacted = EMAIL.sub("[EMAIL]", redacted)
    redacted = PHONE.sub("[TELEPON]", redacted)
    redacted = LONG_ID.sub("[ID]", redacted)
    institutions = INSTITUTION.findall(redacted)
    if institutions:
        pii["institution"] = "; ".join(i.strip() for i in institutions)
        redacted = INSTITUTION.sub("[INSTITUSI]", redacted)

    name = pii.get("name")
    if name:
        redacted = re.sub(re.escape(name), "[NAMA]", redacted, flags=re.IGNORECASE)
    return redacted, pii
