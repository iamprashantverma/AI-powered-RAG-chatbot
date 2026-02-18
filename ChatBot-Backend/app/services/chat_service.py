from langchain_core.runnables import RunnableWithMessageHistory

from app.core.llm import llm
from app.core.prompt import prompt
from app.core.memory import get_session_history

chain = prompt | llm

chatbot = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="input", history_messages_key="history")
