from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def chat():
    return render_template("chat.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")


#remove on production
if __name__ == "__main__":
    app.run(debug=True)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True