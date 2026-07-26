from services.database_service import DatabaseService
from services.matching_service import MatchingService
from models.candidate_profile_model import (
    CandidateProfile,
    Education,
    Experience,
    Certification,
)


class RankingService:

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

    def rank_candidates(self, job_id):

        candidates = self.db.get_all_candidates()

        jobs = self.db.get_all_jobs()

        selected_job = None

        for job in jobs:
            if job["id"] == job_id:
                selected_job = job
                break

        if selected_job is None:
            return []

        ranking = []

        for candidate_data in candidates:

            candidate = self.dict_to_candidate(candidate_data)

            match = MatchingService.calculate_match(
                candidate,
                selected_job
            )

            ranking.append({
                "candidate": candidate_data["full_name"],
                "email": candidate_data["email"],
                "score": match["match_score"],
                "matched_skills": match["matched_skills"],
                "missing_skills": match["missing_skills"],
            })

        ranking.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return ranking