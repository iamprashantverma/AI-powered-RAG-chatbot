from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.models.user import User


def get_chats_by_user_email(db: Session, email: str):
    return (
        db.query(Chat)
        .join(User)
        .filter(User.email == email and Chat.role != "tool" )
        .all()
    )

def create_chat_by_user_email(
    db: Session,
    email: str,
    role: str,
    content: str
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None  

    chat = Chat(
        role=role,
        content=content,
        user_id=user.id
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def get_last_5_chats_by_user_email(db: Session, email: str):
    chats = (
        db.query(Chat)
        .join(User)
        .filter(User.email == email)
        .order_by(Chat.id.desc()) 
        .limit(5)
        .all()
    )
    return list(reversed(chats))

def delete_chat_by_chat_id(db: Session, chat_id: int):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    
    if not chat:
        return None
    
    db.delete(chat)
    db.commit()
    return chat


    chats = (
        db.query(Chat)
        .join(User)
        .filter(User.email == email)
        .all()
    )

    for chat in chats:
        db.delete(chat)

    db.commit()
    return chats