import streamlit as st


def render_header():
    st.title("🤖 Recruiter AI Assistant")
    st.caption(
        "AI-powered Candidate Screening & Recruitment Assistant using "
        "LangChain + Gemini + ChromaDB"
    )

    st.divider()