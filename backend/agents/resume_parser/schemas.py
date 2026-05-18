from pydantic import BaseModel, Field


class Link(BaseModel):
    label: str = Field(description="Platform name like GitHub or LinkedIn")
    url: str


class Experience(BaseModel):
    company: str
    role: str
    employment_type: str | None = Field(
        default=None, description="Internship, Full-time, Contract, etc"
    )
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    duration: str | None = None

    summary: list[str] = Field(description="Bullet points describing work")

    technologies: list[str] = Field(
        default_factory=list, description="Tech stack used in this role"
    )


class Project(BaseModel):
    name: str

    description: list[str] = Field(description="Project bullet points")

    technologies: list[str]

    github_url: str | None = None
    live_url: str | None = None


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str | None = None

    location: str | None = None

    start_date: str | None = None
    end_date: str | None = None


class Resume(BaseModel):
    name: str
    email: str
    phone: str
    location: str | None = None

    summary: str | None = None

    links: list[Link] = Field(default_factory=list)

    skills: dict[str, list[str]] = Field(
        description=(
            "Grouped skills by category. Example: {'Languages': ['Python', 'Go']}"
        )
    )

    experiences: list[Experience] = Field(default_factory=list)

    projects: list[Project] = Field(default_factory=list)

    education: list[Education] = Field(default_factory=list)

    open_source_contributions: list[str] = Field(default_factory=list)
