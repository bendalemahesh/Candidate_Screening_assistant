import streamlit as st

def render_sidebar():

    with st.sidebar:

        st.markdown("# 🤖 Recruiter AI")

        st.caption("AI Powered Hiring Assistant")

        st.divider()

        st.subheader("Navigation")

        page = st.radio(
            "",
        [
            "📄 Screen Candidate",
            "🏠 Dashboard",
            "💬 Recruiter Chat",
            "👥 Candidate Database",
            "📊 Analytics",
            "⚙️ Settings",
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

        st.subheader("Quick Stats")

        st.metric("Candidates", "0")

        st.metric("Jobs", "0")

        st.metric("Screenings", "0")

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