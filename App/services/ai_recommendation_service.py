import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

load_dotenv()


class AIRecommendationService:

    def __init__(self):

        self.llm = ChatGroq(

            model="openai/gpt-oss-20b",

            temperature=0.2,

            api_key=os.getenv("GROQ_API_KEY")

        )

    def generate_recommendation(
        self,
        candidate,
        job,
        match
    ):
        system_prompt = """
            You are an expert Technical Recruiter.

            Your job is to evaluate a candidate for a job opening.

            Analyze:

                • Candidate Skills
                • Education
                • Experience
                • Certifications
                • Match Score
                • Missing Skills

            Then generate a professional hiring recommendation.

            Keep your response short and professional.

            Format:

                ### Overall Assessment

                ### Strengths

                ### Weaknesses

                ### Recommendation

                ### Interview Decision

            Interview Decision should be one of:

                ✅ Strongly Recommend

                🟡 Recommend

                ❌ Not Recommended
            """
            
        human_prompt = f"""
            Candidate Name:
            {candidate.full_name}

            Candidate Skills:
            {candidate.skills}

            Education:
            {candidate.education}

            Experience:
            {candidate.experience}

            Certifications:
            {candidate.certifications}

            Job Title:
            {job["job_title"]}

            Company:
            {job["company"]}

            Required Skills:
            {job["required_skills"]}

            Matched Skills:
            {match["matched_skills"]}

            Missing Skills:
            {match["missing_skills"]}

            Match Score:
            {match["match_score"]}%
            """

        response = self.llm.invoke(

            [

                SystemMessage(
                    content=system_prompt
                ),

                HumanMessage(
                    content=human_prompt
                )

            ]

        )

        return response.content