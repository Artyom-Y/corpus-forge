import os
from dotenv import load_dotenv, find_dotenv, set_key
from unstructured.partition.auto import partition
import chromadb

# .env file interaction
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

# working with embeddings
content_types = {".pdf": "application/pdf", ".md": "text/markdown"}


def parse_file(file):
    path = os.path.join("storage\input", file)
    _, file_extension = os.path.splitext(path)

    if file_extension in content_types.keys():
        elements = partition(filename=path, content_type=content_types[file_extension])
    else:
        elements = partition(filename=path, content_type="text/plain")
    return elements
