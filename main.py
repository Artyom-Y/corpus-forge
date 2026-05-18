from flask import Flask, render_template, jsonify, request
from utilities import read_history, add_to_history

app = Flask(__name__)

@app.route("/")
def chat():
    return render_template("chat.html")
    
@app.get("/dialogue")
def get_messages():
    return jsonify(read_history())

@app.post("/dialogue")
def post_message():
    msg = request.json
    add_to_history(msg)



#remove on production
if __name__ == "__main__":
    app.run(debug=True)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True