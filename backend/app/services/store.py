"""Small JSON-file store for jobs, parsed candidates, screening results and HR summaries.

Enough for a single-user proof of concept; the same Pydantic models would map onto
database tables. The file contains personal data and must never be committed.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

from app.schemas.cv import CandidateProfile
from app.schemas.screening import HRSummary, JobProfile, ScreeningResult


class JsonStore:
    def __init__(self, path: Path):
        self._path = path
        self._lock = threading.Lock()
        self._state = {"jobs": {}, "candidates": {}, "screenings": {}, "summaries": {}}
        if path.exists():
            self._state.update(json.loads(path.read_text(encoding="utf-8")))

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(self._state, ensure_ascii=False), encoding="utf-8")

    # ---------- jobs ----------

    def save_job(self, job: JobProfile) -> None:
        with self._lock:
            self._state["jobs"][job.job_id] = job.model_dump()
            self._state["candidates"].setdefault(job.job_id, {})
            self._save()

    def get_job(self, job_id: str) -> JobProfile | None:
        data = self._state["jobs"].get(job_id)
        return JobProfile(**data) if data else None

    def list_jobs(self) -> list[JobProfile]:
        return [JobProfile(**data) for data in self._state["jobs"].values()]

    # ---------- candidates ----------

    def add_candidate(self, job_id: str, profile: CandidateProfile) -> bool:
        """Returns False when this candidate already applied to the job."""
        with self._lock:
            candidates = self._state["candidates"].setdefault(job_id, {})
            if profile.candidate_id in candidates:
                return False
            candidates[profile.candidate_id] = profile.model_dump()
            self._invalidate_screening(job_id)
            self._save()
            return True

    def list_candidates(self, job_id: str) -> list[CandidateProfile]:
        return [CandidateProfile(**c) for c in self._state["candidates"].get(job_id, {}).values()]

    def get_candidate(self, job_id: str, candidate_id: str) -> CandidateProfile | None:
        data = self._state["candidates"].get(job_id, {}).get(candidate_id)
        return CandidateProfile(**data) if data else None

    # ---------- screening results ----------

    def save_screening(
        self, job_id: str, results: list[ScreeningResult], embedding_backend: str
    ) -> None:
        with self._lock:
            self._state["screenings"][job_id] = {
                "embedding_backend": embedding_backend,
                "results": [r.model_dump() for r in results],
            }
            self._state["summaries"].pop(job_id, None)  # summaries describe the old ranking
            self._save()

    def get_screening(self, job_id: str) -> tuple[list[ScreeningResult], str] | None:
        data = self._state["screenings"].get(job_id)
        if not data:
            return None
        return [ScreeningResult(**r) for r in data["results"]], data["embedding_backend"]

    def _invalidate_screening(self, job_id: str) -> None:
        self._state["screenings"].pop(job_id, None)
        self._state["summaries"].pop(job_id, None)

    # ---------- HR summaries ----------

    def save_summary(self, job_id: str, candidate_id: str, summary: HRSummary) -> None:
        with self._lock:
            self._state["summaries"].setdefault(job_id, {})[candidate_id] = summary.model_dump()
            self._save()

    def get_summary(self, job_id: str, candidate_id: str) -> HRSummary | None:
        data = self._state["summaries"].get(job_id, {}).get(candidate_id)
        return HRSummary(**data) if data else None
