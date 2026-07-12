from agents import job_description_agent
from database.update_schema import DB_PATH
import os
import streamlit as st
from agents.resume_parser_agent import ResumeParserAgent
from components.header import render_header
from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.uploader import render_uploader
from components.footer import render_footer
from components.custom_css import load_css
from services.document_loader_service import get_file_loader
from services.matching_service import MatchingService
from agents.job_description_agent import JobDescriptionAgent
from services.database_service import DatabaseService
from services.batch_maneger_service import BatchManager
from services.document_generator_service import DocumentGenerator


# Page Configuration
st.set_page_config(
    page_title="Recruiter AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("""
<h1 style="text-align:center;color:#2563EB;">
🤖 Recruiter AI Assistant
</h1>

<p style="text-align:center;color:gray;">
AI Powered Resume Screening System
</p>
""", unsafe_allow_html=True)

# Load Custom CSS
load_css()

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)
# Sidebar

page = render_sidebar()

if page == "📄 Screen Candidate":

    # Header
    render_header()

    # Dashboard Metrics
    render_metrics()

    # Resume Upload Section
    resume, jd, screen = render_uploader()

    # Placeholder Logic
    if screen:
        if resume is None:
            st.warning("Please upload a Resume.")
            st.stop()

        if jd is None:
            st.warning("Please upload a Job Description.")
            st.stop()
        else:
            import os

            os.makedirs("App/uploads/assets/resumes", exist_ok=True)
            os.makedirs("App/uploads/assets/job_descriptions", exist_ok=True)

            resume_path = os.path.join(
                "App/uploads/assets/resumes",
                resume.name
            )

            jd_path = os.path.join(
                "App/uploads/assets/job_descriptions",
                jd.name
            )

            with open(resume_path, "wb") as f:
                f.write(resume.getbuffer())

            with open(jd_path, "wb") as f:
                f.write(jd.getbuffer())

            # Load document using LangChain
            resume_docs = get_file_loader(resume_path)

            jd_docs = get_file_loader(jd_path)

            resume_text = "\n".join(
                doc.page_content
                for doc in resume_docs
            )

            jd_text = "\n".join(
                doc.page_content
                for doc in jd_docs
            )

            st.success("✅ Resume uploaded successfully!")

            resume_text = "\n".join(
                doc.page_content for doc in resume_docs
            )

            resume_agent = ResumeParserAgent()

            jd_agent = JobDescriptionAgent()

            with st.spinner("🤖 AI is screening the candidate..."):

                result = resume_agent.parse_resume(resume_text)

                candidate = result["candidate"]
                analysis = result["analysis"]

                job = jd_agent.parse_job_description(jd_text)

                match = MatchingService.calculate_match(candidate, job)

            st.divider()
            
            st.subheader("📝 Candidate Summary")

            with st.container(border=True):
                st.write(analysis.candidate_summary)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("💪 Strengths")

                for strength in analysis.strengths:
                    st.success(f"✔ {strength}")

            with col2:
                st.subheader("⚠️ Weaknesses")

                for weakness in analysis.weaknesses:
                    st.warning(f"• {weakness}")

            st.subheader("🎯 Final Recommendation")

            st.divider()

            if analysis.recommendation == "Shortlist":
                st.success("🟢 SHORTLIST")

            elif analysis.recommendation == "Hold":
                st.warning("🟡 HOLD")

            else:
                st.error("🔴 REJECT")

            st.divider()

            st.subheader("📊 Match Score")

            st.progress(match["match_score"] / 100)

            st.metric(
                label="Overall Match",
                value=f"{match['match_score']}%"
            )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Matched Skills")

                for skill in match["matched_skills"]:
                    st.success(skill)

            with col2:
                st.subheader("❌ Missing Skills")

                for skill in match["missing_skills"]:
                    st.warning(skill)

            st.divider()

            if st.button("Save Candidate"):
                db = DatabaseService()

                candidate_id = db.save_candidate(candidate)
                job_id = db.save_job(job)

                st.success("✅ Candidate saved successfully!")

            st.info("AI-powered candidate screening will be implemented in this week.")

elif page == "🏠 Dashboard":

    st.title("🏠 Dashboard")
    st.info("Welcome to Recruiter AI Assistant")

elif page == "💬 Recruiter Chat":

    st.title("💬 Recruiter Chat")
    st.info("Coming in Week 2")

elif page == "👥 Candidate Database":

    st.title("👥 Candidate Database")
    st.info("Coming in Week 2")

elif page == "📊 Analytics":

    st.title("📊 Analytics")
    st.info("Coming in Week 3")

elif page == "⚙️ Settings":

    st.title("⚙️ Settings")
    st.info("Coming Soon")

elif page == "ℹ️ About":

    st.title("ℹ️ About")

    st.write("""
    ## Recruiter AI Assistant

    AI-powered candidate screening system built using:

    - LangChain
    - Google Gemini
    - ChromaDB
    - SQLite
    - Streamlit
    """)


# Footer
render_footer()