from langchain_community.document_loaders import TextLoader
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

def load_docs():
    file_path = BASE_DIR / "data" / "docs.txt"
    loader = TextLoader(str(file_path))
    return loader.load()
