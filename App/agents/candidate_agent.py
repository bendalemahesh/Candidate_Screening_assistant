from agents.base_agent import BaseAgent

from tools.database_tool import (
    get_all_candidates,
    get_candidate_by_id,
    search_candidate,
    count_candidates,
)


CANDIDATE_PROMPT = """
You are an expert Candidate Screening Agent.

Your responsibility is ONLY candidate-related tasks.

You can:

- Show candidates
- Search candidates
- Count candidates
- Explain candidate profiles
- Summarize candidate skills
- Compare candidate information

Always use tools whenever candidate information is required.

Never invent candidate data.
"""


class CandidateAgent(BaseAgent):

    def __init__(self):

        super().__init__(

            system_prompt=CANDIDATE_PROMPT,

            tools=[

                get_all_candidates,
                get_candidate_by_id,
                search_candidate,
                count_candidates,

            ]

        )