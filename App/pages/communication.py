import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

TEMPLATES = {
    "Interview Invitation": """
Dear {name},

We are pleased to inform you that after reviewing your application for the **{job_title}** position at **{company}**, we would like to invite you for an interview.

**Interview Details:**
- Date: {interview_date}
- Time: {interview_time}
- Mode: {interview_mode}
- Interviewer: {interviewer}

Please confirm your availability by replying to this message.

We look forward to speaking with you.

Best Regards,  
{recruiter_name}  
Recruitment Team
""",
    "Shortlist Notification": """
Dear {name},

Congratulations! We are happy to inform you that you have been **shortlisted** for the **{job_title}** position at **{company}**.

Your profile stood out among many applicants and we look forward to the next steps of the process.

We will be in touch soon with further details.

Best Regards,  
{recruiter_name}  
Recruitment Team
""",
    "Rejection Message": """
Dear {name},

Thank you for your interest in the **{job_title}** position at **{company}** and for the time you invested in the application process.

After careful consideration, we regret to inform you that we will not be moving forward with your application at this time.

We appreciate your interest and encourage you to apply for future openings that match your profile.

We wish you the very best in your career journey.

Best Regards,  
{recruiter_name}  
Recruitment Team
""",
    "Follow-up Message": """
Dear {name},

I hope this message finds you well. I am writing to follow up on your application for the **{job_title}** position at **{company}**.

We wanted to update you that your profile is currently under review and we will get back to you as soon as possible.

Thank you for your patience.

Best Regards,  
{recruiter_name}  
Recruitment Team
"""
}


def _get_candidates():
    try:
        r = requests.get(f"{BACKEND_URL}/candidates", timeout=10)
        return r.json()
    except:
        return []


def render():
    st.title("📧 Communication Templates")

    st.info(
        "ℹ️ These templates assist recruiters in communicating with candidates. "
        "They are for copy/download use only — no emails are sent automatically."
    )

    candidates = _get_candidates()

    st.subheader("🔧 Generate Communication")

    col1, col2 = st.columns(2)

    with col1:
        template_type = st.selectbox("📄 Select Template", list(TEMPLATES.keys()))
        recruiter_name = st.text_input("🧑‍💼 Recruiter Name", value="HR Team")
        company = st.text_input("🏢 Company Name", value="")

    with col2:
        if candidates:
            selected_candidate = st.selectbox(
                "👤 Select Candidate",
                [None] + candidates,
                format_func=lambda c: "-- Manual Entry --" if c is None else f"{c.get('full_name', 'Unknown')} ({c.get('email', '')})"
            )
            if selected_candidate:
                name = selected_candidate.get("full_name", "Candidate")
                st.success(f"✅ Using: {name}")
            else:
                name = st.text_input("👤 Candidate Name")
        else:
            selected_candidate = None
            name = st.text_input("👤 Candidate Name")

        job_title = st.text_input("💼 Job Title", value="")

    # Interview fields (only for Interview Invitation)
    interview_date = interview_time = interview_mode = ""
    if template_type == "Interview Invitation":
        st.subheader("📅 Interview Details")
        c1, c2, c3 = st.columns(3)
        with c1:
            interview_date = str(st.date_input("Date"))
        with c2:
            interview_time = str(st.time_input("Time"))
        with c3:
            interview_mode = st.selectbox(
                "Mode",
                ["Video Call", "Phone Call", "In-Person", "Technical Round"]
            )
        interviewer = st.text_input("Interviewer Name")
    else:
        interviewer = ""

    if st.button("⚡ Generate Message", use_container_width=True):
        template = TEMPLATES[template_type]
        try:
            message = template.format(
                name=name or "Candidate",
                job_title=job_title or "the applied position",
                company=company or "our company",
                recruiter_name=recruiter_name or "Recruiter",
                interview_date=interview_date,
                interview_time=interview_time,
                interview_mode=interview_mode,
                interviewer=interviewer
            )
        except KeyError as e:
            message = template  # Fallback raw template

        st.divider()
        st.subheader("📄 Generated Message")
        st.markdown(message)

        st.divider()
        st.download_button(
            "📥 Download Message",
            data=message,
            file_name=f"{template_type.lower().replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.text_area("📋 Copy from here:", value=message, height=300)
        
