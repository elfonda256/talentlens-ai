"""Screening service: orchestrates the pipeline from uploaded documents to a ranked list.

CV / JD files -> parsing -> candidate JSON -> embedding -> FAISS -> weighted score
              -> decision -> ranking -> (on request) HR summary
"""

from __future__ import annotations

import hashlib
import logging
import re
import time
from functools import lru_cache
from pathlib import Path

from app.core.config import Settings, get_settings
from app.schemas.cv import CandidateProfile
from app.schemas.screening import HRSummary, JobProfile, ScreeningResult
from app.services import explanation, jd_parsing, match_breakdown, matching, taxonomy
from app.services.cv_parsing import UnreadableDocumentError, parse_cv
from app.services.cv_parsing.document_loader import load_document
from app.services.cv_parsing.pii import EMAIL, PHONE
from app.services.embedding import Embedder, create_embedder
from app.services.hr_summary import generate_hr_summary
from app.services.store import JsonStore
from app.services.vector_index import FaissIndex

logger = logging.getLogger(__name__)

MIN_JOB_TEXT_CHARS = 40
RECALL_TOP_K = 50


class JobNotFoundError(Exception):
    pass


class CandidateNotFoundError(Exception):
    pass


class NotAJobDescriptionError(Exception):
    """The uploaded document looks like a CV, not a vacancy."""


class NotScreenedError(Exception):
    """The job has no screening result yet (or it was invalidated by a new upload)."""


