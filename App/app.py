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
resume, job_description, screen = render_uploader()

# Placeholder Logic
if screen:
    if resume is None:
        st.warning("Please upload a resume.")
    elif job_description.strip() == "":
        st.warning("Please enter a Job Description.")
    else:
        import os

        # Create uploads folder
        os.makedirs("App/uploads/assets", exist_ok=True)

        # Save uploaded file
        resume_path = os.path.join("App/uploads/assets", resume.name)

        with open(resume_path, "wb") as f:
            f.write(resume.getbuffer())

        # Load document using LangChain
        documents = get_file_loader(resume_path)

        # Display extracted text
        resume_text = "\n\n".join(doc.page_content for doc in documents)

        st.success("✅ Resume uploaded successfully!")

        st.text_area(
            "Extracted Resume",
            resume_text,
            height=400
        )
        st.info("AI-powered candidate screening will be implemented in this week.")

        resume_text = "\n".join(
            doc.page_content for doc in documents
        )

        agent = ResumeParserAgent()

        result = agent.parse_resume(resume_text)

        candidate = result["candidate"]
        analysis = result["analysis"]

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

# Footer
render_footer()

