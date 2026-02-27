import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix, r2_score
from ui_theme import apply_corporate_theme
apply_corporate_theme()

st.title("📊 Model Performance & Explainability")
st.markdown("Evaluation metrics and model diagnostics")
st.markdown("---")

# -------------------------------------------------
# Load Models
# -------------------------------------------------
revenue_model = joblib.load("../models/revenue_model.pkl")
churn_model = joblib.load("../models/churn_model.pkl")
profit_model = joblib.load("../models/profit_model.pkl")

# -------------------------------------------------
# Revenue Model Evaluation
# -------------------------------------------------
st.subheader("📈 Revenue Forecast Model")

monthly_df = pd.read_csv("../data/monthly_summary.csv")

monthly_df["lag_1"] = monthly_df["revenue"].shift(1)
monthly_df["lag_2"] = monthly_df["revenue"].shift(2)
monthly_df["lag_3"] = monthly_df["revenue"].shift(3)
monthly_df = monthly_df.dropna()

X_rev = monthly_df[["lag_1","lag_2","lag_3"]]
y_rev = monthly_df["revenue"]

pred_rev = revenue_model.predict(X_rev)

rmse = np.sqrt(mean_squared_error(y_rev, pred_rev))

st.metric("Revenue RMSE", f"{rmse:,.2f}")

fig1 = px.line(
    pd.DataFrame({"Actual": y_rev.values, "Predicted": pred_rev}),
    title="Actual vs Predicted Revenue"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# -------------------------------------------------
# Churn Model Evaluation
# -------------------------------------------------
st.subheader("👥 Churn Prediction Model")

customers = pd.read_csv("../data/customers.csv")
customers_model = customers.drop("customer_id", axis=1)
customers_model = pd.get_dummies(customers_model, columns=["region"], drop_first=True)

X_churn = customers_model.drop("churn_flag", axis=1)
y_churn = customers_model["churn_flag"]

pred_churn = churn_model.predict(X_churn)

accuracy = accuracy_score(y_churn, pred_churn)

st.metric("Churn Model Accuracy", f"{accuracy:.2%}")

cm = confusion_matrix(y_churn, pred_churn)

cm_df = pd.DataFrame(cm, columns=["Predicted 0","Predicted 1"], index=["Actual 0","Actual 1"])

fig2 = px.imshow(cm_df, text_auto=True, title="Confusion Matrix")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -------------------------------------------------
# Profit Model Evaluation
# -------------------------------------------------
st.subheader("💰 Profit Model")

transactions = pd.read_csv("../data/transactions.csv")

X_profit = transactions[["price","discount","marketing_spend","quantity"]]
y_profit = transactions["profit"]

pred_profit = profit_model.predict(X_profit)

r2 = r2_score(y_profit, pred_profit)

st.metric("Profit Model R² Score", f"{r2:.2f}")

# Feature Importance (If XGBoost)
try:
    importance = profit_model.feature_importances_
    feat_df = pd.DataFrame({
        "Feature": X_profit.columns,
        "Importance": importance
    }).sort_values("Importance", ascending=False)

    fig3 = px.bar(feat_df, x="Feature", y="Importance", title="Feature Importance")
    st.plotly_chart(fig3, use_container_width=True)

except:
    st.info("Feature importance not available for this model.")