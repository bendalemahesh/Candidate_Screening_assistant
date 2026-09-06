import os
import requests
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from models.candidate_profile_model import (
    CandidateProfile,
    Education,
    Experience,
    Certification,
)

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def _get_jobs():
    try:
        r = requests.get(f"{BACKEND_URL}/jobs", timeout=10)
        return r.json()
    except:
        return []


def _get_candidates():
    try:
        r = requests.get(f"{BACKEND_URL}/candidates", timeout=10)
        return r.json()
    except:
        return []


def _calc_match(candidate_dict, job_dict):
    try:
        r = requests.post(
            f"{BACKEND_URL}/match",
            json={"candidate": candidate_dict, "job": job_dict},
            timeout=10
        )
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return {"match_score": 0, "ats_score": 0, "matched_skills": [], "missing_skills": [], "ats_breakdown": {}}

def dict_to_candidate(data):
    """Convert raw dict from DB/API into CandidateProfile, handling list-of-dicts."""
    return CandidateProfile(
        full_name=data.get("full_name"),
        email=data.get("email"),
        phone=data.get("phone"),
        linkedin=data.get("linkedin"),
        github=data.get("github"),
        skills=data.get("skills", []),
        education=[
            Education(**item) if isinstance(item, dict) else item
            for item in data.get("education", [])
        ],
        experience=[
            Experience(**item) if isinstance(item, dict) else item
            for item in data.get("experience", [])
        ],
        certifications=[
            Certification(**item) if isinstance(item, dict) else item
            for item in data.get("certifications", [])
        ],
        summary=data.get("summary"),
        resume_text=data.get("resume_text", "")
    )

def render():

    st.title("🏆 Candidate Ranking")

    jobs = _get_jobs()
    candidates = _get_candidates()

    if not jobs:
        st.warning("📌 No Job Descriptions found. Please upload a Job Description first.")
        return

    selected_job = st.selectbox(
        "💼 Select Job",
        jobs,
        format_func=lambda job: f"{job.get('job_title','?')} | {job.get('company','?')}"
    )

    highest_score = 0
    if candidates:
        scores = []
        for data in candidates:
            candidate = dict_to_candidate(data)
            match = _calc_match(data, selected_job)
            scores.append(match.get("match_score", 0))
        highest_score = max(scores) if scores else 0

    col1, col2 = st.columns(2)
    col1.metric("👤 Candidates", len(candidates))
    col2.metric("🏆 Highest Score", f"{highest_score}%")

    search = st.text_input("🔍 Search Candidate")
    minimum_score = st.slider("📊 Minimum Match Score", 0, 100, 0)

    ranking = []
    for data in candidates:
        candidate = dict_to_candidate(data)
        match = _calc_match(data, selected_job)
        ranking.append({"candidate": candidate, "data": data, "match": match})

    ranking.sort(key=lambda x: x["match"].get("match_score", 0), reverse=True)

    if search:
        ranking = [item for item in ranking
                   if search.lower() in (item["candidate"].full_name or "").lower()]

    ranking = [item for item in ranking
               if item["match"].get("match_score", 0) >= minimum_score]

    st.divider()
    st.subheader("🏆 Candidate Ranking")

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    csv_data = pd.DataFrame([
        {
            "Rank": i + 1,
            "Candidate": item["candidate"].full_name,
            "Email": item["candidate"].email,
            "Match Score": item["match"].get("match_score", 0),
            "ATS Score": item["match"].get("ats_score", 0),
            "Matched Skills": ", ".join(item["match"].get("matched_skills", [])),
            "Missing Skills": ", ".join(item["match"].get("missing_skills", []))
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

            col_name, col_score, col_ats = st.columns([3, 1, 1])

            with col_name:
                st.markdown(f"### {medal} {candidate.full_name}")
                st.write(f"📧 {candidate.email}")

            with col_score:
                st.metric("Match Score", f"{match.get('match_score', 0)}%")
                st.progress(match.get("match_score", 0) / 100)

            with col_ats:
                ats = match.get('ats_score', 0)
                st.metric("ATS Score", f"{ats}/100")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("✅ Matched Skills")
                if match.get("matched_skills"):
                    for skill in match["matched_skills"]:
                        st.success(skill)
                else:
                    st.info("No matched skills")

            with col2:
                st.subheader("❌ Missing Skills")
                if match.get("missing_skills"):
                    for skill in match["missing_skills"]:
                        st.warning(skill)
                else:
                    st.success("No missing skills 🎉")

            # ATS Breakdown
            ats_breakdown = match.get("ats_breakdown", {})
            if ats_breakdown:
                with st.expander("📊 ATS Score Breakdown *(AI-generated ATS-style score)*"):
                    for key, val in ats_breakdown.items():
                        st.write(f"**{key}:** {val}/100")
                        st.progress(min(val, 100) / 100)

            st.divider()

            with st.expander(f"👁 View {candidate.full_name} Profile"):

                st.subheader("👤 Personal Information")
                st.write(f"**Name:** {candidate.full_name}")
                st.write(f"**Email:** {candidate.email}")
                st.write(f"**Phone:** {candidate.phone}")

                st.divider()
                st.subheader("🛠 Skills")
                for skill in candidate.skills:
                    st.markdown(f"- {skill}")

                st.divider()
                st.subheader("🎓 Education")
                for edu in candidate.education:
                    st.markdown(f"""
                    **Degree:** {edu.degree}  
                    **Branch:** {edu.branch}  
                    **College:** {edu.college}  
                    **Duration:** {edu.start_year} - {edu.end_year}
                    """)

                st.divider()
                st.subheader("💼 Experience")
                if candidate.experience:
                    for exp in candidate.experience:
                        st.markdown(f"""
                        **Company:** {exp.company}  
                        **Designation:** {exp.designation}  
                        **Duration:** {exp.duration}  
                        **Description:** {exp.description}
                        """)
                else:
                    st.info("No experience available.")

                st.divider()
                st.subheader("📜 Certifications")
                if candidate.certifications:
                    for cert in candidate.certifications:
                        st.markdown(f"- **{cert.name}** ({cert.issuer})")
                else:
                    st.info("No certifications available.")

                st.divider()
                st.subheader("📝 Summary")
                st.write(candidate.summary)