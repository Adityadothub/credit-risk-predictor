import streamlit as st
import joblib
import numpy as np
from datetime import datetime
from database.connection import predictions_collection

st.title("Credit Risk Prediction")

# Load model
model = joblib.load("XGB_credit_model.pkl")

st.divider()

# ---------------- INPUT ----------------
st.subheader("Customer Information")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 18, 100, 30)
    credit_amount = st.number_input("Credit Amount (₹)", 0, 100000, 5000)
    duration = st.number_input("Loan Duration (months)", 1, 72, 12)

with col2:
    gender = st.selectbox("Gender", ["Female", "Male"])
    sex = 0 if gender == "Female" else 1

    job_map = {
        "Unskilled": 0,
        "Skilled": 1,
        "Highly Skilled": 2,
        "Management": 3
    }
    job_name = st.selectbox("Job Type", list(job_map.keys()))
    job = job_map[job_name]

# ---------------- FINANCIAL DETAILS ----------------
st.subheader("Financial Details")

col3, col4 = st.columns(2)

with col3:
    housing_map = {
        "Free": 0,
        "Own": 1,
        "Rent": 2
    }
    housing_name = st.selectbox("Housing Status", list(housing_map.keys()))
    housing = housing_map[housing_name]

    saving_map = {
        "Low": 0,
        "Moderate": 1,
        "High": 2,
        "Very High": 3
    }
    saving_name = st.selectbox("Savings Level", list(saving_map.keys()))
    saving = saving_map[saving_name]

with col4:
    checking_map = {
        "Low": 0,
        "Moderate": 1,
        "High": 2
    }
    checking_name = st.selectbox("Checking Account", list(checking_map.keys()))
    checking = checking_map[checking_name]

    purpose_map = {
        "Business": 0,
        "Car": 1,
        "Appliances": 2,
        "Education": 3,
        "Furniture": 4,
        "Electronics": 5,
        "Repairs": 6,
        "Other": 7
    }

    purpose_name = st.selectbox("Loan Purpose", list(purpose_map.keys()))
    purpose = purpose_map[purpose_name]

st.divider()

# ---------------- PREDICTION ----------------
if st.button("Predict Risk"):

    features = np.array([[
        age,
        sex,
        job,
        housing,
        saving,
        checking,
        credit_amount,
        duration,
        purpose
    ]])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    # ---------------- SAVE TO MONGODB ----------------
    prediction_data = {
        "timestamp": datetime.now(),
        "age": age,
        "gender": gender,
        "job": job_name,
        "housing": housing_name,
        "saving_level": saving_name,
        "checking_account": checking_name,
        "credit_amount": credit_amount,
        "loan_duration": duration,
        "loan_purpose": purpose_name,
        "prediction": "High Risk" if prediction == 1 else "Low Risk",
        "risk_probability": float(probability)
    }

    try:
        predictions_collection.insert_one(prediction_data)
    except Exception as e:
        st.warning(f"Prediction completed, but database save failed.\n\n{e}")

    # ---------------- RESULT ----------------
    st.subheader("Result")

    if prediction == 1:
        st.error(f"High Credit Risk ({probability * 100:.1f}%)")
    else:
        st.success(f"Low Credit Risk ({(1 - probability) * 100:.1f}%)")

    st.divider()

    # ---------------- EXPLANATION ----------------
    st.subheader("Why this result?")

    reasons = []

    if credit_amount > 5000:
        reasons.append("High loan amount increases risk")

    if duration > 24:
        reasons.append("Long loan duration increases risk")

    if saving == 0:
        reasons.append("Low savings increases risk")

    if checking == 0:
        reasons.append("Low checking balance increases risk")

    if housing == 2:
        reasons.append("Renting may indicate less financial stability")

    if not reasons:
        reasons.append("Financial profile appears stable")

    for reason in reasons:
        st.write(f"- {reason}")