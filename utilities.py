import os, json, chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from dotenv import load_dotenv, find_dotenv, set_key
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title
from unstructured.cleaners.core import clean
from filelock import FileLock
import toml


# .env file interaction
def create_env_if_not_exists():
    if not os.path.exists(".env"):
        with open(".env", "w") as file:
            file.write("GOOGLE_API_KEY=''")


def get_google_key() -> str | None:
    load_dotenv(".env")
    return os.getenv("GOOGLE_API_KEY")


def set_google_key(value: str):
    path = find_dotenv()
    load_dotenv()
    set_key(path, "GOOGLE_API_KEY", value)


# toml file interaction
def get_config():
    with open("config.toml", "r") as f:
        config = toml.load(f)
    return config


def update_config(
    name=None,
    system_instruction=None,
    temperature=None,
    google_search=None,
    google_maps=None,
    url_context=None,
):
    new_config = {
        "model_parameters": {
            "name": name,
            "system_instruction": system_instruction,
            "temperature": temperature,
        },
        "tools": {
            "google_search": google_search,
            "google_maps": google_maps,
            "url_context": url_context,
        },
    }
    with open("config.toml", "r") as f:
        config = toml.load(f)

    for key, subdict in config.items():
        for subkey, _ in subdict.items():
            if new_config[key][subkey] is not None:
                config[key][subkey] = new_config[key][subkey]

    with open("config.toml", "w") as f:
        toml.dump(config, f)


def config_set_default():
    default_config = {
        "model_parameters": {
            "name": "gemini-2.5-flash",
            "system_instruction": "",
            "temperature": 1.0,
        },
        "tools": {"google_search": False, "google_maps": False, "url_context": False},
    }

    with open("config.toml", "w") as f:
        toml.dump(default_config, f)


# working with embeddings
content_types = {".pdf": "application/pdf", ".md": "text/markdown"}


def parse_file(file: str) -> list[str]:
    path = os.path.join("storage/input", file)

    if not os.path.exists(path):
        raise FileNotFoundError()
    _, file_extension = os.path.splitext(path)

    if file_extension in content_types.keys():
        elements = partition(filename=path, content_type=content_types[file_extension], strategy="fast")
    else:
        elements = partition(filename=path, content_type="text/plain", strategy="fast")
    chunks = chunk_by_title(elements, max_characters=150)

    os.remove(path) # file copies are temporarily stored in "input"
    return [clean(str(chunk), extra_whitespace=True) for chunk in chunks]


def add_to_collection(chunks, name):
    client = chromadb.PersistentClient(path="storage/chroma_db")

    collection_name = os.path.splitext(name)[0]

    if collection_name in [
        collection.name for collection in client.list_collections()
    ]:  # files with the same name aren't supported
        raise ValueError("Files with the same name not allowed")
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        ),
    )
    collection.add(documents=chunks, ids=[f"id{i}" for i in range(len(chunks))])


def remove_collection(name):
    client = chromadb.PersistentClient(path="storage/chroma_db")
    collection_name = os.path.splitext(name)[0]

    client.delete_collection(collection_name)


def list_collection_names():
    client = chromadb.PersistentClient(path="storage/chroma_db")
    return [collection.name for collection in client.list_collections()]


def get_context(query, collection_name, n_results=3):
    """Retrieve context based on one collection"""
    client = chromadb.PersistentClient(path="storage/chroma_db")
    collection = client.get_collection(collection_name)
    results = collection.query(query_texts=[query], n_results=n_results)
    return "\n".join(results["documents"][0]) + "\n"


# saving conversation history
def read_history(path="storage/history.json"):
    """Read history JSON file via json.load()"""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def add_to_history(text, role, path="storage/history.json"):
    """Add role and text to history JSON file in format
    appropriate for gemini API"""
    lock = FileLock(path + ".lock")
    with lock:
        cur_history = read_history(path)
        cur_history.append({"role": role, "parts": [{"text": text}]})
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                cur_history, f, ensure_ascii=False, indent=3
            )  # indent is purely cosmetic


def empty_history():
    open("storage/history.json", "w").close()
