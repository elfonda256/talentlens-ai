"""Regression tests from QA on real CVs.

The fixtures in `fixtures/real_layouts/` copy the layouts that broke the parser, with invented
content. Each test names the behaviour that was wrong before QA Phase 2.
"""

import re

import pytest

from app.services import hr_summary, match_breakdown
from app.services.cv_parsing import extractor, parse_cv, pii
from tests.conftest import FIXTURES, REFERENCE_DATE, SAMPLE_JOB

LAYOUTS = FIXTURES / "real_layouts"
REVIT_IMPLIED = "Revit / BIM (tersirat)"


def parse(name: str):
    return parse_cv(LAYOUTS / name, today=REFERENCE_DATE)


def roles(profile) -> list[tuple[str, str, int]]:
    return [(item.title, item.company, item.months) for item in profile.experiences]


# --- Section headings -------------------------------------------------------------------


@pytest.mark.parametrize(
    ("line", "section"),
    [
        ("Experience", "experience"),
        ("EXPERIENCES", "experience"),
        ("Work Experience:", "experience"),
        ("Work Experiences", "experience"),
        ("Employment History", "experience"),
        ("Professional Experience", "experience"),
        ("Career History", "experience"),
        ("Riwayat Kerja", "experience"),
        ("Riwayat Karier", "experience"),
        ("PENGALAMAN KERJA", "experience"),
        ("W O R K E X P E R I E N C E", "experience"),
        ("Education Level", "education"),
        ("Riwayat Pendidikan", "education"),
        ("E D U C A T I O N", "education"),
        ("Area of Expertise", "skills"),
        ("Soft & Hard Skills", "skills"),
        ("Organizational Experience", "other"),
        ("Organisational Experience", "other"),
        ("Licenses & Certifications", "other"),
    ],
)
def test_heading_variants_are_recognised(line, section):
    assert extractor.heading_of(line) == section


@pytest.mark.parametrize(
    "line",
    [
        "skills.",  # the last word of a wrapped sentence
        "A R C H I T E C T U R A L D R A F T E R",  # a letter-spaced job title
        "Experience in residential and commercial interior projects across Indonesia",
        "Architect",
    ],
)
def test_ordinary_lines_are_not_headings(line):
    assert extractor.heading_of(line) is None


# --- One test per real layout --------------------------------------------------------------


def test_heading_on_the_same_line_as_its_first_entry():
    profile = parse("inline_headings.txt")

    assert roles(profile) == [
        ("Interior Designer", "PT Ruang Contoh", 38),
        ("Architectural Drafter", "PT Garis Contoh Konsultan", 8),
        ("Interior Architect", "Studio Contoh", 46),
        ("kontraktor", "CV Bangun Contoh", 7),
    ]
    assert profile.total_experience_months == 99
    assert [(e.level, e.field) for e in profile.education] == [(4, "architecture")]
    assert profile.education_in_progress == []  # the expected completion date has passed
    assert {"autocad", "sketchup", "revit"} <= set(profile.skills)
    assert profile.chunks and profile.warnings == []


def test_plural_headings_with_employer_and_role_on_separate_lines():
    profile = parse("plural_headings.txt")

    assert roles(profile) == [
        ("Architect", "Freelancer", 58),
        ("Architectural Designer Intern", "PT Contoh Inti", 2),
    ]
    # The committee line under "Organizational Experience" is not a degree
    assert [e.degree for e in profile.education] == ["Bachelors of Architecture (B.Arch.)"]
    assert profile.warnings == []


def test_company_before_role_and_a_degree_still_in_progress():
    profile = parse("company_first.txt")

    assert roles(profile) == [
        ("Drafter & 3D Visualization", "PT Contoh Indah", 46),
        ("Drafter & 3D Visualization", "PT Contoh Cemerlang", 24),
    ]
    assert [(e.level, e.field) for e in profile.education] == [(2, "")]  # vocational school
    assert [(e.level, e.field) for e in profile.education_in_progress] == [(4, "architecture")]
    assert "sketchup" in profile.skills  # written as "Skechup"
    assert "accounting" not in profile.skills  # "accurate" is an adjective here


def test_heading_wording_variants_with_the_role_under_the_dates():
    profile = parse("heading_variants.txt")

    assert [(title, months) for title, _, months in roles(profile)] == [
        ("Architectural Intern", 2),
        ("Architect & drafter", 45),
        ("Architectural Freelance", 45),
    ]
    assert profile.experiences[1].company.startswith("PT Contoh Citra Prima")
    assert profile.total_experience_months == 47  # overlapping jobs are counted once
    assert [e.degree for e in profile.education] == ["Bachelor of Architecture, 3.27/4.00"]
    assert [e.degree for e in profile.education_in_progress] == ["Master of Architecture"]


