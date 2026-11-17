"""Job description understanding: vacancy text -> structured screening criteria.

Rule-based, like the CV extractor: minimum years, degree fields and skills are read from
the requirement lines; skills implied by the responsibilities count as nice-to-have.
"""

from __future__ import annotations

import re

from app.schemas.screening import DEFAULT_WEIGHTS, JobProfile, SkillRequirement
from app.services import taxonomy
from app.services.cv_parsing.extractor import DEGREES, FIELDS
from app.services.cv_parsing.text_utils import split_sentences

NICE_HINT = re.compile(
    r"nice to have|preferred|plus|diutamakan|nilai tambah|advantage", re.IGNORECASE
)
MIN_YEARS = re.compile(
    r"(?:minimum|min\.?|minimal|at least)\s*(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years?|tahun|yrs?)",
    re.IGNORECASE,
)
DEGREE_HINT = re.compile(r"degree|sarjana|lulusan|pendidikan|diploma|\bs1\b|\bd3\b", re.IGNORECASE)
ALTERNATIVE = re.compile(r"\s*(?:/|or|atau)\s*", re.IGNORECASE)
SOFT_ONLY = {"presentation", "visualization"}


def parse_job(job_id: str, text: str, title: str | None = None) -> JobProfile:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    title = title or (lines[0] if lines else job_id)

    section, requirements, responsibilities = "requirements", [], []
    for line in lines[1:]:
        low = line.lower().rstrip(":")
        if low in {"requirements", "requirement", "kualifikasi", "persyaratan", "qualifications"}:
            section = "requirements"
            continue
        if low in {
            "responsibilities",
            "responsibility",
            "tanggung jawab",
            "deskripsi pekerjaan",
            "job description",
        }:
            section = "responsibilities"
            continue
        (requirements if section == "requirements" else responsibilities).extend(
            split_sentences(line)
        )

    req_text = "\n".join(requirements)
    min_years = MIN_YEARS.search(req_text)

    degree_fields, min_level = [], 0
    for sentence in requirements:
        low = sentence.lower()
        if DEGREE_HINT.search(low):
            degree_fields += [name for name, pat in FIELDS.items() if re.search(pat, low)]
            level = next((lvl for lvl, pat in DEGREES if re.search(pat, low)), 0)
            min_level = max(min_level, level or (4 if "degree" in low else 0))

    skills: dict[str, SkillRequirement] = {}
    group_no = 0
    for sentence in requirements:
        if DEGREE_HINT.search(sentence):
            continue  # degree sentences are handled separately, not as skills
        priority = "nice" if NICE_HINT.search(sentence) else "must"
        spans = taxonomy.find_spans(sentence)
        groups = {}
        for (a, _, a_end), (b, b_start, _) in zip(spans, spans[1:], strict=False):
            if ALTERNATIVE.fullmatch(
                sentence[a_end:b_start]
            ):  # "Interior designer/ Architect" = either one
                if a not in groups:
                    group_no += 1
                    groups[a] = f"alt{group_no}"
                groups[b] = groups[a]
        for skill_id, _, _ in spans:
            p = "nice" if skill_id in SOFT_ONLY else priority
            skills.setdefault(
                skill_id,
                SkillRequirement(
                    skill_id=skill_id,
                    label=taxonomy.label(skill_id),
                    priority=p,
                    group=groups.get(skill_id, ""),
                ),
            )
    for sentence in responsibilities:  # skills implied by responsibilities = nice-to-have
        for skill_id in taxonomy.find_skills(sentence):
            skills.setdefault(
                skill_id,
                SkillRequirement(
                    skill_id=skill_id, label=taxonomy.label(skill_id), priority="nice"
                ),
            )

    return JobProfile(
        job_id=job_id,
        title=title,
        min_years_experience=float(min_years.group(1)) if min_years else 0,
        degree_fields=sorted(set(degree_fields)),
        min_degree_level=min_level,
        skills=list(skills.values()),
        requirement_sentences=requirements,
        responsibility_sentences=responsibilities,
        weights=dict(DEFAULT_WEIGHTS),
        raw_text=text,
    )
