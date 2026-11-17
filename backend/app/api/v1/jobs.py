"""Screening workflow: upload a job description, upload CVs, run screening, read results."""

from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from app.api.v1.uploads import temporary_copy, validate_upload
from app.core.config import Settings, get_settings
from app.schemas.cv import CandidateProfile
from app.schemas.screening import (
    CandidateDetail,
    CandidateListItem,
    HRSummary,
    JobProfile,
    JobSummary,
    Ranking,
    RankingRow,
    ScreeningRun,
    UploadOutcome,
)
from app.services import match_breakdown
from app.services.cv_parsing import UnreadableDocumentError, UnsupportedFormatError
from app.services.screening import (
    CandidateNotFoundError,
    JobNotFoundError,
    NotAJobDescriptionError,
    NotScreenedError,
    ScreeningService,
    get_screening_service,
)

router = APIRouter(prefix="/jobs", tags=["Screening"])

Service = Annotated[ScreeningService, Depends(get_screening_service)]
AppSettings = Annotated[Settings, Depends(get_settings)]
Reveal = Annotated[
    bool, Query(description="Show candidate identities. Hidden by default (blind review).")
]

NOT_FOUND = {404: {"description": "Job or candidate not found"}}
NOT_SCREENED = {409: {"description": "Screening has not been run for this job"}}


def _job_or_404(service: ScreeningService, job_id: str) -> JobProfile:
    try:
        return service.get_job(job_id)
    except JobNotFoundError as error:
        raise HTTPException(404, "Lowongan tidak ditemukan") from error


def _name(profile: CandidateProfile, reveal: bool) -> str:
    return profile.pii.get("name", "") if reveal else ""


@router.post(
    "",
    response_model=JobProfile,
    status_code=201,
    summary="Upload a job description and parse it into screening criteria",
    responses={
        413: {},
        415: {},
        422: {"description": "The document could not be read, or it is a CV rather than a vacancy"},
    },
)
def create_job(
    file: Annotated[UploadFile, File(description="Job description as PDF, DOCX or TXT")],
    service: Service,
    settings: AppSettings,
) -> JobProfile:
    suffix = validate_upload(file, settings)
    with temporary_copy(file, suffix) as path:
        try:
            return service.create_job(path)
        except (UnreadableDocumentError, NotAJobDescriptionError) as error:
            raise HTTPException(422, str(error)) from error


@router.get("", response_model=list[JobSummary], summary="List uploaded jobs")
def list_jobs(service: Service) -> list[JobSummary]:
    return [
        JobSummary(
            job_id=job.job_id,
            title=job.title,
            candidate_count=len(service.list_candidates(job.job_id)),
            screened=service.is_screened(job.job_id),
        )
        for job in service.list_jobs()
    ]


@router.get(
    "/{job_id}",
    response_model=JobProfile,
    summary="Parsed criteria of one job",
    responses=NOT_FOUND,
)
def get_job(job_id: str, service: Service) -> JobProfile:
    return _job_or_404(service, job_id)


@router.post(
    "/{job_id}/candidates",
    response_model=list[UploadOutcome],
    summary="Upload one or more CVs for a job",
    responses=NOT_FOUND,
)
def upload_candidates(
    job_id: str,
    files: Annotated[list[UploadFile], File(description="CV files (PDF, DOCX or TXT)")],
    service: Service,
    settings: AppSettings,
) -> list[UploadOutcome]:
    """Each file is handled on its own: one unreadable CV does not fail the whole batch."""
    _job_or_404(service, job_id)
    outcomes = []
    for file in files:
        file_name = file.filename or "cv"
        try:
            suffix = validate_upload(file, settings)
            with temporary_copy(file, suffix) as path:
                profile, is_new = service.add_candidate(job_id, path, file_name)
        except HTTPException as error:
            outcomes.append(
                UploadOutcome(file_name=file_name, status="failed", detail=error.detail)
            )
        except (UnreadableDocumentError, UnsupportedFormatError) as error:
            outcomes.append(UploadOutcome(file_name=file_name, status="failed", detail=str(error)))
        else:
            outcomes.append(
                UploadOutcome(
                    file_name=file_name,
                    status="parsed" if is_new else "duplicate",
                    candidate_id=profile.candidate_id,
                    detail="" if is_new else "Kandidat ini sudah ada pada lowongan",
                )
            )
    return outcomes


