from pydantic import BaseModel, Field, model_validator


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
        default=None, description="e.g. intern, junior, mid, senior, lead"
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