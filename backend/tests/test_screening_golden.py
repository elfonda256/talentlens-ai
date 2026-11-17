"""Regression guard for scoring: results must match the original PoC pipeline.

`fixtures/golden_screening.json` was produced by running the original `cv-screening-poc`
pipeline (TF-IDF embeddings, NumPy vector store) on `fixtures/jobs/junior_architect.txt`
and the text-based CVs in `fixtures/cvs/`. The new pipeline searches with FAISS instead,
so identical results show the swap did not change the scoring.
"""

import json

import pytest

from tests.conftest import FIXTURES

GOLDEN = json.loads((FIXTURES / "golden_screening.json").read_text(encoding="utf-8"))


def test_job_criteria_match_original_parser(screened):
    service, job_id = screened

    job = service.get_job(job_id)

    assert job.model_dump(exclude={"job_id", "raw_text"}) == GOLDEN["job"]


def test_scores_and_decisions_match_original_pipeline(screened):
    service, job_id = screened
    results, backend = service.get_ranking(job_id)
    file_names = {c.candidate_id: c.file_name for c in service.list_candidates(job_id)}

    assert backend == "tfidf"
    assert len(results) == len(GOLDEN["results"]) == 13
    for result in results:
        expected = GOLDEN["results"][file_names[result.candidate_id]]
        assert result.rank == expected["rank"]
        assert result.score == pytest.approx(expected["score"], abs=0.05)
        assert result.recommendation == expected["recommendation"]
        assert result.breakdown.model_dump() == pytest.approx(expected["breakdown"], abs=0.002)
        assert result.matched_skills == expected["matched_skills"]
        assert result.missing_must_skills == expected["missing_must_skills"]
        assert result.knockout_flags == expected["knockout_flags"]
        assert result.reasons == expected["reasons"]
