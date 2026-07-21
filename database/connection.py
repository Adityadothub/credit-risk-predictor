from pymongo import MongoClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

mongo_uri = os.getenv("CR_DB")

if not mongo_uri:
    mongo_uri = st.secrets.get("CR_DB")

if not mongo_uri:
    raise ValueError("MongoDB connection string not found.")

client = MongoClient(mongo_uri)

db = client["credit_risk_db"]
predictions_collection = db["predictions"]