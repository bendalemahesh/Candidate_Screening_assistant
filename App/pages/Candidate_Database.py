import os
import requests
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "https://candidate-screening-assistant.onrender.com")


def render():
    st.title("👥 Candidate Database")

    search_query = st.text_input(
        "🔍 Search",
        placeholder="Search candidates by ID, name, or email"
    )

    try:
        response = requests.get(f"{BACKEND_URL}/candidates", timeout=10)
        response.raise_for_status()
        candidates = response.json()
    except Exception as e:
        st.error(f"❌ Could not fetch candidates from backend: {e}")
        return

    if search_query:
        candidates = [
            c for c in candidates
            if search_query.lower() in (c.get("full_name") or "").lower()
            or search_query.lower() in (c.get("email") or "").lower()
            or search_query.lower() in str(c.get("id", "")).lower()
        ]

    if not candidates:
        st.info("No candidates found. Screen and save candidates first.")
        return

    candidate_df = pd.DataFrame([
        {
            "Candidate ID": c["id"],
            "Name": c.get("full_name", "N/A"),
            "Email": c.get("email", "N/A"),
            "Phone": c.get("phone", "N/A"),
            "Skills": ", ".join((c.get("skills") or [])[:5]),
        }
        for c in sorted(candidates, key=lambda x: x["id"])
    ])

    st.dataframe(
        candidate_df,
        use_container_width=True,
        hide_index=True,
    )

    st.metric("Total Candidates", len(candidates))
