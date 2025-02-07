from flask import Flask, render_template, request, jsonify
import pymongo
from app.chatbot import get_ai_response
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域访问

# 连接数据库
client = pymongo.MongoClient(Config.MONGO_URI)
db = client["chatbot_db"]
collection = db["conversations"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    # 通过 Gemini API 获取 AI 回复
    ai_reply = get_ai_response(user_message)

    # 记录对话数据
    collection.insert_one({"user": user_message, "bot": ai_reply})

    return jsonify({"response": ai_reply})
