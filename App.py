import streamlit as st
import pandas as pd
from datetime import datetime

# Title
st.set_page_config(page_title="Smart Freeze Fraud Detection", layout="centered")
st.title("🔒 Smart Freeze: Fraud Detection System")
st.markdown("If fraud is detected, certain app features will be frozen and an alert will be shown.")

# Upload CSV
uploaded_file = st.file_uploader("Upload your fraud transaction dataset (CSV only)", type=["csv"])

if uploaded_file:
    # Load data
    df = pd.read_csv(uploaded_file)

    # --- Preprocessing ---
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])
    df["PreviousTransactionDate"] = pd.to_datetime(df["PreviousTransactionDate"])
    df["Time Gap"] = (df["TransactionDate"] - df["PreviousTransactionDate"]).dt.days
    df["Time Gap"] = df["Time Gap"].apply(lambda x: x if x < 0 else -1)
    df["Amount/Balance"] = df["TransactionAmount"] / df["AccountBalance"]
    df["High Login Attempts"] = df["LoginAttempts"].apply(lambda x: 1 if x > 3 else 0)

    # AI Logic to Detect Fraud ---
    def detect_fraud(row):
        if row["Time Gap"] < -500 or row["Amount/Balance"] > 0.5 or row["High Login Attempts"] == 1:
            return 1
        return 0

    df["is_fraud"] = df.apply(detect_fraud, axis=1)

    # --- Smart Freeze Logic ---
    def freeze_features(row):
        if row["is_fraud"] == 1:
            return ["Transfer Money", "Change Password", "Update KYC"]
        return []

    df["Frozen Features"] = df.apply(freeze_features, axis=1)

    # ---  Display Results ---
    st.success("Dataset processed. Displaying results below:")
    st.dataframe(df[["TransactionID", "is_fraud", "Frozen Features"]].head(10))

    # ---Show Alert and Simulate Freeze ---
    fraud_rows = df[df["is_fraud"] == 1]

    if not fraud_rows.empty:
        st.error("\ud83d\udea8 ALERT: Fraudulent transaction detected! Freezing app features.")
        st.warning("\u26d4 Access to Transfer, Password Change, and KYC is temporarily frozen.")
        st.stop()  

    else:
        st.success("\ud83d\udee1\ufe0f No fraud detected. App features are safe to use.")
