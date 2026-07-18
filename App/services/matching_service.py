import json


class MatchingService:

    @staticmethod
    def calculate_match(candidate, job):

        print("✅ NEW MatchingService Running")

        candidate_skills = {
            skill.lower().strip()
            for skill in candidate.skills
        }

        if isinstance(job, dict):

            job_skills = {
                skill.lower().strip()
                for skill in job["required_skills"]
            }

        else:

            job_skills = {
                skill.lower().strip()
                for skill in job.required_skills
            }

        matched = candidate_skills & job_skills

        score = round(
            len(matched) /
            max(len(job_skills), 1) * 100
        )

        return {
            "match_score": score,
            "matched_skills": sorted(matched),
            "missing_skills": sorted(job_skills - candidate_skills),
        }