import os
import requests
import streamlit as st
from components.uploader import render_resume_uploader
from models.candidate_profile_model import CandidateProfile
# pyrefly: ignore [missing-import]
from schemas.analysis_schema import JobAnalysis
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

#def candidate_screening():
def render():

    st.title("📄 candidate screening")

    if "candidate" not in st.session_state:
        st.session_state.candidate = None
        st.session_state.analysis = None
        st.session_state.top_matches = None
        st.session_state.best_job = None
        st.session_state.best_match = None

    resume, screen = render_resume_uploader()

    if screen:

        if resume is None:
            st.warning("Please upload a Resume.")
            st.stop()

        with st.spinner("🤖 AI is analyzing the resume..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/candidates/screen",
                    files={"file": (resume.name, resume.getvalue(), resume.type)}
                )
                response.raise_for_status()
                result = response.json()
            except Exception as e:
                st.error(f"Error communicating with backend: {e}")
                st.stop()

        candidate_data = result["candidate"]
        analysis_data = result["analysis"]
        
        # Instantiate model classes for consistency (or use as dict)
        candidate = CandidateProfile(**candidate_data)
        
        class MockAnalysis:
            pass
        analysis = MockAnalysis()
        analysis.candidate_summary = analysis_data.get("candidate_summary", "")
        analysis.strengths = analysis_data.get("strengths", [])
        analysis.weaknesses = analysis_data.get("weaknesses", [])
        analysis.recommendation = analysis_data.get("recommendation", "")

        try:
            jobs_response = requests.get(f"{BACKEND_URL}/jobs")
            jobs = jobs_response.json()
        except:
            jobs = []

        if len(jobs) == 0:
            st.warning("No Job Descriptions found.")
            st.stop()

        all_matches = []

        for job_data in jobs:
            try:
                match_resp = requests.post(
                    f"{BACKEND_URL}/match",
                    json={"candidate": candidate.model_dump(), "job": job_data}
                )
                if match_resp.status_code == 200:
                    match = match_resp.json()
                    all_matches.append({
                        "job": job_data,
                        "match": match
                    })
            except:
                pass

        all_matches.sort(
            key=lambda x: x["match"].get("match_score", 0),
            reverse=True
        )

        top_matches = all_matches[:5]

        st.session_state.candidate = candidate
        st.session_state.analysis = analysis
        st.session_state.top_matches = top_matches
        st.session_state.best_job = top_matches[0]["job"]
        st.session_state.best_match = top_matches[0]["match"]

    if st.session_state.candidate is None:
        return

    candidate = st.session_state.candidate
    analysis = st.session_state.analysis
    top_matches = st.session_state.top_matches
    best_job = st.session_state.best_job
    best_match = st.session_state.best_match


    st.subheader("🎯 Top Matching Jobs")

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    for i, item in enumerate(top_matches):

        current_job = item["job"]
        current_match = item["match"]

        with st.container(border=True):

            st.markdown(
                f"""
    ### {medals[i]} {current_job['job_title']}

    🏢 **{current_job['company']}**

    📊 **Match Score:** {current_match['match_score']}%
    """
            )

            st.progress(current_match["match_score"] / 100)


    # ---------------- Display Results ---------------- #

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

    st.divider()

    st.subheader("🎯 Recommendation")

    if analysis.recommendation == "Shortlist":
        st.success("🟢 SHORTLIST")

    elif analysis.recommendation == "Hold":
        st.warning("🟡 HOLD")

    else:
        st.error("🔴 REJECT")

    st.divider()
    st.subheader("🏆 Best Matching Job")

    st.success(
        f"{best_job['job_title']} | {best_job['company']}"
    )

    st.metric(
        "Match Score",
        f"{best_match['match_score']}%"
    )
    
    # ---------------- Save Candidate ---------------- #

    if st.button("💾 Save Candidate", use_container_width=True):
        try:
            save_resp = requests.post(
                f"{BACKEND_URL}/candidates",
                json=candidate.model_dump()
            )
            if save_resp.status_code == 200:
                candidate_id = save_resp.json().get("id")
                st.success(f"✅ Candidate saved successfully (ID: {candidate_id})")
            else:
                st.warning(f"⚠️ {save_resp.json().get('detail', 'Failed to save')}")
        except Exception as e:
            st.error(f"Error saving candidate: {e}")