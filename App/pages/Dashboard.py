import streamlit as st
import pandas as pd
import plotly.express as px
from workflows.dashboard_workflow import dashboard_workflow


def render():

    st.title("🏠 Recruiter Dashboard")

    response = dashboard_workflow.invoke({

        "dashboard": {}

    })

    data = response["dashboard"]

    top_skill = (
        data["skill_names"][0]
        if data["skill_names"]
        else "N/A"
    )

    top_company = (
        data["company_names"][0]
        if data["company_names"]
        else "N/A"
    )

    skills_df = pd.DataFrame({

        "Skill": data["skill_names"],

        "Count": data["skill_counts"]

    })

    company_df = pd.DataFrame({
        "Company": data["company_names"],
        "Jobs": data["company_counts"]
    })


    st.markdown("## 📊 Dashboard Overview")

    total_candidates = len(data["candidates"])

    total_jobs = len(data["jobs"])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👥 Candidates",
            data["total_candidates"]
        )

    with col2:
        st.metric(
            "💼 Jobs",
            data["total_jobs"]
        )

    with col3:
        st.metric(
            "🏆 Best Match",
            f'{data["best_match_score"]}%'
        )

    with col4:
        top_skill_label = data["skill_names"][0] if data["skill_names"] else "N/A"
        st.metric(
            "⭐ Top Skill",
            top_skill_label
        )

    st.divider()

    st.subheader("📋 Recent Candidates")

    if data["candidates"]:

        table = []

        for candidate in data["candidates"]:

            table.append({

                "Name": candidate["full_name"],

                "Email": candidate["email"],

                "Skills": ", ".join(candidate["skills"][:5])

            })

        st.dataframe(
            table,
            use_container_width=True
        )


    else:

        st.info("No candidates found.")

    st.divider()

    st.subheader("🔥 Top Skills")

    fig_skills = px.bar(
        skills_df,
        x="Skill",
        y="Count",
        color="Count",
        text="Count",
        title="🔥 Most Common Skills"
    )

    fig_skills.update_layout(
        template="plotly_dark",
        height=450
    )


    st.subheader("🏢 Hiring Companies")

    fig_company = px.pie(
        company_df,
        names="Company",
        values="Jobs",
        hole=0.5,
        title="🏢 Hiring Companies"
    )

    fig_company.update_layout(
        template="plotly_dark",
        height=450
    )

    left, right = st.columns(2)

    with left:
        st.plotly_chart(fig_skills, use_container_width=True)

    with right:
        st.plotly_chart(fig_company, use_container_width=True)


    st.divider()
    st.subheader("🤖 Recruiter Insights")

    if data["skill_names"] and data["company_names"]:
        top_skill = data["skill_names"][0]
        top_company = data["company_names"][0]
        st.success(f"""
        • Most candidates have **{top_skill}** skill.
        • Current highest candidate-job match score is **{data["best_match_score"]}%**.
        • Company with available jobs: **{top_company}**.
        • Recruiters should prioritize candidates with Python and SQL skills.
        """)
    else:
        st.info("Add Job Descriptions and screen candidates to see insights here.")