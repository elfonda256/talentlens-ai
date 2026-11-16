"""Structured result of parsing one CV. Field names match the original PoC parser."""

from pydantic import BaseModel, Field


class ExperienceItem(BaseModel):
    title: str = ""
    company: str = ""
    start: str = ""
    end: str = ""
    months: int = 0
    description: str = ""


class EducationItem(BaseModel):
    degree: str = ""
    level: int = 0
    field: str = ""
    institution: str = ""


class CandidateProfile(BaseModel):
    candidate_id: str
    source: str = "upload"
    file_name: str = ""
    extraction_method: str = "text"  # text | ocr
    # Personal data is kept apart and must NEVER be used as a scoring feature.
    pii: dict[str, str] = Field(default_factory=dict)
    redacted_text: str = ""
    summary: str = ""
    experiences: list[ExperienceItem] = Field(default_factory=list)
    total_experience_months: int = 0
    education: list[EducationItem] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)  # canonical skill ids
    chunks: list[str] = Field(default_factory=list)
    extraction_confidence: float = 1.0
    warnings: list[str] = Field(default_factory=list)
