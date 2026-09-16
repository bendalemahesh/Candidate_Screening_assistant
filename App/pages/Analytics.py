import os
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "https://candidate-screening-assistant.onrender.com")


def render():
    st.title("📊 Analytics")

    with st.spinner("Loading analytics..."):
        try:
            response = requests.get(f"{BACKEND_URL}/analytics", timeout=15)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            st.error(f"❌ Could not load analytics. Is the backend running?\n\n`{e}`")
            return

    # ─── Key Metrics ───
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 Total Candidates", data["total_candidates"])
    with col2:
        st.metric("💼 Total Jobs", data["total_jobs"])
    with col3:
        st.metric("📊 Avg Match Score", f"{data['average_match_score']:.2f}%")

    st.divider()

    # ─── Top Skills Chart ───
    top_skills = data.get("top_skills", [])
    if top_skills:
        skills_df = pd.DataFrame(top_skills, columns=["Skill", "Count"])

        st.subheader("🔥 Top Skills")
        fig = px.bar(
            skills_df,
            x="Skill",
            y="Count",
            text="Count",
            color="Count",
            title="Most Common Candidate Skills"
        )
        fig.update_layout(
            xaxis_title="Skills",
            yaxis_title="Candidates",
            template="plotly_dark",
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No skill data available yet. Screen some candidates first.")

    st.divider()

    # ─── Match Score Distribution ───
    match_scores = data.get("match_scores", [])
    if match_scores:
        st.subheader("📈 Match Score Distribution")
        score_df = pd.DataFrame({"Match Score (%)": match_scores})
        fig2 = px.histogram(
            score_df,
            x="Match Score (%)",
            nbins=10,
            title="Candidate Match Score Distribution",
            template="plotly_dark"
        )
        fig2.update_layout(height=350)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ─── Companies ───
    companies = data.get("companies", [])
    if companies:
        st.subheader("🏢 Hiring Companies")
        for company, count in companies:
            st.write(f"**{company}** — {count} job(s)")
    else:
        st.info("No job data available yet.")