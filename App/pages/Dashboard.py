import os
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "https://candidate-screening-assistant.onrender.com")


def render():

    st.title("🏠 Recruiter Dashboard")

    with st.spinner("Loading dashboard data..."):
        try:
            response = requests.get(f"{BACKEND_URL}/dashboard", timeout=15)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            st.error(f"❌ Could not load dashboard data. Is the backend running?\n\n`{e}`")
            st.info("Start the backend with: `uvicorn App.backend.main:app --reload`")
            return

    top_skill = data["skill_names"][0] if data["skill_names"] else "N/A"
    top_company = data["company_names"][0] if data["company_names"] else "N/A"

    skills_df = pd.DataFrame({
        "Skill": data["skill_names"],
        "Count": data["skill_counts"]
    })

    company_df = pd.DataFrame({
        "Company": data["company_names"],
        "Jobs": data["company_counts"]
    })

    st.markdown("## 📊 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Candidates", data["total_candidates"])

    with col2:
        st.metric("💼 Jobs", data["total_jobs"])

    with col3:
        st.metric("🏆 Best Match", f'{data["best_match_score"]}%')

    with col4:
        st.metric("⭐ Top Skill", top_skill)

    st.divider()

    st.subheader("📋 Recent Candidates")

    if data["candidates"]:
        table = [
            {
                "Name": c["full_name"],
                "Email": c["email"],
                "Skills": ", ".join(c["skills"][:5]),
            }
            for c in data["candidates"]
        ]
        st.dataframe(table, use_container_width=True)
    else:
        st.info("No candidates found.")

    st.divider()

    if skills_df.empty:
        st.info("Screen candidates to see skill analytics.")
    else:
        st.subheader("🔥 Top Skills")
        fig_skills = px.bar(
            skills_df,
            x="Skill",
            y="Count",
            color="Count",
            text="Count",
            title="🔥 Most Common Skills"
        )
        fig_skills.update_layout(template="plotly_dark", height=450)

        st.subheader("🏢 Hiring Companies")

        if not company_df.empty:
            fig_company = px.pie(
                company_df,
                names="Company",
                values="Jobs",
                hole=0.5,
                title="🏢 Hiring Companies"
            )
            fig_company.update_layout(template="plotly_dark", height=450)

            left, right = st.columns(2)
            with left:
                st.plotly_chart(fig_skills, use_container_width=True)
            with right:
                st.plotly_chart(fig_company, use_container_width=True)
        else:
            st.plotly_chart(fig_skills, use_container_width=True)

    st.divider()
    st.subheader("🤖 Recruiter Insights")

    if data["skill_names"] and data["company_names"]:
        st.success(f"""
        • Most candidates have **{top_skill}** skill.
        • Current highest candidate-job match score is **{data["best_match_score"]}%**.
        • Company with available jobs: **{top_company}**.
        • Recruiters should prioritize candidates with Python and SQL skills.
        """)
    else:
        st.info("Add Job Descriptions and screen candidates to see insights here.")