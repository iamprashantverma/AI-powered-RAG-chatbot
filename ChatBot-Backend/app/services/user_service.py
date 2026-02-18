from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.user import UserCreate
from app.models.user import User
from app.crud.user import ( get_user_by_email, create_user )
from app.core.security import hash_password


def create_user_service(db: Session, user: UserCreate) -> User:
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    db_user = User( name=user.name, email=user.email, hashed_password=hash_password(user.password))

    return create_user(db, db_user)


def get_user_service(db: Session, email: str) -> User | None:
    return get_user_by_email(db, email)



