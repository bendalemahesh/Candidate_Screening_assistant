from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from agents.ranking_agent import RankingAgent
from services.database_service import DatabaseService
from services.matching_service import MatchingService
from models.candidate_profile_model import (
    CandidateProfile,
    Education,
    Experience,
    Certification,
)


class RankingState(TypedDict):

    job: dict

    candidate: dict

    candidates: list

    ranking: list

    match: dict

    messages: list

def load_candidates(state):

    db = DatabaseService()

    try:

        state["candidates"] = db.get_all_candidates()

        return state

    finally:

        db.close()
        
def load_job(state: RankingState):

    db = DatabaseService()

    try:

        job_id = state["job"]["id"]

        state["job"] = db.get_job_by_id(job_id)

        return state

    finally:

        db.close()

def dict_to_candidate(data):

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

def calculate_ranking(state: RankingState):

    ranking_agent = RankingAgent()

    ranking = []

    for candidate_data in state["candidates"]:

        candidate = dict_to_candidate(candidate_data)

        match = MatchingService.calculate_match(
            candidate,
            state["job"]
        )

        ranking.append({

            "candidate": candidate_data,

            "match": match

        })

    ranking.sort(

        key=lambda x: x["match"]["match_score"],

        reverse=True

    )

    state["ranking"] = ranking

    return state



def explain_ranking(state):

    ranking_agent = RankingAgent()


    ranking = state["ranking"]

    prompt = f"""
        Job:

        {state['job']}

        Ranking:

        {ranking}

        Explain the ranking professionally.

        Mention:

        - Best candidate
        - Match Score
        - Matching Skills
        - Missing Skills
        - Why candidate ranked first
    """

    response = ranking_agent.llm.invoke(prompt)

    state["messages"] = [response]

    return state

graph = StateGraph(RankingState)

graph.add_node(
    "calculate_ranking",
    calculate_ranking
)

graph.add_node(
    "load_candidates",
    load_candidates
)

graph.add_node(
    "load_job",
    load_job
)

graph.add_node(
    "explain",
    explain_ranking
)

graph.add_edge(
    START,
    "load_candidates"
)

graph.add_edge(
    "load_candidates",
    "load_job"
)

graph.add_edge(
    "load_job",
    "calculate_ranking"
)

graph.add_edge(
    "calculate_ranking",
    "explain"
)

graph.add_edge(
    "explain",
END
)


ranking_workflow = graph.compile()