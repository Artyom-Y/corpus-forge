# Corpus Forge

Corpus Forge is a Flask web app that lets you chat with Google Gemini, upload documents into a local RAG store, and generate study materials from selected collections.

It is designed as a simple classroom project: the backend handles file ingestion, history, configuration, and AI calls, while the frontend provides a chat view, a file sidebar, and a settings page.

## Features

- Chat with Gemini using conversation history stored on disk.
- Upload documents and turn them into ChromaDB collections.
- Select uploaded collections as context for the next prompt.
- Generate study tools from stored files: quiz, flashcards, and visualization.
- Update model settings from the web UI.
- Track prompt and token usage in the settings page.

## Project Structure

- `main.py` - Flask app and HTTP routes.
- `model.py` - Gemini client wrapper and content generation logic.
- `prompts.py` - prompt templates used for generated tools.
- `utilities.py` - config, `.env`, history, parsing, and ChromaDB helpers.
- `templates/` - HTML templates for the chat, settings, and navigation UI.
- `static/` - CSS and JavaScript assets.
- `storage/input/` - temporary upload location before parsing.
- `storage/output/` - generated HTML files.
- `storage/chroma_db/` - persistent ChromaDB data.
- `storage/history.json` - stored conversation history.
- `config.toml` - model and tool configuration.
- `.env` - Google API key storage.

## How It Works

1. A user uploads a file from the chat page.
2. The backend parses the file into chunks and stores them in ChromaDB as a collection.
3. The user sends a prompt and optionally chooses one or more collections as context.
4. The backend loads the saved chat history, builds a Gemini chat session, and sends the prompt.
5. Gemini replies are saved to `storage/history.json`.
6. For quizzes, flashcards, or visualizations, the app builds a specialized prompt, generates HTML, saves it to `storage/output/`, and exposes it as a downloadable page.

## Requirements

- Python 3.14.5
- A Google API key for Gemini
- A working virtual environment is strongly recommended

## Setup

1. Create and activate a virtual environment.
2. Install the dependencies from `requirements.txt`.
3. Create a `.env` file in the project root with your Gemini API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

4. Review `config.toml` if you want to change the default model or enable tools.

## Run the App

Start the Flask server with:

```bash
python main.py
```

Then open the local address shown in the terminal, usually `http://127.0.0.1:5000`.

## Main Routes

- `/` - chat page.
- `/settings` - update model settings, tools, and API key.
- `/upload` - upload a file into the local RAG store.
- `/dialogue` - send a chat message to Gemini.
- `/history` - return saved chat history.
- `/files` - list stored collections.
- `/files/<filename>/content` - fetch the stored text for a collection.
- `/generate_tool` - generate quiz, flashcards, or visualization HTML.
- `/generated_tools` - list generated HTML files.
- `/storage/output/<filename>` - serve a generated file.
- `/delete_collection` - remove a stored collection.
- `/delete_tool` - remove a generated HTML file.
- `/reset` - clear history and restore the default config.

## Storage Notes

- Uploaded files are saved temporarily in `storage/input/` and removed after parsing.
- Parsed chunks are stored in ChromaDB under `storage/chroma_db/`.
- Generated HTML files are written to `storage/output/`.
- Chat history is stored in `storage/history.json` for reuse in future chat sessions.

## Configuration

`config.toml` controls the Gemini model and enabled tools.

The current configurable options are:

- model name
- system instruction
- temperature
- Google Search tool
- Google Maps tool
- URL context tool

The settings page also shows token count and prompt count so you can monitor usage.

## Notes

- The app uses Flask templates with JavaScript for client-side interaction.
- Generated content is saved as standalone HTML files so it can be opened directly in a browser.
- If a dependency fails to install, check the package versions in `requirements.txt` against your Python environment.
