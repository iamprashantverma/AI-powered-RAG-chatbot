from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import run_chat, get_user_history
from app.rag.vector_store import get_retriever
from app.api.deps import get_current_user, get_db
from app.models.user import User

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=dict)
async def chat(req: ChatRequest,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_email = current_user["sub"]

    retriever = get_retriever(k=3)

    docs = retriever.invoke(req.message)
    context = "\n".join(d.page_content for d in docs)

    reply = await run_chat(
        db=db,
        message=req.message,
        context=context,
        user_email=user_email
    )

    return {"reply": reply}


@router.get("", response_model=List[ChatResponse])
async def get_chat_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_history(db, current_user["sub"])