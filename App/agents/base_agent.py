import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
)
import json
load_dotenv()


class BaseAgent:

    def __init__(self, system_prompt: str, tools: list):

        self.system_prompt = system_prompt

        self.tools = tools

        self.tools_by_name = {
            tool.name: tool
            for tool in tools
        }

        self.llm = ChatGroq(

            model="openai/gpt-oss-20b",

            temperature=0.2,

            api_key=os.getenv("GROQ_API_KEY")

        )

        self.llm_with_tools = self.llm.bind_tools(
            self.tools
        )

    # ==================================================

    def agent_node(self, state):

        messages = state["messages"]

        llm_input = [

            SystemMessage(
                content=self.system_prompt
            )

        ]

        llm_input.extend(messages)

        response = self.llm_with_tools.invoke(
            llm_input
        )

        return {

            "messages": [response]

        }

    # ==================================================

    def tool_node(self, state):

        messages = state["messages"]

        last_message = messages[-1]

        outputs = []

        if hasattr(last_message, "tool_calls"):

            for tool_call in last_message.tool_calls:

                tool_name = tool_call["name"]

                tool_args = tool_call["args"]

                tool_function = self.tools_by_name.get(
                    tool_name
                )

                if tool_function:

                    result = tool_function.invoke(
                        tool_args
                    )

                else:

                    result = f"Tool {tool_name} not found."

                outputs.append(
                    ToolMessage(
                        content=json.dumps(result, indent=2, default=str),
                        tool_call_id=tool_call["id"]
                    )
                )

        return {

            "messages": outputs

        }