#page 4
import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px
from ui_theme import apply_corporate_theme
apply_corporate_theme()

st.title("Profit Simulation")

profit_model = joblib.load("../models/profit_model.pkl")

marketing_increase = st.slider("Marketing Increase (%)", 0, 30, 10) / 100

transactions = pd.read_csv("../data/transactions.csv")
base_input = transactions[["price","discount","marketing_spend","quantity"]].mean().values.reshape(1,-1)

base_profit = float(profit_model.predict(base_input)[0])

scenario = base_input.copy()
scenario[0][2] *= (1 + marketing_increase)

new_profit = float(profit_model.predict(scenario)[0])

profit_df = pd.DataFrame({
    "Scenario": ["Current", f"Marketing +{int(marketing_increase*100)}%"],
    "Profit": [base_profit, new_profit]
})

fig = px.bar(profit_df, x="Scenario", y="Profit")
roi = ((new_profit - base_profit) / base_profit) * 100

st.metric(
    "Profit Change",
    f"{roi:.2f}%",
    delta=f"₹{(new_profit-base_profit):,.0f}"
)
st.plotly_chart(fig, use_container_width=True)