from app.rag.vector_store import  ingest_incremental

def update_docs(content: str):
    ingest_incremental([content])