def test_letter_spaced_headings_and_a_project_list_inside_a_job():
    profile = parse("spaced_headings.txt")

    assert [(title, months) for title, _, months in roles(profile)] == [
        ("DRAFTER- TESTING TECHNICAL Full Time", 60),
        ("JUNIOR ARCHITECT Independent", 6),  # used to be cut off by "PROJECT :"
    ]
    assert profile.experiences[0].company == "PT. CONTOH STRUKTUR"
    assert [(e.level, e.field) for e in profile.education] == [(2, "")]
    assert [e.field for e in profile.education_in_progress] == ["architecture"]


@pytest.mark.parametrize("path", sorted(LAYOUTS.glob("*.txt")), ids=lambda p: p.stem)
def test_every_layout_is_read_with_full_section_confidence(path):
    profile = parse_cv(path, today=REFERENCE_DATE)

    assert profile.section_confidence["experience"] == 1.0
    assert profile.section_confidence["education"] == 1.0
    assert profile.section_confidence["skills"] >= 0.7
    assert not any("tidak" in warning for warning in profile.warnings)


# --- Personal data ---------------------------------------------------------------------------

PERSONAL = re.compile(
    r"@|\+\s?62|\b08\d{6,}|\bborn\b|\b2003\b|Jalan Contoh|40999|Nusantara|Abadi"
    r"|Contoh (?:University|Institute)|\b(?:Rangga|Sekar|Bagas|Larasati|Galih)\b",
    re.IGNORECASE,
)


@pytest.mark.parametrize("path", sorted(LAYOUTS.glob("*.txt")), ids=lambda p: p.stem)
def test_no_personal_data_survives_redaction(path):
    profile = parse_cv(path, today=REFERENCE_DATE)

    assert PERSONAL.search(profile.redacted_text) is None
    assert all(PERSONAL.search(chunk) is None for chunk in profile.chunks)
    assert {"name", "email", "phone"} <= set(profile.pii)  # kept apart for contacting later


@pytest.mark.parametrize(
    "text",
    [
        "0812 3456 7890",
        "+62 812 3456 7890",
        "+62-812-3456-7890",
        "+ 6281234567890",
        "+62 81234567",
        "orang@contoh.co.id",
        "born in Kota Contoh, 19 February 2003",
        "lahir di Kota Contoh, 19 Februari 2003",
        "3174012345678901",
    ],
)
def test_mask_removes_personal_data_from_any_text(text):
    masked = pii.mask(f"Hubungi {text} untuk wawancara.")

    assert text not in masked and "[" in masked


def test_quotes_sent_to_gemini_are_masked_again(screened):
    service, job_id = screened
    job = service.get_job(job_id)
    result = service.get_ranking(job_id)[0][0]
    profile = service.get_candidate(job_id, result.candidate_id)
    result.evidence[0].best_match = "Hubungi saya di +62 812 3456 7890 atau orang@contoh.co.id"

    facts = hr_summary.build_facts(
        job, result, match_breakdown.build_breakdown(job, profile, result)
    )

    assert facts["bukti_dari_cv"][0]["kutipan"] == "Hubungi saya di [TELEPON] atau [EMAIL]"


# --- Unread sections are unknown, not a failed requirement -----------------------------------

UNSTRUCTURED_CV = """Tanpa Judul
tanpa.judul@example.com
Saya terbiasa memakai AutoCAD dan SketchUp untuk gambar kerja rumah tinggal, juga Revit
untuk koordinasi model. Saya menyukai desain interior dan presentasi kepada klien.
"""


@pytest.fixture
def unread(service, tmp_path):
    job = service.create_job(SAMPLE_JOB)
    path = tmp_path / "unstructured.txt"
    path.write_text(UNSTRUCTURED_CV, encoding="utf-8")
    profile, _ = service.add_candidate(job.job_id, path, path.name)
    service.screen(job.job_id)
    result = service.get_result(job.job_id, profile.candidate_id)
    return service, job, profile, result


