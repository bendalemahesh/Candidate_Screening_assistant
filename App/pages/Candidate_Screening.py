import os
import requests
import streamlit as st
from components.uploader import render_resume_uploader
from models.candidate_profile_model import CandidateProfile
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "https://candidate-screening-assistant.onrender.com")


def render():

    st.title("📄 Candidate Screening")

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
                    files={"file": (resume.name, resume.getvalue(), resume.type)},
                    timeout=120
                )
                response.raise_for_status()
                result = response.json()
            except Exception as e:
                st.error(f"Error communicating with backend: {e}")
                st.stop()

        candidate_data = result["candidate"]
        analysis_data = result["analysis"]

        candidate = CandidateProfile(**candidate_data)

        class MockAnalysis:
            pass

        analysis = MockAnalysis()
        analysis.candidate_summary = analysis_data.get("candidate_summary", "")
        analysis.strengths = analysis_data.get("strengths", [])
        analysis.weaknesses = analysis_data.get("weaknesses", [])
        analysis.recommendation = analysis_data.get("recommendation", "")

        # Fetch jobs for matching (non-fatal if none available)
        try:
            jobs_response = requests.get(f"{BACKEND_URL}/jobs", timeout=10)
            jobs_response.raise_for_status()
            jobs = jobs_response.json()
        except Exception:
            jobs = []

        all_matches = []

        for job_data in jobs:
            try:
                match_resp = requests.post(
                    f"{BACKEND_URL}/match",
                    json={"candidate": candidate.model_dump(), "job": job_data},
                    timeout=15
                )
                if match_resp.status_code == 200:
                    match = match_resp.json()
                    all_matches.append({"job": job_data, "match": match})
            except Exception:
                pass

        all_matches.sort(
            key=lambda x: x["match"].get("match_score", 0),
            reverse=True
        )

        top_matches = all_matches[:5]

        st.session_state.candidate = candidate
        st.session_state.analysis = analysis
        st.session_state.top_matches = top_matches
        st.session_state.best_job = top_matches[0]["job"] if top_matches else None
        st.session_state.best_match = top_matches[0]["match"] if top_matches else None

    if st.session_state.candidate is None:
        return

    candidate = st.session_state.candidate
    analysis = st.session_state.analysis
    top_matches = st.session_state.top_matches
    best_job = st.session_state.best_job
    best_match = st.session_state.best_match

    # ─── Top Matching Jobs ───
    if top_matches:
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
    else:
        st.info("ℹ️ No Job Descriptions found in the database — job matching skipped. Upload a job description to enable matching.")

    # ─── Analysis Results ───
    st.divider()
    st.subheader("📝 Candidate Summary")
    with st.container(border=True):
        st.write(analysis.candidate_summary or "No summary available.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💪 Strengths")
        if analysis.strengths:
            for strength in analysis.strengths:
                st.success(f"✔ {strength}")
        else:
            st.info("No strengths identified.")

    with col2:
        st.subheader("⚠️ Weaknesses")
        if analysis.weaknesses:
            for weakness in analysis.weaknesses:
                st.warning(f"• {weakness}")
        else:
            st.success("No weaknesses identified 🎉")

    st.divider()
    st.subheader("🎯 Recommendation")

    if analysis.recommendation == "Shortlist":
        st.success("🟢 SHORTLIST")
    elif analysis.recommendation == "Hold":
        st.warning("🟡 HOLD")
    else:
        st.error("🔴 REJECT")

    # ─── Best Matching Job ───
    if best_job and best_match:
        st.divider()
        st.subheader("🏆 Best Matching Job")
        st.success(f"{best_job['job_title']} | {best_job['company']}")
        st.metric("Match Score", f"{best_match['match_score']}%")

    # ─── Save Candidate ───
    st.divider()
    if st.button("💾 Save Candidate", use_container_width=True):
        try:
            save_resp = requests.post(
                f"{BACKEND_URL}/candidates",
                json=candidate.model_dump(),
                timeout=10
            )
            if save_resp.status_code == 200:
                candidate_id = save_resp.json().get("id")
                st.success(f"✅ Candidate saved successfully (ID: {candidate_id})")
            else:
                st.warning(f"⚠️ {save_resp.json().get('detail', 'Failed to save')}")
        except Exception as e:
            st.error(f"Error saving candidate: {e}")