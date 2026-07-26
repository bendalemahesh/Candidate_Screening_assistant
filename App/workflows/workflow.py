from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from candidate_workflow import candidate_workflow
from job_workflow import job_workflow
from candidate_screening_workflow import candidate_screening_workflow
from recruiter_chat_workflow import recruiter_chat_workflow

class WorkflowState(TypedDict):

    page: str

    input: dict

    output: dict

def supervisor(state: WorkflowState):

    print("Supervisor")

    print("Page :", state["page"])

    return state

def route_page(state: WorkflowState):

    page = state["page"]

    if page == "screening":
        return "screening"

    elif page == "ranking":
        return "ranking"

    elif page == "chat":
        return "chat"

    elif page == "candidate_db":
        return "candidate_db"

    elif page == "job_db":
        return "job_db"

    elif page == "analytics":
        return "analytics"

    elif page == "settings":
        return "settings"

    return END

def screening_node(state):

    result = candidate_screening_workflow.invoke(
        state["input"]
    )

    state["output"] = result

    return state

def ranking_node(state):
    print("Candidate Ranking Workflow")
    return state


def chat_node(state):

    result = recruiter_chat_workflow.invoke(

        state["input"]

    )

    state["output"] = result

    return state


def candidate_db_node(state):

    result = candidate_workflow.invoke(
        state["input"]
    )

    state["output"] = result

    return state


def job_db_node(state):

    result = job_workflow.invoke(
        state["input"]
    )

    state["output"] = result

    return state


def analytics_node(state):
    print("Analytics Workflow")
    return state


def settings_node(state):
    print("Settings Workflow")
    return state

graph = StateGraph(WorkflowState)

graph.add_node(
    "Supervisor",
    supervisor
)

graph.add_edge(
    START,
    "Supervisor"
)

graph.add_node("screening", screening_node)

graph.add_node("ranking", ranking_node)

graph.add_node("chat", chat_node)

graph.add_node("candidate_db", candidate_db_node)

graph.add_node("job_db", job_db_node)

graph.add_node("analytics", analytics_node)

graph.add_node("settings", settings_node)

graph.add_edge("screening", END)

graph.add_edge("ranking", END)

graph.add_edge("chat", END)

graph.add_edge("candidate_db", END)

graph.add_edge("job_db", END)

graph.add_edge("analytics", END)

graph.add_edge("settings", END)

graph.add_conditional_edges(

    "Supervisor",

    route_page,

    {

        "screening": "screening",

        "ranking": "ranking",

        "chat": "chat",

        "candidate_db": "candidate_db",

        "job_db": "job_db",

        "analytics": "analytics",

        "settings": "settings",

        END: END

    }

)


workflow = graph.compile()
