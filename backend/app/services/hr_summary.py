"""HR summary: a short narrative that explains an existing screening result.

The LLM (Gemini) never scores or ranks. It receives the facts the deterministic pipeline
already computed and only puts them into words. It never receives the candidate's name,
contact details or any other redacted attribute. Without an API key, or when the call
fails, the deterministic narrative is returned instead, labelled as a template.
"""

from __future__ import annotations

import json
import logging

import httpx

from app.core.config import Settings
from app.schemas.screening import HRSummary, JobProfile, ScreeningResult

logger = logging.getLogger(__name__)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

PROMPT = """Anda membantu tim HR memahami hasil penyaringan CV yang SUDAH dihitung oleh sistem.

Aturan:
- Jangan menghitung, mengubah, atau menilai ulang skor, peringkat, maupun rekomendasi.
- Gunakan HANYA fakta pada data di bawah. Jangan menambah fakta, dugaan, atau data pribadi.
- Tulis dalam Bahasa Indonesia yang profesional, 4 sampai 6 kalimat, tanpa daftar butir.
- Urutan isi: rekomendasi dan skor, kekuatan utama, kekurangan atau hal yang perlu diperiksa,
  lalu saran tindak lanjut untuk HR.

Data hasil penyaringan (JSON):
{facts}
"""


def build_facts(job: JobProfile, result: ScreeningResult) -> dict:
    """The only information that leaves the system. Contains no personal data."""
    return {
        "posisi": job.title,
        "minimal_pengalaman_tahun": job.min_years_experience,
        "peringkat": result.rank,
        "skor": result.score,
        "rekomendasi_sistem": result.recommendation,
        "kontribusi_skor": result.contributions,
        "keterampilan_cocok": result.matched_skills,
        "keterampilan_wajib_tidak_ditemukan": result.missing_must_skills,
        "keterampilan_tambahan_tidak_ditemukan": result.missing_nice_skills,
        "syarat_wajib_tidak_terpenuhi": result.knockout_flags,
        "alasan_sistem": result.reasons,
        "bukti_dari_cv": [
            {"syarat": e.requirement, "kutipan": e.best_match} for e in result.evidence[:3]
        ],
    }


def generate_hr_summary(
    job: JobProfile,
    result: ScreeningResult,
    settings: Settings,
    client: httpx.Client | None = None,
) -> HRSummary:
    if not settings.gemini_api_key:
        return HRSummary(
            text=result.narrative, source="template", note="GEMINI_API_KEY belum diatur"
        )
    try:
        text = _ask_gemini(build_facts(job, result), settings, client)
    except (httpx.HTTPError, KeyError, IndexError, ValueError) as error:
        logger.warning("Gemini summary failed (%s); using the template", type(error).__name__)
        return HRSummary(
            text=result.narrative,
            source="template",
            note=f"Gemini tidak dapat dihubungi ({type(error).__name__})",
        )
    logger.info(
        "Gemini summary generated for %s with %s", result.candidate_id, settings.gemini_model
    )
    return HRSummary(text=text, source="gemini", model=settings.gemini_model)


def _ask_gemini(facts: dict, settings: Settings, client: httpx.Client | None) -> str:
    prompt = PROMPT.format(facts=json.dumps(facts, ensure_ascii=False, indent=1))
    http = client or httpx.Client(timeout=settings.gemini_timeout_seconds)
    try:
        response = http.post(
            GEMINI_URL.format(model=settings.gemini_model),
            headers={"x-goog-api-key": settings.gemini_api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
        )
        response.raise_for_status()
    finally:
        if client is None:
            http.close()
    parts = response.json()["candidates"][0]["content"]["parts"]
    text = "".join(part.get("text", "") for part in parts if not part.get("thought")).strip()
    if not text:
        raise ValueError("Gemini returned an empty answer")
    return text
