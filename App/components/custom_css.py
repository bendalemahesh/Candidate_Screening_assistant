import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        .block-container{
            padding-top:2rem;
            padding-bottom:2rem;
        }

        .sidebar{
            background-color:#6897ea;
            
        }

        div[data-testid="metric-container"]{
            border-radius:12px;
            padding:18px;
            background:#FFFFFF;
            border:1px solid #E5E7EB;
        }

        .stApp {
        background-image: url("https://www.shutterstock.com/search/recruitment-background");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
        </style>
        """,
        unsafe_allow_html=True,
    )