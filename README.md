# Capstone Project: Corpus Forge

## Installation
> Python version - 3.14.5
1. Clone the repository
2. Create a virtual environment and run `pip install -r requirements.txt` 
3. Launch flask app: `flask --app main run`, the server will start on http://127.0.0.1:5000 (localhost)

## Using the app
> Note that AI parameters take effect only when launching the app. For them to take effect, you would have to restart the app.
- Go to settings page first and add your google API key (https://aistudio.google.com/app/api-keys)
- Optionally, configure the app to your liking - you can change the model, set the system intstruction, change temperature or enable tools. Among those are google search, google maps and url context (for more info go to https://ai.google.dev/gemini-api/docs/tools)
- In chat.html, you may upload files (.md, .pdf, plain text) to augment your prompts with context
- If you have uploaded any content, you may generate quiz/flashcards or a visualization graph based on your data

## Project files structure:
- `main.py` - flask app
- `model.py` - contains a class for interaction with gemini API
- `utilities.py` - misc functinos for managing configs and storage
- `prompts.py` - helper with AI prompts, chromadb query and prompt making function

- `templates` - html pages for the app
- `static` - css and javascript (async interaction with flask endpoints)
- `storage` - has subfolders for storing temp user input (gets parsed into embeddings), AI's output and chromadb embeddings. `history.json` (AI interaction history) is stored in the top level

- `config.toml` - model configuration file (published to github)
- `.env` - contains an API key (not published)

### Misc
- docs - documentation and presentation for the project
- TODO_archive.txt - TODOs dump