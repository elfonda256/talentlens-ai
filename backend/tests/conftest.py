from datetime import date
from pathlib import Path

import pytest

from app.core.config import Settings
from app.services.screening import ScreeningService
from app.services.store import JsonStore

FIXTURES = Path(__file__).parent / "fixtures"
SAMPLE_CVS = FIXTURES / "cvs"
SAMPLE_JOB = FIXTURES / "jobs" / "junior_architect.txt"
# The golden snapshots were produced with this date as "today".
REFERENCE_DATE = date(2026, 11, 16)
# OCR output differs between Tesseract versions, so the scanned CV is kept out of exact comparisons.
TEXT_BASED_CVS = sorted(p for p in SAMPLE_CVS.iterdir() if "scan" not in p.name)


def make_settings(tmp_path: Path, **overrides) -> Settings:
    """Offline, deterministic settings: TF-IDF embeddings, fixed date, no LLM, temp storage."""
    values = {
        "embedding_backend": "tfidf",
        "reference_date": REFERENCE_DATE,
        "storage_dir": tmp_path,
        "gemini_api_key": "",
    }
    return Settings(**{**values, **overrides})


@pytest.fixture
def settings(tmp_path) -> Settings:
    return make_settings(tmp_path)


@pytest.fixture
def service(settings) -> ScreeningService:
    return ScreeningService(JsonStore(settings.storage_dir / "state.json"), settings)


@pytest.fixture
def screened(service) -> tuple[ScreeningService, str]:
    """A service with the sample job, every text-based sample CV and a finished screening."""
    job = service.create_job(SAMPLE_JOB)
    for path in TEXT_BASED_CVS:
        service.add_candidate(job.job_id, path, path.name)
    service.screen(job.job_id)
    return service, job.job_id
