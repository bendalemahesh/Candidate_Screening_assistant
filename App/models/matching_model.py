from typing import Optional
from pydantic import BaseModel, Field

class MatchingScore(BaseModel):

    match_score: float

    matched_skills: list[str] = Field(default_factory=list)

    missing_skills: list[str] = Field(default_factory=list)

