from flask import Flask, render_template, jsonify, request
from utilities import read_history, add_to_history, create_env_if_not_exists

app = Flask(__name__)

@app.route("/")
def chat():
    create_env_if_not_exists()
    return render_template("chat.html")
    
@app.get("/dialogue")
def get_messages():
    return jsonify(read_history())

@app.post("/dialogue")
def post_message():
    msg = request.json
    add_to_history(msg)

    #call ai here
    #add_to_history with ai's response
    #dont forget to add exception handling
    #if something goes wrong, suggest to check if api key is correct

    return jsonify({"status":"ok"})


@app.route("/settings")
def settings():
    return render_template("settings.html")


#remove on production
if __name__ == "__main__":
    app.run(debug=True)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True