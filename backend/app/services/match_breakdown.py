"""Explanation views of a finished screening result.

Nothing here scores anything. These functions only reorganise what the pipeline already
decided (the result, the job criteria and the parsed profile) into shapes that are easy to
show: per-component points, requirement-by-requirement status and the matching keywords.
"""

from __future__ import annotations

from app.schemas.cv import CandidateProfile
from app.schemas.screening import (
    DEFAULT_WEIGHTS,
    ComponentScore,
    EducationMatch,
    ExperienceMatch,
    ExperienceRelevance,
    JobProfile,
    MatchBreakdown,
    MatchHighlights,
    MatchStatus,
    ScreeningResult,
    SkillMatch,
)
from app.services import matching, taxonomy

IMPLIED_SUFFIX = " (tersirat)"
EDUCATION_MISMATCH_FLAG = "Bidang pendidikan tidak sesuai dengan yang disyaratkan"
EDUCATION_LEVEL_FLAG = "Jenjang pendidikan di bawah yang disyaratkan"

EDUCATION_TEXT = {
    "match": "Bidang pendidikan sesuai dengan yang disyaratkan",
    "related": "Bidang pendidikan serumpun dengan yang disyaratkan",
    "mismatch": "Bidang pendidikan tidak sesuai dengan yang disyaratkan",
    "not_required": "Lowongan tidak mensyaratkan bidang pendidikan tertentu",
}


def build_breakdown(
    job: JobProfile, profile: CandidateProfile, result: ScreeningResult
) -> MatchBreakdown:
    must, bonus = _skill_matches(job, profile, result)
    experience = _experience_match(job, profile)
    education = _education_match(job, profile, result)
    return MatchBreakdown(
        components=_components(job, result, must, bonus, experience, education),
        must_have_skills=must,
        bonus_skills=bonus,
        experience=experience,
        experiences=_experience_relevance(job, profile),
        education=education,
        unmet_requirements=result.knockout_flags
        + [
            f"Keterampilan wajib belum terlihat di CV: {label}"
            for label in result.missing_must_skills
        ],
    )


def build_highlights(
    job: JobProfile, profile: CandidateProfile, result: ScreeningResult
) -> MatchHighlights:
    must, bonus = _skill_matches(job, profile, result)
    experience = _experience_match(job, profile)
    education = _education_match(job, profile, result)
    return MatchHighlights(
        components=_components(job, result, must, bonus, experience, education),
        must_matched=_count_found(must),
        must_total=len(must),
        bonus_matched=_count_found(bonus),
        bonus_total=len(bonus),
        relevant_years=experience.relevant_years,
        required_years=experience.required_years,
    )


def _count_found(skills: list[SkillMatch]) -> int:
    return sum(skill.status != "missing" for skill in skills)


def _skill_matches(
    job: JobProfile, profile: CandidateProfile, result: ScreeningResult
) -> tuple[list[SkillMatch], list[SkillMatch]]:
    """Status of every skill requirement, read back from the lists the matcher produced."""
    matched = set(result.matched_skills)
    terms = taxonomy.find_terms(profile.redacted_text)
    must: list[SkillMatch] = []
    bonus: list[SkillMatch] = []
    for unit in matching.requirement_units(job):
        status: MatchStatus
        if matched & set(unit["labels"]):
            status = "matched"
        elif unit["label"] + IMPLIED_SUFFIX in matched:
            status = "implied"
        else:
            status = "missing"
        found_terms = sorted({term for skill_id in unit["ids"] for term in terms.get(skill_id, [])})
        skill = SkillMatch(label=unit["label"], status=status, terms=found_terms)
        (must if unit["priority"] == "must" else bonus).append(skill)
    return must, bonus


def _experience_match(job: JobProfile, profile: CandidateProfile) -> ExperienceMatch:
    relevant_years = matching.relevant_months(job, profile) / 12
    return ExperienceMatch(
        relevant_years=round(relevant_years, 1),
        total_years=round(profile.total_experience_months / 12, 1),
        required_years=job.min_years_experience,
        met=relevant_years + 1e-9 >= job.min_years_experience,
    )


