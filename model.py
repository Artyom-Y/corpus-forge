#add ai interaction with gemini
#when calling the model taking config.toml, RAG and chat history into account

from google import genai
from utilities import get_google_key, read_history
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

def get_chat():
    client = genai.Client(api_key=get_google_key())
    history = read_history()
    model = config["model_parameters"]["name"]
    chat = client.chats.create(model=model, history=history)
    
    