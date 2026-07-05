import streamlit as st

from components.header import render_header
from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.uploader import render_uploader
from components.footer import render_footer
from components.custom_css import load_css


# Page Configuration
st.set_page_config(
    page_title="Recruiter AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load Custom CSS
load_css()

# Sidebar

render_sidebar()

# Header
render_header()

# Dashboard Metrics
render_metrics()

# Resume Upload Section
resume, job_description, screen = render_uploader()

# Placeholder Logic
if screen:
    if resume is None:
        st.warning("Please upload a resume.")
    elif job_description.strip() == "":
        st.warning("Please enter a Job Description.")
    else:
        st.success("✅ submitted")
        st.info("AI-powered candidate screening will be implemented in next submission.")

# Footer
render_footer()