def _education_match(
    job: JobProfile, profile: CandidateProfile, result: ScreeningResult
) -> EducationMatch:
    if not job.degree_fields:
        status = "not_required"
    elif EDUCATION_MISMATCH_FLAG in result.knockout_flags:
        status = "mismatch"
    elif set(job.degree_fields) & {e.field for e in profile.education}:
        status = "match"
    else:
        status = "related"
    return EducationMatch(
        status=status,
        found_fields=sorted({e.field for e in profile.education if e.field}),
        required_fields=job.degree_fields,
        level_below_requirement=EDUCATION_LEVEL_FLAG in result.knockout_flags,
    )


def _experience_relevance(job: JobProfile, profile: CandidateProfile) -> list[ExperienceRelevance]:
    """How much each role counted towards relevant experience, using the matcher's own rule."""
    job_skill_ids = {skill.skill_id for skill in job.skills}
    roles = []
    for item in profile.experiences:
        # Asking the matcher about one role at a time returns that role's counted months.
        single_role = profile.model_copy(
            update={"experiences": [item], "total_experience_months": item.months}
        )
        counted = matching.relevant_months(job, single_role)
        if item.months and counted >= item.months:
            relevance = "relevant"
        elif counted > 0:
            relevance = "partial"
        else:
            relevance = "not_relevant"
        found = taxonomy.find_terms(f"{item.title} {item.company} {item.description}")
        terms = sorted({t for skill_id in job_skill_ids for t in found.get(skill_id, [])})
        roles.append(ExperienceRelevance(**item.model_dump(), relevance=relevance, terms=terms))
    return roles


def _skill_points(skills: list[SkillMatch], weight: float) -> float:
    """Credit earned on a list of requirements: full for a match, half for an implied one."""
    credit = {"matched": 1.0, "implied": matching.SOFT_MATCH_CREDIT, "missing": 0.0}
    return sum(weight * credit[skill.status] for skill in skills)


def _components(
    job: JobProfile,
    result: ScreeningResult,
    must: list[SkillMatch],
    bonus: list[SkillMatch],
    experience: ExperienceMatch,
    education: EducationMatch,
) -> list[ComponentScore]:
    weights = {**DEFAULT_WEIGHTS, **job.weights}
    total_weight = sum(weights.values()) or 1.0
    share = {key: 100 * weights[key] / total_weight for key in weights}

    # The skills component is one number in the score. It is shown as two rows (must-have and
    # bonus) by splitting it the same way the matcher weighs them: 1 per must-have, 0.5 per bonus.
    possible = len(must) * 1.0 + len(bonus) * 0.5
    must_share = share["skills"] * len(must) / possible if possible else 0.0
    bonus_share = share["skills"] - must_share if possible else 0.0
    must_points = share["skills"] * _skill_points(must, 1.0) / possible if possible else 0.0
    bonus_points = share["skills"] * _skill_points(bonus, 0.5) / possible if possible else 0.0

    criteria = len(job.requirement_sentences) + len(job.responsibility_sentences)
    rows = [
        (
            "must_skills",
            must_share,
            must_points,
            f"{_count_found(must)} dari {len(must)} keterampilan wajib ditemukan di CV",
        ),
        (
            "bonus_skills",
            bonus_share,
            bonus_points,
            f"{_count_found(bonus)} dari {len(bonus)} keterampilan nilai tambah ditemukan di CV",
        ),
        (
            "experience",
            share["experience"],
            result.contributions["experience"],
            f"{experience.relevant_years:.1f} tahun pengalaman yang relevan dengan posisi; "
            f"syarat minimal {experience.required_years:g} tahun",
        ),
        (
            "education",
            share["education"],
            result.contributions["education"],
            EDUCATION_TEXT[education.status]
            + (", tetapi jenjangnya di bawah syarat" if education.level_below_requirement else ""),
        ),
        (
            "semantic",
            share["semantic"],
            result.contributions["semantic"],
            f"Kemiripan makna antara isi CV dan {criteria} butir pada lowongan, "
            "dihitung dengan model embedding",
        ),
    ]
    return [
        ComponentScore(
            key=key,
            weight_percent=round(max_points, 1),
            score_percent=round(100 * points / max_points, 1) if max_points else 0.0,
            points=round(max(points, 0.0), 1),
            max_points=round(max_points, 1),
            explanation=explanation,
        )
        for key, max_points, points, explanation in rows
    ]
