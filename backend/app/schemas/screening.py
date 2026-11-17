"""Data contracts for job criteria, screening results and the HR summary."""

from typing import Literal

from pydantic import BaseModel, Field

Recommendation = Literal["SHORTLIST", "REVIEW", "REJECT"]

# Starting weights of the hybrid score; a job may carry its own.
DEFAULT_WEIGHTS = {"skills": 0.35, "experience": 0.25, "semantic": 0.25, "education": 0.15}


class SkillRequirement(BaseModel):
    skill_id: str
    label: str
    priority: Literal["must", "nice"] = "must"
    group: str = ""  # skills in the same group are alternatives ("A or B")


class JobProfile(BaseModel):
    job_id: str
    title: str
    min_years_experience: float = 0
    degree_fields: list[str] = Field(default_factory=list)
    min_degree_level: int = 0  # 0 = not required, 3 = D3, 4 = S1/D4, 5 = S2
    skills: list[SkillRequirement] = Field(default_factory=list)
    requirement_sentences: list[str] = Field(default_factory=list)
    responsibility_sentences: list[str] = Field(default_factory=list)
    weights: dict[str, float] = Field(default_factory=dict)
    raw_text: str = ""


class Evidence(BaseModel):
    requirement: str
    best_match: str
    similarity: float


class ScoreBreakdown(BaseModel):
    skills: float
    experience: float
    semantic: float
    education: float


class ScreeningResult(BaseModel):
    candidate_id: str
    job_id: str
    rank: int = 0
    score: float
    breakdown: ScoreBreakdown
    contributions: dict[str, float]
    matched_skills: list[str]
    missing_must_skills: list[str]
    missing_nice_skills: list[str]
    knockout_flags: list[str]
    evidence: list[Evidence]
    recommendation: Recommendation
    reasons: list[str]
    narrative: str


class HRSummary(BaseModel):
    text: str
    source: Literal["gemini", "template"]
    model: str = ""
    note: str = ""  # why the template was used, when it was


# ---------- API responses ----------


class JobSummary(BaseModel):
    job_id: str
    title: str
    candidate_count: int
    screened: bool


class UploadOutcome(BaseModel):
    file_name: str
    status: Literal["parsed", "duplicate", "failed"]
    candidate_id: str = ""
    detail: str = ""


class CandidateListItem(BaseModel):
    candidate_id: str
    file_name: str
    extraction_method: str
    extraction_confidence: float
    total_experience_months: int
    skill_count: int
    name: str = ""  # only filled when identities are revealed


class ScreeningRun(BaseModel):
    job_id: str
    screened: int
    embedding_backend: str
    shortlist: int
    review: int
    reject: int


class RankingRow(ScreeningResult):
    file_name: str
    extraction_method: str
    name: str = ""  # only filled when identities are revealed


class Ranking(BaseModel):
    job_id: str
    embedding_backend: str
    results: list[RankingRow]


class CandidateDetail(BaseModel):
    result: ScreeningResult
    summary: str
    experiences: list[dict]
    education: list[dict]
    skills: list[str]
    total_experience_months: int
    extraction_method: str
    extraction_confidence: float
    warnings: list[str]
    identity: dict[str, str] = Field(default_factory=dict)  # empty unless revealed
