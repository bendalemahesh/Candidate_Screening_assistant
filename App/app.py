from sympy import true
import os
import streamlit as st
from dotenv import load_dotenv
if true:
    from App.database.create_tables import create_tables
else:
    from database.create_tables import create_tables

from App.components.sidebar import render_sidebar
from App.components.footer import render_footer
from App.components.custom_css import load_css

# Import pages
from pages import (
    Candidate_Screening,
    Candidate_Ranking,
    Upload_Jobs,
    Dashboard,
    Recruiter_ChatBot,
    Candidate_Database,
    Analytics,
    Features,
    About,
)
from pages import interview
from pages import communication
from pages import Settings

# Initialise DB tables on startup
load_dotenv()
create_tables()

# Page Configuration
st.set_page_config(
    page_title="Recruiter AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<h1 style="text-align:center;color:white;">
🤖 Recruiter AI Assistant
</h1>

<p style="text-align:center;color:gray;">
AI Powered Resume Screening System
</p>
""", unsafe_allow_html=True)

st.divider()

# Load Custom CSS
load_css()

st.markdown("""
<style>
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Sidebar — returns selected page
page = render_sidebar()

if page == "🏠 Dashboard":
    Dashboard.render()

elif page == "📄 Screen Candidate":
    Candidate_Screening.render()

elif page == "💼 Upload Job Description":
    Upload_Jobs.render()

elif page == "🏆 Candidate Ranking":
    Candidate_Ranking.render()

elif page == "👥 Candidate Database":
    Candidate_Database.render()

elif page == "📅 Interview Scheduling":
    interview.render()

elif page == "📧 Communication":
    communication.render()

elif page == "📊 Analytics":
    Analytics.render()

elif page == "💬 Recruiter Chat":
    Recruiter_ChatBot.render()

elif page == "✨ Features":
    Features.render()

elif page == "⚙️ Settings":
    Settings.render()

elif page == "ℹ️ About":
    About.render()

# Footer
render_footer()