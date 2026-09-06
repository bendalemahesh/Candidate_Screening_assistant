import streamlit as st
import pandas as pd
from workflows.dashboard_workflow import dashboard_workflow
def render():
    st.title("👥 Candidate Database")

    search_query = st.text_input("Search", placeholder="Search candidates by candidate id ,name or email")

    response = dashboard_workflow.invoke({

        "dashboard": {}

    })

    data = response["dashboard"]

    if search_query:
        data["candidates"] = [
            c for c in data["candidates"]
            if search_query.lower() in c["full_name"].lower()
            or search_query.lower() in c["email"].lower()
            or search_query.lower() in str(c["id"]).lower()
        ]

    candidate_df = pd.DataFrame([
    {
        "Candidate id": c["id"],
        "Name": c["full_name"],
        "Email": c["email"],
        "Skills": ", ".join(c["skills"][:5])
    }
    for c in sorted(data["candidates"], key=lambda x: x["id"])
    ])
    
    st.dataframe(
        candidate_df,
        use_container_width=True,
        hide_index=True,
    )

    st.metric("Total Candidates", len(data["candidates"]))
