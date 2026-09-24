from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal


class JDInput(BaseModel):
    jd_text: str | None = None
    jd_url: str | None = None

    @model_validator(mode="after")
    def exactly_one(self):
        if bool(self.jd_text) == bool(self.jd_url):
            raise ValueError("Provide exactly one of jd_text or jd_url")
        return self


class ParsedJD(BaseModel):
    job_title: str
    company: str | None = None
    seniority: str | None = Field(
        default=None,
        description="Level word only: intern, junior, mid, senior, lead. "
        "Null if the text does not state a level.",
    )
    years_experience: str | None = Field(
        default=None, description="e.g. '1-3 years'. Null if not stated."
    )
    required_skills: list[str] = Field(
        default_factory=list,
        description="Hard requirements: technologies, tools, methods",
    )
    nice_to_have_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(
        default_factory=list,
        description="Domain words a recruiter or ATS would scan for",
    )
    @field_validator("company", "seniority", "years_experience")
    @classmethod
    def blank_to_none(cls, v):
        if v is not None and not v.strip():
            return None
        return v

class SkillMatch(BaseModel):
    skill: str
    status: Literal["strong", "partial", "missing"]
    evidence: str = Field(
        default="",
        description="Short pointer to the resume evidence; empty if missing",
    )


class SkillAssessment(BaseModel):
    """What the LLM returns."""
    matches: list[SkillMatch]
    advice: list[str] = Field(
        default_factory=list,
        description="Concrete steps to close the biggest gaps",
    )

class FitReport(BaseModel):
    """What our API returns."""
    score: int
    matches: list[SkillMatch]
    gaps: list[str]
    advice: list[str]

class BulletRewrite(BaseModel):
    original: str = Field(description="An existing resume bullet, verbatim")
    improved: str = Field(description="Rewritten to emphasize relevance to this JD")
    reason: str = Field(description="One short sentence on why this helps")


class TailoredOutput(BaseModel):
    summary: str = Field(description="3-4 sentence resume summary for this role")
    bullet_rewrites: list[BulletRewrite] = Field(default_factory=list)
    cover_letter: str

class AnalyzeRequest(JDInput):
    candidate_name: str = "Candidate"
    force: bool = False


class AnalyzeResponse(BaseModel):
    parsed_jd: ParsedJD
    fit: FitReport
    tailored: TailoredOutput | None = None
    application_id: int | None = None