@router.get(
    "/{job_id}/candidates",
    response_model=list[CandidateListItem],
    summary="Candidates uploaded for a job",
    responses=NOT_FOUND,
)
def list_candidates(
    job_id: str, service: Service, reveal: Reveal = False
) -> list[CandidateListItem]:
    _job_or_404(service, job_id)
    return [
        CandidateListItem(
            candidate_id=c.candidate_id,
            file_name=c.file_name if reveal else "",
            extraction_method=c.extraction_method,
            extraction_confidence=c.extraction_confidence,
            total_experience_months=c.total_experience_months,
            skill_count=len(c.skills),
            name=_name(c, reveal),
        )
        for c in service.list_candidates(job_id)
    ]


@router.post(
    "/{job_id}/screen",
    response_model=ScreeningRun,
    summary="Run embedding, matching, scoring and ranking for a job",
    responses={**NOT_FOUND, 409: {"description": "The job has no candidates yet"}},
)
def run_screening(job_id: str, service: Service) -> ScreeningRun:
    _job_or_404(service, job_id)
    if not service.list_candidates(job_id):
        raise HTTPException(409, "Belum ada CV yang diunggah untuk lowongan ini")
    results, backend = service.screen(job_id)
    decisions = [r.recommendation for r in results]
    return ScreeningRun(
        job_id=job_id,
        screened=len(results),
        embedding_backend=backend,
        shortlist=decisions.count("SHORTLIST"),
        review=decisions.count("REVIEW"),
        reject=decisions.count("REJECT"),
    )


@router.get(
    "/{job_id}/ranking",
    response_model=Ranking,
    summary="Ranked candidates with scores and reasons",
    responses={**NOT_FOUND, **NOT_SCREENED},
)
def get_ranking(job_id: str, service: Service, reveal: Reveal = False) -> Ranking:
    job = _job_or_404(service, job_id)
    try:
        results, backend = service.get_ranking(job_id)
    except NotScreenedError as error:
        raise HTTPException(409, "Screening belum dijalankan untuk lowongan ini") from error
    rows = []
    for result in results:
        profile = service.get_candidate(job_id, result.candidate_id)
        rows.append(
            RankingRow(
                **result.model_dump(),
                file_name=profile.file_name if reveal else "",
                extraction_method=profile.extraction_method,
                highlights=match_breakdown.build_highlights(job, profile, result),
                warnings=profile.warnings,
                name=_name(profile, reveal),
            )
        )
    return Ranking(job_id=job_id, embedding_backend=backend, results=rows)


@router.get(
    "/{job_id}/candidates/{candidate_id}",
    response_model=CandidateDetail,
    summary="Score breakdown, evidence and parsed profile of one candidate",
    responses={**NOT_FOUND, **NOT_SCREENED},
)
def get_candidate_detail(
    job_id: str, candidate_id: str, service: Service, reveal: Reveal = False
) -> CandidateDetail:
    job = _job_or_404(service, job_id)
    try:
        result = service.get_result(job_id, candidate_id)
        profile = service.get_candidate(job_id, candidate_id)
    except NotScreenedError as error:
        raise HTTPException(409, "Screening belum dijalankan untuk lowongan ini") from error
    except CandidateNotFoundError as error:
        raise HTTPException(404, "Kandidat tidak ditemukan") from error
    identity = {k: profile.pii[k] for k in ("name", "email", "phone") if k in profile.pii}
    return CandidateDetail(
        result=result,
        breakdown=match_breakdown.build_breakdown(job, profile, result),
        summary=profile.summary,
        experiences=[e.model_dump() for e in profile.experiences],
        education=[e.model_dump() for e in profile.education],
        education_in_progress=[e.model_dump() for e in profile.education_in_progress],
        skills=profile.skills,
        total_experience_months=profile.total_experience_months,
        extraction_method=profile.extraction_method,
        extraction_confidence=profile.extraction_confidence,
        section_confidence=profile.section_confidence,
        warnings=profile.warnings,
        identity=identity if reveal else {},
    )


@router.post(
    "/{job_id}/candidates/{candidate_id}/summary",
    response_model=HRSummary,
    summary="HR summary that explains the candidate's result (Gemini, or a template)",
    responses={**NOT_FOUND, **NOT_SCREENED},
)
def create_hr_summary(
    job_id: str,
    candidate_id: str,
    service: Service,
    refresh: Annotated[bool, Query(description="Ignore a stored summary and ask again")] = False,
) -> HRSummary:
    """The LLM only words the explanation. It never changes a score or a rank."""
    _job_or_404(service, job_id)
    try:
        return service.summarize(job_id, candidate_id, refresh=refresh)
    except NotScreenedError as error:
        raise HTTPException(409, "Screening belum dijalankan untuk lowongan ini") from error
    except CandidateNotFoundError as error:
        raise HTTPException(404, "Kandidat tidak ditemukan") from error
