from pymongo import MongoClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

# Use .env locally, Streamlit Secrets in deployment
mongo_uri = os.getenv("CR_DB")

if not mongo_uri:
    mongo_uri = st.secrets["CR_DB"]

client = MongoClient(mongo_uri)

db = client["credit_risk_db"]
predictions_collection = db["predictions"]