import streamlit as st
import pandas as pd
import joblib

st.title("Customer Churn Risk Lookup")

model = joblib.load("model.pkl")
df = pd.read_csv("data/rfm_features.csv")

customer_id = st.selectbox("Select Customer ID", df["customer_id"].unique())
row = df[df["customer_id"] == customer_id]

st.write("### Customer RFM Profile")
st.write(row[["frequency", "monetary", "recency_days"]])

X = row[["frequency", "monetary"]]
risk = float(model.predict_proba(X)[0][1])

st.write("### Churn Risk Score")
st.progress(risk)
st.write(f"{risk:.1%} estimated probability of churn")