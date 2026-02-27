import streamlit as st

def apply_corporate_theme():
    st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg, #0f172a, #111827);
        color: white;
    }

    .kpi-card {
        background-color: #1f2937;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        transition: transform 0.3s ease;
    }

    .kpi-card:hover {
        transform: scale(1.05);
    }

    .section-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }

    h1 {
        font-weight: 700;
    }

    </style>
    """, unsafe_allow_html=True)