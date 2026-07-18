from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("CR_DB"))

db = client["credit_risk_db"]

predictions_collection = db["predictions"]