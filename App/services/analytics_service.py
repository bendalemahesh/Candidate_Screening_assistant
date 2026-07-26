from collections import Counter

from services.database_service import DatabaseService
from models.candidate_profile_model import (
    CandidateProfile,
    Education,
    Experience,
    Certification,
)
from services.matching_service import MatchingService

class AnalyticsService:

    def __init__(self):

        self.db = DatabaseService()

    def dict_to_candidate(self, data):

        return CandidateProfile(

            full_name=data["full_name"],
            email=data["email"],
            phone=data["phone"],

            linkedin=data["linkedin"],
            github=data["github"],

            skills=data["skills"],

            education=[
                Education(**edu)
                for edu in data["education"]
            ],

            experience=[
                Experience(**exp)
                for exp in data["experience"]
            ],

            certifications=[
                Certification(**cert)
                for cert in data["certifications"]
            ],

            summary=data["summary"],
            resume_text=data["resume_text"]

        )

    def get_dashboard_data(self):

        candidates = self.db.get_all_candidates()

        jobs = self.db.get_all_jobs()

        skills = []

        companies = []

        for candidate in candidates:

            skills.extend(candidate["skills"])

        for job in jobs:

            companies.append(job["company"])

        skill_counter = Counter(skills)

        company_counter = Counter(companies)

        match_scores = []

        for candidate_data in candidates:

            candidate = self.dict_to_candidate(candidate_data)

            best_score = 0

            for job in jobs:

                match = MatchingService.calculate_match(
                    candidate,
                    job
                )

                if match["match_score"] > best_score:

                    best_score = match["match_score"]

            match_scores.append(best_score)

        return {

            "average_match_score":

                round(

                    sum(match_scores) /

                    max(len(match_scores),1),

                    2

                ),

            "highest_match_score": max(match_scores, default=0),

            "total_candidates": len(candidates),

            "total_jobs": len(jobs),

            "top_skills": skill_counter.most_common(10),

            "companies": company_counter.most_common()

        }