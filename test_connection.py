from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("CR_DB"))

try:
    client.admin.command("ping")
    print("Connected to MongoDB successfully!")
except Exception as e:
    print("Connection failed!")
    print(e)