from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from agents.recruiter_chat_agent import RecruiterChatAgent


# =====================================================
# State
# =====================================================

class RecruiterChatState(TypedDict):
    messages: Annotated[list, add_messages]


# =====================================================
# Agent
# =====================================================

recruiter_chat_agent = RecruiterChatAgent()

tool_node = ToolNode(recruiter_chat_agent.tools)


# =====================================================
# Router
# =====================================================

def should_continue(state: RecruiterChatState):

    messages = state["messages"]

    last_message = messages[-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END


# =====================================================
# Graph
# =====================================================

graph = StateGraph(RecruiterChatState)

graph.add_node(
    "agent",
    recruiter_chat_agent.agent_node
)

graph.add_node(
    "tools",
    tool_node
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

recruiter_chat_workflow = graph.compile()