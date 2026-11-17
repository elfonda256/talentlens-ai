"""Hiring recommendation, confidence and risks are read from the result, never change it."""

import pytest

from app.services import assessment, matching
from app.services.screening import ScreeningService


@pytest.fixture
def ranked(screened, settings):
    service, job_id = screened
    job = service.get_job(job_id)
    results = service.get_ranking(job_id)[0]
    return [
        (
            result,
            assessment.build_assessment(
                job, service.get_candidate(job_id, result.candidate_id), result, settings
            ),
        )
        for result in results
    ]


def test_hiring_recommendation_follows_the_system_decision(ranked):
    titles = {
        "SHORTLIST": "Lanjutkan ke wawancara",
        "REVIEW": "Tinjau sebelum memutuskan",
        "REJECT": "Belum sesuai untuk posisi ini",
    }
    for result, view in ranked:
        assert view.hiring.decision == result.recommendation
        assert view.hiring.title == titles[result.recommendation]
        assert view.hiring.next_steps


def test_building_the_assessment_leaves_the_result_untouched(screened, settings):
    service, job_id = screened
    job = service.get_job(job_id)
    before = [r.model_dump() for r in service.get_ranking(job_id)[0]]

    for result in service.get_ranking(job_id)[0]:
        profile = service.get_candidate(job_id, result.candidate_id)
        assessment.build_assessment(job, profile, result, settings)

    assert [r.model_dump() for r in service.get_ranking(job_id)[0]] == before


def test_highly_recommended_needs_a_clear_shortlist_score_and_firm_confidence(ranked, settings):
    for result, view in ranked:
        expected = (
            result.recommendation == "SHORTLIST"
            and view.confidence.level == "high"
            and result.score >= settings.shortlist_threshold + 10
        )
        assert view.highly_recommended is expected
    assert any(view.highly_recommended for _, view in ranked)


def test_a_score_near_a_threshold_lowers_confidence(ranked, settings):
    for result, view in ranked:
        near = any(
            abs(result.score - t) < 5
            for t in (settings.shortlist_threshold, settings.reject_threshold)
        )
        if near:
            assert view.confidence.level != "high"
            assert any("dekat batas keputusan" in r for r in view.confidence.reasons)


def test_unread_sections_mean_low_confidence_and_a_manual_check(
    service: ScreeningService, settings, tmp_path
):
    from tests.conftest import SAMPLE_JOB

    job = service.create_job(SAMPLE_JOB)
    path = tmp_path / "unstructured.txt"
    path.write_text(
        "Tanpa Judul\\nSaya memakai AutoCAD dan SketchUp untuk gambar kerja.\\n", encoding="utf-8"
    )
    profile, _ = service.add_candidate(job.job_id, path, path.name)
    service.screen(job.job_id)
    result = service.get_result(job.job_id, profile.candidate_id)

    view = assessment.build_assessment(job, profile, result, settings)

    assert view.confidence.level == "low"
    assert view.hiring.decision == "REVIEW"
    assert view.hiring.next_steps[0].startswith("Buka CV asli")
    assert any("belum dapat dinilai" in risk for risk in view.risks)
    assert view.highly_recommended is False


def test_missing_and_implied_skills_appear_as_risks(ranked):
    for result, view in ranked:
        if result.missing_must_skills:
            assert any(
                skill in risk for risk in view.risks for skill in result.missing_must_skills
            ) or any("keterampilan wajib belum terlihat" in risk for risk in view.risks)
        assert len(view.risks) <= assessment.MAX_RISKS


def test_implied_count_names_must_and_bonus_skills_separately(screened):
    service, job_id = screened
    job = service.get_job(job_id)
    units = matching.requirement_units(job)
    must = next(u["label"] for u in units if u["priority"] == "must")
    bonus = next(u["label"] for u in units if u["priority"] == "nice")

    assert assessment._implied_count(job, [must]) == "1 keterampilan wajib"
    assert assessment._implied_count(job, [bonus]) == "1 keterampilan tambahan"
    assert (
        assessment._implied_count(job, [must, bonus])
        == "1 keterampilan wajib dan 1 keterampilan tambahan"
    )


def test_ranking_and_detail_responses_carry_the_assessment(screened, settings):
    from fastapi.testclient import TestClient

    from app.core.config import get_settings
    from app.main import app
    from app.services.screening import get_screening_service

    service, job_id = screened
    app.dependency_overrides[get_screening_service] = lambda: service
    app.dependency_overrides[get_settings] = lambda: settings
    try:
        client = TestClient(app)
        row = client.get(f"/api/v1/jobs/{job_id}/ranking").json()["results"][0]
        detail = client.get(f"/api/v1/jobs/{job_id}/candidates/{row['candidate_id']}").json()
    finally:
        app.dependency_overrides.clear()

    assert row["assessment"] == detail["assessment"]
    assert set(detail["assessment"]) == {"hiring", "confidence", "risks", "highly_recommended"}
