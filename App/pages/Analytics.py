import streamlit as st
import pandas as pd
import plotly.express as px
from workflows.analytics_workflow import analytics_workflow

def render():
    st.title("📊 Analytics")

    response = analytics_workflow.invoke({

        "candidates": [],

        "jobs": [],

        "analytics": {}

    })

    data = response["analytics"]

    skills_df = pd.DataFrame(

    data["top_skills"],

    columns=[

        "Skill",

        "Count"

    ]

)

    # Display key metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Candidates", data["total_candidates"])

    with col2:
        st.metric("Total Jobs", data["total_jobs"])

    with col3:
        st.metric(
            "Average Match Score",
            f"{data['average_match_score']:.2f}"
        )
    
    st.divider()

    st.subheader("🔥 Top Skills")

    # Top skills
    st.subheader("Top Skills")

    fig = px.bar(

    skills_df,

    x="Skill",

    y="Count",

    text="Count",

    title="Most Common Candidate Skills"

    )

    fig.update_layout(

    xaxis_title="Skills",

    yaxis_title="Candidates",

    height=450

    )

    st.plotly_chart(

    fig,

    use_container_width=True

    )
    # Companies with most jobs
    st.subheader("Companies")

    for company, count in data["companies"]:
        st.text(f"{company}: {count} jobs")