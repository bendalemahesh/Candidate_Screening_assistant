import streamlit as st

st.title("📄 Candidate Screening")

resume_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

jd_file = st.file_uploader(
    "Upload Job Description",
    type=["pdf", "docx"]
)

analyze = st.button("Analyze Candidate")

if st.button("Screen Candidate"):
    st.success("Week 1 UI completed. AI Screening will be not added yet they will add in next phase.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Candidate Details")
    st.empty()

with col2:
    st.subheader("Match Score")
    st.empty()

st.subheader("AI Summary")
st.empty()

st.subheader("Recommendation")
st.empty()