import streamlit as st
import pandas as pd
from datetime import date, time
from services.database_service import DatabaseService


def render():

    db = DatabaseService()

    st.title("📅 Interview Scheduling")

    candidates = db.get_all_candidates()
    jobs = db.get_all_jobs()

    candidate = st.selectbox(
        "👤 Select Candidate",
        candidates,
        format_func=lambda x: x["full_name"]
    )

    job = st.selectbox(
        "💼 Select Job",
        jobs,
        format_func=lambda x: f"{x['job_title']} | {x['company']}"
    )

    interview_date = st.date_input(
        "📅 Interview Date",
        value=date.today()
    )

    interview_time = st.time_input(
        "⏰ Interview Time",
        value=time(10, 0)
    )

    interviewer = st.text_input(
        "👨‍💼 Interviewer Name"
    )

    meeting_link = st.text_input(
        "🔗 Meeting Link / Location"
    )

    notes = st.text_area(
        "📝 Notes"
    )

    if st.button(
        "📅 Schedule Interview",
        use_container_width=True
    ):
        st.success("Interview Scheduled Successfully ✅")