from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


embeddings = HuggingFaceEmbeddings()
persist_dir = "vectordb"


def get_db():
    return Chroma( persist_directory=persist_dir, embedding_function=embeddings )


def ingest_incremental(texts: list[str]):
    db = get_db()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50 )

    documents = [Document(page_content=t) for t in texts]
    chunks = splitter.split_documents(documents)

    db.add_documents(chunks)

def get_retriever(k: int = 3):
    return get_db().as_retriever(search_kwargs={"k": k})