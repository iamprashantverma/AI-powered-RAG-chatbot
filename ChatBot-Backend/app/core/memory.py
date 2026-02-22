from langchain_community.chat_message_histories import ChatMessageHistory

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    history = store[session_id]
    history.messages = history.messages[-8:]  
    return history

