#add ai interaction with gemini
#when calling the model taking config.toml, RAG and chat history into account

from google import genai
from google.genai import types
from utilities import get_google_key, read_history
import toml

with open("config.toml", "r") as f:
    config = toml.load(f)


model = config["model_parameters"]["name"]
system_instruction = config["model_parameters"]["system_instruction"]
temperature = config["model_parameters"]["temperature"]

all_tools = {
"google_search": types.Tool(google_search=types.GoogleSearch()),
"google_maps": types.Tool(google_maps=types.GoogleMaps()),
"url_context": types.Tool(url_context=types.UrlContext())
}

def get_chat():
    client = genai.Client(api_key=get_google_key()) # ValueError if key is incorrect/not provided
    history = read_history()

    tools = [tool for name, tool in all_tools.items() if config["tools"][name]]
    model_info = client.models.get(model=model)
    config_dict = {}
    if len(system_instruction) > 0:
        config_dict["system_instruction"] = system_instruction
    if tools:
        config_dict["tools"] = tools
    if temperature in [0.0, model_info.max_temperature]:
        config_dict["temperature"] = temperature
    chat_config = types.GenerateContentConfig(**config_dict)
    return client.chats.create(model=model, history=history, config=chat_config)