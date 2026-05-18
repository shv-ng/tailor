from pydantic import BaseModel, Field


class EmailStructure(BaseModel):
    subject: str = Field(description="Punchy, professional email subject line.")
    body: str = Field(description="The email body context, between 100-150 words.")
