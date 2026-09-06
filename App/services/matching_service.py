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
                for skill in job.get("required_skills", [])
            }
            preferred_skills = {
                skill.lower().strip()
                for skill in job.get("preferred_skills", [])
            }
        else:
            job_skills = {
                skill.lower().strip()
                for skill in job.required_skills
            }
            preferred_skills = {
                skill.lower().strip()
                for skill in getattr(job, "preferred_skills", [])
            }

        matched = candidate_skills & job_skills
        matched_preferred = candidate_skills & preferred_skills

        skill_score = min(len(matched) / max(len(job_skills), 1) * 100, 100)
        
        # Simple heuristics for other categories
        experience_score = min(len(candidate.experience) * 20, 100)
        education_score = 100 if candidate.education else 0
        projects_score = min(len(candidate.projects) * 25, 100) if hasattr(candidate, 'projects') and candidate.projects else 0
        cert_score = min(len(candidate.certifications) * 50, 100)
        
        # Calculate overall match score based on weights
        match_score = round(
            (skill_score * 0.40) +
            (experience_score * 0.20) +
            (education_score * 0.10) +
            (projects_score * 0.10) +
            (cert_score * 0.05) +
            (100 * 0.15) # Default buffer for location, notice period, etc.
        )
        
        # ATS Score calculation (similar but different weighting for ATS context)
        ats_score = round(
            (skill_score * 0.45) +
            (experience_score * 0.25) +
            (education_score * 0.15) +
            (projects_score * 0.10) +
            (5) # Base completeness
        )

        return {
            "match_score": min(match_score, 100),
            "ats_score": min(ats_score, 100),
            "matched_skills": sorted(matched),
            "missing_skills": sorted(job_skills - candidate_skills),
            "ats_breakdown": {
                "Skills Relevance": round(skill_score),
                "Experience": round(experience_score),
                "Education": round(education_score),
                "Projects": round(projects_score)
            }
        }