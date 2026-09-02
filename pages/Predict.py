import streamlit as st
import joblib
import numpy as np
import os
from datetime import datetime

from auth import require_login, show_logout_button
from ui import apply_custom_style
from database.connection import predictions_collection


# ---------------- AUTHENTICATION ----------------

apply_custom_style()
require_login()
show_logout_button()


# ---------------- PAGE TITLE ----------------

st.title("Credit Risk Prediction")


# ---------------- LOAD MODEL ----------------

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "XGB_credit_model.pkl"
)

model = joblib.load(MODEL_PATH)

st.divider()


# ---------------- CUSTOMER INFORMATION ----------------

st.subheader("Customer Information")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        18,
        100,
        30
    )

    credit_amount = st.number_input(
        "Credit Amount (₹)",
        0,
        100000,
        5000
    )

    duration = st.number_input(
        "Loan Duration (months)",
        1,
        72,
        12
    )


with col2:
    gender = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )

    sex = 0 if gender == "Female" else 1

    job_map = {
        "Unskilled": 0,
        "Skilled": 1,
        "Highly Skilled": 2,
        "Management": 3
    }

    job_name = st.selectbox(
        "Job Type",
        list(job_map.keys())
    )

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

    housing_name = st.selectbox(
        "Housing Status",
        list(housing_map.keys())
    )

    housing = housing_map[housing_name]


    saving_map = {
        "Low": 0,
        "Moderate": 1,
        "High": 2,
        "Very High": 3
    }

    saving_name = st.selectbox(
        "Savings Level",
        list(saving_map.keys())
    )

    saving = saving_map[saving_name]


with col4:

    checking_map = {
        "Low": 0,
        "Moderate": 1,
        "High": 2
    }

    checking_name = st.selectbox(
        "Checking Account",
        list(checking_map.keys())
    )

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

    purpose_name = st.selectbox(
        "Loan Purpose",
        list(purpose_map.keys())
    )

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

    # Probability corresponding to predicted class
    if prediction == 1:
        risk_probability = probability
    else:
        risk_probability = 1 - probability


    # ---------------- SAVE TO MONGODB ----------------

    prediction_data = {
        "user_id": st.session_state.user_id,
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
        "risk_probability": float(risk_probability)
    }

    try:
        predictions_collection.insert_one(prediction_data)

    except Exception:
        st.warning(
            "Prediction completed, but the result could not be saved "
            "to the database. Please try again later."
        )


    # ---------------- RISK ASSESSMENT ----------------

    st.subheader("Risk Assessment")

    risk_percentage = risk_probability * 100

    st.metric(
        "Estimated Risk",
        f"{risk_percentage:.1f}%"
    )

    if prediction == 1:
        st.error("Status: HIGH RISK")
    else:
        st.success("Status: LOW RISK")


    # ---------------- RECOMMENDED MEASURES ----------------

    st.subheader("Recommended Measures")

    measures = []

    if prediction == 1:

        if credit_amount > 5000:
            measures.append(
                "Consider reviewing or reducing the requested loan amount "
                "to limit credit exposure."
            )

        if duration > 24:
            measures.append(
                "Consider evaluating a shorter loan duration to reduce "
                "long-term repayment exposure."
            )

        if saving == 0:
            measures.append(
                "Review the applicant's savings position and overall "
                "financial liquidity before approving the loan."
            )

        if checking == 0:
            measures.append(
                "Evaluate the applicant's available checking-account balance "
                "and short-term repayment capacity."
            )

        if housing == 2:
            measures.append(
                "Consider additional financial stability and affordability "
                "checks for the applicant."
            )

        if not measures:
            measures.append(
                "Perform additional creditworthiness checks before making "
                "a final lending decision."
            )

    else:

        measures.append(
            "The current profile indicates relatively lower risk based "
            "on the information provided."
        )

        measures.append(
            "Continue standard creditworthiness and affordability checks "
            "before making a final lending decision."
        )


    for measure in measures:
        st.write(f"- {measure}")


    st.divider()


    # ---------------- EXPLANATION ----------------

    st.subheader("Why this result?")

    reasons = []

    if credit_amount > 5000:
        reasons.append(
            "The requested loan amount is relatively high and may increase "
            "the borrower's repayment exposure."
        )

    if duration > 24:
        reasons.append(
            "A longer loan duration can increase the period over which "
            "repayment risk is exposed."
        )

    if saving == 0:
        reasons.append(
            "Low savings may indicate limited financial reserves "
            "to handle unexpected expenses."
        )

    if checking == 0:
        reasons.append(
            "Low checking-account balance may indicate limited short-term "
            "liquidity."
        )

    if housing == 2:
        reasons.append(
            "The applicant is renting, which may be considered alongside "
            "other indicators when assessing financial stability."
        )

    if not reasons:
        reasons.append(
            "The provided financial profile does not contain the specific "
            "risk indicators evaluated by this application's rule-based explanation."
        )


    for reason in reasons:
        st.write(f"- {reason}")