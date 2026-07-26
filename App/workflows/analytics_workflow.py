from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from collections import Counter
from services.database_service import DatabaseService
from services.analytics_service import AnalyticsService

class AnalyticsState(TypedDict):

    candidates: list

    jobs: list

    analytics: dict


def load_candidates(state: AnalyticsState):

    db = DatabaseService()

    try:

        state["candidates"] = db.get_all_candidates()

        return state

    finally:

        db.close()

def load_jobs(state: AnalyticsState):

    db = DatabaseService()

    try:

        state["jobs"] = db.get_all_jobs()

        return state

    finally:

        db.close()

def generate_analytics(state: AnalyticsState):

    analytics_service = AnalyticsService()

    state["analytics"] = analytics_service.get_dashboard_data()

    return state

graph = StateGraph(AnalyticsState)

graph.add_node(
    "load_candidates",
    load_candidates
)

graph.add_node(
    "load_jobs",
    load_jobs
)

graph.add_node(
    "generate_analytics",
    generate_analytics
)

# Edges
graph.add_edge(
    START,
    "load_candidates"
)

graph.add_edge(
    "load_candidates",
    "load_jobs"
)

graph.add_edge(
    "load_jobs",
    "generate_analytics"
)

graph.add_edge(
    "generate_analytics",
    END
)

analytics_workflow = graph.compile()