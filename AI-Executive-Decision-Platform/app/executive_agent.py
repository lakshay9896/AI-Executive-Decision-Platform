import streamlit as st
import joblib
import pandas as pd
import numpy as np

# --------------------------------------------------
# Corporate Styling (Must be included per page)
# --------------------------------------------------

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

.icon {
    font-size: 35px;
    margin-bottom: 10px;
}

h1 {
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Page Title
# --------------------------------------------------

st.title("📊 Executive Overview")
st.markdown("Strategic snapshot of business performance")

st.markdown("---")

# --------------------------------------------------
# Load Models
# --------------------------------------------------

revenue_model = joblib.load("../models/revenue_model.pkl")
churn_model = joblib.load("../models/churn_model.pkl")
profit_model = joblib.load("../models/profit_model.pkl")

# --------------------------------------------------
# Revenue Forecast
# --------------------------------------------------

monthly_df = pd.read_csv("../data/monthly_summary.csv")

monthly_df["lag_1"] = monthly_df["revenue"].shift(1)
monthly_df["lag_2"] = monthly_df["revenue"].shift(2)
monthly_df["lag_3"] = monthly_df["revenue"].shift(3)
monthly_df = monthly_df.dropna()

last_3 = monthly_df["revenue"].values[-3:]
future_preds = []

for _ in range(3):
    input_data = np.array(last_3[-3:]).reshape(1, -1)
    next_pred = revenue_model.predict(input_data)[0]
    future_preds.append(float(next_pred))
    last_3 = np.append(last_3, next_pred)

# --------------------------------------------------
# Churn Risk
# --------------------------------------------------

customers = pd.read_csv("../data/customers.csv")
customers_model = customers.drop("customer_id", axis=1)
customers_model = pd.get_dummies(customers_model, columns=["region"], drop_first=True)

X_customers = customers_model.drop("churn_flag", axis=1)
churn_probs = churn_model.predict_proba(X_customers)[:, 1]
high_risk = int((churn_probs > 0.7).sum())

# --------------------------------------------------
# Profit
# --------------------------------------------------

transactions = pd.read_csv("../data/transactions.csv")
base_input = transactions[["price","discount","marketing_spend","quantity"]].mean().values.reshape(1,-1)
base_profit = float(profit_model.predict(base_input)[0])

# --------------------------------------------------
# Animated KPI Cards
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="icon">📈</div>
        <h3>Next Month Forecast</h3>
        <h2>₹{future_preds[0]:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="icon">⚠️</div>
        <h3>High-Risk Customers</h3>
        <h2>{high_risk}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="icon">💰</div>
        <h3>Base Profit</h3>
        <h2>₹{base_profit:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.success("Executive snapshot generated successfully.")
st.write("DEBUG: Data Loaded Successfully")
st.write("Future Predictions:", future_preds)
st.write("High Risk:", high_risk)
st.write("Base Profit:", base_profit)