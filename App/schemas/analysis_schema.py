from pydantic import BaseModel


class JobAnalysis(BaseModel):
    job_summary: str
    required_skills: list[str]
    preferred_skills: list[str]
    responsibilities: list[str]
    qualifications: list[str]
    job_description_text: str
    
    model_config = {
        "extra": "ignore"  # Allow extra fields from LLM
    }

class ResumeAnalysis(BaseModel):
    candidate_summary: str
    strengths: list[str]
    weaknesses: list[str]
    recommendation: str
    resume_text: str
    
    model_config = {
        "extra": "ignore"
    }