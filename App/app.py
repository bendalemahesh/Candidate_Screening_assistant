from agents import job_description_agent
from database.update_schema import DB_PATH
import os
import streamlit as st
import database.update_schema
from agents.resume_parser_agent import ResumeParserAgent
from components.header import render_header
from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.uploader import render_resume_uploader
from components.footer import render_footer
from components.custom_css import load_css
from services.document_loader_service import get_file_loader
from services.matching_service import MatchingService
from agents.job_description_agent import JobDescriptionAgent

from services.database_service import DatabaseService
from services.batch_maneger_service import BatchManager
from services.document_generator_service import DocumentGenerator
from database.create_tables import create_tables
from pages import (
    Candidate_Screening,
    Candidate_Ranking,
    Upload_Jobs,
    Dashboard,
    Recruiter_ChatBot,
    Candidate_Database,
    Analytics,
    Settings,
    Features,
    About,
)

create_tables()
# Page Configuration
st.set_page_config(
    page_title="Recruiter AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
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

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


</style>
""", unsafe_allow_html=True)
# Sidebar

page = render_sidebar()

if page == "📄 Screen Candidate":
    Candidate_Screening.render()

elif page == "💼 Upload Job Description":
    Upload_Jobs.render()
elif page == "🏆 Candidate Ranking":
    Candidate_Ranking.render()
elif page == "🏠 Dashboard":
    Dashboard.render()

elif page == "💬 Recruiter Chat":
    Recruiter_ChatBot.render()

elif page == "👥 Candidate Database":
    Candidate_Database.render()

elif page == "📊 Analytics":
    Analytics.render()

elif page == "⚙️ Settings":
    Settings.render()

elif page == "✨ Features":
    Features.render()
    
elif page == "ℹ️ About":
    About.render()

# Footer
render_footer()