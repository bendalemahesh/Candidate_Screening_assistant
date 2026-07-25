from langchain_core.messages import HumanMessage

from agents.supervisor_agent import SupervisorAgent

from workflows.candidate_workflow import candidate_workflow
from workflows.job_workflow import job_workflow


class SupervisorWorkflow:

    def __init__(self):

        self.supervisor = SupervisorAgent()

    def invoke(self, query: str):

        # Ask Supervisor which agent to use
        route = self.supervisor.agent_node(
            {
                "messages": [
                    HumanMessage(content=query)
                ]
            }
        )

        selected_agent = route["messages"][-1].content.strip()

        print(f"Routing To -> {selected_agent}")

        # Candidate Agent
        if selected_agent == "CandidateAgent":

            response = candidate_workflow.invoke(
                {
                    "messages": [
                        HumanMessage(content=query)
                    ]
                }
            )

            return response["messages"][-1].content

        # Job Agent
        elif selected_agent == "JobAgent":

            response = job_workflow.invoke(
                {
                    "messages": [
                        HumanMessage(content=query)
                    ]
                }
            )

            return response["messages"][-1].content

        return "I don't know which agent should answer."