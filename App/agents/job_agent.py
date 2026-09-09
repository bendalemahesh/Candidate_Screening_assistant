from agents.base_agent import BaseAgent

from tools.database_tool import (
    get_all_jobs,
    get_job_by_id,
    search_job,
    count_jobs,
)


JOB_PROMPT = """
You are an expert Job Description Agent.

Your responsibility is ONLY job-related tasks.

You can:

- Show all jobs
- Search jobs
- Count jobs
- Explain job descriptions
- Explain required skills
- Explain preferred skills
- Explain responsibilities
- Compare job descriptions

Always use tools whenever job information is required.

Never invent job data.
"""


class JobAgent(BaseAgent):

    def __init__(self):

        super().__init__(

            system_prompt=JOB_PROMPT,

            tools=[

                get_all_jobs,
                get_job_by_id,
                search_job,
                count_jobs,

            ]

        )