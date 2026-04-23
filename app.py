import streamlit as st

st.set_page_config(
    page_title="Credit Risk App",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("Credit Risk Prediction System")

# ---------------- INTRO ----------------
st.write("""
This application helps estimate whether a person is likely to repay a loan or may default.

It uses financial information to calculate a risk level and assist in decision-making.
""")

st.divider()

# ---------------- WHAT IS CREDIT RISK ----------------
st.header("What is Credit Risk?")

st.write("""
Credit risk refers to the possibility that a borrower may fail to repay a loan.

Banks and financial institutions evaluate factors such as income,
loan amount, and financial behavior before approving a loan.
""")

st.divider()

# ---------------- WHY IT MATTERS ----------------
st.header("Why is this important?")

st.write("""
Understanding credit risk helps:

- Reduce financial losses for lenders  
- Encourage responsible borrowing  
- Improve decision-making in financial systems  

This tool demonstrates how machine learning can assist in such evaluations.
""")

st.divider()

# ---------------- HOW TO USE ----------------
st.header("How to Use This App")

st.write("""
1. Use the sidebar to go to the **Predict** page  
2. Enter your financial details  
3. Click **Predict Risk**  
4. View your result and explanation  

The result will indicate whether the profile is **High Risk** or **Low Risk**.
""")

st.divider()

# ---------------- NOTE ----------------
st.info("""
This tool is built for educational purposes and should not be used as the sole basis
for real financial decisions.
""")
