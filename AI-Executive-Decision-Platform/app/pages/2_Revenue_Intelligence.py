#page 2
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import joblib
from ui_theme import apply_corporate_theme
apply_corporate_theme()

st.title("Revenue Intelligence")

revenue_model = joblib.load("../models/revenue_model.pkl")

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

forecast_df = pd.DataFrame({
    "Month": ["Month 1", "Month 2", "Month 3"],
    "Forecast Revenue": future_preds
})

fig = px.line(forecast_df, x="Month", y="Forecast Revenue", markers=True)
#st.plotly_chart(fig, use_container_width=True)
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Revenue Forecast Trend")
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
growth = (future_preds[1] - future_preds[0]) / future_preds[0] * 100
st.metric("Projected Growth", f"{growth:.2f}%")