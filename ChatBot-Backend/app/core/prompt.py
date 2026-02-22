from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the provided context only when relevant."),
    ("system", "Context:\n{context}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])