def test_unread_sections_are_left_out_of_the_score(unread):
    _, job, profile, result = unread

    assert profile.section_confidence["experience"] == 0.0
    assert profile.section_confidence["education"] == 0.0
    assert result.unassessed == ["experience", "education"]
    assert result.contributions["experience"] == 0.0 and result.contributions["education"] == 0.0
    # The remaining components share the whole 100 points between them
    weights = job.weights
    expected = (
        100
        * (
            weights["skills"] * result.breakdown.skills
            + weights["semantic"] * result.breakdown.semantic
        )
        / (weights["skills"] + weights["semantic"])
    )
    assert result.score == pytest.approx(expected, abs=0.1)


def test_unread_sections_never_lead_to_an_automatic_decision(unread):
    _, _, _, result = unread

    assert result.recommendation == "REVIEW"
    assert result.knockout_flags == []  # nothing is reported as "tidak sesuai" or "0 tahun"
    assert any("tidak terbaca dari CV" in reason for reason in result.reasons)
    assert not any("0.0 tahun" in reason for reason in result.reasons)


def test_unread_sections_are_explained_as_unknown(unread):
    service, job, profile, result = unread
    breakdown = match_breakdown.build_breakdown(job, profile, result)
    rows = {row.key: row for row in breakdown.components}

    assert breakdown.experience.assessed is False and breakdown.education.status == "unknown"
    assert rows["experience"].assessed is False and rows["experience"].max_points == 0.0
    assert rows["education"].explanation.startswith("Belum dapat dinilai")
    assert sum(row.points for row in breakdown.components) == pytest.approx(result.score, abs=0.05)

    note = hr_summary.template_note(job, profile, result, breakdown)
    assert "tidak terbaca" in note.fit and "0,0 tahun" not in note.fit
    assert any("periksa CV aslinya" in risk for risk in note.risks)
    assert "sementara" in note.recommendation_reason


# --- Skills are never invented ---------------------------------------------------------------


@pytest.fixture
def layouts_screened(service):
    job = service.create_job(SAMPLE_JOB)
    for path in sorted(LAYOUTS.glob("*.txt")):
        service.add_candidate(job.job_id, path, path.name)
    service.screen(job.job_id)
    names = {c.candidate_id: c.file_name for c in service.list_candidates(job.job_id)}
    results = {names[r.candidate_id]: r for r in service.get_ranking(job.job_id)[0]}
    return service, job, results


@pytest.mark.parametrize("name", ["plural_headings.txt", "spaced_headings.txt"])
def test_a_software_tool_that_is_not_written_is_never_implied(layouts_screened, name):
    _, _, results = layouts_screened  # neither CV mentions Revit

    assert REVIT_IMPLIED not in results[name].matched_skills
    assert "Revit / BIM" in results[name].missing_must_skills


def test_the_note_separates_written_skills_from_implied_ones(layouts_screened):
    service, job, results = layouts_screened
    result = next(r for r in results.values() if any("(tersirat)" in s for s in r.matched_skills))
    profile = service.get_candidate(job.job_id, result.candidate_id)
    breakdown = match_breakdown.build_breakdown(job, profile, result)
    implied = [
        s.label
        for s in breakdown.must_have_skills + breakdown.bonus_skills
        if s.status == "implied"
    ]

    note = hr_summary.template_note(job, profile, result, breakdown)
    facts = hr_summary.build_facts(job, result, breakdown)

    assert not any("Menguasai" in item for item in note.strengths)
    assert not any(
        label in item
        for item in note.strengths
        for label in implied
        if label in facts["keterampilan_wajib_hanya_terindikasi"]
    )
    assert set(facts["keterampilan_wajib_tertulis_di_cv"]).isdisjoint(
        facts["keterampilan_wajib_hanya_terindikasi"]
    )


def test_ranking_follows_what_the_cvs_say(layouts_screened):
    _, _, results = layouts_screened
    rank = {name: result.rank for name, result in results.items()}

    # Two architecture graduates with years of design work outrank the two vocational
    # graduates who are still studying.
    graduates = {"inline_headings.txt", "heading_variants.txt"}
    studying = {"company_first.txt", "spaced_headings.txt"}
    assert max(rank[name] for name in graduates) < min(rank[name] for name in studying)
    assert results["spaced_headings.txt"].rank == 5


# --- A CV uploaded as a vacancy --------------------------------------------------------------


@pytest.mark.parametrize("path", sorted(LAYOUTS.glob("*.txt")), ids=lambda p: p.stem)
def test_a_cv_is_not_accepted_as_a_vacancy(service, path):
    from app.services.screening import NotAJobDescriptionError

    with pytest.raises(NotAJobDescriptionError):
        service.create_job(path)
