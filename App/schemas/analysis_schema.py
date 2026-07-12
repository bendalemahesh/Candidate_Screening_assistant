from pydantic import BaseModel


class ResumeAnalysis(BaseModel):
    candidate_summary: str
    strengths: list[str]
    weaknesses: list[str]
    recommendation: str
    resume_text: str