from flask import Flask, render_template, request, jsonify
import pymongo
from app.chatbot import get_ai_response
from config import get_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域访问

@app.route("/")
def index():
    """返回前端 HTML 页面"""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """处理用户聊天请求"""
    data = request.json
    user_message = data.get("message", "")

    # 获取 MongoDB 连接
    db = get_db()
    collection = db["conversations"]

    # 通过 Gemini API 获取 AI 回复
    ai_reply = get_ai_response(user_message)

    # 记录对话数据
    collection.insert_one({"user": user_message, "bot": ai_reply})

    return jsonify({"response": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)
