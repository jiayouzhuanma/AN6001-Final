# api cannot appear in cloud

from flask import Flask
from flask import render_template, request
import textblob
import google.generativeai as genai
import os

# 读取 GitHub Secrets（Repository Secret）
api = os.getenv("MAKERSUITE")

# 确保 Secret 已正确加载
if api:
    print("Successfully retrieved API Key.")
else:
    print("Error: API Key is missing!")

genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask("__name__")    

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    name = request.form.get("q")
    return(render_template("main.html"))

@app.route("/SA",methods=["GET","POST"])
def SA():
    name = request.form.get("q")
    return(render_template("SA.html"))

@app.route("/SA_result",methods=["GET","POST"])
def SA_result():
    q = request.form.get("q")
    r = textblob.TextBlob(q).sentiment
    return(render_template("SA_result.html", r=r))    #frontend和backend命名一致，这样就不需要区分了


@app.route("/genAI",methods=["GET","POST"])
def genAI():
    return(render_template("genAI.html"))


@app.route("/genAI_result",methods=["GET","POST"])
def genAI_result():
    q = request.form.get("q")
    r = model.generate_content(q)

    return(render_template("genAI_result.html", r = r.candidates[0].content.parts[0].text))


@app.route("/paynow",methods=["GET","POST"])
def paynow():
    return(render_template("paynow.html"))


if __name__ == "__main__":
    app.run()










