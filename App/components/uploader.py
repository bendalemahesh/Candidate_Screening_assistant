import streamlit as st

def render_resume_uploader():

    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        key="resume"
    )

    screen = st.button(
        "🚀 Screen Candidate",
        use_container_width=True
    )

    return resume, screen




def render_job_uploader():

    jd = st.file_uploader(
        "Upload Job Description",
        type=["pdf", "docx"],
        key="job_upload"
    )

    return jd