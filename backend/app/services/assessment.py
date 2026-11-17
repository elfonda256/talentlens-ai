"""What HR should do with a candidate, how firm the assessment is, and what to check first.

Everything here is read from a screening result that already exists. Nothing changes a score,
a rank or a recommendation: these are the same facts arranged as a hiring decision aid.
"""

from app.core.config import Settings
from app.schemas.cv import CandidateProfile
from app.schemas.screening import (
    Assessment,
    AssessmentConfidence,
    HiringRecommendation,
    JobProfile,
    ScreeningResult,
)
from app.services import matching
from app.services.match_breakdown import EDUCATION_MISMATCH_FLAG, IMPLIED_SUFFIX

LEVEL_BELOW_FLAG = "Jenjang pendidikan di bawah yang disyaratkan"
# A score this close to a decision threshold could fall on the other side with a small change
# in the CV, so the decision is less firm.
NEAR_THRESHOLD_POINTS = 5.0
# "Highly recommended": shortlisted, with a score this far above the shortlist threshold,
# and an assessment that is firm.
HIGHLY_RECOMMENDED_MARGIN = 10.0
# Relevant experience this far above the minimum may mean the role is too junior.
OVERQUALIFIED_EXTRA_YEARS = 4.0
MAX_RISKS = 5
SECTION_LABELS = {"experience": "pengalaman kerja", "education": "pendidikan"}


def build_assessment(
    job: JobProfile, profile: CandidateProfile, result: ScreeningResult, settings: Settings
) -> Assessment:
    implied = [
        s.removesuffix(IMPLIED_SUFFIX) for s in result.matched_skills if s.endswith(IMPLIED_SUFFIX)
    ]
    relevant_years = matching.relevant_months(job, profile) / 12
    confidence = _confidence(profile, result, settings, implied)
    return Assessment(
        hiring=_hiring(job, result, implied),
        confidence=confidence,
        risks=_risks(job, profile, result, implied, relevant_years),
        highly_recommended=(
            result.recommendation == "SHORTLIST"
            and confidence.level == "high"
            and result.score >= settings.shortlist_threshold + HIGHLY_RECOMMENDED_MARGIN
        ),
    )


def _confidence(
    profile: CandidateProfile, result: ScreeningResult, settings: Settings, implied: list[str]
) -> AssessmentConfidence:
    """How firm the decision is: is the CV fully read, and is the score clear of a threshold?"""
    low, medium = [], []
    if result.unassessed:
        low.append(
            f"Bagian {_join([SECTION_LABELS[k] for k in result.unassessed])} tidak terbaca dari CV"
        )
    if profile.extraction_method == "ocr":
        medium.append(
            "CV berupa hasil pindai, sehingga sebagian teks mungkin tidak terbaca sempurna"
        )
    partly_read = [
        SECTION_LABELS[key]
        for key in ("experience", "education")
        if 0 < profile.section_confidence.get(key, 1.0) < 0.6
    ]
    if partly_read:
        medium.append(f"Bagian {_join(partly_read)} hanya terbaca sebagian")
    for threshold in (settings.shortlist_threshold, settings.reject_threshold):
        if abs(result.score - threshold) < NEAR_THRESHOLD_POINTS:
            medium.append(f"Skor berada dekat batas keputusan ({threshold:g})")
    if implied:
        medium.append(f"{len(implied)} keterampilan wajib hanya terindikasi, belum tertulis jelas")

    if low:
        return AssessmentConfidence(level="low", reasons=low + medium)
    if medium:
        return AssessmentConfidence(level="medium", reasons=medium)
    return AssessmentConfidence(
        level="high",
        reasons=[
            "Bagian pengalaman, pendidikan, dan keterampilan terbaca lengkap",
            "Skor jauh dari batas keputusan",
        ],
    )


