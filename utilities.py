import os
from dotenv import load_dotenv, find_dotenv, set_key

def create_env_if_not_exists():
    if not os.path.exists(".env"):
        with open(".env", 'w') as file:
            file.write("GOOGLE_API_KEY=''")

def get_google_key():
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")

def set_google_key(value):
    path = find_dotenv()
    load_dotenv()
    set_key(path, "GOOGLE_API_KEY", value)