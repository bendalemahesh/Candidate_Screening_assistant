from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode

from agents.candidate_agent import CandidateAgent


# =====================================================
# Graph State
# =====================================================

class CandidateState(TypedDict):

    messages: Annotated[list, add_messages]


# =====================================================
# Agent
# =====================================================

candidate_agent = CandidateAgent()

tool_node = ToolNode(candidate_agent.tools)


# =====================================================
# Router
# =====================================================

def should_continue(state: CandidateState):

    messages = state["messages"]

    last_message = messages[-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:

        return "tools"

    return END


# =====================================================
# Graph
# =====================================================

graph = StateGraph(CandidateState)

graph.add_node(
    "agent",
    candidate_agent.agent_node
)

graph.add_node(
    "tools",
    candidate_agent.tool_node
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

candidate_workflow = graph.compile()