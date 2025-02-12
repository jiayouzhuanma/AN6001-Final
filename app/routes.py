from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import google.generativeai as genai
import os

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)  # 允许跨域访问

# 配置 SQLite 数据库
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbot.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化数据库
db = SQLAlchemy(app)

# 配置 Gemini API
genai.configure(api_key=os.getenv("MAKERSUITE"))
model = genai.GenerativeModel("gemini-1.5-flash")

# 定义聊天记录数据表
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)

@app.route("/")
def index():
    """返回前端 HTML 页面"""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """处理用户聊天请求"""
    data = request.json
    user_message = data.get("message", "")

    # 通过 Gemini API 获取 AI 回复
    response = model.generate_content(user_message)
    ai_reply = response.text if response else "抱歉，我无法理解你的问题。"

    # 记录对话数据到 SQLite
    new_conversation = Conversation(user_message=user_message, bot_response=ai_reply)
    db.session.add(new_conversation)
    db.session.commit()

    return jsonify({"response": ai_reply})

if __name__ == "__main__":
    # 创建数据库（如果不存在）
    with app.app_context():
        db.create_all()

    app.run(debug=True)