class ScreeningService:
    def __init__(self, store: JsonStore, settings: Settings):
        self._store = store
        self._settings = settings
        self._embedder: Embedder | None = None

    # ---------- jobs ----------

    def create_job(self, path: Path) -> JobProfile:
        try:
            text, _ = load_document(path)
        except ValueError:
            raise
        except Exception as error:
            raise UnreadableDocumentError("Dokumen rusak atau tidak dapat dibaca") from error
        if len(text.strip()) < MIN_JOB_TEXT_CHARS:
            raise UnreadableDocumentError("Dokumen tidak berisi teks yang dapat dibaca")

        if _looks_like_cv(text):
            raise NotAJobDescriptionError(
                "Dokumen ini tampaknya sebuah CV, bukan deskripsi lowongan. "
                "Unggah berkas lowongan di sini, lalu unggah CV pada halaman lowongan."
            )

        title = next((line.strip() for line in text.splitlines() if line.strip()), "job")
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40] or "job"
        job_id = f"{slug}-{hashlib.sha256(text.encode()).hexdigest()[:6]}"
        job = jd_parsing.parse_job(job_id, text)
        self._store.save_job(job)
        logger.info(
            "Parsed job %s: min_years=%g degree_fields=%d skills=%d",
            job_id,
            job.min_years_experience,
            len(job.degree_fields),
            len(job.skills),
        )
        return job

    def list_jobs(self) -> list[JobProfile]:
        return self._store.list_jobs()

    def get_job(self, job_id: str) -> JobProfile:
        job = self._store.get_job(job_id)
        if job is None:
            raise JobNotFoundError(job_id)
        return job

    # ---------- candidates ----------

    def add_candidate(
        self, job_id: str, path: Path, file_name: str
    ) -> tuple[CandidateProfile, bool]:
        """Parse one CV for a job. Returns (profile, is_new)."""
        self.get_job(job_id)
        profile = parse_cv(path, file_name=file_name, today=self._settings.reference_date)
        return profile, self._store.add_candidate(job_id, profile)

    def list_candidates(self, job_id: str) -> list[CandidateProfile]:
        self.get_job(job_id)
        return self._store.list_candidates(job_id)

    def get_candidate(self, job_id: str, candidate_id: str) -> CandidateProfile:
        candidate = self._store.get_candidate(job_id, candidate_id)
        if candidate is None:
            raise CandidateNotFoundError(candidate_id)
        return candidate

    def is_screened(self, job_id: str) -> bool:
        return self._store.get_screening(job_id) is not None

    # ---------- screening ----------

    def screen(self, job_id: str) -> tuple[list[ScreeningResult], str]:
        started = time.perf_counter()
        job = self.get_job(job_id)
        candidates = self._store.list_candidates(job_id)
        embedder = self._get_embedder()

        corpus = [chunk for cand in candidates for chunk in cand.chunks]
        corpus += job.requirement_sentences + job.responsibility_sentences + [job.raw_text]
        corpus += [taxonomy.describe(skill_id) for skill_id in taxonomy.load()]
        embedder.fit(corpus)

        index = FaissIndex()
        for cand in candidates:
            if cand.chunks:
                index.add(cand.candidate_id, embedder.encode(cand.chunks, "passage"), cand.chunks)

        by_id = {cand.candidate_id: cand for cand in candidates}
        recalled = matching.recall_candidates(job, embedder, index, top_k=RECALL_TOP_K)
        # A candidate whose CV produced no chunks cannot be recalled but must still be scored.
        order = recalled + [cid for cid in by_id if cid not in recalled]

        results = []
        for candidate_id in order:
            cand = by_id[candidate_id]
            scored = matching.score_candidate(job, cand, embedder, index)
            recommendation, notes = explanation.decide(
                scored["score"],
                scored["knockout_flags"],
                cand,
                self._settings.shortlist_threshold,
                self._settings.reject_threshold,
            )
            reasons, narrative = explanation.build_reasons(job, cand, scored, recommendation, notes)
            results.append(
                ScreeningResult(
                    candidate_id=candidate_id,
                    job_id=job_id,
                    score=scored["score"],
                    breakdown=scored["breakdown"],
                    contributions=scored["contributions"],
                    matched_skills=scored["matched_skills"],
                    missing_must_skills=scored["missing_must_skills"],
                    missing_nice_skills=scored["missing_nice_skills"],
                    knockout_flags=scored["knockout_flags"],
                    evidence=scored["evidence"][:6],
                    recommendation=recommendation,
                    reasons=reasons,
                    narrative=narrative,
                )
            )
        results.sort(key=lambda r: (-r.score, r.candidate_id))
        for rank, result in enumerate(results, start=1):
            result.rank = rank
        self._store.save_screening(job_id, results, embedder.name)
        logger.info(
            "Screened job %s: candidates=%d chunks=%d embedder=%s in %.0f ms",
            job_id,
            len(results),
            len(index),
            embedder.name,
            (time.perf_counter() - started) * 1000,
        )
        return results, embedder.name

    def get_ranking(self, job_id: str) -> tuple[list[ScreeningResult], str]:
        self.get_job(job_id)
        screening = self._store.get_screening(job_id)
        if screening is None:
            raise NotScreenedError(job_id)
        return screening

    def get_result(self, job_id: str, candidate_id: str) -> ScreeningResult:
        results, _ = self.get_ranking(job_id)
        for result in results:
            if result.candidate_id == candidate_id:
                return result
        raise CandidateNotFoundError(candidate_id)

    # ---------- HR summary ----------

    def summarize(self, job_id: str, candidate_id: str, refresh: bool = False) -> HRSummary:
        result = self.get_result(job_id, candidate_id)
        cached = self._store.get_summary(job_id, candidate_id)
        if cached and not refresh:
            return cached
        job = self.get_job(job_id)
        profile = self.get_candidate(job_id, candidate_id)
        breakdown = match_breakdown.build_breakdown(job, profile, result)
        summary = generate_hr_summary(job, profile, result, breakdown, self._settings)
        if summary.source == "gemini":  # a template is cheap to rebuild and may be upgraded later
            self._store.save_summary(job_id, candidate_id, summary)
        return summary

    def _get_embedder(self) -> Embedder:
        if self._embedder is None:  # loading a model takes seconds, so it is done once
            self._embedder = create_embedder(self._settings)
        return self._embedder


# A short line that names a vacancy section, in English or Indonesian ("Job Requirements:").
JOB_SECTION_HEADING = re.compile(
    r"^[^\n]{0,25}\b(requirements?|qualifications?|responsibilit(?:y|ies)|job description|"
    r"kualifikasi|persyaratan|syarat|kriteria|tanggung jawab|deskripsi pekerjaan)\b[^\n]{0,15}$",
    re.IGNORECASE | re.MULTILINE,
)


def _looks_like_cv(text: str) -> bool:
    """A vacancy has requirement headings; a CV has personal contact details instead."""
    has_job_heading = JOB_SECTION_HEADING.search(text) is not None
    has_contact = EMAIL.search(text) is not None or PHONE.search(text) is not None
    return has_contact and not has_job_heading


@lru_cache
def get_screening_service() -> ScreeningService:
    settings = get_settings()
    return ScreeningService(JsonStore(settings.storage_dir / "state.json"), settings)
