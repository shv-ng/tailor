from pydantic import BaseModel, Field


class Job(BaseModel):
    role: str = Field(description="Job title")
    company: str = Field(description="Company name")
    required_skills: list[str] = Field(description="Required skills")
    preferred_skills: list[str] = Field(description="Preferred skills")
    experience_required: str = Field(description="Required experience")
    responsibilities: list[str] = Field(description="Responsibilities")
    keywords: list[str] = Field(
        description="Important terms that would appear in strong resume  (tech names, methodologies, buzzwords from the jd etc.)"
    )
