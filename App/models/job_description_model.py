from typing import Optional
from pydantic import BaseModel, Field

class JobDescription(BaseModel):

    job_title: str

    company: Optional[str] = None

    company_email: Optional[str] = None

    company_linkedin: Optional[str] = None

    company_location: Optional[str] = None

    employment_type: Optional[str] = None

    work_mode: Optional[str] = None

    salary_range: Optional[str] = None

    notice_period: Optional[str] = None

    experience_required: Optional[str] = None

    education_required: Optional[str] = None

    required_skills: list[str] = Field(default_factory=list)

    preferred_skills: list[str] = Field(default_factory=list)

    programming_languages: list[str] = Field(default_factory=list)

    responsibilities: list[str] = Field(default_factory=list)

    certifications: list[str] = Field(default_factory=list)

    job_description: Optional[str] = None

    match_skills: list[str] = Field(default_factory=list)

    

    