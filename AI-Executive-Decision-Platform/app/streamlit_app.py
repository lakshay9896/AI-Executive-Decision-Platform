import streamlit as st

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Executive AI Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Corporate Styling
# --------------------------------------------------
st.markdown("""
<style>

/* Gradient Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827);
    color: white;
}

/* Main container padding */
.block-container {
    padding-top: 2rem;
}

/* Header Styling */
h1 {
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -1px;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #0b1120;
    color: white;
}

/* KPI Card Styling */
.kpi-card {
    background-color: #1f2937;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    transition: transform 0.3s ease;
}

.kpi-card:hover {
    transform: scale(1.05);
}

/* Icons */
.icon {
    font-size: 30px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Landing Page
# --------------------------------------------------

st.markdown("# 🚀 Executive Decision Intelligence Platform")

st.markdown("### Data-Driven Strategic Decision Engine")

st.markdown("---")

col1, col2 = st.columns([2,1])

with col1:
    st.markdown("""
    This platform integrates:

    - 📊 **Revenue Forecasting**
    - 👥 **Customer Churn Prediction**
    - 💰 **Profit Sensitivity Simulation**
    - 🤖 **AI Strategic Advisory Engine**

    Designed for executive-level decision making.
    """)

with col2:
    st.info("""
    **System Flow**

    ML Models  
    ↓  
    Business Metrics  
    ↓  
    Scenario Simulation  
    ↓  
    LLM Strategic Intelligence
    """)

st.markdown("---")
st.success("Use the sidebar to navigate between modules.")