import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from utilities import (
    read_history,
    add_to_history,
    create_env_if_not_exists,
    get_google_key,
    set_google_key,
    get_config,
    update_config,
    config_set_default,
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

@app.post("/")
def add_file():
    file_error = ""
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
            chunks = parse_file(filename)
            add_to_collection(chunks, filename)
        except FileNotFoundError:
            file_error = "Couldn't add file to embeddings - filename not found."
        except ValueError:
            file_error = "Couldn't add file to embeddings - same file names not allowed."
    return redirect(url_for('/', file_error=file_error))

@app.get("/current_collection")
def show_current_collections():
    return jsonify(list_collection_names())


@app.post("/delete_collection")
def delete_collection():
    filename = request.form.get("file")
    try:
        remove_collection(filename)
    except:
        return jsonify({"error": "Couldn't remove collection"}), 500


@app.route("/settings", methods = ["GET", "POST"])
def settings():
    settings_error = ""
    config = get_config()
    google_api_key = get_google_key()
    if request.method == "POST":
        new_config = request.form.to_dict()
        new_google_api_key = new_config.pop("google_api_key")
        try:
            new_config["temperature"] = float(new_config["temperature"])
            new_config["google_search"] = "google_search" in request.form
            new_config["google_maps"] = "google_maps" in request.form
            new_config["url_context"] = "url_context" in request.form
            update_config(**new_config)
            config = get_config()
            set_google_key(new_google_api_key)
            google_api_key = new_google_api_key
        except:
            settings_error = "Couldn't update"
    
    
    return render_template("settings.html", config = config, settings_error = settings_error, google_api_key = google_api_key)


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

@app.route("/reset")
def reset():
    if os.path.exists("storage/history.json"):
        os.remove("storage/history.json")
    config_set_default()
    
    

if __name__ == "__main__":
    app.run(debug=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER