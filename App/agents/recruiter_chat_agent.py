from agents.base_agent import BaseAgent

from tools.database_tool import *

system_prompt = """
You are an AI Recruiter.

You answer recruiter questions.

You have access to:

Candidate Database

Job Database

Ranking Database

Always use tools whenever information exists in the database.

Never guess.

Always answer using the retrieved information.
"""

class RecruiterChatAgent(BaseAgent):

    def __init__(self):

        super().__init__(

            system_prompt,

            [

                get_all_candidates,

                get_candidate_by_id,

                search_candidate,

                count_candidates,

                get_all_jobs,

                get_job_by_id,

                search_job,

                count_jobs

            ]

        )