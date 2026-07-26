import streamlit as st
from services.database_service import DatabaseService

def render():

    st.title("📧 Candidate Communication")

    db = DatabaseService()


    candidates = db.get_all_candidates()

    candidate = st.selectbox(
        "Select Candidate",
        candidates,
        format_func=lambda x: f"{x['full_name']} ({x['email']})"
    )

    template = st.selectbox(
        "Select Template",
        [
            "Interview Invitation",
            "Shortlisted",
            "Offer Letter",
            "Rejection"
        ]
    )

    st.divider()

    message = ""

    if template == "Interview Invitation":

        message = f"""
    Dear {candidate['full_name']},

    Congratulations!

    You have been shortlisted for the next interview round.

    Interview Date:
    Interview Time:
    Location / Meeting Link:

    Regards,
    HR Team
    """

    elif template == "Shortlisted":

        message = f"""
    Dear {candidate['full_name']},

    Congratulations!

    Based on your profile, you have been shortlisted for the next stage of our hiring process.

    Our HR team will contact you soon.

    Regards,
    HR Team
    """

    elif template == "Offer Letter":

        message = f"""
    Dear {candidate['full_name']},

    Congratulations!

    We are pleased to offer you a position in our company.

    Our HR team will contact you with further details.

    Regards,
    HR Team
    """

    elif template == "Rejection":

        message = f"""
    Dear {candidate['full_name']},

    Thank you for applying.

    After careful review, we have decided to move forward with another candidate.

    We appreciate your interest and wish you success.

    Regards,
    HR Team
    """

    message = st.text_area(
        "Communication Message",
        value=message,
        height=350
    )

    st.download_button(
        "📥 Download Message",
        message,
        file_name="communication.txt"
    )