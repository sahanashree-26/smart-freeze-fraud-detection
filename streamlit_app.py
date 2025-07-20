import streamlit as st
import pandas as pd

# Title
st.title("Smart Freeze Fraud Detection System")

# File uploader
uploaded_file = st.file_uploader("Upload the Transaction Dataset (CSV)", type="csv")

if uploaded_file is not None:
    # Load dataset
    df = pd.read_csv(uploaded_file)

    #  Feature Engineering
    df['Amount/Balance'] = df['TransactionAmount'] / df['AccountBalance']
    df['Time Gap'] = (pd.to_datetime(df['TransactionDate']) - pd.to_datetime(df['PreviousTransactionDate'])).dt.days
    df['High Login Attempts'] = df['LoginAttempts'].apply(lambda x: 1 if x > 3 else 0)

    # Smart Freeze Rule-Based AI
    def smart_freeze(row):
        if (row['Amount/Balance'] > 0.8 and
            row['Time Gap'] < -500 and
            row['High Login Attempts'] == 1):
            return 1  # Fraud
        else:
            return 0  # Legitimate

    df['is_fraud'] = df.apply(smart_freeze, axis=1)

    #  Freeze Feature Simulation
    def freeze_features(row):
        if row['is_fraud'] == 1:
            return ["Transfer Money", "Change Password"]
        else:
            return []

    df['Frozen Features'] = df.apply(freeze_features, axis=1)

    # Display Results
    st.subheader("Preview of Fraud Detection with Smart Freeze")
    st.dataframe(df[['TransactionID', 'is_fraud', 'Frozen Features']].head(10))

    # Alert Message
    if 1 in df['is_fraud'].values:
        st.error("ALERT: Fraudulent transaction detected! Freezing app features.")
    else:
        st.success("All transactions look safe. No freezing needed.")

else:
    st.info("Please upload a transaction dataset (CSV).")
