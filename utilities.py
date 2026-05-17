import os
from dotenv import load_dotenv, find_dotenv, set_key
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title
from unstructured.cleaners.core import clean

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

# chunks = parse_file("sample.pdf")
# for chunk in chunks:
#     print(chunk)