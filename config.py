import os
import pymongo

class Config:
    GEMINI_API_KEY = os.getenv("MAKERSUITE")
    MONGO_URI = os.getenv("MONGO_URI")

def get_db():
    """每个 Gunicorn Worker 进程创建独立的 MongoDB 连接"""
    client = pymongo.MongoClient(Config.MONGO_URI)
    db = client["chatbot_db"]
    return db