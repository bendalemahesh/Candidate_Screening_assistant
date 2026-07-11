import streamlit as st


def render_uploader():

    st.subheader("📄 Upload Documents")

    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        key="resume"
    )

    jd = st.file_uploader(
        "Upload Job Description",
        type=["pdf", "docx"],
        key="jd"
    )

    screen = st.button(
        "🚀 Screen Candidate",
        use_container_width=True
    )

    return resume, jd, screen