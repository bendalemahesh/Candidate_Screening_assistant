import streamlit as st
from workflows.dashboard_workflow import dashboard_workflow
response = dashboard_workflow.invoke({

        "dashboard": {}

    })

data = response["dashboard"]

def render_sidebar():

    with st.sidebar:

        st.markdown("# 🤖 Recruiter AI")

        st.caption("AI Powered Hiring Assistant")

        st.divider()

        st.subheader("Navigation")

        page = st.radio(
            "Navigation",
        [
            "📄 Screen Candidate",
            "💼 Upload Job Description",
            "🏆 Candidate Ranking",
            "📧 Communication",
            "📅 Interview Scheduling",
            "📊 Analytics",
            "💬 Recruiter Chat",
            "👥 Candidate Database",
            "🏠 Dashboard",
            "⚙️ Settings",
            "✨ Features",
            "ℹ️ About",
        ],
            index=0,
            label_visibility="collapsed"
    )

        st.divider()

        st.subheader("System Status")

        st.success("🟢 AI Online")

        st.info("Embedding Model\nGemini Embeddings")

        st.info("Vector Database\nChromaDB")

        st.info("Database\nSQLite")

        st.divider()

        st.subheader("Quick Status")

        st.metric("Candidates", f"{len(data["candidates"])}")
        st.metric("Jobs", f"{len(data["jobs"])}")

        st.metric("Screenings", f"{len(data["candidates"])}")

        st.divider()

        st.caption("Version 1.0")

    return page

    with st.sidebar:

        st.title("🤖 Recruiter AI")

        st.success("RESUME SCREENING & JOB MATCHING")

        st.divider()

        st.info(
            "AI-powered candidate screening platform."
        )