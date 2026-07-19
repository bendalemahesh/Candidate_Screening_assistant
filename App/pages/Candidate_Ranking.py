import streamlit as st

from services.database_service import DatabaseService
from services.matching_service import MatchingService
from models.candidate_profile_model import (
    CandidateProfile,
    Education,
    Experience,
    Certification,
)


def dict_to_candidate(data):

    return CandidateProfile(

        full_name=data["full_name"],
        email=data["email"],
        phone=data["phone"],

        linkedin=data["linkedin"],
        github=data["github"],

        skills=data["skills"],

        education=[
            Education(**item)
            for item in data["education"]
        ],

        experience=[
            Experience(**item)
            for item in data["experience"]
        ],

        certifications=[
            Certification(**item)
            for item in data["certifications"]
        ],

        summary=data["summary"],
        resume_text=data["resume_text"]

    )


def render():

    st.title("🏆 Candidate Ranking")

    db = DatabaseService()

    jobs = db.get_all_jobs()

    candidates = db.get_all_candidates()

    selected_job = st.selectbox(
        "💼 Select Job",
        jobs,
        format_func=lambda job: f"{job['job_title']} | {job['company']}"
    )

    ranking = []

    for data in candidates:

        candidate = dict_to_candidate(data)

        match = MatchingService.calculate_match(
            candidate,
            selected_job
        )

        ranking.append({
            "candidate": candidate,
            "match": match
        })
    # Sort after all candidates are added
    ranking.sort(
        key=lambda x: x["match"]["match_score"],
        reverse=True
    )

    st.divider()
    st.subheader("🏆 Candidate Ranking")

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    for i, item in enumerate(ranking):

        candidate = item["candidate"]
        match = item["match"]

        medal = medals[i] if i < len(medals) else f"{i+1}"

        with st.container(border=True):

            st.markdown(f"### {medal} {candidate.full_name}")

            st.write(f"📧 {candidate.email}")

            st.write(f"📊 Match Score: {match['match_score']}%")

            st.progress(match["match_score"] / 100)

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("✅ Matched Skills")

                if match["matched_skills"]:
                    for skill in match["matched_skills"]:
                        st.success(skill)
                else:
                    st.info("No matched skills")

            with col2:

                st.subheader("❌ Missing Skills")

                if match["missing_skills"]:
                    for skill in match["missing_skills"]:
                        st.warning(skill)
                else:
                    st.success("No missing skills 🎉")