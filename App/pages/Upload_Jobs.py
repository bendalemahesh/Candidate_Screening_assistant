import os
import requests
import streamlit as st
from dotenv import load_dotenv
from components.uploader import render_job_uploader

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def render():

    st.title("💼 Upload Job Description")
    jd = render_job_uploader()
   

    if jd is None:
        st.info("Please upload a Job Description.")
        return


    # AI Parsing is done by the backend


    with st.spinner("🤖 AI is analyzing Job Description..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/jobs/upload",
                files={"file": (jd.name, jd.getvalue(), jd.type)}
            )
            response.raise_for_status()
            job = response.json()["job"]
        except Exception as e:
            st.error(f"Failed to parse Job Description: {e}")
            return

    # ---------------- Preview ---------------- #

    st.divider()

    st.subheader("📋 Job Summary")

    with st.container(border=True):
        st.write(f"### {job.get('job_title', 'N/A')}")
        st.write(f"**Company:** {job.get('company', 'N/A')}")
        st.write(f"**Location:** {job.get('company_location', 'N/A')}")
        st.write(f"**Employment Type:** {job.get('employment_type', 'N/A')}")
        st.write(f"**Experience:** {job.get('experience_required', 'N/A')}")
        st.write(f"**Education:** {job.get('education_required', 'N/A')}")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Required Skills")
        for skill in job.get("required_skills", []):
            st.success(skill)
    with col2:
        st.subheader("⭐ Preferred Skills")
        for skill in job.get("preferred_skills", []):
            st.info(skill)

    st.divider()
    st.subheader("📝 Responsibilities")
    for item in job.get("responsibilities", []):
        st.success(f"• {item}")

    st.divider()

    # ---------------- Save ---------------- #
    if st.button("💾 Save Job Description", use_container_width=True):
        try:
            save_resp = requests.post(
                f"{BACKEND_URL}/jobs",
                json=job
            )
            if save_resp.status_code == 200:
                st.success(f"✅ Job saved successfully (ID: {save_resp.json().get('id')})")
            else:
                st.warning(f"⚠️ {save_resp.json().get('detail', 'Failed to save.')}")
        except Exception as e:
            st.error(f"Error saving job: {e}")