from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from services.dashboard_service import DashboardService


class DashboardState(TypedDict):

    dashboard: dict


def load_dashboard(state: DashboardState):

    dashboard_service = DashboardService()

    state["dashboard"] = dashboard_service.get_dashboard_data()

    return state


graph = StateGraph(DashboardState)

graph.add_node(
    "load_dashboard",
    load_dashboard
)

graph.add_edge(
    START,
    "load_dashboard"
)

graph.add_edge(
    "load_dashboard",
    END
)

dashboard_workflow = graph.compile()