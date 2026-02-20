from fastapi import APIRouter, Depends, Request
from app.schemas.chat import ChatRequest
from app.services.chat_service import chatbot, get_user_history
from app.rag.retriever import retriever
from app.api.deps import get_current_user
from app.models.user import User
import asyncio

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("")
async def chat(
    req: ChatRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    user_email = current_user["sub"]

    docs = retriever.invoke(req.message)
    context = "\n".join(d.page_content for d in docs)

    llm_task = asyncio.create_task(
        chatbot.ainvoke(
            {
                "input": req.message,
                "context": context,
                "instruction": "Respond ONLY in valid JSON with keys: steps and final_answer"
            },
            config={
                "configurable": {
                    "session_id": user_email
                }
            }
        )
    )

    while not llm_task.done():
        if await request.is_disconnected():
            llm_task.cancel()
            print(f"LLM stopped — client disconnected for {user_email}")
            return
        await asyncio.sleep(0.1)

    response = await llm_task
    return {"reply": response.content}

@router.get("")
async def get_chat_history(current_user: User = Depends(get_current_user)):
    user_email = current_user["sub"]
    return get_user_history(user_email)