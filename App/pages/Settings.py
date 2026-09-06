import streamlit as st


def render():
    st.title("⚙️ Settings")

    st.subheader("🤖 AI Model")
    st.info("AI is powered by Groq (LLM).")

    st.subheader("🛡️ Privacy Notice")
    st.warning(
        "⚠️ **AI Assistance Disclaimer**: This system uses AI to assist recruiters "
        "in screening and ranking candidates. AI-generated scores and recommendations "
        "are for informational purposes only. **The final hiring decision rests solely "
        "with the human recruiter.** Candidate ranking is based exclusively on "
        "job-relevant qualifications (skills, experience, education) and does NOT "
        "consider protected characteristics such as gender, caste, religion, or age."
    )

    