def _hiring(job: JobProfile, result: ScreeningResult, implied: list[str]) -> HiringRecommendation:
    missing = result.missing_must_skills
    if result.recommendation == "SHORTLIST":
        steps = ["Jadwalkan wawancara dengan hiring manager"]
        steps += [f"Konfirmasi pengalaman dengan {skill} saat wawancara" for skill in missing[:2]]
        steps += [f"Minta contoh proyek yang menunjukkan {skill}" for skill in implied[:1]]
        return HiringRecommendation(
            decision="SHORTLIST",
            title="Lanjutkan ke wawancara",
            summary=f"Memenuhi syarat wajib {job.title} dan skornya di atas batas rekomendasi.",
            next_steps=steps[:4],
        )
    if result.recommendation == "REVIEW":
        steps = []
        if result.unassessed:
            sections = _join([SECTION_LABELS[k] for k in result.unassessed])
            steps.append(f"Buka CV asli dan periksa bagian {sections}")
            summary = "CV tidak terbaca lengkap, sehingga penilaian perlu dilengkapi secara manual."
        elif result.knockout_flags:
            summary = "Ada syarat wajib yang belum terpenuhi; tentukan apakah masih dapat diterima."
            steps += [
                f"Putuskan apakah ini dapat ditoleransi: {flag.lower()}"
                for flag in result.knockout_flags[:2]
            ]
        else:
            summary = "Kecocokannya sebagian; bandingkan dengan kandidat lain sebelum memutuskan."
        steps += [
            f"Telusuri pengalaman dengan {skill} lewat wawancara singkat" for skill in missing[:2]
        ]
        steps.append("Bandingkan dengan kandidat di peringkat atas")
        return HiringRecommendation(
            decision="REVIEW",
            title="Tinjau sebelum memutuskan",
            summary=summary,
            next_steps=steps[:4],
        )
    return HiringRecommendation(
        decision="REJECT",
        title="Belum sesuai untuk posisi ini",
        summary="Keterampilan, pengalaman, atau pendidikannya di bawah kebutuhan posisi ini.",
        next_steps=[
            "Kirim pemberitahuan hasil seleksi kepada kandidat",
            "Simpan profil untuk lowongan lain yang lebih sesuai",
        ],
    )


def _risks(
    job: JobProfile,
    profile: CandidateProfile,
    result: ScreeningResult,
    implied: list[str],
    relevant_years: float,
) -> list[str]:
    risks = []
    if result.unassessed:
        sections = _join([SECTION_LABELS[k] for k in result.unassessed])
        risks.append(
            f"Bagian {sections} belum dapat dinilai; keputusan bergantung pada pemeriksaan manual."
        )
    if len(result.missing_must_skills) >= 3:
        risks.append(
            f"{len(result.missing_must_skills)} keterampilan wajib belum terlihat di CV; "
            "kemungkinan perlu masa adaptasi."
        )
    elif result.missing_must_skills:
        risks.append(f"Belum terlihat di CV: {_join(result.missing_must_skills)}.")
    if implied:
        risks.append(f"Perlu dikonfirmasi karena hanya tersirat: {_join(implied)}.")
    experience_flag = next((f for f in result.knockout_flags if f.startswith("Pengalaman")), None)
    if experience_flag:
        risks.append(
            f"Pengalaman relevan baru {relevant_years:.1f}".replace(".", ",")
            + f" tahun, di bawah syarat {job.min_years_experience:g} tahun."
        )
    if EDUCATION_MISMATCH_FLAG in result.knockout_flags:
        risks.append("Bidang pendidikan yang sudah selesai berbeda dari yang diminta.")
    if LEVEL_BELOW_FLAG in result.knockout_flags:
        risks.append("Jenjang pendidikan di bawah yang disyaratkan.")
    if profile.education_in_progress:
        risks.append("Masih menempuh pendidikan; pastikan ketersediaan waktu kerja.")
    if (
        job.min_years_experience > 0
        and not result.unassessed
        and relevant_years >= job.min_years_experience + OVERQUALIFIED_EXTRA_YEARS
    ):
        risks.append("Pengalaman jauh di atas syarat; pastikan ekspektasi peran dan gaji sejalan.")
    if profile.extraction_method == "ocr":
        risks.append("CV hasil pindai; cocokkan angka dan tanggal penting dengan dokumen asli.")
    return risks[:MAX_RISKS]


def _join(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " dan " + items[-1]
