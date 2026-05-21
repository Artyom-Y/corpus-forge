from google import genai
from google.genai import types
from utilities import get_google_key, read_history, get_context, parse_file
import toml

class AIModel:
    def __init__(self):
        # Load the config and initialize the client ONCE when the server starts
        with open("config.toml", "r") as f:
            self.config = toml.load(f)

        self.model_name = self.config["model_parameters"]["name"]
        self.system_instruction = self.config["model_parameters"]["system_instruction"]
        self.temperature = self.config["model_parameters"]["temperature"]
        
        self.all_tools = {
            "google_search": types.Tool(google_search=types.GoogleSearch()),
            "google_maps": types.Tool(google_maps=types.GoogleMaps()),
            "url_context": types.Tool(url_context=types.UrlContext())
        }
        
        self.client = genai.Client(api_key=get_google_key()) # ValueError if key is incorrect/not provided

    def get_chat(self):
        # Reads the latest history every time a message is sent
        history = read_history()
        tools = [tool for name, tool in self.all_tools.items() if self.config["tools"][name]]
        
        config_dict = {}
        if len(self.system_instruction) > 0:
            config_dict["system_instruction"] = self.system_instruction
        if tools:
            config_dict["tools"] = tools
            
        model_info = self.client.models.get(model=self.model_name)
        if self.temperature in [0.0, model_info.max_temperature]:
            config_dict["temperature"] = self.temperature
            
        chat_config = types.GenerateContentConfig(**config_dict)
        
        return self.client.chats.create(model=self.model_name, history=history, config=chat_config)

    def generate_response(self, prompt: str, collections_names: list[str]):
        if collections_names:
            context = "Context: \n"
            for collections_name in collections_names:
                context += get_context(prompt, collections_name)
        
            prompt = prompt + "\n" + context

        chat = self.get_chat()
        response = chat.send_message(prompt)
        
        return response.text

    def token_count(self):
        chat = self.get_chat()
        return self.client.models.count_tokens(model=self.model_name, contents = chat.get_history())

    def prompts_count(self):
        count = 0
        history = read_history()
        for msg in history:
            if getattr(msg, 'role', None) == "user" or (isinstance(msg, dict) and msg.get("role") == "user"):
                count += 1
                
        return count