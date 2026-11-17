from app.services.jd_parsing import parse_job

JD = """Junior Architect
REQUIREMENTS:
Degree in architecture or interior design
Interior designer/ Architect with minimum 2 years experience in design and build
Knowledge of software programs such as AutoCAD, Sketchup
Experience with Revit is a plus
RESPONSIBILITIES:
Plan and monitor the project timeline.
"""


def test_title_years_and_degree_are_extracted():
    job = parse_job("job-1", JD)

    assert job.title == "Junior Architect"
    assert job.min_years_experience == 2
    assert job.degree_fields == ["architecture", "interior design"]
    assert job.min_degree_level == 4


def test_slash_separated_roles_are_alternatives_not_two_requirements():
    skills = {s.skill_id: s for s in parse_job("job-1", JD).skills}

    assert skills["interior_design"].group
    assert skills["interior_design"].group == skills["architecture_design"].group
    assert skills["autocad"].group == ""


def test_priority_follows_wording_and_section():
    skills = {s.skill_id: s.priority for s in parse_job("job-1", JD).skills}

    assert skills["autocad"] == "must"
    assert skills["revit"] == "nice"  # "is a plus"
    assert skills["project_management"] == "nice"  # only implied by a responsibility


def test_degree_sentence_does_not_create_skill_requirements():
    job = parse_job("job-1", "Staff\nREQUIREMENTS:\nDegree in interior design\n")

    assert job.skills == []
    assert job.degree_fields == ["interior design"]


def test_indonesian_headings_are_understood():
    text = (
        "Arsitek\nKualifikasi:\nMinimal 3 tahun pengalaman\nTanggung Jawab:\nMenyusun gambar kerja."
    )
    job = parse_job("job-2", text)

    assert job.min_years_experience == 3
    assert job.requirement_sentences == ["Minimal 3 tahun pengalaman"]
    assert job.responsibility_sentences == ["Menyusun gambar kerja."]
