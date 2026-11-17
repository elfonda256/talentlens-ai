"""Semantic matching and scoring.

Two stages, retrieve-then-rerank:
1) Recall : the whole JD is searched against the vector index to pick the top-K candidates.
2) Rerank : an explainable hybrid score (skills, relevant experience, semantic fit, education).

The score is deterministic. No LLM takes part in it.
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np

from app.schemas.cv import CandidateProfile
from app.schemas.screening import DEFAULT_WEIGHTS, Evidence, JobProfile, ScoreBreakdown
from app.services import taxonomy
from app.services.embedding import Embedder
from app.services.vector_index import FaissIndex

RELATED_FIELDS = {
    "architecture": {"interior design", "civil engineering", "urban planning"},
    "interior design": {"architecture", "product design"},
}
SOFT_MATCH_THRESHOLD = 0.55
SOFT_MATCH_CREDIT = 0.5


def recall_candidates(
    job: JobProfile, embedder: Embedder, index: FaissIndex, top_k: int = 50
) -> list[str]:
    """Recall stage: candidates whose chunks are most similar to the whole JD."""
    query = embedder.encode([job.raw_text], kind="query")[0]
    best: dict[str, float] = defaultdict(float)
    for hit in index.search(query, top_k=top_k * 8):
        best[hit.candidate_id] = max(best[hit.candidate_id], hit.score)
    return [cid for cid, _ in sorted(best.items(), key=lambda kv: -kv[1])[:top_k]]


def _requirement_units(job: JobProfile) -> list[dict]:
    """Merges alternative skills ("A or B") into a single requirement."""
    units: dict[str, dict] = {}
    for req in job.skills:
        key = req.group or req.skill_id
        unit = units.setdefault(key, {"ids": [], "labels": [], "priority": req.priority})
        unit["ids"].append(req.skill_id)
        unit["labels"].append(req.label)
    for unit in units.values():
        unit["label"] = " / ".join(unit["labels"])
    return list(units.values())


def _core_skills(job: JobProfile) -> set[str]:
    tax = taxonomy.load()
    return {
        s.skill_id
        for s in job.skills
        if s.priority == "must" and tax[s.skill_id]["category"] in {"technical", "software"}
    }


def relevant_months(job: JobProfile, cand: CandidateProfile) -> float:
    """Experience only counts when it is relevant to the position, not merely long."""
    job_skills = {s.skill_id for s in job.skills}
    core = _core_skills(job)
    total = 0.0
    for item in cand.experiences:
        found = set(taxonomy.find_skills(f"{item.title} {item.company} {item.description}"))
        overlap = found & job_skills
        if len(overlap & core) >= 2 or len(overlap) >= 3:
            weight = 1.0
        elif overlap & core:
            weight = 0.6
        elif overlap:
            weight = 0.25
        else:
            weight = 0.0
        total += item.months * weight
    return min(total, cand.total_experience_months)


def score_candidate(
    job: JobProfile, cand: CandidateProfile, embedder: Embedder, index: FaissIndex
) -> dict:
    flags: list[str] = []

    # --- Semantic: every JD line looks for its best evidence in the CV ---
    sentences = job.requirement_sentences + job.responsibility_sentences
    evidence: list[Evidence] = []
    if sentences and cand.chunks:
        for sentence, vector in zip(
            sentences, embedder.encode(sentences, kind="query"), strict=True
        ):
            hit = index.best_match(vector, cand.candidate_id)
            if hit:
                evidence.append(
                    Evidence(
                        requirement=sentence,
                        best_match=hit.text,
                        similarity=round(embedder.calibrate(hit.score), 3),
                    )
                )
    semantic = float(np.mean([e.similarity for e in evidence])) if evidence else 0.0

    # --- Skills: exact match through the taxonomy, or soft match through embeddings ---
    cand_skills = set(cand.skills)
    matched, missing_must, missing_nice = [], [], []
    gained = possible = 0.0
    for unit in _requirement_units(job):
        weight = 1.0 if unit["priority"] == "must" else 0.5
        possible += weight
        hit_ids = [sid for sid in unit["ids"] if sid in cand_skills]
        if hit_ids:
            gained += weight
            matched += [taxonomy.label(sid) for sid in hit_ids]
            continue
        soft = 0.0
        if cand.chunks:
            for sid in unit["ids"]:
                vector = embedder.encode([taxonomy.describe(sid)], kind="query")[0]
                hit = index.best_match(vector, cand.candidate_id)
                soft = max(soft, embedder.calibrate(hit.score) if hit else 0.0)
        if soft >= SOFT_MATCH_THRESHOLD:
            gained += weight * SOFT_MATCH_CREDIT
            matched.append(f"{unit['label']} (tersirat)")
        else:
            (missing_must if unit["priority"] == "must" else missing_nice).append(unit["label"])
    skills = gained / possible if possible else 0.0

    # --- Relevant experience ---
    rel_years = relevant_months(job, cand) / 12
    if job.min_years_experience > 0:
        ratio = rel_years / job.min_years_experience
        experience = 0.85 * min(1.0, ratio) + 0.15 * min(
            1.0, max(0.0, rel_years - job.min_years_experience) / 3
        )
        if rel_years + 1e-9 < job.min_years_experience:
            flags.append(
                f"Pengalaman relevan {rel_years:.1f} tahun, di bawah minimal {job.min_years_experience:g} tahun"
            )
    else:
        experience = 1.0

    # --- Education ---
    fields = {e.field for e in cand.education if e.field}
    level = max((e.level for e in cand.education), default=0)
    if not job.degree_fields:
        education = 1.0
    elif fields & set(job.degree_fields):
        education = 1.0
    elif any(fields & RELATED_FIELDS.get(f, set()) for f in job.degree_fields):
        education = 0.6
    else:
        education = 0.15
        flags.append("Bidang pendidikan tidak sesuai dengan yang disyaratkan")
    if job.min_degree_level and level and level < job.min_degree_level:
        education *= 0.7
        flags.append("Jenjang pendidikan di bawah yang disyaratkan")

    breakdown = ScoreBreakdown(
        skills=round(skills, 3),
        experience=round(experience, 3),
        semantic=round(semantic, 3),
        education=round(education, 3),
    )
    weights = {**DEFAULT_WEIGHTS, **job.weights}
    norm = sum(weights.values()) or 1.0
    contributions = {k: round(100 * weights[k] / norm * getattr(breakdown, k), 1) for k in weights}
    return {
        "score": round(sum(contributions.values()), 1),
        "breakdown": breakdown,
        "contributions": contributions,
        "matched_skills": matched,
        "missing_must_skills": missing_must,
        "missing_nice_skills": missing_nice,
        "knockout_flags": flags,
        "evidence": sorted(evidence, key=lambda e: -e.similarity),
        "relevant_years": round(rel_years, 1),
    }
