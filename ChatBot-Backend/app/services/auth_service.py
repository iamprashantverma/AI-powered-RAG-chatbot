from app.schemas.auth import LoginRequest, LoginResponse
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.security import verify_password
from app.crud.user import get_user_by_email
from app.core.security import verify_password
from app.core.jwt import create_access_token  

def login_service(db: Session, login_cred: LoginRequest):
    user = get_user_by_email(db, login_cred.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email"
        )

    if not verify_password(login_cred.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    token = create_access_token(data={"sub": user.email})

    return LoginResponse(
        message=f"Login Successfully {user.email}",
        access_token=token
    )
