import streamlit as st
import pandas as pd
from services.database_service import DatabaseService
from services.matching_service import MatchingService
from services.ai_recommendation_service import AIRecommendationService
from agents.candidate_agent import CandidateAgent
from models.candidate_profile_model import (
    CandidateProfile,
    Education,
    Experience,
    Certification,
)


db = DatabaseService()

jobs = db.get_all_jobs()

candidates = db.get_all_candidates()

ai_service = AIRecommendationService()



def generate_ai_recommendation(candidate, job, match):

    return ai_service.generate_recommendation(
        candidate,
        job,
        match
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

    selected_job = st.selectbox(
        "💼 Select Job",
        jobs,
        format_func=lambda job: f"{job['job_title']} | {job['company']}"
    )

    highest_score = 0

    if candidates:
        scores = []

        for data in candidates:
            candidate = dict_to_candidate(data)

            match = MatchingService.calculate_match(
                candidate,
                selected_job
            )

            scores.append(match["match_score"])

        highest_score = max(scores)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "👤 Candidates",
        len(candidates)
    )

    col2.metric(
        "💼 Jobs",
        len(jobs)
    )

    col3.metric(
        "🏆 Highest Score",
        f"{highest_score}%"
    )

    search = st.text_input(
        "🔍 Search Candidate"
    )

    minimum_score = st.slider(
        "📊 Minimum Match Score",
        0,
        100,
        0
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

    # Search Filter
    if search:

        ranking = [

            item

            for item in ranking

            if search.lower() in item["candidate"].full_name.lower()

        ]


    # Minimum Score Filter
    ranking = [

        item

        for item in ranking

        if item["match"]["match_score"] >= minimum_score

    ]

    st.divider()
    st.subheader("🏆 Candidate Ranking")

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    csv_data = pd.DataFrame([

        {
            "Rank": i + 1,
            "Candidate": item["candidate"].full_name,
            "Email": item["candidate"].email,
            "Match Score": item["match"]["match_score"],
            "Matched Skills": ", ".join(item["match"]["matched_skills"]),
            "Missing Skills": ", ".join(item["match"]["missing_skills"])
        }

        for i, item in enumerate(ranking)

    ])
    st.download_button(

                label="📥 Download Ranking CSV",

                data=csv_data.to_csv(index=False),

                file_name="candidate_ranking.csv",

                mime="text/csv",

                use_container_width=True

            )

    for i, item in enumerate(ranking):

        candidate = item["candidate"]
        match = item["match"]

        medal = medals[i] if i < len(medals) else f"{i+1}"

        with st.container(border=True):

            st.markdown(f"### {medal} {candidate.full_name}")

            st.write(f"📧 {candidate.email}")

            st.metric(
                "Match Score",
                f"{match['match_score']}%"
            )

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

            st.divider()

            with st.expander(f"👁 View {candidate.full_name} Profile"):

                st.subheader("👤 Personal Information")

                st.write(f"**Name:** {candidate.full_name}")
                st.write(f"**Email:** {candidate.email}")
                st.write(f"**Phone:** {candidate.phone}")

                st.divider()

                st.subheader("🛠 Skills")

                for skill in candidate.skills:
                    st.markdown(f"### {skill}")

                st.divider()

                st.subheader("🎓 Education")

                for edu in candidate.education:

                    st.markdown(f"""
                    **Degree:** {edu.degree}

                    **Branch:** {edu.branch}

                    **College:** {edu.college}

                    **Duration:** {edu.start_year} - {edu.end_year}
                    """
                )

                st.divider()

                st.subheader("💼 Experience")

                if candidate.experience:

                    for exp in candidate.experience:

                        st.markdown(f"""
                        **Company:** {exp.company}

                        **Designation:** {exp.designation}

                        **Duration:** {exp.duration}

                        **Description:** {exp.description}
                        """
                    )

                else:

                    st.info("No experience available.")

                st.divider()

                st.subheader("📜 Certifications")

                if candidate.certifications:

                    for cert in candidate.certifications:

                        st.markdown(
                            f"- **{cert.name}** ({cert.issuer})"
                        )

                else:

                    st.info("No certifications available.")

                st.divider()

                st.subheader("📝 Summary")

                st.write(candidate.summary)

            with st.expander("🤖 AI Recruiter Recommendation"):

                st.markdown(generate_ai_recommendation(candidate, selected_job, match))