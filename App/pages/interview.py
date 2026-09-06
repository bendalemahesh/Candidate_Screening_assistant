import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def _get_candidates():
    try:
        r = requests.get(f"{BACKEND_URL}/candidates", timeout=10)
        return r.json()
    except:
        return []


def _get_jobs():
    try:
        r = requests.get(f"{BACKEND_URL}/jobs", timeout=10)
        return r.json()
    except:
        return []


def _get_interviews():
    try:
        r = requests.get(f"{BACKEND_URL}/interviews", timeout=10)
        return r.json()
    except:
        return []


def render():
    st.title("📅 Interview Scheduling")

    candidates = _get_candidates()
    jobs = _get_jobs()

    if not candidates:
        st.warning("⚠️ No candidates found. Please screen and save candidates first.")
        return
    if not jobs:
        st.warning("⚠️ No jobs found. Please create a job description first.")
        return

    st.subheader("📝 Schedule New Interview")

    with st.form("interview_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            selected_candidate = st.selectbox(
                "👤 Select Candidate",
                candidates,
                format_func=lambda c: f"{c.get('full_name', 'Unknown')} ({c.get('email', '')})"
            )
            interview_date = st.date_input("📅 Interview Date")
            interviewer = st.text_input("🧑‍💼 Interviewer Name")
            interview_mode = st.selectbox(
                "🖥️ Interview Type",
                ["Video Call", "Phone Call", "In-Person", "Technical Round", "HR Round"]
            )

        with col2:
            selected_job = st.selectbox(
                "💼 Select Job",
                jobs,
                format_func=lambda j: f"{j.get('job_title', '?')} | {j.get('company', '?')}"
            )
            interview_time = st.time_input("⏰ Interview Time")
            meeting_link = st.text_input("🔗 Meeting Link / Location")
            notes = st.text_area("📝 Notes")

        submitted = st.form_submit_button("📅 Schedule Interview", use_container_width=True)

        if submitted:
            if not interviewer:
                st.warning("Please enter the interviewer name.")
            else:
                try:
                    payload = {
                        "candidate_id": selected_candidate["id"],
                        "job_id": selected_job["id"],
                        "interview_date": str(interview_date),
                        "interview_time": str(interview_time),
                        "interviewer": interviewer,
                        "meeting_link": meeting_link,
                        "notes": notes
                    }
                    resp = requests.post(f"{BACKEND_URL}/interviews", json=payload, timeout=10)
                    if resp.status_code == 200:
                        st.success("✅ Interview scheduled successfully!")
                    else:
                        st.error(f"Error: {resp.json().get('detail', 'Failed to schedule.')}")
                except Exception as e:
                    st.error(f"Error communicating with backend: {e}")

    st.divider()
    st.subheader("📋 Upcoming Interviews")

    interviews = _get_interviews()

    if not interviews:
        st.info("No interviews scheduled yet.")
        return

    for interview in interviews:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### 👤 {interview.get('full_name', 'Unknown')}")
                st.write(f"💼 **Job:** {interview.get('job_title', 'N/A')} @ {interview.get('company', 'N/A')}")
                st.write(f"📅 **Date:** {interview.get('interview_date', 'N/A')}  ⏰ **Time:** {interview.get('interview_time', 'N/A')}")
                st.write(f"🧑‍💼 **Interviewer:** {interview.get('interviewer', 'N/A')}")
                if interview.get("meeting_link"):
                    st.write(f"🔗 **Meeting Link:** {interview.get('meeting_link')}")
                if interview.get("notes"):
                    st.caption(f"📝 Notes: {interview.get('notes')}")
            with col2:
                if st.button("🗑️ Cancel", key=f"del_{interview['id']}"):
                    try:
                        del_resp = requests.delete(
                            f"{BACKEND_URL}/interviews/{interview['id']}", timeout=10
                        )
                        if del_resp.status_code == 200:
                            st.success("Interview cancelled.")
                            st.rerun()
                        else:
                            st.error("Failed to cancel interview.")
                    except Exception as e:
                        st.error(f"Error: {e}")
