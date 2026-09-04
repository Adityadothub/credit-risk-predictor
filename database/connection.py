from pymongo import MongoClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

# Try environment variable first
mongo_uri = os.getenv("CR_DB")

# If not found, try Streamlit Secrets
if not mongo_uri:
    try:
        mongo_uri = st.secrets["CR_DB"]
    except (FileNotFoundError, KeyError, st.errors.StreamlitSecretNotFoundError):
        mongo_uri = None

# Stop if no connection string is available
if not mongo_uri:
    raise ValueError(
        "MongoDB connection string not found. "
        "Set CR_DB in your .env file or Streamlit Secrets."
    )

client = MongoClient(mongo_uri)

db = client["credit_risk_db"]

predictions_collection = db["predictions"]
users_collection = db["users"]