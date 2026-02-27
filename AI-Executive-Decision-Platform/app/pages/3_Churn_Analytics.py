#page 3
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

from ui_theme import apply_corporate_theme
apply_corporate_theme()
st.title("Churn Analytics")

churn_model = joblib.load("../models/churn_model.pkl")

customers = pd.read_csv("../data/customers.csv")
customers_model = customers.drop("customer_id", axis=1)
customers_model = pd.get_dummies(customers_model, columns=["region"], drop_first=True)

X_customers = customers_model.drop("churn_flag", axis=1)
churn_probs = churn_model.predict_proba(X_customers)[:,1]

customers["churn_probability"] = churn_probs

fig = px.histogram(customers, x="churn_probability", nbins=20)
avg_churn = customers["churn_probability"].mean()
high_risk_pct = (customers["churn_probability"] > 0.7).mean() * 100

col1, col2 = st.columns(2)
col1.metric("Average Churn Risk", f"{avg_churn:.2%}")
col2.metric("High Risk %", f"{high_risk_pct:.1f}%")
st.plotly_chart(fig, use_container_width=True)