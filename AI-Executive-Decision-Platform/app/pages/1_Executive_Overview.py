import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.express as px
from ui_theme import apply_corporate_theme
apply_corporate_theme()

# -----------------------------
# Page Title
# -----------------------------
st.title("📊 Executive Overview")
st.markdown("Strategic Snapshot of Business Performance")
st.markdown("---")

# -----------------------------
# Load Models
# -----------------------------
revenue_model = joblib.load("../models/revenue_model.pkl")
churn_model = joblib.load("../models/churn_model.pkl")
profit_model = joblib.load("../models/profit_model.pkl")

# -----------------------------
# Revenue Forecast
# -----------------------------
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

# -----------------------------
# Churn Risk
# -----------------------------
customers = pd.read_csv("../data/customers.csv")
customers_model = customers.drop("customer_id", axis=1)
customers_model = pd.get_dummies(customers_model, columns=["region"], drop_first=True)

X_customers = customers_model.drop("churn_flag", axis=1)
churn_probs = churn_model.predict_proba(X_customers)[:, 1]
high_risk = int((churn_probs > 0.7).sum())

# -----------------------------
# Profit
# -----------------------------
transactions = pd.read_csv("../data/transactions.csv")
base_input = transactions[["price","discount","marketing_spend","quantity"]].mean().values.reshape(1,-1)
base_profit = float(profit_model.predict(base_input)[0])

# -----------------------------
# KPI SECTION
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Next Month Forecast", f"₹{future_preds[0]:,.0f}")
col2.metric("High-Risk Customers", high_risk)
col3.metric("Base Profit", f"₹{base_profit:,.0f}")

st.markdown("---")

# -----------------------------
# Revenue Trend Mini Chart
# -----------------------------
st.subheader("📈 Revenue Forecast Trend")

forecast_df = pd.DataFrame({
    "Month": ["Month 1", "Month 2", "Month 3"],
    "Forecast Revenue": future_preds
})

fig = px.line(
    forecast_df,
    x="Month",
    y="Forecast Revenue",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# -----------------------------
# Executive Insight Section
# -----------------------------
st.subheader("🧠 Executive Insight Summary")

growth_rate = ((future_preds[1] - future_preds[0]) / future_preds[0]) * 100

if growth_rate > 0:
    growth_statement = f"Revenue is projected to grow by approximately {growth_rate:.2f}% in the coming month."
else:
    growth_statement = f"Revenue is projected to decline by approximately {abs(growth_rate):.2f}%."

risk_level = "High" if high_risk > 4000 else "Moderate"

st.info(f"""
• {growth_statement}

• Current churn exposure is categorized as **{risk_level} risk** with {high_risk} customers at risk.

• Base profit level stands at ₹{base_profit:,.0f}, indicating current operational margin position.
""")