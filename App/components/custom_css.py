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

        </style>
        """,
        unsafe_allow_html=True,
    )