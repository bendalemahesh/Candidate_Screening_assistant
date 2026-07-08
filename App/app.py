import streamlit as st
from agents.resume_parser_agent import ResumeParserAgent
from components.header import render_header
from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.uploader import render_uploader
from components.footer import render_footer
from components.custom_css import load_css
from services.document_loader_service import get_file_loader


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
        os.makedirs("App/uploads", exist_ok=True)

        # Save uploaded file
        resume_path = os.path.join("App/uploads", resume.name)

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
        st.info("AI-powered candidate screening will be implemented in next submission.")

        resume_text = "\n".join(
            doc.page_content for doc in documents
        )

        agent = ResumeParserAgent()

        candidate = agent.parse_resume(resume_text)

        st.json(candidate.model_dump())

# Footer
render_footer()

