import streamlit as st
from workflows.supervisor_workflow import SupervisorWorkflow

supervisor = SupervisorWorkflow()

def render():

    st.title("💬 Recruiter AI Assistant")

    # ---------------- Initialize Chat ---------------- #

    if "messages" not in st.session_state:

        st.session_state.messages = [

            {
                "role": "assistant",
                "content":
                """
                👋 Hello Recruiter!

                I'm your **Recruiter AI Assistant**.

                I can help you with:

                • Candidate Search\n
                • Job Search\n
                • Candidate Ranking\n
                • Recommendations\n
                • Analytics\n

                Ask me anything!
                """
            }

        ]

    # ---------------- Display Chat History ---------------- #

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # ---------------- Chat Input ---------------- #

    prompt = st.chat_input(
        "Ask me anything about candidates or jobs..."
    )

    reply = ""

    if prompt:

        # Show User Message

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        # Temporary Assistant Reply  

        if prompt:
            answer = supervisor.invoke(prompt)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.markdown(answer)

        elif prompt == "help" or "what can you do":
            reply = (
                """
            🤖 I can help you with:

                📄 Candidates
                • Show all candidates\n
                • Search candidate\n
                • Total candidates\n\n

                💼 Jobs
                • Show all jobs\n
                • Search job\n
                • Total jobs\n\n

                🏆 Matching
                • Best candidate\n
                • Best job\n\n

                📊 Analytics
                • Candidate ranking\n

            """
            )
        else:
            reply = (
                "🚧 I'm still under development.\n\n"
                "Week 4 features are currently being added."
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

        with st.chat_message("assistant"):

            st.markdown(reply)