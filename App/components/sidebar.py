import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "https://candidate-screening-assistant.onrender.com")


def render_sidebar():

    # Quick stats from backend
    candidates_count = 0
    jobs_count = 0
    try:
        candidates_count = len(requests.get(f"{BACKEND_URL}/candidates", timeout=5).json())
        jobs_count = len(requests.get(f"{BACKEND_URL}/jobs", timeout=5).json())
    except:
        pass

    with st.sidebar:

        st.markdown("# 🤖 Recruiter AI")
        st.caption("AI Powered Hiring Assistant")
        st.divider()

        st.subheader("Navigation")

        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "📄 Screen Candidate",
                "💼 Upload Job Description",
                "🏆 Candidate Ranking",
                "👥 Candidate Database",
                "📅 Interview Scheduling",
                "📧 Communication",
                "📊 Analytics",
                "💬 Recruiter Chat",
                "✨ Features",
                "⚙️ Settings",
                "ℹ️ About",
            ],
            index=0,
            label_visibility="collapsed"
        )

        st.divider()

        st.subheader("System Status")

        backend_ok = False
        try:
            r = requests.get(f"{BACKEND_URL}/health", timeout=3)
            backend_ok = r.status_code == 200
        except:
            pass

        if backend_ok:
            st.success("🟢 Backend Online")
        else:
            st.error("🔴 Backend Offline — start FastAPI")

        st.info("🗄️ Database: SQLite")
        st.info("🤖 AI: Groq LLM")

        st.divider()

        st.subheader("Quick Status")
        st.metric("Candidates", candidates_count)
        st.metric("Jobs", jobs_count)

        st.divider()
        st.caption("v1.0 — Recruiter AI Assistant")

    return page