from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import google.generativeai as genai
import os
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbot.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)

# Configure Gemini API
genai.configure(api_key=os.getenv("MAKERSUITE"))  # Ensure the API key is set in environment variables
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize sentiment analysis tool
analyzer = SentimentIntensityAnalyzer()

# Keywords indicating a user request for human support
TRANSFER_KEYWORDS = ["human support", "talk to an agent", "live agent", "customer service", "speak to a representative"]

# Define the conversation database model
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)

@app.route("/ai")
def chatbot():
    """Serve the frontend HTML page."""
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle user chat requests."""
    data = request.json
    user_message = data.get("message", "").lower()  # Convert to lowercase for keyword matching

    # Perform sentiment analysis
    sentiment_score = analyzer.polarity_scores(user_message)["compound"]

    # Generate AI response using Gemini API
    response = model.generate_content(user_message)
    ai_reply = response.text if response else "Sorry, I couldn't understand your message."


    # **Check if human support is needed**
    if sentiment_score < -0.5 or any(keyword in user_message for keyword in TRANSFER_KEYWORDS):
        ai_reply = "💬 It looks like you may need assistance from a human agent.<br>⏰ Our customer support is available from 9:00 AM to 6:00 PM.<br>You can contact us at (65)12345678"

    # Store the conversation in SQLite
    new_conversation = Conversation(user_message=user_message, bot_response=ai_reply)
    db.session.add(new_conversation)
    db.session.commit()

    return jsonify({"response": ai_reply})

if __name__ == "__main__":
    # Create database if it does not exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)
