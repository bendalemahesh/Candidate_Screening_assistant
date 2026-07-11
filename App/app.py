import streamlit as st
from agents.resume_parser_agent import ResumeParserAgent
from components.header import render_header
from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.uploader import render_uploader
from components.footer import render_footer
from components.custom_css import load_css
from services.document_loader_service import get_file_loader
from services.resume_analyzer import ResumeAnalyzer
from services.matching_service import MatchingService
from agents.job_description_agent import JobDescriptionAgent



# Page Configuration
st.set_page_config(
    page_title="Recruiter AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load Custom CSS
load_css()

# Sidebar

render_sidebar()

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

        import os

        os.makedirs("App/uploads/assets", exist_ok=True)

        resume_path = os.path.join(
            "App/uploads/assets",
            resume.name
        )

        jd_path = os.path.join(
            "App/uploads/assets",
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

        st.subheader("Extracted Resume")
        st.text_area(
            "",
            resume_text,
            height=400
        )
        st.subheader("Extracted Job Description")
        st.text_area(
            "",
            jd_text,
            height=400
        )
        st.info("AI-powered candidate screening will be implemented in this week.")

        resume_text = "\n".join(
            doc.page_content for doc in resume_docs
        )

        resume_agent = ResumeParserAgent()

        jd_agent = JobDescriptionAgent()

        result = resume_agent.parse_resume(resume_text)

        candidate = result["candidate"]
        analysis = result["analysis"]

        job = jd_agent.parse_job_description(jd_text)

        st.subheader("👤 Candidate")
        st.json(candidate.model_dump())

        st.subheader("📝 Resume Analysis")
        st.json(analysis.model_dump())

        st.subheader("💼 Job Description")
        st.json(job.model_dump())

        match = MatchingService.calculate_match(
            candidate,
            job
        )
        
        candidate = result["candidate"]
        analysis = result["analysis"]

        #match = MatchingService.calculate_match(
        #    candidate.skills
        #)


        # analysis = ResumeAnalyzer.analyze(candidate)

        st.subheader("👤 Candidate Information")
        st.json(candidate.model_dump())

        st.subheader("📝 Candidate Summary")
        st.write(analysis.candidate_summary)

        st.subheader("💪 Strengths")
        for strength in analysis.strengths:
            st.success(f"✔ {strength}")

        st.subheader("⚠️ Weaknesses")
        for weakness in analysis.weaknesses:
            st.warning(f"• {weakness}")

        st.subheader("🎯 Recommendation")

        if analysis.recommendation == "Shortlist":
            st.success("🟢 Shortlist")
        elif analysis.recommendation == "Hold":
            st.warning("🟡 Hold")
        else:
            st.error("🔴 Reject")

        st.subheader("📊 Resume Match")

        st.metric(
            "Match Score",
            f"{match['match_score']}%"
        )

        st.write("### ✅ Matched Skills")
        st.write(match["matched_skills"])

        st.write("### ❌ Missing Skills")
        st.write(match["missing_skills"])

# Footer
render_footer()

