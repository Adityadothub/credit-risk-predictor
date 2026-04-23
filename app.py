import streamlit as st

st.set_page_config(
    page_title="Credit Risk App",
    layout="centered"
)

st.title("Credit Risk Prediction System")

st.write("""
Welcome to the Credit Risk Prediction App.

Use the sidebar to navigate:
- Model Info → Understand the model
- Predict → Run predictions
""")