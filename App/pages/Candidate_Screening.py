import os
import streamlit as st
from components.uploader import render_resume_uploader
from services.document_loader_service import get_file_loader
from services.matching_service import MatchingService
from services.database_service import DatabaseService
from agents.resume_parser_agent import ResumeParserAgent
from agents.job_description_agent import JobDescriptionAgent

#def candidate_screening():
def render():

    st.title("📄 candidate screening")

    resume, screen = render_resume_uploader()

    if not screen:
        return

    if resume is None:
        st.warning("Please upload a Resume.")
        return

    # ---------------- Save Resume ---------------- #

    os.makedirs(
        "App/uploads/assets/resumes",
        exist_ok=True
    )

    resume_path = os.path.join(
        "App/uploads/assets/resumes",
        resume.name
    )

    with open(resume_path, "wb") as f:
        f.write(resume.getbuffer())

    # ---------------- Extract Resume Text ---------------- #

    resume_docs = get_file_loader(resume_path)

    resume_text = "\n".join(
        doc.page_content
        for doc in resume_docs
    )

    # ---------------- Parse Resume ---------------- #

    resume_agent = ResumeParserAgent()

    with st.spinner("🤖 AI is analyzing the resume..."):

        result = resume_agent.parse_resume(resume_text)

    candidate = result["candidate"]
    analysis = result["analysis"]

    # ---------------- Load Jobs ---------------- #

    db = DatabaseService()

    jobs = db.get_all_jobs()

    if len(jobs) == 0:
        st.warning("No Job Descriptions found. Please upload a Job Description first.")
        st.stop()

    all_matches = []

    for job_data in jobs:

        match = MatchingService.calculate_match(
            candidate,
            job_data
        )

        all_matches.append({
            "job": job_data,
            "match": match
        })

    # Sort matches by score
    all_matches.sort(
        key=lambda x: x["match"]["match_score"],
        reverse=True
    )

    top_matches = all_matches[:5]
    best_job = top_matches[0]["job"]
    best_match = top_matches[0]["match"]


    st.subheader("🎯 Top Matching Jobs")

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    for i, item in enumerate(top_matches):

        current_job = item["job"]
        current_match = item["match"]

        with st.container(border=True):

            st.markdown(
                f"""
    ### {medals[i]} {current_job['job_title']}

    🏢 **{current_job['company']}**

    📊 **Match Score:** {current_match['match_score']}%
    """
            )

            st.progress(current_match["match_score"] / 100)


    # ---------------- Display Results ---------------- #

    st.divider()

    st.subheader("📝 Candidate Summary")

    with st.container(border=True):
        st.write(analysis.candidate_summary)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💪 Strengths")

        for strength in analysis.strengths:
            st.success(f"✔ {strength}")

    with col2:
        st.subheader("⚠️ Weaknesses")

        for weakness in analysis.weaknesses:
            st.warning(f"• {weakness}")

    st.divider()

    st.subheader("🎯 Recommendation")

    if analysis.recommendation == "Shortlist":
        st.success("🟢 SHORTLIST")

    elif analysis.recommendation == "Hold":
        st.warning("🟡 HOLD")

    else:
        st.error("🔴 REJECT")

    st.divider()
    st.subheader("🏆 Best Matching Job")

    st.success(
        f"{best_job['job_title']} | {best_job['company']}"
    )

    st.metric(
        "Match Score",
        f"{best_match['match_score']}%"
    )
    
    # ---------------- Save Candidate ---------------- #

    if st.button("💾 Save Candidate", use_container_width=True):

        db = DatabaseService()

        candidate_id = db.save_candidate(candidate)

        jobs = db.get_all_jobs()
        for job in jobs:
            st.write(job)

        if len(jobs) == 0:
            st.warning("No Job Descriptions found...")
            st.stop()
        for job in jobs:
            st.write(job["job_title"])

        st.success(f"Candidate saved successfully (ID: {candidate_id})")
        st.divider()
        print(jobs)
        db = DatabaseService()

        jobs = db.get_all_jobs()

        print(len(jobs))

        for job in jobs:
            print(job["job_title"], job["company"])

#candidate_screening()