import streamlit as st


def render_metrics():

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Candidates", "157")
    col2.metric("Shortlisted", "25")
    col3.metric("Average Score", "87%")
    col4.metric("Today's Screening", "12")

    st.divider()