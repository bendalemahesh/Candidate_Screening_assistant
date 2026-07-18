import os
import streamlit as st

from components.uploader import render_job_uploader
from services.document_loader_service import get_file_loader
from agents.job_description_agent import JobDescriptionAgent
from services.database_service import DatabaseService
import inspect
from components.uploader import render_job_uploader

st.code(inspect.getsource(render_job_uploader))


def render():

    st.title("💼 Upload Job Description")
    jd = render_job_uploader()
   

    if jd is None:
        st.info("Please upload a Job Description.")
        return

    # ---------------- Save JD ---------------- #

    os.makedirs(
        "App/uploads/assets/job_descriptions",
        exist_ok=True
    )

    jd_path = os.path.join(
        "App/uploads/assets/job_descriptions",
        jd.name
    )

    with open(jd_path, "wb") as f:
        f.write(jd.getbuffer())

    # ---------------- Extract Text ---------------- #

    docs = get_file_loader(jd_path)

    jd_text = "\n".join(
        doc.page_content
        for doc in docs
    )

    # ---------------- AI Parsing ---------------- #

    agent = JobDescriptionAgent()

    with st.spinner("🤖 AI is analyzing Job Description..."):

        job = agent.parse_job_description(jd_text)

    # ---------------- Preview ---------------- #

    st.divider()

    st.subheader("📋 Job Summary")

    with st.container(border=True):

        st.write(f"### {job.job_title}")

        st.write(f"**Company:** {job.company}")

        st.write(f"**Location:** {job.company_location}")

        st.write(f"**Employment Type:** {job.employment_type}")

        st.write(f"**Experience:** {job.experience_required}")

        st.write(f"**Education:** {job.education_required}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Required Skills")

        for skill in job.required_skills:
            st.success(skill)

    with col2:

        st.subheader("⭐ Preferred Skills")

        for skill in job.preferred_skills:
            st.info(skill)

    st.divider()

    st.subheader("📝 Responsibilities")

    for item in job.responsibilities:
        st.success(f"• {item}")

    st.divider()

    # ---------------- Save ---------------- #

    if st.button("💾 Save Job Description", use_container_width=True):
        db = DatabaseService()
        job_id = db.save_job(job)
        existing = db.job_exists(job)
        
        if existing:
            st.warning("⚠️ This Job Description already exists.")
        else:
            job_id = db.save_job(job)
            st.success(f"✅ Job saved successfully (ID: {job_id})")