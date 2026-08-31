import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# MongoDB Connection
try:
    client = MongoClient(os.getenv("MONGO_URI"))
    client.admin.command('ping')
    print("✅ MongoDB Connected Successfully")

except Exception as e:
    print("❌ MongoDB Connection Failed:", e)
    client = None

# Database + Collections
if client:
    db = client["gyaansetu_db"]
    users = db["users"]

    # Create unique index on email
    users.create_index("email", unique=True)

else:
    db = None
    users = None