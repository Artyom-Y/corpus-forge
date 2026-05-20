#add ai interaction with gemini
#when calling the model taking config.toml, RAG and chat history into account

from google import genai
from google.genai import types
from utilities import get_google_key, read_history, get_context
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


def send_message(prompt: str, collections_names: list[str]):
    if collections_names:
        context = "Context: \n"
        for collections_name in collections_names:
            context += get_context(prompt, collections_name)
    
    prompt = prompt + "\n" + context

    chat = get_chat()
    response = chat.send_message(prompt)
    return response

def token_count(chat):
    client = genai.Client(api_key=get_google_key())
    # client.models.count_tokens()
    chat = get_chat()
    return client.models.count_tokens(model=model, contents=chat.get_history())

def prompts_count():
    count = 0
    history = read_history()

    for msg in history:
        if msg["role"] == "user":
            count += 1

    return count
