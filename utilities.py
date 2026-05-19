import os, json, chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from dotenv import load_dotenv, find_dotenv, set_key
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title
from unstructured.cleaners.core import clean
from filelock import FileLock


# .env file interaction
def create_env_if_not_exists():
    if not os.path.exists(".env"):
        with open(".env", 'w') as file:
            file.write("GOOGLE_API_KEY=''")

def get_google_key() -> str:
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")

def set_google_key(value: str):
    path = find_dotenv()
    load_dotenv()
    set_key(path, "GOOGLE_API_KEY", value)


# working with embeddings
content_types = {".pdf": "application/pdf", ".md": "text/markdown"}

def parse_file(file: str) -> list[str]:
    path = os.path.join("storage\input", file)
    if not os.path.exists(path):
        return 0
    _, file_extension = os.path.splitext(path)
    
    if file_extension in content_types.keys():
        elements = partition(filename=path, content_type=content_types[file_extension])
    else:
        elements = partition(filename=path, content_type="text/plain")
    chunks = chunk_by_title(elements, max_characters=150)
    return [clean(str(chunk), extra_whitespace=True) for chunk in chunks]


def add_to_collection(chunks, name):
    client = chromadb.PersistentClient(path="storage")
    if name in [collection.name for collection in client.list_collections()]: # files with the same name aren't supported
        return 0
    collection = client.get_or_create_collection(name=name, embedding_function=SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2"))
    collection.add(
        documents=chunks,
        ids=[f"id{i}" for i in range(len(chunks))]
    )


#saving conversation history
def read_history(path="storage/history.json"):
    '''Read history JSON file via json.load()'''
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def add_to_history(text, role, path="storage/history.json"):
    '''Add role and text to history JSON file in format 
    appropriate for gemini API'''
    lock = FileLock(path + ".lock")
    with lock:
        cur_history = read_history(path)
        cur_history.append({"role": role, "parts": [text]})
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cur_history, f, ensure_ascii=False, indent=3) # indent is purely cosmetic