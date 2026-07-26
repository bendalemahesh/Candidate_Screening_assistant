import streamlit as st
import pandas as pd
from workflows.dashboard_workflow import dashboard_workflow
def render():
    st.title("👥 Candidate Database")
    
    response = dashboard_workflow.invoke({

        "dashboard": {}

    })

    data = response["dashboard"]
    candidate_df = pd.DataFrame([
        {
            "Name": c["full_name"],
            "Email": c["email"],
            "Skills": ", ".join(c["skills"][:5])
        }
        for c in data["candidates"]
    ])

    st.dataframe(
        candidate_df,
        use_container_width=True,
        hide_index=True
    )