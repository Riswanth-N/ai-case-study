import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(MONGO_URI)

db = client[MONGO_DB_NAME]


def check_database_connection():
    try:
        client.admin.command("ping")
        print("Successfully connected to MongoDB Atlas!")

    except Exception as error:
        print("MongoDB connection failed:")
        print(error)