import streamlit as st



st.title("Model Information")

st.write("""
This model predicts credit risk using financial and personal attributes.
It is built using a machine learning algorithm (XGBoost).
""")

st.divider()

# ---------------- DATASET ----------------
st.header("Dataset")

st.write("""
The dataset includes financial and demographic information such as:
- Age
- Credit amount
- Loan duration
- Employment type
- Housing status
- Savings and checking account details
""")

st.divider()

# ---------------- FEATURES ----------------
st.header("Features Used")

st.write("""
- Age → Applicant's age  
- Credit Amount → Loan size  
- Duration → Loan repayment period  
- Job → Skill level of employment  
- Housing → Living condition  
- Savings → Savings level  
- Checking Account → Account balance status  
- Purpose → Reason for loan  
""")

st.divider()

# ---------------- ENCODING ----------------
st.header("How Inputs Are Interpreted")

st.write("Categorical inputs are converted into numerical values for the model.")

st.subheader("Gender")
st.write("Female → 0 | Male → 1")

st.subheader("Housing")
st.write("Free → 0 | Own → 1 | Rent → 2")

st.subheader("Savings")
st.write("Low → 0 | Moderate → 1 | High → 2 | Very High → 3")

st.subheader("Checking Account")
st.write("Low → 0 | Moderate → 1 | High → 2")

st.subheader("Job Type")
st.write("Unskilled → 0 | Skilled → 1 | Highly Skilled → 2 | Management → 3")

st.subheader("Purpose")
st.write("Business → 0 | Car → 1 | Appliances → 2 | Education → 3 | Furniture → 4 | Electronics → 5 | Repairs → 6 | Other → 7")

st.divider()

# ---------------- MODEL ----------------
st.header("Model Details")

st.write("""
- Algorithm: XGBoost Classifier  
- Output: Probability of default  
- Goal: Classify whether a customer is high or low risk  
""")

st.divider()

# ---------------- DISCLAIMER ----------------
st.warning("""
This model provides an estimated risk score and should not be used as the sole basis for financial decisions.
""")