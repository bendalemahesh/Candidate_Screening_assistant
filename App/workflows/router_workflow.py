from langchain_core.messages import HumanMessage

from workflows.candidate_workflow import candidate_workflow
from workflows.job_workflow import job_workflow
from workflows.ranking_workflow import ranking_workflow
from workflows.candidate_screening_workflow import CandidateScreeningWorkflow


class WorkflowRouter:

    @staticmethod
    def invoke(query: str):

        query = query.lower()

        # Ranking First

        ranking_keywords = [
            "best",
            "rank",
            "ranking",
            "highest",
            "top",
            "match",
            "score",
            "suitable"
        ]
        if any(word in query for word in ranking_keywords):
            print("Routing -> Ranking Workflow")

            return ranking_workflow.invoke(
                {
                    "job": {"id": 1},
                    "candidates": [],
                    "ranking": []
                }
            )

        # -------------------------
        # Candidate Workflow
        # -------------------------

        if "candidate" in query:

            print("Routing -> Candidate Workflow")

            return candidate_workflow.invoke(
                {
                    "messages": [
                        HumanMessage(content=query)
                    ]
                }
            )

        # -------------------------
        # Job Workflow
        # -------------------------

        elif "job" in query:

            print("Routing -> Job Workflow")

            return job_workflow.invoke(
                {
                    "messages": [
                        HumanMessage(content=query)
                    ]
                }
            )

        # -------------------------
        # Screening Workflow
        # -------------------------

        elif "screen" in query:

            print("Routing -> Screening Workflow")

            return CandidateScreeningWorkflow.invoke(
                {
                    "messages": [
                        HumanMessage(content=query)
                    ]
                }
            )

        else:

            return "No suitable workflow found."