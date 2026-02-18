from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest
from app.services.chat_service import chatbot
from app.rag.retriever import retriever
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("")
async def chat(req: ChatRequest,current_user: User = Depends(get_current_user)):

    user_email = current_user["sub"]

    docs = retriever.invoke(req.message)
    context = "\n".join(d.page_content for d in docs)

    response = await chatbot.ainvoke(
        {
            "input": req.message,
            "context": context,
        },
        config={
            "configurable": {
                "session_id": user_email
            }
        }
    )

    return {"reply": response.content}
