import os

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBjaVO0GvzUuhN8X6n2nK-zR6NtwCjiQJU")
    # MONGO_URI = "mongodb://mongodb:27017/chatbot_db"
    MONGO_URI = "mongodb://localhost:27017/chatbot_db"
