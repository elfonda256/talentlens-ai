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
    # Components left out of the score because the CV section behind them was not read
    unassessed: list[str] = Field(default_factory=list)
    evidence: list[Evidence]
    recommendation: Recommendation
    reasons: list[str]
    narrative: str


class HRSummary(BaseModel):
    """A recruiter-style note. Gemini and the template fill the same fields."""

    headline: str  # the verdict in one sentence
    fit: str  # how well the candidate fits the position
    strengths: list[str]
    concerns: list[str]
    risks: list[str]
    interview_focus: list[str]
    recommendation_reason: str
    source: Literal["gemini", "template"]
    model: str = ""
    note: str = ""  # why the template was used, when it was


# ---------- Explanation views (presentation only; never used for scoring) ----------

MatchStatus = Literal["matched", "implied", "missing"]


class SkillMatch(BaseModel):
    label: str
    status: MatchStatus
    terms: list[str] = Field(default_factory=list)  # words in the CV that matched


class ExperienceMatch(BaseModel):
    relevant_years: float
    total_years: float
    required_years: float
    met: bool
    assessed: bool = True  # False: the experience section was not read, so nothing was judged


class EducationMatch(BaseModel):
    status: Literal["match", "related", "mismatch", "not_required", "unknown"]
    found_fields: list[str]
    required_fields: list[str]
    level_below_requirement: bool


ComponentKey = Literal["must_skills", "bonus_skills", "experience", "education", "semantic"]


class ComponentScore(BaseModel):
    key: ComponentKey
    weight_percent: float  # share of the total score this component can give
    score_percent: float  # how well the candidate did on this component
    points: float  # contribution to the 0-100 score
    max_points: float
    explanation: str
    assessed: bool = True


class ExperienceRelevance(BaseModel):
    title: str
    company: str
    start: str
    end: str
    months: int
    description: str
    relevance: Literal["relevant", "partial", "not_relevant"]
    terms: list[str]  # job keywords found in this role


class MatchBreakdown(BaseModel):
    components: list[ComponentScore]
    must_have_skills: list[SkillMatch]
    bonus_skills: list[SkillMatch]
    experience: ExperienceMatch
    experiences: list[ExperienceRelevance]
    education: EducationMatch
    unmet_requirements: list[str]


class MatchHighlights(BaseModel):
    """The few numbers shown next to a candidate in the ranking table."""

    must_matched: int
    must_total: int
    bonus_matched: int
    bonus_total: int
    relevant_years: float
    required_years: float
    components: list[ComponentScore]  # for the small score-composition bar


# ---------- API responses ----------


class JobSummary(BaseModel):
    job_id: str
    title: str
    candidate_count: int
    screened: bool
    # Decision counts of the last screening; zero until the job is screened.
    shortlist: int = 0
    review: int = 0
    reject: int = 0


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


ConfidenceLevel = Literal["high", "medium", "low"]


class HiringRecommendation(BaseModel):
    """The next step for HR, worded from the system's decision."""

    decision: Recommendation
    title: str
    summary: str
    next_steps: list[str]


class AssessmentConfidence(BaseModel):
    """How firm the decision is: the CV was fully read and the score is clear of a threshold."""

    level: ConfidenceLevel
    reasons: list[str]


class Assessment(BaseModel):
    """Decision aid read from the screening result; it never changes a score or a decision."""

    hiring: HiringRecommendation
    confidence: AssessmentConfidence
    risks: list[str]
    highly_recommended: bool


class RankingRow(ScreeningResult):
    file_name: str
    extraction_method: str
    highlights: MatchHighlights
    assessment: Assessment
    warnings: list[str] = Field(default_factory=list)  # what the parser could not read
    name: str = ""  # only filled when identities are revealed


class Ranking(BaseModel):
    job_id: str
    embedding_backend: str
    results: list[RankingRow]


class CandidateDetail(BaseModel):
    result: ScreeningResult
    breakdown: MatchBreakdown
    assessment: Assessment
    summary: str
    experiences: list[dict]
    education: list[dict]
    education_in_progress: list[dict] = Field(default_factory=list)
    skills: list[str]
    total_experience_months: int
    extraction_method: str
    extraction_confidence: float
    section_confidence: dict[str, float] = Field(default_factory=dict)
    warnings: list[str]
    identity: dict[str, str] = Field(default_factory=dict)  # empty unless revealed
