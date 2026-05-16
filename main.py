from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def chat():
    return render_template("chat.html")