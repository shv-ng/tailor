from pydantic import BaseModel, Field


class Question(BaseModel):
    question: str = Field(description="The technical or behavioral interview question")
    category: str = Field(
        description="Must be one of: technical, behavioral, project-based, role-specific"
    )
    answer: str = Field(
        description="A strong, deeply detailed exemplary answer tailored explicitly to this candidate's actual projects, real tools, and real backend experience. Avoid generic phrasing."
    )
    why_asked: str = Field(
        description="One line explaining exactly what the interviewer is validating for this role."
    )


class InterviewPrep(BaseModel):
    questions: list[Question] = Field(
        description="A list containing exactly 5 tailored interview questions.",
        min_items=5,
        max_items=5,
    )
