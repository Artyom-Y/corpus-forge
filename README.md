# Capstone Project: Corpus Forge

## Project files structure:
- `main.py` - flask app
- `model.py` - interaction with google genai
- `utilities.py` - misc functinos for managing configs and storage

- `templates` - html pages for the app
- `static` - css and javascript
- `storage` - has two subfolders for storing user input (gets parsed into embeddings) and AI's output. The rest of the files may be stored outside of those two folders (like chromadb embeddings file and message history)

config.toml - model configuration file (published to github)
.env - contains an API key (not published)

Python version - 3.14.5