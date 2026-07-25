from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from agents.job_agent import JobAgent


# =====================================================
# State
# =====================================================

class JobState(TypedDict):
    messages: Annotated[list, add_messages]


# =====================================================
# Agent
# =====================================================

job_agent = JobAgent()

tool_node = ToolNode(job_agent.tools)


# =====================================================
# Router
# =====================================================

def should_continue(state: JobState):

    messages = state["messages"]

    last_message = messages[-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END


# =====================================================
# Graph
# =====================================================

graph = StateGraph(JobState)

graph.add_node(
    "agent",
    job_agent.agent_node
)

graph.add_node(
    "tools",
    job_agent.tool_node
)

graph.add_edge(
    START,
    "agent"
)

graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

graph.add_edge(
    "tools",
    "agent"
)

job_workflow = graph.compile()