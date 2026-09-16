import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "https://candidate-screening-assistant.onrender.com")


def render():

    st.title("💬 Recruiter AI Assistant")

    # ─── Initialize Chat History ───
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "👋 Hello Recruiter!\n\n"
                    "I'm your **Recruiter AI Assistant**.\n\n"
                    "I can help you with:\n"
                    "- 📄 Candidate Search\n"
                    "- 💼 Job Search\n"
                    "- 🏆 Candidate Ranking\n"
                    "- 📊 Analytics & Recommendations\n\n"
                    "Ask me anything!"
                )
            }
        ]

    # ─── Display Chat History ───
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ─── Chat Input ───
    prompt = st.chat_input("Ask me anything about candidates or jobs...")

    if prompt:
        # Show user message immediately
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call backend /chat endpoint
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                try:
                    resp = requests.post(
                        f"{BACKEND_URL}/chat",
                        json={"query": prompt},
                        timeout=60
                    )
                    resp.raise_for_status()
                    answer = resp.json().get("reply", "Sorry, I couldn't generate a response.")
                except requests.exceptions.ConnectionError:
                    answer = (
                        "⚠️ **Backend is offline.**\n\n"
                        "Please start the FastAPI backend:\n"
                        "```\nuvicorn App.backend.main:app --reload\n```"
                    )
                except Exception as e:
                    answer = f"⚠️ Error communicating with backend: `{e}`"

            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})