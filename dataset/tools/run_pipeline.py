"""Run the unmodified TalentLens pipeline over dataset/architecture and dump the raw results.

Usage: python run_pipeline.py <backend_dir> <category_dir> <out_json>
"""
import json
import sys
import tempfile
from datetime import date
from pathlib import Path

backend, cat, out = map(Path, sys.argv[1:4])
sys.path.insert(0, str(backend))

from app.core.config import Settings  # noqa: E402
from app.services.screening import ScreeningService  # noqa: E402
from app.services.store import JsonStore  # noqa: E402

pools = json.loads((cat / "Expected_Result" / "regression" / "index.json").read_text())["fixtures"]
tmp = Path(tempfile.mkdtemp())
settings = Settings(embedding_backend="tfidf", reference_date=date(2026, 11, 17), storage_dir=tmp)
svc = ScreeningService(JsonStore(tmp / "state.json"), settings)

result = {"embedder": None, "jobs": {}}
for vac in sorted((cat / "Vacancy").glob("*.pdf")):
    vid = vac.name[:10]
    guard = None
    try:
        job = svc.create_job(vac)
    except Exception as error:
        # Record the guard result, then parse the vacancy directly so its CVs can still be scored.
        guard = f"{type(error).__name__}: {error}"
        from app.services import jd_parsing
        from app.services.cv_parsing.document_loader import load_document
        text, _ = load_document(vac)
        job = jd_parsing.parse_job(f"{vid.lower()}-direct", text)
        svc._store.save_job(job)
    cands = {}
    for fx in [f for f in pools if f["target_vacancy"] == vid]:
        cv = next((cat / "CV").glob(f"{fx['cv_id']}_*.pdf"))
        try:
            profile, _ = svc.add_candidate(job.job_id, cv, cv.name)
            cands[profile.candidate_id] = (fx["cv_id"], profile)
        except Exception as error:  # an unreadable upload is a result too
            result["jobs"].setdefault(vid, {"candidates": {}})["candidates"][fx["cv_id"]] = {
                "upload_error": f"{type(error).__name__}: {error}"}
    ranking, embedder = svc.screen(job.job_id)
    result["embedder"] = embedder
    entry = result["jobs"].setdefault(vid, {"candidates": {}})
    entry["job"] = {"upload_guard": guard, "min_years_experience": job.min_years_experience, "degree_fields": job.degree_fields,
                    "min_degree_level": job.min_degree_level,
                    "skills": [(s.skill_id, s.priority, s.group) for s in job.skills]}
    for r in ranking:
        cv_id, p = cands[r.candidate_id]
        entry["candidates"][cv_id] = {
            "rank": r.rank, "score": r.score, "recommendation": r.recommendation,
            "breakdown": r.breakdown.model_dump(), "contributions": r.contributions,
            "unassessed": r.unassessed, "knockout_flags": r.knockout_flags,
            "matched_skills": r.matched_skills, "missing_must_skills": r.missing_must_skills,
            "extraction_method": p.extraction_method, "extraction_confidence": p.extraction_confidence,
            "experiences": len(p.experiences), "total_experience_months": p.total_experience_months,
            "education": [(e.level, e.field) for e in p.education], "skills": p.skills,
            "warnings": p.warnings, "reasons": r.reasons,
            "pii": p.pii, "section_confidence": p.section_confidence,
            "experience_items": [(x.title, x.company, x.start, x.end, x.months) for x in p.experiences],
        }
out.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=str))
print("embedder:", result["embedder"])
