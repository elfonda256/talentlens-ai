"""Decision rules and the deterministic explanation of a score.

Every score is broken down into per-component contributions plus evidence quoted from the CV.
The decision rules are deliberately conservative: nothing is rejected automatically when the
document was hard to read, and nothing is shortlisted automatically when a mandatory
requirement is missing.
"""

from __future__ import annotations

from app.schemas.cv import CandidateProfile
from app.schemas.screening import JobProfile

LABELS = {
    "skills": "Keterampilan",
    "experience": "Pengalaman relevan",
    "semantic": "Kesesuaian isi CV dengan JD",
    "education": "Pendidikan",
}


UNASSESSED_LABELS = {"experience": "pengalaman kerja", "education": "pendidikan"}


def decide(
    score: float,
    flags: list[str],
    cand: CandidateProfile,
    shortlist_at: float,
    reject_below: float,
    unassessed: list[str] | None = None,
) -> tuple[str, list[str]]:
    notes: list[str] = []
    if unassessed:
        sections = " dan ".join(UNASSESSED_LABELS[key] for key in unassessed)
        notes.append(
            f"Bagian {sections} tidak terbaca dari CV, sehingga belum dinilai dan skor ini "
            "bersifat sementara. Periksa CV aslinya sebelum memutuskan"
        )
        return "REVIEW", notes
    if score >= shortlist_at:
        if flags:
            notes.append(
                "Skor tinggi tetapi ada syarat wajib yang belum terpenuhi, sehingga perlu ditinjau HR"
            )
            return "REVIEW", notes
        return "SHORTLIST", notes
    if score >= reject_below:
        return "REVIEW", notes
    if cand.extraction_method == "ocr" or cand.extraction_confidence < 0.7:
        notes.append(
            "Skor rendah tetapi kualitas pembacaan dokumen meragukan, sehingga tidak ditolak otomatis"
        )
        return "REVIEW", notes
    return "REJECT", notes


def build_reasons(
    job: JobProfile, cand: CandidateProfile, scored: dict, recommendation: str, notes: list[str]
) -> tuple[list[str], str]:
    reasons: list[str] = []
    contrib = scored["contributions"]
    top = max(contrib, key=contrib.get)
    reasons.append(f"Kontributor skor terbesar: {LABELS[top]} ({contrib[top]:.1f} poin)")
    if scored["matched_skills"]:
        reasons.append("Keterampilan yang cocok: " + ", ".join(scored["matched_skills"][:8]))
    if scored["missing_must_skills"]:
        reasons.append(
            "Keterampilan wajib yang tidak ditemukan: " + ", ".join(scored["missing_must_skills"])
        )
    unassessed = scored.get("unassessed", [])
    if "experience" in unassessed:
        reasons.append(
            "Pengalaman: belum dapat dinilai karena bagian pengalaman kerja tidak terbaca"
        )
    else:
        reasons.append(
            f"Pengalaman relevan terhitung {scored['relevant_years']:.1f} tahun (syarat minimal {job.min_years_experience:g} tahun)"
        )
    fields = sorted({e.field for e in cand.education if e.field})
    reasons.append("Pendidikan: " + (", ".join(fields) if fields else "tidak terbaca"))
    reasons += scored["knockout_flags"] + notes + cand.warnings
    if scored["evidence"]:
        best = scored["evidence"][0]
        reasons.append(
            f'Bukti terkuat: "{best.best_match[:140]}" untuk syarat "{best.requirement[:90]}"'
        )

    verdict = {
        "SHORTLIST": "direkomendasikan lanjut ke wawancara",
        "REVIEW": "perlu ditinjau HR",
        "REJECT": "tidak direkomendasikan",
    }[recommendation]
    narrative = (
        f"Kandidat {verdict} untuk posisi {job.title} dengan skor {scored['score']:.1f}/100. "
        + " ".join(r if r.endswith(".") else r + "." for r in reasons[:5])
    )
    return reasons, narrative
