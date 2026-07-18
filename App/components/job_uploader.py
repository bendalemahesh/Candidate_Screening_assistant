import streamlit as st

def render_job_uploader():

    st.subheader("💼 Upload Job Description")

    jd = st.file_uploader(
        "Upload Job Description",
        type=["pdf", "docx"],
        key="job_description"
    )

    return jd