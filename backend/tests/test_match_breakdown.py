"""The explanation views must describe the score exactly, without ever changing it."""

import pytest

from app.services import taxonomy
from app.services.match_breakdown import build_breakdown, build_highlights
from tests.conftest import SAMPLE_CVS


def view(screened, file_name):
    service, job_id = screened
    job = service.get_job(job_id)
    profile = next(c for c in service.list_candidates(job_id) if c.file_name == file_name)
    result = service.get_result(job_id, profile.candidate_id)
    return job, profile, result, build_breakdown(job, profile, result)


def test_component_points_add_up_to_the_score(screened):
    service, job_id = screened
    for result in service.get_ranking(job_id)[0]:
        profile = service.get_candidate(job_id, result.candidate_id)
        rows = {
            c.key: c for c in build_breakdown(service.get_job(job_id), profile, result).components
        }

        assert list(rows) == ["must_skills", "bonus_skills", "experience", "education", "semantic"]
        assert sum(c.max_points for c in rows.values()) == pytest.approx(100, abs=0.2)
        assert sum(c.points for c in rows.values()) == pytest.approx(result.score, abs=0.25)
        # Must-have and bonus rows are the skills component, split; the rest are shown as scored.
        skills = rows["must_skills"].points + rows["bonus_skills"].points
        assert skills == pytest.approx(result.contributions["skills"], abs=0.11)
        assert rows["must_skills"].max_points + rows["bonus_skills"].max_points == pytest.approx(35)
        for key in ("experience", "education", "semantic"):
            assert rows[key].points == result.contributions[key]
        for row in rows.values():
            assert 0 <= row.points <= row.max_points + 0.05 and row.explanation


def test_must_and_bonus_split_follows_the_matcher_weights(screened):
    _, _, _, breakdown = view(screened, "cv_raka.pdf")
    rows = {c.key: c for c in breakdown.components}

    # 9 must-have (weight 1) and 3 bonus (weight 0.5) requirements share 35 points as 9 : 1.5
    assert rows["must_skills"].max_points == 30.0
    assert rows["bonus_skills"].max_points == 5.0
    assert rows["must_skills"].score_percent == 100.0  # every must-have was found


def test_each_role_is_marked_by_how_much_it_counted(screened):
    _, profile, _, strong = view(screened, "cv_raka.pdf")
    _, _, _, engineer = view(screened, "cv_bayu.docx")
    _, _, _, accountant = view(screened, "cv_citra.txt")

    assert [r.relevance for r in strong.experiences] == ["relevant", "relevant"]
    assert "AutoCAD" in strong.experiences[0].terms
    assert strong.experiences[0].title == profile.experiences[0].title
    assert {r.relevance for r in accountant.experiences} == {"not_relevant"}
    assert "not_relevant" in {r.relevance for r in engineer.experiences}  # the site engineer role


def test_unmet_requirements_list_flags_and_missing_must_haves(screened):
    _, _, result, graduate = view(screened, "cv_sinta.pdf")
    _, _, _, strong = view(screened, "cv_raka.pdf")

    assert strong.unmet_requirements == []
    assert graduate.unmet_requirements[0].startswith("Pengalaman relevan 0.4 tahun")
    assert len(graduate.unmet_requirements) == len(result.knockout_flags) + len(
        result.missing_must_skills
    )


def test_skill_statuses_mirror_the_matcher_output(screened):
    _, _, result, breakdown = view(screened, "cv_dimas.pdf")

    must = {s.label: s.status for s in breakdown.must_have_skills}
    missing = sorted(label for label, status in must.items() if status == "missing")

    assert missing == sorted(result.missing_must_skills)
    assert must["Architectural Design / Interior Design"] == "matched"  # one alternative is enough
    assert must["AutoCAD"] == "matched"
    assert len(breakdown.must_have_skills) + len(breakdown.bonus_skills) == 12


def test_matched_skills_carry_the_words_found_in_the_cv(screened):
    _, profile, _, breakdown = view(screened, "cv_dimas.pdf")  # an Indonesian CV

    terms = {s.label: s.terms for s in breakdown.must_have_skills}

    assert (
        "Gambar Teknik" in terms["Technical Drawing"]
        or "gambar kerja" in terms["Technical Drawing"]
    )
    for found in (term for values in terms.values() for term in values):
        assert found.lower() in profile.redacted_text.lower()


def test_experience_and_education_views(screened):
    _, _, _, strong = view(screened, "cv_raka.pdf")
    _, _, _, graduate = view(screened, "cv_sinta.pdf")
    _, _, _, accountant = view(screened, "cv_citra.txt")
    _, _, _, engineer = view(screened, "cv_bayu.docx")

    assert (strong.experience.relevant_years, strong.experience.required_years) == (3.2, 2)
    assert strong.experience.met and strong.education.status == "match"
    assert not graduate.experience.met and graduate.education.status == "match"
    assert accountant.education.status == "mismatch"
    assert accountant.education.found_fields == ["accounting"]
    assert engineer.education.status == "related"  # civil engineering for an architecture role


def test_highlights_agree_with_the_breakdown(screened):
    job, profile, result, breakdown = view(screened, "cv_raka.pdf")

    highlights = build_highlights(job, profile, result)

    assert highlights.must_total == len(breakdown.must_have_skills) == 9
    assert highlights.must_matched == sum(s.status != "missing" for s in breakdown.must_have_skills)
    assert highlights.bonus_total == len(breakdown.bonus_skills) == 3
    assert highlights.relevant_years == breakdown.experience.relevant_years


def test_building_views_does_not_change_the_stored_result(screened):
    service, job_id = screened
    before = [r.model_dump() for r in service.get_ranking(job_id)[0]]

    for result in service.get_ranking(job_id)[0]:
        profile = service.get_candidate(job_id, result.candidate_id)
        build_breakdown(service.get_job(job_id), profile, result)

    assert [r.model_dump() for r in service.get_ranking(job_id)[0]] == before


def test_find_terms_returns_spellings_as_written():
    text = (SAMPLE_CVS / "cv_fajar.txt").read_text(encoding="utf-8")

    terms = taxonomy.find_terms(text)

    assert "AutoCAD" in terms["autocad"]
    assert {"gambar teknik", "shop drawing"} <= {t.lower() for t in terms["technical_drawing"]}
    assert "revit" not in terms
