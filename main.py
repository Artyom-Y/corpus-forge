import os
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
from utilities import (
    read_history,
    add_to_history,
    create_env_if_not_exists,
    get_config,
    parse_file,
    add_to_collection,
    list_collection_names,
    remove_collection
)
from model import AIModel

app = Flask(__name__)

# remove on production
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

gemini = AIModel()
UPLOAD_FOLDER = "storage/input"


@app.route("/")
def home():
    create_env_if_not_exists()
    return render_template("chat.html")

@app.route("/settings", methods = ["GET", "POST"])
def settings():
    if request.method == "POST":
        # TODO: try update_config() if an error occurs,
        # redirect back to settings page with an error message.
        # else go back to root
        pass
    
    config = get_config()
    # TODO: pass the config and parse it using jinja
    return render_template("settings.html")

@app.get("/history")
def get_messages():
    return jsonify(read_history())

@app.post("/dialogue")
def post_message():
    data = request.json
    # don't do anything if AI is thinking!

    user_prompt = data.get("prompt")
    collections = data.get("collections_names", [])

    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    add_to_history(user_prompt, "user")

    # TODO: call ai here (the post request should contain name files to include in context)
    # add_to_history with ai's response
    # dont forget to add exception handling
    # if something goes wrong, suggest to check if api key is correct
    try:
        ai_text = gemini.generate_response(user_prompt, collections)
        add_to_history(ai_text, "model")

        return jsonify({"reply": ai_text})
    
    except Exception as e:
        error_message = str(e)
        print(f"AI Error: {error_message}")

        if "API_KEY_INVALID" in error_message:
            return jsonify({"error": "Failed to connect. Please check if your API key in config is correct."}), 500
        
    return jsonify({"error": "The AI encountered an error while thinking."}), 500

@app.post("/add_file")
def add_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
            chunks = parse_file(filename)
            add_to_collection(chunks, filename)
        except FileNotFoundError:
            return jsonify({"error": "Couldn't add file to embeddings - filename not found."}), 500
        except ValueError:
            return jsonify({"error": "Couldn't add file to embeddings - same file names not allowed."}), 500


@app.get("/current_collection")
def show_current_collections():
    return list_collection_names()

@app.post("/delete_collection")
def delete_collection():
    data = request.json
    filename = data.get("filename")
    try:
        remove_collection(filename)
    except:
        return jsonify({"error": "Couldn't remove collection"}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER