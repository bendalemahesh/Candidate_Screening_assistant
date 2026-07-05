import streamlit as st


def render_uploader():

    st.subheader("📂 Resume Upload")

    resume = st.file_uploader(
        "Upload Candidate Resume",
        type=["pdf", "docx"]
    )

    st.subheader("📝 Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=220
    )

    screen = st.button(
        "🚀 Screen Candidate",
        use_container_width=True
    )

    return resume, job_description, screen