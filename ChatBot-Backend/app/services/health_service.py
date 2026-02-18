from pathlib import Path
import os
from langchain_community.chat_models import ChatOllama


async def check_ollama():
    try:
        llm = ChatOllama(model=os.getenv("OLLAMA_MODEL", "qwen2.5"))
        await llm.ainvoke("ping")
        return "ok"
    except Exception:
        return "down"


def check_vectordb():
    path = Path(os.getenv("VECTOR_DB_PATH", "vectordb"))
    return "ok" if path.exists() else "missing"


async def get_health_status():
    return {
        "api": "ok",
        "ollama": await check_ollama(),
        "vectordb": check_vectordb()
    }
