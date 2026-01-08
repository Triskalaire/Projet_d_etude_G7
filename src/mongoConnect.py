import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env
load_dotenv()

# Get MongoDB connection string and database name
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DATABASE_NAME", "bluesky")

# Connect to MongoDB
client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Example: list collections
print("Collections in database:", db.list_collection_names())