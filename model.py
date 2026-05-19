#add ai interaction with gemini
#when calling the model taking config.toml, RAG and chat history into account

from google import genai
from google.genai import types
from utilities import get_google_key, read_history
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

model = config["model_parameters"]["name"]
system_instruction = config["model_parameters"]["system_instruction"]

all_tools = {
"grounding_tool": types.Tool(google_search=types.GoogleSearch()),
"google_maps_tool": types.Tool(google_maps=types.GoogleMaps()),
"url_context_tool": types.Tool(url_context=types.UrlContext())
}

def get_chat():
    client = genai.Client(api_key=get_google_key())
    history = read_history()
    tools = [tool for name, tool in all_tools.items() if config["tools"][name]]
    chat = client.chats.create(model=model, history=history)
    
    
    