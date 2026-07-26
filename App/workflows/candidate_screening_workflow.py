from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from App.services.database_service import DatabaseService
from App.services.matching_service import MatchingService
from App.services.ai_recommendation_service import AIRecommendationService
from App.models.candidate_profile_model import (
    CandidateProfile,
    Education,
    Experience,
    Certification,
)


class ScreeningState(TypedDict):

    candidate_id: int

    job_id: int

    candidate: dict

    job: dict

    match: dict

    recommendation: str


def load_candidate(state: ScreeningState):

    db = DatabaseService()

    try:

        state["candidate"] = db.get_candidate_by_id(
            state["candidate_id"]
        )

        return state

    finally:

        db.close()

def load_job(state: ScreeningState):

    db = DatabaseService()

    try:

        state["job"] = db.get_job_by_id(
            state["job_id"]
        )

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

def calculate_match(state: ScreeningState):
    
    candidate = dict_to_candidate(
        state["candidate"]
    )

    match = MatchingService.calculate_match(

        candidate,

        state["job"]

    )

    state["match"] = match

    return state

def generate_recommendation(state: ScreeningState):

    ai_service = AIRecommendationService()

    candidate = dict_to_candidate(
        state["candidate"]
    )

    recommendation = ai_service.generate_recommendation(

        candidate,

        state["job"],

        state["match"]

    )

    state["recommendation"] = recommendation

    return state

graph = StateGraph(ScreeningState)

graph.add_node(
    "load_candidate",
    load_candidate
)

graph.add_node(
    "load_job",
    load_job
)

graph.add_node(
    "calculate_match",
    calculate_match
)

graph.add_node(
    "generate_recommendation",
    generate_recommendation
)

graph.add_edge(
    START,
    "load_candidate"
)

graph.add_edge(
    "load_candidate",
    "load_job"
)

graph.add_edge(
    "load_job",
    "calculate_match"
)

graph.add_edge(
    "calculate_match",
    "generate_recommendation"
)

graph.add_edge(
    "generate_recommendation",
    END
)

screening_workflow = graph.compile()