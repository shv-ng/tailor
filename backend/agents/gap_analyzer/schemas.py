from pydantic import BaseModel, Field


class Gap(BaseModel):
    profile_score: int = Field(
        description="How well resume matches the jd", maximum=100, minimum=0
    )
    matching_skills: list[str] = Field(
        description="Skills present in both the resume and the jd"
    )
    missing_skills: list[str] = Field(description="Skills in jd but not in resume")
    missing_keywords: list[str] = Field(description="JD keywords not present in resume")
    strong_points: list[str] = Field(
        description="What works well about this profile for this role"
    )
    weak_points: list[str] = Field(
        description="What doesn't work well about this profile for this role"
    )
    recommendations: list[str] = Field(
        description="concrete things candidate can add/fix in resume"
    )
